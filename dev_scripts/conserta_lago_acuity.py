#!/usr/bin/env python3
"""Liga o Lago Acuity ao Acuity Lakefront, tirando o jogador de dentro da água.

Uso:
    python3 dev_scripts/conserta_lago_acuity.py --demo    # só se prova, não grava
    python3 dev_scripts/conserta_lago_acuity.py           # grava (idempotente)

O QUE ESTAVA ERRADO, medido em 12/08/2026 no disco e conferido no emulador
-------------------------------------------------------------------------
O `warp 0` do `LakeAcuity` ficava em (24,24), que é `MB_POND_WATER` com
elevação 1, no meio do lago: quem chegasse ali alcançava **um** tile a pé, ele
mesmo. Só que ninguém chegava, e é isso que o relatório anterior não tinha
medido: o warp do outro lado, `AcuityLakefront` (32,40), está sobre
`MB_SAND`, e `IsWarpMetatileBehavior` não dispara em areia. Ou seja o par
{LakeAcuity, AcuityCavern} era uma ilha do grafo de mapas, alcançável só pelo
menu de debug, que é justamente o que o T94.5 usa.

Fiação medida, antes:
    AcuityLakefront (32,40) MB_SAND         -> LakeAcuity warp 0     MORTO
    AcuityLakefront (32,39) porta           -> LakeAcuityLowWater    vivo
    LakeAcuity      (24,24) MB_POND_WATER   -> AcuityLakefront       MORTO
    LakeAcuity      (23,29) porta           -> AcuityCavern          vivo
    AcuityCavern    (16,21) seta sul        -> LakeAcuity warp 1     vivo

O CONSERTO, e por que é este
----------------------------
Copia o padrão que o Lago VERITY já usa e que funciona (medido:
`VerityLakefront` (2,4) `MB_NORTH_ARROW_WARP` -> `LakeVerity` (38,43)
`MB_SOUTH_ARROW_WARP`):

1. `AcuityLakefront` (32,40) passa a ser o metatile 484 do
   `gTileset_GeneralSinnoh`, que é `MB_NORTH_ARROW_WARP` (o mesmo desenho de
   soleira que outros 20 pontos de Sinnoh já usam). O warp 0, que já estava
   nessa coordenada, passa a disparar.
2. O `warp 0` do `LakeAcuity` sai de (24,24), no meio da água, e vai para
   (24,31), na plataforma da boca da caverna, a dois passos do `coord_event`
   (23,30) que dispara a cutscene da Galáctica. Não é (23,31) porque ali mora o
   template do RIVAL, e (22,31) o da JUPITER: nascer em cima de object_event é a
   armadilha dos guardas de insígnia da Liga de Sinnoh (casos T81.*). O tile vira o metatile 311 do
   mesmo tileset, que é `MB_SOUTH_ARROW_WARP`, então o jogador sai por onde
   entrou apertando para baixo.

Colisão 0 e elevação 3 são preservadas nos dois tiles: só o id do metatile
muda, porque comportamento mora no metatile e não no blockdata.

O QUE ESTE CONSERTO NÃO FAZ, e está aberto de propósito
-------------------------------------------------------
- **A geometria do lago continua errada.** Medido contra
  `fontes-mapas/pokeplatinum/res/field/events/events_lake_acuity.json`: a fonte
  entra por quatro tiles no bordo sul, e na nossa conversão a praia sul (42
  tiles) não se liga à plataforma da caverna (25 tiles), porque virou água um
  caminho que na fonte é terra. Consertar isso é RECONVERTER o `blockdata` a
  partir da grade de permissão do pokeplatinum, que é trabalho de leva, não de
  fechamento. Enquanto isso, a entrada cai direto na boca da caverna: o jogador
  entra, vê a cena e sai, e nenhuma parte do mapa prende ninguém.
- **`LakeAcuityLowWater` perde a única entrada a pé.** (32,39) é alcançável só
  por (32,40), e (32,40) agora é seta. Medido antes de aceitar: aquele mapa tem
  ZERO objetos, ZERO coord_events, ZERO bg_events e um `scripts.inc` de duas
  linhas, ou seja é sobra de conversão sem conteúdo. O warp dele continua no
  lugar, então religá-lo é mudar uma coordenada quando alguém decidir o que ele
  deve ser.
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# metatile -> comportamento, do gTileset_GeneralSinnoh (primário, compartilhado
# pelos dois mapas). Os números saíram da varredura de
# `metatile_attributes.bin`, não de memória: 484 = MB_NORTH_ARROW_WARP,
# 311 = MB_SOUTH_ARROW_WARP.
SETA_NORTE = 484
SETA_SUL = 311

# (layout, x, y, metatile novo). Colisão e elevação ficam como estão.
TILES = [
    ("LAYOUT_ACUITY_LAKEFRONT", 32, 40, SETA_NORTE),
    ("LAYOUT_LAKE_ACUITY", 24, 31, SETA_SUL),
]
# (24,31) e não (23,31): medido no `map.json` do mapa, (23,31) é o template do
# RIVAL e (22,31) o da JUPITER, e nascer em cima de object_event é a armadilha
# dos guardas de insígnia da Liga de Sinnoh (casos T81.*). De (24,31) o jogador
# sobe para (24,30) e anda um tile para oeste até o `coord_event` (23,30).
WARP = ("LakeAcuity", 0, 24, 31)     # mapa, índice do warp, x, y


def layouts():
    return {l["id"]: l for l in
            json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}


def le_palavra(lay, x, y):
    b = open(f"{RAIZ}/{lay['blockdata_filepath']}", "rb").read()
    i = (y * lay["width"] + x) * 2
    return struct.unpack("<H", b[i:i + 2])[0]


def grava_palavra(lay, x, y, palavra):
    caminho = f"{RAIZ}/{lay['blockdata_filepath']}"
    b = bytearray(open(caminho, "rb").read())
    i = (y * lay["width"] + x) * 2
    b[i:i + 2] = struct.pack("<H", palavra)
    open(caminho, "wb").write(bytes(b))


def aplica(gravar=True):
    """Devolve a lista do que mudou. Idempotente: rodar de novo devolve [] ."""
    mudou = []
    tabela = layouts()
    for lid, x, y, novo in TILES:
        lay = tabela[lid]
        antes = le_palavra(lay, x, y)
        # só o id do metatile muda; colisão e elevação são preservadas
        depois = (antes & ~0x3FF) | novo
        if antes != depois:
            if gravar:
                grava_palavra(lay, x, y, depois)
            mudou.append(f"{lid} ({x},{y}) metatile {antes & 0x3FF} -> {novo}")

    mapa, indice, x, y = WARP
    caminho = f"{RAIZ}/data/maps/{mapa}/map.json"
    d = json.load(open(caminho))
    wp = d["warp_events"][indice]
    if (wp["x"], wp["y"]) != (x, y):
        mudou.append(f"{mapa} warp {indice} ({wp['x']},{wp['y']}) -> ({x},{y})")
        wp["x"], wp["y"] = x, y
        if gravar:
            json.dump(d, open(caminho, "w"), indent=2, ensure_ascii=False)
            open(caminho, "a").write("\n")
    return mudou


def demo():
    """Prova com MUTAÇÃO PLANTADA: sujo o tile de propósito, exijo que a
    ferramenta conserte, e exijo que a segunda passada não mude mais nada."""
    tabela = layouts()
    lay = tabela["LAYOUT_LAKE_ACUITY"]
    # coordenada do tile do lago vem de TILES, e não chumbada: quando ela mudou
    # de (23,31) para (24,31) a demo passou a testar o tile errado e reprovou
    # com a ferramenta certa, que é o pior tipo de mentira de validador.
    _, ALVO_X, ALVO_Y, _ = next(t for t in TILES if t[0] == "LAYOUT_LAKE_ACUITY")
    guardado = le_palavra(lay, ALVO_X, ALVO_Y)
    # guarda TODOS os tiles que `aplica` pode escrever, e não só o do lago: a
    # primeira versão restaurava um e deixava o outro sujo na árvore, que é
    # exatamente o tipo de escrita silenciosa que a lição 4 do ESTADO cobra.
    guardados = {(lid, x, y): le_palavra(tabela[lid], x, y)
                 for lid, x, y, _ in TILES}
    guardado_json = open(f"{RAIZ}/data/maps/LakeAcuity/map.json").read()
    falhas = []
    try:
        # (a) estado plantado: metatile de areia e warp de volta na água
        grava_palavra(lay, ALVO_X, ALVO_Y, (guardado & ~0x3FF) | 513)
        d = json.loads(guardado_json)
        d["warp_events"][0]["x"], d["warp_events"][0]["y"] = 24, 24
        json.dump(d, open(f"{RAIZ}/data/maps/LakeAcuity/map.json", "w"),
                  indent=2, ensure_ascii=False)

        primeira = aplica()
        if len(primeira) < 2:
            falhas.append(f"a mutação plantada não foi consertada: {primeira}")
        depois = le_palavra(layouts()["LAYOUT_LAKE_ACUITY"], ALVO_X, ALVO_Y)
        if depois & 0x3FF != SETA_SUL:
            falhas.append(f"metatile ficou {depois & 0x3FF}, esperava {SETA_SUL}")
        if (depois >> 10) & 3 or (depois >> 12) & 0xF != 3:
            falhas.append(f"colisão/elevação não foram preservadas: 0x{depois:04X}")
        d = json.load(open(f"{RAIZ}/data/maps/LakeAcuity/map.json"))
        if (d["warp_events"][0]["x"], d["warp_events"][0]["y"]) != (ALVO_X, ALVO_Y):
            falhas.append("o warp 0 não foi movido")

        # (b) idempotência: a segunda passada não acha nada para fazer
        segunda = aplica()
        if segunda:
            falhas.append(f"não é idempotente, a segunda passada mudou: {segunda}")

        # (c) contraprova: o destino tem que ser terra alcançável, e não água.
        #     Se alguém apontar o warp para o lago de novo, isto acusa.
        alvo = le_palavra(layouts()["LAYOUT_LAKE_ACUITY"], ALVO_X, ALVO_Y)
        if (alvo >> 12) & 0xF != 3:
            falhas.append("o tile de destino não está na elevação 3 (terra)")
        agua = le_palavra(layouts()["LAYOUT_LAKE_ACUITY"], 24, 24)
        if (agua >> 12) & 0xF == 3:
            falhas.append("(24,24) deixou de ser água; a premissa do conserto mudou")
    finally:
        atual = layouts()
        for (lid, x, y), palavra in guardados.items():
            grava_palavra(atual[lid], x, y, palavra)
        open(f"{RAIZ}/data/maps/LakeAcuity/map.json", "w").write(guardado_json)

    for f in falhas:
        print(f"[FALHA] {f}")
    if not falhas:
        print("demo OK: mutação plantada consertada, colisão e elevação preservadas, "
              "idempotente, e o destino é terra e não água.")
    return 1 if falhas else 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        sys.exit(demo())
    for linha in aplica() or ["nada a fazer (já estava consertado)"]:
        print(linha)
