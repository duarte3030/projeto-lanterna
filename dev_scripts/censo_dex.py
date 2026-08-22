#!/usr/bin/env python3
"""Censo de OBTENIBILIDADE da dex neste repo, medido no repo e não de memória.

    python3 censo_dex.py                 # tabela-resumo por categoria e por geração
    python3 censo_dex.py --csv saida.csv # lista completa, uma linha por espécie/forma
    python3 censo_dex.py --demo          # asserts, não escreve nada

Somente LEITURA. Nenhuma função aqui abre arquivo do repo para escrita.

O que ele lê, e por quê cada fonte
----------------------------------
`dev_scripts/catalogo_especies.py`  o universo de espécies e formas (já existe;
                                    não reimplementar). Só entra quem tem
                                    `.natDexNum`.
`src/data/wild_encounters.json`     grama, água, pesca e rock smash, por mapa.
`data/maps/*/map.json`              mapa -> região (mesma regra do completude.py)
                                    e objeto de overworld com gfx de espécie.
`data/maps/*/scripts.inc`           estático (`setwildbattle`, `seteventmon`),
`data/scripts/*.inc`                presente (`givemon`, `giveegg`).
`src/data/trade.h`                  troca in-game.
`src/data/pokemon/species_info/*.h` evoluções (método, alvo) e presença de
                                    `OVERWORLD(` (gfx de overworld, que é o que
                                    um encontro estático exige).

Armadilhas medidas, que valem para quem mexer aqui
--------------------------------------------------
1. **Região não sai do grupo do mapa.** O `completude.py` mede por sufixo no
   NOME do mapa ou do grupo (`_Frlg`, `Johto`, `Sinnoh`, `Unova`, `Galar`), e o
   que sobra é Hoenn. Galar tem 344 mapas em grupos alheios; sem o nome, eles
   caem em Hoenn.
2. **`setwildbattle` não é o único idioma de estático.** O lendário de cena de
   Johto/Hoenn/FRLG usa `seteventmon` + `BattleSetup_StartLegendaryBattle`. Quem
   contar só `setwildbattle` perde Lugia, Ho-Oh, Mew, Deoxys, Latias e Latios.
3. **Nível da fonte é registrado, não julgado.** O modo de teste rebaixa tudo
   para 5 em `CreateWildMon` e em `CreateScriptedWildMon`; a tabela continua
   com o nível da fonte, e é assim que fica.
4. **Forma não é espécie.** `SPECIES_UNOWN_B` é entrada própria do catálogo e
   precisa de fonte própria; o `RANDOM_UNOWN_LETTER` do motor sorteia a letra no
   encontro, então UNOWN é caso especial e está marcado como tal.
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

# Portado do scratchpad para dev_scripts/ em 21/08/2026: a raiz sai do
# proprio caminho do arquivo, e nao de um caminho absoluto decorado, para
# que completude.py possa importa-lo de qualquer diretorio de trabalho.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import catalogo_especies  # noqa: E402

# Mesma régua do completude.py: sufixo no nome do mapa OU do grupo.
MARCA_REGIAO = (("frlg", "Kanto"), ("johto", "Johto"), ("sinnoh", "Sinnoh"),
                ("unova", "Unova"), ("galar", "Galar"))
REGIOES = ("Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Galar",
           "Frontier")
CINCO = ("Kanto", "Johto", "Hoenn", "Sinnoh", "Unova")

TIPOS_SELVAGEM = ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons")

CATEGORIAS = ("selvagem", "estatico", "presente", "troca", "evolucao",
              "forma_permanente", "forma_batalha", "frontier", "inobtenivel")

# Tipos de troca de forma que deixam a forma DE PÉ fora da batalha (item
# segurado, item usado, hora do dia, clima do overworld, depósito no PC).
# Todo o resto reverte: `FORM_CHANGE_FAINT` e `FORM_CHANGE_END_BATTLE` aparecem
# 146 e 155 vezes no `form_change_tables.h` justamente para desfazer mega,
# gmax, primal e ultra burst. Contá-los como obtenção daria Mewtwo Mega como
# "espécie no bolso", que é falso.
FORMA_PERMANENTE = ("FORM_CHANGE_ITEM_HOLD", "FORM_CHANGE_ITEM_USE",
                    "FORM_CHANGE_ITEM_USE_MULTICHOICE", "FORM_CHANGE_MOVE",
                    "FORM_CHANGE_TIME_OF_DAY", "FORM_CHANGE_DAYS_PASSED",
                    "FORM_CHANGE_OVERWORLD_WEATHER", "FORM_CHANGE_WITHDRAW",
                    "FORM_CHANGE_DEPOSIT", "FORM_CHANGE_END_BATTLE_ENVIRONMENT")
FORMA_REVERTE = ("FORM_CHANGE_TERMINATOR", "FORM_CHANGE_FAINT",
                 "FORM_CHANGE_END_BATTLE")


# --------------------------------------------------------------------------
# mapas e regiões
# --------------------------------------------------------------------------
def _regiao_de(nome_mapa, grupo):
    alvo = (nome_mapa + " " + grupo).lower()
    for marca, regiao in MARCA_REGIAO:
        if marca in alvo:
            return regiao
    return "Hoenn"


def mapas():
    """{MAP_ID: (pasta, regiao)}. MAP_ID é o que o wild_encounters.json usa."""
    g = json.load(open(os.path.join(RAIZ, "data/maps/map_groups.json")))
    grupo_de = {m: grp for grp in g["group_order"] for m in g[grp]}
    fora = {}
    for pasta, grupo in grupo_de.items():
        p = os.path.join(RAIZ, "data/maps", pasta, "map.json")
        if not os.path.exists(p):
            continue
        mid = json.load(open(p)).get("id")
        if mid:
            fora[mid] = (pasta, _regiao_de(pasta, grupo))
    return fora


# --------------------------------------------------------------------------
# fontes de obtenção
# --------------------------------------------------------------------------
def selvagem(mapa_regiao):
    """{especie: [(MAP_ID, regiao, tipo, nivel_min, nivel_max)]}."""
    d = json.load(open(os.path.join(RAIZ, "src/data/wild_encounters.json")))
    fora = collections.defaultdict(list)
    for grupo in d["wild_encounter_groups"]:
        # Só o gWildMonHeaders é mundo jogável. Battle Pyramid e Battle Pike
        # são tabelas do Frontier: quem contá-las como fonte dá por obtenível
        # (Squirtle, entre outros) o que só aparece dentro de uma facility de
        # pós-jogo, com o Pokémon devolvido no fim.
        frontier = not grupo.get("for_maps")
        for enc in grupo["encounters"]:
            mid = enc.get("map", enc.get("base_label", grupo["label"]))
            regiao = ("Frontier" if frontier
                      else mapa_regiao.get(mid, (None, "?"))[1])
            for tipo in TIPOS_SELVAGEM:
                if tipo not in enc:
                    continue
                for mon in enc[tipo]["mons"]:
                    fora[mon["species"]].append(
                        (mid, regiao, tipo, mon["min_level"], mon["max_level"]))
    return fora


# Fontes que NÃO passam por tabela nem por script, e que um censo ingênuo perde.
# `gWildFeebas` mora em `src/wild_encounter.c:66` e é sorteado por tile em
# Route 119; não existe linha nenhuma de Feebas no wild_encounters.json.
ESPECIAIS = {
    "SPECIES_FEEBAS": ("Route119", "Hoenn", "gWildFeebas (tile de pesca)", 20),
}


def _varre_scripts():
    """[(pasta_ou_'', caminho, comando, especie, nivel)] de todo .inc de data/."""
    achados = []
    padrao = re.compile(
        r"^\s*(setwildbattle|seteventmon|givemon|giveegg)\s+"
        r"(SPECIES_[A-Z0-9_]+)\s*(?:,\s*(\d+))?", re.M)
    for base, _dirs, arqs in os.walk(os.path.join(RAIZ, "data")):
        for a in arqs:
            if not a.endswith(".inc"):
                continue
            # O menu de debug dá qualquer Pokémon; contá-lo faria a régua
            # declarar Bulbasaur, Squirtle e companhia "presentes" por um
            # caminho que o jogador não tem.
            if a == "debug.inc":
                continue
            caminho = os.path.join(base, a)
            txt = open(caminho, encoding="utf-8", errors="replace").read()
            pasta = ""
            partes = caminho.split(os.sep)
            if "maps" in partes:
                i = partes.index("maps")
                if i + 1 < len(partes):
                    pasta = partes[i + 1]
            for m in padrao.finditer(txt):
                achados.append((pasta, caminho, m.group(1), m.group(2),
                                int(m.group(3) or 0)))
            # Presente INDIRETO: os starters de Kanto e os prêmios do Game
            # Corner não passam espécie literal para o `givemon`; passam uma
            # VAR que foi carregada antes (`setvar PLAYER_STARTER_SPECIES,
            # SPECIES_BULBASAUR` ... `givemon PLAYER_STARTER_SPECIES, 5`).
            # Quem só casar `givemon SPECIES_` perde os três iniciais de Kanto
            # e os seis prêmios de Celadon.
            vars_dadas = set(re.findall(
                r"^\s*give(?:mon|egg)\s+([A-Z][A-Z0-9_]*)", txt, re.M))
            vars_dadas -= {"SPECIES_" + v for v in vars_dadas}
            for m in re.finditer(
                    r"^\s*setvar\s+([A-Z][A-Z0-9_]*)\s*,\s*(SPECIES_[A-Z0-9_]+)",
                    txt, re.M):
                if m.group(1) in vars_dadas:
                    achados.append((pasta, caminho, "givemon", m.group(2), 0))
    return achados


def estatico_e_presente(mapa_regiao):
    """({especie: [ocorrencia]}, {especie: [ocorrencia]}) para estático e presente."""
    pasta_regiao = {p: r for _mid, (p, r) in mapa_regiao.items()}
    est = collections.defaultdict(list)
    pre = collections.defaultdict(list)
    for pasta, caminho, cmd, esp, nivel in _varre_scripts():
        regiao = pasta_regiao.get(pasta, "?")
        oco = (pasta or os.path.basename(caminho), regiao, cmd, nivel)
        (est if cmd in ("setwildbattle", "seteventmon") else pre)[esp].append(oco)
    return est, pre


def troca():
    """{especie: n} das trocas in-game (o que o NPC ENTREGA)."""
    txt = open(os.path.join(RAIZ, "src/data/trade.h"), encoding="utf-8").read()
    fora = collections.Counter()
    for m in re.finditer(r"^\s*\.species\s*=\s*(SPECIES_[A-Z0-9_]+)", txt, re.M):
        fora[m.group(1)] += 1
    return fora


def evolucoes():
    """{alvo: [(de, metodo, param, condicoes)]} lido do species_info."""
    fora = collections.defaultdict(list)
    for gen in range(1, 10):
        p = os.path.join(RAIZ, "src/data/pokemon/species_info",
                         f"gen_{gen}_families.h")
        txt = open(p, encoding="utf-8").read()
        for nome, corpo in catalogo_especies._blocos(txt):
            m = re.search(r"\.evolutions\s*=\s*EVOLUTION\(", corpo)
            if not m:
                continue
            i = corpo.index("(", m.start() + len(".evolutions = EVOLUTION") - 1)
            nivel, j = 0, i
            while j < len(corpo):
                if corpo[j] == "(":
                    nivel += 1
                elif corpo[j] == ")":
                    nivel -= 1
                    if nivel == 0:
                        break
                j += 1
            bloco = corpo[i + 1:j]
            # ARMADILHA: não exigir o `}` de fechamento aqui. Uma entrada como
            # `{EVO_ITEM, ITEM_THUNDER_STONE, SPECIES_RAICHU,
            #   CONDITIONS({IF_NOT_REGION, REGION_ALOLA})}` tem chave ANINHADA
            # dentro do CONDITIONS, e o regex que casava até o `}` seguido de
            # vírgula devolvia None para Raichu, Vileplume, Typhlosion e mais
            # 60 espécies, que caíam em "inobtenível" sem motivo.
            for e in re.finditer(
                    r"\{\s*(EVO_[A-Z_]+)\s*,\s*([^,]+?)\s*,\s*(SPECIES_[A-Z0-9_]+)"
                    r"\s*(,\s*CONDITIONS\((?:[^()]|\([^()]*\))*\))?", bloco, re.S):
                cond = " ".join((e.group(4) or "").split())[:140]
                fora[e.group(3)].append(
                    (nome, e.group(1), e.group(2).strip(), cond))
    return fora


def alias():
    """{apelido: alvo} do `species.h`: `SPECIES_DEOXYS = SPECIES_DEOXYS_NORMAL`.

    São 97 e não contam como entrada nova; quem somar os 1.668 ids do enum sem
    tirá-los infla o total da dex em 6%.
    """
    txt = open(os.path.join(RAIZ, "include/constants/species.h")).read()
    return {m.group(1): m.group(2) for m in re.finditer(
        r"^\s*(SPECIES_[A-Z0-9_]+)\s*=\s*(SPECIES_[A-Z0-9_]+)\s*,", txt, re.M)}


def entradas_macro(cat):
    """Entradas do species_info escritas por MACRO, que o catálogo não enxerga.

    ARMADILHA MEDIDA: `catalogo_especies._blocos` só casa
    `[SPECIES_X] =` seguido de `{` em linha própria, e exige `.natDexNum` no
    corpo. As 243 entradas escritas como `[SPECIES_UNOWN_B] =
    UNOWN_MISC_INFO(B, ...)` ficam de fora: as 28 letras do Unown, os 63
    Alcremie, os 20 padrões de Vivillon (mais Scatterbug e Spewpa), os 18
    Arceus, os 18 Silvally, os 14 Minior, os 10 Furfrou, os 8 Ogerpon, os 6
    Floette e os 5 Genesect. Sem elas o censo diz 1.328 quando o repo tem
    1.571, e some justamente o que o Gui pediu para conferir (as 28 formas do
    Unown e os padrões do Vivillon).

    A geração e o número de dex saem do `form_species_tables.h`: cada tabela
    lista as formas de UMA espécie, então basta achar na tabela um membro que
    o catálogo já conhece e herdar dele.
    """
    info = ""
    for gen in range(1, 10):
        info += open(os.path.join(RAIZ, "src/data/pokemon/species_info",
                                  f"gen_{gen}_families.h"), encoding="utf-8").read()
    presentes = set(re.findall(r"\[\s*(SPECIES_[A-Z0-9_]+)\s*\]\s*=", info))
    ap = alias()
    faltam = {n for n in presentes if n not in cat and n not in ap}

    # A geração e o número de dex saem do NOME: `SPECIES_UNOWN_B` ->
    # `NATIONAL_DEX_UNOWN`, `SPECIES_ALCREMIE_BERRY_CARAMEL_SWIRL` ->
    # `NATIONAL_DEX_ALCREMIE`. Tentar herdar do `form_species_tables.h` não
    # basta: a tabela do Unown tem 28 membros e NENHUM deles está no catálogo,
    # porque a entrada-base `[SPECIES_UNOWN]` também é macro.
    dexnum = catalogo_especies._dex_numeros()
    modelo_por_dex = {e.dex: e for e in cat.values() if e.base}
    fora = {}
    for x in sorted(faltam):
        partes = x.replace("SPECIES_", "").split("_")
        for corte in range(len(partes), 0, -1):
            chave = "NATIONAL_DEX_" + "_".join(partes[:corte])
            if chave in dexnum:
                n = dexnum[chave]
                modelo = modelo_por_dex.get(n)
                if modelo is None:
                    modelo = catalogo_especies.Especie(
                        nome=x, gen=catalogo_especies._gen_do_dex(n), dex=n,
                        tipos=(), bst=0, lenda=False, base=False,
                        familia=None, stats={})
                fora[x] = modelo._replace(nome=x, base=False)
                break
    return fora


def formas():
    """{alvo: [(de, tipo, param)]} lido do form_change_tables + species_info.

    `.formChangeTable = sRotomFormChangeTable` mora no species_info; a tabela
    em si mora no form_change_tables.h. Sem cruzar os dois não dá para dizer
    de QUEM a forma sai.
    """
    txt = open(os.path.join(RAIZ, "src/data/pokemon/form_change_tables.h"),
               encoding="utf-8").read()
    tabelas = {}
    for m in re.finditer(
            r"static const struct FormChange (s\w+)\[\]\s*=\s*\{(.*?)\n\};",
            txt, re.S):
        linhas = []
        for e in re.finditer(
                r"\{\s*(FORM_CHANGE_[A-Z_]+)\s*(?:,\s*(SPECIES_[A-Z0-9_]+))?"
                r"\s*(?:,\s*([^,}]+))?", m.group(2)):
            if e.group(2):
                linhas.append((e.group(1), e.group(2),
                               (e.group(3) or "").strip()))
        tabelas[m.group(1)] = linhas
    fora = collections.defaultdict(list)
    for gen in range(1, 10):
        p = os.path.join(RAIZ, "src/data/pokemon/species_info",
                         f"gen_{gen}_families.h")
        stxt = open(p, encoding="utf-8").read()
        dono = {}
        for nome, corpo in catalogo_especies._blocos(stxt):
            m = re.search(r"\.formChangeTable\s*=\s*(s\w+)", corpo)
            if m:
                dono[nome] = m.group(1)
        # SEGUNDA ARMADILHA das macros: Arceus, Silvally, Vivillon, Furfrou,
        # Minior, Genesect e Alcremie declaram `.formChangeTable` DENTRO do
        # `#define X_SPECIES_INFO(...)`, não no corpo da entrada. Sem ler a
        # macro, as 18 formas do Arceus e as 18 do Silvally continuam
        # "inobteníveis" mesmo depois de o Arceus ganhar fonte, o que faria o
        # plano mandar distribuir 36 estáticos que o motor já resolve com uma
        # placa segurada.
        macro_tab = {}
        for m in re.finditer(r"^#define\s+(\w+)\(([^)]*)\)((?:.*\\\n)*.*)$",
                             stxt, re.M):
            mt = re.search(r"\.formChangeTable\s*=\s*(s\w+)", m.group(3))
            if mt:
                macro_tab[m.group(1)] = mt.group(1)
        for m in re.finditer(r"\[\s*(SPECIES_[A-Z0-9_]+)\s*\]\s*=\s*(\w+)\(",
                             stxt):
            if m.group(2) in macro_tab:
                dono.setdefault(m.group(1), macro_tab[m.group(2)])
        for nome, tab in dono.items():
            for tipo, alvo, param in tabelas.get(tab, []):
                if alvo != nome:
                    fora[alvo].append((nome, tipo, param))
    return fora


def com_overworld():
    """Nomes com a macro OVERWORLD( no species_info: dá para virar estático."""
    fora = set()
    for gen in range(1, 10):
        p = os.path.join(RAIZ, "src/data/pokemon/species_info",
                         f"gen_{gen}_families.h")
        txt = open(p, encoding="utf-8").read()
        for nome, corpo in catalogo_especies._blocos(txt):
            if "OVERWORLD(" in corpo:
                fora.add(nome)
    return fora


# --------------------------------------------------------------------------
# censo
# --------------------------------------------------------------------------
_UNOWN = re.compile(r"^SPECIES_UNOWN")

Linha = collections.namedtuple(
    "Linha", "nome gen dex base lenda categoria regioes detalhe ow")

# Métodos de evolução que FUNCIONAM sem nada além do jogo solo neste motor.
# EVO_TRADE precisa de link (não há item de cabo neste repo, medido) e
# EVO_SCRIPT_TRIGGER precisa de um script que exista em algum mapa.
EVO_SOLO = ("EVO_LEVEL", "EVO_ITEM", "EVO_BATTLE_END", "EVO_LEVEL_BATTLE_ONLY",
            "EVO_SPLIT_FROM_EVO", "EVO_SPIN")

# MEDIDO em `include/regions.h`: `GetRegionForSectionId` só devolve
# REGION_KANTO (mapsec do FRLG) ou REGION_HOENN. Nunca JOHTO, SINNOH, UNOVA,
# ALOLA, GALAR, HISUI ou PALDEA, apesar de o enum ter os dez. Portanto TODA
# evolução com `{IF_REGION, REGION_X}` para X fora dessas duas é código morto
# neste motor, e toda `{IF_NOT_REGION, REGION_X}` é sempre verdadeira.
REGIOES_QUE_O_MOTOR_DEVOLVE = ("REGION_KANTO", "REGION_HOENN")


def _evo_travada(metodo, cond):
    """Motivo pelo qual esta evolução não roda no jogo solo, ou ''."""
    if metodo == "EVO_NONE":
        return "EVO_NONE (nao e evolucao de verdade; forma de Totem)"
    if metodo == "EVO_TRADE":
        return "EVO_TRADE (precisa de link; nao ha item de cabo neste repo)"
    if metodo == "EVO_SCRIPT_TRIGGER":
        return "EVO_SCRIPT_TRIGGER (nenhum script de data/ dispara o gatilho)"
    m = re.search(r"IF_REGION,\s*(REGION_[A-Z]+)", cond)
    if m and m.group(1) not in REGIOES_QUE_O_MOTOR_DEVOLVE:
        return f"IF_REGION {m.group(1)}: GetCurrentRegion() nunca devolve isso"
    if metodo not in EVO_SOLO:
        return f"metodo {metodo} sem caminho solo"
    return ""


def censo():
    mapa_regiao = mapas()
    sel = selvagem(mapa_regiao)
    est, pre = estatico_e_presente(mapa_regiao)
    for esp, oco in ESPECIAIS.items():
        est.setdefault(esp, []).append(oco)
    tro = troca()
    evo = evolucoes()
    ow = com_overworld()
    fmc = formas()
    cat = catalogo_especies.carrega()
    cat.update(entradas_macro(cat))

    # Alcançável por evolução: fecho a partir de quem já tem fonte direta.
    # Frontier NÃO é fonte: no Battle Pyramid não se captura, o Pokémon é
    # emprestado. Espécie que só aparece lá fica na categoria própria.
    sel_mundo = {n: [o for o in oc if o[1] != "Frontier"] for n, oc in sel.items()}
    sel_mundo = {n: oc for n, oc in sel_mundo.items() if oc}

    # UNOWN: `CreateWildMon` chama `GetMonPersonality(..., RANDOM_UNOWN_LETTER)`
    # e `pokemon.c` sorteia a letra na personalidade. Uma única linha de Unown
    # em tabela selvagem entrega as 28 formas; tratá-las como 28 espécies a
    # distribuir seria inventar trabalho que o motor já faz.
    if any(n.startswith("SPECIES_UNOWN") for n in sel_mundo):
        for n in list(cat):
            if n.startswith("SPECIES_UNOWN") and n not in sel_mundo:
                sel_mundo[n] = sel_mundo[next(
                    k for k in sel if k.startswith("SPECIES_UNOWN"))]
                sel[n] = sel_mundo[n]

    direto = set(sel_mundo) | set(est) | set(pre) | set(tro)
    direto &= set(cat)
    alcancavel = set(direto)
    mudou = True
    while mudou:
        mudou = False
        for alvo, origens in evo.items():
            if alvo in alcancavel:
                continue
            for de, metodo, _param, _cond in origens:
                if de in alcancavel and not _evo_travada(metodo, _cond):
                    alcancavel.add(alvo)
                    mudou = True
                    break

    # Alcancavel TAMBEM por troca de forma que nao reverte. Sem este segundo
    # fecho o censo so enxerga UM passo de forma, e uma corrente de duas
    # quebra calada: Deoxys-Defesa e Deoxys-Velocidade saem do Deoxys-Ataque,
    # que por sua vez sai do Normal, e as tres formas de Zygarde com Power
    # Construct saem umas das outras pelo Cube. Eram justamente esses os 5
    # "inobteniveis" de 22/08/2026. `distribui_dex._fecha` sempre fechou assim
    # e dizia no comentario que era "a mesma regra" do censo; nao era, e a
    # divergencia e que fazia a conta parar em 1.566.
    # Fica em conjunto SEPARADO de proposito: `alcancavel` sozinho decide a
    # categoria "evolucao", e forma que virasse "evolucao" perderia o detalhe.
    alc_forma = set(alcancavel)
    mudou = True
    while mudou:
        mudou = False
        for alvo, origens in fmc.items():
            if alvo in alc_forma:
                continue
            for de, t_, _p in origens:
                if t_ not in FORMA_REVERTE and de in alc_forma:
                    alc_forma.add(alvo)
                    mudou = True
                    break
        for alvo, origens in evo.items():
            if alvo in alc_forma:
                continue
            for de, metodo, _param, _cond in origens:
                if de in alc_forma and not _evo_travada(metodo, _cond):
                    alc_forma.add(alvo)
                    mudou = True
                    break

    linhas = []
    for nome, e in sorted(cat.items(), key=lambda kv: (kv[1].dex, kv[0])):
        regioes, detalhe = set(), ""
        if nome in sel_mundo:
            categoria = "selvagem"
            regioes = {r for _m, r, _t, _a, _b in sel[nome]}
            tipos = collections.Counter(t for _m, _r, t, _a, _b in sel[nome])
            niv = [a for _m, _r, _t, a, _b in sel[nome]]
            detalhe = (f"{len(sel[nome])} slots em "
                       f"{len({m for m, *_ in sel[nome]})} mapas; "
                       f"{'/'.join(sorted(tipos))}; "
                       f"nivel fonte {min(niv)}-{max(b for *_x, b in sel[nome])}")
        elif nome in est:
            categoria = "estatico"
            regioes = {r for _p, r, _c, _n in est[nome]}
            detalhe = "; ".join(f"{p} ({c} lv {n})" for p, _r, c, n in est[nome])
        elif nome in pre:
            categoria = "presente"
            regioes = {r for _p, r, _c, _n in pre[nome]}
            detalhe = "; ".join(f"{p} ({c} lv {n})" for p, _r, c, n in pre[nome])
        elif nome in tro:
            categoria = "troca"
            detalhe = f"{tro[nome]} troca(s) in-game"
        elif nome in alcancavel:
            categoria = "evolucao"
            detalhe = "; ".join(
                f"de {de.replace('SPECIES_', '')} por {met}"
                + (f" {par}" if par not in ("0", "") else "")
                + (f" [{cond}]" if cond else "")
                for de, met, par, cond in evo.get(nome, []))
        elif nome in fmc and any(
                t_ in FORMA_PERMANENTE and de in alc_forma
                for de, t_, _p in fmc[nome]):
            categoria = "forma_permanente"
            detalhe = "; ".join(
                f"de {de.replace('SPECIES_', '')} por {t_} {p}"
                for de, t_, p in fmc[nome]
                if t_ in FORMA_PERMANENTE and de in alc_forma)
        elif nome in fmc and any(
                t_ not in FORMA_REVERTE and de in alc_forma
                for de, t_, _p in fmc[nome]):
            categoria = "forma_batalha"
            detalhe = "; ".join(
                f"de {de.replace('SPECIES_', '')} por {t_} {p}"
                for de, t_, p in fmc[nome]
                if t_ not in FORMA_REVERTE and de in alc_forma)[:200]
        elif nome in sel:
            categoria = "frontier"
            regioes = {"Frontier"}
            detalhe = f"{len(sel[nome])} slots so em Battle Pyramid/Pike"
        else:
            categoria = "inobtenivel"
            if nome in evo:
                detalhe = "so por evolucao travada: " + "; ".join(
                    f"de {de.replace('SPECIES_', '')} por {met}"
                    for de, met, _p, _c in evo[nome])
        linhas.append(Linha(nome, e.gen, e.dex, e.base, e.lenda, categoria,
                            ",".join(sorted(regioes)), detalhe, nome in ow))
    return linhas


def resumo(linhas):
    por_cat = collections.Counter(l.categoria for l in linhas)
    return por_cat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    linhas = censo()
    cat = collections.Counter(l.categoria for l in linhas)
    total = len(linhas)
    print(f"entradas com natDexNum: {total} "
          f"({sum(l.base for l in linhas)} bases, "
          f"{sum(not l.base for l in linhas)} formas)")
    print(f"{'categoria':<13} {'total':>6} {'bases':>6} {'formas':>7} {'lendas':>7}")
    for c in CATEGORIAS:
        sub = [l for l in linhas if l.categoria == c]
        print(f"{c:<13} {len(sub):>6} {sum(l.base for l in sub):>6} "
              f"{sum(not l.base for l in sub):>7} {sum(l.lenda for l in sub):>7}")
    print()
    print(f"{'gen':>4} " + " ".join(f"{c[:8]:>9}" for c in CATEGORIAS))
    for g in range(1, 10):
        sub = [l for l in linhas if l.gen == g]
        print(f"{g:>4} " + " ".join(
            f"{sum(l.categoria == c for l in sub):>9}" for c in CATEGORIAS))
    print()
    print("selvagem/estatico/presente por REGIAO (entradas distintas):")
    for r in REGIOES:
        n = len({l.nome for l in linhas if r in l.regioes.split(",")})
        print(f"  {r:<8} {n:>5}")
    ow_falta = [l for l in linhas if not l.ow]
    print(f"\nsem gfx de overworld (nao pode virar estatico): {len(ow_falta)}")
    print(f"inobteniveis SEM overworld: "
          f"{sum(1 for l in ow_falta if l.categoria == 'inobtenivel')}")
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["especie", "gen", "dex", "base", "lenda", "categoria",
                        "regioes", "tem_overworld", "detalhe"])
            for l in linhas:
                w.writerow([l.nome, l.gen, l.dex, int(l.base), int(l.lenda),
                            l.categoria, l.regioes, int(l.ow), l.detalhe])
        print(f"\nCSV: {a.csv} ({len(linhas)} linhas)")


def demo():
    m = mapas()
    assert m["MAP_ROUTE101"][1] == "Hoenn", m["MAP_ROUTE101"]
    assert m["MAP_ROUTE1"][1] == "Kanto", m.get("MAP_ROUTE1")
    assert m["MAP_LAKE_OF_RAGE"][1] == "Johto", m["MAP_LAKE_OF_RAGE"]

    linhas = censo()
    por_nome = {l.nome: l for l in linhas}
    # Estático que existe de verdade, nos dois idiomas.
    assert por_nome["SPECIES_HO_OH"].categoria == "estatico"
    assert por_nome["SPECIES_MEWTWO"].categoria == "estatico"
    assert por_nome["SPECIES_GYARADOS"].categoria in ("selvagem", "estatico")
    # Presente e troca.
    assert por_nome["SPECIES_TOTODILE"].categoria == "presente"
    # Inicial de Kanto: só existe por `givemon PLAYER_STARTER_SPECIES`.
    assert por_nome["SPECIES_PORYGON"].categoria == "presente"
    # Battle Pyramid não é fonte: Squirtle não pode contar como obtenível.
    assert por_nome["SPECIES_SQUIRTLE"].categoria == "presente"
    assert "Frontier" not in por_nome["SPECIES_SQUIRTLE"].regioes
    assert "?" not in {r for l in linhas for r in l.regioes.split(",")}
    # Evolução alcançável a partir de selvagem.
    assert por_nome["SPECIES_IVYSAUR"].categoria in ("selvagem", "evolucao")
    # Mega nunca vira encontro: tem de cair em inobtenivel ou evolucao travada.
    # Mega é forma de BATALHA: existe (tem pedra), mas reverte ao desmaiar e
    # ao fim da luta, então nunca é "espécie no bolso".
    assert por_nome["SPECIES_VENUSAUR_MEGA"].categoria == "forma_batalha"
    # Rotom-Calor sai do catálogo do Rotom e FICA: forma permanente.
    assert por_nome["SPECIES_ROTOM_HEAT"].categoria in (
        "forma_permanente", "inobtenivel")
    # Regional gated por IF_REGION nunca dispara neste motor. A afirmação é
    # sobre a REGRA, e não sobre o Raichu-de-Alola: em 21/08/2026 ele ganhou
    # linha de mato pela obra da Dex e virou "selvagem", o que deixou este
    # `assert` vermelho no HEAD sem que nada estivesse errado.
    assert _evo_travada("EVO_LEVEL", "IF_REGION, REGION_ALOLA")
    assert not _evo_travada("EVO_LEVEL", "")
    # Corrente de troca de forma de MAIS DE UM PASSO. Deoxys-Velocidade está a
    # três usos do Meteorito do Deoxys-Normal, que é estático de Ilha Nascente;
    # até 22/08/2026 o fecho do censo só andava por evolução e parava no
    # primeiro passo, e os cinco "inobteníveis" da rodada eram só isso.
    assert por_nome["SPECIES_DEOXYS_SPEED"].categoria == "forma_permanente", (
        por_nome["SPECIES_DEOXYS_SPEED"])
    assert por_nome["SPECIES_ZYGARDE_COMPLETE"].categoria == "forma_batalha"
    # Régua de sanidade do universo.
    assert len(linhas) > 1300, len(linhas)
    cat = collections.Counter(l.categoria for l in linhas)
    assert cat["selvagem"] > 100, cat

    # MUTAÇÃO PLANTADA: sem o segundo fecho, a corrente de dois passos volta a
    # quebrar. Se este bloco NÃO reprovar, o fecho de forma não está provando
    # nada e o 1.571 é decorado.
    global FORMA_REVERTE
    guarda = FORMA_REVERTE
    try:
        FORMA_REVERTE = FORMA_REVERTE + FORMA_PERMANENTE
        mutante = {l.nome: l for l in censo()}
        assert mutante["SPECIES_DEOXYS_SPEED"].categoria == "inobtenivel", (
            "mutação plantada NÃO reprovou: o fecho de forma não é o que "
            "sustenta o Deoxys-Velocidade")
    finally:
        FORMA_REVERTE = guarda
    print("demo OK:", dict(cat))


if __name__ == "__main__":
    sys.exit(main())
