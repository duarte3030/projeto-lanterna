#!/usr/bin/env python3
"""Gera a tabela de destinos de voo de Unova e Galar (cartucho 2).

Uso:
    python3 dev_scripts/voo_c2.py           # escreve src/data/region_map/voo_c2.h
    python3 dev_scripts/voo_c2.py --demo    # confere sem escrever; sai 1 se algo cair

Por que existe
--------------
MAPSEC é `u8`, então Unova e Galar não têm uma seção por cidade: cada cidade é
apelido de um MAPSEC de grupo (UNOVA_WEST, GALAR_NORTH...). O mapa de voo do
motor escolhe destino por MAPSEC e desenha a arte de Hoenn, então em Unova e
Galar o Fly abria o mapa de Hoenn com "UNOVA EAST" na caixa e não voava para
lugar nenhum. A troca é o voo do próprio BW3 Genesis (estilo Crystal): o jogador
percorre com as setas a lista das cidades já visitadas da região onde está, na
ordem de `data/maps/flypoints.asm` do BW3G, e voa com A.

De onde sai cada número (lido dos dados, nunca de memória)
----------------------------------------------------------
- Cidade = cada ponto de cura (`src/data/heal_locations.json`) de Unova e Galar,
  cujo mapa é o Pokécenter da cidade.
- Pouso = o ladrilho logo ABAIXO da porta do Pokécenter na rua, como o Emerald
  faz. A rua é o destino da saída do Pokécenter cuja porta de volta leva ao
  MESMO Pokécenter (os Pokécenters de Galar têm saídas para mapas de outra
  história; só a que volta conta). O ladrilho tem que ser passável (colisão 0
  no blockdata do layout); se não for, a cidade cai fora e o script acusa.
- Rua coberta (MAP_TYPE_INDOOR) não recebe pouso. Pokécenter dentro de outro
  prédio (Crown Tundra) pousa na rua desse prédio.
- Ponto de cura: cada destino leva o seu `HEAL_LOCATION_*` e o mapa do
  Pokécenter. Entrar no Pokécenter faz `SetLastHealLocationWarp` dele
  (src/region_map.c), o que Unova já fazia por script e Galar não fazia: quem
  desmaiava em Galar voltava para a última cama de Unova.
- Visitada = entrar em qualquer mapa cujo `map_name_popup` é o nome da cidade,
  ou no próprio Pokécenter. Victory Road e Pokémon League só pelo Pokécenter e
  pela rua do pouso: o letreiro delas cobre a caverna e as salas da Liga.
- Flag de cada cidade: `FLAG_VOO_<REGIAO>_<CIDADE>`, apelidos de FLAG_UNUSED em
  `include/constants/flags.h`. Save intacta: o pool de flags não muda de tamanho.
"""
import glob
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = f"{RAIZ}/src/data/region_map/voo_c2.h"

# Ordem do BW3G (fontes-mapas/bw3g/data/maps/flypoints.asm), sem Nuvema, que lá
# pousa na casa do jogador e aqui não tem Pokécenter.
ORDEM_UNOVA = ["HUMILAU", "LACUNOSA", "UNDELLA", "LENTIMAS", "NIMBASA", "CASTELIA",
               "ASPERTIA", "FLOCCESY", "VIRBANK", "NACRENE", "STRIATON", "ACCUMULA",
               "DRIFTVEIL", "MISTRALTON", "OPELUCID", "ICIRRUS", "VICTORY_ROAD",
               "PKMN_LEAGUE"]
# Ordem da campanha do Shield, que o Ultimate Plus segue; DLC no fim.
ORDEM_GALAR = ["WEDGEHURST", "MOTOSTOKE", "TURFFIELD", "HULBURY", "HAMMERLOCKE",
               "STOW_ON_SIDE", "BALLONLEA", "CIRCHESTER", "SPIKEMUTH", "WYNDON",
               "ISLE_OF_ARMOR", "CROWN_TUNDRA"]
SO_PELO_POKECENTER = {"UNOVA_VICTORY_ROAD", "UNOVA_PKMN_LEAGUE"}
FORA_POR_TIPO = {"MAP_TYPE_INDOOR"}


def le_mapas():
    mapas = {}
    for f in glob.glob(f"{RAIZ}/data/maps/*/map.json"):
        j = json.load(open(f))
        mapas[j["id"]] = j
    return mapas


def le_layouts():
    lay = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]
    return {l["id"]: l for l in lay if "id" in l}


def colisao(layouts, mapa, x, y):
    l = layouts[mapa["layout"]]
    w, h = l["width"], l["height"]
    if not (0 <= x < w and 0 <= y < h):
        return None
    with open(f"{RAIZ}/{l['blockdata_filepath']}", "rb") as f:
        dados = f.read()
    bloco = struct.unpack_from("<H", dados, 2 * (y * w + x))[0]
    return (bloco >> 10) & 3


def saidas(mapas, origem, aceita_coberta=False):
    """Saídas de `origem` cuja porta de volta leva a `origem` (a rua e o x,y da porta)."""
    for w in origem.get("warp_events") or []:
        rua = mapas.get(w["dest_map"])
        if rua is None or rua["id"] == origem["id"]:
            continue
        try:
            volta = rua["warp_events"][int(w["dest_warp_id"])]
        except (IndexError, ValueError, KeyError):
            continue
        if volta["dest_map"] != origem["id"]:
            continue
        if rua["map_type"] in FORA_POR_TIPO and not aceita_coberta:
            continue
        yield rua, volta["x"], volta["y"]


def saida_para_rua(mapas, origem):
    """Pouso logo abaixo da porta de `origem` na primeira rua descoberta."""
    for rua, x, y in saidas(mapas, origem):
        return (rua, x, y + 1)
    return None


def flags_definidas():
    texto = open(f"{RAIZ}/include/constants/flags.h").read()
    return set(re.findall(r"#define\s+(FLAG_VOO_\w+)\s", texto))


def monta():
    mapas = le_mapas()
    layouts = le_layouts()
    curas = json.load(open(f"{RAIZ}/src/data/heal_locations.json"))["heal_locations"]
    curas = {c["id"]: c for c in curas}
    flags = flags_definidas()
    destinos, problemas = [], []
    for regiao, ordem in (("UNOVA", ORDEM_UNOVA), ("GALAR", ORDEM_GALAR)):
        for cidade in ordem:
            chave = f"{regiao}_{cidade}"
            cura = curas.get(f"HEAL_LOCATION_{chave}")
            if cura is None:
                problemas.append(f"{chave}: sem ponto de cura")
                continue
            pc_id = cura["map"]
            pc = mapas[pc_id]
            pouso = saida_para_rua(mapas, pc)
            if pouso is None:
                # Pokécenter dentro de outro prédio (Crown Tundra: o centro fica
                # dentro da estação 05): sai do prédio e pousa na rua dele.
                for predio, _, _ in saidas(mapas, pc, aceita_coberta=True):
                    if predio["map_type"] in FORA_POR_TIPO:
                        pouso = saida_para_rua(mapas, predio)
                        if pouso is not None:
                            break
            if pouso is None:
                problemas.append(f"{chave}: o Pokécenter {pc_id} não sai para rua descoberta (fica fora da lista)")
                continue
            rua, px, py = pouso
            col = colisao(layouts, rua, px, py)
            if col != 0:
                problemas.append(f"{chave}: pouso ({px},{py}) em {rua['id']} tem colisão {col} (fica fora da lista)")
                continue
            flag = f"FLAG_VOO_{chave}"
            if flag not in flags:
                problemas.append(f"{chave}: {flag} não está em include/constants/flags.h")
                continue
            nome = rua.get("map_name_popup") or pc.get("map_name_popup")
            if not nome:
                problemas.append(f"{chave}: sem map_name_popup na rua nem no Pokécenter")
                continue
            if chave in SO_PELO_POKECENTER:
                marcam = sorted({rua["id"], pc_id})
            else:
                marcam = sorted({m for m, j in mapas.items() if j.get("map_name_popup") == nome} | {rua["id"], pc_id})
            if cura.get("respawn_map", pc_id) != pc_id:
                problemas.append(f"{chave}: o ponto de cura renasce em {cura['respawn_map']}, não em {pc_id}")
                continue
            destinos.append(dict(chave=chave, regiao=regiao, nome=nome, flag=flag,
                                 cura=cura["id"], centro=pc_id,
                                 mapa=rua["id"], x=px, y=py, pc=pc_id, marcam=marcam,
                                 tipo=rua["map_type"]))
    return destinos, problemas


def texto_do_h(destinos):
    linhas = [
        "// GERADO por dev_scripts/voo_c2.py. Não editar à mão.",
        "// Destinos de voo de Unova e Galar, na ordem do BW3G e do Shield.",
        "",
        "static const struct DestinoVooC2 sDestinosVooC2[] =",
        "{",
    ]
    for i, d in enumerate(destinos):
        linhas.append(f"    [{i}] = {{ .nome = COMPOUND_STRING(\"{d['nome']}\"), .regiao = REGION_{d['regiao']}, "
                      f".flag = {d['flag']}, .mapa = {d['mapa']}, .x = {d['x']}, .y = {d['y']}, "
                      f".centro = {d['centro']}, .cura = {d['cura']} }},")
    linhas += ["};", "", "// Mapa que, ao entrar, acende a flag de voo do destino (índice em sDestinosVooC2).",
               "static const struct MapaVooC2 sMapasVooC2[] =", "{"]
    for i, d in enumerate(destinos):
        for m in d["marcam"]:
            linhas.append(f"    {{ .mapa = {m}, .destino = {i} }},")
    linhas += ["};", ""]
    return "\n".join(linhas)


def main():
    destinos, problemas = monta()
    for p in problemas:
        print("AVISO:", p)
    for d in destinos:
        print(f"{d['chave']:<20} {d['nome']:<16} {d['mapa']} ({d['x']},{d['y']}) {d['tipo']} marcam={len(d['marcam'])}")
    print(f"{len(destinos)} destinos, {sum(len(d['marcam']) for d in destinos)} mapas que marcam")
    if "--demo" in sys.argv:
        # Toda cidade de Unova com Pokécenter tem que entrar.
        unova = [d for d in destinos if d["regiao"] == "UNOVA"]
        ok = len(unova) == len(ORDEM_UNOVA) and len(destinos) == len(ORDEM_UNOVA) + len(ORDEM_GALAR)
        if not ok:
            print("demo: faltou cidade de Unova ou de Galar")
        # O .h commitado tem que ser o que o script gera hoje.
        atual = open(SAIDA).read() if os.path.exists(SAIDA) else ""
        if atual != texto_do_h(destinos):
            print(f"demo: {SAIDA} velho; rode python3 dev_scripts/voo_c2.py")
            ok = False
        print("demo:", "ok" if ok else "FALHOU")
        sys.exit(0 if ok else 1)
    with open(SAIDA, "w") as f:
        f.write(texto_do_h(destinos))


if __name__ == "__main__":
    main()
