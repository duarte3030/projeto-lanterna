#!/usr/bin/env python3
"""Comprime sprites de overworld (bloco B10 do PRD, "overworld ~330 KB").

O motor já sabe ler gráfico de overworld comprimido: se
`ObjectEventGraphicsInfo.compressed` for TRUE e `OW_GFX_COMPRESS` estiver
ligado (include/config/overworld.h), `LoadSheetGraphicsInfo` carrega a folha
inteira via `LoadCompressedSpriteSheetByTemplate`. Do lado do build, basta
trocar `INCGFX_U32(png, ".4bpp", args)` por `INCGFX_COMP(...)` em
src/data/object_events/object_event_graphics.h: o preproc anexa ".smol" ao
nome do asset e o Makefile (regra genérica `%.smol: %`) gera o arquivo.
Nenhuma regra nova em graphics_file_rules.mk é necessária.

ATENÇÃO (regra da casa, 90_johto_b6.json): marcar `.compressed = TRUE` sem o
asset comprimido TRAVA A ROM NO BOOT. Os dois lados andam juntos, sempre.

Filtro de correção, e o motivo dele: com folha comprimida o índice de frame
da animação vira offset de tile direto na folha
(`sprite.c: tileNum = sheetTileStart + ((imageValue + 1) << sheetSpan)`).
Isso só equivale ao comportamento cru quando a pic table é identidade, ou
seja `overworld_ascending_frames(...)` ou `overworld_frame(pic, w, h, i)` com
i igual à posição na tabela. Tabela fora de ordem (ex.: sPicTable_BrendanSurfing,
que repete frames) mostraria tile errado ou liaria fora da folha, então fica CRUA.

O PREÇO da compressão é VRAM: o sprite comprimido ocupa a FOLHA INTEIRA na VRAM
de OBJ (todos os frames), em vez de um frame só. Um NPC 16x32 de 9 frames sai de
8 para 80 tiles, dentro dos 1024 de `TOTAL_OBJ_TILE_COUNT`. Em sala apertada e
cheia isso estoura, e o sintoma NÃO é sprite invisível: é sprite desenhado com
tile alheio (lixo). Medido em 15/08/2026 no BattleFrontier_BattleDomeBattleRoom
(15 objetos na mesma tela): o NPC de OBJ_EVENT_GFX_VAR_0 virou um borrão. Por
isso os 13 gráficos daquela sala voltaram ao cru (lista SEM_VRAM abaixo).

Uso:
    python3 dev_scripts/comprime_overworld.py --lista            # inventário ordenado por tamanho
    python3 dev_scripts/comprime_overworld.py --aplica --top 20  # comprime os 20 maiores
    python3 dev_scripts/comprime_overworld.py --aplica           # comprime todos os elegíveis
    python3 dev_scripts/comprime_overworld.py --descomprime A,B  # devolve gráficos ao cru
    python3 dev_scripts/comprime_overworld.py --reverte          # volta tudo ao cru
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GFX = os.path.join(RAIZ, "src/data/object_events/object_event_graphics.h")
INFO = os.path.join(RAIZ, "src/data/object_events/object_event_graphics_info.h")
TABELAS = [
    os.path.join(RAIZ, "src/data/object_events/object_event_pic_tables.h"),
    os.path.join(RAIZ, "src/data/object_events/object_event_pic_tables_followers.h"),
]
ASSETS = os.path.join(RAIZ, "build.nosync/assets")
SMOL = os.path.join(RAIZ, "tools/compresSmol/compresSmol")

# gráficos que ficam crus mesmo sendo elegíveis (motivo no valor)
EXCECOES = {
    "gObjectEventPic_RayquazaCutscene": "usado por field_effect_objects.h fora do caminho de object event",
}

# O avatar do jogador troca de gráfico o tempo todo (andar/bike/surf/pesca). As
# poses de surf, mergulho e regar têm pic table fora de ordem e ficam CRUAS de
# qualquer jeito, então o avatar seria misto: e a transição folha -> não-folha
# em `LoadSheetGraphicsInfo` mantém `oam.tileNum` apontando para dentro da folha
# antiga e escreve o frame cru por cima dela (o próprio motor admite:
# "TODO: Realloc usingSheet -> !usingSheet larger gfx"). Como a folha continua
# marcada como carregada, voltar para a bike reexibiria os tiles já sobrescritos.
# Por isso a família do avatar (Brendan/May, Red/Green/Leaf do FRLG e os bonecos
# de link RS) fica inteira crua.
# Os 13 gráficos dos 15 objetos do BattleFrontier_BattleDomeBattleRoom: todos na
# mesma tela, e comprimidos eles estouram a VRAM de OBJ (ver cabeçalho). Ficam
# crus, o que também alivia os outros mapas cheios, porque são NPCs comuns.
SEM_VRAM = {
    "gObjectEventPic_Boy1", "gObjectEventPic_Boy2", "gObjectEventPic_Camper",
    "gObjectEventPic_ExpertM", "gObjectEventPic_FatMan", "gObjectEventPic_Girl1",
    "gObjectEventPic_Girl2", "gObjectEventPic_Man1", "gObjectEventPic_Man2",
    "gObjectEventPic_NinjaBoy", "gObjectEventPic_ReporterM", "gObjectEventPic_Twin",
    "gObjectEventPic_Woman3",
}

RE_AVATAR = re.compile(
    r'^gObjectEventPic_(Brendan|May|Red|Green|Leaf|RubySapphireBrendan|RubySapphireMay)([A-Z]|$)'
)

RE_INCGFX = re.compile(
    r'const\s+u(8|16|32)\s+(gObjectEventPic_\w+)\[\]\s*=\s*INCGFX_(U8|U16|U32|COMP)\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*(?:,\s*"([^"]*)"\s*)?\)\s*;'
)
RE_ASC = re.compile(r'overworld_ascending_frames\(\s*(\w+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)')
RE_FRAME = re.compile(r'overworld_frame\(\s*(\w+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)')


def caminho_asset(fonte, ext, args):
    """Mesma regra de tools/preproc/c_file.cpp: args viram path, tudo não-alnum vira '_'."""
    sufixo = "".join(c if c.isalnum() else "_" for c in (args or ""))
    return os.path.join(ASSETS, fonte + sufixo + ext)


def le_pics():
    texto = open(GFX, encoding="utf-8").read()
    pics = {}
    for m in RE_INCGFX.finditer(texto):
        largura, nome, tipo = m.group(1), m.group(2), m.group(3)
        fonte, ext, args = m.group(4), m.group(5), m.group(6)
        pics[nome] = {
            "largura": largura,
            "tipo": tipo,
            "fonte": fonte,
            "ext": ext,
            "args": args,
            "asset": caminho_asset(fonte, ext, args),
        }
    return pics


def le_tabelas():
    """sPicTable_X -> (símbolo do pic, identidade?, nº de frames da tabela)."""
    tabelas = {}
    for caminho in TABELAS:
        texto = open(caminho, encoding="utf-8").read()
        for bloco in re.finditer(r'(\w+PicTable_\w+)\[\]\s*=\s*\{(.*?)\n\};', texto, re.S):
            nome, corpo = bloco.group(1), bloco.group(2)
            asc = RE_ASC.findall(corpo)
            frames = RE_FRAME.findall(corpo)
            if asc and not frames:
                tabelas[nome] = (asc[0][0], True, None)
            elif frames and not asc:
                simbolos = {f[0] for f in frames}
                identidade = (
                    len(simbolos) == 1
                    and all(int(f[3]) == i for i, f in enumerate(frames))
                )
                tabelas[nome] = (frames[0][0], identidade, len(frames))
            else:
                tabelas[nome] = (None, False, None)
    return tabelas


def le_infos():
    """Entradas de ObjectEventGraphicsInfo: nome -> dict com images/compressed/tileTag."""
    texto = open(INFO, encoding="utf-8").read()
    infos = {}
    for bloco in re.finditer(
        r'const\s+struct\s+ObjectEventGraphicsInfo\s+(\w+)\s*=\s*\{(.*?)\n\};', texto, re.S
    ):
        nome, corpo = bloco.group(1), bloco.group(2)
        imgs = re.search(r'\.images\s*=\s*(\w+)', corpo)
        tag = re.search(r'\.tileTag\s*=\s*(\w+)', corpo)
        infos[nome] = {
            "images": imgs.group(1) if imgs else None,
            "tileTag": tag.group(1) if tag else None,
            "compressed": ".compressed = TRUE" in corpo,
        }
    return infos


def inventario():
    pics, tabelas, infos = le_pics(), le_tabelas(), le_infos()
    # pic -> infos que o usam; um pic reprovado por qualquer info reprova geral
    por_pic = {}
    for nome_info, info in infos.items():
        tab = tabelas.get(info["images"])
        if not tab:
            continue
        pic, identidade, _ = tab
        if pic is None:
            continue
        d = por_pic.setdefault(pic, {"infos": [], "ok": True, "motivo": ""})
        d["infos"].append(nome_info)
        if not identidade:
            d["ok"] = False
            d["motivo"] = "pic table fora de ordem (frame != índice)"
        if info["tileTag"] != "TAG_NONE":
            d["ok"] = False
            d["motivo"] = "tileTag próprio (já usa folha estática)"

    itens = []
    for pic, d in por_pic.items():
        p = pics.get(pic)
        if p is None:
            d["ok"], d["motivo"] = False, "não é INCGFX (INCBIN cru ou símbolo externo)"
            tamanho = 0
        else:
            tamanho = os.path.getsize(p["asset"]) if os.path.exists(p["asset"]) else 0
            if p["tipo"] == "COMP":
                d["ok"], d["motivo"] = False, "já comprimido"
        if pic in EXCECOES:
            d["ok"], d["motivo"] = False, EXCECOES[pic]
        if RE_AVATAR.match(pic):
            d["ok"], d["motivo"] = False, "família do avatar do jogador (troca de gfx, ver cabeçalho)"
        if pic in SEM_VRAM:
            d["ok"], d["motivo"] = False, "sala cheia do Battle Dome estoura a VRAM de OBJ"
        itens.append(
            {"pic": pic, "tam": tamanho, "ok": d["ok"], "motivo": d["motivo"], "infos": d["infos"]}
        )
    itens.sort(key=lambda x: -x["tam"])
    return itens, pics


def mede_smol(itens, pics, quantos):
    """Roda o compresSmol num tmp só pra estimar economia (não toca na árvore)."""
    total_cru = total_comp = 0
    with tempfile.TemporaryDirectory() as tmp:
        for it in itens[:quantos]:
            if not it["ok"]:
                continue
            origem = pics[it["pic"]]["asset"]
            if not os.path.exists(origem):
                continue
            destino = os.path.join(tmp, os.path.basename(origem) + ".smol")
            subprocess.run([SMOL, "-w", origem, destino], check=True, capture_output=True)
            total_cru += os.path.getsize(origem)
            total_comp += os.path.getsize(destino)
    return total_cru, total_comp


def aplica(alvos, reverter=False):
    """Troca INCGFX_U32<->INCGFX_COMP e .compressed FALSE<->TRUE, em par."""
    pics, tabelas, infos = le_pics(), le_tabelas(), le_infos()
    texto = open(GFX, encoding="utf-8").read()
    trocados = 0
    for pic in alvos:
        # o dado .smol é lido como palavra: a declaração vira u32 junto com a troca.
        # (reverter normaliza para u32/INCGFX_U32; .4bpp cru é sempre múltiplo de 4)
        de, para = ("COMP", "U32") if reverter else ("(?:U8|U16|U32)", "COMP")
        alvo = re.compile(r'const u(?:8|16|32) (%s)\[\] = INCGFX_%s\(' % (re.escape(pic), de))
        texto, n = alvo.subn(r'const u32 \g<1>[] = INCGFX_%s(' % para, texto)
        trocados += n
    open(GFX, "w", encoding="utf-8").write(texto)

    # infos cujo pic table aponta para um dos alvos
    nomes_info = set()
    for nome_info, info in infos.items():
        tab = tabelas.get(info["images"])
        if tab and tab[0] in alvos:
            nomes_info.add(nome_info)

    texto = open(INFO, encoding="utf-8").read()
    de, para = ("TRUE", "FALSE") if reverter else ("FALSE", "TRUE")

    def troca(m):
        if m.group(1) in nomes_info:
            return m.group(0).replace(".compressed = %s" % de, ".compressed = %s" % para)
        return m.group(0)

    texto = re.sub(
        r'const\s+struct\s+ObjectEventGraphicsInfo\s+(\w+)\s*=\s*\{.*?\n\};', troca, texto, flags=re.S
    )
    open(INFO, "w", encoding="utf-8").write(texto)
    return trocados, len(nomes_info)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--reverte", action="store_true")
    ap.add_argument("--descomprime", default="", help="lista de pics, separada por vírgula")
    ap.add_argument("--top", type=int, default=0, help="só os N maiores elegíveis")
    ap.add_argument("--pula", type=int, default=0, help="pula os N maiores (para levas)")
    args = ap.parse_args()

    itens, pics = inventario()
    if args.descomprime:
        alvos = set(args.descomprime.split(","))
        n_gfx, n_info = aplica(alvos, reverter=True)
        print("descomprimido: %d INCGFX trocados, %d entradas de info marcadas"
              % (n_gfx, n_info))
        return
    elegiveis = [i for i in itens if i["ok"]]
    if args.pula:
        elegiveis = elegiveis[args.pula:]
    if args.top:
        elegiveis = elegiveis[: args.top]

    if args.lista or not (args.aplica or args.reverte):
        print("%-52s %8s  %s" % ("pic", "bytes", "situação"))
        for it in itens:
            print("%-52s %8d  %s" % (it["pic"], it["tam"], "ok" if it["ok"] else it["motivo"]))
        crus = sum(i["tam"] for i in itens if i["ok"])
        print("\nelegíveis: %d (%.1f KB crus)   inelegíveis: %d"
              % (len([i for i in itens if i["ok"]]), crus / 1024,
                 len([i for i in itens if not i["ok"]])))
        if os.path.exists(SMOL):
            cru, comp = mede_smol([i for i in itens if i["ok"]], pics, 10**9)
            print("estimativa smol: %.1f KB -> %.1f KB (economia %.1f KB)"
                  % (cru / 1024, comp / 1024, (cru - comp) / 1024))
        return

    alvos = {i["pic"] for i in elegiveis}
    if args.reverte:
        alvos = {p for p, d in pics.items() if d["tipo"] == "COMP"}
    n_gfx, n_info = aplica(alvos, reverter=args.reverte)
    print("%s: %d INCGFX trocados, %d entradas de info marcadas"
          % ("revertido" if args.reverte else "aplicado", n_gfx, n_info))


def demo():
    """ponytail: autoteste mínimo do que pode quebrar calado (parsing e pareamento)."""
    assert caminho_asset("a/b.png", ".4bpp", "-mwidth 2 -mheight 4") == os.path.join(
        ASSETS, "a/b.png_mwidth_2__mheight_4.4bpp")
    tabelas = le_tabelas()
    # tabela fora de ordem conhecida tem que ser reprovada
    assert tabelas["sPicTable_BrendanSurfing"][1] is False, tabelas["sPicTable_BrendanSurfing"]
    # ascending_frames tem que passar
    assert tabelas["sPicTable_BrendanMachBike"][1] is True
    infos = le_infos()
    assert infos["gObjectEventGraphicsInfo_BrendanNormal"]["images"] == "sPicTable_BrendanNormal"
    itens, pics = inventario()
    assert len(itens) > 200, len(itens)
    print("demo ok: %d pics no inventário" % len(itens))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        main()
