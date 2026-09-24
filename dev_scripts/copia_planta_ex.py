#!/usr/bin/env python3
"""Copia a PLANTA de um mapa do Pokémon Emerald EX v1.0.4 para o nosso jogo (frente Hoenn EX).

ESTADO (23/09/2026, piloto de Petalburg verde, T310/T311): FAZ lista, aumenta (translação e
plano de remapeamento), novo, conexoes (dois lados), eventos (fala, placa, item, treinador,
warp) e encontros. Item escondido usa a faixa `ocultos` do lote (0x1F00+, cujo valor
real cabe nos 13 bits do hiddenItemId). AINDA NÃO FAZ: base secreta, gatilho de enredo (pendência), treinador
duplo e órfão da reserva (entra quando o lote precisar), golpes e item segurado do time do EX.

Por que existe
--------------
A frente Hoenn EX (PLANO-HOENN-EX.md, decisão 88 do Gui) traz para a nossa Hoenn
as plantas aumentadas e as áreas novas do Emerald EX. O EX não tem fonte
publicada: tudo sai da ROM. Este script é a peça comum dos três lotes da onda 1
e faz, mapa a mapa, o que o PLANO seção (d) manda, SEM inventar nada:

1. `aumenta`: mapa que já existe e cresceu. Troca `map.bin`, `border.bin`,
   `width` e `height` NO MESMO layout (mesmo `LAYOUT_*`, mesmo `mapLayoutId`:
   a save não muda). Os NOSSOS eventos andam o deslocamento medido em
   `offsets.json` quando a planta antiga está preservada em 75% ou mais
   (translação). Abaixo disso, NADA é movido sozinho: sai a lista de
   remapeamento prédio a prédio, com a PROVA de cada proposta (warp com o mesmo
   destino no EX, NPC com a mesma flag ou o mesmo texto), para decisão humana.
2. `novo`: mapa que não existe. Cria layout e mapa no FIM (`layouts.json` e o
   grupo destino da Tabela A do PLANO; interiores sem grupo próprio vão para o
   grupo novo `gMapGroup_IndoorHoennEx`, acrescentado no FIM do `group_order`).
3. `eventos`: extrai os eventos do EX (posição, sprite, movimento, raio, tipo) e
   os textos da ROM, casa com os nossos (até 1 célula e mesmo tipo; ou mesma
   flag; ou mesmo texto) e escreve os NOVOS no FIM das listas, com o script
   REESCRITO no nosso formato (fala, placa, item com flag da faixa do lote,
   treinador com id da faixa do lote). O que não for desses tipos vai para a
   lista de PENDÊNCIA, sem inventar.
4. `conexoes`: aplica as conexões do EX com o offset do EX, nos DOIS lados.
5. Imprime a lista de conflitos de tudo acima.

O que ele NÃO faz, de propósito
-------------------------------
- Não copia bytecode de script do EX. Script se reescreve a partir do texto.
- Não mexe em metatile redefinido pelo EX: isso é o `depara_metatiles_ex.py`
  (lote C). A planta sai com os índices do EX, que são os do vanilla.
- Não usa flag, id de treinador ou bloco de teste fora da faixa que o lote
  recebeu no briefing (`--faixa-flag`, `--faixa-id`).
- Não grava a ROM do EX nem nada dela no repositório: só o asset convertido.

Material privado (fora do repo): a ROM e a análise da onda 0 em
`fontes-mapas/romhacks/emerald-ex/`, lidos por caminho absoluto.

Uso
---
    copia_planta_ex.py lista 0.0                   # tudo que o EX tem no mapa
    copia_planta_ex.py aumenta 0.0 [--aplica]      # planta aumentada, eventos nossos
    copia_planta_ex.py novo 0.59 [--aplica]        # mapa novo no fim
    copia_planta_ex.py conexoes 0.0 [--aplica]     # conexões do EX, dos dois lados
    copia_planta_ex.py eventos 0.0 --lote A [--aplica]
    copia_planta_ex.py --autoteste

Sem `--aplica`, nada é escrito: imprime o que faria.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXDIR = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/emerald-ex"
ANALISE = EXDIR + "/analise"
ONDA0 = ANALISE + "/onda0"
VAN = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/pokeemerald"

# Faixas cravadas no briefing da onda 1 (23/09/2026). Nada fora delas.
LOTES = {
    "A": {"flags": (0x2F00, 0x2F3F), "ocultos": (0x1F00, 0x1F27), "ids": list(range(2060, 2077)) + list(range(2087, 2097))},
    "B": {"flags": (0x2F40, 0x2F7F), "ocultos": (0x1F28, 0x1F4F), "ids": list(range(2117, 2127)) + list(range(2140, 2154))},
    "C": {"flags": (0x2F80, 0x2FBF), "ocultos": (0x1F50, 0x1F77), "ids": list(range(2154, 2157))},
    # Onda 2 (briefing de 24/09/2026): os três lotes de ginásio dividem a entrada "onda-2" da
    # reserva de ids pela POSIÇÃO na lista ordenada (1 a 25, 26 a 45, 46 a 70; 71 a 80 ficam
    # com o condutor). "fatia" é essa faixa de posições, em índice Python.
    "G1": {"flags": (0x2FC0, 0x2FD4), "ocultos": (0x1F78, 0x1F7A), "ids": [], "reserva": "onda-2", "fatia": (0, 25)},
    "G2": {"flags": (0x2FD5, 0x2FE9), "ocultos": (0x1F7B, 0x1F7D), "ids": [], "reserva": "onda-2", "fatia": (25, 45)},
    "G3": {"flags": (0x2FEA, 0x2FFF), "ocultos": (0x1F7E, 0x1F7F), "ids": [], "reserva": "onda-2", "fatia": (45, 70)},
}

GRUPO_NOVO = "gMapGroup_IndoorHoennEx"

# Nome dos mapas NOVOS. Determinístico e compartilhado pelos três lotes, porque
# conexão e warp entre lotes apontam por nome. Quem não estiver aqui ganha o
# nome padrão de `nome_padrao_novo` (a cidade dona mais o índice do EX).
NOMES_NOVOS = {
    "0.4": "RustboroPart2",
    "0.17": "FoothillTown",
    "0.59": "Route135",
    "0.60": "Route136",
    "0.61": "Route137",
    "0.62": "Route138",
    "27.112": "MuscleIsland",
    "27.113": "DontoIsland",
    "27.114": "HauntedWoods",
    "27.115": "HauntedWoods_Inner",
    "27.116": "Route115_North",
    "27.118": "FrozenHeights",
    "27.119": "PetalburgWoods_River",  # faixa de rio de 16x6 que o EX liga às duas bordas do bosque (MAPSEC 62 é reuso de vaga do autor, não é o navio)
    "27.120": "AncientTomb_1F",
    "27.121": "AncientTomb_2F",
    "29.89": "SafariZone_FarNorth",
    "29.90": "Route133_Cave",
    # lote A: interiores, nome pela casa do EX (o texto de cada um está no commit)
    "8.7": "PetalburgCity_House3",
    "8.8": "PetalburgCity_House4",
    "8.9": "PetalburgCity_House5",
    "8.10": "PetalburgCity_House6",
    "8.11": "PetalburgCity_Shed",
    "1.5": "LittlerootTown_House",
    "2.5": "OldaleTown_House3",
    "2.6": "OldaleTown_House4",
    "2.7": "OldaleTown_CommunityCenter",
    "2.8": "OldaleTown_Unused",
    "2.9": "OldaleTown_Shed",
    "11.17": "RustboroCity_TeachersHouse",
    "11.18": "RustboroCity_Dorm_1F",
    "11.19": "RustboroCity_Dorm_2F",
    "11.20": "RustboroCity_Dorm_3F",
    "11.21": "RustboroCity_Flat3_1F",
    "11.22": "RustboroCity_Flat3_2F",
    "11.23": "RustboroCity_Flat3_3F",
    "11.24": "RustboroCity_House4",
    "11.25": "RustboroCity_House4_2F",
    "11.26": "RustboroCity_House5",
    "11.27": "RustboroCity_House6",
    "11.28": "RustboroCity_Cafe",
    "17.0": "FoothillTown_Mart",
    "17.1": "FoothillTown_PokemonCenter_1F",
    "17.2": "FoothillTown_PokemonCenter_2F",
    "17.3": "FoothillTown_House1",
    "17.4": "FoothillTown_House2",
    "17.5": "FoothillTown_House3",
    "17.6": "FoothillTown_House4",
    "17.7": "FoothillTown_House5",
    "17.8": "FoothillTown_House6",
    "17.9": "FoothillTown_FishingDojo",
    "18.0": "Route102_FishingHut",
    "18.1": "Route102_House",
    "19.3": "PetalburgWoods_RestStop",
    "22.3": "Route115_Hut",
    # onda 2, lote G1: os ginásios novos do EX
    "19.2": "PetalburgWoods_Gym",
    "9.14": "SlateportCity_Gym",
    "6.9": "VerdanturfTown_Gym",
}

DIR_EX = {1: "down", 2: "up", 3: "left", 4: "right", 5: "dive", 6: "emerge"}
OPOSTA = {"down": "up", "up": "down", "left": "right", "right": "left", "dive": "emerge", "emerge": "dive"}


# ------------------------------------------------------------------ carga do EX

_EX = None


def ex():
    """Carrega a ROM e a análise do EX uma vez só (o import do comum lê 32 MB)."""
    global _EX
    if _EX is None:
        sys.path.insert(0, ANALISE)
        import comum as C
        _EX = C
        C.M = {(g, i): m for g, i, m in C.mapas()}
        _alinha_grupos(C)
    return _EX


def _alinha_grupos(C):
    """EX (grupo, índice) -> nome vanilla, casando os grupos pelo CONTEÚDO.

    O EX inseriu mapas no MEIO do grupo 0 (Rustboro parte 2 no índice 4) e
    grupos inteiros no meio do `group_order` (17, 18 e 26), então o índice do EX
    não é o do vanilla. Medido: tirando os mapas de layout novo (> 441), cada
    grupo do EX é igual, layout a layout, a exatamente um grupo vanilla.
    """
    LID = {l["id"]: i + 1 for i, l in enumerate(C.VL) if l}
    vseq = {}
    for vg, gn in enumerate(C.mg["group_order"]):
        vseq[vg] = [(nm, LID[json.load(open("%s/data/maps/%s/map.json" % (C.PE, nm)))["layout"]])
                    for nm in C.mg[gn]]
    usados = set()
    C.EX_NOME = {}
    C.EX_GRUPO_VAN = {}
    for G in C.inv["grupos"]:
        exl = [(i, m["layout_id"]) for i, m in enumerate(G["mapas"]) if m and m["layout_id"] <= len(C.VL)]
        if not exl:
            continue
        cand = [vg for vg, s in vseq.items() if [x[1] for x in s] == [x[1] for x in exl] and vg not in usados]
        if not cand:
            raise SystemExit("ERRO: grupo %d do EX não casa com nenhum grupo vanilla" % G["g"])
        vg = cand[0]
        usados.add(vg)
        C.EX_GRUPO_VAN[G["g"]] = C.mg["group_order"][vg]
        for (i, _), (nm, _) in zip(exl, vseq[vg]):
            C.EX_NOME[(G["g"], i)] = nm


def fidel():
    return json.load(open(ONDA0 + "/fidel.json"))


def offsets():
    return json.load(open(ONDA0 + "/offsets.json"))


def chave(g, i):
    return "%d.%d" % (g, i)


def e_novo(g, i):
    C = ex()
    return (g, i) in C.M and C.M[(g, i)]["layout_id"] > len(C.VL)


def nome_padrao_novo(g, i):
    """Interior novo sem nome na tabela: cidade dona (MAPSEC) + índice do EX."""
    C = ex()
    sec = C.mapsec.get(C.M[(g, i)]["secao"], "HOENN")
    base = "".join(p.capitalize() for p in re.split(r"[^A-Za-z0-9]+", sec) if p)
    return "%s_Ex%d_%d" % (base, g, i)


def nome_nosso(g, i):
    """Nome do mapa no NOSSO repositório para o mapa (g, i) do EX."""
    C = ex()
    k = chave(g, i)
    if k in NOMES_NOVOS:
        return NOMES_NOVOS[k].replace(" ", "")
    if (g, i) in C.EX_NOME:
        return C.EX_NOME[(g, i)]
    if e_novo(g, i):
        return nome_padrao_novo(g, i)
    raise KeyError(k)


def id_mapa(nome):
    """O MESMO id que o `novo` grava no map.json (MAP_ + snake): antes, destino
    para mapa novo ainda não criado saía MAP_ANCIENT_TOMB_1_F e o mapa gravava
    MAP_ANCIENT_TOMB_1F, e o build quebrava (medido pelo lote C, 23/09/2026)."""
    return "MAP_" + snake(nome)


def id_mapa_repo(nome):
    """O id do mapa como o repo JÁ escreve (lê o map.json quando existe)."""
    p = os.path.join(RAIZ, "data/maps", nome, "map.json")
    if os.path.exists(p):
        return json.load(open(p))["id"]
    return id_mapa(nome)


# ------------------------------------------------------------------ texto do EX

def _charmap():
    enc, dec = {}, {}
    for ln in open(os.path.join(RAIZ, "charmap.txt"), encoding="utf-8"):
        m = re.match(r"^'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*(@.*)?$", ln.strip())
        if m:
            dec.setdefault(int(m.group(2), 16), m.group(1))
    return dec


_DEC = None
PLACEHOLDER = {0x01: "{PLAYER}", 0x02: "{STR_VAR_1}", 0x03: "{STR_VAR_2}", 0x04: "{STR_VAR_3}",
               0x05: "{KUN}", 0x06: "{RIVAL}", 0x07: "{VERSION}", 0x08: "{AQUA}", 0x09: "{MAGMA}",
               0x0A: "{ARCHIE}", 0x0B: "{MAXIE}", 0x0C: "{KYOGRE}", 0x0D: "{GROUDON}"}


SETAS = {0x79: "{UP_ARROW}", 0x7A: "{DOWN_ARROW}", 0x7B: "{LEFT_ARROW}", 0x7C: "{RIGHT_ARROW}"}


def texto_ex(off, limite=1200):
    """Decodifica um texto da ROM do EX para a sintaxe `.string` do nosso repo.

    Devolve (lista de linhas .string, True se entendeu tudo). Código de controle
    que não sei traduzir sem adivinhar (0xFC, cor, pausa) faz a função devolver
    falso: o texto vai para a pendência, não para o jogo.
    """
    global _DEC
    if _DEC is None:
        _DEC = _charmap()
    rom = ex().rom
    out, cur, ok, i = [], "", True, off
    while i < off + limite:
        b = rom[i]
        if b == 0xFF:
            cur += "$"
            out.append(cur)
            return out, ok
        if b == 0xFE:
            out.append(cur + "\\n"); cur = ""
        elif b == 0xFA:
            out.append(cur + "\\l"); cur = ""
        elif b == 0xFB:
            out.append(cur + "\\p"); cur = ""
        elif b == 0xFD:
            i += 1
            ph = PLACEHOLDER.get(rom[i])
            if ph is None:
                ok = False
                ph = "{?%02X}" % rom[i]
            cur += ph
        elif b == 0xFC:
            ok = False
            cur += "{?FC}"
            i += 1
        elif b == 0x00:
            cur += " "
        elif b in SETAS:
            cur += SETAS[b]
        else:
            c = _DEC.get(b)
            if c is None:
                ok = False
                c = "{?%02X}" % b
            if c == '"':
                c = '\\"'
            cur += c
        i += 1
    return out + [cur], False


def texto_plano(linhas):
    return "".join(l.replace("\\n", " ").replace("\\l", " ").replace("\\p", " ").rstrip("$") for l in linhas)


# ------------------------------------------------------------------ vanilla -> nomes

def _enum_vanilla(arq, prefixo):
    d = {}
    for ln in open(os.path.join(VAN, arq), encoding="utf-8"):
        m = re.match(r"#define\s+(%s[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)\b" % prefixo, ln)
        if m:
            d.setdefault(int(m.group(2), 0), m.group(1))
    return d


_ENUMS = {}


def enum(nome):
    if nome not in _ENUMS:
        arq, pre = {
            "gfx": ("include/constants/event_objects.h", "OBJ_EVENT_GFX_"),
            "mov": ("include/constants/event_object_movement.h", "MOVEMENT_TYPE_"),
            "classe": ("include/constants/trainers.h", "TRAINER_CLASS_"),
            "pic": ("include/constants/trainers.h", "TRAINER_PIC_"),
            "musica": ("include/constants/trainers.h", "TRAINER_ENCOUNTER_MUSIC_"),
            "flag": ("include/constants/flags.h", "FLAG_"),
            "var": ("include/constants/vars.h", "VAR_"),
        }[nome]
        _ENUMS[nome] = _enum_vanilla(arq, pre)
    return _ENUMS[nome]


TIPO_TREINADOR = {0: "TRAINER_TYPE_NONE", 1: "TRAINER_TYPE_NORMAL", 2: "TRAINER_TYPE_SEE_ALL_DIRECTIONS",
                  3: "TRAINER_TYPE_BURIED"}

_ITENS = None


def itens_ex():
    """Nome de cada item do EX, pela tabela gItemsInfo achada na ROM.

    Medido em 23/09/2026: registro de 60 B, nome em +0x14 ("Potion" em
    0x62A02C, "Super Potion" 60 B depois). A base é o ITEM_NONE ("????????").
    """
    global _ITENS
    if _ITENS is None:
        C = ex()
        rom = C.rom
        pot = rom.find(bytes([0xCA, 0xE3, 0xE8, 0xDD, 0xE3, 0xE2, 0xFF]))  # "Potion$"
        base = pot - 0x14
        q = bytes([0xAC] * 8)  # "????????"
        while base > 0 and rom[base + 0x14:base + 0x1C] != q:
            base -= 60
        _ITENS = {}
        k = 0
        while True:
            s = C.texto(base + 60 * k + 0x14, 20)
            if k > 5 and (not s or len(s) < 2):
                break
            _ITENS[k] = s
            k += 1
            if k > 900:
                break
    return _ITENS


_ITENS_NOSSOS = None


def item_nosso(nome_ex):
    """'Max Revive' -> 'ITEM_MAX_REVIVE' pelo .name do nosso src/data/items.h."""
    global _ITENS_NOSSOS
    if _ITENS_NOSSOS is None:
        _ITENS_NOSSOS = {}
        txt = open(os.path.join(RAIZ, "src/data/items.h"), encoding="utf-8").read()
        for m in re.finditer(r"\[(ITEM_[A-Z0-9_]+)\]\s*=\s*\{\s*\.name\s*=\s*(?:ITEM_NAME|_)\(\"([^\"]+)\"\)", txt):
            _ITENS_NOSSOS.setdefault(re.sub(r"[^a-z0-9]", "", m.group(2).lower()), m.group(1))
    return _ITENS_NOSSOS.get(re.sub(r"[^a-z0-9]", "", nome_ex.lower()))


# gSpeciesInfo do EX: registro de 160 B com o nome no começo, achado pelo nome
# (Bulbasaur, Ivysaur e Venusaur a 160 B um do outro; 812 = Rillaboom e 1370 =
# Annihilape conferidos), 23/09/2026.
EX_ESPECIE_NOME, EX_ESPECIE_PASSO = 11706556, 160


def especie_ex_nome(n):
    return ex().texto(EX_ESPECIE_NOME + EX_ESPECIE_PASSO * n, 12)


def especie_nossa(n):
    """Espécie do EX -> SPECIES_ nosso, pelo VALOR do enum e conferida pelo NOME.

    O EX é pokeemerald-expansion com o MESMO enum de espécie que o nosso
    (formas de 906 em diante inclusive: 906 = Venusaur mega, 1370 =
    Annihilape nos dois). A versão antiga desta função cortava em 1025 e
    chamava isso de numeração nacional: Annihilape e toda a geração 9 caíam na
    pendência. Agora o valor acha a constante e o nome do EX tem de bater com o
    começo dela (forma incluída); se não bater, devolve None (pendência)."""
    global _ESP
    try:
        _ESP
    except NameError:
        _ESP = {}
        txt = open(os.path.join(RAIZ, "include/constants/species.h"), encoding="utf-8").read()
        for m in re.finditer(r"\b(SPECIES_[A-Z0-9_]+)\s*=\s*(\d+)\s*,", txt):
            _ESP.setdefault(int(m.group(2)), m.group(1))
    c = _ESP.get(n)
    if not c:
        return None
    nome = re.sub(r"[^A-Z0-9]", "", especie_ex_nome(n).upper().replace("É", "E"))
    alvo = c[8:].replace("_", "")
    if not nome or alvo[:1] != nome[:1]:
        return None
    # o nome do EX tem 10 letras e vem abreviado (Flechinder, Bsculegion):
    # basta ele ser subsequência da constante, na ordem
    it = iter(alvo)
    return c if all(ch in it for ch in nome) else None


# ------------------------------------------------------------------ eventos do EX

def eventos_ex(g, i):
    """Os quatro tipos de evento do mapa (g, i) do EX, lidos da ROM."""
    C = ex()
    rom, r = C.rom, C.r
    m = C.M[(g, i)]
    e = m["ev"] or {"obj": 0, "warp": 0, "coord": 0, "bg": 0}
    objs, warps, coords, bgs = [], [], [], []
    if e["obj"]:
        p = r.deref(e["p_obj"])
        for k in range(e["obj"]):
            b = rom[p + 24 * k:p + 24 * k + 24]
            lid, gfx = b[0], b[1]
            x, y = struct.unpack_from("<hh", b, 4)
            elev, mov, rng = b[8], b[9], b[10]
            ttype, trng = struct.unpack_from("<HH", b, 12)
            scr, flag = struct.unpack_from("<IH", b, 16)
            objs.append(dict(k=k, local=lid, gfx=gfx, x=x, y=y, elev=elev, mov=mov, rx=rng & 15, ry=rng >> 4,
                             ttype=ttype, trng=trng, script=scr, flag=flag))
    for k, (x, y, gg, mn, wid) in enumerate(C.warps(m)):
        el = rom[r.deref(e["p_warp"]) + 8 * k + 4]
        warps.append(dict(k=k, x=x, y=y, elev=el, g=gg, i=mn, warp=wid))
    if e["coord"]:
        p = r.deref(e["p_coord"])
        for k in range(e["coord"]):
            x, y, el, _, var, val, _, scr = struct.unpack_from("<hhBBHHHI", rom, p + 16 * k)
            coords.append(dict(k=k, x=x, y=y, elev=el, var=var, val=val, script=scr))
    if e["bg"]:
        p = r.deref(e["p_bg"])
        for k in range(e["bg"]):
            x, y, el, kind, _, u = struct.unpack_from("<hhBBHI", rom, p + 12 * k)
            bgs.append(dict(k=k, x=x, y=y, elev=el, kind=kind, u=u))
    return objs, warps, coords, bgs


def _ptr(v):
    C = ex()
    return C.r.deref(v) if C.r.valido(v) else None


_SCRIPT_ITEM = None


def script_item_ex():
    """Endereço do Common_EventScript_FindItem do EX: o script mais comum das bolas de item."""
    global _SCRIPT_ITEM
    if _SCRIPT_ITEM is None:
        C = ex()
        cont = collections.Counter()
        for (g, i) in list(C.M)[:200]:
            for o in eventos_ex(g, i)[0]:
                if o["gfx"] == 59 and o["script"]:
                    cont[o["script"]] += 1
        _SCRIPT_ITEM = cont.most_common(1)[0][0]
    return _SCRIPT_ITEM


def classifica_script(ptr):
    """Lê o bytecode do EX e diz o que o script É, sem copiá-lo.

    Devolve dict com 'tipo' em: fala (msgbox NPC), placa (msgbox SIGN),
    treinador (trainerbattle simples + fala de depois), vazio, outro.
    Padrões medidos na ROM (23/09/2026):
      fala:  0F 00 <texto> 09 02 02        (loadword 0; callstd MSGBOX_NPC; end)
      placa: 0F 00 <texto> 09 03 02        (callstd MSGBOX_SIGN)
    """
    C = ex()
    rom = C.rom
    if not ptr:
        return {"tipo": "vazio"}
    if ptr == script_item_ex():
        return {"tipo": "item"}
    a = _ptr(ptr)
    if a is None:
        return {"tipo": "outro", "motivo": "ponteiro inválido"}
    b = rom[a:a + 64]
    # lock/faceplayer opcionais antes da fala
    j = 0
    while j < 4 and b[j] in (0x6A, 0x6C, 0x5A):
        j += 1
    if b[j] == 0x0F and b[j + 1] == 0x00 and b[j + 6] == 0x09 and cauda_cosmetica(b, j + 8):
        tp = {2: "fala", 3: "placa", 4: "fala", 5: "fala", 6: "fala"}.get(b[j + 7])
        if tp:
            t = struct.unpack_from("<I", b, j + 2)[0]
            linhas, ok = texto_ex(_ptr(t))
            return {"tipo": tp if ok else "outro", "texto": linhas, "std": b[j + 7],
                    "cauda": b[j + 8] != 0x02,
                    "motivo": None if ok else "código de texto que não traduzo"}
    if b[0] == 0x5C:
        return classifica_treinador(a)
    return {"tipo": "outro", "motivo": "bytecode " + b[:12].hex(" ")}


# comprimento dos comandos que podem vir DEPOIS da fala sem mudar o que o NPC
# diz: virar de volta (applymovement do próprio NPC), esperar, soltar, fechar.
_CAUDA = {0x4F: 7, 0x51: 3, 0x6C: 1, 0x6B: 1, 0x68: 1, 0x66: 1}


def cauda_cosmetica(b, j):
    """True se de `j` até o `end` só há comando cosmético (o NPC vira de volta).

    Esse resto NÃO é reproduzido: a fala entra como msgbox simples, e isso é
    declarado no relatório ('cauda' = True)."""
    while j < len(b):
        op = b[j]
        if op == 0x02:
            return True
        if op not in _CAUDA:
            return False
        j += _CAUDA[op]
    return False


def classifica_treinador(a):
    """trainerbattle do EX (pokeemerald-expansion). Aceita só o tipo SINGLE (0)
    seguido de fala de depois; o resto (duplo, revanche, cena) é pendência."""
    C = ex()
    rom = C.rom
    b = rom[a:a + 40]
    tipo = b[1]
    tid, local, intro, derrota = struct.unpack_from("<HHII", b, 2)
    # formato medido (Route 135 do EX, 23/09/2026):
    #   5C 00 <id u16> <local u16> <intro> <derrota> 0F 00 <depois> 09 06 02
    #   = trainerbattle_single id, intro, derrota; msgbox depois, MSGBOX_AUTOCLOSE; end
    base = {"id": tid, "tb_tipo": tipo, "bytes": b[:28].hex(" ")}
    if tipo == 4 and local == 0:
        # DUPLO (gêmeas, casais), medido na Route 137 do EX, 23/09/2026:
        #   5C 04 <id u16> <local u16> <intro> <derrota> <sem_dois> 0F 00 <depois> 09 06 02
        #   = trainerbattle_double id, intro, derrota, sem_dois; msgbox depois; end
        # Os dois objetos do par apontam para o MESMO id.
        if not (b[18] == 0x0F and b[19] == 0x00 and b[24] == 0x09 and b[26] == 0x02):
            return dict(base, tipo="outro", motivo="trainerbattle duplo sem a fala de depois no molde")
        sem_dois, depois = struct.unpack_from("<II", b, 14)[0], struct.unpack_from("<I", b, 20)[0]
        ti, ok1 = texto_ex(_ptr(intro))
        td, ok2 = texto_ex(_ptr(derrota))
        tn, ok3 = texto_ex(_ptr(sem_dois))
        tp, ok4 = texto_ex(_ptr(depois))
        if not (ok1 and ok2 and ok3 and ok4):
            return dict(base, tipo="outro", motivo="código de texto que não traduzo")
        return dict(base, tipo="treinador", duplo=True, intro=ti, derrota=td, sem_dois=tn, depois=tp)
    if tipo != 0 or local != 0:
        return dict(base, tipo="outro", motivo="trainerbattle tipo %d local %d" % (tipo, local))
    if not (b[14] == 0x0F and b[15] == 0x00 and b[20] == 0x09 and b[22] == 0x02):
        return dict(base, tipo="outro", motivo="trainerbattle sem a fala de depois no molde")
    depois = struct.unpack_from("<I", b, 16)[0]
    ti, ok1 = texto_ex(_ptr(intro))
    td, ok2 = texto_ex(_ptr(derrota))
    tp, ok3 = texto_ex(_ptr(depois))
    if not (ok1 and ok2 and ok3):
        return dict(base, tipo="outro", motivo="código de texto que não traduzo")
    return dict(base, tipo="treinador", intro=ti, derrota=td, depois=tp)


# ------------------------------------------------------------------ repo nosso

def carrega_mapa(nome):
    return json.load(open(os.path.join(RAIZ, "data/maps", nome, "map.json"), encoding="utf-8"))


def grava_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def layouts():
    return json.load(open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8"))


def layout_de(nome_layout):
    for l in layouts()["layouts"]:
        if l and l.get("id") == nome_layout:
            return l
    raise KeyError(nome_layout)


# ------------------------------------------------------------------ textos nossos

_IDX = None


def _indice_scripts():
    """Rótulo -> linhas do corpo, em todo .inc de mapa, script comum e texto.

    Serve para ler o TEXTO de um NPC nosso e comparar com o do EX: quando o
    EX mudou o NPC de lugar mas manteve a fala, é o mesmo evento.
    """
    global _IDX
    if _IDX is None:
        _IDX = {}
        pastas = [os.path.join(RAIZ, "data/maps"), os.path.join(RAIZ, "data/scripts"),
                  os.path.join(RAIZ, "data/text"), os.path.join(RAIZ, "data/event_scripts.s")]
        for base in pastas:
            itens = [(os.path.dirname(base), [], [os.path.basename(base)])] if os.path.isfile(base) else os.walk(base)
            for raiz, _, arqs in itens:
                for f in arqs:
                    if not f.endswith((".inc", ".s")):
                        continue
                    rot, corpo = None, []
                    for ln in open(os.path.join(raiz, f), encoding="utf-8", errors="replace"):
                        m = re.match(r"^([A-Za-z0-9_]+)::?\s*$", ln)
                        if m:
                            if rot:
                                _IDX.setdefault(rot, corpo)
                            rot, corpo = m.group(1), []
                        elif rot:
                            corpo.append(ln.rstrip("\n"))
                    if rot:
                        _IDX.setdefault(rot, corpo)
    return _IDX


def texto_nosso(rotulo):
    corpo = _indice_scripts().get(rotulo, [])
    return "".join(re.findall(r'\.string\s+"(.*)"', "\n".join(corpo)))


def falas_do_script(rotulo, prof=0):
    """Todos os textos que um script nosso mostra (msgbox, trainerbattle), 1 nível de goto/call."""
    out = []
    for ln in _indice_scripts().get(rotulo, []):
        if re.match(r"\s*(msgbox|message|trainerbattle\w*)\b", ln):
            for m in re.finditer(r"\b([A-Za-z0-9_]*Text[A-Za-z0-9_]*)\b", ln):
                out.append(texto_nosso(m.group(1)))
        m = re.match(r"\s*(goto|call)\s+([A-Za-z0-9_]+)\s*$", ln)
        if m and prof < 1:
            out += falas_do_script(m.group(2), prof + 1)
    return out


def norm(t):
    t = t.replace("\\n", " ").replace("\\l", " ").replace("\\p", " ").replace("$", "")
    return re.sub(r"[^a-z0-9]", "", t.lower().replace("é", "e"))


# ------------------------------------------------------------------ casamento

def tipo_obj_nosso(o):
    if o.get("graphics_id") == "OBJ_EVENT_GFX_ITEM_BALL":
        return "item"
    if o.get("trainer_type", "TRAINER_TYPE_NONE") not in ("TRAINER_TYPE_NONE", "0"):
        return "treinador"
    return "npc"


def tipo_obj_ex(o, c):
    if c["tipo"] == "item" or o["gfx"] == 59:
        return "item"
    if o["ttype"]:
        return "treinador"
    # treinador que se FALA (trainer_type 0 e script trainerbattle): entra como
    # treinador, com TRAINER_TYPE_NONE (medido pelo lote C: AMELIA, Route 125)
    if c.get("tipo") == "treinador":
        return "treinador"
    return "npc"


def flag_valor(nome):
    """FLAG_X -> número, pelos defines do NOSSO flags.h.

    Resolve literal, apelido (`FLAG_A FLAG_B`) e base mais deslocamento
    (`(FLAG_HIDDEN_ITEMS_START + 0x36)`, o formato de TODO item escondido:
    sem isso o item escondido nosso nunca casava com o do EX pela flag e o
    `eventos` o duplicava, medido na Route 110)."""
    global _FLAGS
    try:
        _FLAGS
    except NameError:
        cru = {}
        for ln in open(os.path.join(RAIZ, "include/constants/flags.h"), encoding="utf-8"):
            m = re.match(r"#define\s+([A-Z][A-Za-z0-9_]*)\s+([^/\n]+?)\s*(//.*)?$", ln)
            if m:
                cru.setdefault(m.group(1), m.group(2).strip())
        # O teto de treinador mora no opponents.h; é dele que as flags de sistema
        # em diante derivam (TRAINER_FLAGS_END, SYSTEM_FLAGS, ...).
        mt = re.search(r"#define\s+MAX_TRAINERS_COUNT_EMERALD\s+(\d+)",
                       open(os.path.join(RAIZ, "include/constants/opponents.h"), encoding="utf-8").read())
        cru["MAX_TRAINERS_COUNT"] = mt.group(1)
        _FLAGS = {}

        def resolve(n, prof=0):
            # expressão só de nomes, números, + e - e parênteses
            if n in _FLAGS:
                return _FLAGS[n]
            e = cru.get(n)
            if e is None or prof > 12 or not re.fullmatch(r"[A-Za-z0-9_+\-()% x]+", e):
                return None
            partes = []
            for tok in re.findall(r"0x[0-9A-Fa-f]+|\d+|[A-Z][A-Za-z0-9_]*|[+\-()%]", e):
                if re.fullmatch(r"[A-Z][A-Za-z0-9_]*", tok):
                    v = resolve(tok, prof + 1)
                    if v is None:
                        return None
                    partes.append(str(v))
                else:
                    partes.append(tok)
            try:
                v = int(eval("".join(partes), {"__builtins__": {}}))
            except Exception:
                return None
            _FLAGS[n] = v
            return v
        for n in list(cru):
            resolve(n)
    return _FLAGS.get(nome)


def nomes_treinador_vanilla():
    """id -> nome do treinador no Emerald vanilla (opponents.h + trainers.h)."""
    global _VN
    try:
        return _VN
    except NameError:
        pass
    ids = {}
    for ln in open(os.path.join(VAN, "include/constants/opponents.h"), encoding="utf-8"):
        m = re.match(r"#define\s+(TRAINER_\w+)\s+(\d+)", ln)
        if m:
            ids[m.group(1)] = int(m.group(2))
    _VN = {}
    txt = open(os.path.join(VAN, "src/data/trainers.h"), encoding="utf-8").read()
    for m in re.finditer(r"\[(TRAINER_\w+)\]\s*=\s*\{[^}]*?\.trainerName\s*=\s*_\(\"([^\"]*)\"\)", txt, re.S):
        if m.group(1) in ids:
            _VN[ids[m.group(1)]] = m.group(2).strip().upper()
    return _VN


def treinadores_do_script(rotulo, prof=0):
    """TRAINER_* que o script nosso usa em trainerbattle, 1 nível de goto/call."""
    out = []
    for ln in _indice_scripts().get(rotulo, []):
        m = re.match(r"\s*trainerbattle\w*\s+(TRAINER_\w+)", ln)
        if m:
            out.append(m.group(1))
        m = re.match(r"\s*(goto|call)\s+([A-Za-z0-9_]+)\s*$", ln)
        if m and prof < 1:
            out += treinadores_do_script(m.group(2), prof + 1)
    return out


def valor_treinador(cst):
    global _TV
    try:
        _TV
    except NameError:
        _TV = {}
        for arq in ("include/constants/opponents.h", "include/constants/opponents_frlg.h"):
            for ln in open(os.path.join(RAIZ, arq), encoding="utf-8"):
                m = re.match(r"#define\s+(TRAINER_\w+)\s+(\d+)", ln)
                if m:
                    _TV.setdefault(m.group(1), int(m.group(2)))
    return _TV.get(cst)


def n_vanilla(nome):
    """Quantos object_events o mapa tem no Emerald vanilla (0 se não existe lá)."""
    p = os.path.join(VAN, "data/maps", nome, "map.json")
    if not os.path.exists(p):
        return 0
    return len(json.load(open(p, encoding="utf-8")).get("object_events") or [])


def casa_eventos(g, i, j, dx, dy, raio=1):
    """Casa cada evento do EX com um evento NOSSO (índices do nosso map.json).

    Ordem das provas, da mais forte para a mais fraca:
      1. mesma flag (não zero): é o mesmo objeto de enredo ou a mesma bola de item;
      2. mesmo texto (fala, placa, treinador): o EX pode ter mudado o NPC de lugar;
      3. mesma posição (nossa + deslocamento) a até `raio` célula e mesmo tipo
         (warp com warp, placa com placa, NPC com NPC de mesmo sprite).
      Warp: mesmo DESTINO (mapa) é prova; entre vários, o mais perto.
    Devolve dict tipo -> {índice EX: (índice nosso, prova)}.
    """
    objs, warps, coords, bgs = eventos_ex(g, i)
    gfx = enum("gfx")
    res = {"obj": {}, "warp": {}, "coord": {}, "bg": {}}
    nossos = j.get("object_events") or []
    usados = set()

    def dist(a, b):
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    info_ex = []
    for o in objs:
        c = classifica_script(o["script"])
        falas = []
        if c["tipo"] in ("fala", "placa"):
            falas = [norm("".join(c["texto"]))]
        elif c["tipo"] == "treinador":
            falas = [norm("".join(c["intro"]))]
        info_ex.append((o, c, tipo_obj_ex(o, c), falas))
    info_nosso = []
    for k, n in enumerate(nossos):
        f = flag_valor(n.get("flag", "0")) or 0
        falas = [norm(t) for t in falas_do_script(n.get("script", ""))]
        info_nosso.append((k, n, tipo_obj_nosso(n), f, falas))
    # Prova mais forte de todas (lote B, 23/09/2026): o EX conserva a ORDEM dos
    # objetos vanilla do mapa e só acrescenta os dele no fim. Objeto do EX de
    # índice k, dentro da contagem VANILLA do mapa, com o MESMO sprite do nosso
    # índice k, é o mesmo objeto, mudado de lugar pelo autor (Route 109: 24 de
    # 24, com Ricky, Lola, o velho e o Zigzagoon em outra praia; Slateport: o
    # gordo, a moça do museu e o maníaco). Nenhum texto casava, porque o
    # script vanilla tem condição e o classificador só lê fala simples.
    nvan = n_vanilla(nome_nosso(g, i))
    gfx_ = enum("gfx")
    # Exceção medida pelo lote C (Route 134, 23/09/2026): o EX tirou um objeto
    # do meio e a ordem andou uma casa; as bolas de item casavam pelo índice com a
    # bola VIZINHA (Carbos com Star Piece, Star Piece com a TM35 nova). Flag é
    # prova mais forte que índice: com as duas flags acesas e DIFERENTES, o
    # índice não vale.
    flag_nosso = {k: f for k, n, tpn, f, fn in info_nosso}
    # Treinador vanilla que o EX só mudou de lugar (lote B, Route 114): o EX
    # troca sprite e às vezes a classe, então índice e texto não casam, e o
    # eventos criava um TRAINER_HOENNEX_* para o MESMO treinador (o NOLAN, id
    # 342). Casa quando o id do trainerbattle do EX é o de um treinador nosso do
    # mapa E o nome do EX é o nome VANILLA daquele id. Só o id não basta: o EX
    # reusa os ids dos tiers de revanche vanilla (_2 a _5) para treinadores
    # NOVOS com outro nome (GARTH no 139, que é o WINSTON_2 vanilla).
    vn = nomes_treinador_vanilla()
    tid_nosso = {}
    for k, n in enumerate(nossos):
        for cst in treinadores_do_script(n.get("script", "")):
            v = valor_treinador(cst)
            if v is not None:
                tid_nosso.setdefault(v, k)
    for o, c, tp, falas in info_ex:
        tid = c.get("id")
        if tid is None or tid not in vn or tid not in tid_nosso or o["k"] in res["obj"]:
            continue
        k = tid_nosso[tid]
        if k in usados:
            continue
        if party_ex(tid)["nome"].strip().upper() == vn[tid]:
            res["obj"][o["k"]] = (k, "treinador")
            usados.add(k)
    for o, c, tp, falas in info_ex:
        k = o["k"]
        if o["k"] in res["obj"]:
            continue
        if k < nvan and k < len(nossos) and k not in usados and nossos[k].get("graphics_id") == gfx_.get(o["gfx"]) \
                and not (o["flag"] and flag_nosso.get(k) and o["flag"] != flag_nosso[k]):
            res["obj"][k] = (k, "indice")
            usados.add(k)
    for prova in ("flag", "texto", "posicao"):
        for o, c, tp, falas in info_ex:
            if o["k"] in res["obj"]:
                continue
            cand = []
            for k, n, tpn, f, fn in info_nosso:
                if k in usados:
                    continue
                if prova == "flag" and o["flag"] and o["flag"] == f and tp == tpn:
                    cand.append((dist((n["x"] + dx, n["y"] + dy), (o["x"], o["y"])), k))
                elif prova == "texto" and falas and falas[0] and any(falas[0] == x for x in fn if x):
                    cand.append((dist((n["x"] + dx, n["y"] + dy), (o["x"], o["y"])), k))
                elif prova == "posicao" and tp == tpn and dist((n["x"] + dx, n["y"] + dy), (o["x"], o["y"])) <= raio:
                    if tp != "npc" or n.get("graphics_id") == gfx.get(o["gfx"]):
                        cand.append((dist((n["x"] + dx, n["y"] + dy), (o["x"], o["y"])), k))
            if cand:
                cand.sort()
                res["obj"][o["k"]] = (cand[0][1], prova)
                usados.add(cand[0][1])
    # warps: destino igual
    nw = j.get("warp_events") or []
    usados = set()
    # Destino = mapa E warp_id. Só o mapa não basta: com duas portas para o
    # mesmo interior (o museu de Slateport, warps 0 e 1), a distância cruzava
    # as duas. Primeiro os pares de mapa e id iguais; depois, sobrando, os de
    # mapa só, pela menor distância, e esses são impressos para revisão.
    for passo in ("destino", "destino_so_mapa"):
        for w in warps:
            if w["k"] in res["warp"]:
                continue
            dest = id_mapa_repo(nome_nosso(w["g"], w["i"]))
            cand = [(dist((n["x"] + dx, n["y"] + dy), (w["x"], w["y"])), k) for k, n in enumerate(nw)
                    if n["dest_map"] == dest and k not in usados
                    and (passo == "destino_so_mapa" or str(n.get("dest_warp_id")) == str(w["warp"]))]
            if cand:
                cand.sort()
                res["warp"][w["k"]] = (cand[0][1], passo)
                usados.add(cand[0][1])
                if passo == "destino_so_mapa":
                    print("  REVISAR: warp EX %d (%d,%d) -> %s warp %d casou com o nosso warp %d só pelo mapa "
                          "(o nosso vai para o warp %s); menor distância decidiu"
                          % (w["k"], w["x"], w["y"], dest, w["warp"], cand[0][1], nw[cand[0][1]].get("dest_warp_id")))
    # bg: placa por texto ou posição; item escondido pela flag
    nb = j.get("bg_events") or []
    usados = set()
    for b in bgs:
        cand = []
        for k, n in enumerate(nb):
            if k in usados:
                continue
            if b["kind"] == 7 and n.get("type") == "hidden_item":
                hid = (b["u"] >> 16) & 0xFFFF
                f = flag_valor(n.get("flag"))
                if f is not None and f - 0x1F4 == hid:
                    cand.append((0, k, "flag"))
                elif dist((n["x"] + dx, n["y"] + dy), (b["x"], b["y"])) <= raio:
                    cand.append((1, k, "posicao"))
            elif b["kind"] != 7 and n.get("type") == "sign":
                c = classifica_script(b["u"])
                t = norm("".join(c.get("texto", [])))
                fn = [norm(x) for x in falas_do_script(n.get("script", ""))]
                if t and t in fn:
                    cand.append((0, k, "texto"))
                elif dist((n["x"] + dx, n["y"] + dy), (b["x"], b["y"])) <= raio:
                    cand.append((1, k, "posicao"))
            elif b["kind"] == 8 and n.get("type") == "secret_base":
                if dist((n["x"] + dx, n["y"] + dy), (b["x"], b["y"])) <= raio:
                    cand.append((0, k, "posicao"))
        if cand:
            cand.sort()
            res["bg"][b["k"]] = (cand[0][1], cand[0][2])
            usados.add(cand[0][1])
    # coord: mesma var e valor (a posição exata vem do EX)
    nc = j.get("coord_events") or []
    usados = set()
    var = enum("var")
    # Gatilhos que dividem var e valor formam um GRUPO (os três do rival da
    # Route 110, os quatro do Birch, os quatro do ginásio de Petalburg). Grupo
    # nosso e grupo do EX do mesmo tamanho casam NA ORDEM (linha, coluna): o EX
    # moveu a cena inteira, e a ordem é o que o script usa (VAR_0x8008 = índice
    # do gatilho). Casar o mais perto um a um invertia a ordem. Grupo de tamanho
    # diferente cai no mais perto, um a um.
    grupos_ex, grupos_nos = collections.defaultdict(list), collections.defaultdict(list)
    for c in coords:
        grupos_ex[(var.get(c["var"]), str(c["val"]))].append(c)
    for k, n in enumerate(nc):
        grupos_nos[(n.get("var"), str(n.get("var_value")))].append(k)
    for chave_, lex in grupos_ex.items():
        lnos = grupos_nos.get(chave_, [])
        if chave_[0] and len(lex) == len(lnos) and len(lex) > 1:
            for c, k in zip(sorted(lex, key=lambda c: (c["y"], c["x"])),
                            sorted(lnos, key=lambda k: (nc[k]["y"], nc[k]["x"]))):
                res["coord"][c["k"]] = (k, "var_grupo")
                usados.add(k)
    for c in coords:
        if c["k"] in res["coord"]:
            continue
        cand = [(dist((n["x"] + dx, n["y"] + dy), (c["x"], c["y"])), k) for k, n in enumerate(nc)
                if k not in usados and n.get("var") == var.get(c["var"]) and str(n.get("var_value")) == str(c["val"])]
        if cand:
            cand.sort()
            res["coord"][c["k"]] = (cand[0][1], "var" if cand[0][0] > raio else "posicao")
            usados.add(cand[0][1])
    return res


# ------------------------------------------------------------------ planta

def planta_ex(g, i):
    C = ex()
    L = C.M[(g, i)]["layout"]
    w, h = L["w"], L["h"]
    blob = C.rom[L["blockdata"]:L["blockdata"] + 2 * w * h]
    borda = C.rom[L["border"]:L["border"] + 8]
    return w, h, blob, borda


def celula(blob, w, x, y):
    return struct.unpack_from("<H", blob, 2 * (y * w + x))[0]


def cabe(w, h):
    return (w + 15) * (h + 14) <= 10240


def refs_coordenada(nome, j):
    """Linhas de script com coordenada absoluta deste mapa (quem precisa andar junto)."""
    mid = j["id"]
    locais = {o.get("local_id") for o in (j.get("object_events") or []) if o.get("local_id")}
    achados = []
    for raiz, _, arqs in os.walk(os.path.join(RAIZ, "data")):
        for f in arqs:
            if not f.endswith((".inc", ".s", ".json", ".pory")):
                continue
            p = os.path.join(raiz, f)
            try:
                txt = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if mid not in txt and not any(l in txt for l in locais):
                continue
            for n, ln in enumerate(txt.splitlines(), 1):
                if re.search(r"\b(warp\w*|setwarp|setdynamicwarp|setescapewarp|setrespawn)\s+%s\s*,\s*[^,]+,\s*\d+\s*,\s*\d+" % mid, ln) \
                        or re.search(r"\b(warp\w*|setwarp|setdynamicwarp|setescapewarp)\s+%s\s*,\s*-?\d+\s*,\s*-?\d+" % mid, ln) \
                        or (re.search(r"\bsetobjectxy(perm)?\s+(%s)\b" % "|".join(map(re.escape, locais)), ln) if locais else False) \
                        or (f == "scripts.inc" and nome in raiz and re.search(r"\b(setobjectxy(perm)?|getplayerxy|goto_if_\w+\s+VAR_TEMP_[0-9A-F],\s*\d+)", ln)):
                    achados.append("%s:%d: %s" % (os.path.relpath(p, RAIZ), n, ln.strip()))
    for p in ("src/data/heal_locations.json", "src/data/heal_locations.h"):
        pp = os.path.join(RAIZ, p)
        if os.path.exists(pp):
            for n, ln in enumerate(open(pp, encoding="utf-8"), 1):
                if mid in ln or ("HEAL_LOCATION_" + mid[4:]) in ln:
                    achados.append("%s:%d: %s" % (p, n, ln.strip()))
    return achados


def _mt(blob, w, h, x, y):
    if 0 <= x < w and 0 <= y < h:
        return struct.unpack_from("<H", blob, 2 * (y * w + x))[0] & 0x3FF
    return None


def alinha_local(j, velho, vw, vh, blob, w, h, dx, dy, R=4, faixa=40):
    """Deslocamento LOCAL de cada evento nosso na planta do EX (lote B, 23/09/2026).

    O deslocamento de `offsets.json` é UM por mapa, e o EX às vezes insere
    colunas ou linhas no MEIO do mapa (medido na Route 110: dez colunas entre
    y 39 e 70). Evento depois da inserção, andando só o global, cai em chão
    errado; o conferidor só pega quando a célula é bloqueada. Aqui cada evento
    compara a janela (2R+1)^2 de metatiles em volta dele na NOSSA planta antiga
    com a planta do EX em todo deslocamento de global +-`faixa`, e fica com o de
    maior casamento; em empate, com o mais perto do global (o global vence se
    empatar com ele).

    Gatilho de cena (coord_event) anda JUNTO com o objeto que o script dele
    move (applymovement/addobject LOCALID_*, seguindo goto/call), para a cena
    continuar coreografada; sem objeto, anda pelo próprio alinhamento. Como
    cada gatilho só anda (nunca troca de posição com outro), a ordem dos
    índices fica preservada.

    Devolve {(tipo, k): (ldx, ldy, casa_local, casa_global, n)}.
    """
    res = {}
    for tipo in ("object_events", "warp_events", "coord_events", "bg_events"):
        for k, e in enumerate(j.get(tipo) or []):
            x, y = e["x"], e["y"]
            jan = [(u, v, _mt(velho, vw, vh, x + u, y + v)) for u in range(-R, R + 1) for v in range(-R, R + 1)]
            jan = [(u, v, m) for u, v, m in jan if m is not None]

            def casa(ddx, ddy):
                return sum(1 for u, v, m in jan if _mt(blob, w, h, x + ddx + u, y + ddy + v) == m)
            sg = casa(dx, dy)
            melhor = (sg, 0, dx, dy)
            for ddx in range(dx - faixa, dx + faixa + 1):
                for ddy in range(dy - faixa, dy + faixa + 1):
                    c = (casa(ddx, ddy), -(abs(ddx - dx) + abs(ddy - dy)), ddx, ddy)
                    if c[:2] > melhor[:2]:
                        melhor = c
            # Margem: o local só vence com folga clara (medido na Route 110: os
            # Aqua da fileira de baixo davam 71 contra 65 num deslocamento (0,-3)
            # falso, porque o EX abriu um caminho ABAIXO deles e a janela perdeu
            # casamento no global; a vizinhança deles é idêntica).
            if melhor[0] < sg + max(6, len(jan) // 8):
                melhor = (sg, 0, dx, dy)
            res[(tipo, k)] = (melhor[2], melhor[3], melhor[0], sg, len(jan))
    objs = j.get("object_events") or []
    por_local = {o.get("local_id"): k for k, o in enumerate(objs) if o.get("local_id")}
    for k, c in enumerate(j.get("coord_events") or []):
        for lid in localids_do_script(c.get("script") or ""):
            if lid in por_local:
                ko = por_local[lid]
                ldx, ldy = res[("object_events", ko)][:2]
                _, _, cl, cg, n = res[("coord_events", k)]
                res[("coord_events", k)] = (ldx, ldy, cl, cg, n)
                break
    return res


def localids_do_script(rotulo, prof=0, vistos=None):
    """LOCALID_* que o script move ou mostra (applymovement, addobject, ...), seguindo goto/call."""
    vistos = vistos if vistos is not None else set()
    if rotulo in vistos or prof > 3:
        return []
    vistos.add(rotulo)
    out = []
    for ln in _indice_scripts().get(rotulo, []):
        m = re.match(r"\s*(applymovement|addobject|removeobject|showobjectat|turnobject|setobjectxy)\s+(LOCALID_[A-Z0-9_]+)", ln)
        if m and m.group(2) not in out:
            out.append(m.group(2))
        m = re.match(r"\s*(goto|call)(?:_if_\w+\s+[^,]+,\s*[^,]+,)?\s+([A-Za-z0-9_]+)\s*$", ln)
        if m:
            for x in localids_do_script(m.group(2), prof + 1, vistos):
                if x not in out:
                    out.append(x)
    return out


def cmd_aumenta(a):
    C = ex()
    g, i = map(int, a.ex.split("."))
    if e_novo(g, i):
        raise SystemExit("ERRO: %s é mapa NOVO; use `novo`." % a.ex)
    nome = nome_nosso(g, i)
    pj = os.path.join(RAIZ, "data/maps", nome, "map.json")
    j = json.load(open(pj, encoding="utf-8"))
    lj = layouts()
    lay = next(l for l in lj["layouts"] if l and l.get("id") == j["layout"])
    w, h, blob, borda = planta_ex(g, i)
    O = offsets().get(nome, {"dx": 0, "dy": 0, "igual": 1.0})
    dx = a.dx if a.dx is not None else O["dx"]
    dy = a.dy if a.dy is not None else O["dy"]
    trans = O["igual"] >= 0.75 or a.translacao
    F = fidel()[a.ex]
    print("AUMENTA %s (EX %s): %dx%d -> %dx%d, planta antiga %.0f%% preservada, deslocamento (%d,%d): %s"
          % (nome, a.ex, lay["width"], lay["height"], w, h, 100 * O["igual"], dx, dy,
             "TRANSLAÇÃO" if trans else "REMAPEAMENTO"))
    if (lay["primary_tileset"], lay["secondary_tileset"]) != (F["ts1"], F["ts2"]):
        print("  CONFLITO: par de tilesets nosso %s/%s, do EX %s/%s. A planta do EX aponta para o secundário DELE."
              % (lay["primary_tileset"], lay["secondary_tileset"], F["ts1"], F["ts2"]))
    if not cabe(w, h):
        raise SystemExit("ERRO: %dx%d passa de MAX_MAP_DATA_SIZE." % (w, h))
    novo = json.loads(json.dumps(j))
    conflitos = []
    if trans:
        # Alinhamento LOCAL (ver `alinha_local`): cada evento anda o deslocamento
        # da vizinhança dele, que é o global quando o EX não inseriu nada ali.
        velho = open(os.path.join(RAIZ, lay["blockdata_filepath"]), "rb").read()
        loc = alinha_local(j, velho, lay["width"], lay["height"], blob, w, h, dx, dy)
        for tipo in ("object_events", "warp_events", "coord_events", "bg_events"):
            for k, e in enumerate(novo.get(tipo) or []):
                ldx, ldy, cl, cg, n = loc[(tipo, k)]
                if (ldx, ldy) != (dx, dy):
                    print("  %s %d (%s) anda o deslocamento LOCAL (%d,%d) e não o global (%d,%d): "
                          "janela %d/%d contra %d/%d, (%d,%d) -> (%d,%d)"
                          % (tipo, k, e.get("script") or e.get("dest_map") or e.get("item"), ldx, ldy, dx, dy,
                             cl, n, cg, n, e["x"], e["y"], e["x"] + ldx, e["y"] + ldy))
                e["x"] += ldx
                e["y"] += ldy
        # Mesmo com a planta preservada, o EX troca prédio de função (Petalburg:
        # o Pokécenter foi para o leste e o prédio velho virou casa). Warp segue o
        # DESTINO, placa o TEXTO, item escondido a FLAG e gatilho a VAR: esses vão
        # para a célula do EX. NPC nosso fica na posição transladada.
        cas = casa_eventos(g, i, j, dx, dy)
        objs_, warps_, coords_, bgs_ = eventos_ex(g, i)
        delta_obj = {}
        for kex, (k, prova) in cas["obj"].items():
            if prova not in ("indice", "treinador"):
                continue
            e, d = novo["object_events"][k], objs_[kex]
            if not (0 <= d["x"] < w and 0 <= d["y"] < h):
                # defeito do próprio EX (Route 133: a bola de Max Revive em (45,56)
                # num mapa de 41 linhas): o objeto fica na posição transladada
                print("  object_events %d (%s) FICA em (%d,%d): a célula do EX (%d,%d) está fora do mapa do EX"
                      % (k, e.get("script"), e["x"], e["y"], d["x"], d["y"]))
                continue
            if (e["x"], e["y"]) != (d["x"], d["y"]):
                print("  object_events %d (%s) vai para a célula do EX (%d,%d) -> (%d,%d), prova: %s"
                      % (k, e.get("script"), e["x"], e["y"], d["x"], d["y"],
                         "índice e sprite" if prova == "indice" else "mesmo treinador (id e nome vanilla)"))
            delta_obj[k] = (d["x"] - j["object_events"][k]["x"], d["y"] - j["object_events"][k]["y"])
            e["x"], e["y"] = d["x"], d["y"]
        por_local = {o.get("local_id"): k for k, o in enumerate(j.get("object_events") or []) if o.get("local_id")}
        coord_do_ex = {k: kex for kex, (k, prova) in cas["coord"].items()}
        for k, c in enumerate(novo.get("coord_events") or []):
            if k in coord_do_ex:
                d = coords_[coord_do_ex[k]]
                if (c["x"], c["y"]) != (d["x"], d["y"]):
                    print("  coord_events %d (%s) vai para a célula do EX (%d,%d) -> (%d,%d), prova: %s"
                          % (k, c.get("script"), c["x"], c["y"], d["x"], d["y"], cas["coord"][coord_do_ex[k]][1]))
                c["x"], c["y"] = d["x"], d["y"]
                continue
            for lid in localids_do_script(c.get("script") or ""):
                if por_local.get(lid) in delta_obj:
                    ddx, ddy = delta_obj[por_local[lid]]
                    c0 = j["coord_events"][k]
                    if (c["x"], c["y"]) != (c0["x"] + ddx, c0["y"] + ddy):
                        print("  coord_events %d (%s) anda junto com %s: (%d,%d) -> (%d,%d)"
                              % (k, c.get("script"), lid, c["x"], c["y"], c0["x"] + ddx, c0["y"] + ddy))
                    c["x"], c["y"] = c0["x"] + ddx, c0["y"] + ddy
                    break
        # Gatilho (coord) NÃO vai para a célula do EX: casar por var embaralha a
        # ordem quando vários gatilhos dividem a var (Route 110: RivalTrigger 1
        # a 3 iam para 45, 44 e 43). Ele fica no alinhamento local, junto do
        # objeto da cena.
        for t, lst, dele in (("warp", "warp_events", warps_), ("bg", "bg_events", bgs_)):
            for kex, (k, prova) in cas[t].items():
                e = novo[lst][k]
                d = dele[kex]
                if (e["x"], e["y"]) != (d["x"], d["y"]):
                    print("  %s %d (%s) vai para a célula do EX (%d,%d) -> (%d,%d), prova: %s"
                          % (lst, k, e.get("script") or e.get("dest_map") or e.get("item"), e["x"], e["y"], d["x"], d["y"], prova))
                    e["x"], e["y"] = d["x"], d["y"]
    else:
        pplano = os.path.join(RAIZ, "dev_scripts/hoennex_planos", nome + ".json")
        if not os.path.exists(pplano):
            plano = propoe_plano(g, i, j, dx, dy, w, h, blob)
            os.makedirs(os.path.dirname(pplano), exist_ok=True)
            grava_json(pplano, plano)
            print("  plano de REMAPEAMENTO escrito em %s: revise cada linha e rode de novo." % os.path.relpath(pplano, RAIZ))
            for tipo, lst in plano.items():
                if tipo.startswith("_"):
                    continue
                for k, v in lst.items():
                    print("    %s %s %s" % (tipo, k, v))
            return
        plano = json.load(open(pplano, encoding="utf-8"))
        chave_tipo = {"obj": "object_events", "warp": "warp_events", "coord": "coord_events", "bg": "bg_events"}
        for tipo, lst in plano.items():
            if tipo.startswith("_"):
                continue
            for k, v in lst.items():
                e = novo[chave_tipo[tipo]][int(k)]
                e["x"], e["y"] = v["para"]
    # conferência de cada evento nosso na planta nova
    for tipo in ("object_events", "warp_events", "coord_events", "bg_events"):
        for k, e in enumerate(novo.get(tipo) or []):
            if not (0 <= e["x"] < w and 0 <= e["y"] < h):
                conflitos.append("%s %d (%s) FORA do mapa em (%d,%d)" % (tipo, k, e.get("script") or e.get("dest_map"), e["x"], e["y"]))
                continue
            v = celula(blob, w, e["x"], e["y"])
            if tipo == "object_events" and (v >> 10) & 3 and e.get("graphics_id") not in (
                    "OBJ_EVENT_GFX_CUTTABLE_TREE", "OBJ_EVENT_GFX_BREAKABLE_ROCK", "OBJ_EVENT_GFX_BERRY_TREE"):
                conflitos.append("object_events %d (%s, %s) em célula BLOQUEADA (%d,%d) metatile %d"
                                 % (k, e.get("graphics_id"), e.get("script"), e["x"], e["y"], v & 0x3FF))
    refs = refs_coordenada(nome, j) if (dx or dy or not trans) else []
    for r_ in refs:
        conflitos.append("coordenada absoluta em script (andar %+d,%+d ou remapear): %s" % (dx, dy, r_))
    for c in conflitos:
        print("  CONFLITO: " + c)
    if not a.aplica:
        print("  (demo: nada escrito; --aplica para gravar)")
        return
    pasta = os.path.join(RAIZ, os.path.dirname(lay["blockdata_filepath"]))
    open(os.path.join(RAIZ, lay["blockdata_filepath"]), "wb").write(blob)
    open(os.path.join(RAIZ, lay["border_filepath"]), "wb").write(borda)
    lay["width"], lay["height"] = w, h
    grava_json(os.path.join(RAIZ, "data/layouts/layouts.json"), lj)
    grava_json(pj, novo)
    print("  gravado: %s (map.bin %d B, border.bin), layouts.json %dx%d, eventos nossos %s"
          % (pasta, len(blob), w, h, "transladados" if trans else "remapeados pelo plano"))


def propoe_plano(g, i, j, dx, dy, w, h, blob):
    """Proposta de remapeamento, evento por evento, com a prova ao lado.

    Nada aqui é aplicado sem revisão: o arquivo é escrito e o executor decide.
    Evento casado com o EX (flag, texto, destino de warp, var de gatilho) vai
    para a posição do EX. O resto fica na posição antiga + deslocamento, marcado
    `SEM_PROVA`, e o executor escolhe o lugar (método §2: perto do mesmo prédio,
    em chão andável).
    """
    objs, warps, coords, bgs = eventos_ex(g, i)
    cas = casa_eventos(g, i, j, dx, dy)
    plano = {"_nota": "para = posição nova; prova = por que. SEM_PROVA pede decisão humana.",
             "obj": {}, "warp": {}, "coord": {}, "bg": {}}
    inv = {t: {v[0]: (k, v[1]) for k, v in cas[t].items()} for t in cas}
    lista = {"obj": (j.get("object_events") or [], objs), "warp": (j.get("warp_events") or [], warps),
             "coord": (j.get("coord_events") or [], coords), "bg": (j.get("bg_events") or [], bgs)}
    for t, (nossos, dele) in lista.items():
        for k, e in enumerate(nossos):
            if k in inv[t]:
                kex, prova = inv[t][k]
                d = dele[kex]
                plano[t][str(k)] = {"de": [e["x"], e["y"]], "para": [d["x"], d["y"]], "prova": "%s (EX %d)" % (prova, kex),
                                    "quem": e.get("script") or e.get("dest_map") or e.get("item")}
            else:
                nx, ny = e["x"] + dx, e["y"] + dy
                ok = 0 <= nx < w and 0 <= ny < h and not ((celula(blob, w, nx, ny) >> 10) & 3)
                plano[t][str(k)] = {"de": [e["x"], e["y"]], "para": [nx, ny],
                                    "prova": "SEM_PROVA (deslocamento%s)" % ("" if ok else ", célula BLOQUEADA ou fora"),
                                    "quem": e.get("script") or e.get("dest_map") or e.get("item")}
    return plano


# ------------------------------------------------------------------ conexões

def conexoes_ex(g, i):
    C = ex()
    out = []
    for d, off, gg, mn in C.conexoes(C.M[(g, i)]):
        dd = {"S": "down", "N": "up", "O": "left", "L": "right", "mergulho": "dive", "emergir": "emerge"}[d]
        out.append({"map": id_mapa_repo(nome_nosso(gg, mn)), "offset": off, "direction": dd, "_ex": (gg, mn)})
    return out


def cmd_conexoes(a):
    """Conexões do EX nos DOIS lados. O offset é o do próprio EX, dos dois lados
    (o EX grava as duas pontas; nada é recalculado à mão)."""
    g, i = map(int, a.ex.split("."))
    nome = nome_nosso(g, i)
    pj = os.path.join(RAIZ, "data/maps", nome, "map.json")
    if not os.path.exists(pj):
        raise SystemExit("ERRO: %s ainda não existe no repo." % nome)
    j = json.load(open(pj, encoding="utf-8"))
    mid = j["id"]
    novas = conexoes_ex(g, i)
    antigas = j.get("connections") or []
    print("CONEXÕES %s (EX %s)" % (nome, a.ex))
    for c in antigas:
        if not any(n["map"] == c["map"] and n["direction"] == c["direction"] for n in novas):
            print("  sai    %s %s offset %d" % (c["direction"], c["map"], c["offset"]))
    for n in novas:
        velha = next((c for c in antigas if c["map"] == n["map"] and c["direction"] == n["direction"]), None)
        print("  %s %s %s offset %d%s" % ("fica  " if velha and velha["offset"] == n["offset"] else ("muda  " if velha else "entra "),
                                          n["direction"], n["map"], n["offset"],
                                          (" (era %d)" % velha["offset"]) if velha and velha["offset"] != n["offset"] else ""))
    escrever = {pj: dict(j, connections=[{k: v for k, v in n.items() if k != "_ex"} for n in novas] or None)}
    # o outro lado: o que o EX grava no vizinho apontando para cá
    vizinhos = {n["map"]: n for n in novas}
    for c in antigas:
        vizinhos.setdefault(c["map"], None)
    for vmid, n in vizinhos.items():
        vnome = next((d for d in os.listdir(os.path.join(RAIZ, "data/maps"))
                      if os.path.exists(os.path.join(RAIZ, "data/maps", d, "map.json"))
                      and d == nome_de_id(vmid)), None)
        if not vnome:
            print("  outro lado: %s ainda não existe neste branch (a conexão de lá entra quando ele entrar)" % vmid)
            continue
        pv = os.path.join(RAIZ, "data/maps", vnome, "map.json")
        jv = json.load(open(pv, encoding="utf-8"))
        cv = [c for c in (jv.get("connections") or []) if c["map"] != mid]
        if n is not None:
            gg, mn = n["_ex"]
            volta = [x for x in conexoes_ex(gg, mn) if x["_ex"] == (g, i)]
            if not volta:
                print("  CONFLITO: o EX não grava a volta de %s para %s" % (vmid, mid))
            for x in volta:
                cv.append({k: v for k, v in x.items() if k != "_ex"})
                print("  outro lado: %s ganha %s %s offset %d" % (vnome, x["direction"], mid, x["offset"]))
        else:
            print("  outro lado: %s perde a conexão para %s" % (vnome, mid))
        escrever[pv] = dict(jv, connections=cv or None)
    if not a.aplica:
        print("  (demo: nada escrito)")
        return
    n_ = 0
    for p_, d in escrever.items():
        d = json.loads(json.dumps(d))
        orig = json.load(open(p_, encoding="utf-8"))
        chave = lambda l: sorted(json.dumps(x, sort_keys=True) for x in (l or []))
        if (chave(orig.get("connections")) == chave(d.get("connections"))
                and {k: v for k, v in orig.items() if k != "connections"} == {k: v for k, v in d.items() if k != "connections"}):
            continue  # nada mudou: o arquivo fica byte a byte igual (a ordem das conexões inclusive)
        grava_json(p_, reordena(d))
        n_ += 1
    print("  gravado: %d map.json (%d sem mudança, intocados)" % (n_, len(escrever) - n_))


_ID_NOME = None


def nome_de_id(mid):
    global _ID_NOME
    if _ID_NOME is None:
        _ID_NOME = {}
        base = os.path.join(RAIZ, "data/maps")
        for d in os.listdir(base):
            p = os.path.join(base, d, "map.json")
            if os.path.exists(p):
                try:
                    _ID_NOME[json.load(open(p, encoding="utf-8"))["id"]] = d
                except (ValueError, KeyError):
                    pass
    return _ID_NOME.get(mid)


ORDEM_CHAVES = ["id", "name", "layout", "music", "region", "region_map_section", "map_name_popup", "requires_flash",
                "weather", "map_type", "allow_cycling", "allow_escaping", "allow_running", "show_map_name",
                "battle_scene", "floor_number", "connections", "object_events", "warp_events", "coord_events", "bg_events",
                "shared_events_map", "shared_scripts_map"]


def reordena(d):
    out = {k: d[k] for k in ORDEM_CHAVES if k in d}
    for k in d:
        if k not in out:
            out[k] = d[k]
    return out


# ------------------------------------------------------------------ mapa novo

def grupo_destino(k):
    g, i = map(int, k.split("."))
    IND = {1: "IndoorLittleroot", 2: "IndoorOldale", 3: "IndoorDewford", 4: "IndoorLavaridge", 5: "IndoorFallarbor",
           6: "IndoorVerdanturf", 7: "IndoorPacifidlog", 8: "IndoorPetalburg", 9: "IndoorSlateport", 10: "IndoorMauville",
           11: "IndoorRustboro", 12: "IndoorFortree", 13: "IndoorLilycove", 14: "IndoorMossdeep", 16: "IndoorEverGrande"}
    if k == "27.117":
        return None
    if k == "29.89":
        return "gMapGroup_SpecialArea"
    if g == 0:
        return "gMapGroup_TownsAndRoutes"
    if g in (27, 29):
        return "gMapGroup_Dungeons"
    if g in IND:
        return "gMapGroup_" + IND[g]
    return GRUPO_NOVO


def snake(nome):
    """PokemonCenter_1F -> POKEMON_CENTER_1F (sem quebrar "1F" em "1_F", como o repo escreve)."""
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", nome).upper()


# MAPSEC dos nomes novos (decisões do Fable, briefing da onda 1 e decisão 6)
MAPSEC_NOVO = {
    "FOOTHILL TOWN": ("MAPSEC_FOOTHILL_TOWN", None),
    "HAUNTED WOODS": ("MAPSEC_HAUNTED_WOODS", None),
    "FROZEN HEIGHTS": ("MAPSEC_FROZEN_HEIGHTS", None),
    "DONTO ISLAND": ("MAPSEC_DONTO_ISLAND", None),
    "ROUTE 135": ("MAPSEC_ROUTE_104", "ROUTE 135"),
    "ROUTE 136": ("MAPSEC_ROUTE_117", "ROUTE 136"),
    "ROUTE 137": ("MAPSEC_ROUTE_110", "ROUTE 137"),
    "ROUTE 138": ("MAPSEC_ROUTE_111", "ROUTE 138"),
    "MUSCLE ISLAND": ("MAPSEC_ROUTE_125", "MUSCLE ISLAND"),
}


def mapsec_nosso(nome_sec):
    if nome_sec in MAPSEC_NOVO:
        return MAPSEC_NOVO[nome_sec]
    secs = json.load(open(os.path.join(RAIZ, "src/data/region_map/region_map_sections.json"), encoding="utf-8"))["map_sections"]
    # a seção cujo id é o próprio nome ganha (conserto do lote C, 23/09/2026: o
    # filtro de id terminado em "2", feito para METEOR_FALLS2 e irmãos, recusava
    # MAPSEC_ROUTE_122, _102, _112 e _132)
    direto = "MAPSEC_" + re.sub(r"[^A-Z0-9]+", "_", nome_sec.upper()).strip("_")
    for s_ in secs:
        if s_.get("name") == nome_sec and s_["id"] == direto:
            return s_["id"], None
    for s_ in secs:
        if s_.get("name") == nome_sec and not s_["id"].endswith("2"):
            return s_["id"], None
    raise KeyError(nome_sec)


def musica_nossa(n):
    d = _enum_vanilla("include/constants/songs.h", "MUS_")
    return d.get(n)


def cabecalho_ex(g, i):
    C = ex()
    m = C.M[(g, i)]
    b = C.rom[m["off"]:m["off"] + 0x1C]
    fl = b[0x1A]
    return {"musica": m["musica"], "secao": C.mapsec.get(m["secao"]), "flash": b[0x15], "clima": b[0x16], "tipo": b[0x17],
            "bicicleta": bool(fl & 1), "fuga": bool(fl & 2), "corre": bool(fl & 4), "nome": bool(fl >> 3), "batalha": b[0x1B]}


def warp_nosso_dest(gg, mn, wid):
    """Id do warp NOSSO no destino que corresponde ao warp `wid` do mapa (gg, mn) do EX.

    Destino que já tem a planta do EX (aumentado já aplicado, ou novo): o warp
    nosso que está na MESMA célula do warp do EX. Destino que o EX não mudou de
    tamanho: o índice é o do vanilla, conferido pela posição.
    """
    dnome = nome_nosso(gg, mn)
    wex = eventos_ex(gg, mn)[1]
    if wid >= len(wex):
        return None, "o EX aponta para warp %d que não existe em %s" % (wid, dnome)
    alvo = (wex[wid]["x"], wex[wid]["y"])
    pj = os.path.join(RAIZ, "data/maps", dnome, "map.json")
    if not os.path.exists(pj):
        if e_novo(gg, mn):
            return wid, None
        return None, "%s não existe no repo" % dnome
    ws = json.load(open(pj, encoding="utf-8")).get("warp_events") or []
    for k, w in enumerate(ws):
        if (w["x"], w["y"]) == alvo:
            return k, None
    if wid < len(ws):
        return wid, "posição do warp %d em %s não bate com a do EX %s (nosso %s): conferir" % (
            wid, dnome, alvo, (ws[wid]["x"], ws[wid]["y"]))
    return None, "nenhum warp nosso em %s na célula %s" % (dnome, alvo)


# secundário do EX sem rótulo único no fidel.json (usado por mapas cujo vanilla
# era Mossdeep e Cave): pela maioria dos metatiles, é o gTileset_Mossdeep
# (medido pelo lote C em 23/09/2026: Mossdeep City, Routes 125 e 128, Muscle e Donto)
ROTULO_HEX = {"0xc61fb4": "gTileset_Mossdeep",
              # primário NOVO do EX, só da Frozen Heights (27.118): instalado pelo
              # lote B como gTileset_FrozenHeights (extrai_tileset + instala_tileset)
              "0xc625ec": "gTileset_FrozenHeights",
              # secundários NOVOS dos ginásios do EX (onda 2, lote G1): só os metatiles que
              # o ginásio usa, renumerados; o map.bin sai com o de-para do plano do lote
              "0xc62604": "gTileset_PetalburgWoodsGym",
              "0xc6261c": "gTileset_VerdanturfGym"}


# Onda 2, lote G3 (Clair e Blaine de Hoenn): nomes dos mapas e rótulos dos dois
# secundários novos. Bloco separado de propósito, para não encostar nas linhas que o
# G1 e o G2 acrescentam aos dicionários lá em cima. As salas 33.5 e 33.6 do EX não
# têm porta (a 33.4 leva direto à arena 33.7) e ficam FORA, como os interiores sem
# porta da onda 1.
NOMES_NOVOS.update({
    "34.1": "Route123_HiddenRiver",
    "34.2": "Route123_Gym",
    "34.3": "Route123_Gym2",
    "33.1": "MtChimney_GymEntrance",
    "33.2": "MtChimney_GymQuiz1",
    "33.3": "MtChimney_GymQuiz2",
    "33.4": "MtChimney_GymQuiz3",
    "33.7": "MtChimney_Gym",
})
# 0xc62664: secundário novo do ginásio da Route 123, arte do EX, recortado nos 69
# metatiles que o 34.2 e o 34.3 usam (mais os do `setmetatile` das portas).
# 0xc6217c: é o Facility (512 tiles iguais aos nossos, 3 metatiles redefinidos pelo
# EX); as salas do Mt. Chimney ganham cópia própria, recortada nos 27 metatiles
# usados, com a NOSSA paleta. O Facility de 511 metatiles não é tocado.
ROTULO_HEX.update({"0xc62664": "gTileset_Route123Gym"})
ROTULO_TROCA_G3 = {"33.1": "gTileset_MtChimneyGym", "33.2": "gTileset_MtChimneyGym",
                   "33.3": "gTileset_MtChimneyGym", "33.4": "gTileset_MtChimneyGym"}


def rotulo_tileset(v, k):
    ex_k = k.split(" ")[-1]
    if k.startswith("ts2") and ex_k in ROTULO_TROCA_G3:
        return ROTULO_TROCA_G3[ex_k]
    v = ROTULO_HEX.get(v, v)
    if v.startswith("0x"):
        raise SystemExit("ERRO: o %s de %s sai em hexadecimal (%s): tileset NOVO do EX (onda 2) ou rótulo a medir;"
                         " nada é gravado em layouts.json com hexadecimal." % ("secundário" if "2" in k else "primário", k, v))
    return v


def cmd_novo(a):
    C = ex()
    g, i = map(int, a.ex.split("."))
    if not e_novo(g, i):
        raise SystemExit("ERRO: %s não é mapa novo." % a.ex)
    nome = nome_nosso(g, i)
    grupo = grupo_destino(a.ex)
    if grupo is None:
        raise SystemExit("ERRO: %s fica FORA (Viridian Forest órfão, PLANO a.1)." % a.ex)
    F = dict(fidel()[a.ex])
    F["ts1"], F["ts2"] = rotulo_tileset(F["ts1"], "ts1 " + a.ex), rotulo_tileset(F["ts2"], "ts2 " + a.ex)
    w, h, blob, borda = planta_ex(g, i)
    hdr = cabecalho_ex(g, i)
    sec, popup = mapsec_nosso(hdr["secao"])
    lay_id = "LAYOUT_" + snake(nome)
    mid = "MAP_" + snake(nome)
    mus = musica_nossa(hdr["musica"])
    tipos = _enum_vanilla("include/constants/map_types.h", "MAP_TYPE_")
    climas = _enum_vanilla("include/constants/weather.h", "WEATHER_")
    cenas = _enum_vanilla("include/constants/map_types.h", "MAP_BATTLE_SCENE_")
    print("NOVO %s (EX %s): %dx%d, %s + %s, grupo %s, %s, %s%s, música %s, %s, %s"
          % (nome, a.ex, w, h, F["ts1"], F["ts2"], grupo, mid, sec, (" letreiro %s" % popup) if popup else "",
             mus, tipos.get(hdr["tipo"]), climas.get(hdr["clima"])))
    if not cabe(w, h):
        raise SystemExit("ERRO: %dx%d passa de MAX_MAP_DATA_SIZE." % (w, h))
    conflitos = []
    if mus is None:
        conflitos.append("música %d do EX sem nome no vanilla: usei MUS_ROUTE101, trocar à mão" % hdr["musica"])
        mus = "MUS_ROUTE101"
    warps = []
    for wv in eventos_ex(g, i)[1]:
        dest = nome_nosso(wv["g"], wv["i"])
        did, prob = warp_nosso_dest(wv["g"], wv["i"], wv["warp"])
        if prob:
            conflitos.append("warp %d -> %s: %s" % (wv["k"], dest, prob))
        warps.append({"x": wv["x"], "y": wv["y"], "elevation": wv["elev"], "dest_map": id_mapa_repo(dest),
                      "dest_warp_id": str(did if did is not None else 0)})
    for c in conflitos:
        print("  CONFLITO: " + c)
    lj = layouts()
    if any(l and l.get("id") == lay_id for l in lj["layouts"]):
        raise SystemExit("ERRO: %s já existe em layouts.json." % lay_id)
    if not a.aplica:
        print("  (demo: nada escrito)")
        return
    rel_lay = "data/layouts/" + nome
    os.makedirs(os.path.join(RAIZ, rel_lay), exist_ok=True)
    open(os.path.join(RAIZ, rel_lay, "map.bin"), "wb").write(blob)
    open(os.path.join(RAIZ, rel_lay, "border.bin"), "wb").write(borda)
    lj["layouts"].append({"id": lay_id, "name": nome + "_Layout", "width": w, "height": h,
                          "primary_tileset": F["ts1"], "secondary_tileset": F["ts2"],
                          "border_filepath": rel_lay + "/border.bin", "blockdata_filepath": rel_lay + "/map.bin",
                          "layout_version": "emerald"})
    grava_json(os.path.join(RAIZ, "data/layouts/layouts.json"), lj)
    mj = {"id": mid, "name": nome, "layout": lay_id, "music": mus, "region": "REGION_HOENN",
          "region_map_section": sec}
    if popup:
        mj["map_name_popup"] = popup
    mj.update({"requires_flash": bool(hdr["flash"]), "weather": climas.get(hdr["clima"], "WEATHER_NONE"),
               "map_type": tipos.get(hdr["tipo"], "MAP_TYPE_NONE"), "allow_cycling": hdr["bicicleta"],
               "allow_escaping": hdr["fuga"], "allow_running": hdr["corre"], "show_map_name": hdr["nome"],
               "battle_scene": cenas.get(hdr["batalha"], "MAP_BATTLE_SCENE_NORMAL"), "connections": None,
               "object_events": [], "warp_events": warps, "coord_events": [], "bg_events": []})
    os.makedirs(os.path.join(RAIZ, "data/maps", nome), exist_ok=True)
    grava_json(os.path.join(RAIZ, "data/maps", nome, "map.json"), mj)
    open(os.path.join(RAIZ, "data/maps", nome, "scripts.inc"), "w", encoding="utf-8").write(
        "@ %s: planta copiada do Pokémon Emerald EX v1.0.4 (mapa %s) por dev_scripts/copia_planta_ex.py.\n\n"
        "%s_MapScripts::\n\t.byte 0\n" % (nome, a.ex, nome))
    pg = os.path.join(RAIZ, "data/maps/map_groups.json")
    gr = json.load(open(pg, encoding="utf-8"))
    if grupo not in gr:
        gr["group_order"].append(grupo)   # grupo novo sempre no FIM (não desloca mapa salvo)
        gr[grupo] = []
    if nome not in gr[grupo]:
        gr[grupo].append(nome)
    grava_json(pg, gr)
    pe = os.path.join(RAIZ, "data/event_scripts.s")
    linha = '\t.include "data/maps/%s/scripts.inc"\n' % nome
    t = open(pe, encoding="utf-8").read()
    if linha not in t:
        open(pe, "a", encoding="utf-8").write(linha)
    global _ID_NOME
    _ID_NOME = None
    print("  gravado: layout %s, mapa %s no fim de %s (índice %d), %d warps do EX"
          % (lay_id, mid, grupo, gr[grupo].index(nome), len(warps)))


# ------------------------------------------------------------------ eventos novos

ANCORAS_F = [(2, 95), (18, 104), (25, 107), (34, 110), (37, 114), (38, 116), (41, 117), (48, 124), (56, 126)]


def nivel_f(n):
    """PLANO (c.1): teto do EX -> nível nosso, linear entre os 8 líderes que já
    temos, com a ponta baixa 2 -> 95. Fora das pontas, satura."""
    if n <= ANCORAS_F[0][0]:
        return ANCORAS_F[0][1]
    for (a0, b0), (a1, b1) in zip(ANCORAS_F, ANCORAS_F[1:]):
        if n <= a1:
            return int(b0 + (b1 - b0) * (n - a0) / (a1 - a0) + 0.5)
    return ANCORAS_F[-1][1]


def _defines(arq, prefixo):
    out = {}
    for ln in open(os.path.join(RAIZ, arq), encoding="utf-8"):
        m = re.match(r"#define\s+(%s[A-Z0-9_]+)\s+(\S+)" % prefixo, ln)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def flags_livres_do_lote(lote, faixa="flags"):
    """Nomes FLAG_UNUSED_0xNNNN livres da faixa do lote. ATENÇÃO: o nome NÃO é o
    valor (medido em 23/09/2026: FLAG_UNUSED_0x1F00 vale 0x1625 e FLAG_UNUSED_0x2F00
    vale 0x2625). Item escondido guarda (flag - 0x1F4) em 13 bits, então usa a
    faixa `ocultos`, cujo valor real cabe; `valor_flag` confere compilando."""
    a, b = LOTES[lote][faixa]
    usados = set(_defines("include/constants/flags.h", "FLAG_").values())
    return ["FLAG_UNUSED_0x%04X" % v for v in range(a, b + 1) if "FLAG_UNUSED_0x%04X" % v not in usados]


_VAL = {}


def valor_flag(nome):
    """Valor numérico de uma flag, pelo pré-processador de verdade (cc do host)."""
    if nome not in _VAL:
        import subprocess, tempfile
        d = tempfile.mkdtemp()
        open(d + "/f.c", "w").write('#include <stdio.h>\n#include "constants/flags.h"\nint main(){printf("%%d",%s);}\n' % nome)
        subprocess.run(["cc", "-I", os.path.join(RAIZ, "include"), "-o", d + "/f", d + "/f.c"], check=True)
        _VAL[nome] = int(subprocess.run([d + "/f"], capture_output=True, text=True).stdout)
    return _VAL[nome]


def reserva_do_lote(lote):
    """Entrada do lote no dev_scripts/hoennex_reserva_ids.json. A chave lá é
    "A-oeste", "B-centro", "C-leste" (conserto do lote C, 23/09/2026: a busca por
    "C" cru devolvia nada e os órfãos nunca entravam)."""
    pr = os.path.join(RAIZ, "dev_scripts/hoennex_reserva_ids.json")
    if not os.path.exists(pr):
        return {}
    lotes = json.load(open(pr, encoding="utf-8")).get("lotes", {})
    L = LOTES.get(lote, {})
    if "reserva" in L:
        # lote da onda 2: a fatia de posições da lista ordenada da entrada compartilhada
        v = lotes.get(L["reserva"], {})
        a, b = L["fatia"]
        ids = sorted(int(x) for x in v.get("orfaos_ids", []))[a:b]
        nomes = v.get("nomes_antigos", {})
        return {"orfaos_ids": ids, "nomes_antigos": {str(i): nomes.get(str(i), []) for i in ids}}
    for k, v in lotes.items():
        if k == lote or k.startswith(lote + "-"):
            return v
    return {}


def ids_livres_do_lote(lote):
    """Livres da faixa do lote primeiro, depois os ÓRFÃOS da reserva que ainda
    não ganharam nome TRAINER_HOENNEX_* (um órfão reusado sai da lista)."""
    usados = set()
    novos = set()
    for arq in ("include/constants/opponents.h", "include/constants/opponents_frlg.h"):
        for nome, v in _defines(arq, "TRAINER_").items():
            if v.isdigit():
                usados.add(int(v))
                if nome.startswith("TRAINER_HOENNEX_"):
                    novos.add(int(v))
    ids = [i for i in LOTES[lote]["ids"] if i not in usados]
    for i in reserva_do_lote(lote).get("orfaos_ids", []):
        if int(i) not in novos:
            ids.append(int(i))
    return ids


def reusa_orfao(lote, tid):
    """Receita do ids_orfaos.py para UM órfão: apaga o #define antigo (opponents.h
    ou opponents_frlg.h) e o bloco `=== TRAINER_ANTIGO ===` do trainers.party.
    Id que não é órfão (livre da faixa) não tem nada a apagar."""
    antigos = reserva_do_lote(lote).get("nomes_antigos", {}).get(str(tid), [])
    feitos = []
    for nome in antigos:
        for arq in ("include/constants/opponents.h", "include/constants/opponents_frlg.h"):
            p = os.path.join(RAIZ, arq)
            t = open(p, encoding="utf-8").read()
            t2 = re.sub(r"^#define\s+%s\s+%d\b[^\n]*\n" % (re.escape(nome), tid), "", t, flags=re.M)
            if t2 != t:
                open(p, "w", encoding="utf-8").write(t2)
                feitos.append("%s (%s)" % (nome, arq))
        p = os.path.join(RAIZ, "src/data/trainers.party")
        t = open(p, encoding="utf-8").read()
        m = re.search(r"^=== %s ===\n.*?(?=^=== |\Z)" % re.escape(nome), t, flags=re.M | re.S)
        if m:
            t = t[:m.start()] + t[m.end():]
            open(p, "w", encoding="utf-8").write(t)
            feitos.append("bloco %s do trainers.party" % nome)
    return feitos


RESERVA_FIM = "// <<< RESERVA DE IDS DA FRENTE HOENN EX <<<"


def define_na_reserva(linhas):
    """TRAINER_HOENNEX_* vai DENTRO do bloco da reserva do opponents.h (guarda b
    do ids_orfaos.py), logo antes da marca de fim."""
    p = os.path.join(RAIZ, "include/constants/opponents.h")
    t = open(p, encoding="utf-8").read()
    if RESERVA_FIM not in t:
        raise SystemExit("ERRO: bloco da reserva de ids não achado no opponents.h")
    i = t.index(RESERVA_FIM)
    t = t[:i] + "".join(l + "\n" for l in linhas) + t[i:]
    open(p, "w", encoding="utf-8").write(t)


def acrescenta_bloco(arq, abre, fecha, linhas, antes_de=None):
    """Acrescenta linhas num bloco marcado do arquivo (cria o bloco se faltar)."""
    p = os.path.join(RAIZ, arq)
    t = open(p, encoding="utf-8").read()
    if abre not in t:
        bloco = abre + "\n" + fecha + "\n"
        if antes_de and antes_de in t:
            t = t.replace(antes_de, bloco + "\n" + antes_de, 1)
        else:
            t = t.rstrip("\n") + "\n\n" + bloco
    i = t.index(fecha, t.index(abre))
    t = t[:i] + "".join(l + "\n" for l in linhas) + t[i:]
    open(p, "w", encoding="utf-8").write(t)


def strings_inc(rotulo, linhas):
    return [rotulo + ":"] + ['\t.string "%s"' % l for l in linhas] + [""]


def gfx_nosso(n):
    nome = enum("gfx").get(n)
    if nome and re.search(r"\b%s\b" % nome, open(os.path.join(RAIZ, "include/constants/event_objects.h")).read()):
        return nome
    return None


def party_ex(tid):
    """Time do EX (espécie nacional + nível), o registro de 36 B e a party de 32 B."""
    C = ex()
    rom = C.rom
    S = C.TR_BASE + 36 * tid
    p = _ptr(struct.unpack_from("<I", rom, S + 4)[0])
    n = rom[S + 32]
    mons = []
    for k in range(n):
        q = p + 32 * k
        mons.append({"especie": struct.unpack_from("<H", rom, q + 20)[0], "nivel": rom[q + 26],
                     "golpes": list(struct.unpack_from("<4H", rom, q + 12))})
    return {"nome": C.texto(S + 19, 12), "classe": rom[S + 16], "musica": rom[S + 17], "pic": rom[S + 18],
            "duplo": False, "mons": mons}


def cmd_eventos(a):
    """Escreve os eventos NOVOS do EX no fim das listas do nosso mapa.

    Roda DEPOIS de `aumenta` ou `novo` (os nossos já estão na grade do EX, por
    isso o casamento aqui é com deslocamento zero)."""
    g, i = map(int, a.ex.split("."))
    nome = nome_nosso(g, i)
    pj = os.path.join(RAIZ, "data/maps", nome, "map.json")
    j = json.load(open(pj, encoding="utf-8"))
    objs, warps, coords, bgs = eventos_ex(g, i)
    cas = casa_eventos(g, i, j, 0, 0)
    snk = snake(nome)
    novos = {"object_events": [], "warp_events": [], "bg_events": []}
    inc, flags_h, opp_h, party, pend, casados = [], [], [], [], [], []
    flags_livres = flags_livres_do_lote(a.lote)
    ocultos_livres = flags_livres_do_lote(a.lote, "ocultos")
    ids_livres = ids_livres_do_lote(a.lote)
    mov = enum("mov")
    duplos_feitos = {}
    for o in objs:
        if o["k"] in cas["obj"]:
            k, prova = cas["obj"][o["k"]]
            casados.append("obj EX %d = nosso %d (%s)" % (o["k"], k, prova))
            continue
        c = classifica_script(o["script"])
        tp = tipo_obj_ex(o, c)
        gx = gfx_nosso(o["gfx"])
        base = {"graphics_id": gx, "x": o["x"], "y": o["y"], "elevation": o["elev"],
                "movement_type": mov.get(o["mov"], "MOVEMENT_TYPE_NONE"), "movement_range_x": o["rx"],
                "movement_range_y": o["ry"], "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
                "script": None, "flag": "0"}
        if not gx:
            pend.append("obj EX %d (%d,%d): sprite %d do EX sem equivalente nosso" % (o["k"], o["x"], o["y"], o["gfx"]))
            continue
        if tp == "item" and c["tipo"] == "item":
            it = item_nosso(itens_ex().get(o["trng"], "?"))
            if not it:
                pend.append("obj EX %d (%d,%d): item %s do EX sem equivalente nosso" % (o["k"], o["x"], o["y"], itens_ex().get(o["trng"])))
                continue
            if not flags_livres:
                pend.append("obj EX %d: item %s sem flag livre na faixa do lote %s" % (o["k"], it, a.lote))
                continue
            fl = "FLAG_ITEM_HOENNEX_%s_%s" % (snk, it[5:])
            n_ = 2
            while fl in _defines("include/constants/flags.h", "FLAG_") or any(fl + " " in x for x in flags_h):
                fl = "FLAG_ITEM_HOENNEX_%s_%s_%d" % (snk, it[5:], n_); n_ += 1
            flags_h.append("#define %-52s %s  // %s" % (fl, flags_livres.pop(0), it))
            base.update(trainer_sight_or_berry_tree_id=it, script="Common_EventScript_FindItem", flag=fl)
            novos["object_events"].append(base)
        elif c["tipo"] in ("fala", "placa") and tp == "npc":
            rot = "%s_EventScript_ExNpc%d" % (nome, o["k"])
            txt = "%s_Text_ExNpc%d" % (nome, o["k"])
            std = "MSGBOX_SIGN" if c["tipo"] == "placa" else "MSGBOX_NPC"
            inc += [rot + "::", "\tmsgbox %s, %s" % (txt, std), "\tend", ""] + strings_inc(txt, c["texto"])
            base.update(script=rot)
            if o["flag"]:
                pend.append("obj EX %d (%d,%d): NPC novo com flag de esconder 0x%X do EX: entrou SEM flag (sempre visível)"
                            % (o["k"], o["x"], o["y"], o["flag"]))
            if c.get("cauda"):
                casados.append("obj EX %d: a volta de olhar do NPC depois da fala não foi copiada" % o["k"])
            novos["object_events"].append(base)
        elif c["tipo"] == "treinador" and tp == "treinador" and c["id"] in duplos_feitos:
            # segundo objeto do par duplo: mesmo treinador, mesma fala
            tconst, rot = duplos_feitos[c["id"]]
            base.update(trainer_type=TIPO_TREINADOR.get(o["ttype"], "TRAINER_TYPE_NORMAL"),
                        trainer_sight_or_berry_tree_id=str(o["trng"]), script=rot)
            novos["object_events"].append(base)
            casados.append("par do duplo %s = EX %d, mesmo script %s" % (tconst, c["id"], rot))
        elif c["tipo"] == "treinador" and tp == "treinador":
            P = party_ex(c["id"])
            cls = enum("classe").get(P["classe"])
            pic = enum("pic").get(P["pic"])
            mus = enum("musica").get(P["musica"] & 0x7F)
            esp = [(especie_nossa(m["especie"]), nivel_f(m["nivel"])) for m in P["mons"]]
            if not (cls and pic and mus) or any(e is None for e, _ in esp):
                pend.append("obj EX %d: treinador %s (EX %d): classe/pic/música/espécie sem equivalente %s"
                            % (o["k"], P["nome"], c["id"], [m["especie"] for m in P["mons"]]))
                continue
            if not ids_livres:
                pend.append("obj EX %d: treinador %s (EX %d) sem id livre na faixa do lote %s (ESPERA órfãos)"
                            % (o["k"], P["nome"], c["id"], a.lote))
                continue
            tid = ids_livres.pop(0)
            nm = re.sub(r"[^A-Z0-9]", "_", P["nome"].upper()).strip("_")
            tconst = "TRAINER_HOENNEX_%s_%s" % (snk, nm)
            opp_h.append("#define %-52s %d" % (tconst, tid))
            party += ["=== %s ===" % tconst, "Name: %s" % P["nome"], "Class: %s" % cls, "Pic: %s" % pic,
                      "Gender: %s" % ("Female" if P["musica"] & 0x80 else "Male"), "Music: %s" % mus,
                      "Double Battle: %s" % ("Yes" if c.get("duplo") else "No"), "AI: Check Bad Move", ""]
            for e, lv in esp:
                party += [e, "Level: %d" % lv, "IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe", ""]
            rot = "%s_EventScript_ExTrainer%d" % (nome, o["k"])
            ti, td, tp_ = ("%s_Text_ExTrainer%d%s" % (nome, o["k"], x) for x in ("Intro", "Defeat", "PostBattle"))
            if c.get("duplo"):
                tn = "%s_Text_ExTrainer%dNotEnough" % (nome, o["k"])
                inc += [rot + "::", "\ttrainerbattle_double %s, %s, %s, %s" % (tconst, ti, td, tn),
                        "\tmsgbox %s, MSGBOX_AUTOCLOSE" % tp_, "\tend", ""]
                inc += strings_inc(tn, c["sem_dois"])
                duplos_feitos[c["id"]] = (tconst, rot)
            else:
                inc += [rot + "::", "\ttrainerbattle_single %s, %s, %s" % (tconst, ti, td),
                        "\tmsgbox %s, MSGBOX_AUTOCLOSE" % tp_, "\tend", ""]
            inc += strings_inc(ti, c["intro"]) + strings_inc(td, c["derrota"]) + strings_inc(tp_, c["depois"])
            base.update(trainer_type=TIPO_TREINADOR.get(o["ttype"], "TRAINER_TYPE_NORMAL"),
                        trainer_sight_or_berry_tree_id=str(o["trng"]), script=rot)
            novos["object_events"].append(base)
            casados.append("treinador novo %s = EX %d %s, id %d, níveis EX %s -> %s"
                           % (tconst, c["id"], P["nome"], tid, [m["nivel"] for m in P["mons"]], [lv for _, lv in esp]))
        else:
            pend.append("obj EX %d (%d,%d) %s %s: %s %s" % (o["k"], o["x"], o["y"], enum("gfx").get(o["gfx"]), tp, c["tipo"],
                                                             c.get("motivo") or ("texto: " + texto_plano(c.get("texto", []))[:60]
                                                                                  if c.get("texto") else "")))
    for w in warps:
        if w["k"] in cas["warp"]:
            continue
        dest = nome_nosso(w["g"], w["i"])
        did, prob = warp_nosso_dest(w["g"], w["i"], w["warp"])
        if prob:
            pend.append("warp EX %d -> %s: %s" % (w["k"], dest, prob))
            if did is None:
                continue
        novos["warp_events"].append({"x": w["x"], "y": w["y"], "elevation": w["elev"], "dest_map": id_mapa_repo(dest),
                                     "dest_warp_id": str(did)})
    FACE = {0: "BG_EVENT_PLAYER_FACING_ANY", 1: "BG_EVENT_PLAYER_FACING_NORTH", 2: "BG_EVENT_PLAYER_FACING_SOUTH",
            3: "BG_EVENT_PLAYER_FACING_EAST", 4: "BG_EVENT_PLAYER_FACING_WEST"}
    for b in bgs:
        if b["k"] in cas["bg"]:
            continue
        if b["kind"] in FACE:
            c = classifica_script(b["u"])
            if c["tipo"] in ("placa", "fala"):
                rot = "%s_EventScript_ExSign%d" % (nome, b["k"])
                txt = "%s_Text_ExSign%d" % (nome, b["k"])
                inc += [rot + "::", "\tmsgbox %s, MSGBOX_SIGN" % txt, "\tend", ""] + strings_inc(txt, c["texto"])
                novos["bg_events"].append({"type": "sign", "x": b["x"], "y": b["y"], "elevation": b["elev"],
                                           "player_facing_dir": FACE[b["kind"]], "script": rot})
                continue
            pend.append("bg EX %d (%d,%d): %s %s" % (b["k"], b["x"], b["y"], c["tipo"], c.get("motivo")))
        elif b["kind"] == 7:
            it = item_nosso(itens_ex().get(b["u"] & 0xFFFF, "?"))
            if not it or not ocultos_livres:
                pend.append("bg EX %d (%d,%d): item ESCONDIDO %s sem item nosso ou sem flag livre na faixa de ocultos do lote"
                            % (b["k"], b["x"], b["y"], itens_ex().get(b["u"] & 0xFFFF)))
                continue
            un = ocultos_livres.pop(0)
            if not (0x1F4 <= valor_flag(un) < 0x1F4 + 8192):
                raise SystemExit("ERRO: %s vale 0x%X e não cabe no hiddenItemId de 13 bits" % (un, valor_flag(un)))
            fl = "FLAG_HIDDEN_ITEM_HOENNEX_%s_%s" % (snk, it[5:])
            n_ = 2
            while fl in _defines("include/constants/flags.h", "FLAG_") or any(fl + " " in x for x in flags_h):
                fl = "FLAG_HIDDEN_ITEM_HOENNEX_%s_%s_%d" % (snk, it[5:], n_); n_ += 1
            flags_h.append("#define %-52s %s  // %s, escondido" % (fl, un, it))
            novos["bg_events"].append({"type": "hidden_item", "x": b["x"], "y": b["y"], "elevation": b["elev"],
                                       "item": it, "flag": fl})
        else:
            pend.append("bg EX %d (%d,%d): tipo %d (base secreta ou outro)" % (b["k"], b["x"], b["y"], b["kind"]))
    for c in coords:
        if c["k"] in cas["coord"]:
            continue
        pend.append("coord EX %d (%d,%d): gatilho de enredo var 0x%X=%d, script 0x%X" % (c["k"], c["x"], c["y"], c["var"], c["val"], c["script"]))
    print("EVENTOS %s (EX %s), lote %s" % (nome, a.ex, a.lote))
    for x in casados:
        print("  casado: " + x)
    for t, l in novos.items():
        for e in l:
            print("  NOVO %s (%d,%d) %s" % (t, e["x"], e["y"], e.get("script") or e.get("dest_map")))
    for x in pend:
        print("  PENDÊNCIA: " + x)
    if not a.aplica:
        print("  (demo: nada escrito)")
        return
    for t, l in novos.items():
        j[t] = (j.get(t) or []) + l
    grava_json(pj, reordena(j))
    if inc:
        ps = os.path.join(RAIZ, "data/maps", nome, "scripts.inc")
        with open(ps, "a", encoding="utf-8") as f:
            f.write("\n@ Eventos novos do Pokémon Emerald EX (mapa %s), reescritos a partir do texto da ROM\n"
                    "@ por dev_scripts/copia_planta_ex.py.\n" % a.ex)
            f.write("\n".join(inc) + "\n")
    L = a.lote
    if flags_h:
        acrescenta_bloco("include/constants/flags.h", "// >>> Hoenn EX, lote %s (faixa 0x%04X a 0x%04X) >>>" % ((L,) + LOTES[L]["flags"]),
                         "// <<< Hoenn EX, lote %s <<<" % L,
                         ["// %s (EX %s): bolas de item novas, apelidos de FLAG_UNUSED da faixa do lote; save intacta." % (nome, a.ex)] + flags_h)
    if opp_h:
        for ln in opp_h:
            for x in reusa_orfao(L, int(ln.split()[-1])):
                print("  órfão reusado: apagado %s" % x)
        define_na_reserva(["// lote %s, %s (EX %s): ids da reserva (livre da faixa ou órfão provado); abaixo de 2200, save intacta."
                           % (L, nome, a.ex)] + opp_h)
    if party:
        with open(os.path.join(RAIZ, "src/data/trainers.party"), "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(party))
    print("  gravado: %s" % ", ".join("%d %s" % (len(l), t) for t, l in novos.items()))


# ------------------------------------------------------------------ encontros selvagens

WILD_TAB = 0xC7F9C0   # gWildMonHeaders do EX (achado pela entrada da Route 101, registro de 20 B como o vanilla)
WILD_SLOTS = (("land_mons", 12), ("water_mons", 5), ("rock_smash_mons", 5), ("fishing_mons", 10))


def encontros_ex(g, i):
    C = ex()
    rom, r = C.rom, C.r
    o = WILD_TAB
    while o > 0 and rom[o - 20] != 0xFF and r.valido(struct.unpack_from("<I", rom, o - 16)[0] or 0x08000000):
        o -= 20
    while rom[o] != 0xFF:
        if (rom[o], rom[o + 1]) == (g, i):
            out = {}
            for k, (tipo, n) in enumerate(WILD_SLOTS):
                p = struct.unpack_from("<I", rom, o + 4 + 4 * k)[0]
                if not p:
                    continue
                q = r.deref(p)
                taxa = rom[q]
                mp = r.deref(struct.unpack_from("<I", rom, q + 4)[0])
                mons = []
                for s_ in range(n):
                    mn, mx, sp = struct.unpack_from("<BBH", rom, mp + 4 * s_)
                    mons.append((mn, mx, sp))
                out[tipo] = (taxa, mons)
            return out
        o += 20
        if o > WILD_TAB + 20 * 2000:
            break
    return None


def cmd_encontros(a):
    g, i = map(int, a.ex.split("."))
    nome = nome_nosso(g, i)
    mid = id_mapa_repo(nome)
    e = encontros_ex(g, i)
    if not e:
        print("ENCONTROS %s: o EX não tem tabela para o mapa" % nome)
        return
    ent = {"map": mid, "base_label": "g" + nome}
    for tipo, (taxa, mons) in e.items():
        lst = []
        for mn, mx, sp in mons:
            esp = especie_nossa(sp)
            if not esp:
                raise SystemExit("ERRO: espécie %d do EX sem equivalente" % sp)
            lst.append({"min_level": nivel_f(mn), "max_level": nivel_f(mx), "species": esp})
        ent[tipo] = {"encounter_rate": taxa, "mons": lst}
        print("ENCONTROS %s %s taxa %d: %s" % (nome, tipo, taxa, ", ".join(
            "%s %d-%d" % (m["species"][8:], m["min_level"], m["max_level"]) for m in lst)))
    pw = os.path.join(RAIZ, "src/data/wild_encounters.json")
    d = json.load(open(pw, encoding="utf-8"))
    grp = d["wild_encounter_groups"][0]
    if any(x.get("map") == mid for x in grp["encounters"]):
        print("  já existe tabela para %s: nada escrito" % mid)
        return
    if not a.aplica:
        print("  (demo: nada escrito)")
        return
    grp["encounters"].append(ent)
    with open(pw, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("  gravado em src/data/wild_encounters.json (níveis pela f do PLANO c.1)")


# ------------------------------------------------------------------ lista

def cmd_lista(a):
    C = ex()
    g, i = map(int, a.ex.split("."))
    m = C.M[(g, i)]
    L = m["layout"]
    F = fidel().get(a.ex, {})
    print("EX %s  %s  nosso nome: %s  %dx%d  %s + %s  MAPSEC %s  música %d  tipo %d"
          % (a.ex, C.mapsec.get(m["secao"]), nome_nosso(g, i), L["w"], L["h"], F.get("ts1"), F.get("ts2"),
             m["secao"], m["musica"], m["tipo"]))
    for d, off, gg, mn in C.conexoes(m):
        print("  conexão %-6s offset %4d -> %s (EX %d.%d)" % (d, off, nome_nosso(gg, mn), gg, mn))
    objs, warps, coords, bgs = eventos_ex(g, i)
    gfx, mov = enum("gfx"), enum("mov")
    for w in warps:
        print("  warp %2d (%2d,%2d) el %d -> %s warp %d" % (w["k"], w["x"], w["y"], w["elev"], nome_nosso(w["g"], w["i"]), w["warp"]))
    for o in objs:
        c = classifica_script(o["script"])
        extra = ""
        if c["tipo"] in ("fala", "placa"):
            extra = texto_plano(c["texto"])[:70]
        elif c["tipo"] == "treinador" or c.get("id") is not None:
            t = C.treinador(c["id"])
            extra = "id %d %s classe %d n%d niv %s" % (c["id"], t["nome"], t["classe"], t["n"], t["niveis"])
        elif c["tipo"] == "item":
            extra = "item %s -> %s" % (itens_ex().get(o["trng"], "?"), item_nosso(itens_ex().get(o["trng"], "?")))
        else:
            extra = c.get("motivo") or ""
        print("  obj %2d local %2d (%2d,%2d) %-28s %-30s ttype %d rng %d flag 0x%X %s | %s"
              % (o["k"], o["local"], o["x"], o["y"], gfx.get(o["gfx"], o["gfx"]), mov.get(o["mov"], o["mov"]),
                 o["ttype"], o["trng"], o["flag"], c["tipo"], extra))
    for c in coords:
        print("  coord (%2d,%2d) var 0x%X=%d script 0x%X" % (c["x"], c["y"], c["var"], c["val"], c["script"]))
    for b in bgs:
        if b["kind"] == 7:
            it = b["u"] & 0xFFFF
            print("  bg (%2d,%2d) ESCONDIDO item %s flag+%d" % (b["x"], b["y"], itens_ex().get(it, it), (b["u"] >> 16) & 0xFFFF))
        else:
            c = classifica_script(b["u"])
            print("  bg (%2d,%2d) kind %d %s %s" % (b["x"], b["y"], b["kind"], c["tipo"],
                                                   texto_plano(c.get("texto", []))[:70] or c.get("motivo")))


def autoteste():
    falhas = []
    ok = [nivel_f(x) for x in (2, 18, 22, 25, 26, 32, 35, 47, 56, 80)] == [95, 104, 106, 107, 107, 109, 111, 123, 126, 126]
    print("1. função f do PLANO (c.1) nas âncoras e nos líderes novos: %s" % ("OK" if ok else "FALHOU"))
    falhas += [] if ok else ["nivel_f"]
    ok = (snake("PetalburgCity_House3") == "PETALBURG_CITY_HOUSE3" and snake("Route135") == "ROUTE135"
          and snake("FoothillTown_PokemonCenter_1F") == "FOOTHILL_TOWN_POKEMON_CENTER_1F")
    print("2. nome de constante (MAP_/LAYOUT_): %s" % ("OK" if ok else "FALHOU"))
    falhas += [] if ok else ["snake"]
    ok = nome_nosso(0, 4) == "RustboroPart2" and nome_nosso(0, 21) == "Route104" and nome_nosso(19, 0) == "Route104_MrBrineysHouse"
    print("3. índice do EX -> nome nosso, com o mapa inserido no meio do grupo 0 e os grupos novos: %s" % ("OK" if ok else "FALHOU"))
    falhas += [] if ok else ["nome_nosso"]
    c = classifica_script(eventos_ex(0, 59)[3][0]["u"])
    ok = c["tipo"] == "placa" and c["texto"] == ["ROUTE 103.5\\n", "{LEFT_ARROW} ROUTE 104.$"]
    print("4. placa da Route 135 lida da ROM com seta e quebra de linha: %s" % ("OK" if ok else "FALHOU %s" % c))
    falhas += [] if ok else ["texto"]
    c = classifica_script(eventos_ex(0, 59)[0][1]["script"])
    ok = c["tipo"] == "treinador" and c["id"] == 49
    print("5. trainerbattle simples do EX reconhecido (KENNETH, id 49): %s" % ("OK" if ok else "FALHOU"))
    falhas += [] if ok else ["treinador"]
    # 6. Alinhamento local na Route 110, contra a planta de ANTES da frente
    # (commit 53f37dabab, base do tronco): o EX inseriu dez colunas no meio
    # do mapa, e o rival e os três gatilhos da cena dele andam (+10,0) juntos,
    # na ordem 1, 2, 3 da esquerda para a direita; o Edwin idem.
    import subprocess
    base = "53f37dabab"
    jr = json.loads(subprocess.run(["git", "-C", RAIZ, "show", base + ":data/maps/Route110/map.json"],
                                   capture_output=True, text=True, check=True).stdout)
    lj0 = json.loads(subprocess.run(["git", "-C", RAIZ, "show", base + ":data/layouts/layouts.json"],
                                    capture_output=True, text=True, check=True).stdout)
    l0 = next(l for l in lj0["layouts"] if l and l.get("id") == jr["layout"])
    velho = subprocess.run(["git", "-C", RAIZ, "show", base + ":" + l0["blockdata_filepath"]],
                           capture_output=True, check=True).stdout
    w, h, blob, _ = planta_ex(0, 27)
    loc = alinha_local(jr, velho, l0["width"], l0["height"], blob, w, h, 0, 0)
    gat = [(c["x"] + loc[("coord_events", k)][0], c["script"]) for k, c in enumerate(jr["coord_events"])
           if c.get("script", "").startswith("Route110_EventScript_RivalTrigger")]
    riv = [k for k, o in enumerate(jr["object_events"]) if o.get("local_id") == "LOCALID_ROUTE110_RIVAL"][0]
    edw = [k for k, o in enumerate(jr["object_events"]) if o.get("script") == "Route110_EventScript_Edwin"][0]
    ok = (sorted(gat) == [(43, "Route110_EventScript_RivalTrigger1"), (44, "Route110_EventScript_RivalTrigger2"),
                          (45, "Route110_EventScript_RivalTrigger3")]
          and loc[("object_events", riv)][:2] == (10, 0) and loc[("object_events", edw)][:2] == (10, 0)
          and all(loc[("object_events", k)][:2] == (0, 0) for k, o in enumerate(jr["object_events"])
                  if o.get("script", "").startswith("Route110_EventScript_AquaGrunt")))
    print("6. alinhamento local da Route 110 (rival, gatilhos 1-3 em 43-45 na ordem, Edwin +10, Aqua parados): %s"
          % ("OK" if ok else "FALHOU %s" % gat))
    falhas += [] if ok else ["alinha_local"]
    ok = flag_valor("FLAG_HIDDEN_ITEM_ROUTE_110_REVIVE") == 0x1F4 + 0x36 and flag_valor("FLAG_HIDDEN_ITEMS_START") == 0x1F4
    print("7. flag de item escondido (base + deslocamento) resolvida para casar com o EX: %s" % ("OK" if ok else "FALHOU"))
    falhas += [] if ok else ["flag_valor"]
    c = classifica_script(eventos_ex(0, 61)[0][5]["script"])
    ok = c["tipo"] == "treinador" and c.get("duplo") and c["id"] == 113 and c["sem_dois"]
    print("8. treinador DUPLO do EX reconhecido (gêmeas da Route 137, id 113): %s" % ("OK" if ok else "FALHOU %s" % c.get("motivo")))
    falhas += [] if ok else ["duplo"]
    ok = (especie_nossa(1370) == "SPECIES_ANNIHILAPE" and especie_nossa(812) == "SPECIES_RILLABOOM"
          and especie_nossa(74) == "SPECIES_GEODUDE" and especie_nossa(906) == "SPECIES_VENUSAUR_MEGA")
    print("9. espécie do EX pelo enum conferido pelo nome (74, 812, 906 e 1370): %s" % ("OK" if ok else "FALHOU"))
    falhas += [] if ok else ["especie"]
    jr109 = json.loads(subprocess.run(["git", "-C", RAIZ, "show", base + ":data/maps/Route109/map.json"],
                                      capture_output=True, text=True, check=True).stdout)
    cas = casa_eventos(0, 26, jr109, 0, 0)
    ind = {k: v for k, v in cas["obj"].items() if v[1] in ("indice", "treinador")}
    ok = len(ind) == 24 and all(k == v[0] for k, v in ind.items())
    print("10. objetos do EX casados por índice e sprite na Route 109 (24 de 24): %s" % ("OK" if ok else "FALHOU %d" % len(ind)))
    falhas += [] if ok else ["indice"]
    js = json.loads(subprocess.run(["git", "-C", RAIZ, "show", base + ":data/maps/SlateportCity/map.json"],
                                   capture_output=True, text=True, check=True).stdout)
    cas = casa_eventos(0, 1, js, 0, 0)["warp"]
    # nosso warp 5 = Museum warp 0, nosso 7 = Museum warp 1; no EX, 4 = Museum 0 (52,26) e 6 = Museum 1 (53,26)
    ok = cas.get(4, (None,))[0] == 5 and cas.get(6, (None,))[0] == 7
    print("11. as duas portas do museu de Slateport casam pelo warp_id de destino, sem cruzar: %s" % ("OK" if ok else "FALHOU %s" % cas))
    falhas += [] if ok else ["warp_id"]
    jp = json.loads(subprocess.run(["git", "-C", RAIZ, "show", base + ":data/maps/PetalburgCity/map.json"],
                                   capture_output=True, text=True, check=True).stdout)
    cex = eventos_ex(0, 0)[2]
    cc = casa_eventos(0, 0, jp, 0, 0)["coord"]
    gin = sorted((jp["coord_events"][k]["y"], (cex[kex]["x"], cex[kex]["y"])) for kex, (k, pr) in cc.items()
                 if cex[kex]["var"] == 0x4057)
    ok = [xy for _, xy in gin] == [(8, 10), (8, 11), (8, 12), (8, 13)]
    cr = casa_eventos(0, 27, jr, 0, 0)["coord"]
    riv = {jr["coord_events"][k]["script"][-1]: eventos_ex(0, 27)[2][kex]["x"] for kex, (k, pr) in cr.items()
           if jr["coord_events"][k]["script"].startswith("Route110_EventScript_RivalTrigger")}
    ok = ok and riv == {"1": 43, "2": 44, "3": 45}
    print("12. gatilhos em grupo casam com o EX na ordem (ginásio de Petalburg em (8,10)-(8,13), rival da 110 em 43-45): %s"
          % ("OK" if ok else "FALHOU %s %s" % (gin, riv)))
    falhas += [] if ok else ["coord_grupo"]
    o = eventos_ex(0, 42)[0][10]
    ok = o["ttype"] == 0 and tipo_obj_ex(o, classifica_script(o["script"])) == "treinador"
    print("treinador que se fala (trainer_type 0, AMELIA da Route 125) entra como treinador: %s" % ("OK" if ok else "FALHOU"))
    falhas += [] if ok else ["treinador_de_conversa"]
    j114 = json.loads(subprocess.run(["git", "-C", RAIZ, "show", base + ":data/maps/Route114/map.json"],
                                     capture_output=True, text=True, check=True).stdout)
    c114 = casa_eventos(0, 31, j114, 0, 0)["obj"]
    nolan = [kex for kex, (k, pr) in c114.items() if pr == "treinador" and j114["object_events"][k]["script"] == "Route114_EventScript_Nolan"]
    vn = nomes_treinador_vanilla()
    ok = nolan == [14] and vn.get(342) == "NOLAN" and vn.get(139) == "WINSTON" and party_ex(139)["nome"].strip() == "GARTH"
    print("13. treinador vanilla que o EX mudou de lugar casa por id E nome (Nolan, 342); o 139 do EX (GARTH, reuso do WINSTON_2) não: %s"
          % ("OK" if ok else "FALHOU %s" % nolan))
    falhas += [] if ok else ["treinador"]
    print("\n%s" % ("autoteste PASSOU" if not falhas else "autoteste REPROVOU: " + ", ".join(falhas)))
    return 0 if not falhas else 1


def cmd_audita_treinadores(a):
    """Auditoria dos mapas já aplicados (pedido do condutor, 23/09/2026): todo
    TRAINER_HOENNEX_* cujo NOME é o de um treinador nosso (não HOENNEX) do MESMO
    mapa é suspeito de ser o mesmo treinador duplicado. Lê só a árvore dada."""
    repo = a.repo
    nomes = {}
    for m in re.finditer(r"^=== (TRAINER_\w+) ===\nName: ([^\n]*)", open(os.path.join(repo, "src/data/trainers.party"),
                                                                       encoding="utf-8").read(), re.M):
        nomes[m.group(1)] = m.group(2).strip().upper()
    achados = 0
    base = os.path.join(repo, "data/maps")
    for d in sorted(os.listdir(base)):
        p = os.path.join(base, d, "scripts.inc")
        if not os.path.exists(p):
            continue
        csts = set(re.findall(r"trainerbattle\w*\s+(TRAINER_\w+)", open(p, encoding="utf-8").read()))
        novos = [c for c in csts if c.startswith("TRAINER_HOENNEX_")]
        velhos = {nomes.get(c): c for c in csts if not c.startswith("TRAINER_HOENNEX_") and nomes.get(c)}
        for c in sorted(novos):
            if nomes.get(c) in velhos:
                achados += 1
                print("SUSPEITO %-28s %s (%s) tem o mesmo nome de %s" % (d, c, nomes[c], velhos[nomes[c]]))
    print("audita-treinadores: %d suspeito(s)" % achados)
    return 1 if achados else 0


def main():
    if "--autoteste" in sys.argv:
        sys.exit(autoteste())
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("lista"); p.add_argument("ex")
    p = sub.add_parser("aumenta"); p.add_argument("ex"); p.add_argument("--aplica", action="store_true")
    p.add_argument("--dx", type=int); p.add_argument("--dy", type=int)
    p.add_argument("--translacao", action="store_true", help="força translação mesmo abaixo de 75%%")
    p = sub.add_parser("conexoes"); p.add_argument("ex"); p.add_argument("--aplica", action="store_true")
    p = sub.add_parser("novo"); p.add_argument("ex"); p.add_argument("--aplica", action="store_true")
    p = sub.add_parser("eventos"); p.add_argument("ex"); p.add_argument("--lote", required=True, choices=sorted(LOTES))
    p.add_argument("--aplica", action="store_true")
    p = sub.add_parser("encontros"); p.add_argument("ex"); p.add_argument("--aplica", action="store_true")
    p = sub.add_parser("audita-treinadores", help="TRAINER_HOENNEX_* que é o mesmo treinador de um nosso do mesmo mapa")
    p.add_argument("--repo", default=RAIZ)
    a = ap.parse_args()
    if a.cmd == "audita-treinadores":
        sys.exit(cmd_audita_treinadores(a))
    if a.cmd == "encontros":
        cmd_encontros(a)
    elif a.cmd == "eventos":
        cmd_eventos(a)
    elif a.cmd == "conexoes":
        cmd_conexoes(a)
    elif a.cmd == "novo":
        cmd_novo(a)
    elif a.cmd == "lista":
        cmd_lista(a)
    elif a.cmd == "aumenta":
        cmd_aumenta(a)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
