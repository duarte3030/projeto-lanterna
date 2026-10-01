#!/usr/bin/env python3
"""Gera os lugares e a grade do mapa de região de JOHTO e de SINNOH.

Uso:
    python3 dev_scripts/mapa_voo_regioes.py            # regrava o .h gerado
    python3 dev_scripts/mapa_voo_regioes.py --confere  # só confere, sai 1 se mudaria

Por que existe (fila de bugs 3, 30/09/2026): o Gui abriu o FLY em Sinnoh e viu o
mapa de HOENN com "SINNOH NORTH" na caixa. Johto e Sinnoh não tinham mapa de
região: `GetRegionMapType` caía no `default` (Hoenn) e o MAPSEC de cada lugar é
apelido de um MAPSEC de GRUPO (`MAPSEC` é u8, ver o letreiro de mapa no ESTADO),
então nem a grade nem o nome podiam sair do `gRegionMapEntries`.

A saída, `src/data/region_map/region_map_johto_sinnoh.h`, é uma tabela de
LUGARES por região (nome, retângulo do ícone, flag de voo, ponto de pouso) e uma
grade 28x15 de índices de lugar, a mesma geometria do mapa de Hoenn. O código
do mapa trata o índice como um MAPSEC "virtual" (acima de 0xFF, só dentro do
mapa da região; nunca vai para a save).

A GRADE e o NOME de cada célula são COPIADOS, não inventados:
- Johto: pokemonHnS (Heart & Soul), `src/data/region_map/region_map_layout_johto.h`
  e `region_map_sections_johto.json`, a grade do `johtomap.png` dele.
- Sinnoh: Sinnoh-pokeemerald-expansion (LiderMorti00),
  `src/data/region_map/region_map_layout.h` e `region_map_sections.json`, a grade
  do `map.png` dele.
Os dois usam a mesma geometria do pokeemerald (MAP_WIDTH 28, MAP_HEIGHT 15), e
por isso a posição de cada cidade entra sem conversão.

O que é NOSSO é só: (1) o de-para de nome para o nome do letreiro
(`map_name_popup`), que é o que liga o lugar ao mapa onde o jogador está;
(2) o ponto de pouso, na frente da porta do Pokécenter de cada cidade, lido do
`map.json` (warp para o Pokécenter, uma célula abaixo); (3) as flags de voo.
"""
import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.environ.get(
    "FONTES_MAPAS",
    "/Users/duarte/Documents/CLAUDE/Claude Workspace - Pokemon Rom Hacks/"
    "Pokemon Claude/fontes-mapas")
SAIDA = os.path.join(RAIZ, "src", "data", "region_map", "region_map_johto_sinnoh.h")
LARGURA, ALTURA = 28, 15
NOME_MAX = 16  # MAP_NAME_LENGTH, include/region_map.h

REGIOES = {
    "Johto": {
        "layout": "hns/src/data/region_map/region_map_layout_johto.h",
        "secoes": "hns/src/data/region_map/region_map_sections_johto.json",
        "grupos": (70, 85),
    },
    "Sinnoh": {
        "layout": "sinnoh/src/data/region_map/region_map_layout.h",
        "secoes": "sinnoh/src/data/region_map/region_map_sections.json",
        "grupos": (86, 100),
    },
}

# Nome da fonte -> nome do letreiro desta ROM. Só grafia; o lugar é o mesmo.
DEPARA_NOME = {
    "MT MORTAR": "MT. MORTAR",
    "DRAGON'S DEN": "DRAGONS DEN",
    "MT CORONET": "MT. CORONET",
    "MT STARK": "MT. STARK",
    "SUNNYSHORE CITY": "SUNYSHORE CITY",
    "ROUTE  219": "ROUTE 219",
    "FIGHT ARE": "FIGHT AREA",
}
# Nome exibido (cabe em 16) -> nome do letreiro que também cai neste lugar.
APELIDO_POPUP = {
    "LIGHTHOUSE": "OLIVINE LIGHTHOUSE",
}

# Destinos de voo: nome do lugar -> (mapa de pouso, x, y, flag). O pouso é uma
# célula abaixo da porta do Pokécenter (warp_event do map.json); onde não há
# Pokécenter (New Bark, Twinleaf), abaixo da porta da casa do jogador. A Liga
# de Sinnoh pousa na frente da entrada, onde fica o Pokécenter dela.
VOO = {
    "Johto": [
        ("NEW BARK TOWN", "MAP_NEW_BARK_TOWN", "NewBarkTown", "MAP_NEW_BARK_TOWN_PLAYERS_HOUSE_1F", "FLAG_VISITED_NEW_BARK_TOWN"),
        ("CHERRYGROVE CITY", "MAP_CHERRYGROVE_CITY", "CherrygroveCity", "MAP_CHERRYGROVE_CITY_POKEMON_CENTER", "FLAG_VISITED_CHERRYGROVE_CITY"),
        ("VIOLET CITY", "MAP_VIOLET_CITY", "VioletCity", "MAP_VIOLET_CITY_POKEMON_CENTER", "FLAG_VISITED_VIOLET_CITY"),
        ("AZALEA TOWN", "MAP_AZALEA_TOWN", "AzaleaTown", "MAP_AZALEA_TOWN_POKEMON_CENTER", "FLAG_VISITED_AZALEA_TOWN"),
        ("GOLDENROD CITY", "MAP_GOLDENROD_CITY", "GoldenrodCity", "MAP_GOLDENROD_CITY_POKEMON_CENTER", "FLAG_VISITED_GOLDENROD_CITY"),
        ("ECRUTEAK CITY", "MAP_ECRUTEAK_CITY", "EcruteakCity", "MAP_ECRUTEAK_CITY_POKEMON_CENTER", "FLAG_VISITED_ECRUTEAK_CITY"),
        ("OLIVINE CITY", "MAP_OLIVINE_CITY", "OlivineCity", "MAP_OLIVINE_CITY_POKEMON_CENTER", "FLAG_VISITED_OLIVINE_CITY"),
        ("CIANWOOD CITY", "MAP_CIANWOOD_CITY", "CianwoodCity", "MAP_CIANWOOD_POKECENTER", "FLAG_VISITED_CIANWOOD_CITY"),
        ("MAHOGANY TOWN", "MAP_MAHOGANYTOWN", "Mahoganytown", "MAP_MAHOGANY_TOWN_POKEMON_CENTER", "FLAG_VISITED_MAHOGANY_TOWN"),
        ("BLACKTHORN CITY", "MAP_BLACKTHORN_CITY", "BlackthornCity", "MAP_BLACKTHORN_CITY_POKEMON_CENTER", "FLAG_VISITED_BLACKTHORN_CITY"),
        # Indigo Plateau é de Kanto: a célula do mapa do HnS voa para o MESMO
        # pouso e com a MESMA flag do mapa de Kanto (heal location do FRLG).
        ("INDIGO PLATEAU", "MAP_INDIGO_PLATEAU_EXTERIOR", None, (11, 7), "FLAG_WORLD_MAP_INDIGO_PLATEAU_EXTERIOR"),
    ],
    "Sinnoh": [
        ("TWINLEAF TOWN", "MAP_TWINLEAF_TOWN", "TwinleafTown", "MAP_TWINLEAF_TOWN_MAIN_HOUSE_1F", "FLAG_VISITED_TWINLEAF_TOWN"),
        ("SANDGEM TOWN", "MAP_SANDGEM_TOWN", "SandgemTown", "MAP_SANDGEM_TOWN_POKEMON_CENTER_1F", "FLAG_VISITED_SANDGEM_TOWN"),
        ("JUBILIFE CITY", "MAP_JUBILIFE_CITY", "JubilifeCity", "MAP_JUBILIFE_CITY_POKEMON_CENTER_1F", "FLAG_VISITED_JUBILIFE_CITY"),
        ("OREBURGH CITY", "MAP_OREBURGH_CITY", "OreburghCity", "MAP_OREBURGH_CITY_POKEMON_CENTER_1F", "FLAG_VISITED_OREBURGH_CITY"),
        ("FLOAROMA TOWN", "MAP_FLOAROMA_TOWN", "FloaromaTown", "MAP_FLOAROMA_TOWN_POKEMON_CENTER_1F", "FLAG_VISITED_FLOAROMA_TOWN"),
        ("ETERNA CITY", "MAP_ETERNA_CITY", "EternaCity", "MAP_ETERNA_CITY_POKECENTER_1F", "FLAG_VISITED_ETERNA_CITY"),
        ("HEARTHOME CITY", "MAP_HEARTHOME_CITY", "HearthomeCity", "MAP_HEARTHOME_CITY_POKECENTER_1F", "FLAG_VISITED_HEARTHOME_CITY"),
        ("SOLACEON TOWN", "MAP_SOLACEON_TOWN", "SolaceonTown", "MAP_SOLACEON_TOWN_POKECENTER_1F", "FLAG_VISITED_SOLACEON_TOWN"),
        ("CELESTIC TOWN", "MAP_CELESTIC_TOWN", "CelesticTown", "MAP_CELESTIC_TOWN_POKECENTER_1F", "FLAG_VISITED_CELESTIC_TOWN"),
        ("VEILSTONE CITY", "MAP_VEILSTONE_CITY", "VeilstoneCity", "MAP_VEILSTONE_CITY_POKECENTER_1F", "FLAG_VISITED_VEILSTONE_CITY"),
        ("PASTORIA CITY", "MAP_PASTORIA_CITY", "PastoriaCity", "MAP_PASTORIA_CITY_POKECENTER_1F", "FLAG_VISITED_PASTORIA_CITY"),
        ("CANALAVE CITY", "MAP_CANALAVE_CITY", "CanalaveCity", "MAP_CANALAVE_CITY_POKECENTER_1F", "FLAG_VISITED_CANALAVE_CITY"),
        ("SNOWPOINT CITY", "MAP_SNOWPOINT_CITY", "SnowpointCity", "MAP_SNOWPOINT_CITY_POKECENTER_1F", "FLAG_VISITED_SNOWPOINT_CITY"),
        ("SUNYSHORE CITY", "MAP_SUNYSHORE_CITY", "SunyshoreCity", "MAP_SUNYSHORE_CITY_POKECENTER_1F", "FLAG_VISITED_SUNYSHORE_CITY"),
        ("POKEMON LEAGUE", "MAP_POKMON_LEAGUE", "PokmonLeague", "MAP_SINNOH_LEAGUE_ENTRANCE", "FLAG_VISITED_SINNOH_POKEMON_LEAGUE"),
    ],
}


def le_grade(caminho):
    texto = open(caminho, encoding="utf-8").read()
    linhas = re.findall(r"\{(MAPSEC[^}]*)\}", texto)
    grade = [[c.strip() for c in l.split(",") if c.strip()] for l in linhas]
    if len(grade) != ALTURA or any(len(l) != LARGURA for l in grade):
        sys.exit(f"{caminho}: grade não é {LARGURA}x{ALTURA}")
    return grade


def nomes_popup(grupos):
    d = json.load(open(os.path.join(RAIZ, "data", "maps", "map_groups.json")))
    ordem = d["group_order"]
    nomes = set()
    for gi in range(grupos[0], grupos[1] + 1):
        for m in d[ordem[gi]]:
            j = json.load(open(os.path.join(RAIZ, "data", "maps", m, "map.json")))
            if j.get("map_name_popup"):
                nomes.add(j["map_name_popup"])
    return nomes


def pouso(pasta, destino_porta):
    j = json.load(open(os.path.join(RAIZ, "data", "maps", pasta, "map.json")))
    portas = [w for w in j.get("warp_events", []) if w["dest_map"] == destino_porta]
    if len(portas) != 1:
        sys.exit(f"{pasta}: esperava UMA porta para {destino_porta}, achei {len(portas)}")
    return portas[0]["x"], portas[0]["y"] + 1


def c_str(s):
    return 'COMPOUND_STRING("' + s + '")'


def gera():
    out = ["// GERADO por dev_scripts/mapa_voo_regioes.py. Não editar à mão.",
           "// Grade e nomes copiados do pokemonHnS (Johto) e do",
           "// Sinnoh-pokeemerald-expansion (Sinnoh); ver o cabeçalho do script.",
           ""]
    avisos = []
    for regiao, cfg in REGIOES.items():
        grade = le_grade(os.path.join(FONTES, cfg["layout"]))
        secoes = {s["map_section"]: s for s in
                  json.load(open(os.path.join(FONTES, cfg["secoes"])))["map_sections"]}
        popup = nomes_popup(cfg["grupos"])
        voo = {v[0]: v for v in VOO[regiao]}
        ordem, celulas = [], {}
        for y in range(ALTURA):
            for x in range(LARGURA):
                c = grade[y][x]
                if c != "MAPSEC_NONE":
                    if c not in ordem:
                        ordem.append(c)
                    celulas.setdefault(c, []).append((x, y))
        lugares = []
        for c in ordem:
            s = secoes[c]
            nome = DEPARA_NOME.get(s["name"], s["name"])
            if len(nome) > NOME_MAX:
                sys.exit(f"{regiao}: nome '{nome}' passa de {NOME_MAX}")
            casa = APELIDO_POPUP.get(nome, nome)
            if casa not in popup:
                avisos.append(f"{regiao}: '{casa}' não é letreiro de nenhum mapa (só nome no mapa)")
            v = voo.pop(nome, None)
            if v:
                _, mapa, pasta, porta, flag = v
                px, py = porta if pasta is None else pouso(pasta, porta)
            else:
                mapa, px, py, flag = "MAP_UNDEFINED", 0, 0, "0"
            # Retângulo do ícone tirado da GRADE, não do x/y do .json da fonte:
            # o .json do HnS tem entradas velhas (DRAGON'S DEN, ROUTE 36, ROUTE 37
            # e TRAINER HILL apontam para células que a grade dele não usa).
            xs = [cx for cx, _ in celulas[c]]
            ys = [cy for _, cy in celulas[c]]
            lugares.append(dict(nome=nome, casa=casa, x=min(xs), y=min(ys),
                                w=max(xs) - min(xs) + 1, h=max(ys) - min(ys) + 1,
                                mapa=mapa, px=px, py=py, flag=flag))
        if voo:
            sys.exit(f"{regiao}: destino de voo sem célula no mapa: {sorted(voo)}")
        if len(lugares) > 254:
            sys.exit(f"{regiao}: lugares demais para u8")
        out.append(f"static const struct LugarMapaRegiao sLugares{regiao}[] =")
        out.append("{")
        for i, l in enumerate(lugares):
            casa = "NULL" if l["casa"] == l["nome"] else c_str(l["casa"])
            out.append(f"    [{i}] = {{ .nome = {c_str(l['nome'])}, .nomePopup = {casa}, "
                       f".x = {l['x']}, .y = {l['y']}, .largura = {l['w']}, .altura = {l['h']}, "
                       f".flag = {l['flag']}, .mapa = {l['mapa']}, .pousoX = {l['px']}, .pousoY = {l['py']} }},")
        out.append("};")
        out.append("")
        idx = {c: i + 1 for i, c in enumerate(ordem)}
        out.append(f"// 0 = nada; n = sLugares{regiao}[n - 1].")
        out.append(f"static const u8 sGrade{regiao}[MAP_HEIGHT][MAP_WIDTH] =")
        out.append("{")
        for y in range(ALTURA):
            out.append("    {" + ", ".join(f"{idx.get(c, 0):2d}" for c in grade[y]) + "},")
        out.append("};")
        out.append("")
    return "\n".join(out), avisos


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--confere", action="store_true")
    a = p.parse_args()
    texto, avisos = gera()
    for av in avisos:
        print("aviso:", av)
    velho = open(SAIDA, encoding="utf-8").read() if os.path.exists(SAIDA) else None
    if a.confere:
        print("igual" if velho == texto else "DIFERENTE")
        sys.exit(0 if velho == texto else 1)
    if velho != texto:
        open(SAIDA, "w", encoding="utf-8").write(texto)
        print("gravado", os.path.relpath(SAIDA, RAIZ))
    else:
        print("sem mudança")


if __name__ == "__main__":
    main()
