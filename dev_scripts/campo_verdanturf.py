#!/usr/bin/env python3
"""Refino de `VerdanturfTown` (tema CAMPO FLORIDO), no `gTileset_Mauville`.

Segunda e última cidade do lote das duas que dividem o `gTileset_Mauville`. O
KIT de metatiles entrou INTEIRO no commit de `MauvilleCity`
(`eletrica_mauville.py`), com as peças das duas cidades, e este arquivo IMPORTA
aquele módulo: motor, portões, auto-teste e as 55 peças são os mesmos, e o
`metatiles.bin` NÃO MUDA nesta passada. O que muda aqui é só o
`data/layouts/VerdanturfTown/map.bin`.

O QUE ESTA VILA TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` nesta
árvore em 09/09/2026: das 231 células andáveis a pé, 98 (42,4%) são o metatile
516, a relva curta do próprio `gTileset_Mauville`, e outras 60 (26,0%) são o
metatile 1, a grama lisa do `gTileset_General`. As duas somam 68,4%, e com o 517
(26 células) o `liso3` chega a 79,7%, o mais alto das duas cidades desta dupla.
A vila do ar puro, do Contest e do túnel Rusturf é um lençol verde de dois tons
com quatro prédios em cima.

DOIS CARIMBOS COM DOIS ATRIBUTOS DIFERENTES, e essa é a diferença dela para
`MauvilleCity`. Lá as duas famílias (grama e calçada) têm o MESMO atributo,
0x0000. Aqui não:

    família   carimbo(s)   atributo   comportamento          células
    relva     516, 517       0x0007   MB_SHORT_GRASS             124
    grama     1              0x0000   MB_NORMAL                   60

`MB_SHORT_GRASS` é o que faz a pegada aparecer atrás do jogador na relva de
Verdanturf. O portão 4 do `portao_planta.py` cobra `(comportamento, layerType)`
idêntico em toda célula que continua andável, então toda variante de relva sai
com 0x0007 bit a bit e toda variante de grama com 0x0000 bit a bit. Trocar um
pelo outro não quebraria build nenhum e apareceria só dentro do jogo, na hora em
que a pegada sumisse.

O QUE ESTA CIDADE TEM QUE `MauvilleCity` NÃO TEM: as FLORES ANIMADAS. Os seis
metatiles de canteiro que o kit criou (dois grupos de três, branco e amarelo)
apontam para os mesmos tiles pinados 96 a 159 dos metatiles 520 a 535, mas com o
atributo 0x0007 da relva no lugar do 0x0000 original. Eles só são usados AQUI:
`MauvilleCity` não tem uma única célula de relva. O efeito é canteiro de flor que
BALANÇA dentro do jogo, e ele sai de graça, porque `InitTilesetAnim_Mauville`
roda sempre que o tileset carrega, em qualquer um dos sete mapas irmãos.

O QUE ELA NÃO FAZ, e o motivo é medido:
  - NÃO TEM CALÇADA. A família de calçada existe no kit e cobre 176 células em
    `MauvilleCity`; aqui ela tem ZERO células, porque `VerdanturfTown` não usa
    nenhum dos cinco metatiles de calçada do `gTileset_General`. Pôr calçada onde
    não há rua seria desenhar cidade em cima de vila.
  - NÃO TEM POSTE DE LUZ NEM MÁQUINA DE BEBIDA. As peças estão no kit, mas o tema
    daqui é feira de vila: cerca de madeira, bancada de feira, moita escura,
    placa e canteiro. Poste de rua ao lado do salão de Contest lê como outro
    mapa, que é a mesma poda que Dewford fez com a espreguiçadeira.
  - NÃO TEM ÁGUA. Medido pelo comportamento do metatile: `VerdanturfTown` tem
    ZERO célula de água, então o portão da água passa por construção, e isso é
    dito e não fabricado.

Uso:
    python3 dev_scripts/campo_verdanturf.py
    python3 dev_scripts/campo_verdanturf.py --aplicar
    python3 dev_scripts/campo_verdanturf.py --desfazer
    python3 dev_scripts/campo_verdanturf.py --demo
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import eletrica_mauville as M        # noqa: E402

ALVO = "VerdanturfTown"
CIDADE = M.CIDADE_VERDANTURF


def main():
    if "--desfazer" in sys.argv:
        return M.desfaz(ALVO)
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return M.demo(ALVO, CIDADE)
    if "--so-tileset" in sys.argv:
        metas, attrs, _c = M.desenha_kit()
        M.grava_tileset(metas, attrs)
        print("tileset escrito: 0 tiles, %d metatiles" % len(metas))
        return 0
    return M.roda(ALVO, CIDADE, "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
