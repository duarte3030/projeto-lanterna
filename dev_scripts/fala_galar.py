#!/usr/bin/env python3
"""FASE DE CONTEUDO DE GALAR, baldes (a) fala e (b) flag: le o roteiro da FONTE.

    python3 dev_scripts/fala_galar.py             # so a tabela dos quatro baldes
    python3 dev_scripts/fala_galar.py --gravar    # + dev_scripts/galar_roteiros.json
    python3 dev_scripts/fala_galar.py --aplicar   # + escreve mapa, script e flags
    python3 dev_scripts/fala_galar.py --demo      # autoteste com mutacao plantada

## Por que este arquivo existe

A obra G0..G5 trouxe Galar inteira como GEOMETRIA e deixou 3.257 linhas de
cobranca em `dev_scripts/fila_galar.json`, cada uma com um PONTEIRO para o
script da fonte e nada mais. Ponteiro nao e classificacao: sem abrir o
bytecode, ninguem sabe se aquele NPC diz uma frase (custo zero de estado), da
um item (custo de uma flag) ou move meio mapa (custo de var e cena). Este
arquivo abre o bytecode.

O desmontador nao tem tabela de opcode digitada a mao: ele PARSEIA
`fontes-mapas/pokefirered/asm/macros/event.inc`, que e a fonte de verdade do
motor de script do FireRed, e monta {opcode: (nome, tamanhos)}. Licao 4.11 do
ESTADO: teste (e ferramenta) que guarda copia de um fato envelhece calado.

## Os quatro baldes, e a regra de cada um

    a_fala      o script inteiro, seguindo TODOS os ramos, usa so comando sem
                estado (travar, encarar, falar, soltar, terminar) e tem UM
                texto. Vira `msgbox TEXTO, MSGBOX_NPC` (ou MSGBOX_SIGN).
    b_flag      acrescenta a isso flag PERSISTENTE e/ou a entrega padrao de
                item (`callstd STD_OBTAIN_ITEM/STD_FIND_ITEM`). Custa uma flag
                do pool novo por linha.
    c_var_cena  usa var salva, movimento, cena, batalha selvagem, `special`,
                warp, loja: precisa da maquina de vars de Galar, que ainda nao
                foi desenhada. NAO se executa aqui.
    d_treinador `trainerbattle` no bytecode ou `trainer_type` sadio na fonte.
                Fase F congelada pelo Gui (ESTADO 0.h): mede-se, nao se executa.

DECODIFICACAO INCOMPLETA CAI EM c, NUNCA EM a OU b. Se qualquer ramo do script
bate em opcode que o FireRed nao tem (o demake reaproveita espaco de dado como
se fosse codigo em alguns ponteiros), a linha e `indeciso` e fica no balde c.
Emitir fala a partir de um script que nao foi lido inteiro seria inventar.

## O texto vem da fonte, e quando nao vem o NPC continua mudo

Texto com `FD` (marcador de buffer: nome do jogador, do item, do Pokemon) ou
`FC` (codigo de controle) NAO entra: o buffer que o enche e comando de estado
que este balde nao executa, entao a frase sairia com um buraco. Essas linhas
ficam pendentes, e o NPC continua mudo. Nunca se inventa fala.

## Ordem de uso das ferramentas de Galar, que e a lei LEVA_DONA

    python3 dev_scripts/gente_galar.py  --gravar   # flags dos itens escondidos
    python3 dev_scripts/mundo_galar.py  --gravar   # mapas e scripts.inc
    python3 dev_scripts/fala_galar.py   --aplicar  # ESTE, por ultimo
    python3 dev_scripts/fila_galar.py   --gravar   # a fila reconta a verdade

`mundo_galar.py` reescreve `data/maps/Galar_*/{map.json,scripts.inc}` inteiros.
Por isso este arquivo NAO escreve dentro de `scripts.inc`: a fala mora em
`data/scripts/galar_fala.inc`, arquivo so dele, e no `map.json` ele toca apenas
os campos `script` e `flag` dos object events que ele mesmo reconheceu, mais os
bg events de placa que ele acrescenta. Rodar `mundo_galar.py` de novo apaga
esses campos; rodar este de novo os repoe, e o `--conferir` mostra a diferenca.
"""
import argparse
import collections
import glob
import json
import os
import re
import struct

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.dirname(RAIZ)
PKFR = os.path.join(FONTES, "fontes-mapas/pokefirered")
ROM_FONTE = os.path.join(FONTES,
                         "fontes-mapas/galar-swsh/ultimate-plus-v1.2.1.2.gba")
FILA = f"{RAIZ}/dev_scripts/fila_galar.json"
CENSO_GENTE = f"{RAIZ}/dev_scripts/galar_gente.json"
ROTEIROS = f"{RAIZ}/dev_scripts/galar_roteiros.json"
INC = f"{RAIZ}/data/scripts/galar_fala.inc"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
EVENT_S = f"{RAIZ}/data/event_scripts.s"

BASE = 0x08000000
MARCA_INI = "// >>> Fase de conteudo de Galar, baldes a e b (dev_scripts/fala_galar.py) >>>"
MARCA_FIM = "// <<< Fase de conteudo de Galar, baldes a e b <<<"

# Reserva pedida pela condutora: 150 flags no minimo tem que sobrar do pool
# livre para a maquina de vars/cena que ainda nao foi desenhada.
RESERVA_DE_CENA = 150

# ---------------------------------------------------------------- opcodes ---
TAM = {".byte": 1, ".2byte": 2, ".4byte": 4}
# Macros auxiliares do FireRed e o tamanho em bytes que cada uma emite.
AUX = {"map": 2, "stringvar": 1, "formatwarp": 7}
# `trainerbattle` (0x5C) tem tamanho por TIPO, e o tipo e o byte seguinte.
# Vem de asm/macros/event.inc, ramo a ramo do `.if \type == ...`.
TRAINERBATTLE = {0: 14, 1: 14, 2: 18, 3: 10, 4: 18, 5: 10, 6: 22, 7: 14,
                 8: 22, 9: 6}


def tabela_de_opcodes(caminho=None):
    """{opcode: (nome, [tamanhos dos argumentos])} lido do event.inc do FireRed.

    Macro com argumento opcional (`.ifb`) fica com o PRIMEIRO ramo: o ramo do
    `.else` e outro opcode (applymovement 0x4F contra applymovement_at 0x50).
    Macro que este parser nao consegue dimensionar entra com tamanho None e o
    desmontador para nela, em vez de chutar e sair andando por cima de dado.
    """
    txt = open(caminho or f"{PKFR}/asm/macros/event.inc").read()
    tab = {}
    for m in re.finditer(r"^\t\.macro\s+(\w+)([^\n]*)\n(.*?)^\t\.endm",
                         txt, re.S | re.M):
        nome, corpo = m.group(1), m.group(3)
        linhas = [l.split("@")[0].strip() for l in corpo.split("\n")]
        linhas = [l for l in linhas if l]
        if linhas and linhas[0].startswith(".ifb"):
            corte, prof = [], 0
            for l in linhas[1:]:
                if l.startswith(".if"):
                    prof += 1
                elif l.startswith(".endif"):
                    if prof == 0:
                        break
                    prof -= 1
                elif l.startswith(".else") and prof == 0:
                    break
                else:
                    corte.append(l)
            linhas = corte
        if not linhas or not linhas[0].startswith(".byte 0x"):
            continue
        toks = linhas[0].split()
        if len(toks) != 2:
            continue
        op = int(toks[1], 16)
        tamanhos, ok = [], True
        for l in linhas[1:]:
            p = l.split(None, 1)
            if p[0] in TAM:
                tamanhos.extend([TAM[p[0]]] *
                                ((p[1].count(",") + 1) if len(p) > 1 else 1))
            elif p[0] in AUX:
                tamanhos.append(AUX[p[0]])
            else:
                ok = False
                break
        if not ok:
            tab.setdefault(op, (nome, None))
            continue
        if op in tab and tab[op][1] is not None:
            continue
        tab[op] = (nome, tamanhos)
    return tab


# --------------------------------------------------------------- charmap ----
def charmap(caminho=None):
    """{byte: caractere} do charmap.txt DESTE repo, so as entradas de 1 byte."""
    mapa = {}
    for l in open(caminho or f"{RAIZ}/charmap.txt"):
        l = l.split("@")[0].strip()
        if "=" not in l:
            continue
        esq, dir_ = l.split("=", 1)
        by = dir_.split()
        if len(by) != 1:
            continue
        try:
            b = int(by[0], 16)
        except ValueError:
            continue
        esq = esq.strip()
        if esq.startswith("'") and esq.endswith("'") and len(esq) >= 3:
            mapa.setdefault(b, esq[1:-1])
    return mapa


CONTROLE = {0xFE: "\\n", 0xFA: "\\l", 0xFB: "\\p"}


# --------------------------------------------------------------- vocabulario -
# Comando que NAO deixa marca no save nem no mapa. Balde (a) e exatamente isto.
SEM_ESTADO = {
    "nop", "nop1", "end", "return", "goto", "call", "lock", "lockall",
    "faceplayer", "release", "releaseall", "loadword", "loadbyte", "callstd",
    "message", "waitmessage", "waitbuttonpress", "closemessage", "delay",
    "playse", "waitse", "playfanfare", "waitfanfare", "textcolor",
    "waitmoncry", "playmoncry", "showmonpic", "hidemonpic", "erasebox",
    "gotostd", "callstd_if", "gotostd_if", "goto_if", "call_if",
    "compare_var_to_value", "compare_var_to_var",
}
# Acrescenta o balde (b): flag persistente e a entrega padrao de item.
SO_FLAG = {"setflag", "clearflag", "checkflag", "removeobject", "addobject",
           "hideobject", "showobject", "setorcopyvar", "copyvarifnotzero",
           "checkitemspace", "additem", "bufferitemname", "checkitem"}
# Batalha de treinador: balde (d), Fase F congelada.
TREINADOR = {"trainerbattle"}

STD_ITEM = (0, 1)          # STD_OBTAIN_ITEM, STD_FIND_ITEM
STD_MSG = (2, 3, 4, 5, 6)  # MSGBOX_NPC, SIGN, DEFAULT, YESNO, AUTOCLOSE
# STD_OBTAIN_DECORATION/PUT_ITEM_AWAY/RECEIVED_ITEM: mexem na mochila por
# caminho que este balde nao porta. Caem em c de proposito.
STD_OUTRO = (7, 8, 9)

# Faixas do FireRed. Var >= 0x8000 e especial (EWRAM, nao salva); 0x4000-0x400F
# e temporaria de mapa. Flag < 0x20 e temporaria; >= 0x4000 e especial.
def var_salva(v):
    return 0x4010 <= v < 0x4000 + 0x100 or 0x4000 <= v < 0x8000 and v > 0x400F


def flag_salva(f):
    return 0x20 <= f < 0x4000


class Roteiro:
    """O que a leitura do bytecode achou a partir de um ponteiro da fonte."""

    def __init__(self):
        self.ops = collections.Counter()
        self.textos = []            # [(offset, tipo de callstd)]
        self.flags = []
        self.vars = []
        self.itens = []             # [(item, quantidade)]
        self.falha = None
        self.blocos = 0
        self.moldura = set()   # lock/lockall/faceplayer/release/releaseall


def desmonta(rom, tab, inicio, maxi=400):
    r = Roteiro()
    vistos, pilha = set(), [inicio]
    while pilha:
        off = pilha.pop()
        if off in vistos or not (0 <= off < len(rom)):
            continue
        vistos.add(off)
        r.blocos += 1
        palavra, ultimo_var = {}, None
        for _ in range(maxi):
            if off + 1 > len(rom):
                r.falha = r.falha or "fim de rom"
                break
            op = rom[off]
            if op not in tab:
                r.falha = r.falha or "opcode 0x%02X" % op
                break
            nome, tams = tab[op]
            if nome == "trainerbattle":
                t = rom[off + 1]
                if t not in TRAINERBATTLE:
                    r.falha = r.falha or "trainerbattle tipo %d" % t
                    break
                r.ops[nome] += 1
                off += TRAINERBATTLE[t]
                continue
            if tams is None:
                r.falha = r.falha or ("macro variavel " + nome)
                break
            args, p = [], off + 1
            for s in tams:
                if p + s > len(rom):
                    args = None
                    break
                args.append(int.from_bytes(rom[p:p + s], "little"))
                p += s
            if args is None:
                r.falha = r.falha or "fim de rom"
                break
            r.ops[nome] += 1
            if nome in ("lock", "lockall", "faceplayer", "release", "releaseall"):
                r.moldura.add(nome)
            if nome == "loadword" and len(args) == 2:
                palavra[args[0]] = args[1]
            elif nome in ("setflag", "clearflag", "checkflag") and args:
                r.flags.append(args[0])
            elif nome in ("setvar", "addvar", "subvar", "copyvar",
                          "setorcopyvar", "copyvarifnotzero") and args:
                r.vars.append(args[0])
                if args[0] in (0x8000, 0x8001) and len(args) > 1:
                    ultimo_var = (args[0], args[1])
                    if args[0] == 0x8000:
                        palavra["item"] = args[1]
                    else:
                        palavra["qtd"] = args[1]
            elif nome == "callstd" and args:
                if args[0] in STD_OUTRO:
                    r.ops["callstd_de_mochila"] += 1
                elif args[0] in STD_ITEM:
                    r.itens.append((palavra.get("item", 0),
                                    palavra.get("qtd", 1)))
                elif args[0] in STD_MSG and 0 in palavra:
                    alvo = palavra[0]
                    if BASE <= alvo < BASE + len(rom):
                        r.textos.append((alvo - BASE, args[0]))
            elif nome in ("message", "vmessage") and args:
                if BASE <= args[0] < BASE + len(rom):
                    r.textos.append((args[0] - BASE, 4))
            if nome == "goto":
                if BASE <= args[0] < BASE + len(rom):
                    pilha.append(args[0] - BASE)
                break
            if nome in ("call", "goto_if", "call_if"):
                alvo = args[-1]
                if BASE <= alvo < BASE + len(rom):
                    pilha.append(alvo - BASE)
            if nome in ("end", "return"):
                break
            off = p
        else:
            r.falha = r.falha or "script longo demais"
        del ultimo_var
    return r


def tabela_de_map_script(rom, off, maxi=16):
    """[(tipo, offset do script)] da tabela de map script do FireRed.

    A LICAO desta rodada: `map_script_ptr` do de-para NAO aponta para bytecode,
    aponta para a tabela `.byte type / .4byte script` terminada por type 0
    (asm/macros/map.inc, `map_script`). Desmontar a partir dali le a tabela como
    se fosse codigo: o primeiro byte 3 (ON_FRAME_TABLE) vira `return`, e o
    censo sai limpo e errado. Os 256 map_script da fila caem todos no balde c
    por isto, nao por medida de estado.
    """
    fora = []
    for i in range(maxi):
        p = off + i * 5
        if p + 5 > len(rom):
            break
        tipo = rom[p]
        if tipo == 0:
            break
        ptr = int.from_bytes(rom[p + 1:p + 5], "little")
        fora.append((tipo, ptr - BASE if BASE <= ptr < BASE + len(rom) else None))
    return fora


def texto(rom, cmap, off, limite=1000):
    """(texto decodificado, motivo de recusa ou None)."""
    saida = []
    for i in range(limite):
        if off + i >= len(rom):
            return "", "texto sem fim"
        b = rom[off + i]
        if b == 0xFF:
            return "".join(saida), None
        if b in (0xFC, 0xFD):
            return "", "texto com marcador 0x%02X (buffer/controle)" % b
        if b in CONTROLE:
            saida.append(CONTROLE[b])
            continue
        c = cmap.get(b)
        if c is None:
            return "", "byte 0x%02X fora do charmap" % b
        saida.append(c)
    return "", "texto sem fim"


def classifica(linha, r, textos_ok):
    """(balde, motivo). A ordem importa: d ganha de c, c ganha de b, b de a."""
    ops = set(r.ops)
    if ops & TREINADOR or linha.get("trainer_type_fonte", 0):
        return "d_treinador", "trainerbattle no bytecode" if ops & TREINADOR \
            else "trainer_type %d na fonte" % linha["trainer_type_fonte"]
    if r.falha:
        return "c_var_cena", "decodificacao incompleta: " + r.falha
    fora = ops - SEM_ESTADO - SO_FLAG
    if fora:
        return "c_var_cena", "comando de estado: " + ",".join(sorted(fora)[:4])
    if any(v not in (0x8000, 0x8001) and not (0x8000 <= v <= 0x800F)
           for v in r.vars):
        return "c_var_cena", "escreve var salva"
    if any(not flag_salva(f) for f in r.flags):
        return "c_var_cena", "mexe em flag especial/temporaria"
    if r.itens:
        # Bola de item: `finditem`/`giveitem` com item literal. Sem item
        # literal (VAR_0x8000 vindo de copyvar) nao da para escrever a linha.
        if any(i for i, _ in r.itens) and len(r.itens) == 1:
            return "b_flag", "entrega de item padrao"
        return "c_var_cena", "item vindo de var, nao de literal"
    if not textos_ok:
        return "c_var_cena", "sem texto aproveitavel"
    if len(textos_ok) != 1:
        return "c_var_cena", ("%d textos, os baldes a e b so escrevem um"
                              % len(textos_ok))
    if ops & SO_FLAG:
        return "b_flag", "uma fala atras de flag"
    return "a_fala", "so fala"


# -------------------------------------------------------------- varredura ---
def carrega():
    rom = open(ROM_FONTE, "rb").read()
    tab = tabela_de_opcodes()
    cmap = charmap()
    fila = json.load(open(FILA))["linhas"]
    return rom, tab, cmap, fila


def varre(rom, tab, cmap, fila):
    saida = []
    for l in fila:
        p = l.get("ponteiro_fonte")
        if l["tipo"] == "map_script" and p:
            tab_ms = tabela_de_map_script(rom, int(p, 16))
            saida.append(dict(
                l, balde="c_var_cena",
                motivo_balde="tabela de map script (%s): cena, precisa de var"
                             % ",".join(str(t) for t, _ in tab_ms) or "vazia",
                tipos_map_script=[t for t, _ in tab_ms],
                texto=None, tipo_msgbox=None, item=0, item_qtd=0, n_flags=0,
                bytes_texto=0))
            continue
        if not p:
            saida.append(dict(l, balde="c_var_cena",
                              motivo_balde="porta morta, e pendencia de mapa",
                              texto=None, bytes_texto=0))
            continue
        r = desmonta(rom, tab, int(p, 16))
        textos, recusa = [], None
        vistos = set()
        for off, tipo in r.textos:
            if off in vistos:
                continue
            vistos.add(off)
            t, motivo = texto(rom, cmap, off)
            if motivo:
                recusa = recusa or motivo
                continue
            textos.append((t, tipo))
        balde, motivo = classifica(l, r, textos)
        if balde in ("a_fala", "b_flag") and recusa:
            balde, motivo = "c_var_cena", recusa
        saida.append(dict(
            l, balde=balde, motivo_balde=motivo,
            texto=textos[0][0] if textos else None,
            tipo_msgbox=textos[0][1] if textos else None,
            item=r.itens[0][0] if r.itens else 0,
            item_qtd=r.itens[0][1] if r.itens else 0,
            n_flags=len(r.flags),
            moldura=sorted(r.moldura),
            bytes_texto=sum(len(t.encode()) for t, _ in textos)))
    return saida


def tabela(linhas):
    por = collections.defaultdict(collections.Counter)
    for l in linhas:
        por[l["balde"]][l["tipo"]] += 1
        por[l["balde"]]["_total"] += 1
    return por


def imprime(linhas):
    por = tabela(linhas)
    tipos = ["script_objeto", "placa", "map_script", "porta_morta"]
    print("%-14s %8s  %s" % ("balde", "total",
                             "  ".join("%14s" % t for t in tipos)))
    for b in ("a_fala", "b_flag", "c_var_cena", "d_treinador"):
        c = por[b]
        print("%-14s %8d  %s" % (b, c["_total"],
                                 "  ".join("%14d" % c[t] for t in tipos)))
    print("%-14s %8d" % ("TOTAL", len(linhas)))
    ind = [l for l in linhas
           if l["motivo_balde"].startswith("decodificacao incompleta")]
    print("\ndentro de c_var_cena: %d indecisos (bytecode nao lido inteiro)"
          % len(ind))
    ab = [l for l in linhas if l["balde"] in ("a_fala", "b_flag")]
    print("texto dos baldes a+b: %d bytes crus em %d linhas"
          % (sum(l["bytes_texto"] for l in ab), len(ab)))
    print("flags que o balde b consome: %d"
          % sum(1 for l in linhas if l["balde"] == "b_flag"))
    mot = collections.Counter(l["motivo_balde"].split(":")[0]
                              for l in linhas if l["balde"] == "c_var_cena")
    print("\nmotivos de c_var_cena:")
    for m, c in mot.most_common(12):
        print("  %5d  %s" % (c, m))


# ------------------------------------------------------------------ plano ---
TIPO_MSGBOX = {2: "MSGBOX_NPC", 3: "MSGBOX_SIGN", 4: "MSGBOX_DEFAULT",
               5: "MSGBOX_YESNO", 6: "MSGBOX_AUTOCLOSE"}
# Primeira flag da faixa de Galar ainda livre. 0x1C00-0x1C20 sao os itens
# escondidos do G4 e 0x1CFF e a FLAG_GALAR_QA_ANDAR (dona anotada em flags.h).
PRIMEIRA_FLAG_BOLA = 0x1C21
ULTIMA_FLAG_BOLA = 0x1CFE


def _gente():
    import gente_galar
    return gente_galar


def rotulo(chave, l):
    """Rotulo estavel: sai da chave da FONTE, nunca do nosso nome de mapa.

    O G3 renomeia 140 dos 438 mapas (ESTADO 0.f). Rotulo com nome nosso muda de
    nome sozinho na proxima renomeacao, e o `.inc` inteiro vira diff.
    """
    k = chave.upper()
    if l["tipo"] == "placa":
        return "GalarFala_%s_bg%d" % (k, int(l["chave"].rsplit("/", 1)[1]))
    return "GalarFala_%s_o%d" % (k, int(l["chave"].rsplit("/", 1)[1]))


def plano(linhas):
    """(falas, placas, bolas, recusados). So o que da para executar HOJE."""
    G = _gente()
    por_chave, de_para = G.carrega()
    itens_fr = G.itens_da_fonte()
    nossos = G.nossos_itens()
    falas, placas, bolas, recusa = [], [], [], []

    def nega(l, motivo):
        recusa.append({"chave": l["chave"], "balde": l["balde"], "motivo": motivo})

    for l in linhas:
        chave = l["mapa_fonte"]
        dp = de_para.get(chave)
        if dp is None:
            nega(l, "mapa da fonte nao esta no de-para do G3")
            continue
        if l["balde"] == "a_fala":
            if l["tipo"] == "script_objeto":
                if not l["no_mapa"]:
                    nega(l, "NPC nao entrou no mapa no G4")
                    continue
                falas.append(dict(l, nome=dp["nome"], rotulo=rotulo(chave, l)))
            elif l["tipo"] == "placa":
                placas.append(dict(l, nome=dp["nome"], rotulo=rotulo(chave, l)))
        elif l["balde"] == "b_flag":
            if not l["item"]:
                nega(l, "balde b sem item literal: e fala atras de flag, fica")
                continue
            if l["no_mapa"]:
                nega(l, "objeto ja entrou como NPC mudo; dar finditem o apagaria")
                continue
            nome_fr = itens_fr.get(l["item"])
            if nome_fr is None or nome_fr not in nossos:
                nega(l, "item %d da fonte sem equivalente no nosso items.h"
                        % l["item"])
                continue
            j = int(l["chave"].rsplit("/", 1)[1])
            bruto = dict(por_chave[chave]["objetos"]).get(j)
            if bruto is None:
                nega(l, "objeto foi para a sujeira do G0")
                continue
            x, y = bruto["x"], bruto["y"]
            if not G.andavel(chave, dp["w"], dp["h"], x, y):
                nega(l, "bola em tile nao andavel: o jogador nunca a alcanca")
                continue
            if (x, y) in G.warps_limpos(chave):
                nega(l, "bola em cima de warp: trancaria a porta")
                continue
            if G.tiles_de_cura().get(dp["mapa"]) == (x, y):
                nega(l, "bola em cima do tile de cura")
                continue
            bolas.append(dict(l, nome=dp["nome"], rotulo=rotulo(chave, l),
                              item_nome=nome_fr, x=x, y=y,
                              elevation=min(bruto.get("elevacao", 3), 15)))
    bolas.sort(key=lambda b: b["chave"])
    for i, b in enumerate(bolas):
        end = PRIMEIRA_FLAG_BOLA + i
        b["flag"] = "FLAG_BOLA_GALAR_%s_%02d" % (b["mapa_fonte"].upper(),
                                                 int(b["chave"].rsplit("/", 1)[1]))
        b["flag_end"] = end
    return falas, placas, bolas, recusa


# ------------------------------------------------------------------ saida ---
def corpo_inc(falas, placas, bolas):
    out = ["@ Fala de Galar, baldes (a) e (b) da fase de conteudo.",
           "@ Gerado por dev_scripts/fala_galar.py; NAO editar a mao.",
           "@ O texto vem do demake (fontes-mapas/galar-swsh), lido do bytecode",
           "@ do FireRed. Onde a fonte nao tem texto, o NPC continua mudo.",
           ""]
    por_mapa = collections.defaultdict(list)
    for l in falas + placas + bolas:
        por_mapa[(l["mapa_fonte"], l["nome"])].append(l)
    for (chave, nome) in sorted(por_mapa):
        out.append("@ ---- %s (%s) ----" % (nome, chave))
        for l in sorted(por_mapa[(chave, nome)], key=lambda z: z["chave"]):
            r = l["rotulo"]
            out.append("%s::" % r)
            if "item_nome" in l:
                qtd = l["item_qtd"] or 1
                out.append("\tfinditem %s%s" % (l["item_nome"],
                                                ", %d" % qtd if qtd != 1 else ""))
                out.append("\tend")
                out.append("")
                continue
            if l["tipo"] == "placa":
                # PLACA usa MSGBOX_SIGN e nada mais, mesmo quando a fonte poe
                # `lock/faceplayer` em volta. `faceplayer` num bg event vira
                # objeto errado (nao ha objeto falado), e `Std_MsgboxSign` ja
                # trava e solta. Mesmo molde do data/scripts/sinnoh_placas.inc.
                out.append("\tmsgbox %s_Text, MSGBOX_SIGN" % r)
                out.append("\tend")
                out.append("")
                out.append("%s_Text:" % r)
                out.append('\t.string "%s$"' % l["texto"])
                out.append("")
                continue
            mold = set(l.get("moldura") or [])
            if "lockall" in mold:
                out.append("\tlockall")
            elif "lock" in mold:
                out.append("\tlock")
            if "faceplayer" in mold:
                out.append("\tfaceplayer")
            out.append("\tmsgbox %s_Text, %s"
                       % (r, TIPO_MSGBOX.get(l["tipo_msgbox"], "MSGBOX_DEFAULT")))
            if "releaseall" in mold:
                out.append("\treleaseall")
            elif "release" in mold:
                out.append("\trelease")
            out.append("\tend")
            out.append("")
            out.append("%s_Text:" % r)
            out.append('\t.string "%s$"' % l["texto"])
            out.append("")
    return "\n".join(out) + "\n"


def bloco_de_flags(bolas):
    if not bolas:
        return ""
    out = [MARCA_INI,
           "// Uma flag por bola de item de Galar, da faixa 0x1C21 em diante",
           "// (a faixa 0x1C00+ e da obra de Galar; 0x1C00-0x1C20 sao os itens",
           "// escondidos do G4 e 0x1CFF e a FLAG_GALAR_QA_ANDAR).",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/fala_galar.py; nao editar a mao."]
    larg = max(len(b["flag"]) for b in bolas) + 2
    for b in bolas:
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // %s"
                   % (larg, b["flag"], b["flag_end"], b["item_nome"]))
    out.append(MARCA_FIM)
    return "\n".join(out) + "\n"


def substitui_bloco(texto_arq, bloco):
    """Troca o bloco marcado, ou acrescenta no fim. Idempotente por construcao."""
    i = texto_arq.find(MARCA_INI)
    if i < 0:
        if not bloco:
            return texto_arq
        return texto_arq.rstrip("\n") + "\n\n" + bloco
    j = texto_arq.find(MARCA_FIM, i)
    j = len(texto_arq) if j < 0 else j + len(MARCA_FIM) + 1
    return texto_arq[:i] + bloco + texto_arq[j:]


def casa_objeto(mapa_json, x, y):
    """Indice UNICO do object event naquele tile, ou (None, motivo).

    Casar por coordenada da FONTE, nunca por ordem: o G4 pula objeto por
    filtro, entao o indice da fonte nao e o nosso. Tile com dois objetos
    reprova em vez de escolher (licao de Oreburgh, ESTADO 0.g).
    """
    achados = [i for i, o in enumerate(mapa_json.get("object_events", []))
               if o["x"] == x and o["y"] == y]
    if len(achados) == 1:
        return achados[0], None
    return None, ("nenhum objeto nosso em (%d,%d)" % (x, y) if not achados
                  else "%d objetos no mesmo tile (%d,%d)" % (len(achados), x, y))


def aplica(falas, placas, bolas, gravar):
    """Devolve (mudancas, recusas). Sem `gravar`, so simula."""
    mudou, recusa = collections.Counter(), []
    por_nome = collections.defaultdict(lambda: {"falas": [], "placas": [],
                                                "bolas": []})
    for l in falas:
        por_nome[l["nome"]]["falas"].append(l)
    for l in placas:
        por_nome[l["nome"]]["placas"].append(l)
    for l in bolas:
        por_nome[l["nome"]]["bolas"].append(l)

    for nome, d in sorted(por_nome.items()):
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, nome)
        if not os.path.exists(caminho):
            recusa.append({"chave": nome, "motivo": "map.json nao existe"})
            continue
        doc = json.load(open(caminho))
        antes = json.dumps(doc, sort_keys=True)
        for l in d["falas"]:
            i, motivo = casa_objeto(doc, l["x"], l["y"])
            if i is None:
                recusa.append({"chave": l["chave"], "motivo": motivo})
                continue
            doc["object_events"][i]["script"] = l["rotulo"]
            mudou["fala"] += 1
        # bg de placa: append no fim, depois dos itens escondidos do G4.
        ja = {b.get("script") for b in doc.get("bg_events", [])}
        for l in sorted(d["placas"], key=lambda z: z["chave"]):
            if l["rotulo"] in ja:
                continue
            doc.setdefault("bg_events", []).append({
                "type": "sign", "x": l["x"], "y": l["y"], "elevation": 0,
                "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                "script": l["rotulo"]})
            mudou["placa"] += 1
        # bola: APPEND no fim da lista de objetos, sempre. A save guarda indice
        # de object event; objeto novo no meio renumeraria os que ja existem.
        ja_o = {o.get("script") for o in doc.get("object_events", [])}
        for l in sorted(d["bolas"], key=lambda z: z["chave"]):
            if l["rotulo"] in ja_o:
                continue
            doc.setdefault("object_events", []).append({
                "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL",
                "x": l["x"], "y": l["y"], "elevation": l["elevation"],
                "movement_type": "MOVEMENT_TYPE_NONE",
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": l["rotulo"], "flag": l["flag"]})
            mudou["bola"] += 1
        if json.dumps(doc, sort_keys=True) != antes:
            mudou["mapa"] += 1
            if gravar:
                with open(caminho, "w") as f:
                    json.dump(doc, f, indent=2, ensure_ascii=False)
                    f.write("\n")
    return mudou, recusa


def escreve_inc(falas, placas, bolas, gravar):
    corpo = corpo_inc(falas, placas, bolas)
    if gravar:
        open(INC, "w").write(corpo)
        fonte = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_fala.inc"'
        if linha not in fonte:
            open(EVENT_S, "w").write(fonte.rstrip("\n") + "\n" + linha + "\n")
    return corpo


def escreve_flags(bolas, gravar):
    bloco = bloco_de_flags(bolas)
    atual = open(FLAGS_H).read()
    novo = substitui_bloco(atual, bloco)
    if gravar and novo != atual:
        open(FLAGS_H, "w").write(novo)
    return novo


# ------------------------------------------------------------------- demo ---
def demo():
    """Autoteste. Nao grava nada, e planta mutacoes para provar que sao vistas."""
    falhas = []
    rom, tab, cmap, fila = carrega()

    # 1. a tabela de opcodes saiu do event.inc do FireRed, e nao de memoria.
    for op, nome in ((0x02, "end"), (0x05, "goto"), (0x09, "callstd"),
                     (0x0F, "loadword"), (0x4F, "applymovement"),
                     (0x53, "removeobject"), (0x5C, "trainerbattle")):
        if tab.get(op, ("?",))[0] != nome:
            falhas.append("opcode 0x%02X devia ser %s, veio %s"
                          % (op, nome, tab.get(op, ("?",))[0]))
    if len(tab) < 200:
        falhas.append("tabela de opcodes pequena demais: %d" % len(tab))

    linhas = varre(rom, tab, cmap, fila)
    falas, placas, bolas, recusa = plano(linhas)

    # 2. IDA E VOLTA DO TEXTO: reescrever o texto emitido com o NOSSO charmap
    # tem que devolver byte a byte o que a fonte tem. Sem isto, acento vira
    # outro caractere e ninguem percebe ate alguem ler a placa no jogo.
    inverso = {}
    for b, c in sorted(cmap.items()):
        inverso.setdefault(c, b)
    ctrl = {"\\n": 0xFE, "\\l": 0xFA, "\\p": 0xFB}
    ruins = 0
    for l in falas + placas:
        bruto, i, saida = l["texto"], 0, []
        while i < len(bruto):
            if bruto[i] == "\\" and bruto[i:i + 2] in ctrl:
                saida.append(ctrl[bruto[i:i + 2]])
                i += 2
                continue
            b = inverso.get(bruto[i])
            if b is None:
                ruins += 1
                break
            saida.append(b)
            i += 1
        else:
            off = int(l["ponteiro_fonte"], 16)
            achado = bytes(saida)
            # o offset do texto nao esta na linha; refaz pelo desmontador
            r = desmonta(rom, tab, off)
            alvos = [o for o, _t in r.textos]
            if not alvos or rom[alvos[0]:alvos[0] + len(achado)] != achado:
                ruins += 1
    if ruins:
        falhas.append("%d textos nao voltam byte a byte pelo charmap" % ruins)

    # 3. rotulo unico, senao o assembler junta duas falas numa so.
    rot = [l["rotulo"] for l in falas + placas + bolas]
    if len(set(rot)) != len(rot):
        falhas.append("rotulo repetido: %d de %d" % (len(rot) - len(set(rot)),
                                                     len(rot)))

    # 4. flag: dentro da faixa de Galar, sem repetir, sem pisar nas do G4 nem
    # na FLAG_GALAR_QA_ANDAR, e com a reserva de cena de pe.
    ends = [b["flag_end"] for b in bolas]
    if ends and (min(ends) < PRIMEIRA_FLAG_BOLA or max(ends) > ULTIMA_FLAG_BOLA):
        falhas.append("flag de bola fora da faixa 0x%04X-0x%04X"
                      % (PRIMEIRA_FLAG_BOLA, ULTIMA_FLAG_BOLA))
    if len(set(ends)) != len(ends):
        falhas.append("flag de bola repetida")
    livres = ULTIMA_FLAG_BOLA - PRIMEIRA_FLAG_BOLA + 1 - len(ends)
    if livres < RESERVA_DE_CENA:
        falhas.append("sobram %d flags na faixa de Galar, menos que a reserva %d"
                      % (livres, RESERVA_DE_CENA))

    # 5. bola nunca em tile que trave o jogo (o plano ja filtra; aqui e prova).
    G = _gente()
    _pc, de_para = G.carrega()
    for b in bolas:
        dp = de_para[b["mapa_fonte"]]
        if not G.andavel(b["mapa_fonte"], dp["w"], dp["h"], b["x"], b["y"]):
            falhas.append("bola %s em tile nao andavel" % b["chave"])
        if (b["x"], b["y"]) in G.warps_limpos(b["mapa_fonte"]):
            falhas.append("bola %s em cima de warp" % b["chave"])

    # 6. IDEMPOTENCIA de verdade: aplicar em cima do que ja esta gravado nao
    # muda mapa nenhum, e o .inc sai igual duas vezes.
    corpo1 = corpo_inc(falas, placas, bolas)
    corpo2 = corpo_inc(falas, placas, bolas)
    if corpo1 != corpo2:
        falhas.append("o .inc nao e estavel entre duas geracoes")
    mudou, _r = aplica(falas, placas, bolas, gravar=False)
    aplicado = os.path.exists(INC) and open(INC).read() == corpo1
    if os.path.exists(INC) and not aplicado:
        falhas.append("data/scripts/galar_fala.inc gravado NAO e o que este "
                      "gerador produz hoje (mutacao a mao, ou fonte mudou): "
                      "rode --aplicar")
    if aplicado and mudou["mapa"]:
        falhas.append("segunda passada ainda mexeria em %d mapas: nao e idempotente"
                      % mudou["mapa"])

    # 7. MUTACAO PLANTADA 1: um texto corrompido no .inc tem de ser visto.
    sujo = corpo1.replace(".string \"", ".string \"XX", 1)
    if sujo == corpo1 or sujo == corpo_inc(falas, placas, bolas):
        falhas.append("mutacao de texto no .inc nao seria vista")

    # 8. MUTACAO PLANTADA 2: dois objetos no mesmo tile tem de REPROVAR o
    # casamento por coordenada, em vez de escolher um.
    finge = {"object_events": [{"x": 5, "y": 5}, {"x": 5, "y": 5}]}
    i, motivo = casa_objeto(finge, 5, 5)
    if i is not None or "2 objetos" not in (motivo or ""):
        falhas.append("casamento por coordenada aceitou tile ambiguo")
    i, motivo = casa_objeto({"object_events": [{"x": 1, "y": 1}]}, 1, 1)
    if i != 0:
        falhas.append("casamento por coordenada perdeu o caso simples")

    # 9. MUTACAO PLANTADA 3: bloco de flags trocado tem de voltar ao lugar.
    atual = open(FLAGS_H).read()
    bloco = bloco_de_flags(bolas)
    sujo_h = substitui_bloco(atual, bloco.replace("0x1C21", "0x0001", 1))
    if substitui_bloco(sujo_h, bloco) != substitui_bloco(atual, bloco):
        falhas.append("substituicao do bloco de flags nao repoe o bloco certo")

    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    for f in falhas:
        print("  FALHA", f)
    print("  opcodes %d | linhas %d | falas %d | placas %d | bolas %d | recusas %d"
          % (len(tab), len(linhas), len(falas), len(placas), len(bolas),
             len(recusa)))
    return 1 if falhas else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gravar", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--amostra", type=int, default=0)
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    rom, tab, cmap, fila = carrega()
    linhas = varre(rom, tab, cmap, fila)
    imprime(linhas)
    falas, placas, bolas, recusa = plano(linhas)
    print("\nEXECUTAVEL HOJE: %d falas de NPC, %d placas, %d bolas de item"
          % (len(falas), len(placas), len(bolas)))
    mot = collections.Counter(r["motivo"].split(":")[0] for r in recusa)
    for m, c in mot.most_common(10):
        print("  recusado %5d  %s" % (c, m))
    if a.aplicar:
        escreve_inc(falas, placas, bolas, True)
        escreve_flags(bolas, True)
        mudou, rec = aplica(falas, placas, bolas, True)
        print("\ngravado: %d falas, %d placas, %d bolas em %d map.json"
              % (mudou["fala"], mudou["placa"], mudou["bola"], mudou["mapa"]))
        for r in rec[:10]:
            print("  nao aplicado: %s %s" % (r["chave"], r["motivo"]))
        if len(rec) > 10:
            print("  ... mais %d" % (len(rec) - 10))
    if a.amostra:
        print("\namostra do balde a:")
        for l in [x for x in linhas if x["balde"] == "a_fala"][:a.amostra]:
            print("  %-26s %-22s %r" % (l["chave"], l["mapa"], l["texto"][:90]))
        print("\namostra do balde b:")
        for l in [x for x in linhas if x["balde"] == "b_flag"][:a.amostra]:
            print("  %-26s item=%d x%d flags=%d %r" %
                  (l["chave"], l["item"], l["item_qtd"], l["n_flags"],
                   (l["texto"] or "")[:60]))
    if a.gravar:
        # O TEXTO nao entra no censo: ele ja mora em data/scripts/galar_fala.inc,
        # que e o porte de verdade. Guardar a fala duas vezes so cria duas
        # verdades e uma delas envelhece.
        linhas = [{k: v for k, v in l.items() if k != "texto"} for l in linhas]
        json.dump({"gerado_por": "dev_scripts/fala_galar.py",
                   "fonte": "fontes-mapas/galar-swsh (datamine, fora do repo)",
                   "linhas": linhas}, open(ROTEIROS, "w"), indent=1,
                  ensure_ascii=False)
        print("\ngravado %s (%d linhas)" % (ROTEIROS, len(linhas)))


if __name__ == "__main__":
    main()
