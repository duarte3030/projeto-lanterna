#!/usr/bin/env python3
"""FASE DE CONTEÚDO DE GALAR, blocos c1 (faixa de vars) e c3 (map script).

    python3 dev_scripts/cenas_galar.py            # só mede e relata
    python3 dev_scripts/cenas_galar.py --aplicar  # escreve vars.h, flags.h, .inc, mapas
    python3 dev_scripts/cenas_galar.py --demo     # autoteste com mutação plantada

## O que a MEDIÇÃO derrubou antes de uma linha ser escrita

O `PLANO-CONTEUDO-GALAR.md` (rascunho de 21/08) chama os 144 map_scripts de
tabela `(3,)` de "ON_FRAME_TABLE puro" e desenha a fase inteira em cima disso.
**Está errado, e o erro é de constante, não de contagem.** Em
`fontes-mapas/pokefirered/include/constants/map_scripts.h`:

    MAP_SCRIPT_ON_LOAD                 1
    MAP_SCRIPT_ON_FRAME_TABLE          2      <- a tabela `var, valor, script`
    MAP_SCRIPT_ON_TRANSITION           3      <- bytecode solto, os "144"
    MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE  4      <- também tabela

Ou seja: os 144 são ON_TRANSITION, que é bytecode e NÃO tem var nem valor. Quem
pede `map_script_2 VAR, valor, Script` são os tipos 2 e 4, e deles a fonte tem
**19 tabelas em 17 mapas**, não 144. Medido aqui, não lembrado:
`--demo` refaz a contagem e reprova se ela mudar calada.

Consequência de orçamento, que é o que a condutora pediu para medir antes de
comprometer a faixa: **o desenho "uma var por MAPA" custa uma casa por mapa com
tabela de tipo 2/4 que passe no filtro, e não 144.** A faixa de 150 vars livres
sobra inteira; o gargalo desta fase nunca foi var.

## O segundo achado, e ele é o que esvazia o bloco c3

Dos 144 ON_TRANSITION, **139 não escrevem var nenhuma** e 77 são literalmente
`setflag 0x918; setflag 0x90E; release; end`. As quatro flags que dominam
(0x90D, 0x90E, 0x918, 0x91A) estão ACIMA de `FLAGS_COUNT` do FireRed (0x900), ou
seja são flags que o demake acrescentou ao próprio motor, e o varrimento cru da
ROM mostra que **0x90E nunca aparece num `checkflag` de script nenhum** (98
`setflag`, 97 `clearflag`, ZERO `checkflag`): quem lê essas flags é código C do
hack, que a nossa ROM não tem. Portá-las seria acender uma lâmpada sem fio.
Elas saem com motivo contado, nunca com fala inventada.

## O que ENTRA, então

Só cena que a nossa ROM consegue reproduzir com o mesmo efeito. O filtro é
mecânico e cada recusa é contada por motivo:

  - opcode que o desmontador não leu inteiro (nunca se emite script pela metade);
  - `special`/`specialvar`: o índice do FireRed não é o nosso;
  - id de objeto local que o G4 não pôs no mapa (mover o NPC errado é pior que
    não mover nenhum): o de-para de id sai da COORDENADA, como o `fala_galar`
    já fazia, nunca da ordem;
  - `MOVEMENT_ACTION_*` que existe na fonte e não aqui (as tabelas divergem: o
    FRLG tem `FACE_*_FAST` em 0x4-0x7 e tudo depois anda quatro casas). A
    tradução é por NOME, resolvida dos dois headers, nunca por valor;
  - flag da fonte que não é `flag_fonte` de nenhum objeto importado (é flag de
    motor do demake, ver acima);
  - texto que o nosso charmap não devolve byte a byte;
  - warp: o destino depende do de-para de mapa, que é outra obra.

## DECISÃO declarada, para ninguém achar que foi descuido

Cena que faz `removeobject` de um objeto cuja FONTE declara flag de esconder
(`flag_fonte` no censo do G4) sai com `setflag <essa flag>` imediatamente antes
do `removeobject`. Motivo: `removeobject` só vale para a sessão de mapa, e sem a
flag o NPC volta a estar de pé na próxima entrada, depois de a cena já ter dito
que ele foi embora. A flag é a que a PRÓPRIA fonte pendurou no objeto; o que se
acrescenta é o momento de acendê-la. Está anotado por linha no `.inc`.

## Ordem de uso (lei LEVA_DONA), com este arquivo no fim

    python3 dev_scripts/gente_galar.py  --gravar
    python3 dev_scripts/mundo_galar.py  --gravar
    python3 dev_scripts/fala_galar.py   --aplicar
    python3 dev_scripts/cenas_galar.py  --aplicar   # ESTE
    python3 dev_scripts/fila_galar.py   --gravar

`mundo_galar.py` reescreve `data/maps/Galar_*/scripts.inc` INTEIRO, e é lá que
mora a tabela `Galar_X_MapScripts` que o `mapjson` exige por mapa (o gerador de
mapa só entende `shared_scripts_map`, não aceita apontar para um rótulo
qualquer, medido em `tools/mapjson/mapjson.cpp`). Por isso este arquivo é o
único de Galar que escreve dentro de `scripts.inc`, e só nos mapas que recebem
cena; o CORPO das cenas mora em `data/scripts/galar_cenas.inc`, que é só dele.
Rodar `mundo_galar.py` de novo apaga a tabela; rodar este de novo a repõe.
"""
import argparse
import collections
import json
import os
import re
import shutil
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import fala_galar as FALA                     # noqa: E402
import guarda_colisao_vars as GUARDA          # noqa: E402
import flags_livres as FL                      # noqa: E402

FONTES = os.path.dirname(RAIZ)
PKFR = os.path.join(FONTES, "fontes-mapas/pokefirered")
INC = f"{RAIZ}/data/scripts/galar_cenas.inc"
VARS_H = f"{RAIZ}/include/constants/vars.h"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
BASE = FALA.BASE

MARCA_VAR_INI = ("// >>> Fase de conteudo de Galar, bloco c1: vars de cena "
                 "(dev_scripts/cenas_galar.py) >>>")
MARCA_VAR_FIM = "// <<< Fase de conteudo de Galar, bloco c1 <<<"
MARCA_FLAG_INI = ("// >>> Fase de conteudo de Galar, bloco c3: flags de esconder "
                  "(dev_scripts/cenas_galar.py) >>>")
MARCA_FLAG_FIM = "// <<< Fase de conteudo de Galar, bloco c3 <<<"

# Orçamento da condutora (21/08/2026): no máximo 120 vars nesta fase, com 30 de
# reserva por cima. A faixa de onde elas saem é MEDIDA, nunca escrita aqui.
ORCAMENTO_VARS = 120
RESERVA_VARS = 30

# Flags de esconder de Galar: a mesma faixa 0x1C00+ da obra, depois do que o G4
# (0x1C00-0x1C20), o fala_galar (0x1C21-0x1C58) e a FLAG_GALAR_QA_ANDAR (0x1CFF)
# já tomaram. Começa folgado depois da última bola para não brigar com uma leva
# nova de bolas.
PRIMEIRA_FLAG_CENA = 0x1C80
ULTIMA_FLAG_CENA = 0x1CFE

# Tipos de map script do FireRed, lidos do header da fonte em vez de digitados.
TIPOS_TABELA = (2, 4)      # os que pedem `map_script_2 var, valor, script`

# BLOCO c6, 06/09/2026 (lote C da onda 1 da Frente A). Até aqui só o tipo 3
# entrava como bytecode direto, e os tipos 1, 5 e 7 saíam com o motivo "fora do
# bloco c3", que era ESCOPO e não impossibilidade: `include/constants/map_scripts.h`
# tem os MESMOS sete números nos dois motores (conferido linha a linha contra
# `fontes-mapas/pokefirered/include/constants/map_scripts.h` em 06/09/2026), então
# o tipo atravessa 1:1 e o que precisa de julgamento é o CORPO, não o número.
TIPOS_DIRETOS = (1, 3, 5, 7)
MACRO_DIRETO = {1: "MAP_SCRIPT_ON_LOAD", 3: "MAP_SCRIPT_ON_TRANSITION",
                5: "MAP_SCRIPT_ON_RESUME", 7: "MAP_SCRIPT_ON_RETURN_TO_FIELD"}
MACRO_TABELA = {2: "MAP_SCRIPT_ON_FRAME_TABLE",
                4: "MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE"}

# ON_LOAD roda ANTES de o mapa ser desenhado e ON_RESUME roda no fim da carga e
# a cada volta ao campo (ver o comentário do próprio map_scripts.h). Nenhum dos
# dois tem caixa de fala, câmera nem jogador andando: é lugar de arrumar o
# cenário, não de contar cena. Comando que precisa do campo RODANDO recusa a
# cena inteira nesses dois tipos, em vez de virar defeito calado na tela de
# carregamento. O tipo 7 (ON_RETURN_TO_FIELD) entra na mesma lei pelo mesmo
# motivo: ele roda logo depois do ON_RESUME.
TIPOS_QUIETOS = (1, 5, 7)
PRECISA_DO_CAMPO = {"lock", "lockall", "release", "releaseall", "faceplayer",
                    "applymovement", "waitmovement", "fadescreen", "delay",
                    "waitstate", "closemessage", "waitmessage",
                    "waitbuttonpress", "playse", "waitse", "playfanfare",
                    "waitfanfare", "playbgm", "fadedefaultbgm", "callstd",
                    "hidemonpic", "waitmoncry", "waitdooranim", "doweather",
                    "turnobject"}

# Byte de enchimento de espaço livre da ROM do FireRed.
ENCHIMENTO = 0xFF

# DE-PARA de `special`: nome do FireRed -> nome daqui, para a MESMA função.
# Conferido corpo a corpo em 22/08/2026 pelo bloco c4a, e não por semelhança de
# nome. Ele MOROU em `dev_scripts/objetos_galar.py` até 06/09/2026 e subiu para
# cá quando o c6 precisou do mesmo de-para em map script: duas cópias do mesmo
# dicionário em dois arquivos é divergência esperando acontecer.
#   StartLegendaryBattle    -> BattleSetup_StartLegendaryBattle (src/battle_setup.c)
#   GetPartyMonSpecies      -> ScriptGetPartyMonSpecies         (src/field_specials.c)
#   GetPokedexCount         -> GetFrlgPokedexCount              (src/birch_pc.c, cópia
#                              linha a linha do prof_pc.c do FR)
#   SelectMoveDeleterMove   -> MoveDeleterChooseMoveToForget    (src/party_menu.c)
# Os no-ops de Quest Log e Help System NÃO entram aqui: eles ganharam o MESMO
# nome em data/specials.inc, com corpo nulo (ver o bloco marcado lá).
DE_PARA_SPECIAL = {
    "StartLegendaryBattle": "BattleSetup_StartLegendaryBattle",
    "GetPartyMonSpecies": "ScriptGetPartyMonSpecies",
    "GetPokedexCount": "GetFrlgPokedexCount",
    "SelectMoveDeleterMove": "MoveDeleterChooseMoveToForget",
}


# ----------------------------------------------------------------- leitura ---
def constantes(caminho, prefixo):
    """{nome: valor} dos `#define PREFIXO_*` de um header, sem pré-processador.

    Serve para as duas tabelas que este arquivo traduz POR NOME (movimento e
    clima). Corpo que não é número inteiro é ignorado de propósito: alias não é
    entrada de tabela de tradução.
    """
    fora = {}
    for m in re.finditer(r"^#define\s+(%s_[A-Za-z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)"
                         r"\s*(?://.*)?$" % prefixo, open(caminho).read(), re.M):
        fora[m.group(1)] = int(m.group(2), 0)
    return fora


def tradutor_por_nome(header_fonte, header_nosso, prefixo):
    """(valor da fonte -> valor nosso) resolvido pelo NOME da constante.

    As duas tabelas de `MOVEMENT_ACTION_*` divergem em 166 das 172 entradas
    (o FRLG tem `FACE_*_FAST` em 0x4-0x7 e empurra o resto), então traduzir por
    valor escreveria o passo errado sem nenhum sinal. Nome que só existe na
    fonte devolve None, e a cena inteira é recusada.
    """
    fonte = constantes(header_fonte, prefixo)
    nosso = constantes(header_nosso, prefixo)
    de_para, nomes = {}, {}
    for nome, valor in fonte.items():
        alvo = nosso.get(nome)
        de_para[valor] = alvo
        nomes[valor] = nome
    return de_para, nomes


def macros_do_motor():
    """Nome de toda macro que o NOSSO asm/macros/event.inc define."""
    return set(re.findall(r"^\t\.macro\s+(\w+)",
                          open(f"{RAIZ}/asm/macros/event.inc").read(), re.M))


def tabela_de_map_script_tipo2(rom, off, maxi=16):
    """[(var, valor, offset)] de uma tabela ON_FRAME/ON_WARP do FireRed.

    Formato `.2byte var / .2byte valor / .4byte script`, terminada por var 0
    (asm/macros/map.inc, `map_script_2`). Entrada cujo ponteiro cai fora da ROM
    é SUJEIRA (a fonte tem tabelas lidas em cima de dado, e o G0 já viu isso nos
    eventos): ela entra na lista com offset None e é recusada com motivo, em vez
    de sumir calada.

    A LEITURA PARA NO PRIMEIRO PONTEIRO SUJO, e isso foi medido em 06/09/2026,
    no bloco c6. A tabela da `Galar_Route1601` (fonte `g10m23`, tabela em
    0x71D238) tem UMA entrada e **nenhum terminador**: logo depois dela vem a
    tabela EXTERNA de map script da `Galar_Route1603` (`g10m26`), e 24 bytes
    adiante a tabela interna dela. Lendo até `var == 0` a leitura atravessava a
    fronteira e trazia a entrada do mapa VIZINHO para dentro deste, com o mesmo
    rótulo de cena; o autoteste pegou como "rotulo de cena repetido". Tabela de
    verdade não tem ponteiro fora da ROM no meio, então o primeiro ponteiro sujo
    é fim de tabela. Ele fica na lista, uma vez, para a recusa continuar sendo
    contada em voz alta; o que vem depois dele é dado de outra pessoa.
    """
    fora = []
    for i in range(maxi):
        p = off + i * 8
        if p + 8 > len(rom):
            break
        var = int.from_bytes(rom[p:p + 2], "little")
        if var == 0:
            break
        valor = int.from_bytes(rom[p + 2:p + 4], "little")
        ptr = int.from_bytes(rom[p + 4:p + 8], "little")
        if not (BASE <= ptr < BASE + len(rom)):
            fora.append((var, valor, None))
            break
        fora.append((var, valor, ptr - BASE))
    return fora


# ------------------------------------------------------------- desmontagem ---
class Bloco:
    def __init__(self, inicio):
        self.inicio = inicio
        self.ins = []
        self.enchimento = False


def blocos(rom, tab, inicio, maxi=400):
    """([Bloco] na ordem de descoberta, falha) seguindo goto/call/goto_if.

    Mesma travessia do `fala_galar.desmonta`, mas guardando os ARGUMENTOS de
    cada instrução, porque aqui a saída é código e não classificação.
    """
    fora, vistos, fila, falha = [], set(), [inicio], None
    while fila:
        off = fila.pop(0)
        if off in vistos or not (0 <= off < len(rom)):
            continue
        vistos.add(off)
        b = Bloco(off)
        fora.append(b)
        for _ in range(maxi):
            op = rom[off]
            if op == ENCHIMENTO and b.ins and b.ins[-1][0] in ("goto_if", "call_if"):
                # A fonte deixa a saída de uma cadeia de `compare`/`goto_if`
                # CAIR no byte de enchimento de espaço livre (0xFF). Cair no
                # enchimento é defeito da fonte, não comportamento a copiar: o
                # emissor põe um `end` explícito aqui. No caso que isto
                # destrava (o clima da Wild Area) o ramo é INALCANÇÁVEL, e dá
                # para provar: `random 9` devolve 0 a 8 e a cadeia cobre 0 a 9.
                b.ins.append(("end", []))
                b.enchimento = True
                break
            if op not in tab:
                falha = falha or "opcode 0x%02X" % op
                break
            nome, tams = tab[op]
            if tams is None or nome == "trainerbattle":
                falha = falha or "macro de tamanho variavel: " + nome
                break
            args, p = [], off + 1
            for s in tams:
                if p + s > len(rom):
                    args = None
                    break
                args.append(int.from_bytes(rom[p:p + s], "little"))
                p += s
            if args is None:
                falha = falha or "fim de rom"
                break
            b.ins.append((nome, args))
            if nome == "goto":
                if BASE <= args[0] < BASE + len(rom):
                    fila.append(args[0] - BASE)
                break
            if nome in ("call", "goto_if", "call_if"):
                alvo = args[-1]
                if BASE <= alvo < BASE + len(rom):
                    fila.append(alvo - BASE)
            if nome in ("end", "return"):
                break
            off = p
        else:
            falha = falha or "script longo demais"
    return fora, falha


# ---------------------------------------------------------------- tradução ---
class Recusa(Exception):
    """Motivo pelo qual uma cena INTEIRA não entra. Nunca meia cena."""


# Comando que sai igual, com os argumentos como estão. Todo nome daqui é
# conferido contra `macros_do_motor()` antes de qualquer emissão.
IGUAIS_SEM_ARG = {"lock", "lockall", "release", "releaseall", "faceplayer",
                  "end", "return", "waitstate", "closemessage", "waitmessage",
                  "waitbuttonpress", "waitse", "waitfanfare", "doweather",
                  "fadedefaultbgm", "hidemonpic", "waitmoncry", "waitdooranim",
                  "nop", "nop1"}
IGUAIS_COM_ARG = {"delay": 1, "playse": 1, "playfanfare": 1, "waitmovement": 1,
                  "fadescreen": 1, "textcolor": 1, "savebgm": 1, "random": 1,
                  # `erasebox` existe neste motor com o CORPO COMENTADO
                  # (`src/scrcmd.c:1973`, `Menu_EraseWindowRect` fora de uso):
                  # ele le os quatro bytes e nao faz nada. Emitir e fiel ao
                  # bytecode da fonte e nao muda pixel nenhum; por isso ele
                  # tambem entra em MOLDURA logo abaixo, para nao contar como
                  # efeito e deixar passar cena que virou no-op.
                  "erasebox": 4}
# Comando que mexe em objeto pelo id LOCAL da fonte.
POR_ID = {"applymovement": 2, "addobject": 1, "removeobject": 1,
          "setobjectxyperm": 3, "setobjectxy": 3, "setobjectmovementtype": 2,
          "turnobject": 2}

# Comando que so emoldura a cena: nao muda nada que o jogador leve consigo.
# Cena cujo corpo traduzido so tem isto e no-op, e no-op nao entra.
MOLDURA = {"lock", "lockall", "release", "releaseall", "faceplayer", "end",
           "return", "delay", "waitstate", "closemessage", "waitmessage",
           "waitbuttonpress", "goto", "call", "goto_if", "call_if",
           "compare_var_to_value", "textcolor", "waitmovement", "nop", "nop1",
           "erasebox"}

STD_MSGBOX = {2: "MSGBOX_NPC", 3: "MSGBOX_SIGN", 4: "MSGBOX_DEFAULT",
              5: "MSGBOX_YESNO", 6: "MSGBOX_AUTOCLOSE"}

# =========================================================================== #
# REABERTURA DAS RECUSAS (onda 3, lote L1, 08/09/2026)
#
# Tres motivos de recusa do bloco c4a foram medidos como CUSTO DE ENDERECO e
# nao como impossibilidade, e sao os que abrem aqui.
#
# 1. "flag de motor do demake": a fonte le com `checkflag` uma flag que nao
#    esconde nenhum objeto importado, entao ela nao tinha nome nosso e a cena
#    inteira caia. Agora ela GANHA nome, da faixa de Galar 0x2300-0x237F, e o
#    `setflag`/`clearflag` da mesma flag passa a escrever nesse endereco em vez
#    de virar comentario inerte: a cena volta a ler e escrever o proprio estado.
#    Flag que a cena SO escreve e nunca le continua comentario -- dar endereco a
#    ela seria gastar vaga para acender lampada sem fio.
#
#    O LIMITE E MEDIDO, nao chutado: `FLAGS_COUNT` do FireRed e 0x900
#    (`include/constants/flags.h` da fonte). Numero acima disso num `checkflag`
#    NAO e flag: o ponteiro caiu em dado, e dar endereco a ele seria inventar
#    estado. Abaixo de TEMP_FLAGS_FIM sao as flags de rascunho da fonte, que o
#    motor limpa a cada mapa; traduzi-las para uma flag PERSISTENTE mudaria o
#    que a cena faz. As duas pontas saem com o valor no motivo.
#
# 2. "var salva da fonte sem dono": mesma historia do lado das vars. A faixa de
#    save do FireRed e 0x4000-0x40FF (`VARS_START`/`VARS_END` da fonte), e as
#    dezesseis primeiras sao TEMP. Endereco fora disso nao e var.
#
# 3. "comando de cena fora do filtro": os que tem MACRO no nosso motor e
#    semantica identica passam a ser emitidos (`copyvar`, `setorcopyvar`,
#    `setfieldeffectargument`, `checkcoins`, `checkmoney`). Os de NAO_PORTAVEL
#    continuam fora, com o nome do comando no motivo, e agora a fila os fecha
#    como `descartada` em vez de os deixar voltando a cada varredura.
# =========================================================================== #
FLAGS_COUNT_FONTE = 0x900       # include/constants/flags.h do pokefirered
TEMP_FLAGS_FIM = 0x20           # abaixo disso e flag de rascunho da fonte
PRIMEIRA_VAR_SAVE_FONTE = 0x4010    # 0x4000-0x400F sao as TEMP do FireRed
ULTIMA_VAR_SAVE_FONTE = 0x40FF      # VARS_END do FireRed

# Comando que tem macro aqui e NAO tem como atravessar, com o porque medido.
# Fica em UM lugar so porque a fila le esta lista para decidir entre `adiada`
# (falta trabalho) e `descartada` (nao ha o que fazer).
NAO_PORTAVEL = {
    "multichoice": "a lista de opcoes e um indice em gMultichoiceLists, e a "
                   "tabela deste motor tem outro conteudo: portar o indice "
                   "poria outro menu na tela",
    "multichoicedefault": "mesma tabela do multichoice",
    "multichoicegrid": "mesma tabela do multichoice",
    "copybyte": "os dois argumentos sao ENDERECOS de RAM da fonte, e a RAM "
                "deste motor tem outro mapa",
    "callnative": "o argumento e o endereco de uma funcao da ROM da fonte",
    "trywondercardscript": "o Wonder Card do FRLG nao existe neste motor",
    "setworldmapflag": "comando so do FRLG, sem equivalente aqui",
}


class Tradutor:
    """Escreve a cena da fonte no dialeto do nosso motor, ou recusa por inteiro."""

    def __init__(self, rom, tab, cmap, de_para_obj, flags_de_esconder,
                 nome_da_var, nome_da_flag, musica):
        self.rom, self.tab, self.cmap = rom, tab, cmap
        self.de_para_obj = de_para_obj          # {id local da fonte: id nosso}
        self.flags_de_esconder = flags_de_esconder  # {flag da fonte: [id local]}
        self.nome_da_var = nome_da_var          # {endereço da fonte: nome nosso}
        self.nome_da_flag = nome_da_flag        # {flag da fonte: nome nosso}
        self.musica = musica                    # {id da fonte: MUS_* nosso}
        self.macros = macros_do_motor()
        self.mov_de_para, self.mov_nomes = tradutor_por_nome(
            f"{PKFR}/include/constants/event_object_movement.h",
            f"{RAIZ}/include/constants/event_object_movement.h",
            "MOVEMENT_ACTION")
        self.clima_de_para, self.clima_nomes = tradutor_por_nome(
            f"{PKFR}/include/constants/weather.h",
            f"{RAIZ}/include/constants/weather.h", "WEATHER")
        # ONDA 3: efeito de campo POR NOME, nunca por numero. O `FLDEFF_*` do
        # FireRed e do nosso motor comeca igual e diverge no meio da lista (66
        # dos 75 nomes da fonte existem aqui, medido em 08/09/2026), entao
        # copiar o indice poria outro efeito na tela em silencio.
        self.fldeff_de_para, self.fldeff_nomes = tradutor_por_nome(
            f"{PKFR}/include/constants/field_effects.h",
            f"{RAIZ}/include/constants/field_effects.h", "FLDEFF")
        self.usou_flag = set()
        # Bloco solto que o gancho `extra` precisa emitir fora do corpo (lista
        # de loja, por exemplo). Fica aqui e nao no gancho porque quem monta o
        # arquivo e o `cena()`.
        self.extras_gancho = []
        self.var_especial = {v: n for n, v in
                             constantes(f"{RAIZ}/include/constants/vars.h",
                                        "VAR").items()
                             if 0x8000 <= v < 0x8100}
        # DIR_* é enum no nosso global.h e #define no da fonte: a conferência é
        # pelo NOME aparecer no nosso header, que é o que o assembler vai pedir.
        self.dir_fonte = {v: k for k, v in constantes(
            f"{PKFR}/include/constants/global.h", "DIR").items()}
        self.dir_nossas = set(re.findall(r"\bDIR_[A-Z]+\b",
                                        open(f"{RAIZ}/include/constants/global.h").read()))
        # SPECIAL: índice do FireRed -> nome, e o nome tem que existir AQUI.
        # As duas tabelas são listas ordenadas (`def_special`) e o índice NÃO é
        # o mesmo nos dois motores; só o NOME atravessa. Mesma máquina que o
        # bloco c4a já usava em `objetos_galar.py` desde 22/08/2026.
        self.specials_fonte = re.findall(
            r"^\s*def_special\s+(\w+)",
            open(f"{PKFR}/data/specials.inc").read(), re.M)
        self.specials_nossos = set(re.findall(
            r"^\s*def_special\s+(\w+)",
            open(f"{RAIZ}/data/specials.inc").read(), re.M))
        # Tipo de map script desta cena, para o portão dos tipos quietos. Quem
        # chama põe antes de `cena()`; sem ele o portão não morde, que é o
        # comportamento de todo chamador que não é map script (o c4a).
        self.tipo_map_script = None
        # Linha da fila a que esta cena pertence. Só serve para o caderno de
        # `dev_scripts/onda3_falta_traduzir.json` saber a quem cobrar o texto
        # que falta; quem chama põe antes de `cena()`.
        self.chave_da_fila = None
        # Nome nosso para a flag de MOTOR e para a var SEM DONO da fonte, os
        # dois preenchidos por quem chama (o alocador de `objetos_galar.plano`
        # e o de `cenas_galar.plano`). Vazio quer dizer "esta rodada nao alocou
        # nenhuma", e a recusa volta a ser a de antes.
        self.nome_flag_motor = {}
        self.nome_var_livre = {}
        # Preenchido por `cena()` a cada chamada; aqui so para o objeto nunca
        # ficar sem o atributo.
        self.flags_lidas = set()

    def special_nome(self, idx):
        """Nome do special do FireRed, se ele existir NESTE motor também."""
        nome = (self.specials_fonte[idx] if idx < len(self.specials_fonte)
                else None)
        if nome is None:
            raise Recusa("special 0x%03X fora da tabela do FireRed" % idx)
        nome = DE_PARA_SPECIAL.get(nome, nome)
        if nome not in self.specials_nossos:
            raise Recusa("special %s do FireRed nao existe aqui" % nome)
        return nome

    # -- pedaços ------------------------------------------------------------
    def macro(self, nome):
        if nome not in self.macros:
            raise Recusa("comando sem macro no nosso motor: " + nome)
        return nome

    def objeto(self, local):
        if local == 0xFF:
            return "OBJ_EVENT_ID_PLAYER"
        if local == 0x7F:
            return "OBJ_EVENT_ID_CAMERA"
        if 0x8000 <= local <= 0x800F:
            # Id de objeto que vem de VAR e legitimo: `ScrCmd_applymovement` e
            # irmaos leem o id por `VarGet`, entao `applymovement
            # VAR_LAST_TALKED` e o idioma de "mexa no NPC com quem eu falei".
            # Emitir o NOME da var e fiel; recusar seria perder a cena por um
            # detalhe que o nosso motor entende igual.
            return self.var(local)
        if local >= 0x4000:
            raise Recusa("id de objeto vem de var salva (0x%04X), fora do "
                         "alcance deste bloco" % local)
        nosso = self.de_para_obj.get(local)
        if nosso is None:
            raise Recusa("objeto local %d nao entrou no mapa no G4" % local)
        return str(nosso)

    def var(self, endereco):
        # Var especial sai pelo NOME que o NOSSO header da, nunca por
        # `VAR_0x%04X` montado a mao: 0x800C e VAR_FACING, 0x800D e VAR_RESULT,
        # 0x800E e VAR_ITEM_ID e 0x800F e VAR_LAST_TALKED, e so quatro dos
        # dezesseis primeiros tem o nome numerico. Montar o nome errado nao
        # passa no assembler, mas so na hora do link, longe daqui.
        if 0x8000 <= endereco < 0x8100:
            nome = self.var_especial.get(endereco)
            if nome is None:
                raise Recusa("var especial 0x%04X sem nome no nosso vars.h"
                             % endereco)
            return nome
        nome = self.nome_da_var.get(endereco)
        if nome is None:
            nome = self.nome_var_livre.get(endereco)
        if nome is None:
            if not (PRIMEIRA_VAR_SAVE_FONTE <= endereco
                    <= ULTIMA_VAR_SAVE_FONTE):
                raise Recusa("0x%04X nao e var de save da fonte (a faixa e "
                             "0x%04X-0x%04X): o ponteiro caiu em dado"
                             % (endereco, PRIMEIRA_VAR_SAVE_FONTE,
                                ULTIMA_VAR_SAVE_FONTE))
            raise Recusa("var salva 0x%04X da fonte sem dono nosso" % endereco)
        return nome

    def flag(self, f):
        nome = self.nome_da_flag.get(f)
        if nome is None:
            nome = self.nome_flag_motor.get(f)
        if nome is None:
            if f >= FLAGS_COUNT_FONTE:
                raise Recusa("0x%04X esta acima da FLAGS_COUNT do FireRed "
                             "(0x%03X): nao e flag, o ponteiro caiu em dado"
                             % (f, FLAGS_COUNT_FONTE))
            if f < TEMP_FLAGS_FIM:
                raise Recusa("flag 0x%03X e de RASCUNHO na fonte (abaixo de "
                             "0x%03X): dar-lhe endereco persistente mudaria o "
                             "que a cena faz" % (f, TEMP_FLAGS_FIM))
            raise Recusa("flag 0x%03X da fonte nao esconde objeto importado "
                         "(e flag de motor do demake)" % f)
        return nome

    def quer_flag_de_motor(self, f):
        """A flag da fonte merece endereco nosso? So a que a cena LE."""
        return (f not in self.nome_da_flag
                and TEMP_FLAGS_FIM <= f < FLAGS_COUNT_FONTE)

    def movimento(self, ptr, rotulo):
        """(linhas do bloco de movimento, rótulo) traduzido passo a passo."""
        if not (BASE <= ptr < BASE + len(self.rom)):
            raise Recusa("ponteiro de movimento fora da rom")
        off = ptr - BASE
        passos = []
        for i in range(64):
            b = self.rom[off + i]
            if b == 0xFE:                       # MOVEMENT_ACTION_STEP_END
                nosso = self.mov_de_para.get(0xFE)
                if nosso is None:
                    raise Recusa("step_end sem equivalente")
                passos.append("MOVEMENT_ACTION_STEP_END")
                break
            nome = self.mov_nomes.get(b)
            if nome is None:
                raise Recusa("passo de movimento 0x%02X fora da tabela do FR" % b)
            if self.mov_de_para.get(b) is None:
                raise Recusa("passo %s nao existe no nosso motor" % nome)
            passos.append(nome)
        else:
            raise Recusa("movimento sem fim")
        return ["%s:" % rotulo] + ["\t.byte %s" % p for p in passos]

    def texto(self, ptr, rotulo):
        """O bloco `.string` da fala, JA EM INGLES, ou recusa a cena inteira.

        ONDA 3, LOTE L1: a tradução entra aqui, na geração, e não mais numa
        segunda passada de `aplica_traducao_galar.py`. A regra dos três degraus
        (rótulo, texto, régua do portão) está escrita no alto de
        `dev_scripts/fala_galar.py`.

        POR QUE A CENA INTEIRA CAI quando falta tradução, e não só este bloco: o
        texto de uma cena é chamado por `msgbox RÓTULO, CAIXA` de dentro do
        corpo. Emitir o corpo sem o bloco deixaria um rótulo sem símbolo, e a
        build só acusaria no LINK, longe daqui. Cena é tudo ou nada, que é a
        mesma lei de toda `Recusa` deste arquivo. Na fala solta
        (`fala_galar.py`) o texto É o script, e lá o que fica de fora é a linha.
        """
        if not (BASE <= ptr < BASE + len(self.rom)):
            raise Recusa("ponteiro de texto fora da rom")
        t, motivo = FALA.texto(self.rom, self.cmap, ptr - BASE)
        if motivo:
            raise Recusa("texto recusado: " + motivo)
        en, origem = FALA.traducao().resolve(rotulo, t, self.chave_da_fila)
        if en is None:
            raise Recusa(FALA.MOTIVO_SEM_TRADUCAO)
        return FALA.linhas_de_texto(rotulo, en,
                                    quebra=origem in ("rotulo", "texto"))

    # -- a cena inteira -----------------------------------------------------
    def cena(self, inicio, base):
        """([linhas do .inc], usadas) ou levanta Recusa.

        `usadas` conta o que a cena consumiu (flags acesas, objetos escondidos),
        para o relatório poder somar sem reler o texto emitido.
        """
        bs, falha = blocos(self.rom, self.tab, inicio)
        if falha:
            raise Recusa("decodificacao incompleta: " + falha)
        # PORTÃO DOS TIPOS QUIETOS (bloco c6). ON_LOAD roda antes de o mapa ser
        # desenhado, ON_RESUME no fim da carga e a cada volta ao campo, e
        # ON_RETURN_TO_FIELD logo depois: em nenhum dos três há caixa de fala
        # nem jogador andando. Cena com comando que precisa do campo rodando
        # sai INTEIRA com motivo, em vez de virar trava na tela de carga.
        if self.tipo_map_script in TIPOS_QUIETOS:
            for b in bs:
                for nome, _args in b.ins:
                    if nome in PRECISA_DO_CAMPO:
                        raise Recusa(
                            "map script de tipo %d (%s) com `%s`, que precisa do "
                            "campo rodando" % (self.tipo_map_script,
                                               MACRO_DIRETO[self.tipo_map_script],
                                               nome))
        # ONDA 3: QUAIS FLAGS ESTA CENA LE. So a flag lida merece endereco
        # nosso; a que a cena so escreve continua comentario inerte, porque
        # gastar vaga da faixa de Galar para acender lampada que ninguem le e
        # dividir um recurso escasso por nada. A varredura e da cena INTEIRA e
        # feita antes de emitir uma linha: o `checkflag` costuma vir num bloco
        # depois do `setflag`, e decidir bloco a bloco daria resposta diferente
        # conforme a ordem.
        self.flags_lidas = {a[0] for b in bs for n_i, a in b.ins
                            if n_i == "checkflag" and a}
        rotulo = {b.inicio: ("%s" % base if i == 0 else "%s_b%d" % (base, i))
                  for i, b in enumerate(bs)}
        corpo, extras, usadas = [], [], collections.Counter()
        n_mov = n_txt = 0

        def alvo(ptr):
            off = ptr - BASE
            if off not in rotulo:
                raise Recusa("ramo para offset nao visitado")
            return rotulo[off]

        for b in bs:
            corpo.append("%s::" % rotulo[b.inicio])
            ini_do_bloco = len(corpo)
            palavra = {}
            for nome, args in b.ins:
                if nome == "loadword":
                    palavra[args[0]] = args[1]
                    continue
                if nome == "callstd":
                    if args[0] not in STD_MSGBOX or 0 not in palavra:
                        raise Recusa("callstd %d fora do que este bloco escreve"
                                     % args[0])
                    r = "%s_Text%d" % (base, n_txt)
                    extras.extend(self.texto(palavra[0], r))
                    n_txt += 1
                    corpo.append("\t%s %s, %s" % (self.macro("msgbox"), r,
                                                  STD_MSGBOX[args[0]]))
                    usadas["efeito"] += 1
                    continue
                if nome in IGUAIS_SEM_ARG:
                    corpo.append("\t" + self.macro(nome))
                elif nome in IGUAIS_COM_ARG:
                    corpo.append("\t%s %s" % (self.macro(nome),
                                              ", ".join(str(a) for a in args)))
                elif nome in ("setflag", "clearflag"):
                    # Flag que nao esconde objeto importado e flag do MOTOR do
                    # demake (0x900+ e acima da FLAGS_COUNT do FireRed): a nossa
                    # ROM nao tem quem a leia, e nenhuma cena portada faz
                    # `checkflag` nela, porque `checkflag` de flag sem dono
                    # RECUSA a cena inteira logo abaixo. Escrever nela seria
                    # gastar endereco para acender lampada sem fio; nao escrever
                    # nao muda nada que o jogo consiga observar. Fica a marca.
                    # A flag que a cena tambem LE ganhou endereco nosso na
                    # onda 3 (`nome_flag_motor`), e entao o `setflag` dela tem
                    # de ESCREVER de verdade: escrever no lugar certo e ler no
                    # lugar certo e a mesma decisao. O comentario inerte fica
                    # so para a flag que ninguem le.
                    if (args[0] not in self.nome_da_flag
                            and not (args[0] in self.flags_lidas
                                     and args[0] in self.nome_flag_motor)):
                        corpo.append("\t@ %s 0x%03X da fonte: flag de motor do "
                                     "demake, sem leitor aqui (cenas_galar.py)"
                                     % (nome, args[0]))
                        usadas["flag_inerte"] += 1
                        continue
                    corpo.append("\t%s %s" % (self.macro(nome),
                                              self.flag(args[0])))
                    usadas[nome] += 1
                elif nome == "checkflag":
                    corpo.append("\t%s %s" % (self.macro(nome),
                                              self.flag(args[0])))
                    usadas[nome] += 1
                elif nome in ("setvar", "addvar", "subvar"):
                    corpo.append("\t%s %s, %d" % (self.macro(nome),
                                                  self.var(args[0]), args[1]))
                elif nome == "compare_var_to_value":
                    corpo.append("\t%s %s, %d" % (self.macro("compare"),
                                                  self.var(args[0]), args[1]))
                elif nome == "setweather":
                    n = self.clima_nomes.get(args[0])
                    if n is None or self.clima_de_para.get(args[0]) is None:
                        raise Recusa("clima %d da fonte sem nome nosso" % args[0])
                    corpo.append("\t%s %s" % (self.macro("setweather"), n))
                elif nome == "playbgm":
                    mus = self.musica.get(args[0])
                    if mus is None:
                        raise Recusa("musica %d da fonte sem MUS_* nosso" % args[0])
                    corpo.append("\t%s %s, %d" % (self.macro("playbgm"), mus,
                                                  args[1]))
                elif nome in POR_ID:
                    ids = self.objeto(args[0])
                    if nome == "applymovement":
                        r = "%s_Mov%d" % (base, n_mov)
                        extras.extend(self.movimento(args[1], r))
                        n_mov += 1
                        corpo.append("\t%s %s, %s"
                                     % (self.macro("applymovement"), ids, r))
                    elif nome == "turnobject":
                        d = self.dir_fonte.get(args[1])
                        if d is None or d not in self.dir_nossas:
                            raise Recusa("direcao %d da fonte sem DIR_* nosso"
                                         % args[1])
                        corpo.append("\t%s %s, %s" % (self.macro(nome), ids, d))
                    else:
                        resto = ", ".join(str(a) for a in args[1:])
                        corpo.append("\t%s %s%s" % (self.macro(nome), ids,
                                                    ", " + resto if resto else ""))
                        if nome == "removeobject":
                            corpo[-1:] = self._esconde(args[0]) + [corpo[-1]]
                            usadas["esconde"] += 1
                elif nome == "setmetatile":
                    # O ÍNDICE DE METATILE ATRAVESSA 1:1, e isso é medido e não
                    # suposto: `dev_scripts/tileset_galar.py` importa o
                    # `metatiles.bin` da fonte na MESMA ordem (o índice é a
                    # posição no arquivo), e o corte primário/secundário do FRLG
                    # (640, contra os 512 do pokeemerald) é resolvido pelo
                    # próprio motor em `src/fieldmap.c:438`, que devolve
                    # NUM_METATILES_IN_PRIMARY_FRLG quando o layout é `isFrlg`,
                    # que é o caso de todos os 438 mapas de Galar. Traduzir o
                    # número seria o erro; copiá-lo é o certo.
                    corpo.append("\t%s %d, %d, %d, %d"
                                 % (self.macro(nome), args[0], args[1],
                                    args[2], args[3]))
                elif nome == "special":
                    alvo_sp = self.special_nome(args[0])
                    if (alvo_sp == "InitUnionRoom"
                            and self.tipo_map_script != 5):
                        # `InitUnionRoom` (src/union_room.c:3293) cria uma task
                        # e faz `AllocZeroed` de uma `WirelessLink_URoom` a
                        # cada chamada, e o ponteiro anterior se perde. Neste
                        # motor ele mora em UM lugar só: o `CableClub_OnResume`
                        # dos 49 Centros Pokémon da árvore, sempre em
                        # MAP_SCRIPT_ON_RESUME. A fonte chama o mesmo special
                        # também no ON_TRANSITION do `Galar_Wedgehurst03`, o
                        # que somaria uma segunda alocação na MESMA entrada de
                        # mapa, e a cena não ganha nada com isso: aquele mapa
                        # já recebe o ON_RESUME. Sai com motivo em vez de
                        # entrar como risco novo por zero conteúdo.
                        raise Recusa("InitUnionRoom fora de ON_RESUME: neste "
                                     "motor ele so e chamado pelo "
                                     "CableClub_OnResume, e ele aloca a cada "
                                     "chamada")
                    corpo.append("\t%s %s" % (self.macro(nome), alvo_sp))
                elif nome == "specialvar":
                    corpo.append("\t%s %s, %s" % (self.macro(nome),
                                                  self.var(args[0]),
                                                  self.special_nome(args[1])))
                elif nome in ("goto", "call"):
                    corpo.append("\t%s %s" % (self.macro(nome), alvo(args[0])))
                elif nome in ("goto_if", "call_if"):
                    corpo.append("\t%s %d, %s" % (self.macro(nome), args[0],
                                                  alvo(args[1])))
                elif nome in ("copyvar", "setorcopyvar"):
                    # `copyvar` copia var para var; `setorcopyvar` aceita valor
                    # OU var na origem, e o motor decide pelo numero (`VarGet`
                    # so resolve o que esta na faixa de var). Por isso a origem
                    # so passa pelo tradutor quando ela E um endereco de var:
                    # traduzir um literal daria outro numero.
                    origem = (self.var(args[1]) if args[1] >= 0x4000
                              else str(args[1]))
                    corpo.append("\t%s %s, %s" % (self.macro(nome),
                                                  self.var(args[0]), origem))
                elif nome in ("dofieldeffect", "waitfieldeffect"):
                    n_fld = self.fldeff_nomes.get(args[0])
                    if n_fld is None or self.fldeff_de_para.get(args[0]) is None:
                        raise Recusa("efeito de campo %d da fonte sem FLDEFF_* "
                                     "nosso" % args[0])
                    corpo.append("\t%s %s" % (self.macro(nome), n_fld))
                elif nome == "checkcoins":
                    corpo.append("\t%s %s" % (self.macro(nome),
                                              self.var(args[0])))
                elif nome in ("setfieldeffectargument", "checkmoney"):
                    corpo.append("\t%s %s" % (self.macro(nome),
                                              ", ".join(str(a) for a in args)))
                elif nome in NAO_PORTAVEL:
                    raise Recusa("comando de cena fora do filtro: %s (%s)"
                                 % (nome, NAO_PORTAVEL[nome]))
                elif not self.extra(nome, args, corpo, base):
                    raise Recusa("comando de cena fora do filtro: " + nome)
                if nome not in MOLDURA:
                    usadas["efeito"] += 1
            corpo[ini_do_bloco:] = self._arruma_rabo(corpo[ini_do_bloco:])
            corpo.append("")
        if not usadas["efeito"]:
            # Cena que, depois de tirar o que a nossa ROM não observa, virou
            # `release; end`. Escrever map script que não faz nada é pior que
            # não escrever: fica dívida com cara de trabalho feito.
            raise Recusa("cena vira no-op depois da traducao (so moldura)")
        return corpo + extras + self.extras_gancho, usadas

    # Comandos que TRANSFEREM o controle: depois deles nada mais roda neste
    # bloco, entao a soltura tem que ficar ANTES.
    TRANSFERE = {"goto", "goto_if", "call_if", "return", "end",
                 "gotopostbattlescript", "gotobeatenscript"}

    @classmethod
    def _arruma_rabo(cls, linhas):
        """Duas correcoes de RABO, as duas medidas pela QA de 23/08/2026 no
        `GalarObj_G06M33_o0_b2` (`data/scripts/galar_objetos.inc:692`).

        1. `checkflag` sem `goto_if`/`call_if` depois nao decide NADA: e leitura
           morta, e era o unico caso da arvore inteira (C27). Na fonte o ramo
           existia; o filtro nao o trouxe, e o que sobrou foi uma linha que so
           gasta ROM. Vira comentario COM o nome da flag, para quem for portar
           o ramo saber onde ele entrava.
        2. `release`/`releaseall` no MEIO do bloco solta o jogador antes de a
           cena acabar: ele anda enquanto o `removeobject` apaga um NPC e o
           `fadescreen` escurece a tela. A soltura desce ate a ultima linha
           antes do primeiro comando que transfere o controle. Duas solturas no
           mesmo bloco viram uma: `ScrCmd_release` e idempotente.
        """
        sem_morta = []
        for i, ln in enumerate(linhas):
            if ln.strip().split(" ")[0] == "checkflag":
                prox = next((x.strip() for x in linhas[i + 1:]
                             if x.strip() and not x.strip().startswith("@")), "")
                if prox.split(" ")[0] not in ("goto_if", "call_if"):
                    sem_morta.append(
                        "\t@ %s sem goto_if/call_if depois: leitura morta, o "
                        "ramo da fonte nao atravessou o filtro (cenas_galar.py)"
                        % ln.strip())
                    continue
            sem_morta.append(ln)
        fora, pendente = [], None
        for ln in sem_morta:
            c = ln.strip()
            if c in ("release", "releaseall"):
                if pendente is None:
                    pendente = ln
                continue
            if pendente is not None and (not c or c.split(" ")[0] in cls.TRANSFERE):
                fora.append(pendente)
                pendente = None
            fora.append(ln)
        if pendente is not None:
            fora.append(pendente)
        return fora

    def extra(self, nome, args, corpo, base):
        """Gancho para quem herda: emite um comando a mais, ou devolve False.

        Existe para o bloco c4a (`dev_scripts/objetos_galar.py`) acrescentar
        `warp` sem tocar no filtro do c3, que ja esta commitado e provado pelo
        T127. Quem herda so acrescenta; nunca tira nada daqui.
        """
        del nome, args, corpo, base
        return False

    def _esconde(self, local):
        """`setflag` da flag que a FONTE pendurou no objeto (DECISÃO do topo)."""
        for f, ids in sorted(self.flags_de_esconder.items()):
            if local in ids and f in self.nome_da_flag:
                self.usou_flag.add(f)
                return ["\t@ DECISAO cenas_galar.py: removeobject so vale a "
                        "sessao de mapa; a flag e a que a FONTE pendurou neste "
                        "objeto, o que se acrescenta e o momento de acende-la",
                        "\t%s %s" % (self.macro("setflag"), self.nome_da_flag[f])]
        return []


# ------------------------------------------------------------- de-para e pool -
def de_para_de_objetos(chave, doc, gente_por_mapa):
    """{id local da fonte (1-based): id local nosso (1-based)} pela COORDENADA.

    Casar por ORDEM na LISTA INTEIRA seria quase certo e às vezes errado: 9 dos
    391 mapas de Galar têm objeto NOSSO no meio da lista que não veio da fonte
    (marinheiro da travessia, bola do fala_galar), e a partir dele toda a
    numeração anda. Por isso a chave continua sendo a coordenada, e a ordem só é
    consultada DENTRO de um tile, onde a coordenada já não separa ninguém.

    EMPATE DE TILE, e por que ele deixou de ser recusa (onda 5, lote S,
    06/09/2026)
    -----------------------------------------------------------------------
    Até aqui, tile com dois objetos nossos reprovava em vez de escolher, pela
    lição de Oreburgh (ESTADO 0.g). Medido na região inteira, o preço disso são
    10 tiles com 2+ objetos nossos, 31 objetos ao todo, e em **8 desses tiles a
    fonte tem EXATAMENTE o mesmo número de colocáveis** (23 objetos). Nesses a
    dúvida não é quem é quem: é só a ordem, e a ordem existe nos dois lados.

    A regra passa a ser:

      1 nosso no tile           -> como sempre: casa, e mais de um registro da
                                   fonte no mesmo tile continua caindo todos no
                                   mesmo objeto (comportamento antigo, intocado).
      2+ nossos, MESMA contagem -> casa por ORDEM dentro do tile: o k-ésimo
                                   objeto do nosso `map.json` com o k-ésimo
                                   registro colocável da fonte (ordenado por
                                   `i`, que é a ordem da tabela da fonte).
      2+ nossos, contagem       -> RECUSA, como antes. Sem a mesma contagem não
        diferente                  há emparelhamento a fazer, só chute.

    A ordem é evidência medida, e não fé: nos 8 tiles empatados o gráfico casa
    um a um na mesma ordem (162 é `SIGN` nos três mapas em que aparece, 39 é
    `WORKER_M` e 40 é `WORKER_F` em Turffield05 e IsleOfArmor28, 60 é
    `POLICEMAN` e 20 é `MAN` em WildArea03 e Wyndon01), e em `Galar_Wyndon01` o
    INTERCALAMENTO entre dois tiles é idêntico dos dois lados: a fonte escreve 3
    registros em (3,40), 2 em (3,39) e mais 2 em (3,40), e os nossos objetos 1-7
    estão exatamente nessa sequência. Se a numeração tivesse andado, ela teria
    andado aqui.

    A prova fechada, em números: o de-para gráfico da fonte -> `OBJ_EVENT_GFX_*`
    aprendido SÓ nos casamentos um-a-um de Galar tem 78 gráficos distintos e
    ZERO ambiguidade, e os 16 gráficos distintos que aparecem nos 23 objetos do
    empate batem com ele nos 16, sem um conflito e sem um sem-referência.
    """
    por_tile = collections.defaultdict(list)
    for i, o in enumerate(doc.get("object_events", [])):
        por_tile[(o["x"], o["y"])].append(i + 1)
    deles = collections.defaultdict(list)
    for l in gente_por_mapa.get(chave, []):
        if l["tipo"] != "objeto" or not l["motivo"].startswith("entrou"):
            continue
        deles[(l["x"], l["y"])].append(l)
    fora = {}
    for tile, linhas in deles.items():
        nossos = por_tile.get(tile, [])
        if len(nossos) == 1:
            for l in linhas:
                fora[l["i"] + 1] = nossos[0]
        elif len(nossos) > 1 and len(nossos) == len(linhas):
            for l, nosso in zip(sorted(linhas, key=lambda x: x["i"]), nossos):
                fora[l["i"] + 1] = nosso
    return fora


def vars_livres():
    """Endereços 0x4010-0x41FF cujo único dono é o rótulo do pool.

    MEDIÇÃO, com o mesmo pré-processador do portão de colisão, e sobre uma
    árvore em que o BLOCO DESTE GERADOR foi retirado: sem isso a segunda rodada
    veria as vars que ela mesma alocou como ocupadas e escolheria outras, e o
    `.inc` inteiro viraria diff a cada `--aplicar`.
    """
    GUARDA.usa("vars")
    with tempfile.TemporaryDirectory() as tmp:
        for h in GUARDA.HEADERS:
            destino = os.path.join(tmp, h)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy(os.path.join(RAIZ, h), destino)
        limpo = os.path.join(tmp, "include/constants/vars.h")
        # LER ANTES de abrir para escrita: `open(x, "w")` trunca o arquivo na
        # hora, e a leitura no meio da mesma expressão devolveria vazio.
        # Tira TODOS os blocos da fase de conteudo de Galar, nao so o deste
        # gerador: o c4d (`dev_scripts/objetos_galar.py`) tem bloco proprio no
        # mesmo header, e deixa-lo de pe faria a segunda rodada ver as vars que
        # ela mesma alocou como ocupadas e escolher outras, virando diff eterno.
        texto = re.sub(r"// >>> Fase de conteudo de Galar.*?// <<< Fase de "
                       r"conteudo de Galar[^\n]*\n", "",
                       open(limpo).read(), flags=re.S)
        open(limpo, "w").write(texto)
        caminhos = [os.path.join(tmp, h) for h in GUARDA.HEADERS]
        defs = GUARDA.le_defines(caminhos)
        valores = GUARDA.resolve(sorted(defs), os.path.join(tmp, "include"))
    donos = collections.defaultdict(list)
    for nome, v in valores.items():
        if 0x4010 <= v < 0x4200:
            donos[v].append(nome)
    pool = re.compile(r"^VAR_UNUSED")
    return [v for v in sorted(donos)
            if donos[v] and all(pool.match(n) for n in donos[v])]


def flags_livres_de_galar(bloco_atual):
    """Faixa de Galar ainda livre, tirando o que este próprio bloco já apelidou.

    CONSERTO DE 22/08/2026 (rodada 9): a varredura casava QUALQUER ocorrência de
    `FLAG_UNUSED_0xNNNN`, e a maior parte delas é a PRÓPRIA DEFINIÇÃO
    (`#define FLAG_UNUSED_0x1C80 ...`). Com isso a faixa inteira lia como tomada
    e o pool vinha VAZIO; enquanto nenhuma cena pedia flag de esconder ninguém
    percebeu, e na primeira que pediu o gerador parou com "0 livres na faixa de
    Galar". Tomada agora é só a flag que tem APELIDO de outro dono, que é o mesmo
    critério do `estaticos_galar.flags_realmente_livres`. A faixa é
    COMPARTILHADA com o bloco c4b do `objetos_galar.py`, e é por isso que os dois
    lados têm de enxergar o apelido do outro: quem roda depois pula o que o
    primeiro já pegou.
    """
    texto = sem_bloco(open(FLAGS_H).read(), MARCA_FLAG_INI, MARCA_FLAG_FIM)
    tomadas = {int(m, 16) for m in re.findall(
        r"#define\s+(?!FLAG_UNUSED)\w+\s+\(?\s*FLAG_UNUSED_0x([0-9A-Fa-f]{3,4})\b",
        texto)}
    definidas = {int(m, 16) for m in re.findall(
        r"#define\s+FLAG_UNUSED_0x([0-9A-Fa-f]{3,4})\b", texto)}
    del bloco_atual
    return [f for f in range(PRIMEIRA_FLAG_CENA, ULTIMA_FLAG_CENA + 1)
            if f in definidas and f not in tomadas]


def sem_bloco(texto, ini, fim):
    i = texto.find(ini)
    if i < 0:
        return texto
    j = texto.find(fim, i)
    j = len(texto) if j < 0 else j + len(fim) + 1
    return texto[:i] + texto[j:]


# Bloco de OUTRO DONO dentro de um `scripts.inc` de Galar: quem escreve nesses
# arquivos marca a própria obra com um par `@ >>> dono >>>` / `@ <<< ... <<<`.
# Este gerador NÃO escreve bloco marcado (a tabela `MapScripts` dele é o corpo
# solto do arquivo), então TODO bloco marcado que já esteja lá é de outra casa e
# tem de sobreviver a `--aplicar`. O caso real é a Dex de Galar
# (`distribui_dex.py --galar-objetos`), que mora em 7 mapas, um deles com cena.
RE_BLOCO_ALHEIO = re.compile(r"^@ >>> .*? >>>\n.*?^@ <<< .*? <<<[ \t]*$",
                             re.S | re.M)


def blocos_de_outro_dono(caminho):
    """Os blocos marcados que já estão no arquivo, na ordem em que aparecem."""
    if not os.path.exists(caminho):
        return []
    return [m.group(0) for m in RE_BLOCO_ALHEIO.finditer(open(caminho).read())]


def caudas_manuais(arq, ini, fim, corpo_gerado):
    """Comentário de fim de linha que ALGUÉM ESCREVEU À MÃO no bloco marcado.

    A conta é por LINHA INTEIRA de `#define`: só sobrevive a cauda cuja parte
    gerada (`#define NOME VALOR`) é idêntica à que este gerador acabou de
    escrever. Se o endereço mudar, a anotação à mão fala de outro endereço e
    morre junto, que é o certo. Vale para qualquer bloco deste arquivo.
    """
    if not os.path.exists(arq):
        return {}
    texto = open(arq).read()
    i = texto.find(ini)
    if i < 0:
        return {}
    j = texto.find(fim, i)
    velho = texto[i:len(texto) if j < 0 else j]
    gerado = {}
    for linha in corpo_gerado.splitlines():
        m = re.match(r"(#define\s+\S+\s+\S+)\s*(?://\s?(.*))?$", linha)
        if m:
            gerado[re.sub(r"\s+", " ", m.group(1))] = m.group(2) or ""
    caudas = {}
    for linha in velho.splitlines():
        m = re.match(r"(#define\s+\S+\s+\S+)\s*//\s?(.*)$", linha)
        if not m:
            continue
        chave = re.sub(r"\s+", " ", m.group(1))
        if chave not in gerado:
            continue                      # define que saiu: a cauda vai junto
        antiga, agora = m.group(2).rstrip(), gerado[chave]
        if antiga != agora and antiga.startswith(agora):
            caudas[chave] = antiga        # a mão só ACRESCENTOU: preserva
        elif antiga != agora and not agora:
            caudas[chave] = antiga        # linha que nasce sem comentário
    return caudas


def com_caudas_manuais(corpo, arq, ini, fim):
    """Recoloca no corpo recém-gerado as caudas escritas à mão que sobrevivem."""
    caudas = caudas_manuais(arq, ini, fim, corpo)
    if not caudas:
        return corpo
    saida = []
    for linha in corpo.splitlines():
        m = re.match(r"(#define\s+\S+\s+\S+)(\s*)(?://\s?(.*))?$", linha)
        chave = re.sub(r"\s+", " ", m.group(1)) if m else None
        if chave in caudas:
            espaco = m.group(2) or "  "
            linha = "%s%s// %s" % (m.group(1), espaco, caudas[chave])
        saida.append(linha)
    return "\n".join(saida) + ("\n" if corpo.endswith("\n") else "")


def poe_bloco(texto, ini, fim, corpo):
    """Idempotente: troca o bloco marcado NO LUGAR, ou acrescenta no fim.

    O "no lugar" é de 22/08/2026 e nasceu do `--demo` vermelho do fechador.
    Até aqui a função apagava o bloco e colava o novo no FIM do arquivo, e por
    isso dois geradores que escrevem no MESMO header (o bloco c1 daqui e o c4d
    do `objetos_galar.py`, que chama esta mesma função) ficavam trocando de
    última posição a cada rodada: quem rodasse por último empurrava o outro
    para cima. Nenhuma letra do conteúdo mudava, só a ordem, e mesmo assim
    `aplica()` via arquivo diferente e a idempotência caía.
    """
    i = texto.find(ini)
    if i >= 0:
        j = texto.find(fim, i)
        j = len(texto) if j < 0 else j + len(fim) + 1
        return texto[:i] + corpo + texto[j:]
    if not corpo:
        return texto
    return texto.rstrip("\n") + "\n\n" + corpo


# ------------------------------------------------------------------ plano ----
def rotulo_de(chave, sufixo):
    """Rótulo do rótulo da FONTE, nunca do nosso nome de mapa (o G3 renomeia)."""
    return "GalarCena_%s_%s" % (chave.upper(), sufixo)


def levanta():
    """(linhas de map_script da fila, rom, tabela de opcodes, charmap, censos)."""
    rom = open(FALA.ROM_FONTE, "rb").read()
    tab = FALA.tabela_de_opcodes()
    cmap = FALA.charmap()
    roteiros = json.load(open(FALA.ROTEIROS))["linhas"]
    linhas = [l for l in roteiros if l["tipo"] == "map_script"]
    gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
    por_mapa = collections.defaultdict(list)
    for l in gente:
        por_mapa[l["mapa"]].append(l)
    mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
    return rom, tab, cmap, linhas, por_mapa, mundo["de_para"]


def musica_da_fonte():
    try:
        import mundo_galar
        return mundo_galar.tabela_musica()
    except Exception:                                            # noqa: BLE001
        return {}


def plano():
    """(cenas aceitas, recusas contadas, vars alocadas, flags alocadas, censo)."""
    rom, tab, cmap, linhas, gente_por_mapa, de_para = levanta()
    musica = musica_da_fonte()
    recusa = collections.Counter()
    censo = collections.Counter()
    docs = {}
    # Motivo por MAPA DA FONTE do que a etapa 1 (inventario) ja barra, antes de
    # qualquer traducao. Junta com o `por_mapa_motivo` da etapa 4 no fim, e e
    # esse par que a FILA recebe: sem ele um mapa recusado aqui sairia da fila
    # sem motivo nenhum, que e o silencio que esta fase inteira existe para
    # nao deixar acontecer.
    pre_motivo = collections.defaultdict(list)

    # 1. inventário: cada linha da fila vira uma ou mais ENTRADAS de map script.
    entradas = []
    for l in sorted(linhas, key=lambda z: z["chave"]):
        chave = l["mapa_fonte"]
        dp = de_para.get(chave)
        if dp is None:
            recusa["mapa da fonte fora do de-para do G3"] += 1
            pre_motivo[chave].append("mapa da fonte fora do de-para do G3")
            continue
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, dp["nome"])
        if not os.path.exists(caminho):
            recusa["map.json do mapa nao existe"] += 1
            pre_motivo[chave].append("map.json do mapa nao existe")
            continue
        if caminho not in docs:
            docs[caminho] = json.load(open(caminho))
        for tipo, off in FALA.tabela_de_map_script(rom, int(l["ponteiro_fonte"], 16)):
            censo["tipo %d" % tipo] += 1
            if off is None:
                recusa["ponteiro de map script fora da rom"] += 1
                pre_motivo[chave].append("ponteiro de map script fora da rom")
                continue
            if tipo in TIPOS_TABELA:
                itens = tabela_de_map_script_tipo2(rom, off)
                if not itens:
                    recusa["tabela de tipo 2/4 vazia"] += 1
                    pre_motivo[chave].append("tabela de tipo 2/4 vazia")
                for var, valor, alvo in itens:
                    entradas.append((chave, dp, caminho, tipo, var, valor, alvo))
            elif tipo in TIPOS_DIRETOS:
                entradas.append((chave, dp, caminho, tipo, None, None, off))
            else:
                recusa["tipo %d de map script sem macro neste motor" % tipo] += 1
                pre_motivo[chave].append(
                    "tipo %d de map script sem macro neste motor" % tipo)

    # 2. quem precisa de flag de esconder: flag_fonte de objeto que ENTROU, nos
    #    mapas que recebem cena. Nada é alocado "por via das dúvidas".
    esconde_por_mapa = {}
    for chave in {c for c, *_ in entradas}:
        por_flag = collections.defaultdict(list)
        for l in gente_por_mapa.get(chave, []):
            if (l["tipo"] == "objeto" and l.get("flag_fonte")
                    and l["motivo"].startswith("entrou")):
                por_flag[l["flag_fonte"]].append(l["i"] + 1)
        esconde_por_mapa[chave] = dict(por_flag)

    # 3. UMA var por mapa, e a escolha é medida: entre as vars de estado que a
    #    fonte usa nas tabelas daquele mapa, ganha a que tem MAIS entradas
    #    (empate resolve pelo endereço menor, para a escolha não depender da
    #    ordem de leitura). As entradas das outras vars saem com motivo; é o
    #    preço declarado do desenho aprovado em 21/08.
    quantas = collections.defaultdict(collections.Counter)
    for chave, _d, _p, tipo, var, _val, alvo in entradas:
        if tipo in TIPOS_TABELA and alvo is not None and 0x4010 <= var < 0x4200:
            quantas[chave][var] += 1
    var_escolhida = {c: max(v, key=lambda a: (v[a], -a)) for c, v in quantas.items()}

    # 4. tradução, cena a cena, em DUAS passadas com a mesma ordem. A primeira
    #    usa nome de VAR e de FLAG de ensaio, só para descobrir quais cenas
    #    passam no filtro e o que cada uma consome; a segunda escreve com os
    #    nomes de verdade. Assim endereço só é gasto por cena que ENTROU (var
    #    declarada e nunca citada é a dívida que a própria medição de 21/08
    #    contou: 28 casos), e a alocação continua estável entre rodadas porque a
    #    ordem é a da chave da fonte, nunca a da descoberta.
    def traduz(nome_var_de, nome_flag_de):
        """(cenas, recusas, mapas que usaram var, {(chave, flag)} acesas)."""
        fora, motivos, com_var, acesas = [], collections.Counter(), set(), set()
        # Mesmo motivo, guardado POR MAPA DA FONTE: o Counter acima serve ao
        # relatorio, e este serve a FILA, que cobra por mapa e precisa saber o
        # que travou AQUELE mapa, e nao quantas vezes cada motivo apareceu.
        por_mapa_motivo = collections.defaultdict(list)
        compartilhado = {}
        for chave, dp, caminho, tipo, var, valor, alvo in entradas:
            if alvo is None:
                motivos["entrada de map script com ponteiro sujo"] += 1
                por_mapa_motivo[chave].append("entrada de map script com ponteiro sujo")
                continue
            if tipo in TIPOS_TABELA and not (0x4010 <= var < 0x4200):
                motivos["tabela aponta para var que nao e de save"] += 1
                por_mapa_motivo[chave].append("tabela aponta para var que nao e de save")
                continue
            if tipo in TIPOS_TABELA and var_escolhida.get(chave) != var:
                # O PREÇO do desenho "uma var por MAPA", dito em voz alta: a
                # fonte usa duas vars de estado no mesmo mapa e aqui só cabe
                # uma. A segunda sai com motivo, nunca dividindo a mesma casa
                # com a primeira, que é o defeito calado que isto evita.
                motivos["segundo estado no mesmo mapa: o desenho e uma var por "
                        "MAPA"] += 1
                por_mapa_motivo[chave].append("segundo estado no mesmo mapa: o desenho e uma var por "
                        "MAPA")
                continue
            esconde = esconde_por_mapa[chave]
            nome = nome_var_de(chave)
            t = Tradutor(rom, tab, cmap,
                         de_para_de_objetos(chave, docs[caminho], gente_por_mapa),
                         esconde, {var: nome} if nome else {},
                         {f: nome_flag_de(chave, f) for f in esconde}, musica)
            base = rotulo_de(chave, "t%d_%s" % (tipo, "x" if valor is None
                                                else "v%d" % valor))
            t.tipo_map_script = tipo
            # A quem o caderno de falta de traducao cobra este texto: a linha de
            # map_script daquele mapa da fonte, que e como a fila o chama.
            t.chave_da_fila = "%s/map_script" % chave
            try:
                linhas_inc, usadas = t.cena(alvo, base)
            except Recusa as e:
                motivos[str(e)] += 1
                por_mapa_motivo[chave].append(str(e))
                continue
            acesas |= {(chave, f) for f in t.usou_flag}
            if tipo in TIPOS_TABELA:
                com_var.add(chave)
            # DEDUPE: 12 mapas da Wild Area apontam para o MESMO offset da
            # fonte. Emitir doze cópias byte a byte iguais é gastar ROM sem
            # mudar nada; o segundo mapa em diante aponta para o corpo do
            # primeiro. Só vale quando a cena não cita var (var é por mapa).
            corpo_dono = None
            if nome is None:
                corpo_dono = compartilhado.get(alvo)
                if corpo_dono is None:
                    compartilhado[alvo] = base
            fora.append(dict(chave=chave, nome=dp["nome"], caminho=caminho,
                             tipo=tipo, var=var, valor=valor,
                             base=corpo_dono or base,
                             linhas=[] if corpo_dono else linhas_inc,
                             usadas=usadas))
        return fora, motivos, com_var, acesas, por_mapa_motivo

    _ensaio, _mot, com_var, acesas, _pm = traduz(
        lambda c: "VAR_GALAR_ENSAIO", lambda c, f: "FLAG_GALAR_ENSAIO_%03X" % f)

    livres = vars_livres()
    # TIRAR DA LISTA O QUE O IRMÃO JÁ TOMOU, e isto nasceu de um REPROVA de
    # `dev_scripts/guarda_colisao_vars.py` em 06/09/2026, no bloco c6.
    # `vars_livres()` apaga TODOS os blocos "Fase de conteudo de Galar" do
    # header antes de medir (é o que mantém a alocação estável entre rodadas),
    # então as vars que o c4d (`objetos_galar.py`) já gravou voltam a aparecer
    # como livres. `aloca_append_only` só sabe do teto dos nomes DESTA rodada,
    # e a primeira var nova caiu em 0x4113, em cima de `VAR_GALAR_G00M17_OBJ`.
    # Duas cenas dividindo a mesma casa de save é defeito calado: o portão
    # pegou, e o conserto é aqui, na entrada da alocação, não no portão.
    ja_de_outro = {e for n, e in FL.apelidos_gravados(
        VARS_H, "VAR_GALAR_", "UNUSED_0x").items()
        if n not in {"VAR_GALAR_%s_CENA" % c.upper() for c in com_var}}
    livres = [e for e in livres if e not in ja_de_outro]
    if len(com_var) > min(ORCAMENTO_VARS, len(livres) - RESERVA_VARS):
        raise SystemExit("PARE: %d mapas pedem var, o orcamento e %d e ha %d "
                         "livres" % (len(com_var), ORCAMENTO_VARS, len(livres)))
    # APPEND-ONLY (ver flags_livres.aloca_append_only): a var ja gravada em
    # vars.h NAO muda de endereco. Ate 23/08/2026 era `livres[i]` sobre
    # `sorted(com_var)`, e VAR_GALAR_G09M11_CENA, entrando no meio, empurrou
    # VAR_GALAR_G21M01_CENA de 0x410A para 0x410B entre duas ROMs.
    nomes_c = {c: "VAR_GALAR_%s_CENA" % c.upper() for c in com_var}
    ende_c = FL.aloca_append_only(
        nomes_c.values(), livres,
        FL.apelidos_gravados(VARS_H, "VAR_GALAR_", "UNUSED_0x"))
    vars_alocadas = {c: (nomes_c[c], ende_c[nomes_c[c]]) for c in sorted(com_var)}
    pool = flags_livres_de_galar(None)
    # REUSAR ANTES DE ALOCAR, e isso nao e economia de flag: e correcao.
    #
    # O bloco c4b (`objetos_galar.py`) ja batiza UMA flag por FLAG DE ESCONDER DA
    # FONTE, com o nome `FLAG_GALAR_ESCONDE_<hex da flag da fonte>`, e e ESSA que
    # vai parar no campo `flag` do object_event no map.json. Enquanto o c3
    # alocava outra para o MESMO numero, a cena acendia uma flag que NINGUEM le:
    # o `removeobject` so valia a sessao de mapa e os dois NPCs voltavam ao
    # reentrar. Medido em 23/08/2026 no `Galar_Hammerlocke05`, a primeira cena
    # desta casa que pediu flag de esconder: ela acendia
    # FLAG_GALAR_ESCONDE_G09M11_230 e os objetos 1 e 2 do map.json escondiam por
    # FLAG_GALAR_ESCONDE_230, duas vagas diferentes (0x1C89 e 0x1C81).
    #
    # ORDEM: isto depende de o c4b ter rodado antes, que ja e a ordem escrita no
    # cabecalho (fala, objetos, estaticos). Se o nome do c4b ainda nao existir no
    # header, o c3 aloca o proprio, como fazia antes, e a cena continua correta
    # dentro da sessao de mapa; o que se perde e a permanencia.
    _fh = open(FLAGS_H).read()

    def _do_c4b(f):
        """O nome que o bloco c4b deu a esta flag da fonte, ou None."""
        n = "FLAG_GALAR_ESCONDE_%03X" % f
        return n if ("#define %s " % n) in _fh else None

    reusadas = {(c, f): _do_c4b(f) for c, f in acesas if _do_c4b(f)}
    novas = sorted(x for x in acesas if x not in reusadas)
    if len(novas) > len(pool):
        raise SystemExit("PARE: %d flags de esconder pedidas e %d livres na "
                         "faixa de Galar" % (len(novas), len(pool)))
    nomes = {k: (v, None) for k, v in reusadas.items()}
    nomes.update({(c, f): ("FLAG_GALAR_ESCONDE_%s_%03X" % (c.upper(), f), pool[i])
                  for i, (c, f) in enumerate(novas)})


    aceitas, motivos, _cv, _ac, por_mapa_motivo = traduz(
        lambda c: vars_alocadas[c][0] if c in vars_alocadas else None,
        lambda c, f: nomes[(c, f)][0] if (c, f) in nomes else None)
    recusa.update(motivos)
    for chave, ms in pre_motivo.items():
        por_mapa_motivo[chave].extend(ms)
    # So o que o c3 alocou entra no bloco do header: a flag reusada do c4b
    # ja esta declarada la, e declarar duas vezes e colisao de verdade.
    return (aceitas, recusa, vars_alocadas,
            sorted(v for v in nomes.values() if v[1] is not None),
            censo, docs, por_mapa_motivo)


# ------------------------------------------------------------------ saída ----
def corpo_inc(aceitas):
    out = ["@ Cenas de map script de Galar (bloco c3 da fase de conteudo).",
           "@ Gerado por dev_scripts/cenas_galar.py; NAO editar a mao.",
           "@ A cena vem do demake (fontes-mapas/galar-swsh), desmontada do",
           "@ bytecode do FireRed. O que nao coube saiu com motivo contado.",
           ""]
    por_mapa = collections.defaultdict(list)
    for a in aceitas:
        por_mapa[(a["chave"], a["nome"])].append(a)
    for chave, nome in sorted(por_mapa):
        out.append("@ ---- %s (%s) ----" % (nome, chave))
        vistos = set()
        for a in sorted(por_mapa[(chave, nome)], key=lambda z: z["base"]):
            if a["base"] in vistos:
                continue
            vistos.add(a["base"])
            out.extend(a["linhas"])
            out.append("")
    return "\n".join(out) + "\n"


def corpo_scripts_inc(nome, aceitas_do_mapa):
    """A tabela `Galar_X_MapScripts` do mapa, com as cenas que passaram."""
    out = ["@ Gerado por dev_scripts/cenas_galar.py (blocos c3 e c6 da fase",
           "@ de conteudo). Rodar dev_scripts/mundo_galar.py apaga este",
           "@ arquivo; rodar cenas_galar.py --aplicar o repoe. Corpo das",
           "@ cenas em data/scripts/galar_cenas.inc.", "",
           "%s_MapScripts::" % nome]
    tabelas = collections.defaultdict(list)
    diretos = []
    for a in sorted(aceitas_do_mapa, key=lambda z: (z["tipo"], z["base"])):
        if a["tipo"] in TIPOS_TABELA:
            tabelas[a["tipo"]].append(a)
        else:
            diretos.append(a)
    for a in diretos:
        out.append("\tmap_script %s, %s" % (MACRO_DIRETO[a["tipo"]], a["base"]))
    for tipo in sorted(tabelas):
        out.append("\tmap_script %s, %s_Tabela%d"
                   % (MACRO_TABELA[tipo], nome, tipo))
    out.append("\t.byte 0")
    for tipo in sorted(tabelas):
        out.append("")
        out.append("%s_Tabela%d:" % (nome, tipo))
        for a in tabelas[tipo]:
            out.append("\tmap_script_2 %s, %d, %s"
                       % (a["var_nome"], a["valor"], a["base"]))
        out.append("\t.2byte 0")
    return "\n".join(out) + "\n"


def texto_do_scripts_inc(caminho, nome, aceitas_do_mapa):
    """O `scripts.inc` inteiro: a tabela DESTE gerador mais os blocos marcados
    de outro dono que já estavam no arquivo, colados de volta no fim, na mesma
    forma que o dono deles usa (`rstrip` mais linha em branco)."""
    texto = corpo_scripts_inc(nome, aceitas_do_mapa)
    for bloco in blocos_de_outro_dono(caminho):
        texto = texto.rstrip("\n") + "\n\n" + bloco + "\n"
    return texto


def bloco_vars(vars_alocadas):
    if not vars_alocadas:
        return ""
    out = [MARCA_VAR_INI,
           "// Uma var por MAPA de Galar com tabela de map script (tipo 2 ou 4",
           "// do FireRed), com o VALOR codificando a etapa da cena, que e o",
           "// que o proprio FireRed faz com VAR_MAP_SCENE_*. Decisao da",
           "// condutora em 21/08/2026.",
           "// Apelidar VAR_UNUSED nao mexe em VARS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/cenas_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in vars_alocadas.values()) + 2
    for chave in sorted(vars_alocadas):
        nome, end = vars_alocadas[chave]
        out.append("#define %-*s VAR_UNUSED_0x%04X  // mapa %s da fonte"
                   % (larg, nome, end, chave))
    out.append(MARCA_VAR_FIM)
    return com_caudas_manuais("\n".join(out) + "\n", VARS_H,
                              MARCA_VAR_INI, MARCA_VAR_FIM)


def bloco_flags(usadas_flag):
    if not usadas_flag:
        return ""
    out = [MARCA_FLAG_INI,
           "// Flag de esconder que a FONTE pendurou no objeto (flag_fonte do",
           "// censo do G4), traduzida para a faixa de Galar. Ver a DECISAO no",
           "// cabecalho de dev_scripts/cenas_galar.py.",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/cenas_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in usadas_flag) + 2
    for nome, end in sorted(usadas_flag):
        out.append("#define %-*s FLAG_UNUSED_0x%04X" % (larg, nome, end))
    out.append(MARCA_FLAG_FIM)
    return com_caudas_manuais("\n".join(out) + "\n", FLAGS_H,
                              MARCA_FLAG_INI, MARCA_FLAG_FIM)


def aplica(aceitas, vars_alocadas, usadas_flag, docs, gravar):
    for a in aceitas:
        a["var_nome"] = (vars_alocadas[a["chave"]][0]
                         if a["chave"] in vars_alocadas else None)
    mudou = collections.Counter()
    corpo = corpo_inc(aceitas)
    if gravar:
        open(INC, "w").write(corpo)
        fonte = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_cenas.inc"'
        if linha not in fonte:
            open(EVENT_S, "w").write(fonte.rstrip("\n") + "\n" + linha + "\n")
    por_mapa = collections.defaultdict(list)
    for a in aceitas:
        por_mapa[a["nome"]].append(a)
    for nome, lista in sorted(por_mapa.items()):
        caminho = "%s/data/maps/%s/scripts.inc" % (RAIZ, nome)
        texto = texto_do_scripts_inc(caminho, nome, lista)
        if not os.path.exists(caminho) or open(caminho).read() != texto:
            mudou["scripts.inc"] += 1
            if gravar:
                open(caminho, "w").write(texto)
    for arq, marca_i, marca_f, bloco in (
            (VARS_H, MARCA_VAR_INI, MARCA_VAR_FIM, bloco_vars(vars_alocadas)),
            (FLAGS_H, MARCA_FLAG_INI, MARCA_FLAG_FIM, bloco_flags(usadas_flag))):
        atual = open(arq).read()
        novo = poe_bloco(atual, marca_i, marca_f, bloco)
        if novo != atual:
            mudou[os.path.basename(arq)] += 1
            if gravar:
                open(arq, "w").write(novo)
    del docs
    return mudou, corpo


# ------------------------------------------------------------------ demo -----
def demo():
    falhas = []
    aceitas, recusa, vars_alocadas, usadas_flag, censo, docs, motivos_mapa = plano()

    # 1. A CONSTANTE que o rascunho errou. Tipo 3 e ON_TRANSITION, tipo 2 e
    #    ON_FRAME_TABLE: se o header da fonte mudar, este caso cai antes de o
    #    gerador escrever a tabela errada num mapa.
    tipos = constantes(f"{PKFR}/include/constants/map_scripts.h", "MAP_SCRIPT")
    if tipos.get("MAP_SCRIPT_ON_TRANSITION") != 3 or \
            tipos.get("MAP_SCRIPT_ON_FRAME_TABLE") != 2:
        falhas.append("os tipos de map script do FireRed mudaram: %r" % tipos)

    # 2. A tradução de movimento é POR NOME e as tabelas divergem de verdade:
    #    se um dia passarem a bater por valor, este caso avisa em vez de deixar
    #    a tradução silenciosamente redundante virar tradução por valor.
    de_para, nomes = tradutor_por_nome(
        f"{PKFR}/include/constants/event_object_movement.h",
        f"{RAIZ}/include/constants/event_object_movement.h", "MOVEMENT_ACTION")
    diferentes = sum(1 for v, alvo in de_para.items()
                     if alvo is not None and alvo != v)
    if diferentes < 100:
        falhas.append("so %d passos de movimento mudam de valor entre FR e nos; "
                      "a traducao por nome era o motivo de este arquivo existir"
                      % diferentes)

    # 3. faixa de var: dentro do medido, sem repetir, dentro do orçamento e com
    #    a reserva de pe.
    livres = vars_livres()
    ends = [e for _n, e in vars_alocadas.values()]
    if len(set(ends)) != len(ends):
        falhas.append("var de cena repetida")
    if any(e not in livres for e in ends):
        falhas.append("var de cena fora da faixa medida como livre")
    if len(ends) > ORCAMENTO_VARS:
        falhas.append("estourou o orcamento de %d vars" % ORCAMENTO_VARS)
    if len(livres) - len(ends) < RESERVA_VARS:
        falhas.append("sobram %d vars, menos que a reserva de %d"
                      % (len(livres) - len(ends), RESERVA_VARS))

    # 4. rótulo único: rótulo repetido faz o assembler juntar duas cenas.
    rot = [l[:-2] for a in aceitas for l in a["linhas"] if l.endswith("::")]
    if len(set(rot)) != len(rot):
        falhas.append("rotulo de cena repetido")

    # 5. IDEMPOTÊNCIA: gerar duas vezes dá o mesmo texto, e aplicar em cima do
    #    que já está gravado não mexe em arquivo nenhum.
    mudou, corpo1 = aplica(aceitas, vars_alocadas, usadas_flag, docs, False)
    if corpo1 != corpo_inc(aceitas):
        falhas.append("o .inc nao e estavel entre duas geracoes")
    if os.path.exists(INC) and open(INC).read() == corpo1 and mudou:
        falhas.append("segunda passada ainda mexeria em %r: nao e idempotente"
                      % dict(mudou))

    # 6. MUTAÇÃO PLANTADA, a que a condutora pediu: DUAS vars de Galar apontando
    #    para o MESMO endereço tem que REPROVAR no portão de colisão. O plante
    #    entra numa árvore de mentira, com os headers copiados e o resto do repo
    #    por link, exatamente como o `--demo` do próprio portão faz.
    GUARDA.usa("vars")
    with tempfile.TemporaryDirectory() as tmp:
        for h in list(GUARDA.HEADERS) + [os.path.join("include", p)
                                         for p in GUARDA.PONTA]:
            destino = os.path.join(tmp, h)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            if not os.path.exists(destino):
                shutil.copy(os.path.join(RAIZ, h), destino)
        for r in ("data", "src", "test"):
            os.symlink(os.path.join(RAIZ, r), os.path.join(tmp, r))
        os.makedirs(os.path.join(tmp, "plante"))
        # A vaga do plante é uma AINDA LIVRE da faixa medida (nunca uma que
        # este gerador já apelidou): o que se prova aqui é que DUAS frentes
        # apelidando a MESMA vaga reprovam, não que a alocação de hoje briga
        # com ela mesma.
        vaga = [v for v in livres if v not in ends][-1]
        caminho = os.path.join(tmp, "include/constants/vars.h")
        texto = open(caminho).read()
        corte = texto.rindex("#endif")
        open(caminho, "w").write(
            texto[:corte]
            + "#define VAR_GALAR_PLANTADA_A VAR_UNUSED_0x%04X\n" % vaga
            + "#define VAR_GALAR_PLANTADA_B VAR_UNUSED_0x%04X\n" % vaga
            + texto[corte:])
        raizes = ["data", "src", "include", "test", "plante"]
        open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
            "VAR_GALAR_PLANTADA_A VAR_GALAR_PLANTADA_B\n")
        # A lista autorizada é a DE VERDADE: as 23 colisões herdadas do merge
        # de FRLG não são assunto deste caso, e escondê-las com uma lista vazia
        # trocaria a prova por ruído.
        aut = GUARDA.AUTORIZADAS
        novas = GUARDA.portao(base=tmp, raizes=raizes,
                              caminho_autorizadas=aut, verboso=False)
        if not (len(novas) == 1 and int(novas[0]["endereco"], 16) == vaga
                and set(novas[0]["nomes"]) == {"VAR_GALAR_PLANTADA_A",
                                               "VAR_GALAR_PLANTADA_B"}):
            falhas.append("duas vars de Galar na mesma vaga NAO reprovaram: %r"
                          % novas)
        # e o par negativo: uma alocação sozinha não pode brigar com o rótulo.
        open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
            "VAR_GALAR_PLANTADA_A\n")
        if GUARDA.portao(base=tmp, raizes=raizes, caminho_autorizadas=aut,
                         verboso=False):
            falhas.append("alocacao sozinha reprovou; o portao viraria ruido")

    # 7. o portão da árvore de VERDADE continua verde depois desta leva.
    if GUARDA.portao(verboso=False):
        falhas.append("o portao de colisao de vars esta vermelho na arvore")

    # 8. ONDA 3, LOTE L1: o pipeline nasce em ingles, e cena com texto sem
    #    traducao NAO e escrita. O caso comum vale para os tres geradores; o
    #    de baixo e o desta casa: `Tradutor.texto` tem de RECUSAR a cena
    #    inteira, e nao devolver um bloco meio traduzido.
    falhas.extend(FALA.demo_pipeline_ingles())
    velha = FALA.traducao()
    try:
        qa = FALA.Traducao(traducao="/nao/existe.json", resgate="/nao/existe.json")
        FALA.reinicia_traducao(qa)
        de_texto = FALA.texto
        FALA.texto = lambda *_a, **_k: ("qa aqui uma seu sua", None)
        falso = Tradutor.__new__(Tradutor)
        falso.rom, falso.cmap = b"\0" * 16, {}
        falso.chave_da_fila = "qa/objeto/0"
        try:
            Tradutor.texto(falso, BASE, "QA_Cena_Text")
            falhas.append("cena com texto sem traducao NAO foi recusada")
        except Recusa as e:
            if "sem traducao" not in str(e):
                falhas.append("recusa de texto sem traducao com outro motivo: %s" % e)
        if "qa/objeto/0" not in qa.chaves_faltando():
            falhas.append("a cena recusada nao deixou o texto no caderno de falta")
        qa.por_rotulo["QA_Cena_Text"] = "Answer by the label."
        if Tradutor.texto(falso, BASE, "QA_Cena_Text") != [
                "QA_Cena_Text:", '\t.string "Answer by the label.$"']:
            falhas.append("cena COM traducao nao saiu em ingles")
    finally:
        FALA.texto = de_texto
        FALA.reinicia_traducao(velha)

    # 9. ONDA 4, LOTE P, MUTAÇÃO PLANTADA: bloco de OUTRO DONO sobrevive.
    #    O `--aplicar` reescreve `scripts.inc` dos mapas com cena, e um desses
    #    mapas (Galar_Wedgehurst03) guarda o bloco da Dex de Galar, escrito
    #    pelo `distribui_dex.py`. Até 06/09/2026 ele era apagado calado. O
    #    plante é um bloco de dono inventado num arquivo de mentira: ele tem de
    #    sair do outro lado BYTE A BYTE, e a segunda passada não pode mexer.
    algum = collections.defaultdict(list)
    for a_ in aceitas:
        algum[a_["nome"]].append(a_)
    nome_qa, lista_qa = sorted(algum.items())[0]
    alheio = ("@ >>> Bloco de outro dono (dev_scripts/qa_plantado.py) >>>\n"
              "QaPlantado_EventScript_Nada::\n\tend\n"
              "@ <<< Bloco de outro dono <<<")
    with tempfile.TemporaryDirectory() as tmp:
        caminho = os.path.join(tmp, "scripts.inc")
        open(caminho, "w").write(
            "Galar_Velho_MapScripts::\n\t.byte 0\n\n" + alheio + "\n")
        saiu = texto_do_scripts_inc(caminho, nome_qa, lista_qa)
        if alheio not in saiu:
            falhas.append("bloco de outro dono NAO sobreviveu ao --aplicar")
        if corpo_scripts_inc(nome_qa, lista_qa).rstrip("\n") not in saiu:
            falhas.append("a tabela deste gerador sumiu ao preservar o alheio")
        open(caminho, "w").write(saiu)
        if texto_do_scripts_inc(caminho, nome_qa, lista_qa) != saiu:
            falhas.append("preservar bloco alheio quebrou a idempotencia")
        # e o par negativo: arquivo sem bloco marcado sai igual ao de sempre.
        open(caminho, "w").write("Galar_Velho_MapScripts::\n\t.byte 0\n")
        if texto_do_scripts_inc(caminho, nome_qa, lista_qa) != \
                corpo_scripts_inc(nome_qa, lista_qa):
            falhas.append("arquivo sem bloco alheio mudou de forma")

    # 10. ONDA 4, LOTE P: comentário escrito À MÃO no bloco de vars sobrevive.
    #     A linha real é a do VAR_GALAR_G10M23_CENA, que carrega desde 07/09 a
    #     nota de por que o endereço mudou. O gerador escrevia só "mapa X da
    #     fonte" e comia a nota a cada `--aplicar`.
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "vars.h")
        corpo_qa = ("%s\n#define VAR_QA_UM   VAR_UNUSED_0x4100  // mapa qa1 da fonte\n"
                    "#define VAR_QA_DOIS VAR_UNUSED_0x4101  // mapa qa2 da fonte\n%s\n"
                    % (MARCA_VAR_INI, MARCA_VAR_FIM))
        mao = corpo_qa.replace("// mapa qa1 da fonte",
                               "// mapa qa1 da fonte (movida a mao em 07/09/2026)")
        open(h, "w").write(mao)
        saiu = com_caudas_manuais(corpo_qa, h, MARCA_VAR_INI, MARCA_VAR_FIM)
        if saiu != mao:
            falhas.append("comentario a mao no vars.h nao sobreviveu: %r" % saiu)
        if com_caudas_manuais(saiu, h, MARCA_VAR_INI, MARCA_VAR_FIM) != saiu:
            falhas.append("preservar comentario a mao quebrou a idempotencia")
        # par negativo: se o ENDEREÇO mudar, a nota fala de outro endereço e cai.
        outro = corpo_qa.replace("VAR_UNUSED_0x4100", "VAR_UNUSED_0x4102")
        if com_caudas_manuais(outro, h, MARCA_VAR_INI, MARCA_VAR_FIM) != outro:
            falhas.append("nota a mao sobreviveu a troca de endereco")

    # 11. ONDA 5, LOTE S: EMPATE DE TILE no `de_para_de_objetos`, com caso
    #     plantado. Empate com a MESMA contagem casa por ordem; contagem
    #     diferente continua recusando; e o tile de um objeto só não muda.
    def _linha(i, x, y, motivo="entrou mudo"):
        return {"tipo": "objeto", "i": i, "x": x, "y": y, "motivo": motivo}

    doc_qa = {"object_events": [{"x": 3, "y": 3}, {"x": 9, "y": 1},
                                {"x": 3, "y": 3}, {"x": 7, "y": 7}]}
    gente_qa = {"qa": [_linha(0, 3, 3), _linha(1, 9, 1), _linha(2, 3, 3),
                       _linha(3, 7, 7), _linha(4, 7, 7)]}
    #  (3,3): 2 nossos e 2 da fonte -> casa por ordem, 1->1 e 3->3
    #  (9,1): 1 e 1 -> como sempre
    #  (7,7): 1 nosso e 2 da fonte -> os dois caem no mesmo, comportamento antigo
    esperado = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4}
    saiu = de_para_de_objetos("qa", doc_qa, gente_qa)
    if saiu != esperado:
        falhas.append("empate de tile: esperava %r, veio %r" % (esperado, saiu))
    #  contagem DIFERENTE no tile empatado continua recusando os dois lados.
    gente_dif = {"qa": [_linha(0, 3, 3), _linha(1, 9, 1)]}
    saiu = de_para_de_objetos("qa", doc_qa, gente_dif)
    if saiu != {2: 2}:
        falhas.append("empate com contagem diferente devia recusar, veio %r" % saiu)
    #  e registro que o filtro G4 nao aprovou nao conta para a contagem.
    gente_impossivel = {"qa": [_linha(0, 3, 3), _linha(1, 3, 3),
                               _linha(2, 3, 3, "grafico e pokemon, nao vira NPC")]}
    saiu = de_para_de_objetos("qa", doc_qa, gente_impossivel)
    if saiu != {1: 1, 2: 3}:
        falhas.append("registro impossivel entrou na contagem do empate: %r" % saiu)

    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    for f in falhas:
        print("  FALHA", f)
    relatorio(aceitas, recusa, vars_alocadas, usadas_flag, censo, livres)
    return 1 if falhas else 0


def relatorio(aceitas, recusa, vars_alocadas, usadas_flag, censo, livres=None):
    livres = vars_livres() if livres is None else livres
    print("\nentradas de map script na fonte, por tipo do FireRed:")
    for k in sorted(censo):
        print("  %-10s %d" % (k, censo[k]))
    print("\ncenas portadas: %d em %d mapas"
          % (len(aceitas), len({a["nome"] for a in aceitas})))
    por_tipo = collections.Counter(a["tipo"] for a in aceitas)
    for t in sorted(por_tipo):
        print("  tipo %d: %d" % (t, por_tipo[t]))
    print("\nvars: %d alocadas, %d livres medidas, %d sobrando "
          "(orcamento %d, reserva %d)"
          % (len(vars_alocadas), len(livres), len(livres) - len(vars_alocadas),
             ORCAMENTO_VARS, RESERVA_VARS))
    print("flags de esconder alocadas: %d" % len(usadas_flag))
    print("\nde fora, por motivo (%d no total):" % sum(recusa.values()))
    for m, c in recusa.most_common(20):
        print("  %5d  %s" % (c, m))


# Motivo que NUNCA vai mudar sozinho: o dado da fonte nao existe ou nao e
# legivel, e nenhuma decisao nossa o traz de volta. Linha assim vira
# `descartada`. Todo o resto vira `adiada`, porque uma decisao futura (um
# de-para de heal location, um special novo, uma var por mapa a mais) destrava.
MOTIVO_TERMINAL = (
    "cena vira no-op depois da traducao",
    "entrada de map script com ponteiro sujo",
    "ponteiro de map script fora da rom",
    "decodificacao incompleta",
    "tabela de tipo 2/4 vazia",
    "tabela aponta para var que nao e de save",
    "nao esconde objeto importado",
    "mapa da fonte fora do de-para do G3",
    "map.json do mapa nao existe",
)


def devolve_para_fila(aceitas, motivos_mapa, gravar):
    """Escreve na fila o motivo MEDIDO de cada mapa de map_script recusado.

    A fila cobra POR MAPA (`<chave>/map_script`) e calcula `feita` lendo a
    arvore. O que ela nao sabe calcular e por que um mapa NAO entrou, e sem
    isso as linhas voltam pendentes a cada varredura, sem nada escrito, e a
    proxima rodada remede tudo de novo. Aqui o motivo volta como `status` +
    `motivo_do_status`, que `fila_galar.decisoes_anteriores` preserva.

    Mapa que RECEBEU cena nao e tocado: quem manda nele e o rotulo na arvore.
    Linha que JA TEM decisao (`descartada` ou `adiada`) tambem nao e tocada,
    pela lei do cabecalho de `fila_galar.py`: "status que alguem escreveu nao
    pode ser apagado por uma regeneracao". Ate 06/09/2026 este laco so pulava
    `feita`, e uma decisao escrita a mao pela condutora seria sobrescrita pelo
    motivo do gerador na rodada seguinte, calada.
    """
    import json as _json
    fila = f"{RAIZ}/dev_scripts/fila_galar.json"
    doc = _json.load(open(fila))
    feitos = {a["chave"] for a in aceitas}
    n, quadro = 0, collections.Counter()
    for l in doc["linhas"]:
        if (l["tipo"] != "map_script"
                or l["status"] in ("feita", "descartada", "adiada")):
            continue
        chave = l["mapa_fonte"]
        if chave in feitos:
            continue
        ms = motivos_mapa.get(chave)
        if not ms:
            continue
        conta = collections.Counter(ms)
        texto = "; ".join("%s (x%d)" % (m, k) if k > 1 else m
                          for m, k in conta.most_common())
        st = ("descartada"
              if all(any(t in m for t in MOTIVO_TERMINAL) for m in conta)
              else "adiada")
        novo = st, ("bloco c6, lote C da onda 1, 06/09/2026: " + texto)
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
        quadro[st] += 1
    if gravar and n:
        with open(fila, "w") as f:
            _json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return n, quadro


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--fila", action="store_true",
                    help="devolve o motivo medido de cada mapa recusado para "
                         "dev_scripts/fila_galar.json (use junto com --aplicar "
                         "para gravar)")
    ap.add_argument("--falta", action="store_true",
                    help="grava SO dev_scripts/onda3_falta_traduzir.json e o "
                         "motivo na fila; nao toca .inc, map.json nem header. "
                         "Existe porque `--aplicar` deste arquivo reescreve os "
                         "438 data/maps/Galar_*/scripts.inc, e o bloco da Dex "
                         "de Galar mora la (ver ESTADO-CARTUCHO-2.md, onda 2).")
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    aceitas, recusa, vars_alocadas, usadas_flag, censo, docs, motivos_mapa = plano()
    if a.falta:
        print("textos sem traducao (distintos): %d, em %d linhas da fila"
              % (len(FALA.traducao().faltam),
                 len(FALA.traducao().chaves_faltando())))
        if FALA.traducao().grava_falta(True):
            print("gravado %s" % FALA.FALTA_JSON)
        print("fila: %d linhas adiadas por texto sem traducao"
              % FALA.marca_fila_sem_traducao(True))
        raise SystemExit(0)
    mudou, _corpo = aplica(aceitas, vars_alocadas, usadas_flag, docs, a.aplicar)
    if a.fila:
        n, quadro = devolve_para_fila(aceitas, motivos_mapa, a.aplicar)
        print("fila: %d linhas de map_script ganharam motivo medido" % n)
        for st, c in sorted(quadro.items()):
            print("   %-12s %d" % (st, c))
    relatorio(aceitas, recusa, vars_alocadas, usadas_flag, censo)
    print("traducao na geracao: %s" % dict(FALA.traducao().conta))
    print("textos sem traducao (distintos): %d, em %d linhas da fila"
          % (len(FALA.traducao().faltam),
             len(FALA.traducao().chaves_faltando())))
    if a.aplicar:
        if FALA.traducao().grava_falta(True):
            print("gravado %s" % FALA.FALTA_JSON)
        print("fila: %d linhas adiadas por texto sem traducao"
              % FALA.marca_fila_sem_traducao(True))
    if a.aplicar:
        print("\ngravado: %r" % dict(mudou))
    else:
        print("\n(nada gravado; use --aplicar). mudaria: %r" % dict(mudou))


if __name__ == "__main__":
    main()
