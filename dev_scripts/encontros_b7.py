#!/usr/bin/env python3
"""Bloco B7: encontro selvagem em todo mapa que tem encontro NA FONTE.

    python3 dev_scripts/encontros_b7.py --analise   # só mede, não escreve
    python3 dev_scripts/encontros_b7.py --aplica    # reescreve wild_encounters.json
    python3 dev_scripts/encontros_b7.py --demo      # asserts, não toca em nada

Escreve um arquivo só: `src/data/wild_encounters.json`, que é o ÚNICO que vira
`src/data/wild_encounters.h` (regra do `Makefile`, linha 258). `src/data/
wild_encounters_sinnoh.json` NÃO é compilado por ninguém e está aqui só como
acervo; este script o substitui por inteiro e diz por quê.

## As três coisas que este arquivo conserta, e a medida de cada uma

1. **Kanto tinha 124 mapas de encontro e ZERO deles entrava na ROM.** Todo
   rótulo de Kanto terminava em `_FireRed` ou `_LeafGreen`, e
   `tools/wild_encounters/wild_encounters_to_header.py` transforma esse sufixo
   em `#ifdef FIRERED` / `#ifdef LEAFGREEN`. A build é `-DEMERALD`
   (`Makefile:164`), então os 264 blocos eram apagados pelo pré-processador.
   Medido abrindo o `src/data/wild_encounters.h` gerado: `MAP_VIRIDIAN_FOREST`
   só aparece dentro de `#ifdef FIRERED` e de `#ifdef LEAFGREEN`. O inventário
   dava "124 / 124" porque ele conta a entrada no JSON, não o que sobra depois
   do `#ifdef`: é o mesmo defeito de régua que deu 98% para Unova.
   Conserto: tirar o sufixo `_FireRed` dos 132 rótulos, o que os joga no ramo
   `EMERALD`. A fonte de Kanto é o `pokefirered` (`ESTADO.md`, seção 1), então a
   versão que fica é a FireRed. As 132 entradas `_LeafGreen` não são apagadas,
   continuam no arquivo e continuam fora da build, para que a escolha seja
   reversível trocando um sufixo pelo outro.
   Conferido antes de aplicar: nenhum dos 124 `MAP_*` de FireRed falta no
   `include/constants/map_groups.h`, e nenhum rótulo colide ao perder o sufixo.

2. **As 36 tabelas de pesca de Sinnoh estavam desalinhadas.** O acervo trouxe os
   15 slots do Platinum (5 por vara) para dentro de um campo que declara 10
   (`fishing_mons`, grupos `old_rod` 0-1, `good_rod` 2-4, `super_rod` 5-9). O
   motor indexa por macro de slot, então nada estoura, mas a vara errada pescava
   a espécie errada: os slots 5-9, que aqui são a super, liam a vara BOA do
   Platinum. As taxas por slot foram medidas em
   `pokeplatinum/src/overlay006/wild_encounters.c` (`GetRodEncounterSlot`) e
   valem uma comparação direta, não um chute:

       grama     Platinum 20,20,10,10,10,10,5,5,4,4,1,1  = aqui, slot a slot
       surf      Platinum 60,30,5,4,1                    = aqui, slot a slot
       vara velha Platinum 60,30,5,4,1   -> aqui 70,30       (2 slots, cortam 3)
       vara boa   Platinum 40,40,15,4,1  -> aqui 60,20,20    (3 slots, cortam 2)
       super      Platinum 40,40,15,4,1  -> aqui 40,40,15,4,1 (igual, 5 slots)

   Grama e surf casam SLOT A SLOT com o Platinum, o que torna Sinnoh a conversão
   mais barata das cinco regiões. Só a pesca perde cauda, e ela é nomeada abaixo.
   O `encounter_rate` da pesca fica com o MAIOR dos três do Platinum porque o
   campo é um só e as varas são três. Conferido antes de escolher: o motor daqui
   nunca lê esse número (`fishingMonsInfo` só é usado em
   `src/wild_encounter.c:928` e `:954`, para a LISTA; em Emerald a vara sempre
   fisga), então a escolha é cosmética e nenhuma delas muda o jogo.

3. **Os 74 mapas de Sinnoh sem tabela.** O casamento mapa nosso -> header do
   Platinum não é inventado aqui: é o mesmo de `inventario.py`
   (`importa_npcs_sinnoh.APELIDOS` e `.chave`), que é a régua que mede a lacuna.
   Usar outra régua para preencher do que para medir é como se fabrica verde
   falso, então aqui é a mesma.

## O que do gen 4 é DESCARTADO, por categoria

O motor daqui não tem esses conceitos por mapa, e nenhum deles tem campo no
schema do `wild_encounters.json`:

- **horário** (`day`, `night`): pares de espécie que substituem os slots 2 e 3
  da grama conforme a hora. `OW_TIME_OF_DAY_ENCOUNTERS` é FALSE em
  `include/config/overworld.h`, então fica só a tabela base (que no Platinum é a
  de dia).
- **Poké Radar** (`radar`): 4 espécies que só saem com o radar ligado.
- **swarm** (`swarms`): 2 espécies do enxame diário sorteado pela TV.
- **exclusivas de versão** (`ruby`, `sapphire`, `emerald`, `firered`,
  `leafgreen`): 2 espécies cada, liberadas por ter o cartucho de GBA na fenda.
- **formas** (`rate_form0..4`, `unown_table`): distribuição de forma de Unown e
  de Burmy.
- **cauda da pesca**: 3 slots da vara velha (5+4+1 = 10% dos fisgados) e 2 da
  vara boa (4+1 = 5%), pelo aperto de 15 slots em 10 descrito acima.
- **rock smash**: o Platinum não tem o campo; nenhum mapa de Sinnoh gera
  `rock_smash_mons`, e isso não é perda, é ausência na fonte.

## Johto e Unova

Johto vem do `hns`, que é decomp de gen 3 com o MESMO schema: os 9 mapas que
faltavam são cópia direta, com duas correções. A primeira é o rótulo `_Night`,
que o hns usa e que aqui viraria `TIME_NIGHT`: com `OW_TIME_OF_DAY_ENCOUNTERS`
FALSE a entrada seria escrita e ignorada, então só a tabela base entra. A
segunda é `gRoute28`, que no hns tem 12 mons em `water_mons` num campo de 5
slots: os 7 do fim são inalcançáveis pelo motor e ficam de fora.

Unova NÃO é tocado por este script, e o motivo está no relatório: os 22 mapas
que o inventário acusa de ter tabela sem encontro na fonte são os 22 mapas de
ROTA, e a fonte tem encontro em todos os 22. O que erra é a régua:
`inventario.encontros_gen2` casa o nome do ARQUIVO do mapa (`maps/Rt1.asm`) com
a constante citada em `data/wild/*.asm` (`map_id R_1`), e `chave_simples`
devolve "rt1" contra "r1". A única rota que casa é a 22, porque o arquivo dela é
`R22.asm`, sem o "t". 65 + 22 = 87, que é exatamente o que temos.
"""
import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(os.path.dirname(RAIZ), "fontes-mapas")
PLAT = os.path.join(FONTES, "pokeplatinum")
HNS = os.path.join(FONTES, "hns")
ALVO = os.path.join(RAIZ, "src/data/wild_encounters.json")
ACERVO = os.path.join(RAIZ, "src/data/wild_encounters_sinnoh.json")

sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

# Quantos slots cada campo tem AQUI. Não é escolha deste arquivo: sai do próprio
# `fields` do JSON, conferido em `checa_schema()`, porque o motor indexa por
# macro `ENCOUNTER_CHANCE_*_SLOT_n` e um mon a mais nunca é sorteado.
SLOTS = {"land_mons": 12, "water_mons": 5, "rock_smash_mons": 5, "fishing_mons": 10}
# old_rod fica com os 2 primeiros dos 5 do Platinum, good_rod com 3 dos 5, super
# com os 5. Ver a tabela de taxas no docstring.
CORTE_VARA = {"old_rod_encounters": 2, "good_rod_encounters": 3, "super_rod_encounters": 5}
# Palavra que o gerador de header lê como horário e que come a tabela inteira
# quando `OW_TIME_OF_DAY_ENCOUNTERS` é FALSE (ver `WriteEncounters`).
HORARIOS = ("Morning", "Day", "Evening", "Night")


def especies_validas():
    txt = open(os.path.join(RAIZ, "include/constants/species.h")).read()
    return set(re.findall(r"\bSPECIES_[A-Z0-9_]+", txt))


def mapas_do_repo():
    txt = open(os.path.join(RAIZ, "include/constants/map_groups.h")).read()
    return set(re.findall(r"^\s+(MAP_[A-Z0-9_]+)\s*=", txt, re.M))


def carrega():
    with open(ALVO, encoding="utf-8") as f:
        return json.load(f)


def grupo_principal(d):
    for g in d["wild_encounter_groups"]:
        if g.get("for_maps") and "fields" in g:
            return g
    raise SystemExit("wild_encounters.json sem grupo for_maps com fields")


def checa_schema(g):
    """O `fields` do arquivo tem que ser o que este script assume. Senão, pare.

    Existe porque o número de slots é a única coisa que, se mudar em silêncio,
    faz o motor sortear fora do array. Reprovar aqui é melhor que gerar.
    """
    vistos = {f["type"]: len(f["encounter_rates"]) for f in g["fields"]}
    assert vistos == SLOTS, f"fields mudou: {vistos} != {SLOTS}"
    pesca = next(f for f in g["fields"] if f["type"] == "fishing_mons")
    assert pesca["groups"] == {"old_rod": [0, 1], "good_rod": [2, 3, 4],
                               "super_rod": [5, 6, 7, 8, 9]}, "grupos de vara mudaram"


def rotulo(mapa_pasta, usados):
    """`g` + o nome da pasta sem separador, e nunca com palavra de horário."""
    base = "g" + re.sub(r"[^A-Za-z0-9]", "", mapa_pasta)
    for h in HORARIOS:
        if h in base:
            # "PokemonDayCare" viraria TIME_DAY e a tabela sumiria calada.
            base = base.replace(h, h.upper())
    n, saida = 1, base
    while saida in usados:
        n += 1
        saida = f"{base}{n}"
    usados.add(saida)
    return saida


# ------------------------------------------------------------------ Sinnoh

def le_platinum(stem):
    p = os.path.join(PLAT, "res/field/encounters", stem + ".json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def converte_sinnoh(dados, descartes):
    """A tabela base do Platinum no schema daqui. Nada de horário/radar/swarm."""
    fora = {}

    if dados.get("land_rate") and dados.get("land_encounters"):
        mons = [{"min_level": e["level"], "max_level": e["level"],
                 "species": e["species"]} for e in dados["land_encounters"]]
        if any(m["species"] != "SPECIES_NONE" for m in mons):
            fora["land_mons"] = {"encounter_rate": dados["land_rate"],
                                 "mons": mons[:SLOTS["land_mons"]]}
    for k in ("day", "night"):
        if any(s != "SPECIES_NONE" for s in dados.get(k) or []):
            descartes[k] += 1
    for k in ("radar", "swarms"):
        if any(s != "SPECIES_NONE" for s in dados.get(k) or []):
            descartes[k] += 1
    for k in ("ruby", "sapphire", "emerald", "firered", "leafgreen"):
        if any(s != "SPECIES_NONE" for s in dados.get(k) or []):
            descartes["versao"] += 1
            break
    if dados.get("unown_table") or any(dados.get(f"rate_form{i}") for i in range(5)):
        descartes["forma"] += 1

    surf = dados.get("surf_encounters") or []
    if dados.get("surf_rate") and any(e["species"] != "SPECIES_NONE" for e in surf):
        fora["water_mons"] = {
            "encounter_rate": dados["surf_rate"],
            "mons": [{"min_level": e["level_min"], "max_level": e["level_max"],
                      "species": e["species"]} for e in surf][:SLOTS["water_mons"]],
        }

    mons, taxa = [], 0
    for chave, corte in CORTE_VARA.items():
        vara = dados.get(chave) or []
        if len(vara) > corte:
            descartes["cauda_pesca"] += len(vara) - corte
        mons += [{"min_level": e["level_min"], "max_level": e["level_max"],
                  "species": e["species"]} for e in vara[:corte]]
        taxa = max(taxa, dados.get(chave.replace("_encounters", "_rate")) or 0)
    if taxa and any(m["species"] != "SPECIES_NONE" for m in mons):
        # 10 slots exatos: o motor sorteia por macro e um a menos lê lixo.
        while len(mons) < SLOTS["fishing_mons"]:
            mons.append(dict(mons[-1]))
        fora["fishing_mons"] = {"encounter_rate": taxa,
                                "mons": mons[:SLOTS["fishing_mons"]]}
    return fora


def entradas_sinnoh(descartes):
    """[(MAP_*, pasta, tabela)] para todo mapa nosso de Sinnoh com encontro lá."""
    import inventario as V
    import importa_npcs_sinnoh as I

    heads = V.headers_plat()
    por_chave = {}
    for h in heads:
        por_chave.setdefault(I.chave(h), h)
    idx, comp = {}, {}
    fora = []
    for pasta in sorted(I.nossos_mapas_sinnoh()):
        h = I.APELIDOS.get(pasta) or por_chave.get(I.chave(pasta))
        if h not in heads:
            continue
        stem = heads[h]["encontros"]
        dados = le_platinum(stem) if stem else None
        if not dados:
            continue
        tabela = converte_sinnoh(dados, descartes)
        if not tabela:
            continue
        pj = os.path.join(RAIZ, "data/maps", pasta, "map.json")
        if not os.path.exists(pj):
            continue
        with open(pj, encoding="utf-8") as f:
            mid = json.load(f).get("id")
        if mid:
            fora.append((mid, pasta, tabela, stem))
    return fora


# ------------------------------------------------------------------- Johto

def entradas_johto(faltantes):
    """As tabelas do hns dos mapas pedidos, já podadas para o schema daqui."""
    with open(os.path.join(HNS, "src/data/wild_encounters.json"), encoding="utf-8") as f:
        g = json.load(f)["wild_encounter_groups"][0]
    fora, cortes = [], []
    for e in g["encounters"]:
        if e["map"] not in faltantes:
            continue
        if any(h in e["base_label"] for h in HORARIOS):
            cortes.append(("horario", e["base_label"]))
            continue
        nova = {"map": e["map"], "base_label": e["base_label"]}
        for tipo, n in SLOTS.items():
            if tipo not in e:
                continue
            mons = e[tipo]["mons"]
            if len(mons) > n:
                cortes.append((f"{tipo} {len(mons)}->{n}", e["base_label"]))
            nova[tipo] = {"encounter_rate": e[tipo]["encounter_rate"],
                          "mons": mons[:n]}
        fora.append(nova)
    return fora, cortes


# ------------------------------------------------------------------- Kanto

def versao(label):
    if "FireRed" in label:
        return "FIRERED"
    if "LeafGreen" in label:
        return "LEAFGREEN"
    return "EMERALD"


# Tabela de Sinnoh pendurada no mapa de HOENN. `MAP_VICTORY_ROAD_1F` e
# `MAP_VICTORY_ROAD_B1F` são a Victory Road de Hoenn; a de Sinnoh entrou na ROM
# com prefixo de região (`MAP_SINNOH_VICTORY_ROAD_*`, ver
# `importa_npcs_sinnoh.APELIDOS`) e ninguém corrigiu o encontro. Hoenn é o
# CONTROLE do projeto, o vanilla intocado, e já tem `gVictoryRoad_1F` e
# `gVictoryRoad_B1F` nesses dois mapas: as duas entradas de Sinnoh são
# duplicata de alvo errado, saem pela regra 2 da seção 2 do PRD, e os mesmos
# dados voltam no lugar certo pelo gerador de Sinnoh deste arquivo.
FORA_ALVO_ERRADO = {"gSinnohVictoryRoad_1F", "gSinnohVictoryRoad_B1F"}


def poda_slots(g):
    """Corta o mon que passa do número de slots do campo, e nunca completa.

    Mon além do slot declarado é inalcançável: o motor sorteia por macro
    `ENCOUNTER_CHANCE_*_SLOT_n`. São bytes de ROM que nenhum jogador encontra, e
    vieram de fonte com schema mais largo (o hns põe 12 em `water_mons`, o
    Platinum 15 na pesca). Faltar mon seria o contrário e é grave, então isso
    aqui reprova em vez de completar.
    """
    cortes = []
    for e in g["encounters"]:
        for k, v in e.items():
            if not k.endswith("_mons"):
                continue
            n = len(v["mons"])
            assert n >= SLOTS[k], f"{e['base_label']}.{k} tem {n} de {SLOTS[k]}"
            if n > SLOTS[k]:
                cortes.append((e["base_label"], k, n, SLOTS[k]))
                v["mons"] = v["mons"][:SLOTS[k]]
    return cortes


def liga_kanto(g, no_repo):
    """Tira `_FireRed` do rótulo, que é o que joga a entrada no ramo EMERALD."""
    labels = {e["base_label"] for e in g["encounters"]}
    mudados, recusados = [], []
    for e in g["encounters"]:
        if versao(e["base_label"]) != "FIRERED":
            continue
        novo = e["base_label"].replace("_FireRed", "")
        if novo in labels or e["map"] not in no_repo:
            recusados.append((e["base_label"], e["map"]))
            continue
        labels.discard(e["base_label"])
        labels.add(novo)
        mudados.append((e["base_label"], novo))
        e["base_label"] = novo
    return mudados, recusados


# ----------------------------------------------------------------- relatório

def por_regiao(g):
    """Quantos mapas de cada região têm tabela que a build de verdade enxerga."""
    conta = {}
    for e in g["encounters"]:
        if versao(e["base_label"]) != "EMERALD":
            continue
        conta.setdefault(e["map"], True)
    return conta


BW3G = os.path.join(FONTES, "bw3g")
# Gen 2 -> gen 3 no NOME da espécie. Só o que não casa por prefixo.
GEN2_ESPECIE = {"NIDORAN_M": "NIDORAN_M", "NIDORAN_F": "NIDORAN_F",
                "FARFETCH_D": "FARFETCHD", "MR__MIME": "MR_MIME",
                "HO_OH": "HO_OH", "PORYGON_Z": "PORYGON_Z",
                "MIME_JR_": "MIME_JR", "MR__RIME": "MR_RIME"}


def le_wild_gen2():
    """{constante do mapa: {'grama': (taxa%, [(nivel, especie)] x3), 'agua': ...}}

    Formato do BW3G, medido nos arquivos: `map_id X`, depois `db N percent`
    (uma taxa para água, três para grama: morn/day/nite), depois os slots como
    `db nivel, ESPECIE`. Grama tem 10 slots por horário (`GrassMonProbTable`),
    água tem 3 (`WaterMonProbTable`). Linha comentada com `;` é enxame
    desativado e não conta.
    """
    import glob
    fora = {}
    for kind, arqs in (("grama", ("johto_grass.asm", "kanto_grass.asm")),
                       ("agua", ("johto_water.asm", "kanto_water.asm"))):
        n_slots = 10 if kind == "grama" else 3
        for nome in arqs:
            p = os.path.join(BW3G, "data/wild", nome)
            if not os.path.exists(p):
                continue
            linhas = [l.split(";")[0].strip() for l in open(p, encoding="utf-8",
                                                            errors="replace")]
            i, atual = 0, None
            while i < len(linhas):
                l = linhas[i]
                m = re.match(r"map_id\s+(\w+)$", l)
                if m:
                    atual = m.group(1)
                    taxas = []
                    slots = []
                    i += 1
                    while i < len(linhas) and not re.match(r"map_id\s", linhas[i]):
                        mt = re.findall(r"(\d+)\s*percent", linhas[i])
                        if mt and not slots:
                            taxas = [int(x) for x in mt]
                        ms = re.match(r"db\s+(\d+),\s*([A-Z0-9_]+)\s*$", linhas[i])
                        if ms:
                            slots.append((int(ms.group(1)), ms.group(2)))
                        i += 1
                    blocos = [slots[k:k + n_slots] for k in range(0, len(slots), n_slots)]
                    fora.setdefault(atual, {})[kind] = (taxas, blocos)
                    continue
                i += 1
    _ = glob
    return fora


def confere_unova():
    """Espécie, nível e taxa dos mapas de Unova contra o BW3G, slot a slot.

    Só grama e água: a pesca do gen 2 não é por mapa, é por FISHGROUP escolhido
    no header do mapa (`data/wild/fish.asm`), e comparar por mapa aqui seria
    comparar contra a régua errada.
    """
    fonte = le_wild_gen2()
    g = grupo_principal(carrega())
    validas = especies_validas()
    nossos = {e["map"]: e for e in g["encounters"] if e["map"].startswith("MAP_UNOVA_")}

    def esp(n):
        return "SPECIES_" + GEN2_ESPECIE.get(n, n)

    casados, difs, sem_par, esp_ruim = 0, [], [], set()
    for const, dados in sorted(fonte.items()):
        mid = "MAP_UNOVA_" + const
        e = nossos.get(mid)
        if e is None:
            sem_par.append(const)
            continue
        casados += 1
        for kind, campo, n in (("grama", "land_mons", 10), ("agua", "water_mons", 3)):
            if kind not in dados:
                continue
            taxas, blocos = dados[kind]
            if not blocos or not any(blocos):
                continue
            if campo not in e:
                difs.append((mid, campo, "fonte tem, aqui não"))
                continue
            meus = e[campo]["mons"]
            # A tabela base é a de dia; o BW3G repete morn/day/nite quando não
            # há diferença. Aceita casar com qualquer um dos três blocos, e diz
            # qual, para que "descartei a noite" seja afirmação medida.
            alvo = [(m["max_level"], m["species"]) for m in meus[:n]]
            achou = None
            for j, bloco in enumerate(blocos[:3]):
                if [(lv, esp(sp)) for lv, sp in bloco] == alvo:
                    achou = ("morn", "day", "nite")[j]
                    break
            if achou is None:
                difs.append((mid, campo, "slots diferem",
                             [(lv, esp(sp)) for lv, sp in blocos[0]], alvo))
            esp_ruim |= {esp(sp) for bloco in blocos for _, sp in bloco
                         if esp(sp) not in validas}
            esperado = round(taxas[0] * 1.8) if taxas else None
            if esperado is not None and abs(e[campo]["encounter_rate"] - esperado) > 1:
                difs.append((mid, campo, "taxa",
                             f"fonte {taxas[0]}% -> {esperado}",
                             e[campo]["encounter_rate"]))
    print(f"[Unova] mapas com encontro no BW3G: {len(fonte)}; casados com mapa "
          f"nosso: {casados}; sem par aqui: {len(sem_par)} {sem_par}")
    print(f"[Unova] divergências de espécie/nível/taxa: {len(difs)}")
    for x in difs[:20]:
        print("   ", x)
    print(f"[Unova] espécie do BW3G sem símbolo no expansion: {sorted(esp_ruim)}")
    sobra = sorted(set(nossos) - {"MAP_UNOVA_" + c for c in fonte})
    print(f"[Unova] tabela nossa sem encontro na fonte: {len(sobra)} {sobra}")


def curva():
    """Nível do SELVAGEM por região, na ordem cronológica das cinco.

    `dev_scripts/curva_de_nivel.py` mede a curva do TREINADOR, lendo
    `trainers.party`, e não vê tabela de encontro. Sem esta medida o bloco B8
    remapearia metade da curva: o jogador chega em Sinnoh com time de nível 145
    e a grama continua cuspindo nível 12 do Platinum. Só MEDE.
    """
    import completude as C
    import importa_npcs_sinnoh as I

    mg = C.todos_os_mapas(RAIZ)
    sinnoh = set(I.nossos_mapas_sinnoh())

    def ids(pastas):
        fora = set()
        for p in pastas:
            pj = os.path.join(RAIZ, "data/maps", p, "map.json")
            if os.path.exists(pj):
                with open(pj, encoding="utf-8") as f:
                    mid = json.load(f).get("id")
                if mid:
                    fora.add(mid)
        return fora

    regiao = {}
    for nome, chave in (("Kanto", "Frlg"), ("Johto", "Johto"),
                        ("Hoenn", "TownsAndRoutes"), ("Unova", "Unova")):
        regiao[nome] = ids(m for m in C.nossos_da_regiao(mg, chave) if m not in sinnoh)
    regiao["Sinnoh"] = ids(sinnoh)

    g = grupo_principal(carrega())
    niveis = {k: [] for k in regiao}
    for e in g["encounters"]:
        if versao(e["base_label"]) != "EMERALD":
            continue
        for nome, ms in regiao.items():
            if e["map"] in ms:
                for k, v in e.items():
                    if k.endswith("_mons"):
                        niveis[nome] += [m["max_level"] for m in v["mons"]]
                break

    print("CURVA DO SELVAGEM (nível máximo de cada slot que a build enxerga)")
    print("região     slots   mín   média  mediana   máx")
    ordem = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova"]
    resumo = []
    for nome in ordem:
        v = sorted(niveis[nome])
        if not v:
            print(f"{nome:<10} {'0':>5}   (sem tabela)")
            resumo.append(None)
            continue
        med = v[len(v) // 2]
        print(f"{nome:<10} {len(v):>5} {v[0]:>5} {sum(v)/len(v):>7.1f} "
              f"{med:>8} {v[-1]:>5}")
        resumo.append((v[0], med, v[-1]))
    quebras = [(ordem[i], ordem[i + 1]) for i in range(4)
               if resumo[i] and resumo[i + 1] and resumo[i + 1][1] < resumo[i][1]]
    print("quebra de monotonicidade (mediana cai da região para a seguinte): "
          + (str(quebras) if quebras else "nenhuma"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--analise", action="store_true")
    ap.add_argument("--curva", action="store_true")
    ap.add_argument("--unova", action="store_true")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        return demo()
    if args.curva:
        return curva()
    if args.unova:
        return confere_unova()

    validas = especies_validas()
    no_repo = mapas_do_repo()
    d = carrega()
    g = grupo_principal(d)
    checa_schema(g)

    antes_emerald = len(por_regiao(g))
    print(f"mapas com tabela VISÍVEL na build (-DEMERALD), antes: {antes_emerald}")

    # 1. Kanto
    mudados, recusados = liga_kanto(g, no_repo)
    print(f"[Kanto] rótulos `_FireRed` religados ao ramo EMERALD: {len(mudados)}"
          f" (recusados: {len(recusados)})")

    # 2. duplicata de alvo errado
    antes_n = len(g["encounters"])
    g["encounters"] = [e for e in g["encounters"]
                       if e["base_label"] not in FORA_ALVO_ERRADO]
    print(f"[Hoenn] tabelas de Sinnoh penduradas em mapa de Hoenn, removidas: "
          f"{antes_n - len(g['encounters'])} {sorted(FORA_ALVO_ERRADO)}")

    # 3. Sinnoh
    descartes = {k: 0 for k in ("day", "night", "radar", "swarms", "versao",
                                "forma", "cauda_pesca")}
    novas = entradas_sinnoh(descartes)
    por_mapa = {e["map"]: e for e in g["encounters"]}
    usados = {e["base_label"] for e in g["encounters"]}
    troca, cria = 0, 0
    for mid, pasta, tabela, _stem in novas:
        if mid not in no_repo:
            print(f"  ! {mid} não existe em map_groups.h, pulado")
            continue
        alvo = por_mapa.get(mid)
        if alvo is not None:
            for k in list(alvo):
                if k.endswith("_mons"):
                    del alvo[k]
            alvo.update(tabela)
            troca += 1
        else:
            lab = rotulo(pasta, usados)
            nova = {"map": mid, "base_label": lab}
            nova.update(tabela)
            g["encounters"].append(nova)
            por_mapa[mid] = nova
            cria += 1
    print(f"[Sinnoh] {len(novas)} mapas da fonte: {cria} tabelas novas, "
          f"{troca} reescritas da fonte")
    print("[Sinnoh] descartado do gen 4, por categoria (mapas afetados):")
    print(f"  horário (day): {descartes['day']} mapas")
    print(f"  horário (night): {descartes['night']} mapas")
    print(f"  Poké Radar: {descartes['radar']} mapas")
    print(f"  swarm: {descartes['swarms']} mapas")
    print(f"  exclusiva de versão GBA: {descartes['versao']} mapas")
    print(f"  forma (Unown/Burmy): {descartes['forma']} mapas")
    print(f"  cauda da pesca: {descartes['cauda_pesca']} slots")

    # 4. Johto
    faltam = {"MAP_CLIFF_EDGE_CAVE", "MAP_CLIFF_EDGE_GATE", "MAP_DIGLETTS_CAVE_TUNNEL",
              "MAP_ROUTE26", "MAP_ROUTE27", "MAP_ROUTE28", "MAP_ROUTE47",
              "MAP_ROUTE48", "MAP_SAFARI_ZONE_GATE"} - set(por_mapa)
    jo, cortes = entradas_johto(faltam)
    for e in jo:
        if e["map"] not in no_repo:
            continue
        g["encounters"].append(e)
        por_mapa[e["map"]] = e
    print(f"[Johto] tabelas importadas do hns: {len(jo)}; podas: {cortes}")

    # 5. slot além do campo, venha de onde vier
    podadas = poda_slots(g)
    print(f"[slots] tabelas com mon além do slot declarado, podadas: {len(podadas)}")
    for x in podadas:
        print("   ", x)

    # 6. espécie inválida
    ruins = {}
    for e in g["encounters"]:
        for k, v in e.items():
            if not k.endswith("_mons"):
                continue
            for m in v["mons"]:
                if m["species"] not in validas:
                    ruins.setdefault(m["species"], []).append(e["base_label"])
    print(f"[espécies] símbolos fora de include/constants/species.h: {len(ruins)}"
          + ("" if not ruins else f" -> {sorted(ruins)}"))

    erro_slot = [(e["base_label"], k, len(v["mons"]))
                 for e in g["encounters"] for k, v in e.items()
                 if k.endswith("_mons") and len(v["mons"]) != SLOTS[k]]

    # 7. rótulo que o gerador leria como horário
    risco = [e["base_label"] for e in g["encounters"]
             if any(h in e["base_label"] for h in HORARIOS)]
    print(f"[rótulos] com palavra de horário (seriam engolidos): {len(risco)}")

    # 8. rótulo repetido vira símbolo C duplicado; mapa repetido no ramo EMERALD
    #    faz o motor usar sempre o primeiro e esconder o segundo.
    labels = [e["base_label"] for e in g["encounters"]]
    rep = sorted({x for x in labels if labels.count(x) > 1})
    vistos, dup_mapa = {}, []
    for e in g["encounters"]:
        if versao(e["base_label"]) != "EMERALD":
            continue
        vistos.setdefault(e["map"], []).append(e["base_label"])
    for m, v in vistos.items():
        # As 9 tabelas da Altering Cave (Hoenn e Kanto) são do vanilla: a mesma
        # caverna troca de conteúdo por evento Mystery Gift, e o jogo escolhe a
        # tabela por variável, não por mapa.
        if len(v) > 1 and m not in ("MAP_ALTERING_CAVE",
                                    "MAP_SIX_ISLAND_ALTERING_CAVE"):
            dup_mapa.append((m, v))
    print(f"[duplicata] rótulo repetido: {len(rep)}; mapa com duas tabelas "
          f"visíveis: {len(dup_mapa)} {dup_mapa}")

    depois = len(por_regiao(g))
    print(f"mapas com tabela VISÍVEL na build (-DEMERALD), depois: {depois}")

    if not args.aplica:
        print("\n(--analise: nada foi escrito)")
        return
    assert not ruins and not erro_slot and not risco and not rep and not dup_mapa, \
        "não escrevo com erro acima"
    with open(ALVO, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"escrito: {ALVO}")


def demo():
    """Asserts sobre a lógica que pode quebrar calada. Não escreve nada."""
    d = carrega()
    g = grupo_principal(d)
    checa_schema(g)

    # O sufixo de versão é o que decide o `#ifdef`, e é substring, não sufixo.
    assert versao("sViridianForest_FireRed") == "FIRERED"
    assert versao("sViridianForest") == "EMERALD"

    # A poda de vara tem que dar exatamente os 10 slots do campo.
    plat = {
        "land_rate": 0, "surf_rate": 0,
        "old_rod_rate": 25,
        "old_rod_encounters": [{"level_min": i, "level_max": i,
                                "species": "SPECIES_MAGIKARP"} for i in range(5)],
        "good_rod_rate": 25,
        "good_rod_encounters": [{"level_min": 10 + i, "level_max": 10 + i,
                                 "species": "SPECIES_GYARADOS"} for i in range(5)],
        "super_rod_rate": 25,
        "super_rod_encounters": [{"level_min": 20 + i, "level_max": 20 + i,
                                  "species": "SPECIES_REMORAID"} for i in range(5)],
    }
    desc = {k: 0 for k in ("day", "night", "radar", "swarms", "versao", "forma",
                           "cauda_pesca")}
    t = converte_sinnoh(plat, desc)
    assert len(t["fishing_mons"]["mons"]) == 10, t
    assert desc["cauda_pesca"] == 5, desc          # 3 da velha + 2 da boa
    # A super vara daqui (slots 5-9) tem que ser a super vara de lá, inteira.
    assert [m["min_level"] for m in t["fishing_mons"]["mons"][5:]] == [20, 21, 22, 23, 24]
    # A vara velha daqui (slots 0-1) são os dois primeiros de lá.
    assert [m["min_level"] for m in t["fishing_mons"]["mons"][:2]] == [0, 1]

    # Grama e surf casam slot a slot: 12 e 5, sem inventar nem cortar.
    plat2 = {"land_rate": 30,
             "land_encounters": [{"level": 5, "species": "SPECIES_BIDOOF"}] * 12,
             "surf_rate": 4,
             "surf_encounters": [{"level_min": 20, "level_max": 30,
                                  "species": "SPECIES_TENTACOOL"}] * 5}
    t2 = converte_sinnoh(plat2, desc)
    assert len(t2["land_mons"]["mons"]) == 12 and len(t2["water_mons"]["mons"]) == 5

    # Bloco com taxa 0 não vira tabela: seria encontro que nunca dispara.
    assert converte_sinnoh({"land_rate": 0, "surf_rate": 0}, desc) == {}

    # Rótulo com palavra de horário some na geração do header; tem que ser mudado.
    assert "Day" not in rotulo("PokemonDayCare", set())

    # A régua de Unova que este arquivo NÃO conserta, provada aqui para não
    # virar folclore: o arquivo do mapa tem "t" e a constante do encontro não.
    import inventario as V
    assert V.chave_simples("Rt1") != V.chave_simples("R_1")
    assert V.chave_simples("R22") == V.chave_simples("R_22")
    print("demo ok")


if __name__ == "__main__":
    main()
