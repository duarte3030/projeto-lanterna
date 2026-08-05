#!/usr/bin/env python3
"""Anda o jogo inteiro pelo grafo de warps e conexoes, e acha o que trava.

Uso:
    python3 dev_scripts/valida_conectividade.py [MAP_DE_PARTIDA]

Existe porque "alcancavel" checado dentro de UM mapa e geometria de colisao, nao
jogo. O que prende o jogador de verdade e warp que aponta para indice que nao
existe, warp so de ida, e mapa que nenhum caminho alcanca. Tres bugs desse tipo
ja passaram por aqui despercebidos: dois ginasios inacessiveis por warp fora da
porta, e 6 de 7 ginasios cuspindo o jogador numa rota ao sair.

Reporta:
  1. warp cujo `dest_warp_id` nao existe no mapa de destino  (trava garantida)
  2. mapa alcancavel de onde NAO se volta                    (beco sem saida)
  3. mapa de Sinnoh/Johto que nenhum caminho alcanca         (conteudo morto)
"""
import json
import os
import re
import sys
from collections import deque

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(REPO, "data/maps")


def tabela_de_constantes():
    """dir do mapa -> constante MAP_*, lida da FONTE, nao adivinhada.

    Derivar a constante por regex erra: "OreburghCity_PokemonCenter_1F" vira
    "..._1_F" se a regra separar digito de maiuscula, e aparecem 1882 warps
    "quebrados" que nao existem. A verdade e o par (grupo, indice) de
    map_groups.json casado com o valor em constants/map_groups.h.
    """
    grupos = json.load(open(os.path.join(MAPS, "map_groups.json")))
    header = open(os.path.join(REPO, "include/constants/map_groups.h")).read()
    por_valor = {}
    for const, num, grp in re.findall(
            r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)", header):
        por_valor[(int(grp), int(num))] = const
    tabela = {}
    for g_idx, nome_grupo in enumerate(grupos["group_order"]):
        for m_idx, nome_mapa in enumerate(grupos.get(nome_grupo, [])):
            const = por_valor.get((g_idx, m_idx))
            if const:
                tabela[nome_mapa] = const
    return tabela


def carrega():
    const = tabela_de_constantes()
    mapas = {}
    for nome in sorted(os.listdir(MAPS)):
        if nome not in const:
            continue
        caminho = os.path.join(MAPS, nome, "map.json")
        if not os.path.exists(caminho):
            continue
        try:
            d = json.load(open(caminho))
        except json.JSONDecodeError as e:
            print(f"  JSON QUEBRADO: {nome}/map.json: {e}")
            continue
        mapas[const[nome]] = dict(dir=nome, dados=d)
    return mapas


def main():
    mapas = carrega()
    partida = sys.argv[1] if len(sys.argv) > 1 else "MAP_TWINLEAF_TOWN"
    if partida not in mapas:
        # cai para o que o modo de desenvolvimento usa hoje
        dbg = open(os.path.join(REPO, "include/config/debug.h")).read()
        m = re.search(r"#define DEV_START_MAP\s+(MAP_\w+)", dbg)
        partida = m.group(1) if m and m.group(1) in mapas else sorted(mapas)[0]
    print(f"partindo de {partida}\n")

    quebrados = []
    saidas = {}
    for origem, info in mapas.items():
        vizinhos = set()
        for i, w in enumerate(info["dados"].get("warp_events", [])):
            destino = w.get("dest_map", "")
            if destino in ("MAP_NONE", "MAP_DYNAMIC", ""):
                continue
            if destino not in mapas:
                quebrados.append((origem, i, destino, "mapa de destino nao existe"))
                continue
            n_la = len(mapas[destino]["dados"].get("warp_events", []))
            try:
                alvo = int(w.get("dest_warp_id", 0))
            except (TypeError, ValueError):
                alvo = -1
            if alvo < 0 or alvo >= n_la:
                quebrados.append((origem, i, destino,
                                  f"dest_warp_id {w.get('dest_warp_id')} mas o destino tem {n_la} warps"))
                continue
            vizinhos.add(destino)
        # conexoes de rota (andar de um mapa para o outro sem warp) sao bidirecionais
        for c in info["dados"].get("connections") or []:
            if c.get("map") in mapas:
                vizinhos.add(c["map"])
        # Warp escrito DENTRO de script tambem liga mapa, e e assim que a viagem
        # entre regioes funciona (o marinheiro de Canalave leva a Olivine). Sem
        # ler isto, a ferramenta declarava Johto inteira inalcancavel, que era
        # falso: o erro era da ferramenta, nao do jogo.
        inc = os.path.join(MAPS, info["dir"], "scripts.inc")
        if os.path.exists(inc):
            texto = open(inc, encoding="utf-8", errors="replace").read()
            for destino in re.findall(r"\bwarp(?:silent|hole|door|teleport)?\s+(MAP_[A-Z0-9_]+)",
                                      texto):
                if destino in mapas:
                    vizinhos.add(destino)
        saidas[origem] = vizinhos

    print(f"=== 1. warps quebrados: {len(quebrados)} ===")
    for origem, i, destino, motivo in quebrados[:25]:
        print(f"  {origem} warp {i} -> {destino}: {motivo}")
    if len(quebrados) > 25:
        print(f"  ... e mais {len(quebrados) - 25}")

    vistos = {partida}
    fila = deque([partida])
    while fila:
        atual = fila.popleft()
        for v in saidas.get(atual, ()):
            if v not in vistos:
                vistos.add(v)
                fila.append(v)
    print(f"\n=== 2. alcance: {len(vistos)} de {len(mapas)} mapas ===")

    becos = [m for m in vistos if not saidas.get(m)]
    print(f"\n=== 3. becos sem saida (entra e nao sai): {len(becos)} ===")
    for m in sorted(becos)[:20]:
        print("  ", m)

    def regiao(m):
        d = mapas[m]["dados"]
        ms = str(d.get("region_map_section", ""))
        if "SINNOH" in ms:
            return "Sinnoh"
        nome = mapas[m]["dir"]
        johto = ("Azalea", "Blackthorn", "Cherrygrove", "Cianwood", "Ecruteak",
                 "Goldenrod", "Mahogany", "Olivine", "Violet", "NewBark", "Ilex",
                 "UnionCave", "MtMortar", "IcePath", "Whirl", "Sprout", "Burned",
                 "Tin", "RuinsOfAlph", "Dragons", "MtSilver", "National", "Bellchime",
                 "LakeOfRage")
        return "Johto" if any(nome.startswith(p) for p in johto) else "outro"

    orfaos = {}
    for m in mapas:
        if m not in vistos:
            r = regiao(m)
            if r != "outro":
                orfaos.setdefault(r, []).append(m)
    print("\n=== 4. mapas de Sinnoh/Johto que NENHUM caminho alcanca ===")
    for r, lst in sorted(orfaos.items()):
        print(f"  {r}: {len(lst)}")
        for m in sorted(lst)[:12]:
            print("     ", m)
        if len(lst) > 12:
            print(f"      ... e mais {len(lst) - 12}")
    if not orfaos:
        print("  nenhum")

    return 1 if quebrados else 0


if __name__ == "__main__":
    sys.exit(main())
