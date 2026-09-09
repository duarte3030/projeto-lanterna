#!/usr/bin/env python3
"""Refino de `OldaleTown` (tema VILAREJO DE ESTRADA), no `gTileset_Petalburg`.

Terceira e última cidade do lote das três que dividem o `gTileset_Petalburg`. O
KIT de metatiles entrou inteiro no commit de `LittlerootTown`
(`mato_littleroot.py`) e este arquivo IMPORTA aquele módulo: motor, portões,
auto-teste e as 25 peças são os mesmos.

O QUE ESTA CIDADE TEM DE ERRADO, e ela é o caso mais interessante das três,
medido pela `dev_scripts/regua_cidades.py` nesta árvore em 09/09/2026:
`OldaleTown` tem DOIS carimbos quase do mesmo tamanho. O metatile 1, a grama
lisa, come 70 das 239 células andáveis a pé (29,3%), e o metatile 473, o MIOLO
do autotile de grama gasta, come outras 69 (28,9%). Somados, dois metatiles
cobrem 58,2% do chão: o vilarejo é um tapete verde com um tapete verde-menta
recortado dentro dele.

POR ISSO A PASSADA AQUI É DE RUÍDO EM DOSE DUPLA, e essa é a diferença dela para
as outras duas. As duas famílias têm nove arranjos cada (espelho, giro e mistura
dos tiles 2 e 3 da grama e 266 e 282 da grama gasta), e as duas entram: a grama
recebe os arranjos da grama e o MIOLO da grama gasta recebe os arranjos da grama
gasta. A borda do recorte de grama gasta (as oito peças 464, 465, 466, 472, 474,
480, 481 e 482) NÃO É TOCADA, e isso não é detalhe: o ruído só troca a célula
cujo metatile é EXATAMENTE o miolo, então o contorno do recorte, que é a arte de
transição desenhada pelo Emerald, continua exatamente onde estava. Trocar uma
peça de borda por um arranjo do miolo abriria costura, e é o erro que a sabotagem
N6 do auto-teste acusa.

O QUE ELA NÃO FAZ, e o motivo é medido:
  - NÃO TEM TRILHA. O gerador só pinta chão em célula do carimbo (o metatile 1),
    e em `OldaleTown` a grama do carimbo está partida em canto e beira, com o
    recorte de grama gasta ocupando o meio da praça. Um caminho traçado ali sairia
    em pedaços de duas e três células em volta do recorte, e a abertura 3x3 comeria
    quase tudo. O vilarejo já tem a praça central desenhada; o que faltava era ela
    parar de ser chapada.
  - NÃO TEM PRAIA. `OldaleTown` tem ZERO célula de água (medido pelo
    comportamento do metatile), então a opção `perto="agua"` que Petalburg usou
    não tem onde encostar aqui.

Uso:
    python3 dev_scripts/estrada_oldale.py
    python3 dev_scripts/estrada_oldale.py --aplicar
    python3 dev_scripts/estrada_oldale.py --desfazer
    python3 dev_scripts/estrada_oldale.py --demo
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import enfeita_cidades as E          # noqa: E402
import mato_littleroot as M          # noqa: E402

E.BLOCO_PROPRIO = "212_estrada_oldale.json"

ALVO = "OldaleTown"
# O MIOLO do autotile de grama gasta do `gTileset_General`, o segundo carimbo
# desta cidade: 69 células, 28,9%.
CARIMBO2 = 473

CIDADE = dict(
    trilha=None,
    remendos=[
        dict(familia="terra", quantos=3, larg=(3, 4), alt=(3, 3), espaco=2,
             semente=0x701),
        dict(familia="gasta", quantos=3, larg=(3, 3), alt=(3, 3), espaco=2,
             semente=0x702),
    ],
    regioes_antes=True,
    # As DUAS bases: a praça central desta cidade é o miolo do recorte de grama
    # gasta, e é lá que cabe mobília. Medido nesta árvore: as 70 células de grama
    # do carimbo 1 dão UM único canto de retângulo 3x3, e 49 delas ficam fora do
    # gelo de evento e de corredor; sem a segunda base a cidade fecharia com
    # dezessete peças e nada no meio. As peças da base clara são cópias com a
    # camada de baixo do metatile 473, e por isso não deixam quadrado verde em
    # volta quando pousam na praça.
    bases=[M.CARIMBO, CARIMBO2],
    beira_da_mancha=True,
    # RUÍDO EM DOSE DUPLA: a grama recebe arranjo de grama e o MIOLO da grama
    # gasta recebe arranjo de grama gasta. A borda do recorte não entra.
    ruido=[(M.CARIMBO, "grama"), (CARIMBO2, "gasta")],
    moveis={"moita redonda": (4, 4), "matacao": (2, 6), "pedra": (3, 5),
            "pedra virada": (3, 5), "arbusto": (4, 4), "touceira": (3, 5),
            "touceira espelhada": (3, 5), "mourao": (3, 6),
            "moita redonda clara": (4, 5), "matacao clara": (2, 7),
            "pedra clara": (3, 6), "pedra virada clara": (3, 6),
            "arbusto clara": (4, 5), "touceira clara": (3, 6),
            "touceira espelhada clara": (3, 6), "mourao clara": (3, 7)},
    cercas=4, cerca_comp=(3, 4), cerca_espaco=7,
    # NOVE, e o número é medido, não escolhido: as 70 células do carimbo 1 desta
    # cidade dão UM único canto de retângulo 3x3 (em (2,12)), então cabe um
    # remendo de terra e mais nenhum. O miolo do recorte de grama gasta NÃO
    # recebe remendo: o autotile de terra do gTileset_General tem a franja
    # desenhada contra a grama VERDE, e pousá-lo no verde-menta da praça poria
    # uma orla verde em volta do buraco de terra, que é a costura que esta onda
    # inteira existe para evitar.
    min_regiao=9,
)


def main():
    if "--desfazer" in sys.argv:
        return M.desfaz(ALVO)
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return M.demo(ALVO, CIDADE)
    return M.roda(ALVO, CIDADE, "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
