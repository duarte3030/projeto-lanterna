#!/usr/bin/env python3
"""Poe os grupos de mapa em blocos contiguos por regiao, na quebra unica de save.

    python3 dev_scripts/reorganiza_grupos.py            # tabela, nao escreve
    python3 dev_scripts/reorganiza_grupos.py --demo     # autoteste
    python3 dev_scripts/reorganiza_grupos.py --aplicar  # escreve

O que muda, e por que so aqui
-----------------------------
`group_order` de `data/maps/map_groups.json` e a ORDEM dos grupos, e o indice
de cada grupo e gravado na save (`SaveBlock1.location.mapGroup`). Reordenar
quebra a save de quem estava parado em qualquer lugar, entao isto so pode
acontecer dentro da quebra unica (`SAVE_LAYOUT_REVISION` 1 -> 2).

Depois desta onda a ordem passa a ser: HOENN, KANTO, JOHTO, SINNOH e por fim os
grupos COMUNS (mapas dinamicos e salas de link, que nao pertencem a regiao
nenhuma). Cada bloco e contiguo, e isso e o que faz `GetCurrentRegion`
(`include/regions.h`) continuar podendo separar Johto por intervalo de grupo.

Hoenn continua PRIMEIRO, e o grupo 0 continua sendo `gMapGroup_TownsAndRoutes`,
porque `src/overworld.c` (`ShouldLegendaryMusicPlayAtLocation`) e
`src/field_specials.c` (`AbnormalWeatherHasExpired`) comparam
`mapGroup == 0` na mao para reconhecer o mapa de Hoenn.

Os tres mapas presos (decisao 25 do Gui)
----------------------------------------
`Route116_TunnelersRestHouse`, `Route117_PokemonDayCare` e
`Route121_SafariZoneEntrance` eram o unico morador vivo de tres grupos que
Galar tinha lotado. Eles vao para `gMapGroup_SpecialArea`, que e o balde de
instalacao de rota de Hoenn (ja guarda a Zona Safari inteira, que e justamente
onde a entrada da Route 121 leva, e o Trainer Hill da Route 111), e os tres
grupos vazios somem junto com os 23 de Unova e Galar: 26 vagas de grupo
liberadas.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRUPOS = os.path.join(RAIZ, "data/maps/map_groups.json")

# Mudanca de casa dos tres mapas presos (decisao 25 do Gui).
MUDANCAS = {
    "Route116_TunnelersRestHouse": "gMapGroup_SpecialArea",
    "Route117_PokemonDayCare": "gMapGroup_SpecialArea",
    "Route121_SafariZoneEntrance": "gMapGroup_SpecialArea",
}

HOENN = [
    "gMapGroup_TownsAndRoutes",
    "gMapGroup_IndoorLittleroot",
    "gMapGroup_IndoorOldale",
    "gMapGroup_IndoorDewford",
    "gMapGroup_IndoorLavaridge",
    "gMapGroup_IndoorFallarbor",
    "gMapGroup_IndoorVerdanturf",
    "gMapGroup_IndoorPacifidlog",
    "gMapGroup_IndoorPetalburg",
    "gMapGroup_IndoorSlateport",
    "gMapGroup_IndoorMauville",
    "gMapGroup_IndoorRustboro",
    "gMapGroup_IndoorFortree",
    "gMapGroup_IndoorLilycove",
    "gMapGroup_IndoorMossdeep",
    "gMapGroup_IndoorSootopolis",
    "gMapGroup_IndoorEverGrande",
    "gMapGroup_IndoorRoute104",
    "gMapGroup_IndoorRoute104Prototype",
    "gMapGroup_IndoorRoute109",
    "gMapGroup_IndoorRoute110",
    "gMapGroup_IndoorRoute111",
    "gMapGroup_IndoorRoute112",
    "gMapGroup_IndoorRoute113",
    "gMapGroup_IndoorRoute114",
    "gMapGroup_IndoorRoute119",
    "gMapGroup_IndoorRoute123",
    "gMapGroup_IndoorRoute124",
    "gMapGroup_Dungeons",
    "gMapGroup_SpecialArea",
]

KANTO = [
    "gMapGroup_TownsAndRoutes_Frlg",
    "gMapGroup_IndoorPallet_Frlg",
    "gMapGroup_IndoorViridian_Frlg",
    "gMapGroup_IndoorPewter_Frlg",
    "gMapGroup_IndoorCerulean_Frlg",
    "gMapGroup_IndoorLavender_Frlg",
    "gMapGroup_IndoorVermilion_Frlg",
    "gMapGroup_IndoorCeladon_Frlg",
    "gMapGroup_IndoorFuchsia_Frlg",
    "gMapGroup_IndoorCinnabar_Frlg",
    "gMapGroup_IndoorSaffron_Frlg",
    "gMapGroup_IndoorIndigoPlateau_Frlg",
    "gMapGroup_IndoorRoute2_Frlg",
    "gMapGroup_IndoorRoute4_Frlg",
    "gMapGroup_IndoorRoute5_Frlg",
    "gMapGroup_IndoorRoute6_Frlg",
    "gMapGroup_IndoorRoute7_Frlg",
    "gMapGroup_IndoorRoute8_Frlg",
    "gMapGroup_IndoorRoute10_Frlg",
    "gMapGroup_IndoorRoute11_Frlg",
    "gMapGroup_IndoorRoute12_Frlg",
    "gMapGroup_IndoorRoute15_Frlg",
    "gMapGroup_IndoorRoute16_Frlg",
    "gMapGroup_IndoorRoute18_Frlg",
    "gMapGroup_IndoorRoute22_Frlg",
    "gMapGroup_IndoorRoute25_Frlg",
    "gMapGroup_IndoorOneIsland_Frlg",
    "gMapGroup_IndoorTwoIsland_Frlg",
    "gMapGroup_IndoorThreeIsland_Frlg",
    "gMapGroup_IndoorFourIsland_Frlg",
    "gMapGroup_IndoorFiveIsland_Frlg",
    "gMapGroup_IndoorSixIsland_Frlg",
    "gMapGroup_IndoorSevenIsland_Frlg",
    "gMapGroup_IndoorTwoIslandRoute_Frlg",
    "gMapGroup_IndoorThreeIslandRoute_Frlg",
    "gMapGroup_IndoorFiveIslandRoute_Frlg",
    "gMapGroup_IndoorSixIslandRoute_Frlg",
    "gMapGroup_IndoorSevenIslandRoute_Frlg",
    "gMapGroup_Dungeons_Frlg",
    "gMapGroup_SpecialArea_Frlg",
]

# TownsAndRoutes_Johto tem de ser o PRIMEIRO e SpecialArea_Johto o ULTIMO:
# GetCurrentRegion compara o intervalo MAP_GROUP(MAP_NEW_BARK_TOWN) ate
# MAP_GROUP(MAP_WORLD_HUB2), que sao esses dois.
JOHTO = [
    "gMapGroup_TownsAndRoutes_Johto",
    "gMapGroup_IndoorNewBark_Johto",
    "gMapGroup_IndoorCherrygrove_Johto",
    "gMapGroup_IndoorViolet_Johto",
    "gMapGroup_IndoorAzalea_Johto",
    "gMapGroup_IndoorGoldenrod_Johto",
    "gMapGroup_IndoorEcruteak_Johto",
    "gMapGroup_IndoorOlivine_Johto",
    "gMapGroup_IndoorCianwood_Johto",
    "gMapGroup_IndoorMahogany_Johto",
    "gMapGroup_IndoorBlackthorn_Johto",
    "gMapGroup_IndoorJohtoRoutes_Johto",
    "gMapGroup_IndoorKantoRoutes_Johto",
    "gMapGroup_JohtoPortas",
    "gMapGroup_Dungeons_Johto",
    "gMapGroup_SpecialArea_Johto",
]

SINNOH = [
    "gMapGroup_SinnohTownsRoutes",
    "gMapGroup_IndoorTwinleaf",
    "gMapGroup_IndoorSandgem",
    "gMapGroup_IndoorJubilife",
    "gMapGroup_IndoorOreburgh",
    "gMapGroup_IndoorFloaroma",
    "gMapGroup_IndoorSinnoh",
    "gMapGroup_IndoorSinnohPortas",
    "gMapGroup_IndoorSinnohPortas2",
    "gMapGroup_SinnohInteriores",
    "gMapGroup_DungeonsSinnoh",
    "gMapGroup_SinnohCavernas",
    "gMapGroup_TeamGalactic",
    "gMapGroup_SinnohLeague",
    "gMapGroup_SpecialAreasSinnoh",
]

# Mapas que nao pertencem a regiao nenhuma: base secreta, sala de link, quadrado
# da Battle Pyramid, caminhao da abertura.
COMUM = [
    "gMapGroup_IndoorDynamic",
    "gMapGroup_Link_Frlg",
]

NOVA_ORDEM = HOENN + KANTO + JOHTO + SINNOH + COMUM


def indices(grupos):
    """nome do mapa -> (indice do grupo, indice dentro do grupo)."""
    saida = {}
    for gi, grupo in enumerate(grupos["group_order"]):
        for mi, nome in enumerate(grupos[grupo]):
            saida[nome] = (gi, mi)
    return saida


def reorganiza(grupos):
    novo = {"group_order": list(NOVA_ORDEM)}
    for grupo in grupos["group_order"]:
        novo.setdefault(grupo, list(grupos[grupo]))
    for mapa, destino in MUDANCAS.items():
        for grupo in list(novo):
            if grupo == "group_order":
                continue
            if mapa in novo[grupo] and grupo != destino:
                novo[grupo].remove(mapa)
                novo[destino].append(mapa)
    vazios = sorted(g for g in novo if g != "group_order" and not novo[g])
    for grupo in vazios:
        del novo[grupo]
        if grupo in novo["group_order"]:
            novo["group_order"].remove(grupo)
    saida = {"group_order": novo["group_order"]}
    for grupo in novo["group_order"]:
        saida[grupo] = novo[grupo]
    return saida, vazios


def confere(grupos, novo, vazios):
    """Nenhum mapa pode sumir, e nenhum grupo pode passar dos tetos."""
    antes = set()
    for grupo in grupos["group_order"]:
        antes |= set(grupos[grupo])
    depois = set()
    for grupo in novo["group_order"]:
        depois |= set(novo[grupo])
    erros = []
    if antes != depois:
        erros.append(f"mapas perdidos: {sorted(antes - depois)[:8]}")
        erros.append(f"mapas inventados: {sorted(depois - antes)[:8]}")
    if len(novo["group_order"]) > 255:
        erros.append(f"grupos demais: {len(novo['group_order'])}")
    for grupo in novo["group_order"]:
        if len(novo[grupo]) > 128:
            erros.append(f"{grupo} com {len(novo[grupo])} mapas")
    for grupo in novo["group_order"]:
        if len(novo[grupo]) != len(set(novo[grupo])):
            erros.append(f"{grupo} com mapa repetido")
    faltando = set(grupos["group_order"]) - set(NOVA_ORDEM) - set(vazios)
    sobrando = set(NOVA_ORDEM) - set(grupos["group_order"])
    if faltando:
        erros.append(f"grupo do disco vivo e fora da NOVA_ORDEM: {sorted(faltando)}")
    if sobrando:
        erros.append(f"grupo da NOVA_ORDEM que nao existe: {sorted(sobrando)}")
    return erros


def main():
    aplicar = "--aplicar" in sys.argv
    demo = "--demo" in sys.argv

    grupos = json.load(open(GRUPOS))
    velho = indices(grupos)
    novo, vazios = reorganiza(grupos)
    erros = confere(grupos, novo, vazios)
    atual = indices(novo)

    print(f"grupos: {len(grupos['group_order'])} -> {len(novo['group_order'])} "
          f"(de 255; {255 - len(novo['group_order'])} vagas)")
    print(f"grupos apagados por ficarem vazios: {len(vazios)}")
    for grupo in vazios:
        print(f"    {grupo}")
    print("mapas que mudaram de casa:")
    for mapa, destino in sorted(MUDANCAS.items()):
        print(f"    {mapa}: grupo {velho[mapa][0]} pos {velho[mapa][1]} -> "
              f"{destino} grupo {atual[mapa][0]} pos {atual[mapa][1]}")
    andaram = sum(1 for m in velho if velho[m] != atual[m])
    print(f"mapas cujo par (grupo, numero) andou: {andaram} de {len(velho)}")
    print("blocos:")
    inicio = 0
    for nome, bloco in (("HOENN", HOENN), ("KANTO", KANTO), ("JOHTO", JOHTO),
                        ("SINNOH", SINNOH), ("COMUM", COMUM)):
        vivos = [g for g in bloco if g in novo["group_order"]]
        print(f"    {nome:7s} grupos {inicio} a {inicio + len(vivos) - 1} "
              f"({len(vivos)} grupos, {sum(len(novo[g]) for g in vivos)} mapas)")
        inicio += len(vivos)
    maior = max(novo["group_order"], key=lambda g: len(novo[g]))
    print(f"maior grupo: {maior} com {len(novo[maior])} mapas (teto 128)")

    if erros:
        print("\nRECUSADO:")
        for erro in erros:
            print("   ", erro)
        return 1
    print("\nnenhum mapa perdido, nenhum teto estourado.")

    if demo:
        estragado = json.loads(json.dumps(novo))
        estragado[estragado["group_order"][0]].pop()
        if not confere(grupos, estragado, vazios):
            print("DEMO REPROVOU: a checagem nao viu o mapa sumido")
            return 1
        print("DEMO OK: mapa sumido plantado foi recusado")
        return 0

    if not aplicar:
        print("\n(nada foi escrito; use --aplicar)")
        return 0

    json.dump(novo, open(GRUPOS, "w"), indent=2, ensure_ascii=False)
    open(GRUPOS, "a").write("\n")
    print("\nAPLICADO em data/maps/map_groups.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
