#!/usr/bin/env python3
"""Lente de paletas de OBJ: conta as paletas distintas que os NPCs de um mapa pedem.

Uso:
    python3 dev_scripts/qa/lente_paletas_obj.py            # portão: exit 1 se algum mapa estoura
    python3 dev_scripts/qa/lente_paletas_obj.py --lista    # os 20 mapas mais cheios e a folga
    python3 dev_scripts/qa/lente_paletas_obj.py --mapa Galar_Wyndon01   # um mapa, tag a tag
    python3 dev_scripts/qa/lente_paletas_obj.py --demo     # mutação plantada tem que reprovar

Por que existe
--------------
O OBJ do GBA tem 16 paletas de 16 cores (src/sprite.c, sSpritePaletteTags[16]).
Cada NPC pede a paleta pelo `paletteTag` da folha dele; NPCs com o MESMO tag
dividem um slot, e cada tag DISTINTO gasta um. Quando os 16 acabam,
`LoadSpritePalette` devolve 0xFF e o NPC sai com a cor de outro, sem erro nem
aviso. As 59 folhas novas de Galar e Unova (arte da fase 1) têm 59 tags, todos
diferentes; quando a decisão 130 espalhar esses NPCs pelos mapas, é aqui que o
estouro aparece, antes de alguém ver um NPC roxo no emulador.

O que conta
-----------
Para cada `data/maps/*/map.json`, o número de tags DISTINTOS entre os
`object_events`, resolvendo `graphics_id` pelo mesmo caminho do motor:
`OBJ_EVENT_GFX_*` -> `gObjectEventGraphicsInfo_*`
(src/data/object_events/object_event_graphics_info_pointers.h) -> `.paletteTag`
(object_event_graphics_info.h). `OBJ_EVENT_GFX_SPECIES(X)` usa a paleta da
espécie, um tag por espécie (src/event_object_movement.c, palTag = species +
OBJ_EVENT_MON). `OBJ_EVENT_GFX_VAR_*` é decidido em tempo de execução e conta
como um tag próprio. Tag `NONE` não gasta slot.

Somado a isso, `RESERVADOS`: os slots que o campo já ocupa sem NPC nenhum
(clima, jogador, efeitos de campo e o reflexo do jogador). Medido no emulador
onde deu para medir; ver o comentário de RESERVADOS.

A janela foi conferida no emulador em 28/10/2026: no warp 5 da Unova Relic
Castle B1F a lente prevê 9 tags de NPC e o motor ocupou 11 slots (9 + clima +
jogador); no warp 10 da Victory Road Cave 2F, 8 previstos e 10 ocupados.

A conta é por MAPA e não por tela, de propósito: o motor só cria o NPC que
está perto da câmera, então um mapa grande pode ter mais tags que slots sem
estourar nunca. A lente é conservadora; quem estourar aqui é mapa para olhar,
e a correção é dividir paleta ou trocar NPC por um de paleta já usada.

Só lê arquivos de texto. Não compila. Cerca de 1 s.
"""
import argparse
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PONTEIROS = os.path.join(RAIZ, "src/data/object_events/object_event_graphics_info_pointers.h")
INFOS = [
    os.path.join(RAIZ, "src/data/object_events/object_event_graphics_info.h"),
    os.path.join(RAIZ, "src/data/object_events/object_event_graphics_info_followers.h"),
]
CONSTANTES = os.path.join(RAIZ, "include/constants/event_objects.h")

SLOTS = 16
NPCS_VIVOS = 15  # OBJECT_EVENTS_COUNT (16) menos o jogador
# Slots que o campo ocupa sem NPC nenhum. MEDIDO em 28/10/2026 lendo
# sSpritePaletteTags (src/sprite.c) no emulador (ESTADO-CARTUCHO-2.md, seção
# c2-galar-ui): parado em Galar_Route03_02, Slumbering Weald 02 (neblina) e
# Route10_01 (neve), o campo usa SEMPRE 2 slots, o do clima (PALTAG_WEATHER,
# 0x1200, carregado mesmo sem clima) e o do jogador (0x1100). Andando na grama
# alta da Wild Area 09 entra o FLDEFF_PAL_TAG_GENERAL_1 (0x1005). Somados, por
# leitura de src/field_effect_helpers.c e não medidos: o GENERAL_0 (sombra de
# pulo, ondinha na água) e o reflexo do jogador, que ganha paleta própria
# filtrada (tag base + PAL_TAG_REFLECTION_OFFSET). Total 5.
# Fora da conta, de propósito: NPC refletido na água também ganha paleta
# própria, uma por tag refletido. Mapa com poça e NPC colado nela pede folga.
RESERVADOS = 5
LIMITE = SLOTS - RESERVADOS

# Túmulo do cartucho 1 (dev_scripts/remove_regioes_cartucho1.py): mapa 1x1 que
# só existe porque o motor ainda cita a constante. Ninguém entra; os objetos
# que sobraram nele (as bonecas do quarto de Littleroot, o Contest Hall) nunca
# são criados. Fica fora da conta.
LAYOUT_TUMULO = "LAYOUT_TOCO_VAGO"

TAGS_SEM_SLOT = {"TAG_NONE", "OBJ_EVENT_PAL_TAG_NONE", "0xFFFF"}


def le_ponteiros():
    """OBJ_EVENT_GFX_X -> nome do ObjectEventGraphicsInfo."""
    mapa = {}
    for m in re.finditer(r"\[(OBJ_EVENT_GFX_\w+)\]\s*=\s*&(gObjectEventGraphicsInfo_\w+)",
                         open(PONTEIROS, encoding="utf-8").read()):
        mapa[m.group(1)] = m.group(2)
    # Apelidos: #define OBJ_EVENT_GFX_A OBJ_EVENT_GFX_B (fora de comentário).
    for linha in open(CONSTANTES, encoding="utf-8"):
        m = re.match(r"\s*#define\s+(OBJ_EVENT_GFX_\w+)\s+(OBJ_EVENT_GFX_\w+)\s*(//.*)?$", linha)
        if m and m.group(2) in mapa and m.group(1) not in mapa:
            mapa[m.group(1)] = mapa[m.group(2)]
    return mapa


def le_tags():
    """nome do ObjectEventGraphicsInfo -> paletteTag."""
    tags = {}
    for caminho in INFOS:
        if not os.path.exists(caminho):
            continue
        texto = open(caminho, encoding="utf-8").read()
        for m in re.finditer(r"(gObjectEventGraphicsInfo_\w+)\s*=\s*\{(.*?)\n\};", texto, re.S):
            t = re.search(r"\.paletteTag\s*=\s*([\w()+ ]+?)\s*,", m.group(2))
            if t:
                tags[m.group(1)] = t.group(1).strip()
    return tags


def tag_do_objeto(gfx, ponteiros, tags):
    """Devolve (tag, problema). tag None quer dizer que não gasta slot."""
    gfx = gfx.strip()
    m = re.match(r"OBJ_EVENT_GFX_SPECIES(_SHINY|_FEMALE|_SHINY_FEMALE)?\((\w+)\)$", gfx)
    if m:
        return f"ESPECIE:{m.group(2)}{m.group(1) or ''}", None
    if re.match(r"OBJ_EVENT_GFX_VAR_[0-9A-F]$", gfx):
        return f"VAR:{gfx}", None
    info = ponteiros.get(gfx)
    if info is None:
        return None, f"graphics_id sem folha: {gfx}"
    tag = tags.get(info)
    if tag is None:
        return None, f"folha sem paletteTag: {info}"
    if tag in TAGS_SEM_SLOT:
        return None, None
    return tag, None


def le_dimensoes():
    """id do layout -> (largura, altura), de data/layouts/layouts.json."""
    caminho = os.path.join(RAIZ, "data/layouts/layouts.json")
    if not os.path.exists(caminho):
        return {}
    return {l["id"]: (l["width"], l["height"])
            for l in json.load(open(caminho, encoding="utf-8")).get("layouts", []) if "id" in l}


def pior_janela(objetos, largura, altura):
    """Maior número de tags distintos numa mesma janela de criação de NPC.

    O motor só cria o NPC que cai na janela em volta do jogador
    (TrySpawnObjectEvents e RemoveObjectEventsOutsideView, em
    src/event_object_movement.c): com o jogador em (px, py), x de px-9 a px+10 e
    y de py-7 a py+9. Testa toda posição do jogador dentro do mapa e devolve
    (n, (px, py), tags) da pior. Teto de OBJECT_EVENTS_COUNT - 1 = 15 NPCs vivos:
    acima disso o motor nem cria o NPC, e a paleta não chega a ser pedida.
    """
    melhor = (0, None, set())
    if not objetos:
        return melhor
    for py in range(max(altura, 1)):
        dentro_y = [o for o in objetos if py - 7 <= o[1] <= py + 9]
        if len({o[2] for o in dentro_y}) <= melhor[0]:
            continue
        for px in range(max(largura, 1)):
            janela = [o for o in dentro_y if px - 9 <= o[0] <= px + 10][:NPCS_VIVOS]
            t = {o[2] for o in janela}
            if len(t) > melhor[0]:
                melhor = (len(t), (px, py), t)
    return melhor


def conta(mapas_json, ponteiros, tags, dimensoes=None):
    """nome do mapa -> dict com os tags do mapa inteiro, a pior janela e os problemas."""
    dimensoes = dimensoes or {}
    saida = {}
    for caminho in mapas_json:
        d = json.load(open(caminho, encoding="utf-8"))
        nome = d.get("name") or os.path.basename(os.path.dirname(caminho))
        if d.get("layout") == LAYOUT_TUMULO:
            continue
        vistos, problemas, objetos = set(), [], []
        for obj in d.get("object_events", []):
            gfx = obj.get("graphics_id")
            if not gfx:
                continue  # clone sem gráfico próprio: desenha o do mapa vizinho
            tag, problema = tag_do_objeto(gfx, ponteiros, tags)
            if problema:
                problemas.append(problema)
            if tag:
                vistos.add(tag)
                objetos.append((obj.get("x", 0), obj.get("y", 0), tag))
        largura, altura = dimensoes.get(d.get("layout"), (0, 0))
        if not largura:
            xs = [o[0] for o in objetos] or [0]
            ys = [o[1] for o in objetos] or [0]
            largura, altura = max(xs) + 1, max(ys) + 1
        saida[nome] = {"mapa": vistos, "janela": pior_janela(objetos, largura, altura),
                       "problemas": problemas}
    return saida


def demo(ponteiros, tags):
    """Mutação: um mapa com LIMITE+1 tags distintos tem que reprovar, e um com
    LIMITE NPCs da MESMA folha tem que passar."""
    distintos = sorted({t for t in tags.values() if t not in TAGS_SEM_SLOT})
    por_tag = {}
    for gfx, info in ponteiros.items():
        t = tags.get(info)
        if t in distintos and t not in por_tag:
            por_tag[t] = gfx
    gfxs = list(por_tag.values())[:LIMITE + 1]
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        cheio = os.path.join(tmp, "cheio.json")
        igual = os.path.join(tmp, "igual.json")
        json.dump({"name": "Mutacao_Cheio", "object_events": [{"graphics_id": g} for g in gfxs]},
                  open(cheio, "w"))
        json.dump({"name": "Mutacao_Igual", "object_events": [{"graphics_id": gfxs[0]}] * (LIMITE + 5)},
                  open(igual, "w"))
        r = conta([cheio, igual], ponteiros, tags)
    ok_cheio = r["Mutacao_Cheio"]["janela"][0] > LIMITE
    ok_igual = r["Mutacao_Igual"]["janela"][0] == 1
    print(f"mutação {LIMITE + 1} tags distintos: {'reprovou (certo)' if ok_cheio else 'PASSOU (errado)'}")
    print(f"mutação {LIMITE + 5} NPCs da mesma folha: {'1 tag (certo)' if ok_igual else 'ERRADO'}")
    return 0 if ok_cheio and ok_igual else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--mapa")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()

    ponteiros, tags = le_ponteiros(), le_tags()
    if a.demo:
        return demo(ponteiros, tags)

    arquivos = sorted(glob.glob(os.path.join(RAIZ, "data/maps/*/map.json")))
    r = conta(arquivos, ponteiros, tags, le_dimensoes())

    if a.mapa:
        if a.mapa not in r:
            print(f"mapa {a.mapa} não existe")
            return 1
        e = r[a.mapa]
        n, pos, t = e["janela"]
        print(f"{a.mapa}: {len(e['mapa'])} tags no mapa inteiro; pior janela {n} com o jogador em {pos}:")
        for tag in sorted(t):
            print(" ", tag)
        for p in e["problemas"]:
            print("  problema:", p)
        print(f"  {n} de NPC + {RESERVADOS} reservados = {n + RESERVADOS} de {SLOTS}")
        return 0

    def pior(n):
        return r[n]["janela"][0]

    estouram = sorted((n for n in r if pior(n) > LIMITE), key=lambda n: -pior(n))
    problemas = sorted({p for e in r.values() for p in e["problemas"]})
    maior = max(r, key=pior)
    print(f"{len(r)} mapas (túmulos fora); limite {LIMITE} tags de NPC por janela ({SLOTS} slots - {RESERVADOS} reservados); "
          f"pior janela: {maior} com {pior(maior)}, jogador em {r[maior]['janela'][1]}")
    if a.lista:
        print("  janela  mapa inteiro  folga  mapa")
        for n in sorted(r, key=lambda n: (-pior(n), -len(r[n]["mapa"])))[:20]:
            print(f"  {pior(n):6d}  {len(r[n]['mapa']):12d}  {LIMITE - pior(n):5d}  {n}")
    for p in problemas:
        print("  aviso:", p)
    if estouram:
        for n in estouram:
            print(f"  ESTOURA: {n} com {pior(n)} tags numa janela, jogador em {r[n]['janela'][1]} (limite {LIMITE})")
        print(f"VERMELHO: {len(estouram)} mapa(s) acima do limite")
        return 1
    print("VERDE: nenhum mapa acima do limite")
    return 0


if __name__ == "__main__":
    sys.exit(main())
