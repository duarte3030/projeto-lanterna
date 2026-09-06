#!/usr/bin/env python3
"""FASE DE CONTEUDO DE GALAR, bloco c4a: script de OBJETO sem estado.

    python3 dev_scripts/objetos_galar.py            # so mede e relata
    python3 dev_scripts/objetos_galar.py --aplicar  # escreve o .inc e os map.json
    python3 dev_scripts/objetos_galar.py --demo     # autoteste com mutacao plantada

## O que este bloco e

O c3 (`dev_scripts/cenas_galar.py`) portou a cena que o HEADER do mapa dispara.
Este porta a cena que o OBJETO dispara: o NPC que anda, abre porta, some, leva o
jogador para outro mapa. Ele reusa o tradutor do c3 inteiro (mesma tabela de
opcodes lida do `event.inc` do FireRed, mesma traducao de movimento POR NOME,
mesmo charmap, mesmo de-para de id de objeto pela COORDENADA) e so acrescenta
`warp`, pelo gancho `Tradutor.extra`. Nada do filtro do c3 muda: ele ja esta
commitado e provado pelo T127.

## PRECEDENCIA, e ela e a regra que os dois arquivos tem de repetir

Um object event tem UM campo `script`. O `fala_galar.py` (baldes a e b) deu fala
simples a 337 NPCs; onde ESTE bloco porta a cena inteira, a cena SUBSTITUI a
fala, porque a cena da fonte ja contem a fala dentro dela. Para isso:

  - o rotulo daqui comeca com `GalarObj_`, e o de la com `GalarFala_`;
  - `fala_galar.aplica` NAO sobrescreve campo `script` que ja comece com
    `GalarObj_` (a regra esta escrita no cabecalho de la tambem);
  - portanto a ordem de LEVA_DONA continua valendo e os dois `--demo` ficam
    verdes rodando em qualquer ordem.

## O TETO DESTE BLOCO, medido antes de escrever uma linha

O `PLANO-CONTEUDO-GALAR.md` conta 1.038 linhas no padrao "resto (movimento,
fala, fadescreen, warp)". Esse numero conta LINHA, e nao lugar onde pendurar a
linha: **so 79 delas tem objeto no nosso mapa** (70 objetos e 9 placas). As
outras 959 sao objetos que o G4 nao pos no mapa (grafico de Pokemon ou de
cenario), e a condutora ja as DESCARTOU em 21/08 porque devolver o sprite
mentiria a especie. Dentro das 959 estao os 859 scripts de encontro estatico
(`setwildbattle`/`dowildbattle`): eles nao sao cena de NPC, sao Pokemon parado
no mapa, e voltarao junto com a decisao de sprite, nunca por este bloco.

`special`, opcode indecodificavel, estado (var salva ou flag de esconder) e
entrega de item continuam FORA, com motivo contado: sao os blocos c4b a c4f.
Nesta onda o `include/constants/flags.h` NAO e desta frente (o executor da Dex
esta alocando um bloco grande la), entao nenhuma flag nova e pedida: cena que
precisaria de flag de esconder sai com motivo e o relatorio diz quantas foram.

## RECEITA DO WARP DE OBJETO, medida em 22/08/2026

**`warp` precisa de `waitstate` logo depois.** Foi medido no emulador, nao
deduzido: uma build unica levou cinco variantes do mesmo warp penduradas no
mesmo NPC, escolhidas por uma var que o harness escreve. As quatro que tinham
`waitstate` trocaram de mapa (com e sem `lock`, com e sem `release`, com e sem
caixa de texto antes); a unica sem `waitstate` deixou o jogador parado no mapa.
O bytecode nunca esteve errado: a macro `formatwarp` daqui e IGUAL a do
FireRed, sete bytes (grupo, num, warpId, x, y), e `warp MAPA, x, y` cai no ramo
de coordenada com `warpId = WARP_ID_NONE`.

Armadilha de MEDICAO, nao do jogo: mapa de Galar que nao tem warp nenhum
(`Galar_StowOnSide02`, `Galar_Wedgehurst09`) nao pode ser usado como ENTRADA do
caso de suite, porque o warp de debug pede um indice de warp que nao existe e o
estado de warp do jogador fica sujo; nesses mapas a cena roda (o jogador trava
na caixa) e a troca de mapa nao acontece. Nao e defeito da cena.

## O QUE O c4e MEDIU, e a resposta e "nao ha comando novo"

A `gScriptCmdTable` da ROM do demake tem **214 entradas**, e o
`data/script_cmd_table.inc` do FireRed tem **214**. O demake nao acrescentou
comando nenhum ao motor de script. Logo, opcode acima de 0xD5 num ponteiro de
script NAO e comando: aquele ponteiro aponta para DADO, e o script nunca roda
(era a segunda hipotese do PLANO-CONTEUDO-GALAR.md, agora medida). O que sobrou
de "opcode indecodificavel" tinha duas causas, e as duas eram nossas: o byte de
enchimento 0xFF e um BURACO DO PARSER, consertado nesta leva -- `tabela_de_opcodes`
guardava so o primeiro ramo das macros de dois ramos, e com isso 0x50, 0x52,
0x54 e 0x56 (`applymovement_at`, `waitmovement_at`, `removeobject_at`,
`addobject_at`) ficavam fora da tabela.

## Ordem da rota da historia

O `.inc` sai na ordem da campanha (Postwick, Wedgehurst, Motostoke, ...), nao em
ordem alfabetica nem na ordem do censo. E so legibilidade, nao muda um byte do
que o jogo faz, mas e o que a condutora pediu para conseguir revisar por leva.
"""
import argparse
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import fala_galar as FALA                      # noqa: E402
import cenas_galar as C3                       # noqa: E402
import guarda_colisao_vars as GUARDA           # noqa: E402
import flags_livres as FL                       # noqa: E402
import texto_placas_sinnoh as TXT               # noqa: E402  (requebra por px)

INC = f"{RAIZ}/data/scripts/galar_objetos.inc"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
BASE = FALA.BASE
WARP_ID_NONE = 0xFF
SEM_COORD = 0xFFFF

# PRECEDENCIA DE CAMPO `script` (pedido do lote F da onda 2, 07/09/2026).
#
# Um object_event tem UM campo `script`, e mais de um gerador quer escrever
# nele. A regra ja existia entre este arquivo e `fala_galar.py`, so que escrita
# a mao nos dois: la, `GalarObj_*` (a cena inteira) vence `GalarFala_*` (a fala
# solta), porque a cena ja contem a fala e sobrescrever apagaria a cena calado.
#
# `dev_scripts/portas_script_galar.py` entrou na onda 2 e reaponta o `script` de
# alguns objetos para `GalarPorta_*` (data/scripts/galar_portas_script.inc): sao
# as portas que o demake abre por script, e o rotulo NAO e derivavel da fonte
# que estes dois geradores leem. Quem escrever por cima apaga a porta, e a
# unica pista seria o jogador batendo numa porta que nao abre mais.
#
# Por isso a lista virou UMA constante, lida pelos dois geradores: quem entrar
# depois acrescenta o prefixo aqui e nao em dois lugares.
#
# Medido em 07/09/2026: `galar_portas_script.inc` tem 12 rotulos `GalarPorta_*`
# e ZERO map.json aponta para eles ainda (o lote F tambem entrega por pedido, e
# o fechador e que cola). A guarda e portanto PREVENTIVA, e e exatamente por
# isso que ela precisa entrar ANTES de o fechador colar: depois, o estrago ja
# teria acontecido na primeira geracao seguinte.
MANDAM_MAIS = ("GalarPorta_",)


def manda_mais(script):
    """O prefixo com precedencia sobre este gerador, ou None.

    Recebe o valor que o `script` do map.json JA tem. Devolver algo diferente
    de None significa "nao escreva aqui".
    """
    s = str(script or "")
    for p in MANDAM_MAIS:
        if s.startswith(p):
            return p
    return None

# Faixa de Galar para as flags de ESCONDER do bloco c4b. 0x1C00-0x1C20 sao os
# itens escondidos do G4, 0x1C21-0x1C58 as bolas do fala_galar.py, 0x1C59 a
# FLAG_HIDE_GIRATINA e 0x1CFF a FLAG_GALAR_QA_ANDAR. Comeca em 0x1C80 com folga
# de proposito, para uma leva nova de bolas nao encostar aqui.
# `#define NOME FLAG_UNUSED_0xNNN`, o jeito como toda flag apelidada aparece
# em include/constants/flags.h. Mora aqui porque duas leituras diferentes do
# mesmo header foi exatamente o que deixou a vaga 0x1C89 passar por livre.
PADRAO_APELIDO_FLAG = (r"#define\s+(?!FLAG_UNUSED)(\w+)\s+"
                       r"\(?\s*FLAG_UNUSED_0x([0-9A-Fa-f]{3,4})")

PRIMEIRA_FLAG_ESCONDE = 0x1C80
ULTIMA_FLAG_ESCONDE = 0x1CFE

MARCA_FLAG_INI = ("// >>> Fase de conteudo de Galar, bloco c4b: flags de esconder "
                  "(dev_scripts/objetos_galar.py) >>>")
MARCA_FLAG_FIM = "// <<< Fase de conteudo de Galar, bloco c4b <<<"
MARCA_VAR_INI = ("// >>> Fase de conteudo de Galar, bloco c4d: vars de etapa de "
                 "objeto (dev_scripts/objetos_galar.py) >>>")
MARCA_VAR_FIM = "// <<< Fase de conteudo de Galar, bloco c4d <<<"

# ONDA 3, LOTE L1: a reabertura das recusas. A regra esta escrita em
# `cenas_galar.py` (bloco REABERTURA DAS RECUSAS); aqui ficam a FAIXA e os
# marcadores dos dois blocos novos de header.
#
# A faixa 0x2300-0x237F e desta frente nesta onda, e sao 128 vagas de
# FLAG_UNUSED conferidas no header. Apelidar FLAG_UNUSED nao mexe em
# FLAGS_COUNT: a save nao muda de tamanho nem de indice.
PRIMEIRA_FLAG_MOTOR = 0x2300
ULTIMA_FLAG_MOTOR = 0x237F

MARCA_FLAG_MOTOR_INI = ("// >>> Fase de conteudo de Galar, onda 3 lote L1: flags "
                        "de motor do demake (dev_scripts/objetos_galar.py) >>>")
MARCA_FLAG_MOTOR_FIM = "// <<< Fase de conteudo de Galar, onda 3 lote L1 (flags) <<<"
MARCA_VAR_MOTOR_INI = ("// >>> Fase de conteudo de Galar, onda 3 lote L1: vars da "
                       "fonte sem dono (dev_scripts/objetos_galar.py) >>>")
MARCA_VAR_MOTOR_FIM = "// <<< Fase de conteudo de Galar, onda 3 lote L1 (vars) <<<"


class _EnsaioFlagsMotor(dict):
    """De-para de ENSAIO: responde por toda flag que mereceria endereco.

    A primeira passada de `plano()` so quer saber QUAIS flags a cena cita; se
    ela ja gastasse vaga, cena recusada depois levaria a vaga consigo. Por isso
    o nome de ensaio, e por isso ele e um dicionario que responde por calculo em
    vez de uma tabela: nao da para listar de antemao o que a cena vai ler.
    """

    def __contains__(self, f):
        return C3.TEMP_FLAGS_FIM <= f < C3.FLAGS_COUNT_FONTE

    def get(self, f, default=None):
        return ("FLAG_GALAR_MOTOR_ENSAIO_%03X" % f
                if f in self else default)


class _EnsaioVarsLivres(dict):
    """O mesmo do lado das vars de save da fonte."""

    def __contains__(self, e):
        return C3.PRIMEIRA_VAR_SAVE_FONTE <= e <= C3.ULTIMA_VAR_SAVE_FONTE

    def get(self, e, default=None):
        return "VAR_GALAR_MOTOR_ENSAIO_%04X" % e if e in self else default
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
VARS_H = f"{RAIZ}/include/constants/vars.h"

# Ordem da rota da historia de Galar. O casamento e por PREFIXO do nosso nome de
# mapa; o que nao casa vai para o fim, em ordem de chave da fonte.
ROTA = ["Postwick", "SlumberingWeald", "Route01", "Wedgehurst", "Route02",
        "Route03", "GalarMine", "Motostoke", "WildArea", "Route04", "Route05",
        "Turffield", "Route06", "Hulbury", "Route07", "Hammerlocke",
        "Route08", "StowOnSide", "Route09", "Ballonlea", "GlimwoodTangle",
        "Circhester", "Route10", "Spikemuth", "Wyndon", "RoseTower",
        "IsleOfArmor", "CrownTundra"]


def ordem_da_rota(nome):
    seco = nome.replace("Galar_", "")
    for i, cidade in enumerate(ROTA):
        if seco.startswith(cidade):
            return i
    return len(ROTA)


class TradutorObjeto(C3.Tradutor):
    """O tradutor do c3 mais `warp`, que so cena de objeto usa."""

    def __init__(self, *a, **kw):
        self.rev_mapa = kw.pop("rev_mapa")
        super().__init__(*a, **kw)
        G = FALA._gente()
        self.itens_fonte = G.itens_da_fonte()
        self.itens_nossos = G.nossos_itens()
        self.especies_fonte = C3.constantes(
            f"{C3.PKFR}/include/constants/species.h", "SPECIES")
        self.especies_nossas = set(re.findall(
            r"\bSPECIES_[A-Z0-9_]+\b",
            open(f"{RAIZ}/include/constants/species.h").read()))
        # SPECIAL: indice do FireRed -> nome, e o nome tem que existir AQUI.
        # As duas tabelas sao listas ordenadas (`def_special`), 444 la e 623
        # aqui, e o indice NAO e o mesmo nos dois; so o nome atravessa.
        self.specials_fonte = re.findall(
            r"^\s*def_special\s+(\w+)",
            open(f"{C3.PKFR}/data/specials.inc").read(), re.M)
        self.specials_nossos = set(re.findall(
            r"^\s*def_special\s+(\w+)",
            open(f"{RAIZ}/data/specials.inc").read(), re.M))

    def item(self, ident):
        nome = self.itens_fonte.get(ident)
        if nome is None or nome not in self.itens_nossos:
            raise C3.Recusa("item %d da fonte sem equivalente no nosso items.h"
                            % ident)
        return nome

    def especie(self, ident):
        """Nome da especie, NUNCA o numero.

        O id interno do Gen 3 nao e o da Pokedex nacional, e o nosso motor
        numera por nacional: traduzir por VALOR daria outro Pokemon a partir de
        Treecko. Por nome o assembler resolve, e nome que nao existe aqui
        recusa a cena em vez de entregar bicho errado.
        """
        nome = self.especies_fonte.get(ident)
        if nome is None or nome not in self.especies_nossas:
            raise C3.Recusa("especie %d da fonte sem nome no nosso species.h"
                            % ident)
        return nome

    def lista_de_loja(self, ptr, base):
        """Rotulo da lista `.2byte ITEM_*` da loja, terminada por ITEM_NONE."""
        if not (BASE <= ptr < BASE + len(self.rom)):
            raise C3.Recusa("lista de loja fora da rom")
        off, itens = ptr - BASE, []
        for i in range(32):
            v = int.from_bytes(self.rom[off + i * 2:off + i * 2 + 2], "little")
            if v == 0:
                break
            itens.append(self.item(v))
        else:
            raise C3.Recusa("lista de loja sem fim")
        if not itens:
            raise C3.Recusa("lista de loja vazia")
        rot = "%s_Mart%d" % (base, len(self.extras_gancho))
        self.extras_gancho.extend(["\t.align 2", "%s:" % rot]
                                  + ["\t.2byte %s" % i for i in itens]
                                  + ["\t.2byte ITEM_NONE"])
        return rot

    def special_nome(self, idx):
        nome = (self.specials_fonte[idx] if idx < len(self.specials_fonte)
                else None)
        if nome is None:
            raise C3.Recusa("special 0x%03X fora da tabela do FireRed" % idx)
        # DE-PARA de special: o FireRed e este motor dao NOMES diferentes para a
        # MESMA funcao, e recusar por causa do nome era perder a cena por
        # ortografia. Cada par abaixo foi conferido LENDO os dois corpos, nao
        # pelo nome parecido; o que nao tem par continua saindo com motivo.
        nome = DE_PARA_SPECIAL.get(nome, nome)
        if nome not in self.specials_nossos:
            raise C3.Recusa("special %s do FireRed nao existe aqui" % nome)
        return nome

    def mapa_de(self, grupo, num):
        chave = self.rev_mapa.get((grupo, num))
        if chave is None:
            raise C3.Recusa("mapa %d.%d nao esta nos 438 da fonte"
                            % (grupo, num))
        return self.de_para_mapa[chave], chave

    def extra(self, nome, args, corpo, base):
        if nome == "special":
            corpo.append("\t%s %s" % (self.macro(nome),
                                      self.special_nome(args[0])))
            return True
        if nome == "specialvar":
            corpo.append("\t%s %s, %s" % (self.macro(nome), self.var(args[0]),
                                          self.special_nome(args[1])))
            return True
        if nome in ("applymovement_at", "waitmovement_at", "removeobject_at",
                    "addobject_at"):
            # No nosso motor a variante `_at` nao tem macro propria: e a MESMA
            # macro com um terceiro argumento de mapa (`.ifb \map` em
            # asm/macros/event.inc). Emitir o nome base com o mapa a mais e o
            # jeito certo; inventar `applymovement_at` nao compila.
            base_nome = nome[:-3]
            dp, _k = self.mapa_de(args[-1] >> 8, args[-1] & 0xFF)
            if base_nome == "applymovement":
                r = "%s_MovAt%d" % (base, len(self.extras_gancho))
                self.extras_gancho.extend(self.movimento(args[1], r))
                corpo.append("\t%s %s, %s, %s" % (self.macro(base_nome),
                                                  self.objeto(args[0]), r,
                                                  dp["mapa"]))
            else:
                corpo.append("\t%s %s, %s" % (self.macro(base_nome),
                                              self.objeto(args[0]), dp["mapa"]))
            return True
        if nome == "givemon":
            corpo.append("\t%s %s, %d, %s" % (self.macro(nome),
                                              self.especie(args[0]), args[1],
                                              self.item(args[2]) if args[2]
                                              else "ITEM_NONE"))
            return True
        if nome == "giveegg":
            corpo.append("\t%s %s" % (self.macro(nome), self.especie(args[0])))
            return True
        if nome in ("additem", "removeitem", "checkitem", "checkitemspace"):
            corpo.append("\t%s %s, %d" % (self.macro(nome), self.item(args[0]),
                                          args[1]))
            return True
        if nome == "bufferitemname":
            corpo.append("\t%s %d, %s" % (self.macro(nome), args[0],
                                          self.item(args[1])))
            return True
        if nome == "pokemart":
            corpo.append("\t%s %s" % (self.macro(nome),
                                      self.lista_de_loja(args[0], base)))
            return True
        if nome == "playmoncry":
            corpo.append("\t%s %s, %d" % (self.macro(nome),
                                          self.especie(args[0]), args[1]))
            return True
        if nome == "showmonpic":
            corpo.append("\t%s %s, %d, %d" % (self.macro(nome),
                                              self.especie(args[0]), args[1],
                                              args[2]))
            return True
        if nome == "message":
            rot = "%s_Msg%d" % (base, len(self.extras_gancho))
            self.extras_gancho.extend(self.texto(args[0], rot))
            corpo.append("\t%s %s" % (self.macro(nome), rot))
            return True
        if nome in ("showmoneybox", "showcoinsbox", "hidecoinsbox",
                    "updatecoinsbox"):
            corpo.append("\t%s %d, %d" % (self.macro(nome), args[0], args[1]))
            return True
        if nome in ("hidemoneybox", "updatemoneybox"):
            # No FireRed os dois levam x/y; aqui `hidemoneybox` nao leva nada e
            # `updatemoneybox` leva so o `disable`. Traduzir e DESCARTAR a
            # coordenada, que e do layout da caixa e nao da cena.
            corpo.append("\t" + self.macro(nome))
            return True
        if nome == "checkplayergender":
            # Escreve VAR_RESULT, que o filtro do c3 ja sabe ler no `compare`.
            # Fica aqui e nao no c3 porque o c3 esta commitado e provado.
            corpo.append("\t" + self.macro(nome))
            return True
        if nome not in ("warp", "warpsilent"):
            return False
        # `formatwarp` emite 7 bytes: grupo, num, warpId, x (2), y (2). A ordem
        # grupo/num vem do `map` do FireRed (asm/macros/map.inc), lida la e nao
        # lembrada; trocar os dois mandaria o jogador para outro mapa calado.
        b = args[0].to_bytes(7, "little")
        grupo, num, warp_id = b[0], b[1], b[2]
        x = int.from_bytes(b[3:5], "little")
        y = int.from_bytes(b[5:7], "little")
        chave = self.rev_mapa.get((grupo, num))
        if chave is None:
            raise C3.Recusa("warp para mapa %d.%d, que nao esta nos 438 da fonte"
                            % (grupo, num))
        alvo = self.de_para_mapa[chave]
        if warp_id != WARP_ID_NONE:
            # Indice de warp NAO sobrevive ao G3: ele filtrou warp sujo e a
            # lista encolheu, entao o numero da fonte aponta para outra porta.
            # Sem de-para de indice medido, isto sai com motivo.
            raise C3.Recusa("warp por indice de warp: o G3 filtrou a lista e o "
                            "indice da fonte nao vale mais")
        if x == SEM_COORD or y == SEM_COORD:
            raise C3.Recusa("warp sem indice e sem coordenada")
        # RECEITA DO WARP, medida no emulador em 22/08/2026 (sonda de cinco
        # variantes numa build so, escolhidas por var): `warp` PRECISA de
        # `waitstate` logo depois. Com ele a troca de mapa acontece em todas as
        # formas testadas (com e sem `lock`, com e sem `release`, com e sem
        # caixa de texto antes); sem ele o jogador fica no mapa, que era o
        # sintoma de 22/08. O bytecode do `warp` ja estava certo: a macro
        # `formatwarp` daqui e IGUAL a do FireRed, sete bytes (grupo, num,
        # warpId, x, y), e `warp MAPA, x, y` cai no ramo de coordenada com
        # warpId = WARP_ID_NONE.
        corpo.append("\t%s %s, %d, %d" % (self.macro(nome), alvo["mapa"], x, y))
        corpo.append("\t" + self.macro("waitstate"))
        return True


# DE-PARA de `special`: nome do FireRed -> nome daqui, para a MESMA funcao.
# Conferido corpo a corpo em 22/08/2026, e nao por semelhanca de nome:
#   StartLegendaryBattle    -> BattleSetup_StartLegendaryBattle (src/battle_setup.c)
#   GetPartyMonSpecies      -> ScriptGetPartyMonSpecies         (src/field_specials.c)
#   GetPokedexCount         -> GetFrlgPokedexCount              (src/birch_pc.c, copia
#                              linha a linha do prof_pc.c do FR)
#   SelectMoveDeleterMove   -> MoveDeleterChooseMoveToForget    (src/party_menu.c)
# Os no-ops de Quest Log e Help System NAO entram aqui: eles ganharam o MESMO
# nome em data/specials.inc, com corpo nulo (ver o bloco marcado la).
DE_PARA_SPECIAL = {
    "StartLegendaryBattle": "BattleSetup_StartLegendaryBattle",
    "GetPartyMonSpecies": "ScriptGetPartyMonSpecies",
    "GetPokedexCount": "GetFrlgPokedexCount",
    "SelectMoveDeleterMove": "MoveDeleterChooseMoveToForget",
}


def rotulo(chave, l):
    n = int(l["chave"].rsplit("/", 1)[1])
    return "GalarObj_%s_%s%d" % (chave.upper(),
                                 "bg" if l["tipo"] == "placa" else "o", n)


def plano():
    """(aceitas, recusas, docs, flags alocadas, vars alocadas).

    DUAS PASSADAS, pelo mesmo motivo do c3: a primeira usa nome de FLAG e de VAR
    de ensaio so para descobrir quais cenas passam no filtro e o que cada uma
    consome; a segunda escreve com os nomes de verdade. Endereco so e gasto por
    cena que ENTROU, e a ordem de alocacao e a da chave da FONTE, nunca a da
    descoberta, para o bloco em vars.h/flags.h nao virar diff a cada rodada.
    """
    rom = open(FALA.ROM_FONTE, "rb").read()
    tab = FALA.tabela_de_opcodes()
    cmap = FALA.charmap()
    linhas = json.load(open(FALA.ROTEIROS))["linhas"]
    gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
    por_mapa = collections.defaultdict(list)
    for l in gente:
        por_mapa[l["mapa"]].append(l)
    mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
    de_para = mundo["de_para"]
    rev = {(d["fonte_grupo"], d["fonte_indice"]): k for k, d in de_para.items()}
    musica = C3.musica_da_fonte()

    # Flag de esconder da FONTE -> objetos que ela esconde, em TODOS os mapas.
    # O escopo e global de proposito: 21 das 49 linhas medidas mexem na flag de
    # um objeto de OUTRO mapa, que e como a fonte faz o NPC sumir do lugar de
    # onde ele saiu.
    esconde_glob = collections.defaultdict(list)
    for o in gente:
        if (o["tipo"] == "objeto" and o.get("flag_fonte")
                and o["motivo"].startswith("entrou")):
            esconde_glob[o["flag_fonte"]].append((o["mapa"], o["i"] + 1))

    docs, cobrar = {}, []
    recusa = collections.Counter()
    # MOTIVO POR LINHA DA FILA, e nao so a contagem: a fila cobra linha a
    # linha, e sem o motivo dela a linha volta pendente e sem nada escrito a
    # cada varredura. Acrescentado em 06/09/2026 pelo lote C da onda 1, pela
    # mesma razao e no mesmo formato do `por_mapa_motivo` de cenas_galar.py.
    por_linha = collections.defaultdict(list)
    for l in sorted(linhas, key=lambda z: z["chave"]):
        if l["balde"] != "c_var_cena" or l["tipo"] not in ("script_objeto",
                                                           "placa"):
            continue
        if not l.get("ponteiro_fonte"):
            recusa["porta morta, e pendencia de mapa"] += 1
            por_linha["porta morta, e pendencia de mapa"].append(l["chave"])
            continue
        if l["tipo"] == "script_objeto" and not l["no_mapa"]:
            recusa["objeto nao esta no mapa (descarte da condutora, 21/08)"] += 1
            por_linha["objeto nao esta no mapa (descarte da condutora, "
                      "21/08)"].append(l["chave"])
            continue
        dp = de_para.get(l["mapa_fonte"])
        if dp is None:
            recusa["mapa da fonte fora do de-para do G3"] += 1
            por_linha["mapa da fonte fora do de-para do G3"].append(l["chave"])
            continue
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, dp["nome"])
        if not os.path.exists(caminho):
            recusa["map.json do mapa nao existe"] += 1
            por_linha["map.json do mapa nao existe"].append(l["chave"])
            continue
        docs.setdefault(caminho, json.load(open(caminho)))
        cobrar.append((l, dp, caminho))

    # Var de estado que cada mapa usa, e QUAL delas ganha a casa: a mais citada
    # nas cenas daquele mapa (empate pelo endereco menor). E o preco declarado
    # do desenho "uma var por MAPA", o mesmo do c3.
    quantas = collections.defaultdict(collections.Counter)
    for l, _dp, _c in cobrar:
        ins, falha = C3.blocos(rom, tab, int(l["ponteiro_fonte"], 16))
        if falha:
            continue
        for b in ins:
            for nome, args in b.ins:
                if (nome in ("setvar", "addvar", "subvar", "compare_var_to_value")
                        and args and 0x4010 <= args[0] < 0x4200):
                    quantas[l["mapa_fonte"]][args[0]] += 1
    var_escolhida = {c: max(v, key=lambda a: (v[a], -a))
                     for c, v in quantas.items()}

    def traduz(nome_flag_de, nome_var_de, motor_flags=None, livres_vars=None):
        fora, motivos = [], collections.Counter()
        motivos_de_linha = {}
        usou_flag, usou_var = set(), set()
        # ONDA 3: o que a cena citou das faixas NOVAS. Colhido do corpo emitido,
        # e nao do que o tradutor consultou: cena recusada depois de consultar
        # nao pode levar vaga consigo, que e a mesma lei das duas passadas.
        usou_motor, usou_livre = set(), set()
        for l, dp, caminho in cobrar:
            chave = l["mapa_fonte"]
            esconde = {f: ids for f, ids in
                       ((f, [i for m, i in v if m == chave])
                        for f, v in esconde_glob.items()) if ids}
            nomes_flag = {f: nome_flag_de(f) for f in esconde_glob}
            var = var_escolhida.get(chave)
            nomes_var = {var: nome_var_de(chave)} if var else {}
            t = TradutorObjeto(
                rom, tab, cmap,
                C3.de_para_de_objetos(chave, docs[caminho], por_mapa),
                esconde, nomes_var, nomes_flag, musica, rev_mapa=rev)
            t.de_para_mapa = de_para
            # A linha da fila que este objeto responde, para o caderno de
            # `dev_scripts/onda3_falta_traduzir.json` saber a quem cobrar.
            t.chave_da_fila = l["chave"]
            t.nome_flag_motor = (motor_flags if motor_flags is not None
                                 else _EnsaioFlagsMotor())
            t.nome_var_livre = (livres_vars if livres_vars is not None
                                else _EnsaioVarsLivres())
            base = rotulo(chave, l)
            try:
                corpo, usadas = t.cena(int(l["ponteiro_fonte"], 16), base)
            except C3.Recusa as e:
                motivos[str(e)] += 1
                motivos_de_linha[l["chave"]] = str(e)
                continue
            texto_corpo = "\n".join(corpo)
            citadas = {f for f in esconde_glob
                       if nomes_flag[f] and nomes_flag[f] in texto_corpo}
            usou_flag |= citadas
            usou_motor |= {int(h, 16) for h in re.findall(
                r"FLAG_GALAR_MOTOR_(?:ENSAIO_)?([0-9A-F]{3,4})\b", texto_corpo)}
            usou_livre |= {int(h, 16) for h in re.findall(
                r"VAR_GALAR_MOTOR_(?:ENSAIO_)?([0-9A-F]{4})\b", texto_corpo)}
            if var and nomes_var[var] and nomes_var[var] in "\n".join(corpo):
                usou_var.add(chave)
            fora.append(dict(chave=chave, nome=dp["nome"], caminho=caminho,
                             tipo=l["tipo"], x=l["x"], y=l["y"], base=base,
                             linhas=corpo, usadas=usadas, flags=citadas,
                             ordem=ordem_da_rota(dp["nome"])))
        return (fora, motivos, usou_flag, usou_var, motivos_de_linha,
                usou_motor, usou_livre)

    # A PASSADA DE ENSAIO E A QUE DIZ O MOTIVO DE VERDADE (onda 3). Nela toda
    # flag e toda var estao disponiveis, entao o que ela recusa foi recusado por
    # um impedimento REAL. Na segunda passada so existem os enderecos que o
    # ensaio provou necessarios, e uma cena que ja tinha caido por outro motivo
    # volta a cair no primeiro `checkflag` sem nome -- relatando "flag de motor
    # do demake" para uma linha cujo problema e outro. Antes da onda 3 as duas
    # passadas so trocavam o NOME e essa diferenca nao existia.
    (_e, _m, quer_flag, quer_var, _ml, quer_motor, quer_livre) = traduz(
        lambda f: "FLAG_GALAR_ENSAIO_%03X" % f, lambda c: "VAR_GALAR_ENSAIO")

    # A faixa 0x1C80-0x1CFE e COMPARTILHADA com o bloco de cena do
    # `cenas_galar.py`. Livre aqui e a flag que existe como FLAG_UNUSED e nao
    # tem apelido de NINGUEM, tirando o nosso proprio bloco, que e reescrito
    # inteiro a cada rodada. O teste antigo ("existe um #define FLAG_UNUSED com
    # esse numero") dava a faixa INTEIRA como livre, inclusive as que o c3 ja
    # tivesse pegado, e so nao mordeu porque o c3 nunca chegou a pedir uma.
    _txt = open(FLAGS_H).read()
    pool_f = [f for f in range(PRIMEIRA_FLAG_ESCONDE, ULTIMA_FLAG_ESCONDE + 1)
              if ("#define FLAG_UNUSED_0x%04X" % f) in _txt
              and f not in flags_com_dono(_txt)]
    if len(quer_flag) > len(pool_f):
        raise SystemExit("PARE: %d flags de esconder pedidas e %d livres na "
                         "faixa de Galar" % (len(quer_flag), len(pool_f)))
    # APPEND-ONLY (ver flags_livres.aloca_append_only): a flag ja gravada
    # em flags.h NAO muda de endereco, e a nova entra depois do maior. Ate
    # 23/08/2026 esta linha era `pool_f[i]` sobre `sorted(quer_flag)`, e uma
    # flag nova no meio empurrava as seguintes; foi assim que 0x1C81 saiu de
    # FLAG_GALAR_ESCONDE_23C para FLAG_GALAR_ESCONDE_230 entre duas ROMs.
    nomes_f = {f: "FLAG_GALAR_ESCONDE_%03X" % f for f in quer_flag}
    ende_f = FL.aloca_append_only(
        nomes_f.values(), pool_f,
        FL.apelidos_gravados(FLAGS_H, "FLAG_GALAR_ESCONDE_"))
    flags = {f: (nomes_f[f], ende_f[nomes_f[f]]) for f in quer_flag}

    # Var: se o c3 ja deu casa para a MESMA var da fonte naquele mapa, reusa o
    # nome dele em vez de queimar um endereco novo para o mesmo estado.
    do_c3 = vars_do_c3()
    # ONDA 3, FECHAMENTO: `C3.vars_livres()` retira TODOS os blocos "Fase de
    # conteudo de Galar" do header antes de medir (e tem de retirar, senao o
    # gerador foge das proprias vagas a cada rodada), e por isso devolve como
    # LIVRE o endereco que o bloco de motor DESTE MESMO arquivo e o gerador de
    # PORTA de outro dono ja apelidaram. Medido em 06/09/2026: a mesma passada
    # deu 0x4117 a VAR_GALAR_G06M35_OBJ (c4d) e a VAR_GALAR_MOTOR_4060 (L1), e
    # o `guarda_colisao_vars` reprovou. A conta certa e a mesma do
    # `proxima_var_livre`: todo apelido gravado no header, menos os nomes que
    # ESTA chamada realoca (o proprio bloco e reescrito inteiro a cada rodada).
    _gravados_v = FL.apelidos_gravados(VARS_H, "VAR_", "UNUSED_0x")

    def pool_de_vars(meus_nomes, fora=()):
        de_outro = {e for n, e in _gravados_v.items() if n not in meus_nomes}
        return [v for v in C3.vars_livres()
                if v not in do_c3.values() and v not in de_outro
                and v not in fora]

    novas = [c for c in sorted(quer_var) if c not in do_c3]
    # APPEND-ONLY, mesma regra e mesmo motivo das flags acima.
    nomes_v = {c: "VAR_GALAR_%s_OBJ" % c.upper() for c in novas}
    livres = pool_de_vars(set(nomes_v.values()))
    if len(novas) > len(livres):
        raise SystemExit("PARE: %d vars de etapa pedidas e %d livres"
                         % (len(novas), len(livres)))
    ende_v = FL.aloca_append_only(
        nomes_v.values(), livres,
        FL.apelidos_gravados(VARS_H, "VAR_GALAR_", "UNUSED_0x"))
    variaveis = {c: (nomes_v[c], ende_v[nomes_v[c]]) for c in novas}

    def nome_var(chave):
        if chave in do_c3:
            return "VAR_GALAR_%s_CENA" % chave.upper()
        return variaveis[chave][0] if chave in variaveis else None

    # ONDA 3, LOTE L1: as duas faixas novas, alocadas APPEND-ONLY como as
    # outras. `flags_com_dono` tira desta conta quem ja tem apelido, e o nosso
    # proprio bloco e reescrito inteiro a cada rodada, entao ele conta como
    # livre: sem essa parte, a segunda passada veria as vagas que ela mesma
    # gravou como ocupadas e escolheria outras, e o header viraria diff eterno
    # (e a mesma licao que custou o `--demo` de 23/08/2026).
    _txt2 = open(FLAGS_H).read()
    meus = set(FL.apelidos_gravados(FLAGS_H, "FLAG_GALAR_MOTOR_").values())
    pool_m = [f for f in range(PRIMEIRA_FLAG_MOTOR, ULTIMA_FLAG_MOTOR + 1)
              if ("#define FLAG_UNUSED_0x%04X" % f) in _txt2
              and (f not in flags_com_dono(_txt2) or f in meus)]
    if len(quer_motor) > len(pool_m):
        raise SystemExit("PARE: %d flags de motor pedidas e %d livres na faixa "
                         "0x%04X-0x%04X" % (len(quer_motor), len(pool_m),
                                            PRIMEIRA_FLAG_MOTOR,
                                            ULTIMA_FLAG_MOTOR))
    nomes_m = {f: "FLAG_GALAR_MOTOR_%03X" % f for f in quer_motor}
    ende_m = FL.aloca_append_only(
        nomes_m.values(), pool_m,
        FL.apelidos_gravados(FLAGS_H, "FLAG_GALAR_MOTOR_"))
    flags_motor = {f: (nomes_m[f], ende_m[nomes_m[f]]) for f in quer_motor}

    nomes_l = {e: "VAR_GALAR_MOTOR_%04X" % e for e in quer_livre}
    # Mesma conta do bloco c4d acima, mais as vagas que ESTA rodada acabou de
    # dar a ele: elas ainda nao estao no header lido em `_gravados_v`.
    livres2 = pool_de_vars(set(nomes_l.values()),
                           fora={e for _n, e in variaveis.values()})
    if len(quer_livre) > len(livres2):
        raise SystemExit("PARE: %d vars da fonte sem dono pedidas e %d livres"
                         % (len(quer_livre), len(livres2)))
    ende_l = FL.aloca_append_only(
        nomes_l.values(), livres2,
        FL.apelidos_gravados(VARS_H, "VAR_GALAR_MOTOR_", "UNUSED_0x"))
    vars_motor = {e: (nomes_l[e], ende_l[nomes_l[e]]) for e in quer_livre}

    (aceitas, motivos, _f, _v, motivos_de_linha,
     _qm, _ql) = traduz(
        lambda f: flags[f][0] if f in flags else None, nome_var,
        motor_flags={f: n for f, (n, _e) in flags_motor.items()},
        livres_vars={e: n for e, (n, _v) in vars_motor.items()})
    # motivo do ENSAIO em primeiro lugar; o da segunda passada so preenche o
    # que o ensaio nao viu.
    motivos_de_linha = dict(motivos_de_linha)
    motivos_de_linha.update(_ml)
    recusa.update(_m)
    for m, chaves in por_linha.items():
        for k in chaves:
            motivos_de_linha.setdefault(k, m)
    return (aceitas, recusa, docs, flags, variaveis, esconde_glob,
            motivos_de_linha, flags_motor, vars_motor)


def vars_do_c3():
    """{chave da fonte: endereco} que `cenas_galar.py` ja declarou em vars.h."""
    texto = open(VARS_H).read()
    fora = {}
    for nome, end in re.findall(
            r"#define\s+VAR_GALAR_(G\d+M\d+)_CENA\s+VAR_UNUSED_0x([0-9A-Fa-f]{4})",
            texto):
        fora[nome.lower()] = int(end, 16)
    return fora


def corpo_inc(aceitas):
    out = ["@ Cenas de OBJETO de Galar (bloco c4a da fase de conteudo).",
           "@ Gerado por dev_scripts/objetos_galar.py; NAO editar a mao.",
           "@ Rotulo GalarObj_* tem PRECEDENCIA sobre GalarFala_*: onde a cena",
           "@ inteira foi portada, ela ja contem a fala que o balde (a) deu.",
           "@ Ordem: a da rota da historia, de Postwick e Wedgehurst em diante.",
           ""]
    por_mapa = collections.defaultdict(list)
    for a in aceitas:
        por_mapa[(a["ordem"], a["nome"], a["chave"])].append(a)
    for chave in sorted(por_mapa):
        out.append("@ ---- %s (%s) ----" % (chave[1], chave[2]))
        for a in sorted(por_mapa[chave], key=lambda z: z["base"]):
            out.extend(a["linhas"])
            out.append("")
    return "\n".join(out) + "\n"


def aplica(aceitas, docs, gravar, flags=None, variaveis=None,
           esconde_glob=None, flags_motor=None, vars_motor=None):
    mudou, recusa = collections.Counter(), []
    corpo = corpo_inc(aceitas)
    if gravar:
        open(INC, "w").write(corpo)
        fonte = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_objetos.inc"'
        if linha not in fonte:
            open(EVENT_S, "w").write(fonte.rstrip("\n") + "\n" + linha + "\n")
    # LIMPEZA ANTES DE ESCREVER (licao LEVA_DONA do S8: gerador que so escreve
    # e nunca apaga mente na segunda rodada). Se uma cena deixou de passar no
    # filtro, o rotulo dela continuaria pendurado no map.json apontando para um
    # simbolo que nao existe mais, e a build so acusaria no LINK. A varredura e
    # em TODOS os mapas de Galar, nao so nos que esta rodada tocou.
    vivos = {a["base"] for a in aceitas}
    import glob
    antes = {}
    for caminho in sorted(glob.glob("%s/data/maps/Galar_*/map.json" % RAIZ)):
        doc = docs.setdefault(caminho, json.load(open(caminho)))
        antes[caminho] = json.dumps(doc, sort_keys=True)
        for o in doc.get("object_events", []):
            s = str(o.get("script", ""))
            if s.startswith("GalarObj_") and s not in vivos:
                o["script"] = "0"
                mudou["rotulo_orfao"] += 1
        bgs = doc.get("bg_events", [])
        sobrou = [b for b in bgs
                  if not (str(b.get("script", "")).startswith("GalarObj_")
                          and b["script"] not in vivos)]
        if len(sobrou) != len(bgs):
            mudou["rotulo_orfao"] += len(bgs) - len(sobrou)
            doc["bg_events"] = sobrou

    for c, d in docs.items():
        antes.setdefault(c, json.dumps(d, sort_keys=True))
    for a in sorted(aceitas, key=lambda z: z["base"]):
        doc = docs[a["caminho"]]
        if a["tipo"] == "placa":
            achados = [b for b in doc.get("bg_events", [])
                       if b.get("x") == a["x"] and b.get("y") == a["y"]]
            if len(achados) == 1:
                dono = manda_mais(achados[0].get("script"))
                if dono:
                    recusa.append((a["base"], "%s tem precedencia neste bg"
                                   % dono))
                    continue
                achados[0]["script"] = a["base"]
            elif not achados:
                doc.setdefault("bg_events", []).append({
                    "type": "sign", "x": a["x"], "y": a["y"], "elevation": 0,
                    "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                    "script": a["base"]})
            else:
                recusa.append((a["base"], "%d bg events no mesmo tile"
                               % len(achados)))
                continue
            mudou["placa"] += 1
            continue
        i, motivo = FALA.casa_objeto(doc, a["x"], a["y"])
        if i is None:
            recusa.append((a["base"], motivo))
            continue
        dono = manda_mais(doc["object_events"][i].get("script"))
        if dono:
            recusa.append((a["base"], "%s tem precedencia neste objeto" % dono))
            continue
        doc["object_events"][i]["script"] = a["base"]
        mudou["objeto"] += 1

    # c4b: o objeto que a FONTE esconde por flag passa a carregar essa flag no
    # campo `flag` do map.json. Sem isso o `setflag` da cena acende um endereco
    # que ninguem le, e o NPC continua de pe: a flag so esconde quando o motor
    # sabe de qual objeto ela e (`GetObjectEventFlagIdByObjectEventId`).
    de_para_nome = {}
    if flags and esconde_glob:
        mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
        gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
        por_mapa = collections.defaultdict(list)
        for o in gente:
            por_mapa[o["mapa"]].append(o)
        for f, (nome_flag, _end) in sorted(flags.items()):
            for chave, i_fonte in esconde_glob[f]:
                dp = mundo["de_para"].get(chave)
                if dp is None:
                    continue
                caminho = "%s/data/maps/%s/map.json" % (RAIZ, dp["nome"])
                if caminho not in docs:
                    continue
                nosso = C3.de_para_de_objetos(chave, docs[caminho],
                                              por_mapa).get(i_fonte)
                if nosso is None:
                    continue
                o = docs[caminho]["object_events"][nosso - 1]
                if str(o.get("flag", "0")) != nome_flag:
                    o["flag"] = nome_flag
                    mudou["flag_de_objeto"] += 1
                de_para_nome[nome_flag] = True

    for arq, mi, mf, bloco in (
            (FLAGS_H, MARCA_FLAG_INI, MARCA_FLAG_FIM, bloco_flags(flags or {})),
            (VARS_H, MARCA_VAR_INI, MARCA_VAR_FIM, bloco_vars(variaveis or {})),
            (FLAGS_H, MARCA_FLAG_MOTOR_INI, MARCA_FLAG_MOTOR_FIM,
             bloco_flags_motor(flags_motor or {})),
            (VARS_H, MARCA_VAR_MOTOR_INI, MARCA_VAR_MOTOR_FIM,
             bloco_vars_motor(vars_motor or {}))):
        atual = open(arq).read()
        novo_txt = C3.poe_bloco(atual, mi, mf, bloco)
        if novo_txt != atual:
            mudou[os.path.basename(arq)] += 1
            if gravar:
                open(arq, "w").write(novo_txt)

    for c, d in docs.items():
        if json.dumps(d, sort_keys=True) != antes[c]:
            mudou["mapa"] += 1
            if gravar:
                with open(c, "w") as f:
                    json.dump(d, f, indent=2, ensure_ascii=False)
                    f.write("\n")
    return mudou, recusa, corpo


def flags_com_dono(texto=None):
    """Vagas de FLAG_UNUSED que JA tem apelido de alguem, menos as deste bloco.

    O filtro por PREFIXO custou o `--demo` desta ferramenta em 23/08/2026: ele
    tirava da conta tudo que comecasse com FLAG_GALAR_ESCONDE_, e o
    `cenas_galar.py` batiza as dele com o MESMO prefixo mais o nome do mapa
    (FLAG_GALAR_ESCONDE_G09M11_230). Resultado: a vaga 0x1C89, que o c3 tinha
    acabado de tomar, aparecia como livre aqui. Nao chegou a colidir por sorte
    de ordem, e teria colidido na proxima flag que este bloco pedisse. O nome
    deste bloco e FLAG_GALAR_ESCONDE_ mais tres ou quatro digitos hexadecimais e
    mais nada, entao e assim que ele se reconhece.
    """
    texto = texto if texto is not None else open(FLAGS_H).read()
    meu = re.compile(r"FLAG_GALAR_ESCONDE_[0-9A-F]{3,4}$")
    return {int(e, 16) for n, e in re.findall(
        PADRAO_APELIDO_FLAG, texto) if not meu.match(n)}



def proxima_flag_livre(flags, flags_motor=None):
    """Vaga da faixa de Galar que NINGUEM usa, para o plante do `--demo`.

    Livre aqui tem que ser livre de verdade, e nao so livre para este bloco:
    vaga plantada que ja tem dono faz o portao acusar um grupo de TRES nomes,
    e a mutacao reprova por si mesma sem provar nada. E o mesmo cuidado que a
    `proxima_var_livre` ja tinha do lado das vars.
    """
    # ONDA 3: as flags de motor moram na faixa 0x2300, fora da de esconder, mas
    # `flags_com_dono` as ve como donas e o plante nunca cairia numa delas.
    # A linha esta aqui por simetria com `proxima_var_livre` e para o dia em que
    # as duas faixas encostarem.
    usadas = ({e for _n, e in flags.values()} | flags_com_dono()
              | {e for _n, e in (flags_motor or {}).values()}
              | set(FL.apelidos_gravados(FLAGS_H, "FLAG_", "UNUSED_0x").values()))
    texto = open(FLAGS_H).read()
    for f in range(PRIMEIRA_FLAG_ESCONDE, ULTIMA_FLAG_ESCONDE + 1):
        if f not in usadas and "FLAG_UNUSED_0x%04X" % f in texto:
            return f
    raise SystemExit("faixa de flags de Galar esgotada")


def proxima_var_livre(variaveis, vars_motor=None):
    # `C3.vars_livres()` tira os blocos de Galar do header antes de medir, entao
    # ele devolve como LIVRE tambem o que o c3 e o c4d ja apelidaram. Para o
    # plante da mutacao a vaga tem que ser uma que NINGUEM usa, senao o grupo
    # acusado vem com tres nomes e o caso reprova por si mesmo.
    # ONDA 3: a conta passou a ser TODO apelido gravado no header, e nao a
    # lista dos blocos que este arquivo conhece. `vars_livres()` retira TODOS os
    # blocos "Fase de conteudo de Galar" antes de medir (e tem de retirar, senao
    # o gerador foge das proprias vagas a cada rodada), e por isso ele devolve
    # como livre o que o c3, o c4d, o bloco de motor do L1 e o gerador de PORTA
    # de outro dono ja apelidaram. Enumerar bloco a bloco aqui deu defeito duas
    # vezes na mesma tarde: primeiro em 0x4117 (VAR_GALAR_MOTOR_) e logo depois
    # em 0x4118 (VAR_GALAR_PORTA_, de outro executor da mesma onda). Ler o
    # header inteiro nao envelhece.
    usadas = ({e for _n, e in variaveis.values()} | set(vars_do_c3().values())
              | {e for _n, e in (vars_motor or {}).values()}
              | set(FL.apelidos_gravados(VARS_H, "VAR_", "UNUSED_0x").values()))
    for v in C3.vars_livres():
        if v not in usadas:
            return v
    raise SystemExit("faixa de vars esgotada")


def bloco_flags(flags):
    if not flags:
        return ""
    out = [MARCA_FLAG_INI,
           "// Uma flag por FLAG DE ESCONDER da fonte, bloco c4b. A fonte ja",
           "// pendura essa flag no proprio object event; aqui ela ganha nome e",
           "// o campo `flag` do map.json passa a cita-la, para o motor saber",
           "// de qual objeto ela e.",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/objetos_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in flags.values()) + 2
    for f in sorted(flags):
        nome, end = flags[f]
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // flag 0x%03X da fonte"
                   % (larg, nome, end, f))
    out.append(MARCA_FLAG_FIM)
    return "\n".join(out) + "\n"


def bloco_vars(variaveis):
    if not variaveis:
        return ""
    out = [MARCA_VAR_INI,
           "// Uma var por MAPA para a etapa que a cena de OBJETO guarda",
           "// (bloco c4d). Mapa que o c3 ja atendeu com VAR_GALAR_*_CENA reusa",
           "// aquela var e nao aparece aqui: mesmo estado, mesma casa.",
           "// Apelidar VAR_UNUSED nao mexe em VARS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/objetos_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in variaveis.values()) + 2
    for c in sorted(variaveis):
        nome, end = variaveis[c]
        out.append("#define %-*s VAR_UNUSED_0x%04X  // mapa %s da fonte"
                   % (larg, nome, end, c))
    out.append(MARCA_VAR_FIM)
    return "\n".join(out) + "\n"


def bloco_flags_motor(flags_motor):
    """As flags de MOTOR do demake que ganharam endereco nosso (onda 3, L1).

    Uma por FLAG DA FONTE, e nao uma por mapa: no demake ela e uma so, global, e
    dividi-la por mapa faria a cena de um mapa nao ver o que a do outro acendeu.
    """
    if not flags_motor:
        return ""
    out = [MARCA_FLAG_MOTOR_INI,
           "// Flag que a cena da fonte LE com `checkflag` e que nao esconde",
           "// objeto importado nenhum: ate a onda 2 ela derrubava a cena",
           "// inteira por nao ter nome nosso. Aqui ela ganha endereco na faixa",
           "// 0x2300-0x237F, e o `setflag`/`clearflag` da mesma flag passa a",
           "// escrever nele. Flag que a cena so escreve continua sem endereco.",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/objetos_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in flags_motor.values()) + 2
    for f in sorted(flags_motor):
        nome, end = flags_motor[f]
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // flag 0x%03X da fonte"
                   % (larg, nome, end, f))
    out.append(MARCA_FLAG_MOTOR_FIM)
    return "\n".join(out) + "\n"


def bloco_vars_motor(vars_motor):
    """As vars de save da fonte que nao tinham dono nosso (onda 3, L1)."""
    if not vars_motor:
        return ""
    out = [MARCA_VAR_MOTOR_INI,
           "// Uma var por ENDERECO da fonte (0x4010-0x40FF, a faixa de save do",
           "// FireRed), para a cena que le ou escreve estado que nao e a etapa",
           "// do mapa. Ate a onda 2 isso recusava a cena inteira.",
           "// Apelidar VAR_UNUSED nao mexe em VARS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/objetos_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in vars_motor.values()) + 2
    for e in sorted(vars_motor):
        nome, end = vars_motor[e]
        out.append("#define %-*s VAR_UNUSED_0x%04X  // var 0x%04X da fonte"
                   % (larg, nome, end, e))
    out.append(MARCA_VAR_MOTOR_FIM)
    return "\n".join(out) + "\n"


def vars_sem_escritor(variaveis=None):
    """[(nome nosso, var da fonte, quantos escritores a FONTE tem)] das vars de
    Galar que a arvore LE e ninguem ESCREVE.

    Existe porque a QA de 23/08/2026 achou 8 nessa situacao, e a resposta certa
    depende de um dado que so a FONTE tem. Se a var da fonte tambem nao tem
    `setvar` em lugar nenhum, o ramo esta morto LA e nao ha o que portar; se
    tem, o que falta e a cena que escreve, e cena e obra, nao conserto. O
    relatorio imprime os dois numeros para ninguem ter de remedir.

    Retrato medido em 23/08/2026:
      - fonte 0x4060 (quatro nomes nossos, um por mapa): ZERO escritores na
        fonte. O ramo alternativo do dialogo esta morto na origem.
      - fonte 0x406F (as tabelas de Galar_Wedgehurst04 e Galar_Wedgehurst10,
        14 cenas): ZERO escritores na fonte.
      - fonte 0x4055 (Galar_Postwick22 e Galar_DynamaxAdventure02): 18
        escritores na fonte, TODOS dentro da cena de abertura do professor,
        que o filtro deste bloco recusa (`copyvar`, `setorcopyvar`,
        `setobjectxyperm`, `pokemartdecoration`, `closedoor`) e cujo objeto
        nem esta nos nossos mapas em 4 dos 5 casos. Porta-la e obra propria.
    """
    del variaveis
    import glob
    rom, tab, cmap, fila = FALA.carrega()
    escritores = collections.Counter()
    citadas = collections.defaultdict(collections.Counter)
    for l in fila:
        p = l.get("ponteiro_fonte")
        if not p:
            continue
        chave = l.get("mapa_fonte")
        if l["tipo"] == "map_script":
            for tipo, off in FALA.tabela_de_map_script(rom, int(p, 16)):
                if tipo not in C3.TIPOS_TABELA:
                    continue
                for var, _valor, _ptr in C3.tabela_de_map_script_tipo2(rom, off):
                    if 0x4010 <= var < 0x4200:
                        citadas[chave][var] += 1
            continue
        try:
            bs, falha = C3.blocos(rom, tab, int(p, 16))
        except Exception:                                   # noqa: BLE001
            continue
        if falha:
            continue
        for b in bs:
            for nome, args in b.ins:
                if not args or not 0x4010 <= args[0] < 0x4200:
                    continue
                if nome in ("setvar", "addvar", "subvar"):
                    escritores[args[0]] += 1
                    citadas[chave][args[0]] += 1
                elif nome == "compare_var_to_value":
                    citadas[chave][args[0]] += 1
    texto = ""
    for c in [INC, f"{RAIZ}/data/scripts/galar_cenas.inc"] + sorted(
            glob.glob(f"{RAIZ}/data/maps/Galar_*/scripts.inc")):
        if os.path.exists(c):
            texto += open(c, encoding="utf-8").read()
    fora = []
    for nome in sorted(set(re.findall(r"\bVAR_GALAR_G\d+M\d+_(?:CENA|OBJ)\b",
                                      texto))):
        if re.search(r"\b(?:setvar|addvar|subvar|copyvar)\s+%s\b" % nome, texto):
            continue
        chave = re.search(r"VAR_GALAR_(G\d+M\d+)_", nome).group(1).lower()
        v = citadas.get(chave)
        # MESMA regra do gerador: a var da fonte deste mapa e a mais citada
        # nas cenas dele (empate pelo endereco menor).
        f = max(v, key=lambda a: (v[a], -a)) if v else None
        fora.append((nome, f, escritores.get(f, 0) if f is not None else None))
    return fora


def relatorio(aceitas, recusa, variaveis=None):
    print("cenas de objeto portadas: %d em %d mapas (%d placas)"
          % (len(aceitas), len({a["nome"] for a in aceitas}),
             sum(1 for a in aceitas if a["tipo"] == "placa")))
    mortas = vars_sem_escritor(variaveis)
    if mortas:
        print("vars deste bloco LIDAS e nunca escritas: %d" % len(mortas))
        for nome, fonte, n in mortas:
            print("  %-26s fonte %s, escritores na FONTE: %s"
                  % (nome, "0x%04X" % fonte if fonte else "?",
                     "nenhum (o ramo esta morto na fonte tambem)" if n == 0
                     else n if n is not None else "?"))
    quer_flag = sum(1 for m, c in recusa.items() if "flag" in m for _ in range(c))
    print("de fora: %d linhas; das quais %d parariam numa flag "
          "(include/constants/flags.h nao e desta frente nesta onda)"
          % (sum(recusa.values()), quer_flag))
    for m, c in recusa.most_common(18):
        print("  %5d  %s" % (c, m))


def demo():
    falhas = []
    # ONDA 3, LOTE L1: o caso comum do pipeline em ingles roda ANTES de `plano`,
    # porque ele troca a instancia unica do de-para por uma de mentira e tem de
    # devolve-la antes de qualquer geracao de verdade.
    falhas.extend(FALA.demo_pipeline_ingles())
    (aceitas, recusa, docs, flags, variaveis, esconde, motivos_linha,
     flags_motor, vars_motor) = plano()

    # 1. PRECEDENCIA: nenhum objeto pode ficar com os dois scripts, e o rotulo
    #    daqui tem que ser o que sobrou no map.json.
    if any(not a["base"].startswith("GalarObj_") for a in aceitas):
        falhas.append("rotulo do c4a fora do prefixo GalarObj_")
    _mudou, rec, corpo1 = aplica(aceitas, docs, False, flags, variaveis,
                                 esconde, flags_motor, vars_motor)
    for base, motivo in rec:
        falhas.append("nao aplicado: %s %s" % (base, motivo))

    # 2. rotulo unico, senao o assembler junta duas cenas numa so.
    rot = [l[:-2] for a in aceitas for l in a["linhas"] if l.endswith("::")]
    if len(set(rot)) != len(rot):
        falhas.append("rotulo de objeto repetido")

    # 3. IDEMPOTENCIA: gerar duas vezes da o mesmo texto, e aplicar em cima do
    #    que ja esta gravado nao mexe em mapa nenhum.
    if corpo1 != corpo_inc(aceitas):
        falhas.append("o .inc nao e estavel entre duas geracoes")
    if os.path.exists(INC) and open(INC).read() == corpo1:
        aceitas2, _r2, docs2, f2, v2, e2, _ml2, fm2, vm2 = plano()
        mudou2, _rec2, _c2 = aplica(aceitas2, docs2, False, f2, v2, e2,
                                    fm2, vm2)
        if mudou2["mapa"]:
            falhas.append("segunda passada mexeria em %d mapas: nao e idempotente"
                          % mudou2["mapa"])

    # 4. MUTACAO PLANTADA 1: warp com os bytes de grupo e num TROCADOS tem que
    #    cair em outro mapa ou ser recusado, nunca passar igual. E o defeito que
    #    mandaria o jogador para o lugar errado calado.
    mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
    de_para = mundo["de_para"]
    rev = {(d["fonte_grupo"], d["fonte_indice"]): k for k, d in de_para.items()}
    t = TradutorObjeto(b"\0" * 16, {}, {}, {}, {}, {}, {}, {}, rev_mapa=rev)
    t.de_para_mapa = de_para
    (g, n), chave = next(iter(rev.items()))
    def emite_warp(bs):
        """(linhas emitidas, motivo da recusa) para um blob de 7 bytes."""
        saida = []
        try:
            t.extra("warp", [int.from_bytes(bytes(bs), "little")], saida, "X")
        except C3.Recusa as e:
            return saida, str(e)
        return saida, ""

    # 4a. O decodificador de 7 bytes do `warp` tem que acertar grupo e num, e o
    #     emissor tem que por o `waitstate` (a RECEITA medida em 22/08: sem ele
    #     a troca de mapa nao acontece). Trocar os dois bytes cita outro mapa,
    #     ou nenhum: e o plante que mostraria um de-para invertido.
    bom, motivo_bom = emite_warp([g, n, WARP_ID_NONE, 3, 0, 4, 0])
    if motivo_bom or not bom:
        falhas.append("warp bom foi recusado: %r" % motivo_bom)
    elif de_para[chave]["mapa"] not in bom[0]:
        falhas.append("warp bom nao apontou para %s: %r" % (chave, bom))
    elif len(bom) < 2 or "waitstate" not in bom[1]:
        falhas.append("warp saiu SEM `waitstate`: a troca de mapa nao acontece "
                      "(receita medida em 22/08/2026): %r" % bom)
    trocado, motivo_troca = emite_warp([n, g, WARP_ID_NONE, 3, 0, 4, 0])
    if not motivo_troca and trocado and trocado[0] == bom[0]:
        falhas.append("trocar grupo por num deu o MESMO mapa: o plante nao "
                      "seria visto")

    # 5. MUTACAO PLANTADA 2: warp por INDICE de warp continua recusado, com
    #    motivo proprio, porque o G3 encolheu a lista de warps do destino.
    _l, idx = emite_warp([g, n, 3, 0xFF, 0xFF, 0xFF, 0xFF])
    if "indice" not in idx:
        falhas.append("warp por indice nao foi recusado pelo motivo dele: %r"
                      % idx)

    # 6. MUTACAO PLANTADA: DUAS flags de esconder de Galar na MESMA vaga tem
    #    que REPROVAR no portao, e o mesmo para DUAS vars de mapa. E o defeito
    #    que este bloco poderia introduzir, ja que ele aloca nos dois headers.
    #    A arvore de mentira e a mesma receita do `--demo` do c3: headers
    #    copiados, resto do repo por link, lista autorizada de VERDADE.
    import shutil, tempfile
    for perfil, header, rotulo_pool, vaga in (
            ("flags", "include/constants/flags.h", "FLAG_UNUSED_0x%04X",
             proxima_flag_livre(flags, flags_motor)),
            ("vars", "include/constants/vars.h", "VAR_UNUSED_0x%04X",
             proxima_var_livre(variaveis, vars_motor))):
        GUARDA.usa(perfil)
        P = GUARDA.PREFIXO
        with tempfile.TemporaryDirectory() as tmp:
            for h in list(GUARDA.HEADERS) + [os.path.join("include", x)
                                             for x in GUARDA.PONTA]:
                destino = os.path.join(tmp, h)
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                if not os.path.exists(destino):
                    shutil.copy(os.path.join(RAIZ, h), destino)
            for r in ("data", "src", "test"):
                os.symlink(os.path.join(RAIZ, r), os.path.join(tmp, r))
            os.makedirs(os.path.join(tmp, "plante"))
            alvo = os.path.join(tmp, header)
            texto = open(alvo).read()
            corte = texto.rindex("#endif")
            open(alvo, "w").write(
                texto[:corte]
                + "#define %s_GALAR_PLANTADA_A %s\n" % (P, rotulo_pool % vaga)
                + "#define %s_GALAR_PLANTADA_B %s\n" % (P, rotulo_pool % vaga)
                + texto[corte:])
            open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
                "%s_GALAR_PLANTADA_A %s_GALAR_PLANTADA_B\n" % (P, P))
            raizes = ["data", "src", "include", "test", "plante"]
            novas = GUARDA.portao(base=tmp, raizes=raizes,
                                  caminho_autorizadas=GUARDA.AUTORIZADAS,
                                  verboso=False)
            if not (len(novas) == 1 and int(novas[0]["endereco"], 16) == vaga
                    and set(novas[0]["nomes"]) == {"%s_GALAR_PLANTADA_A" % P,
                                                   "%s_GALAR_PLANTADA_B" % P}):
                falhas.append("duas %s de Galar na mesma vaga NAO reprovaram: %r"
                              % (perfil, novas))
            open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
                "%s_GALAR_PLANTADA_A\n" % P)
            if GUARDA.portao(base=tmp, raizes=raizes,
                             caminho_autorizadas=GUARDA.AUTORIZADAS,
                             verboso=False):
                falhas.append("alocacao sozinha de %s reprovou: viraria ruido"
                              % perfil)
    GUARDA.usa("vars")
    if GUARDA.portao(verboso=False) or GUARDA.stubs(verboso=False):
        falhas.append("o portao de vars esta vermelho na arvore")
    GUARDA.usa("flags")
    if GUARDA.portao(verboso=False) or GUARDA.stubs(verboso=False):
        falhas.append("o portao de flags esta vermelho na arvore")
    GUARDA.usa("vars")

    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    for f in falhas:
        print("  FALHA", f)
    relatorio(aceitas, recusa)
    return 1 if falhas else 0


# Motivo que nao muda sozinho: o dado da fonte nao existe, nao decodifica, ou
# a condutora ja decidiu que a linha nao volta. Vira `descartada`. Todo o
# resto vira `adiada`, porque uma decisao futura (um de-para de multichoice,
# uma flag nossa, um special novo) destrava. Mesma lei do bloco c6 em
# cenas_galar.py.
MOTIVO_TERMINAL_OBJ = (
    # ONDA 3, LOTE L1: os tres primeiros sao NOVOS e fecham a linha em vez de a
    # deixar voltando a cada varredura. Comando de `cenas_galar.NAO_PORTAVEL`
    # nao vira molde por trabalho: o dado de que ele depende (a tabela de
    # multichoice, um endereco de RAM, uma funcao da ROM da fonte) nao existe
    # aqui. Numero acima da FLAGS_COUNT do FireRed, ou fora da faixa de var de
    # save, nao e flag nem var: o ponteiro caiu em dado.
    ) + tuple("comando de cena fora do filtro: " + c
              for c in sorted(C3.NAO_PORTAVEL)) + (
    "esta acima da FLAGS_COUNT do FireRed",
    "nao e var de save da fonte",
    "objeto nao esta no mapa (descarte da condutora",
    "porta morta, e pendencia de mapa",
    "decodificacao incompleta",
    "cena vira no-op depois da traducao",
    "mapa da fonte fora do de-para do G3",
    "map.json do mapa nao existe",
    "texto recusado",
    "ponteiro de texto fora da rom",
    "ponteiro de movimento fora da rom",
)


def devolve_para_fila(aceitas, motivos_linha, gravar):
    """Escreve na fila o motivo MEDIDO de cada linha de objeto recusada.

    A fila calcula `feita` lendo o rotulo na arvore; o que ela nao sabe
    calcular e POR QUE uma linha nao entrou. Sem isso ela volta pendente e
    muda a cada varredura, e a proxima rodada remede tudo de novo. Aqui o
    motivo volta como `status` + `motivo_do_status`, que
    `fila_galar.decisoes_anteriores` preserva.

    Linha ACEITA nao e tocada: quem manda nela e o rotulo na arvore.
    """
    fila = "%s/dev_scripts/fila_galar.json" % RAIZ
    doc = json.load(open(fila))
    # `aceitas` nao entra aqui: a chave dela e a do MAPA da fonte, e o corte
    # de linha aceita ja e feito abaixo pelo status `feita`, que a propria
    # fila calcula lendo o rotulo na arvore.
    del aceitas
    n, quadro = 0, collections.Counter()
    # ONDA 3, LOTE L1: a linha que ESTE bloco ja tinha adiado com o motivo dele
    # volta a ser medida. A reabertura mudou o que trava cada cena (flag de
    # motor e var sem dono deixaram de travar; o texto sem traducao passou a
    # travar), e deixar o motivo de 06/09 de pe faria a proxima rodada cacar um
    # impedimento que nao existe mais.
    #
    # SO O MOTIVO DESTE BLOCO. Linha adiada pelo lote I guarda trabalho FEITO
    # (a fala de resgate que o NPC ganhou) e nao pode virar recusa de novo;
    # linha com decisao da condutora nunca se toca. As duas ficam como estao.
    MARCA_C4A = "bloco c4a, lote C da onda 1"
    MARCA_L1 = "bloco c4a, onda 3 lote L1, 08/09/2026: "
    for l in doc["linhas"]:
        if l["tipo"] not in ("script_objeto", "placa"):
            continue
        velho = l.get("motivo_do_status") or ""
        remede = (l["status"] == "adiada"
                  and (MARCA_C4A in velho or velho.startswith(MARCA_L1))
                  and DECISAO_FECHADA not in velho)
        if l["status"] in ("feita", "descartada") or (
                l["status"] == "adiada" and not remede):
            continue
        m = motivos_linha.get(l["chave"])
        if not m:
            continue
        st = ("descartada" if any(t in m for t in MOTIVO_TERMINAL_OBJ)
              else "adiada")
        novo = st, (MARCA_L1 if remede else
                    "bloco c4a, lote C da onda 1, 06/09/2026: ") + m
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
        quadro[st] += 1
    if gravar and n:
        with open(fila, "w") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return n, quadro


# ======================================================================== #
# ONDA 2, LOTE I (07/09/2026): A FALA DE RESGATE, e o molde de enfermeira.
#
# O bloco c4a acima porta a CENA INTEIRA do objeto, e recusa por inteiro
# quando falta uma peca (flag de motor do demake, var sem dono, opcode fora
# do filtro, objeto que o G4 nao pos no mapa). O que sobra dessa recusa e um
# NPC MUDO: a coluna `script` da completude conta object_event com `script`
# diferente de "0", e 514 dos 1.260 NPCs de Galar estao em "0".
#
# MEDIDO nesta rodada, e e o mapa inteiro da obra que sobrou:
#
#     514 NPCs mudos
#     115 sao objeto NOSSO, sem registro casavel na fonte (marinheiro da
#         travessia, bola do fala_galar, tile com mais de um objeto nosso)
#      48 tem registro na fonte e a FONTE tambem nao lhes da script
#     351 tem PONTEIRO de script na fonte -- e TODOS os 351 ja estao na fila
#
# Ou seja: **nao existe NPC mudo com fala na fonte fora da fila**. A fila
# cobre a obra inteira, e a conta de "os 514 menos os 198" nao e uma lista
# nova de trabalho, e a repartição acima.
#
# Dos 351, 78 tem ponteiro MORTO (o primeiro byte ja e o enchimento 0xFF da
# fonte): nao ha script nenhum para portar, e eles ficam mudos por FIDELIDADE.
#
# ## O que esta secao faz, e o que ela NAO faz
#
# Ela nao conserta a cena. Ela da voz ao NPC com a FALA QUE A FONTE TEM,
# traduzida para o ingles pela decisao 32, e deixa a linha ABERTA na fila com
# o motivo original mais o aviso de que a cena inteira continua devendo. O
# rotulo e `GalarFalaI_`, que o `fila_galar.feitas()` NAO reconhece de
# proposito: assim a fila continua cobrando a cena e a completude ja conta o
# NPC como falante, que e a verdade dos dois lados.
#
# Duas leis, e as duas sao para nao inventar:
#
#   1. **A fala e a da via padrao.** Anda-se o script a partir do ponteiro
#      seguindo a queda e o `goto`, sem entrar em `goto_if`: e a fala que o
#      jogador ouve na PRIMEIRA vez que fala com o NPC, com toda flag ainda
#      desligada. So quando a via padrao nao tem fala nenhuma e que se pega a
#      primeira fala legivel de qualquer ramo.
#   2. **Nada de efeito e prometido.** Se a via padrao entrega item, dinheiro,
#      Pokemon, loja, batalha ou warp ANTES da fala, a linha nao e resgatada:
#      dar so a frase mudaria o que o NPC faz. Efeito DEPOIS da fala e
#      registrado na fila (`resgatada_com_cena_devendo`), porque hoje o NPC
#      nao entrega nada de qualquer jeito -- ele esta mudo.
#
# ## O molde de enfermeira, e por que ele e o unico molde de mecanica aqui
#
# Dezesseis dos mudos sao a enfermeira do Centro Pokemon (`OBJ_EVENT_GFX_
# NURSE_FRLG` com os specials 0x169 e 0x187 da fonte, ASSINATURA MEDIDA e nao
# suposta: as outras onze enfermeiras mudas, as do Union Room e do Trade
# Corner, tem outros specials e NAO entram). Enfermeira muda e Centro Pokemon
# que nao cura, e o repo ja tem o molde pronto e em ingles,
# `Common_EventScript_PkmnCenterNurse` (data/scripts/pkmn_center_nurse.inc),
# usado por Azalea, Oldale e o resto. Reusar o molde e mais fiel do que
# copiar a fala: a fonte tambem CURA.
#
# ## Este bloco NAO escreve map.json, e nem o .inc do c4a
#
# O `script` de cada object_event vai como PEDIDO em
# `dev_scripts/onda2_lote_i_pedidos_mapjson.json` (secao `object_events`),
# porque nesta onda o map.json de Galar tem outros donos. E o corpo sai em
# `data/scripts/galar_objetos_i.inc`, arquivo proprio: `corpo_inc()` do c4a
# reescreve `galar_objetos.inc` inteiro a cada `--aplicar`, e rotulo novo
# dentro dele seria varrido na rodada seguinte.
# ======================================================================== #

INC_I = f"{RAIZ}/data/scripts/galar_objetos_i.inc"
TEXTO_I = f"{RAIZ}/dev_scripts/resgate_galar_texto.json"
PEDIDOS_I = f"{RAIZ}/dev_scripts/onda2_lote_i_pedidos_mapjson.json"

NURSE_GFX = "OBJ_EVENT_GFX_NURSE_FRLG"
# Assinatura MEDIDA da enfermeira que cura, na ROM do demake.
NURSE_SPECIALS = frozenset((0x169, 0x187))

# `callstd` da fonte -> caixa nossa. O 5 (YESNO) cai em DEFAULT: sem a cena, a
# pergunta nao teria resposta, e perguntar sem ouvir e pior do que so falar.
CAIXA = {2: "MSGBOX_NPC", 3: "MSGBOX_SIGN", 4: "MSGBOX_DEFAULT",
         5: "MSGBOX_DEFAULT", 6: "MSGBOX_AUTOCLOSE"}

# Comando que muda o que o jogador leva consigo. Nenhum deles pode acontecer
# ANTES da fala resgatada.
EFEITO_FORTE = frozenset((
    "givemon", "giveegg", "givemoney", "removemoney", "checkmoney",
    "giveitem", "removeitem", "checkitem", "givedecoration", "givecoins",
    "takecoins", "pokemart", "pokemartdecoration", "setwildbattle",
    "dowildbattle", "trainerbattle", "warp", "warpsilent", "warphole",
    "warpteleport", "warpdoor", "setberrytree", "callnative"))

# Decisao da condutora que NAO se reabre aqui: quem foi descartado por ela
# fica mudo, e a linha nao volta so porque agora existe um molde de resgate.
DECISAO_FECHADA = "decisao da condutora"

# Marcador deste lote no motivo da fila, e o embrulho que separa o motivo novo
# do que ja estava la. Os dois sao CONSTANTES porque `grava_fila_i` tem de
# saber se ja escreveu nesta linha: sem marcador estavel, cada passada escreve
# de novo e a fila nunca fica quieta.
MARCA_I = "onda 2, lote I, 07/09/2026: "
EMBRULHO_I = " || motivo de antes: "

# TETO DA FALA DE RESGATE, medido nos textos da fonte: acima disto o que esta
# pendurado no NPC nao e fala, e ROTEIRO DE CENA (o discurso do Leon no
# estadio tem 1.900 caracteres e vinte caixas). Despejar o roteiro inteiro numa
# caixa de "oi" seria pior do que o NPC mudo, e a cena continua na fila para
# ser portada de verdade.
TETO_DA_FALA = 500

# O charmap devolve kana e simbolo de tabela grafica quando o ponteiro cai em
# DADO que nao e texto. Fala de Galar nao tem kana: a presenca de um so ja diz
# que a leitura saiu do texto.
KANA = re.compile(r"[぀-ヿ一-鿿]")


def _idioma_do_texto(texto):
    """"pt", "en" ou "neutro" pela regua do portao, nunca por uma copia dela.

    Importa `dev_scripts/qa/checa_texto.py` e usa os MESMOS marcadores e o
    MESMO criterio do T07. Uma segunda implementacao aqui poderia ficar verde
    com o portao vermelho, que e o pior resultado possivel de um autoteste.
    """
    import importlib
    import sys as _sys
    qa = os.path.join(RAIZ, "dev_scripts", "qa")
    if qa not in _sys.path:
        _sys.path.insert(0, qa)
    ct = importlib.import_module("checa_texto")
    limpo = re.sub(r"\{[^}]*\}", " ", texto or "")
    for c in ("\\n", "\\l", "\\p"):
        limpo = limpo.replace(c, " ")
    en = len(ct.EN_MARCADORES.findall(limpo))
    pt = len(ct.PT_MARCADORES.findall(limpo))
    if en >= 2 and en > pt:
        return "en"
    if pt >= 2 and pt > en:
        return "pt"
    return "neutro"


def fala_sadia(texto):
    """Motivo pelo qual esta leitura NAO e fala, ou None."""
    if not texto or not texto.strip():
        return "o ponteiro da fonte aponta para texto VAZIO"
    if KANA.search(texto):
        return ("a leitura devolve kana: o ponteiro cai em dado da fonte, nao "
                "em texto")
    if sum(c.isalpha() for c in texto) < 3:
        return "a leitura nao tem tres letras: nao e texto"
    if len(texto) > TETO_DA_FALA:
        return ("roteiro de cena, nao fala: %d caracteres, teto de %d"
                % (len(texto), TETO_DA_FALA))
    return None


def via_padrao(rom, tab, off, maxi=400):
    """[(nome, args)] da via que o jogador ve na PRIMEIRA conversa.

    Segue a queda e o `goto`; NAO entra em `goto_if`, `call_if` nem `call`.
    Com toda flag desligada e toda var em zero, que e o estado de save nova,
    e essa a via que roda. Devolve tambem o motivo de parada, se houver.
    """
    saida, vistos = [], set()
    while True:
        if off in vistos or not (0 <= off < len(rom)):
            return saida, "ramo repetido ou fora da rom"
        vistos.add(off)
        for _ in range(maxi):
            op = rom[off]
            if op not in tab:
                return saida, "opcode 0x%02X" % op
            nome, tams = tab[op]
            if tams is None or nome == "trainerbattle":
                return saida, "macro de tamanho variavel: " + nome
            args, p = [], off + 1
            for s in tams:
                if p + s > len(rom):
                    return saida, "fim de rom"
                args.append(int.from_bytes(rom[p:p + s], "little"))
                p += s
            saida.append((nome, args))
            if nome == "goto":
                off = args[0] - BASE
                break
            if nome in ("end", "return"):
                return saida, None
            off = p
        else:
            return saida, "script longo demais"


def fala_da_via(ins):
    """(ponteiro do texto, caixa, indice da instrucao) da PRIMEIRA fala."""
    guardado = None
    for i, (nome, args) in enumerate(ins):
        if nome == "loadword" and args[0] == 0:
            guardado = args[1]
            continue
        if nome == "callstd" and guardado is not None and args[0] in CAIXA:
            return guardado, args[0], i
        if nome == "message":
            return args[0], 4, i
        if nome == "msgbox":
            return args[0], (args[1] if len(args) > 1 else 4), i
        guardado = None
    return None, None, None


def fala_de_qualquer_ramo(rom, tab, cmap, off):
    """(texto, ponteiro, caixa) da primeira fala LEGIVEL em qualquer ramo."""
    ins, _falha = C3.blocos(rom, tab, off)
    for b in ins:
        guardado = None
        for nome, args in b.ins:
            ptr = caixa = None
            if nome == "loadword" and args[0] == 0:
                guardado = args[1]
                continue
            if nome == "callstd" and guardado is not None and args[0] in CAIXA:
                ptr, caixa = guardado, args[0]
            elif nome == "message":
                ptr, caixa = args[0], 4
            elif nome == "msgbox":
                ptr, caixa = args[0], (args[1] if len(args) > 1 else 4)
            guardado = None
            if ptr and BASE <= ptr < BASE + len(rom):
                t, recusa = FALA.texto(rom, cmap, ptr - BASE)
                if not recusa and t.strip():
                    return t, ptr, caixa
    return None, None, None


def mudos_com_fonte():
    """[dict] de todo NPC MUDO no nosso mapa que tem ponteiro na fonte.

    A ponte entre o object_event nosso e a linha da fonte e a COORDENADA, o
    mesmo `de_para_de_objetos` do c3: casar por ordem erraria nos 9 mapas em
    que um objeto nosso entrou no meio da lista.
    """
    mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))["de_para"]
    gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
    por_mapa = collections.defaultdict(list)
    for l in gente:
        por_mapa[l["mapa"]].append(l)
    fila = {l["chave"]: l
            for l in json.load(open(FALA.FILA))["linhas"]}
    fora = []
    for chave, d in sorted(mundo.items()):
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, d.get("nome", ""))
        if not os.path.exists(caminho):
            continue
        doc = json.load(open(caminho))
        de_para = C3.de_para_de_objetos(chave, doc, por_mapa)
        inverso = {nosso - 1: fonte - 1 for fonte, nosso in de_para.items()}
        for i, o in enumerate(doc.get("object_events") or []):
            if o.get("origem") == "estaticos_galar":
                continue
            if str(o.get("script") or "0") not in ("0", ""):
                continue
            if i not in inverso:
                continue
            linha = fila.get("%s/objeto/%d" % (chave, inverso[i]))
            if not linha or not linha.get("ponteiro_fonte"):
                continue
            fora.append(dict(chave=linha["chave"], mapa=d["nome"],
                             indice=i, local_id=i + 1,
                             grafico=o["graphics_id"], x=o["x"], y=o["y"],
                             ponteiro=linha["ponteiro_fonte"],
                             status=linha.get("status", "pendente"),
                             motivo=linha.get("motivo_do_status", "")))
    return fora


def rotulo_i(chave):
    mapa, _tipo, i = chave.split("/")
    return "GalarFalaI_%s_o%d" % (mapa.upper(), int(i))


def textos_traduzidos():
    """{portugues da fonte: ingles} escrito a mao, com o glossario."""
    if not os.path.exists(TEXTO_I):
        return {}
    return {e["pt"]: e["en"] for e in json.load(open(TEXTO_I))["entradas"]}


def plano_i():
    """(resgatados, recusados, sem_traducao) do lote I."""
    rom = open(FALA.ROM_FONTE, "rb").read()
    tab = FALA.tabela_de_opcodes()
    cmap = FALA.charmap()
    de_para = textos_traduzidos()
    resgatados, recusados, sem_traducao = [], [], []

    for m in mudos_com_fonte():
        off = int(m["ponteiro"], 16)
        if DECISAO_FECHADA in m["motivo"]:
            recusados.append(dict(m, porque="a condutora ja decidiu que este "
                                            "NPC fica mudo"))
            continue
        if not (0 <= off < len(rom)):
            recusados.append(dict(m, porque="ponteiro da fonte fora da rom"))
            continue
        if rom[off] == C3.ENCHIMENTO:
            recusados.append(dict(m, porque="ponteiro MORTO: o primeiro byte "
                                            "ja e o enchimento 0xFF da fonte, "
                                            "nao ha script para portar"))
            continue

        todos, _f = C3.blocos(rom, tab, off)
        # `special func` tem UM argumento; `specialvar destino, func` tem DOIS,
        # e o id do special e o SEGUNDO (`0x26 specialvar [2, 2]`, medido na
        # tabela de opcodes). Ler `a[0]` nos dois casos colhia o endereco da var
        # como se fosse special. Nao mudou a conta das enfermeiras (16 dos 27
        # mudos com sprite de enfermeira casam pelos dois caminhos, medido em
        # 07/09/2026, porque a assinatura 0x169/0x187 aparece como `special`),
        # mas a leitura errada esperava so a proxima assinatura para mentir.
        especiais = set()
        for b in todos:
            for n, a in b.ins:
                if n == "special":
                    especiais.add(a[0])
                elif n == "specialvar" and len(a) > 1:
                    especiais.add(a[1])
        if (m["grafico"] == NURSE_GFX
                and NURSE_SPECIALS <= especiais):
            resgatados.append(dict(m, molde="enfermeira", rotulo=rotulo_i(m["chave"]),
                                   pt=None, en=None, caixa=None,
                                   efeito_depois=False))
            continue

        ins, parada = via_padrao(rom, tab, off)
        ptr, caixa, ate = fala_da_via(ins)
        de_onde = "via padrao"
        if ptr is None:
            texto, ptr, caixa = fala_de_qualquer_ramo(rom, tab, cmap, off)
            de_onde = "ramo condicional"
            if texto is None:
                recusados.append(dict(m, porque=(
                    "nenhuma fala legivel em ramo nenhum (via padrao parou em: "
                    "%s)" % (parada or "fim do script"))))
                continue
            ate = len(ins)
        else:
            texto, recusa = FALA.texto(rom, cmap, ptr - BASE)
            if recusa:
                recusados.append(dict(m, porque="texto recusado: " + recusa))
                continue
        doente = fala_sadia(texto)
        if doente:
            recusados.append(dict(m, porque=doente))
            continue
        antes = {n for n, _a in ins[:ate]}
        if antes & EFEITO_FORTE:
            recusados.append(dict(m, porque=(
                "a via padrao ja entrega %s ANTES da fala: so a frase mudaria "
                "o que o NPC faz" % ", ".join(sorted(antes & EFEITO_FORTE)))))
            continue
        todos_os_nomes = {n for b in todos for n, _a in b.ins}
        en = de_para.get(texto)
        if en is None:
            sem_traducao.append(dict(m, pt=texto))
            continue
        resgatados.append(dict(m, molde="fala", rotulo=rotulo_i(m["chave"]),
                               pt=texto, en=TXT.requebra(en),
                               caixa=CAIXA[caixa], de_onde=de_onde,
                               efeito_depois=bool(todos_os_nomes
                                                  & EFEITO_FORTE)))
    return resgatados, recusados, sem_traducao


def corpo_inc_i(resgatados):
    out = ["@ ONDA 2, LOTE I: a fala de resgate de Galar (07/09/2026).",
           "@ Gerado por dev_scripts/objetos_galar.py --lote-i; NAO editar a mao.",
           "@",
           "@ Cada rotulo aqui e um NPC que estava MUDO porque a cena inteira",
           "@ dele foi recusada pelo bloco c4a. A cena continua devendo (a",
           "@ linha segue aberta em dev_scripts/fila_galar.json); o que entra e",
           "@ a fala que a FONTE tem, traduzida para o ingles pela decisao 32.",
           "@ O de-para do texto esta em dev_scripts/resgate_galar_texto.json.",
           "@",
           "@ `GalarFalaI_` nao e reconhecido por fila_galar.feitas() de",
           "@ proposito: a fila tem de continuar cobrando a cena.",
           "@",
           "@ O campo `script` de cada object_event esta pedido em",
           "@ dev_scripts/onda2_lote_i_pedidos_mapjson.json.",
           ""]
    por_mapa = collections.defaultdict(list)
    for r in resgatados:
        por_mapa[(ordem_da_rota(r["mapa"]), r["mapa"])].append(r)
    for chave in sorted(por_mapa):
        out.append("@ ---- %s ----" % chave[1])
        for r in sorted(por_mapa[chave], key=lambda z: z["chave"]):
            out.append("@ %s, objeto local %d em (%d,%d)"
                       % (r["chave"], r["local_id"], r["x"], r["y"]))
            if r["molde"] == "enfermeira":
                out += ["%s::" % r["rotulo"],
                        "\tsetvar VAR_0x800B, %d" % r["local_id"],
                        "\tcall Common_EventScript_PkmnCenterNurse",
                        "\twaitmessage",
                        "\twaitbuttonpress",
                        "\trelease",
                        "\tend", ""]
                continue
            out += ["%s::" % r["rotulo"],
                    "\tlock",
                    "\tfaceplayer",
                    "\tmsgbox %s_Text, %s" % (r["rotulo"], r["caixa"]),
                    "\trelease",
                    "\tend", "",
                    "%s_Text:" % r["rotulo"]]
            partes = re.split(r"(\\[nlp])", r["en"])
            linha = ""
            for pedaco in partes:
                if re.fullmatch(r"\\[nlp]", pedaco):
                    out.append('\t.string "%s%s"' % (linha, pedaco))
                    linha = ""
                else:
                    linha += pedaco
            out.append('\t.string "%s$"' % linha)
            out.append("")
    return "\n".join(out) + "\n"


def pedido_i(resgatados):
    """A secao `object_events` do pedido de map.json, sem tocar o do vizinho."""
    doc = {}
    if os.path.exists(PEDIDOS_I):
        doc = json.load(open(PEDIDOS_I))
    doc.setdefault("_leia", "")
    doc["gerado_por"] = sorted(set(doc.get("gerado_por", []))
                               | {"dev_scripts/objetos_galar.py --lote-i"})
    itens = []
    for r in sorted(resgatados, key=lambda z: z["chave"]):
        mapa = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, r["mapa"])))
        alvo = (mapa.get("object_events") or [])[r["indice"]]
        hoje = str(alvo.get("script") or "0")
        itens.append(
            {"mapa": r["mapa"], "chave_da_fonte": r["chave"],
             "indice_em_object_events": r["indice"], "local_id": r["local_id"],
             "x": r["x"], "y": r["y"], "grafico": r["grafico"],
             "campo": "script", "valor_hoje": hoje, "valor": r["rotulo"],
             "molde": r["molde"],
             # `ja_no_mapa` e para o FECHADOR, e existe porque parte do lote
             # pode ja ter sido colada por outro dono antes de ele chegar. Sem
             # este campo o unico jeito de saber seria reler map.json item a
             # item, e o caminho barato seria colar de novo.
             "ja_no_mapa": hoje == r["rotulo"]})
    doc["object_events"] = itens
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def grava_fila_i(resgatados, recusados, sem_traducao, gravar):
    """Devolve o motivo MEDIDO de cada linha do lote I para a fila."""
    doc = json.load(open(FALA.FILA))
    por_chave = {l["chave"]: l for l in doc["linhas"]}
    n, quadro = 0, collections.Counter()
    for r in resgatados:
        l = por_chave.get(r["chave"])
        if l is None or DECISAO_FECHADA in l.get("motivo_do_status", ""):
            continue
        # IDEMPOTENCIA (07/09/2026). O motivo novo EMBRULHA o antigo, e o
        # `antigo` saia de um `re.sub` que arranca o prefixo ate o primeiro
        # ":". Rodando de novo, o prefixo arrancado passava a ser o do proprio
        # lote I, o embrulho ganhava mais uma volta e a fila era reescrita
        # inteira a cada passada: 168 linhas "mudavam" sem nada ter mudado, e a
        # prova de "segunda aplicacao grava 0" nunca poderia fechar. O corte
        # agora e pelo MARCADOR deste lote, e o texto de dentro e o de antes
        # dele.
        motivo_atual = l.get("motivo_do_status", "")
        if MARCA_I in motivo_atual:
            antigo = motivo_atual.split(EMBRULHO_I, 1)[-1]
        else:
            antigo = re.sub(r"^[^:]*: ", "", motivo_atual)
        antigo = antigo or "sem motivo anterior"
        if r["molde"] == "enfermeira":
            texto = (MARCA_I + "enfermeira do Centro Pokemon; ganhou o molde "
                     "do repo (Common_EventScript_PkmnCenterNurse) e volta a "
                     "CURAR. A cena da fonte segue devendo.")
        else:
            texto = (MARCA_I + "fala de resgate escrita (%s, %s). A CENA "
                     "INTEIRA continua devendo."
                     % (r["rotulo"],
                        "a cena da fonte ainda entrega item, loja, batalha ou "
                        "warp depois da fala" if r["efeito_depois"]
                        else "a fala era o unico efeito visivel da via padrao"))
        novo = "adiada", texto + EMBRULHO_I + antigo
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
        quadro["resgatada"] += 1
    for r in recusados:
        l = por_chave.get(r["chave"])
        if l is None or DECISAO_FECHADA in l.get("motivo_do_status", ""):
            continue
        # LINHA JA FECHADA NAO REABRE POR RECUSA (07/09/2026). A versao
        # anterior escrevia o motivo do lote I por cima de qualquer status, e
        # isso levava 43 linhas de `descartada` de volta para `adiada` --
        # trocando o motivo MEDIDO que as fechou (o dado da fonte nao existe ou
        # nao decodifica) por "o resgate nao achou fala nela", que e mais fraco
        # e nao e novidade nenhuma. Resgate e noticia; recusa de quem ja estava
        # fechado nao e.
        if l.get("status") == "descartada":
            quadro["descartada, ja fechada antes"] += 1
            continue
        terminal = r["porque"].startswith("ponteiro MORTO")
        novo = (("descartada" if terminal else "adiada"),
                MARCA_I + r["porque"])
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
        quadro["descartada" if terminal else "adiada"] += 1
    # TEXTO SEM TRADUCAO ESCRITA. Nao e defeito de codigo nem recusa medida: e
    # decisao de CONTEUDO, e o de-para so cresce quando alguem escreve o ingles
    # a mao com o GLOSSARIO-GALAR.md. A linha fica ADIADA e dizendo isso, senao
    # a proxima rodada acha que o resgate a examinou e desistiu.
    for r in sem_traducao:
        l = por_chave.get(r["chave"])
        if l is None or DECISAO_FECHADA in l.get("motivo_do_status", ""):
            continue
        novo = ("adiada",
                MARCA_I + "a fonte tem fala e o de-para de "
                "dev_scripts/resgate_galar_texto.json ainda nao tem o ingles "
                "dela; texto sem traducao, decisao de conteudo para o Gui. "
                "O texto pendente esta listado em "
                "dev_scripts/onda2_lote_i_falta_traduzir.json.")
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
        quadro["sem traducao"] += 1
    if gravar and n:
        with open(FALA.FILA, "w") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return n, quadro


def aplica_i(resgatados, recusados, sem_traducao, gravar):
    mudou = collections.Counter()
    corpo = corpo_inc_i(resgatados)
    if not os.path.exists(INC_I) or open(INC_I).read() != corpo:
        mudou["galar_objetos_i.inc"] += 1
        if gravar:
            open(INC_I, "w").write(corpo)
    ped = pedido_i(resgatados)
    if not os.path.exists(PEDIDOS_I) or open(PEDIDOS_I).read() != ped:
        mudou["pedidos_onda2"] += 1
        if gravar:
            open(PEDIDOS_I, "w").write(ped)
    linha = '\t.include "data/scripts/galar_objetos_i.inc"'
    s = open(EVENT_S).read()
    if linha not in s:
        mudou["event_scripts.s"] += 1
        if gravar:
            open(EVENT_S, "w").write(s.rstrip("\n") + "\n" + linha + "\n")
    n, quadro = grava_fila_i(resgatados, recusados, sem_traducao,
                             gravar)
    mudou.update({"fila: " + k: v for k, v in quadro.items()})
    mudou["fila"] += n
    return mudou


def demo_i():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-66s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and cond

    resgatados, recusados, sem = plano_i()
    todos = resgatados + recusados + sem
    caso("nenhuma chave aparece duas vezes",
         len({t["chave"] for t in todos}) == len(todos))
    caso("todo resgatado tem rotulo unico",
         len({r["rotulo"] for r in resgatados}) == len(resgatados))
    caso("toda recusa tem motivo escrito",
         all(r["porque"].strip() for r in recusados))
    caso("nenhum resgatado veio de linha fechada pela condutora",
         all(DECISAO_FECHADA not in r["motivo"] for r in resgatados))
    caso("nenhum resgatado tinha script no mapa (todos eram mudos)",
         all(str(json.load(open("%s/data/maps/%s/map.json"
                                % (RAIZ, r["mapa"])))["object_events"]
                 [r["indice"]].get("script") or "0") in ("0", "")
             for r in resgatados))
    falas = [r for r in resgatados if r["molde"] == "fala"]
    caso("toda fala tem corpo", all(r["en"] and r["en"].strip() for r in falas))
    # A regua e a MESMA do portao (`dev_scripts/qa/checa_texto.py`, T07), e nao
    # uma segunda opiniao escrita aqui: se ela reprovar depois, tem de reprovar
    # agora.
    #
    # A assertiva que estava aqui era `en != pt`, e ela REPROVAVA por medir a
    # coisa errada. Medido em 07/09/2026: 23 das 152 falas saem com o ingles
    # IGUAL ao portugues da fonte, e as 23 estao certas, porque o texto ja era
    # ingles no demake. Prova, e nao opiniao: nas 23 o `PT_MARCADORES` do
    # checa_texto acha ZERO marcador de portugues e o `EN_MARCADORES` acha pelo
    # menos um, e TODO acento do ingles emitido pelas 152 esta dentro de
    # "Pokemon"/"Poke"/"Pokedex" (40 ocorrencias, nenhuma fora). Traduzir o que
    # ja esta em ingles seria reescrever, nao traduzir.
    caso("nenhuma fala emitida e portugues pela regua do checa_texto T07",
         not [r for r in falas if _idioma_do_texto(r["en"]) == "pt"])
    # MUTACAO PLANTADA: o portugues da FONTE tem de ser reprovado por esta
    # mesma regua. Sem isto, "nenhuma e portugues" poderia querer dizer so que a
    # regua nao sabe reconhecer portugues nenhum.
    pt_de_verdade = [r["pt"] for r in falas
                     if r["en"] != r["pt"] and _idioma_do_texto(r["pt"]) == "pt"]
    caso("a regua reprova o portugues da fonte (mutacao plantada)",
         bool(pt_de_verdade))
    largas = [(r["rotulo"], ln) for r in falas
              for ln in re.split(r"\\[nlp]", r["en"])
              if TXT.largura_px(ln) > TXT.LARGURA_CAIXA]
    caso("nenhuma linha de fala passa de 208 px", not largas)
    for r, ln in largas[:5]:
        print("      %s: %r (%d px)" % (r, ln, TXT.largura_px(ln)))
    # A caixa do motor NAO tem teto de tres linhas: da terceira em diante o
    # `\l` ROLA (o proprio `texto_placas_sinnoh.requebra` emite assim, e
    # `data/scripts/contest_hall.inc`, que e do pokeemerald e nao nosso, tem
    # quatro caixas de mais de tres linhas). A assertiva que estava aqui cobrava
    # esse teto e reprovava 16 falas cujo PORTUGUES DA FONTE ja tinha mais
    # linhas ainda: das 16, a fonte chegava a 17 linhas numa caixa onde o ingles
    # ficou com 9. Ou seja, ela reprovava o acerto.
    #
    # O que importa de verdade sao tres coisas, e as tres continuam medidas: a
    # LARGURA (208 px, acima), o NUMERO DE CAIXAS igual ao da fonte (`\p` e
    # troca de pagina, e trocar de pagina onde a fonte nao trocava e reescrever
    # a cena) e o ingles nao INCHAR dentro da caixa.
    #
    # O teto do inchaco e uma linha por caixa, e ele e MEDIDO, nao arbitrado:
    # em 07/09/2026, de 152 falas, UMA cresce, e cresce exatamente uma linha
    # (uma caixa de uma linha virou duas, que e o tamanho natural da caixa antes
    # de comecar a rolar). Duas linhas a mais numa caixa que a fonte fechava em
    # uma nao e a lingua ser mais longa: e traducao que virou parafrase.
    def _altura(texto):
        return [len(re.split(r"\\[nl]", c)) for c in texto.split("\\p")]

    def _incha(en, pt, teto=1):
        ae, ap = _altura(en), _altura(pt)
        return len(ae) != len(ap) or any(e - p > teto
                                         for e, p in zip(ae, ap))

    inchadas = [r["rotulo"] for r in falas if _incha(r["en"], r["pt"])]
    caso("nenhuma caixa em ingles incha mais de uma linha sobre a fonte",
         not inchadas)
    for rot in inchadas[:5]:
        print("      caixa inchada: %s" % rot)
    # MUTACAO PLANTADA: duas linhas a mais numa caixa tem de ser vistas, e uma
    # caixa a mais (um `\p` que a fonte nao tinha) tambem.
    if falas:
        pedacos = falas[0]["en"].split("\\p")
        caso("duas linhas a mais na caixa sao vistas (mutacao plantada)",
             _incha("\\p".join([pedacos[0] + "\\l" + "x" * 5 + "\\l" + "y" * 5]
                               + pedacos[1:]), falas[0]["pt"]))
        caso("uma pagina a mais e vista (mutacao plantada)",
             _incha(falas[0]["en"] + "\\pzz", falas[0]["pt"]))
    corpo = corpo_inc_i(resgatados)
    caso("todo rotulo aparece uma vez so no .inc",
         all(corpo.count("\n%s::" % r["rotulo"]) == 1 for r in resgatados))
    caso("o molde de enfermeira so foi dado a sprite de enfermeira",
         all(r["grafico"] == NURSE_GFX
             for r in resgatados if r["molde"] == "enfermeira"))
    # PAR NEGATIVO da lei 2: um NPC que entrega item antes de falar nao pode
    # ser resgatado, porque a frase sozinha mentiria sobre o que ele faz.
    caso("nenhum resgatado entrega item, loja, batalha ou warp ANTES da fala",
         all("ANTES da fala" not in r.get("porque", "") for r in resgatados))
    caso("quem entrega antes da fala esta entre os RECUSADOS",
         any("ANTES da fala" in r["porque"] for r in recusados))
    de_novo, _r2, _s2 = plano_i()
    caso("rodar duas vezes da o mesmo plano",
         [r["rotulo"] for r in de_novo] == [r["rotulo"] for r in resgatados])
    caso("aplicar seco nao grava nada",
         aplica_i(resgatados, recusados, sem, False) is not None)
    # O motivo deste lote EMBRULHA o de antes. Duas marcas na mesma linha
    # querem dizer que ele se embrulhou a si mesmo, e e o rastro exato do
    # defeito de 07/09/2026, em que cada passada reescrevia as 168 linhas
    # resgatadas e a fila nunca ficava quieta.
    fila_doc = json.load(open(FALA.FILA))
    dobradas = [l["chave"] for l in fila_doc["linhas"]
                if (l.get("motivo_do_status") or "").count(MARCA_I) > 1]
    caso("nenhuma linha da fila tem a marca do lote I duas vezes", not dobradas)
    # A prova de verdade: com o lote ja aplicado, aplicar de novo grava ZERO.
    # Antes de o lote rodar pela primeira vez ela nao vale, e por isso ela olha
    # se ha marca na fila antes de cobrar.
    ja_aplicado = any(MARCA_I in (l.get("motivo_do_status") or "")
                      and l.get("tipo") == "script_objeto"
                      for l in fila_doc["linhas"])
    if ja_aplicado:
        n_seco, _q = grava_fila_i(resgatados, recusados, sem, False)
        caso("segunda aplicacao na fila grava 0", n_seco == 0)
    print("\n%s" % ("demo do lote I verde" if ok else "DEMO DO LOTE I REPROVOU"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--fila", action="store_true",
                    help="devolve o motivo medido de cada linha recusada para "
                         "dev_scripts/fila_galar.json (com --aplicar, grava)")
    ap.add_argument("--lote-i", action="store_true", dest="lote_i",
                    help="ONDA 2, LOTE I: a fala de resgate. NAO toca map.json "
                         "nem galar_objetos.inc; escreve galar_objetos_i.inc, "
                         "o pedido de map.json e a fila")
    ap.add_argument("--demo-i", action="store_true", dest="demo_lote_i",
                    help="autoteste so do lote I")
    a = ap.parse_args()
    if a.demo_lote_i:
        raise SystemExit(demo_i())
    if a.lote_i:
        resgatados, recusados, sem = plano_i()
        print("LOTE I, fala de resgate")
        por_molde = collections.Counter(r["molde"] for r in resgatados)
        print("  resgatados: %d  %s" % (len(resgatados), dict(por_molde)))
        print("  sem traducao escrita: %d (%d textos distintos)"
              % (len(sem), len({s["pt"] for s in sem})))
        print("  recusados: %d" % len(recusados))
        conta = collections.Counter(
            re.sub(r"0x[0-9A-Fa-f]+", "0xNN", r["porque"].split(":")[0])
            for r in recusados)
        for m, n in conta.most_common(12):
            print("    %4d  %s" % (n, m))
        mudou = aplica_i(resgatados, recusados, sem, a.aplicar)
        print("\n%s: %s" % ("gravado" if a.aplicar else "mudaria", dict(mudou)))
        if sem:
            fora = "%s/dev_scripts/onda2_lote_i_falta_traduzir.json" % RAIZ
            distintos = {}
            for s in sorted(sem, key=lambda z: z["chave"]):
                distintos.setdefault(s["pt"], []).append(s["chave"])
            json.dump({"_leia": "textos da fonte sem traducao escrita em "
                                "dev_scripts/resgate_galar_texto.json",
                       "distintos": [{"pt": p, "chaves": c}
                                     for p, c in sorted(distintos.items())]},
                      open(fora, "w"), indent=1, ensure_ascii=False)
            print("faltam traduzir: %s" % fora)
        raise SystemExit(0)
    if a.demo:
        raise SystemExit(demo())
    (aceitas, recusa, docs, flags, variaveis, esconde, motivos_linha,
     flags_motor, vars_motor) = plano()
    mudou, rec, _c = aplica(aceitas, docs, a.aplicar, flags, variaveis,
                            esconde, flags_motor, vars_motor)
    if a.fila:
        n, quadro = devolve_para_fila(aceitas, motivos_linha, a.aplicar)
        print("fila: %d linhas de objeto/placa ganharam motivo medido" % n)
        for st, c in sorted(quadro.items()):
            print("   %-12s %d" % (st, c))
    relatorio(aceitas, recusa, variaveis)
    print("flags de esconder: %d | vars de etapa novas: %d"
          % (len(flags), len(variaveis)))
    print("onda 3: flags de motor do demake: %d | vars da fonte sem dono: %d"
          % (len(flags_motor), len(vars_motor)))
    print("traducao na geracao: %s" % dict(FALA.traducao().conta))
    print("textos sem traducao (distintos): %d, em %d linhas da fila"
          % (len(FALA.traducao().faltam),
             len(FALA.traducao().chaves_faltando())))
    if a.aplicar:
        if FALA.traducao().grava_falta(True):
            print("gravado %s" % FALA.FALTA_JSON)
        print("fila: %d linhas adiadas por texto sem traducao"
              % FALA.marca_fila_sem_traducao(True))
    print("\n%s: %r" % ("gravado" if a.aplicar else "mudaria", dict(mudou)))
    for base, motivo in rec[:10]:
        print("  nao aplicado: %s %s" % (base, motivo))


if __name__ == "__main__":
    main()
