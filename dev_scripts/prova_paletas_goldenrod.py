#!/usr/bin/env python3
"""Prova, NO EMULADOR, que as casas de Goldenrod nao estao mais pretas.

Por que existe
--------------
Em 06/09/2026 o Gui trouxe do playtest a foto de "algumas casas em Goldenrod
City estao pretas": a Radio Tower com o corpo inteiro preto e so as janelas
aparecendo. A causa nao era arte nem DNS, era a ORDEM do array de paleta.
`LoadTilesetPalette` copia `tileset->palettes[numPalsInPrimary]` em bloco, entao
a POSICAO da linha dentro de `gTilesetPalettes_X` E o slot de paleta. O
importador de tilesets de Johto listava a pasta com `sorted()` e emitia tambem
os `.pal` que NAO sao slot (`08_over.pal`, a camada de luz noturna do hns),
empurrando 09, 10, 11 e 12 um degrau para cima: os slots 9 e 11 do jogo
recebiam paleta quase toda preta.

O que esta ferramenta mede, e por que so o PNG serve
----------------------------------------------------
Cor nao esta em EWRAM que se leia por simbolo: ela esta na PLTT e no
framebuffer. Entao a prova e o PNG, medido e nao olhado: o roteiro warpa por
debug para a porta da Radio Tower e a ferramenta conta, na faixa de tela onde o
predio esta, quanto do quadro e PRETO PURO. Na ROM `2026-09-05` a faixa mede
38,5% de preto na porta da Radio Tower; consertada mede 0,9%. A fracao varia cerca
de 0,1 ponto entre rodadas feitas em horas diferentes, porque o DNS tinge a tela,
e por isso o teto do caso e 12% e nao um valor colado na medida.

Uso
---
    python3 dev_scripts/prova_paletas_goldenrod.py                 # ROM do repo
    python3 dev_scripts/prova_paletas_goldenrod.py --rom outra.gba --map outra.map
    python3 dev_scripts/prova_paletas_goldenrod.py --demo
"""
import argparse
import os
import subprocess
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import testa_critico as tc  # noqa: E402

SAIDA = "/tmp/claude-501/paletas-goldenrod"

# (mapa, warp, faixa vertical da tela em pixels, teto de preto aceito, o que cobre)
# A faixa exclui a barra de baixo (grama e o proprio jogador) e o topo, onde o
# letreiro de mapa pode estar desenhado.
CASOS = [
    ("MAP_GOLDENROD_CITY", 7, (0, 96), 0.12, "Radio Tower, o predio da foto do Gui"),
    ("MAP_GOLDENROD_CITY", 10, (0, 96), 0.12, "Game Corner, mesmo tileset"),
    # CONTROLE, e nao segundo defeito: `ruins_of_alph_outside` tinha o array
    # desalinhado do mesmo jeito, mas NENHUM metatile colocado nos mapas dele usa
    # os slots que ficavam pretos (medido: 0 blocos de 2.208 em
    # LAYOUT_RUINS_OF_ALPH_OUTSIDE, contra 151 de 2.668 em Goldenrod). Ele passa
    # nas duas ROMs, e e isso que prova que a medida abaixo mede o defeito e nao
    # a hora do dia.
    ("MAP_RUINS_OF_ALPH_OUTSIDE", 0, (0, 96), 0.12, "CONTROLE: array desalinhado, slot preto nao usado"),
]


def fracao_preta(png, faixa):
    im = Image.open(png).convert("RGB")
    y0, y1 = faixa
    corte = im.crop((0, y0, im.width, y1))
    pixels = list(corte.tobytes())
    trincas = [tuple(pixels[i:i + 3]) for i in range(0, len(pixels), 3)]
    pretos = sum(1 for p in trincas if p == (0, 0, 0))
    return pretos / len(trincas)


def roda_caso(rom, simbolos, grupo, num, warp, prefixo):
    os.makedirs(SAIDA, exist_ok=True)
    roteiro = ",".join([tc.ABERTURA, tc.rota_warp(grupo, num, warp), "240:NADA"])
    png = f"{SAIDA}/{prefixo}.png"
    cmd = [tc.RUNNER, rom, "900", roteiro, png, "--dump-estado",
           "--sb1ptr", simbolos["gSaveBlock1Ptr"],
           "--partycount", simbolos["gPartiesCount"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(png):
        raise SystemExit(f"gba_runner nao gravou PNG. stderr:\n{r.stderr}")
    return png


# LENTE QUE FOI TENTADA E NAO ENTROU, com a medida por escrito para ninguem
# refazer o caminho: "procurar metatile COLOCADO num mapa cujo slot de paleta sai
# TODO PRETO". Ela NAO pega o defeito de 06/09/2026, medido no `graphics.h` de
# `7b9a11ce64`: `08_over.pal` tem 12 cores pretas e 4 amarelas (as janelas
# acesas), entao nao e "toda preta" e a lente passa direto. E, rodada nos 2.053
# layouts com blockdata em disco, ela acusa 56 de Kanto, Hoenn e Galar com
# tileset VANILLA, que precisariam de calibracao contra o `pret/pokeemerald`
# intocado antes de virarem gate. Duas razoes para nao existir: nao acha o que
# esta rodada consertou, e acenderia vermelho permanente. Quem pega o defeito e
# a invariante de ORDEM no `--demo` do `importa_tilesets_johto.py` (a posicao da
# linha em `gTilesetPalettes_X` tem que ser o numero do arquivo), calibrada nos
# dois lados: 4 tilesets acusados no `graphics.h` de `7b9a11ce64` e 0 no de hoje.


def demo():
    """Autoteste do que da para autotestar sem emulador."""
    por_nome, _ = tc.carrega_mapas()
    faltam = [c[0] for c in CASOS if c[0] not in por_nome]
    assert not faltam, f"mapa desconhecido: {faltam}"
    # um quadro todo preto tem que medir 1.0, e um todo branco 0.0
    os.makedirs(SAIDA, exist_ok=True)
    for cor, esperado in (((0, 0, 0), 1.0), ((255, 255, 255), 0.0)):
        p = f"{SAIDA}/_demo.png"
        Image.new("RGB", (240, 160), cor).save(p)
        assert abs(fracao_preta(p, (0, 96)) - esperado) < 1e-9, cor
    print(f"demo OK: {len(CASOS)} mapas resolvidos, medidor de preto calibrado")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=os.path.join(RAIZ, "pokeemerald.gba"))
    ap.add_argument("--map", dest="mapa")
    ap.add_argument("--prefixo", default="atual")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    mapa = a.mapa or os.path.splitext(a.rom)[0] + ".map"
    simbolos = tc.carrega_simbolos(mapa)
    por_nome, _ = tc.carrega_mapas()
    ruim = 0
    for nome, warp, faixa, teto, oque in CASOS:
        grupo, num = por_nome[nome]
        prefixo = f"{a.prefixo}-{nome.lower()}-w{warp}"
        png = roda_caso(a.rom, simbolos, grupo, num, warp, prefixo)
        f = fracao_preta(png, faixa)
        ok = f <= teto
        ruim += not ok
        print(f"{'OK  ' if ok else 'RUIM'} {nome} warp {warp}: {f:.1%} de preto "
              f"(teto {teto:.0%})  {oque}  -> {png}")
    print("PALETAS OK" if not ruim else f"PALETAS RUINS: {ruim} casos")
    return 1 if ruim else 0


if __name__ == "__main__":
    sys.exit(main() or 0)
