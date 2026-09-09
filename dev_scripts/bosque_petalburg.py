#!/usr/bin/env python3
"""Refino de `PetalburgCity` (tema BOSQUE E MAR), no `gTileset_Petalburg`.

Segunda cidade do lote das três que dividem o `gTileset_Petalburg`. O KIT de
metatiles já entrou inteiro no commit de `LittlerootTown` (`mato_littleroot.py`),
e este arquivo IMPORTA aquele módulo: o motor, os portões, o auto-teste e as 25
peças são os mesmos, e o que muda é o plano do mapa. Se o kit ainda não estiver
no `metatiles.bin`, rodar com `--aplicar` o escreve de novo, e a escrita é
idempotente (locais fixos, 144 a 168).

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: `PetalburgCity` gasta 42,4% do chão andável a pé
(140 células de 330) com o metatile 1, a grama lisa do `gTileset_General`. Ela
não é o tapete que Littleroot era, porque o Emerald já desenhou aqui uma rede de
RUA DE AREIA ligando as portas (o autotile 280 a 298, 102 células somadas), mas
tudo que não é rua, prédio, árvore ou lago é um único verde chapado.

O QUE ESTA PASSADA FAZ DE DIFERENTE DE LITTLEROOT, e a diferença é de desenho,
não de código:

  1. NÃO TEM TRILHA. O gerador sabe traçar um caminho de custo mínimo ligando as
     portas, e foi assim que a rua de Littleroot nasceu. Aqui isso seria uma
     SEGUNDA rede de caminho correndo em paralelo à rua de areia que já existe,
     duas ruas dizendo a mesma coisa. `trilha=None` desliga o traçado e a cidade
     recebe só remendo, mobília e ruído.
  2. TEM PRAIA. `PetalburgCity` tem 141 células de água (dois lagos, medidos pelo
     comportamento do metatile), e o remendo de AREIA desta passada só é aceito
     se ENCOSTAR na água, a duas células de Chebyshev. É a opção `perto="agua"`,
     que entrou no motor nesta rodada: sem ela o gerador espalharia areia pelo
     meio do bosque, que lê como buraco e não como margem. A areia do remendo é o
     MESMO autotile da rua da cidade (280 a 298), então a margem nova casa de
     desenho com a rua velha por construção.
  3. O BOSQUE. Os remendos de GRAMA GASTA (o autotile 464 a 482, verde-menta com
     pinta amarela) são as clareiras encostadas na linha de árvores, que é o que
     liga visualmente a cidade à Petalburg Woods do lado de fora.

A ARMADILHA DOS QUATRO LAYOUTS DE KALOS, e ela é DESTA cidade, não das outras
duas. O `data/layouts/layouts.json` tem QUATRO layouts a mais apontando para o
`gTileset_Petalburg` (`SnowbelleCity_Layout`, `KiloudeCity_Layout`,
`VictoryRoad_Kalos_Layout` e `KalosLeague_Layout`) e os quatro têm
`blockdata_filepath` igual a `data/layouts/PetalburgCity/map.bin`. São esboços de
Kalos que ainda EMPRESTAM o mapa de Petalburg e não têm `map.bin` próprio.
Mexer neste arquivo mexe nos quatro POR CONSTRUÇÃO, e isso é fato medido, não
risco escondido: os quatro passam a mostrar a Petalburg refinada, que é
exatamente o que mostravam antes, só que refinada.

Uso:
    python3 dev_scripts/bosque_petalburg.py
    python3 dev_scripts/bosque_petalburg.py --aplicar
    python3 dev_scripts/bosque_petalburg.py --desfazer
    python3 dev_scripts/bosque_petalburg.py --demo
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import enfeita_cidades as E          # noqa: E402
import mato_littleroot as M          # noqa: E402

# O bloco de teste DESTA rodada é o único que o varredor de corredores pula: os
# casos dele foram escritos DEPOIS do desenho e a partir dele.
E.BLOCO_PROPRIO = "211_bosque_petalburg.json"

ALVO = "PetalburgCity"
CIDADE = dict(
    # sem trilha: a cidade já tem a rua de areia do Emerald ligando as portas
    trilha=None,
    remendos=[
        # a PRAIA: só encostada na água, e é a opção que entrou no motor aqui
        dict(familia="areia", quantos=3, larg=(3, 4), alt=(3, 3), espaco=2,
             semente=0x501, perto="agua", raio=2),
        # o BOSQUE: clareiras de grama gasta
        dict(familia="gasta", quantos=5, larg=(3, 5), alt=(3, 4), espaco=2,
             semente=0x502),
        dict(familia="gasta", quantos=4, larg=(3, 3), alt=(3, 3), espaco=2,
             semente=0x503),
        dict(familia="terra", quantos=2, larg=(3, 3), alt=(3, 3), espaco=3,
             semente=0x504),
    ],
    regioes_antes=True,
    ruido=[(M.CARIMBO, "grama")],
    moveis={"moita redonda": (6, 4), "matacao": (3, 6), "pedra": (3, 5),
            "pedra virada": (3, 5), "arbusto": (6, 4), "touceira": (5, 5),
            "touceira espelhada": (5, 5), "mourao": (4, 6)},
    cercas=2, cerca_comp=(3, 4), cerca_espaco=8,
    min_regiao=30,
)


def main():
    if "--desfazer" in sys.argv:
        return M.desfaz(ALVO)
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return M.demo(ALVO, CIDADE)
    return M.roda(ALVO, CIDADE, "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
