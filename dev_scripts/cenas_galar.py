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
# Byte de enchimento de espaço livre da ROM do FireRed.
ENCHIMENTO = 0xFF


# ----------------------------------------------------------------- leitura ---
def constantes(caminho, prefixo):
    """{nome: valor} dos `#define PREFIXO_*` de um header, sem pré-processador.

    Serve para as duas tabelas que este arquivo traduz POR NOME (movimento e
    clima). Corpo que não é número inteiro é ignorado de propósito: alias não é
    entrada de tabela de tradução.
    """
    fora = {}
    for m in re.finditer(r"^#define\s+(%s_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)"
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
        fora.append((var, valor,
                     ptr - BASE if BASE <= ptr < BASE + len(rom) else None))
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
                  "fadedefaultbgm", "hidemonpic", "waitmoncry"}
IGUAIS_COM_ARG = {"delay": 1, "playse": 1, "playfanfare": 1, "waitmovement": 1,
                  "fadescreen": 1, "textcolor": 1, "savebgm": 1, "random": 1}
# Comando que mexe em objeto pelo id LOCAL da fonte.
POR_ID = {"applymovement": 2, "addobject": 1, "removeobject": 1,
          "setobjectxyperm": 3, "setobjectxy": 3, "setobjectmovementtype": 2,
          "turnobject": 2}

# Comando que so emoldura a cena: nao muda nada que o jogador leve consigo.
# Cena cujo corpo traduzido so tem isto e no-op, e no-op nao entra.
MOLDURA = {"lock", "lockall", "release", "releaseall", "faceplayer", "end",
           "return", "delay", "waitstate", "closemessage", "waitmessage",
           "waitbuttonpress", "goto", "call", "goto_if", "call_if",
           "compare_var_to_value", "textcolor", "waitmovement"}

STD_MSGBOX = {2: "MSGBOX_NPC", 3: "MSGBOX_SIGN", 4: "MSGBOX_DEFAULT",
              5: "MSGBOX_YESNO", 6: "MSGBOX_AUTOCLOSE"}


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
        self.usou_flag = set()
        # DIR_* é enum no nosso global.h e #define no da fonte: a conferência é
        # pelo NOME aparecer no nosso header, que é o que o assembler vai pedir.
        self.dir_fonte = {v: k for k, v in constantes(
            f"{PKFR}/include/constants/global.h", "DIR").items()}
        self.dir_nossas = set(re.findall(r"\bDIR_[A-Z]+\b",
                                        open(f"{RAIZ}/include/constants/global.h").read()))

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
        if local >= 0x4000:
            raise Recusa("id de objeto vem de var (0x%04X), nao de literal"
                         % local)
        nosso = self.de_para_obj.get(local)
        if nosso is None:
            raise Recusa("objeto local %d nao entrou no mapa no G4" % local)
        return str(nosso)

    def var(self, endereco):
        if endereco == 0x800D:
            return "VAR_RESULT"
        if 0x8000 <= endereco <= 0x800F:
            return "VAR_0x%04X" % endereco
        nome = self.nome_da_var.get(endereco)
        if nome is None:
            raise Recusa("var salva 0x%04X da fonte sem dono nosso" % endereco)
        return nome

    def flag(self, f):
        nome = self.nome_da_flag.get(f)
        if nome is None:
            raise Recusa("flag 0x%03X da fonte nao esconde objeto importado "
                         "(e flag de motor do demake)" % f)
        return nome

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
        if not (BASE <= ptr < BASE + len(self.rom)):
            raise Recusa("ponteiro de texto fora da rom")
        t, motivo = FALA.texto(self.rom, self.cmap, ptr - BASE)
        if motivo:
            raise Recusa("texto recusado: " + motivo)
        return ["%s:" % rotulo, '\t.string "%s$"' % t]

    # -- a cena inteira -----------------------------------------------------
    def cena(self, inicio, base):
        """([linhas do .inc], usadas) ou levanta Recusa.

        `usadas` conta o que a cena consumiu (flags acesas, objetos escondidos),
        para o relatório poder somar sem reler o texto emitido.
        """
        bs, falha = blocos(self.rom, self.tab, inicio)
        if falha:
            raise Recusa("decodificacao incompleta: " + falha)
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
                    if args[0] not in self.nome_da_flag:
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
                elif nome in ("goto", "call"):
                    corpo.append("\t%s %s" % (self.macro(nome), alvo(args[0])))
                elif nome in ("goto_if", "call_if"):
                    corpo.append("\t%s %d, %s" % (self.macro(nome), args[0],
                                                  alvo(args[1])))
                else:
                    raise Recusa("comando de cena fora do filtro: " + nome)
                if nome not in MOLDURA:
                    usadas["efeito"] += 1
            corpo.append("")
        if not usadas["efeito"]:
            # Cena que, depois de tirar o que a nossa ROM não observa, virou
            # `release; end`. Escrever map script que não faz nada é pior que
            # não escrever: fica dívida com cara de trabalho feito.
            raise Recusa("cena vira no-op depois da traducao (so moldura)")
        return corpo + extras, usadas

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

    Casar por ORDEM seria quase certo e às vezes errado: 9 dos 391 mapas de
    Galar têm objeto NOSSO no meio da lista que não veio da fonte (marinheiro da
    travessia, bola do fala_galar), e a partir dele toda a numeração anda. Tile
    com dois objetos nossos reprova em vez de escolher, que é a lição de
    Oreburgh (ESTADO 0.g) e a mesma régua do `fala_galar.casa_objeto`.
    """
    por_tile = collections.defaultdict(list)
    for i, o in enumerate(doc.get("object_events", [])):
        por_tile[(o["x"], o["y"])].append(i + 1)
    fora = {}
    for l in gente_por_mapa.get(chave, []):
        if l["tipo"] != "objeto" or not l["motivo"].startswith("entrou"):
            continue
        nossos = por_tile.get((l["x"], l["y"]), [])
        if len(nossos) == 1:
            fora[l["i"] + 1] = nossos[0]
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
        texto = sem_bloco(open(limpo).read(), MARCA_VAR_INI, MARCA_VAR_FIM)
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
    """Faixa de Galar ainda livre, tirando o que este próprio bloco já apelidou."""
    texto = sem_bloco(open(FLAGS_H).read(), MARCA_FLAG_INI, MARCA_FLAG_FIM)
    tomadas = {int(m, 16) for m in re.findall(r"FLAG_UNUSED_0x([0-9A-Fa-f]{4})",
                                              texto)}
    del bloco_atual
    return [f for f in range(PRIMEIRA_FLAG_CENA, ULTIMA_FLAG_CENA + 1)
            if f not in tomadas]


def sem_bloco(texto, ini, fim):
    i = texto.find(ini)
    if i < 0:
        return texto
    j = texto.find(fim, i)
    j = len(texto) if j < 0 else j + len(fim) + 1
    return texto[:i] + texto[j:]


def poe_bloco(texto, ini, fim, corpo):
    """Idempotente: troca o bloco marcado, ou acrescenta no fim do arquivo."""
    limpo = sem_bloco(texto, ini, fim)
    if not corpo:
        return limpo
    return limpo.rstrip("\n") + "\n\n" + corpo


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

    # 1. inventário: cada linha da fila vira uma ou mais ENTRADAS de map script.
    entradas = []
    for l in sorted(linhas, key=lambda z: z["chave"]):
        chave = l["mapa_fonte"]
        dp = de_para.get(chave)
        if dp is None:
            recusa["mapa da fonte fora do de-para do G3"] += 1
            continue
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, dp["nome"])
        if not os.path.exists(caminho):
            recusa["map.json do mapa nao existe"] += 1
            continue
        if caminho not in docs:
            docs[caminho] = json.load(open(caminho))
        for tipo, off in FALA.tabela_de_map_script(rom, int(l["ponteiro_fonte"], 16)):
            censo["tipo %d" % tipo] += 1
            if off is None:
                recusa["ponteiro de map script fora da rom"] += 1
                continue
            if tipo in TIPOS_TABELA:
                itens = tabela_de_map_script_tipo2(rom, off)
                if not itens:
                    recusa["tabela de tipo 2/4 vazia"] += 1
                for var, valor, alvo in itens:
                    entradas.append((chave, dp, caminho, tipo, var, valor, alvo))
            elif tipo == 3:
                entradas.append((chave, dp, caminho, tipo, None, None, off))
            else:
                recusa["tipo %d de map script fora do bloco c3" % tipo] += 1

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
        compartilhado = {}
        for chave, dp, caminho, tipo, var, valor, alvo in entradas:
            if alvo is None:
                motivos["entrada de map script com ponteiro sujo"] += 1
                continue
            if tipo in TIPOS_TABELA and not (0x4010 <= var < 0x4200):
                motivos["tabela aponta para var que nao e de save"] += 1
                continue
            if tipo in TIPOS_TABELA and var_escolhida.get(chave) != var:
                # O PREÇO do desenho "uma var por MAPA", dito em voz alta: a
                # fonte usa duas vars de estado no mesmo mapa e aqui só cabe
                # uma. A segunda sai com motivo, nunca dividindo a mesma casa
                # com a primeira, que é o defeito calado que isto evita.
                motivos["segundo estado no mesmo mapa: o desenho e uma var por "
                        "MAPA"] += 1
                continue
            esconde = esconde_por_mapa[chave]
            nome = nome_var_de(chave)
            t = Tradutor(rom, tab, cmap,
                         de_para_de_objetos(chave, docs[caminho], gente_por_mapa),
                         esconde, {var: nome} if nome else {},
                         {f: nome_flag_de(chave, f) for f in esconde}, musica)
            base = rotulo_de(chave, "t%d_%s" % (tipo, "x" if valor is None
                                                else "v%d" % valor))
            try:
                linhas_inc, usadas = t.cena(alvo, base)
            except Recusa as e:
                motivos[str(e)] += 1
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
        return fora, motivos, com_var, acesas

    _ensaio, _mot, com_var, acesas = traduz(
        lambda c: "VAR_GALAR_ENSAIO", lambda c, f: "FLAG_GALAR_ENSAIO_%03X" % f)

    livres = vars_livres()
    if len(com_var) > min(ORCAMENTO_VARS, len(livres) - RESERVA_VARS):
        raise SystemExit("PARE: %d mapas pedem var, o orcamento e %d e ha %d "
                         "livres" % (len(com_var), ORCAMENTO_VARS, len(livres)))
    vars_alocadas = {c: ("VAR_GALAR_%s_CENA" % c.upper(), livres[i])
                     for i, c in enumerate(sorted(com_var))}
    pool = flags_livres_de_galar(None)
    if len(acesas) > len(pool):
        raise SystemExit("PARE: %d flags de esconder pedidas e %d livres na "
                         "faixa de Galar" % (len(acesas), len(pool)))
    nomes = {(c, f): ("FLAG_GALAR_ESCONDE_%s_%03X" % (c.upper(), f), pool[i])
             for i, (c, f) in enumerate(sorted(acesas))}

    aceitas, motivos, _cv, _ac = traduz(
        lambda c: vars_alocadas[c][0] if c in vars_alocadas else None,
        lambda c, f: nomes[(c, f)][0] if (c, f) in nomes else None)
    recusa.update(motivos)
    return (aceitas, recusa, vars_alocadas, sorted(nomes.values()), censo, docs)


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
    out = ["@ Gerado por dev_scripts/cenas_galar.py (bloco c3 da fase de",
           "@ conteudo). Rodar dev_scripts/mundo_galar.py apaga este arquivo;",
           "@ rodar cenas_galar.py --aplicar o repoe. Corpo das cenas em",
           "@ data/scripts/galar_cenas.inc.", "",
           "%s_MapScripts::" % nome]
    tabelas = collections.defaultdict(list)
    diretos = []
    for a in sorted(aceitas_do_mapa, key=lambda z: (z["tipo"], z["base"])):
        if a["tipo"] in TIPOS_TABELA:
            tabelas[a["tipo"]].append(a)
        else:
            diretos.append(a)
    for a in diretos:
        out.append("\tmap_script MAP_SCRIPT_ON_TRANSITION, %s" % a["base"])
    for tipo in sorted(tabelas):
        macro = ("MAP_SCRIPT_ON_FRAME_TABLE" if tipo == 2
                 else "MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE")
        out.append("\tmap_script %s, %s_Tabela%d" % (macro, nome, tipo))
    out.append("\t.byte 0")
    for tipo in sorted(tabelas):
        out.append("")
        out.append("%s_Tabela%d:" % (nome, tipo))
        for a in tabelas[tipo]:
            out.append("\tmap_script_2 %s, %d, %s"
                       % (a["var_nome"], a["valor"], a["base"]))
        out.append("\t.2byte 0")
    return "\n".join(out) + "\n"


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
    return "\n".join(out) + "\n"


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
    return "\n".join(out) + "\n"


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
        texto = corpo_scripts_inc(nome, lista)
        caminho = "%s/data/maps/%s/scripts.inc" % (RAIZ, nome)
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
    aceitas, recusa, vars_alocadas, usadas_flag, censo, docs = plano()

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    aceitas, recusa, vars_alocadas, usadas_flag, censo, docs = plano()
    mudou, _corpo = aplica(aceitas, vars_alocadas, usadas_flag, docs, a.aplicar)
    relatorio(aceitas, recusa, vars_alocadas, usadas_flag, censo)
    if a.aplicar:
        print("\ngravado: %r" % dict(mudou))
    else:
        print("\n(nada gravado; use --aplicar). mudaria: %r" % dict(mudou))


if __name__ == "__main__":
    main()
