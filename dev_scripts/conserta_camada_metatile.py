#!/usr/bin/env python3
"""Tira o jogador de baixo do bloco preto: camada de desenho errada no tileset.

Por que existe
--------------
No playtest de 06/09/2026 o Gui trouxe, da Route 212 South (a rota de CHUVA que
encosta em Pastoria, capitulo "before Crasher Wake"), um "retangulo de tiles
pretos em que o jogador entra embaixo e some". Nao era metatile indefinido, nem
tile preto de mapa cortado, nem `setmetatile` apagado: era CAMADA DE DESENHO.

`DrawMetatile` (src/fieldmap.c) so tem tres casos, e eles decidem em qual BG
cada uma das duas camadas do metatile vai parar:

    NORMAL   camada de baixo -> BG2 (abaixo do sprite)
             camada de cima  -> BG1, que e desenhado ACIMA de todo sprite
    COVERED  camada de baixo -> BG3, camada de cima -> BG2: as duas ficam
             ABAIXO do sprite, e o BG1 fica vazio
    SPLIT    camada de baixo -> BG3, camada de cima -> BG1 (acima do sprite)

Os metatiles do brejo da Route 212 (o `gTileset_LilycoveSinnoh`) trazem a arte
inteira na camada de CIMA, 100% opaca, com tipo NORMAL. O resultado e um bloco
que desenha por cima do jogador, e como o `map.bin` marca colisao 0 ele e
ANDAVEL: o jogador entra e desaparece. A noite, com chuva, o bloco fica quase
preto, que foi como o Gui o descreveu.

Passar esses metatiles para COVERED coloca a MESMA arte no BG2, abaixo do
sprite. Nao muda um pixel de desenho, nao mexe em `map.bin`, nao mexe em mapa
nenhum: muda dois bytes por metatile no `metatile_attributes.bin`.

O que ele NAO toca, de proposito
--------------------------------
Passar por baixo de ponte ou de copa de arvore usa exatamente o mesmo
mecanismo, e ali esconder o jogador e o desenho certo. A diferenca esta na
camada de BAIXO: numa passagem de verdade ela traz o CHAO por onde se anda, e e
diferente do que esta por cima. Por isso a regra so aceita metatile cuja camada
de baixo esteja VAZIA ou repita a de cima em METADE dos quadrantes, que e a
assinatura de arte empurrada para a camada errada pelo conversor de tileset.
Medido: passagem por baixo de verdade nao compartilha quadrante nenhum (o
metatile 669 do `gTileset_Facility`, no Aqua Hideout do vanilla, tem 0 de 4),
e os cantos do brejo da Route 212 tem 3 de 4.

E ele so mexe em tileset que **nenhum mapa de Hoenn ou de Kanto usa**. A mesma
lente (`E3` em `dev_scripts/qa/mapas_qa.py`) acusa 491 celulas em Hoenn e as
MESMAS 491 na arvore do `pokeemerald` intocado, e as de Kanto tinham atributo
identico ao do `pokefirered`: la e idioma do jogo original, nao defeito nosso, e
consertar seria divergir da fonte por zero ganho.

`--contra`, e por que a protecao de Kanto tem uma porta
--------------------------------------------------------
A protecao acima vale enquanto a frase "as de Kanto tem atributo identico ao do
`pokefirered`" for verdade. Em 11/09/2026 ela deixou de ser: a arte de Kanto
trocou pelo Ikarus' Tileset Patch v3.2, e a lente E3 subiu de 240 para 272
celulas na regiao, com 54 celulas NOVAS em 10 mapas. Proteger essas seria
proteger o estrago, nao a fonte.

`--contra <arvore>` roda a mesma lente na arvore de referencia e so conserta o
metatile que acusa alguma celula que a referencia NAO acusava. Em cima disso,
duas travas caem para essas linhas, e as duas com motivo medido:

  - a protecao de regiao, porque a fonte daquele metatile nao e mais o
    `pokefirered`;
  - o censo de solido, porque medido nos 37 metatiles novos de Kanto a camada de
    BAIXO esta VAZIA (0 pixels) em 37 de 37, com a de cima 100% opaca. Nao ha
    chao para revelar: COVERED so desce a MESMA arte para baixo do sprite. O
    idioma do FireRed para "andar por tras do predio" e o oposto disso, chao
    cheio embaixo (256 px) e so um pedaco de telhado em cima (40, 64 ou 116 px),
    medido nos metatiles que ocupavam as mesmas celulas antes da troca. E tornar
    solidas as 54 celulas mudaria a topologia andavel de 10 mapas, que e uma
    mudanca maior e de outra natureza.

Uso
---
    python3 dev_scripts/conserta_camada_metatile.py            # so mede
    python3 dev_scripts/conserta_camada_metatile.py --aplica   # grava
    python3 dev_scripts/conserta_camada_metatile.py --regiao Johto
    python3 dev_scripts/conserta_camada_metatile.py --regiao Kanto \
        --contra /caminho/arvore-antes --aplica
    python3 dev_scripts/conserta_camada_metatile.py --demo     # autoteste

Idempotente: rodar duas vezes com `--aplica` da 0 metatiles alterados na
segunda, porque depois da primeira o tipo ja e COVERED e a regra nao morde.
"""
import argparse
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts", "qa"))
import mapas_qa as M  # noqa: E402

COVERED = 1
PROTEGIDAS = ("Hoenn", "Kanto")


def levanta(raiz, regiao, contra=None):
    """[(tileset, id local, id no mapa, mapas)] que a regra E3 acusa na região.

    A varredura inteira roda porque o alcance (a BFS a partir de warp, heal e
    conexão) é o que separa o defeito do enchimento: mapa importado tem centenas
    de células pretas FORA da sala, atrás da parede, onde ninguém pisa.

    `contra` é a árvore de REFERÊNCIA, e o campo `novo` de cada linha diz se
    aquele metatile acusa ALGUMA célula que a referência não acusava. É esse
    campo que separa o idioma do jogo original (que fica intocado) do estrago que
    uma troca de arte trouxe. Ver o comentário de PROTEGIDAS.
    """
    ach, _nm, _censo, _ = M.varre(raiz, "E3")
    A = M.Arvore(raiz)
    grupos = A.grupos
    layout_de, regiao_de_mapa = {}, {}
    for gn in grupos["group_order"]:
        for mn in grupos.get(gn, []):
            p = os.path.join(raiz, "data/maps", mn, "map.json")
            if not os.path.exists(p):
                continue
            d = json.load(open(p, encoding="utf-8"))
            layout_de[mn] = d.get("layout")
            regiao_de_mapa[mn] = M.regiao_de(mn, gn)

    # tileset -> conjunto de regiões que o usam. É esta tabela que protege o
    # desenho de Hoenn e de Kanto de um conserto pedido para outra região.
    usos = collections.defaultdict(set)
    for mn, lid in layout_de.items():
        L = A.layouts.get(lid)
        if not L:
            continue
        for k in ("primary_tileset", "secondary_tileset"):
            if L.get(k) and L[k] != "0":
                usos[L[k]].add(regiao_de_mapa[mn])

    # CENSO DE COLISÃO por metatile, e é ele que separa DOIS defeitos que a
    # lente E3 acusa igual e que se consertam em lugares opostos:
    #
    #   metatile que nunca aparece em célula SÓLIDA  -> é chão, e o defeito é a
    #       CAMADA: a arte foi para a de cima e tapa quem anda em cima dela.
    #   metatile que aparece sólido na maioria das vezes -> é telhado ou parede,
    #       e desenhar por cima do jogador é o certo; o defeito é a COLISÃO da
    #       CÉLULA, no `map.bin`, e passá-lo para COVERED só trocaria "jogador
    #       sumiu" por "jogador andando por cima do telhado".
    #
    # Medido em 06/09/2026: os metatiles 12, 80-82, 89, 131 e 139 do
    # `gTileset_GeneralSinnoh` são o telhado vermelho e a fachada do Centro
    # Pokémon, 12 usos sólidos contra 1 andável (uma célula de OreburghCity), e
    # o brejo da Route 212 é o oposto exato: 405 usos, nenhum sólido.
    censo = collections.Counter()
    for mn, lid in layout_de.items():
        L = A.layouts.get(lid)
        g = A.grade(lid) if L else None
        if not g:
            continue
        W, H, linhas, corte = g
        for y in range(H):
            for x in range(W):
                v = linhas[y][x]
                mid = v & 0x3FF
                ts, loc = ((L["primary_tileset"], mid) if mid < corte
                           else (L["secondary_tileset"], mid - corte))
                censo[(ts, loc, 1 if (v >> 10) & 3 else 0)] += 1

    referencia = set()
    if contra:
        ach_ref, _nm, _c, _ = M.varre(contra, "E3")
        referencia = {(it["mapa"], tuple(it["coord"] or ()))
                      for it in ach_ref.itens if it["regra"] == "E3"}

    alvos = {}
    for it in ach.itens:
        if it["regra"] != "E3" or it["regiao"] != regiao:
            continue
        mid = int(it["detalhe"].split()[1])
        L = A.layouts[layout_de[it["mapa"]]]
        corte = 640 if L.get("layout_version") in ("frlg", "johto") else 512
        ts, local = ((L["primary_tileset"], mid) if mid < corte
                     else (L["secondary_tileset"], mid - corte))
        chave = (ts, local)
        alvos.setdefault(chave, dict(mapas=set(), mid=mid, novas=0, celulas=0))
        alvos[chave]["mapas"].add(it["mapa"])
        alvos[chave]["celulas"] += 1
        if contra and (it["mapa"], tuple(it["coord"] or ())) not in referencia:
            alvos[chave]["novas"] += 1
    fora = []
    for (ts, local), info in sorted(alvos.items()):
        protegido = sorted(usos[ts] & set(PROTEGIDAS))
        solido = censo[(ts, local, 1)]
        fora.append(dict(tileset=ts, local=local, mid=info["mid"],
                         mapas=sorted(info["mapas"]), protegido=protegido,
                         solido=solido, andavel=censo[(ts, local, 0)],
                         celulas=info["celulas"], novas=info["novas"],
                         novo=bool(info["novas"])))
    return fora, A


def decide(item, com_contra):
    """('conserta'|'pula'|'fora'), e o motivo. A porta da protecao mora aqui.

    Separada de `main` de proposito: e a unica regra de decisao da ferramenta, e
    o `--demo` precisa mordê-la sem rodar a varredura inteira.
    """
    if com_contra and not item.get("novo"):
        return "fora", "ja acusava na arvore de referencia: idioma da fonte"
    if item["protegido"] and not item.get("novo"):
        return "pula", ("tileset compartilhado com "
                        + ", ".join(item["protegido"]))
    if item["solido"] and not item.get("novo"):
        return "pula", (f"{item['solido']} usos SOLIDOS contra {item['andavel']} "
                        "andaveis, e telhado ou parede: o defeito e a colisao da "
                        "celula, nao a camada")
    return "conserta", ""


def grava(A, ts, locais):
    """Marca COVERED os metatiles `locais` do tileset. Devolve quantos mudaram."""
    d = A.pastas().get(ts)
    if not d:
        raise SystemExit(f"tileset {ts} sem pasta")
    pa = os.path.join(d, "metatile_attributes.bin")
    pm = os.path.join(d, "metatiles.bin")
    n = os.path.getsize(pm) // 16
    b = bytearray(open(pa, "rb").read())
    larg = len(b) // n if n else 2
    mudou = 0
    for i in locais:
        if larg == 4:
            v = struct.unpack_from("<I", b, i * 4)[0]
            novo = (v & ~(3 << 29)) | (COVERED << 29)
            if novo != v:
                struct.pack_into("<I", b, i * 4, novo)
                mudou += 1
        else:
            v = struct.unpack_from("<H", b, i * 2)[0]
            novo = (v & ~0xF000) | (COVERED << 12)
            if novo != v:
                struct.pack_into("<H", b, i * 2, novo)
                mudou += 1
    if mudou:
        open(pa, "wb").write(bytes(b))
    return mudou


def demo():
    """Autoteste: a régua morde a assinatura e larga a passagem por baixo."""
    # (1) o predicado, nos quatro casos que decidem tudo
    cheio, vazio = M.PX_POR_CAMADA, 0
    assert M.tapa_o_jogador(vazio, cheio, 0, 0), "camada de cima cheia, chão vazio"
    assert M.tapa_o_jogador(cheio, cheio, 4, 0), "chão idêntico ao teto"
    assert M.tapa_o_jogador(cheio, cheio, 3, 0), "canto do brejo: 3 de 4 quadrantes"
    assert M.tapa_o_jogador(vazio, cheio, 0, 2), "SPLIT também põe no BG1"
    assert not M.tapa_o_jogador(cheio, cheio, 0, 0), "ponte: chão != teto, é passagem"
    assert not M.tapa_o_jogador(cheio, cheio, 1, 0), "1 de 4 quadrantes ainda é passagem"
    assert not M.tapa_o_jogador(vazio, cheio, 0, COVERED), "COVERED já está certo"
    assert not M.tapa_o_jogador(vazio, cheio - 1, 0, 0), "teto com furo deixa ver"

    # (2) a leitura do bit: escrever COVERED e ler de volta, nos dois formatos
    def volta16(v):
        b = bytearray(struct.pack("<H", v))
        x = struct.unpack_from("<H", b, 0)[0]
        return ((x & ~0xF000) | (COVERED << 12)) >> 12 & 0xF
    assert volta16(0x0000) == COVERED and volta16(0x2008) == COVERED

    def volta32(v):
        return (((v & ~(3 << 29)) | (COVERED << 29)) >> 29) & 3
    assert volta32(0x01000008) == COVERED and volta32(0x41000008) == COVERED

    # (3) o alvo real desta rodada continua sendo o brejo da Route 212 South:
    #     o metatile 705 do LilycoveSinnoh é o miolo do retângulo que o Gui viu.
    A = M.Arvore(RAIZ)
    des = A.desenho_do_metatile("LAYOUT_ROUTE212_SOUTH", 705)
    assert des, "o metatile 705 sumiu do LilycoveSinnoh: a árvore mudou"
    px_baixo, px_cima, iguais, tipo = des
    assert px_cima == M.PX_POR_CAMADA, f"a camada de cima parou de ser opaca: {px_cima}"
    assert iguais == 4, "as duas camadas do 705 deixaram de ser idênticas"
    assert tipo in (0, COVERED), f"tipo inesperado: {tipo}"

    # (4) a porta da protecao: sem `--contra` nada de Kanto passa, e com
    #     `--contra` so passa o que a referencia nao acusava
    velho = dict(protegido=["Kanto"], solido=0, andavel=3, novo=False)
    assert decide(velho, False)[0] == "pula"
    assert decide(velho, True)[0] == "fora"
    novo_chao = dict(protegido=["Kanto"], solido=0, andavel=3, novo=True)
    assert decide(novo_chao, True)[0] == "conserta"
    novo_telhado = dict(protegido=["Kanto"], solido=2, andavel=3, novo=True)
    assert decide(novo_telhado, True)[0] == "conserta"
    telhado_velho = dict(protegido=[], solido=12, andavel=1, novo=False)
    assert decide(telhado_velho, False)[0] == "pula"
    print("demo ok")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--regiao", default="Sinnoh")
    ap.add_argument("--tileset", action="append",
                    help="restringe a estes tilesets (pode repetir)")
    ap.add_argument("--contra", help="árvore de referência: só conserta o "
                                     "metatile que acusa célula que ela não acusava")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()

    alvos, A = levanta(RAIZ, a.regiao, a.contra)
    if not alvos:
        print(f"{a.regiao}: nenhum metatile com a assinatura")
        return 0
    por_ts = collections.defaultdict(list)
    for t in alvos:
        veredito, motivo = decide(t, bool(a.contra))
        if veredito == "fora":
            continue
        if veredito == "pula":
            print(f"  PULADO {t['tileset']} {t['local']}: {motivo} "
                  f"({', '.join(t['mapas'][:3])})")
            continue
        if t.get("novo") and t["solido"]:
            print(f"  NOVO E SOLIDO {t['tileset']} {t['local']}: {t['solido']} usos "
                  f"solidos contra {t['andavel']} andaveis. Vai para COVERED "
                  f"assim mesmo: a camada de BAIXO esta vazia, entao nao ha chao "
                  f"para revelar, e tornar solida a celula andavel mudaria a "
                  f"topologia de {', '.join(t['mapas'][:3])}")
        if a.tileset and t["tileset"] not in a.tileset:
            print(f"  FORA DO RECORTE {t['tileset']} {t['local']} "
                  f"({', '.join(t['mapas'][:3])})")
            continue
        por_ts[t["tileset"]].append(t)
    print(f"{a.regiao}: {sum(len(v) for v in por_ts.values())} metatiles "
          f"em {len(por_ts)} tilesets")
    for ts, itens in sorted(por_ts.items()):
        mapas = sorted({m for t in itens for m in t["mapas"]})
        print(f"  {ts}: {[t['local'] for t in itens]}  ({', '.join(mapas[:4])}"
              f"{'...' if len(mapas) > 4 else ''})")
    if not a.aplica:
        print("\n(só medindo; use --aplica para gravar)")
        return 0
    total = 0
    for ts, itens in sorted(por_ts.items()):
        total += grava(A, ts, [t["local"] for t in itens])
    print(f"\n{total} metatiles passaram para COVERED")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
