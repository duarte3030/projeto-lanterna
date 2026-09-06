#!/usr/bin/env python3
"""Anda o BYTECODE dos scripts do demake de Galar e acha quem abre porta por script.

Uso:
    python3 dev_scripts/anda_scripts_galar.py            # grava o JSON
    python3 dev_scripts/anda_scripts_galar.py --seco     # só relata
    python3 dev_scripts/anda_scripts_galar.py --demo     # autoteste, sai 1 se cair
    python3 dev_scripts/anda_scripts_galar.py --tudo     # todo warp de script, não só órfão

POR QUE ESTE SCRIPT EXISTE
==========================
`valida_conectividade.py` monta o grafo de Galar só com `warp_events` e
`connections` do `map.json`. Em pokeemerald ele também lê `scripts.inc` por
regex, mas os mapas de Galar entraram sem script nenhum: a extração trouxe
geometria, warps e objetos, e os scripts ficaram na ROM do demake. Então um
mapa que no demake só se entra por `warp` DENTRO de cena (o elevador que leva ao
andar, a porta que só abre depois da fala, o teleporte do fim de ginásio)
aparece aqui como "nenhum caminho alcança", e a causa não é porta perdida: é
porta que nunca foi olhada.

O lote AB mediu a fonte pelo lado dos `warp_events` e concluiu, certo, que a
extração é fiel e que o que falta é ENTRADA. Este script mede o lado que
faltava, e mede no bytecode, não por varredura cega de bytes: sai dos pontos de
entrada declarados de cada mapa (a tabela de map scripts, e o script de cada
objeto, placa e gatilho), anda comando a comando pelo tamanho REAL de cada
opcode, segue `goto`/`call`/`goto_if`/`call_if` e os ponteiros de continuação do
`trainerbattle`, e anota todo comando de warp que encontrar.

DE ONDE VEM A TABELA DE OPCODES, E POR QUE NÃO DA CABEÇA
========================================================
A base do demake é FireRed (BPRE), e a tabela é LIDA da fonte do pokefirered
(`fontes-mapas/pokefirered`), nunca digitada aqui:

  * `data/script_cmd_table.inc` dá a ORDEM (a posição na tabela é o opcode);
  * `asm/macros/event.inc` dá o TAMANHO de cada comando, somando as diretivas
    `.byte/.2byte/.4byte` do macro correspondente e expandindo submacros
    (`map`, `formatwarp`).

Isso importa porque os números de opcode do FireRed NÃO são os que a memória
sugere. Medido em 06/09/2026, lendo a tabela: `warp` é 0x39, `warpsilent` 0x3A,
`warpdoor` 0x3B (não existe "warpwalk"), `warphole` 0x3C (3 bytes, só o mapa),
`warpteleport` 0x3D, `setwarp` 0x3E, `setdynamicwarp` 0x3F, `setdivewarp` 0x40,
`setholewarp` 0x41, `setescapewarp` 0xC4 e `warpspinenter` 0xD1. Não há warp
nenhum na faixa 0xBE-0xBF nem em 0xC0-0xC3.

O argumento de mapa de `warp` é `map` (asm/macros/map.inc): GRUPO primeiro,
número depois, e depois o índice do warp de chegada (1 byte) e x/y (2+2). São 7
bytes de argumento, confirmados em `ScrCmd_warp` (src/scrcmd.c:719 do
pokefirered), que lê mapGroup, mapNum, warpId, x, y nessa ordem. A ordem é o
INVERSO da struct do warp de evento (número antes de grupo), e trocar as duas faz
o resultado inteiro apontar para o mapa errado sem nenhum erro visível.

Nove comandos não dão para dimensionar só pelo macro, porque o próprio macro
escolhe opcode ou tamanho conforme o argumento; eles entram na tabela
`TAMANHOS_A_MAO`, cada um com a linha da fonte que o sustenta.

O QUE É EVIDÊNCIA AQUI, E O QUE NÃO É
=====================================
Evidência: alvo de comando de warp alcançado a partir de um ponto de entrada
declarado. Não é evidência: achar dois bytes que parecem um par (grupo, mapa)
no meio da ROM, que é o que uma varredura cega faz e por isso ela não entra.

A cada script andado o script anota se ele terminou LIMPO (parou num `end`,
`return`, `gotostd`, byte de preenchimento, ou seguiu até o fim de todo ramo) ou
se DESCARRILOU (opcode fora da tabela, ponteiro fora da ROM). A taxa de
descarrilamento é a prova de que a tabela de tamanhos está certa: tabela errada
desalinha tudo e a taxa explode.

TRÊS COISAS QUE O DEMAKE FAZ E QUE PRECISARAM SER MEDIDAS (06/09/2026)
======================================================================
A primeira versão deste andador dava 26,3% de descarrilamento, e nenhuma das
três causas era tabela de opcode errada:

1. **Ponteiro de script nulo.** A extração grava `hex(ponteiro - ROM_BASE)`, e
   quando o campo do objeto vale 0x08000000 (objeto sem script, que é a maioria
   dos objetos decorativos) isso vira a string "0x0". Somar a base de volta dá
   0x08000000, que é o CABEÇALHO da ROM: o andador saía passeando pelo logotipo
   da Nintendo. Eram 526 dos 3981 pontos de entrada, e 528 dos 626
   descarrilamentos. `desloca()` corta esses, e eles não são script nenhum.
2. **`gotostd` (0x08) é salto sem volta.** Ele pula para `gStdScripts[i]` e não
   retorna, então a linha seguinte no bytecode NÃO é código. Continuar em linha
   depois dele fazia o andador entrar em texto.
3. **O demake não termina script com `end`.** Um número grande de scripts do
   autor acaba logo depois de um `callstd` ou de uma cadeia de
   `compare`+`goto_if` sem caso padrão, e o que vem a seguir é 0xFF, o byte de
   preenchimento do espaço livre. 0xFF não é opcode do FireRed (a tabela tem 214
   comandos, 0x00 a 0xD5), então aqui ele é tratado como FIM DE SCRIPT, e não
   como descarrilamento. Isso também reduz o risco na direção que importa: parar
   no 0xFF impede o andador de continuar por texto e por acaso ler um byte 0x39
   com dois bytes plausíveis atrás e INVENTAR uma porta.

Com as três, a taxa cai de 26,3% para 2,9% (100 de 3455), e o resultado em
órfãos alcançados não muda, o que é a evidência de que as correções tiraram
ruído e não conteúdo.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(os.path.dirname(RAIZ), "fontes-mapas")
FIRERED = os.path.join(FONTES, "pokefirered")
GALAR = os.path.join(FONTES, "galar-swsh")
EXTRAIDOS = os.path.join(GALAR, "extraidos-ultimate")
ROM = os.path.join(GALAR, "ultimate-plus-v1.2.1.2.gba")
CENSO = os.path.join(RAIZ, "dev_scripts/galar_mundo.json")
SAIDA = os.path.join(RAIZ, "dev_scripts/orfaos_galar_por_script.json")

ROM_BASE = 0x08000000

# Comandos de warp, por opcode. O valor e (nome, tem_alvo_completo). Quando
# tem_alvo_completo e False o comando so carrega o mapa (warphole), sem indice.
# Todos lidos de data/script_cmd_table.inc; ver o cabecalho.
WARPS = {
    0x39: "warp", 0x3A: "warpsilent", 0x3B: "warpdoor", 0x3C: "warphole",
    0x3D: "warpteleport", 0x3E: "setwarp", 0x3F: "setdynamicwarp",
    0x40: "setdivewarp", 0x41: "setholewarp", 0xC4: "setescapewarp",
    0xD1: "warpspinenter",
}
SO_MAPA = {0x3C}  # warphole: `map \map` e mais nada (asm/macros/event.inc)

# Os nove que o macro nao dimensiona sozinho, com a fonte de cada um.
TAMANHOS_A_MAO = {
    # applymovement escolhe o OPCODE pelo argumento opcional `map`:
    # sem map vira 0x4f (1+2+4), com map vira 0x50 (1+2+4+2).
    0x4F: 7, 0x50: 9,
    # waitmovement / removeobject / addobject: mesma dupla, sem e com map.
    0x51: 3, 0x52: 5,
    0x53: 3, 0x54: 5,
    0x55: 3, 0x56: 5,
}
# trainerbattle (0x5C): 6 bytes de cabecalho (opcode, tipo, treinador:2,
# local_id:2) e depois um numero de ponteiros que depende do TIPO. Valores de
# include/constants/battle_setup.h do pokefirered.
TRAINERBATTLE = {
    0: (2, None), 1: (3, 2), 2: (3, 2), 3: (1, None), 4: (3, None),
    5: (2, None), 6: (4, 3), 7: (3, None), 8: (4, 3), 9: (2, None),
}
TRAINERBATTLE_CAB = 6

IR = {0x04: "call", 0x05: "goto"}          # opcode -> ponteiro em +1
IR_COND = {0x06: "goto_if", 0x07: "call_if"}  # ponteiro em +2
PARA = {0x02, 0x03, 0x08, 0x0C, 0x0D}      # end, return, gotostd, returnram, endram
PREENCHIMENTO = 0xFF

# Tipos de map script que apontam para TABELA de (var, valor, script) em vez de
# script direto (include/constants/map_scripts.h).
MAP_SCRIPT_TABELA = {2, 4}


# ------------------------------------------------------- tabela de opcodes --

def tabela_de_opcodes():
    """opcode -> (nome, tamanho), lido do pokefirered. Nunca digitado aqui."""
    tab = open(os.path.join(FIRERED, "data/script_cmd_table.inc")).read()
    nomes = re.findall(r"\.4byte\s+ScrCmd_(\w+)", tab)
    macros = {}
    for arq in ("asm/macros/event.inc", "asm/macros/map.inc"):
        t = open(os.path.join(FIRERED, arq)).read()
        for m in re.finditer(r"^\s*\.macro\s+(\w+)([^\n]*)\n(.*?)^\s*\.endm",
                             t, re.S | re.M):
            macros.setdefault(m.group(1), m.group(3))
    largura = {".byte": 1, ".2byte": 2, ".4byte": 4, ".short": 2,
               ".hword": 2, ".word": 4, ".int": 4, ".space": 1}

    def limpa(corpo):
        return [l for l in (x.split("@")[0].strip() for x in corpo.split("\n")) if l]

    def ramo(linhas, i, prof):
        """Soma ate encontrar .else/.endif/fim. Devolve (tamanho|None, i)."""
        tam = 0
        while i < len(linhas):
            l = linhas[i]
            d = l.split()[0]
            if d.startswith(".if"):
                sub, i = bloco(linhas, i + 1, prof + 1)
                if not isinstance(sub, int):
                    return None, i
                tam += sub
                continue
            if d in (".else", ".elseif", ".endif"):
                return tam, i
            i += 1
            if d in largura:
                args = [x for x in l[len(d):].split(",") if x.strip()]
                if d == ".space":
                    tam += int(args[0]) if args and args[0].strip().isdigit() else 1
                else:
                    tam += largura[d] * max(len(args), 1)
            elif d in macros and prof < 8:
                sub = mede(macros[d], prof + 1)
                if not isinstance(sub, int):
                    return None, i
                tam += sub
            elif d.startswith("."):
                continue
            else:
                return None, i
        return tam, i

    def bloco(linhas, i, prof):
        vistos = []
        while True:
            t, i = ramo(linhas, i, prof)
            vistos.append(t)
            if i >= len(linhas):
                return None, i
            d = linhas[i].split()[0]
            i += 1
            if d == ".endif":
                break
        reais = [x for x in vistos if x is not None]
        # Ramos de tamanhos diferentes = comando de tamanho variavel: recusa,
        # para cair na TAMANHOS_A_MAO em vez de chutar um dos ramos.
        if not reais or len(set(reais)) != 1:
            return None, i
        return reais[0], i

    def mede(corpo, prof=0):
        linhas = limpa(corpo)
        t, i = ramo(linhas, 0, prof)
        return t if i >= len(linhas) else None

    tabela = {}
    for op, nome in enumerate(nomes):
        t = mede(macros[nome]) if nome in macros else None
        if isinstance(t, int):
            tabela[op] = (nome, t)
        elif op in TAMANHOS_A_MAO:
            tabela[op] = (nome, TAMANHOS_A_MAO[op])
        elif op != 0x5C:  # trainerbattle e tratado no andador
            tabela[op] = (nome, None)
    tabela[0x5C] = ("trainerbattle", None)
    return tabela


# ------------------------------------------------------------- o andador ----

class Andador:
    def __init__(self, rom, tabela):
        self.rom = rom
        self.tab = tabela
        self.fim = ROM_BASE + len(rom)

    def valido(self, p):
        return ROM_BASE <= p < self.fim

    def u8(self, o):
        return self.rom[o]

    def u16(self, o):
        return struct.unpack_from("<H", self.rom, o)[0]

    def u32(self, o):
        return struct.unpack_from("<I", self.rom, o)[0]

    def anda(self, inicio, limite=4000):
        """Devolve (achados, estado, motivo).

        achados: lista de (nome do comando, grupo, mapa, índice de chegada).
        estado: 'limpo' quando todo ramo terminou num comando de parada, num
        byte de preenchimento, ou num endereço já andado; 'descarrilou' quando
        encontrou opcode fora da tabela ou ponteiro fora da ROM. motivo diz
        QUAL das duas, para a medição poder separar erro de tabela de sujeira
        da fonte. Não segue o mesmo endereço duas vezes.
        """
        achados, vistos, pilha = [], set(), [inicio]
        estado, motivo = "limpo", None
        passos = 0

        def cai(razao):
            return "descarrilou", razao

        while pilha:
            p = pilha.pop()
            if not self.valido(p) or p in vistos:
                if not self.valido(p):
                    estado, motivo = cai(motivo or "ponteiro fora da ROM")
                continue
            o = p - ROM_BASE
            while True:
                passos += 1
                if passos > limite:
                    estado, motivo = cai(motivo or "limite de passos")
                    break
                if o + 1 > len(self.rom) or (o + ROM_BASE) in vistos:
                    break
                vistos.add(o + ROM_BASE)
                op = self.rom[o]
                if op == PREENCHIMENTO:
                    break          # espaço livre: fim do script do autor
                if op not in self.tab:
                    estado, motivo = cai(motivo or "opcode 0x%02X fora da tabela" % op)
                    break
                nome, tam = self.tab[op]
                if op in WARPS and o + 4 <= len(self.rom):
                    grupo, num = self.rom[o + 1], self.rom[o + 2]
                    warp = None if op in SO_MAPA else self.rom[o + 3]
                    achados.append((nome, grupo, num, warp))
                if op == 0x5C:  # trainerbattle: tamanho pelo tipo
                    tipo = self.rom[o + 1]
                    if tipo not in TRAINERBATTLE:
                        estado, motivo = cai(motivo or "trainerbattle tipo %d" % tipo)
                        break
                    n_ptr, cont = TRAINERBATTLE[tipo]
                    tam = TRAINERBATTLE_CAB + 4 * n_ptr
                    if cont is not None:
                        alvo = self.u32(o + TRAINERBATTLE_CAB + 4 * cont)
                        if self.valido(alvo):
                            pilha.append(alvo)
                if tam is None:
                    estado, motivo = cai(motivo or "comando sem tamanho: %s" % nome)
                    break
                if op in IR or op in IR_COND:
                    desl = 1 if op in IR else 2
                    alvo = self.u32(o + desl)
                    if not self.valido(alvo):
                        estado, motivo = cai(motivo or "goto/call fora da ROM")
                        break
                    pilha.append(alvo)
                    if op == 0x05:  # goto incondicional: nao ha linha seguinte
                        break
                if op in PARA:
                    break
                o += tam
        return achados, estado, motivo


# ------------------------------------------------------------- a medicao ----

def desloca(bruto):
    """Ponteiro de ROM a partir do campo da extracao, ou None.

    A extração grava `hex(ponteiro - ROM_BASE)`, então aqui só somamos a base
    de volta. O campo vale None quando o ponteiro não cabia na ROM, e vale
    "0x0" quando o ponteiro era 0x08000000, que é o CABEÇALHO da ROM, não
    script nenhum: os dois casos são entrada morta e saem daqui. Sem este
    filtro o andador passeia pelo logotipo da Nintendo e conta como script
    descarrilado (medido em 06/09/2026: 528 dos 626 descarrilamentos).
    """
    if not bruto:
        return None
    v = int(bruto, 16)
    return None if v == 0 else v + ROM_BASE


def pontos_de_entrada(and_, comp, src):
    """(rótulo, endereço) de cada script de UM mapa da fonte."""
    pts = []
    p = desloca((comp or {}).get("map_script_ptr"))
    if p and and_.valido(p):
        pts += tabela_de_map_scripts(and_, p - ROM_BASE)
    for o in src.get("objetos") or []:
        p = desloca(o.get("script"))
        if p:
            pts.append(("objeto %d" % o["local_id"], p))
    for c in src.get("coords") or []:
        p = desloca(c.get("script"))
        if p:
            pts.append(("gatilho (%d,%d)" % (c["x"], c["y"]), p))
    for b in src.get("bg_events") or []:
        p = desloca(b.get("script"))
        if p:
            pts.append(("placa (%d,%d)" % (b["x"], b["y"]), p))
    return [(r, p) for r, p in pts if and_.valido(p)]


def tabela_de_map_scripts(and_, base):
    """A tabela de map scripts: pares (tipo, ponteiro) ate um tipo 0.

    Tipo 2 e 4 (ON_FRAME_TABLE, ON_WARP_INTO_MAP_TABLE) apontam para uma
    sub-tabela de (var:2, valor:2, script:4) terminada por var 0.
    """
    pts = []
    o = base
    for _ in range(16):
        if o + 5 > len(and_.rom):
            break
        tipo = and_.rom[o]
        if tipo == 0 or tipo > 7:
            break
        p = and_.u32(o + 1)
        o += 5
        if not and_.valido(p):
            continue
        if tipo in MAP_SCRIPT_TABELA:
            q = p - ROM_BASE
            for _ in range(16):
                if q + 8 > len(and_.rom) or and_.u16(q) == 0:
                    break
                alvo = and_.u32(q + 4)
                if and_.valido(alvo):
                    pts.append(("cena (map script %d)" % tipo, alvo))
                q += 8
        else:
            pts.append(("cena (map script %d)" % tipo, p))
    return pts


def classe_do_rotulo(rotulo):
    if rotulo.startswith("cena"):
        return "cena (map script)"
    if rotulo.startswith("gatilho"):
        return "gatilho de coordenada"
    if rotulo.startswith("placa"):
        return "placa"
    return "objeto (NPC, porta de script)"


def carrega_orfaos():
    """Os órfãos de Galar de HOJE, pela regra de valida_conectividade.py."""
    sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    import liga_orfaos_galar
    return set(liga_orfaos_galar.orfaos_hoje())


def mede(tudo=False):
    cen = json.load(open(CENSO, encoding="utf-8"))
    dp = cen["de_para"]
    id_de = {k: v["mapa"] for k, v in dp.items()}
    nome_de = {k: v["nome"] for k, v in dp.items()}
    mapas = json.load(open(os.path.join(EXTRAIDOS, "mapas.json"), encoding="utf-8"))
    comp = json.load(open(os.path.join(EXTRAIDOS, "complemento.json"), encoding="utf-8"))
    src = {}
    for g in mapas:
        for i, m in enumerate(g["mapas"]):
            src["g%02dm%02d" % (g["grupo"], i)] = m

    rom = open(ROM, "rb").read()
    and_ = Andador(rom, tabela_de_opcodes())
    orfaos = carrega_orfaos()

    estados = collections.Counter()
    motivos = collections.Counter()
    n_scripts = 0
    achados = []   # (origem_fonte, rotulo, comando, destino_fonte, warp)
    for f, v in sorted(dp.items()):
        for rotulo, p in pontos_de_entrada(and_, comp.get(f), src[f]):
            n_scripts += 1
            res, estado, motivo = and_.anda(p)
            estados[estado] += 1
            if motivo:
                motivos[motivo] += 1
            for nome, grupo, num, warp in res:
                d = "g%02dm%02d" % (grupo, num)
                if d in dp:
                    achados.append((f, rotulo, nome, d, warp))

    por_alvo = collections.defaultdict(list)
    for f, rotulo, cmd, d, warp in achados:
        alvo = id_de[d]
        if not tudo and alvo not in orfaos:
            continue
        por_alvo[alvo].append({
            "origem": id_de[f], "origem_dir": nome_de[f],
            "origem_orfa": id_de[f] in orfaos,
            "script": rotulo, "classe": classe_do_rotulo(rotulo),
            "comando": cmd, "warp_de_chegada": warp,
        })
    alcancados = sorted(k for k in por_alvo if k in orfaos)
    de_vivo = sorted(k for k in alcancados
                     if any(not x["origem_orfa"] for x in por_alvo[k]))
    return {
        "gerado_por": "dev_scripts/anda_scripts_galar.py",
        "fonte": os.path.relpath(ROM, os.path.dirname(RAIZ)),
        "scripts_andados": n_scripts,
        "scripts_limpos": estados["limpo"],
        "scripts_descarrilados": estados["descarrilou"],
        "motivos_de_descarrilamento": dict(motivos.most_common()),
        "orfaos_hoje": len(orfaos),
        "orfaos_alcancados_por_script": len(alcancados),
        "orfaos_alcancados_de_mapa_vivo": len(de_vivo),
        "orfaos_sem_entrada_nenhuma": sorted(set(orfaos) - set(alcancados)),
        "alvos_no_arquivo": sorted(por_alvo),
        "orfaos": {k: v for k, v in sorted(por_alvo.items())},
    }, orfaos


def relata(dados, orfaos):
    print("scripts andados: %d  (limpos %d, descarrilados %d, %.1f%%)"
          % (dados["scripts_andados"], dados["scripts_limpos"],
             dados["scripts_descarrilados"],
             100.0 * dados["scripts_descarrilados"] / max(dados["scripts_andados"], 1)))
    for k, n in list(dados["motivos_de_descarrilamento"].items())[:6]:
        print("   %4d  %s" % (n, k))
    print("órfãos de Galar hoje: %d" % dados["orfaos_hoje"])
    print("órfãos alcançados por warp de script: %d"
          % dados["orfaos_alcancados_por_script"])
    print("  dos quais a origem é mapa VIVO: %d"
          % dados["orfaos_alcancados_de_mapa_vivo"])
    print("  só por mapa que também é órfão: %d"
          % (dados["orfaos_alcancados_por_script"]
             - dados["orfaos_alcancados_de_mapa_vivo"]))
    classes = collections.Counter()
    comandos = collections.Counter()
    for alvo, v in dados["orfaos"].items():
        if alvo not in orfaos:
            continue
        for x in v:
            classes[x["classe"]] += 1
            comandos[x["comando"]] += 1
    print("por classe de script (arestas que caem em órfão):")
    for k, n in classes.most_common():
        print("  %4d  %s" % (n, k))
    print("por comando:")
    for k, n in comandos.most_common():
        print("  %4d  %s" % (n, k))
    print("órfãos SEM entrada nenhuma (nem warp, nem script): %d"
          % len(dados["orfaos_sem_entrada_nenhuma"]))
    if len(dados["alvos_no_arquivo"]) != dados["orfaos_alcancados_por_script"]:
        print("(--tudo: %d mapas no total são alvo de warp de script)"
              % len(dados["alvos_no_arquivo"]))


def rom_sintetica():
    """Uma ROM de mentira com bytecode escrito a mao, para provar o ANDADOR.

    Não usa a ROM do demake de propósito: aqui o gabarito é conhecido, então um
    erro de caminhada aparece como diferença, e não como número plausível.

      0x100  lock
             setvar 0x8000, 5
             call_if 1 -> 0x180        (sub-rotina, tem que ser andada)
             goto_if 1 -> 0x1C0        (ramo condicional, tem que ser andado)
             warp grupo 3 mapa 7 warp 2
             gotostd 5                 (salto sem volta: PARA aqui)
             warp grupo 9 mapa 9 warp 9   <- ARMADILHA, nao pode ser lida
      0x180  warpdoor grupo 4 mapa 1 warp 0 ; return
      0x1C0  warphole grupo 5 mapa 6   (3 bytes, sem índice de chegada)
             end ; 0xFF de preenchimento
      0x300  goto -> 0x08009000        (fora da ROM: tem que descarrilar)
      0x320  0xD6                      (opcode fora da tabela: descarrilar)
    """
    rom = bytearray(b"\xFF" * 0x400)

    def ptr(a):
        return struct.pack("<I", ROM_BASE + a)

    def poe(off, b):
        rom[off:off + len(b)] = b

    poe(0x100,
        b"\x6a"                                   # lock
        + b"\x16\x00\x80\x05\x00"                # setvar
        + b"\x07\x01" + ptr(0x180)                # call_if
        + b"\x06\x01" + ptr(0x1C0)                # goto_if
        + b"\x39\x03\x07\x02\x00\x00\x00\x00"     # warp 3/7/2
        + b"\x08\x05"                             # gotostd 5
        + b"\x39\x09\x09\x09\x00\x00\x00\x00")    # armadilha
    poe(0x180, b"\x3b\x04\x01\x00\x00\x00\x00\x00" + b"\x03")
    poe(0x1C0, b"\x3c\x05\x06" + b"\x02")
    poe(0x300, b"\x05" + struct.pack("<I", 0x08009000))
    poe(0x320, b"\xd6")
    return bytes(rom)


def autoteste():
    falhou = []

    def confere(o_que, deu, esperado):
        ok = deu == esperado
        print("  %-58s %s  (%s)" % (o_que, "OK" if ok else "CAIU", deu))
        if not ok:
            falhou.append(o_que)

    tab = tabela_de_opcodes()
    # Os tamanhos que o cabecalho afirma, conferidos contra a fonte lida.
    confere("0x39 e warp", tab[0x39], ("warp", 8))
    confere("0x3B e warpdoor (nao 'warpwalk')", tab[0x3B][0], "warpdoor")
    confere("0x3C e warphole, 3 bytes", tab[0x3C], ("warphole", 3))
    confere("0xC4 e setescapewarp", tab[0xC4][0], "setescapewarp")
    confere("0xD1 e warpspinenter", tab[0xD1][0], "warpspinenter")
    confere("nao ha warp em 0xBE/0xBF",
            sorted(op for op in (0xBE, 0xBF) if op in WARPS), [])
    confere("0x05 e goto de 5 bytes", tab[0x05], ("goto", 5))
    confere("0x08 gotostd é salto sem volta", 0x08 in PARA, True)
    confere("a tabela do FireRed tem 214 comandos, 0x00 a 0xD5",
            (len(tab), max(tab)), (214, 0xD5))
    confere("0xFF não é opcode do FireRed", 0xFF in tab, False)
    confere("todo opcode da tabela tem tamanho",
            sorted(op for op, (n, t) in tab.items() if t is None), [0x5C])

    # ---- o andador, contra bytecode sintetico de gabarito conhecido --------
    sin = Andador(rom_sintetica(), tab)
    achados, estado, motivo = sin.anda(ROM_BASE + 0x100)
    confere("sintético: o ramo principal termina limpo", estado, "limpo")
    confere("sintético: acha os 3 warps, e só eles",
            sorted(achados),
            sorted([("warp", 3, 7, 2), ("warpdoor", 4, 1, 0),
                    ("warphole", 5, 6, None)]))
    confere("sintético: não lê o warp depois do gotostd",
            [a for a in achados if a[1] == 9], [])
    confere("sintético: ponteiro fora da ROM descarrilha",
            sin.anda(ROM_BASE + 0x300)[1], "descarrilou")
    confere("sintético: opcode fora da tabela descarrilha",
            Andador(rom_sintetica(), tab).anda(ROM_BASE + 0x320)[1], "descarrilou")
    confere("sintético: preenchimento 0xFF é fim, não queda",
            Andador(rom_sintetica(), tab).anda(ROM_BASE + 0x1C4)[1], "limpo")
    confere("desloca() recusa ponteiro nulo e ausente",
            (desloca("0x0"), desloca(None), desloca("0x100")),
            (None, None, ROM_BASE + 0x100))

    # ---- a prova de alinhamento na ROM de verdade --------------------------
    dados, orfaos = mede()
    ruim = 100.0 * dados["scripts_descarrilados"] / max(dados["scripts_andados"], 1)
    print("  %-58s %s  (%.1f%%)"
          % ("taxa de descarrilamento abaixo de 5%",
             "OK" if ruim < 5 else "CAIU", ruim))
    if ruim >= 5:
        falhou.append("taxa de descarrilamento")
    confere("andou pelo menos 1000 scripts", dados["scripts_andados"] >= 1000, True)
    print("\n%s" % ("autoteste: tudo de pé" if not falhou
                     else "autoteste: %d caiu" % len(falhou)))
    return 1 if falhou else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seco", action="store_true", help="não escreve o JSON")
    ap.add_argument("--demo", action="store_true", help="autoteste")
    ap.add_argument("--autoteste", action="store_true", help="autoteste")
    ap.add_argument("--tudo", action="store_true",
                    help="registra todo warp de script, não só o que cai em órfão")
    args = ap.parse_args()
    if args.demo or args.autoteste:
        return autoteste()
    dados, orfaos = mede(tudo=args.tudo)
    relata(dados, orfaos)
    if not args.seco and not args.tudo:
        with open(SAIDA, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print("\ngravado: %s" % os.path.relpath(SAIDA, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
