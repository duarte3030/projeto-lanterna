#!/usr/bin/env python3
"""Lente de CAMADA: objeto que o jogador tem ATRÁS de si não pode tampar a cabeça dele.

Uso:
    python3 dev_scripts/qa/lente_camada.py           # lista os achados
    python3 dev_scripts/qa/lente_camada.py --demo    # autoteste, exit 1 se cair

Por que existe
--------------
Playtest do Gui na ROM bugs2b (30/09/2026): "em Sinnoh inteira está invertida a
sobreposição de tile: minha cabeça é tampada pelos objetos". O sprite do jogador
tem 16x32 e a cabeça invade a célula do norte; se essa célula é bloqueada e tem
arte na camada de CIMA de um metatile NORMAL ou SPLIT, o BG1 desenha a arte por
cima do sprite. Os tilesets de Sinnoh vieram assim da fonte. O conserto mora em
`dev_scripts/camada_sinnoh.py`, e esta lente usa a MESMA régua dele para pegar a
volta do defeito: tileset novo copiado com camada errada, ou metatile trocado.

Regra
-----
    Z1  célula andável de prioridade 2 (elevação que não é ponte) cujo vizinho do
        norte é bloqueado e tem arte na camada de cima, num tileset que só Sinnoh
        usa. Classe "trava" quando o metatile seria trocado pela regra do
        camada_sinnoh.py; "falso positivo" quando ele é um dos que ficam de
        propósito (pisado em mais células do que tampa: ali a cobertura é o
        desenho de passar por trás).

A calibração (30/09/2026): a mesma régua em cidades e rotas dá 0,37% das células
andáveis em Hoenn, 0,34% em Kanto e 0,20% em Johto, todas iguais às fontes. Por
isso a lente só olha Sinnoh: nas outras três regiões o desenho é o do vanilla, e
cobrar ali seria mandar consertar o jogo original.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ACIMA = os.path.dirname(AQUI)
for p in (AQUI, ACIMA):
    if p not in sys.path:
        sys.path.insert(0, p)

import camada_sinnoh  # noqa: E402


def varre():
    """Devolve (achados, censo) no formato do roda_qa."""
    exclusivos, celulas, por, troca, conflito, total = camada_sinnoh.plano()
    troca = set(troca)
    achados = []
    for mapa, x, y, rot, loc in celulas:
        classe = "trava" if (rot, loc) in troca else "falso positivo"
        achados.append(dict(regra="Z1", classe=classe, regiao="Sinnoh", mapa=mapa,
                            x=x, y=y + 1,
                            detalhe="cabeça tampada por %s 0x%03x em (%d,%d)" % (rot, loc, x, y)))
    censo = dict(tilesets=len(exclusivos), andaveis=total, tampadas=len(celulas))
    return achados, censo


def demo():
    """A lente tem que morder: devolve um metatile consertado a NORMAL e cobra o achado."""
    ruim = 0
    achados, _ = varre()
    travas = [a for a in achados if a["classe"] == "trava"]
    if travas:
        print("  lente_camada DEMO: a árvore tem %d trava(s) Z1, ex. %s" % (len(travas), travas[0]["detalhe"]))
        ruim = 1
    # Mutação plantada: a copa 0x1d6 do GeneralSinnoh volta a NORMAL só na
    # memória. Ela tampa a cabeça em Floaroma Meadow e em dezenas de rotas.
    ts = camada_sinnoh.tileset("gTileset_GeneralSinnoh")
    antes = ts[0][0x1D6]
    ts[0][0x1D6] = camada_sinnoh.NORMAL
    try:
        mutado, _ = varre()
        if not any(a["classe"] == "trava" and "0x1d6" in a["detalhe"] for a in mutado):
            print("  lente_camada DEMO: a copa 0x1d6 voltou a NORMAL e a lente não viu")
            ruim = 1
    finally:
        ts[0][0x1D6] = antes
    # Tem que medir de verdade: Sinnoh sem células andáveis é leitura quebrada.
    _, censo = varre()
    if censo["andaveis"] < 50000 or censo["tilesets"] < 20:
        print("  lente_camada DEMO: censo pequeno demais %s" % censo)
        ruim = 1
    if not ruim:
        print("demo ok")
    return ruim


def main():
    if "--demo" in sys.argv:
        return demo()
    achados, censo = varre()
    print("tilesets %(tilesets)d, células andáveis %(andaveis)d, cabeças tampadas %(tampadas)d" % censo)
    for a in achados:
        print("  %-4s %-15s %-28s %s" % (a["regra"], a["classe"], a["mapa"], a["detalhe"]))
    print("%d trava(s)" % sum(1 for a in achados if a["classe"] == "trava"))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
