#!/usr/bin/env python3
"""FASE DE CONTEUDO DE GALAR, balde d: TREINADOR.

    python3 dev_scripts/treinadores_galar.py            # so mede e relata
    python3 dev_scripts/treinadores_galar.py --aplicar  # escreve tudo
    python3 dev_scripts/treinadores_galar.py --demo     # autoteste

## O STRIDE, medido antes de acreditar em qualquer numero

O `PLANO-CONTEUDO-GALAR.md` avisa que so 165 de 741 times passavam na validacao
e manda medir o stride antes de acreditar. Medido em 22/08/2026, e o aviso
estava meio certo:

  - **A tabela `gTrainers` E a do FireRed**: base 0x23EAC8, 40 B por entrada,
    ponteiro de party em +0x24. Provado por CONTAGEM, nao por fe: varrendo
    palavras alinhadas na regiao, 736 dos 774 ponteiros de ROM achados estao a
    exatamente 40 B do anterior. Nenhum outro delta chega perto.
  - **O que NAO e do FireRed e o struct do POKEMON da party.** O FireRed usa
    `u16 iv; u8 lvl; u16 species` (6 B, 8 com item, 14 com golpes, 16 com os
    dois). O demake usa o molde do CFRU: `u16 iv; u16 lvl; u16 species;
    u16 heldItem` e mais `u16 moves[4]` quando ha golpe proprio, ou seja
    **8 B e 16 B, so dois tamanhos**. Foi isso que reprovou os 576: `lvl` como
    u8 desalinha `species` em dois bytes e o resto da party vira lixo.

Com 8/16, **735 dos 741 times passam** (1 ponteiro nulo, que e o id 0, e 5
entradas de sobra da fonte). 2.057 Pokemon, 511 especies distintas, nivel de 2 a
100 com mediana 48. O `--demo` planta o molde 6/14 e exige que o portao reprove.

## A CURVA: 255 EM TUDO, e e decisao do Gui (22/08/2026)

*"curva de Galar TRAVADA EM 255 (regiao plana de pos-jogo: todo treinador de
Galar no nivel 255, lider ou comum)"*. Entao o nivel da fonte e LIDO (para
medir) e DESCARTADO (para escrever). Nao ha reescalonamento, nao ha
`curva_de_nivel.py` para Galar.

## O que NAO atravessa da fonte, e o motivo de cada um

- **Golpes.** A tabela de golpes do demake e a do CFRU, e o id dela nao e o
  nosso. Traduzir por id daria golpe errado calado. E traduzir por nome so
  valeria a pena se o moveset servisse: um moveset montado para nivel 13 num
  Pokemon de nivel 255 e pior do que o que o motor escolhe sozinho (os quatro
  ultimos golpes do learnset). Fica de fora **de proposito**, e os chefes da
  Fase F trazem moveset escrito a mao.
- **Item de segurar.** Mesmo argumento: Oran Berry de treinador de nivel 13 e
  ruido em 255. Fora, de proposito.
- **IV/EV/natureza/habilidade.** A fonte nao tem (o struct CFRU so guarda um
  `iv` unico). Treinador comum fica com o padrao do motor; chefe recebe da
  Fase F.

## CLASSE: de-para POR NOME, lido da propria ROM da fonte

`gTrainerClassNames` do demake, 13 B por entrada, achada por ANCORA (a cadeia
"Youngster" no indice 57, que e `TRAINER_CLASS_YOUNGSTER` do FireRed; base
0x23E558, confirmada porque o indice 12 volta "Model" e o 84 volta "Leader").
O demake REESCREVEU boa parte dos nomes (0..56 viraram classes de Galar), entao
casar por INDICE entregaria classe errada. Casa-se por NOME normalizado contra
as 117 classes deste motor, com `TRAINER_CLASS_*_FRLG` na frente. O que nao casa
entra em `MAO` com decisao escrita, e o que nem em `MAO` esta vira placeholder e
sai listado em `CLASSES_NOVAS_GALAR.md`.

## Faixa de id: 3000 a 3399, e ela e escolhida para nao brigar

O maior id declarado hoje e 2536 e `MAX_TRAINERS_COUNT` e 4000. Comecar em 2537
seria o "proximo livre", mas seis executores rodam em paralelo e o proximo livre
e exatamente onde todo mundo apende. Galar apanha **3000-3399**, longe do ponto
de apend. Custo: **zero**. A flag de "ja venci" e `TRAINER_FLAGS_START + id`, e
a faixa inteira ja esta dimensionada por `MAX_TRAINERS_COUNT`; nenhuma flag nova
e pedida e a save nao muda.

## UMA batalha por objeto, e o resto sai com motivo

Um `script_objeto` da fonte pode carregar varios `trainerbattle`: rival com tres
variantes por inicial, revanche, missao de estadio. Este gerador emite **a
PRIMEIRA batalha alcancada num percurso LINEAR** (sem seguir `goto_if`/`call`),
que e a unica que se pode afirmar sem ler a condicao de cada ramo. As demais
saem contadas. Vale para a missao de ginasio tambem: ver o relatorio por
ginasio que `--aplicar` imprime.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import fala_galar as FALA           # noqa: E402
import estaticos_galar as EST       # noqa: E402

BASE = 0x08000000
TRAINERS_OFF = 0x23EAC8             # gTrainers, medido
TRAINERS_N = 741
STRIDE = 40                         # struct Trainer do FireRed
MON = {0: 8, 1: 16, 2: 8, 3: 16}    # partyFlags & 3 -> bytes por Pokemon (CFRU)
CLASSES_OFF = 0x23E558              # confirmado pela ancora, nao digitado
CLASSE_STRIDE = 13
ANCORA_CLASSE = ("Youngster", 57)

# TRAINER_NAME_LENGTH deste motor (include/constants/global.h). O demake grava
# ate 12 bytes de nome; nome mais longo estoura o array e o build reprova com
# "excess elements in array initializer". Corta-se, e o corte e contado.
NOME_MAX = 10

ID_BASE = 3000
ID_TETO = 3400
NIVEL = 255                         # decisao do Gui, 22/08/2026

INC = f"{RAIZ}/data/scripts/galar_treinadores.inc"
PARTY = f"{RAIZ}/src/data/trainers.party"
OPPS = f"{RAIZ}/include/constants/opponents.h"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
CLASSES_MD = f"{RAIZ}/CLASSES_NOVAS_GALAR.md"

MARCA_INI = "// >>> Fase de conteudo de Galar, balde d: treinadores (dev_scripts/treinadores_galar.py) >>>"
MARCA_FIM = "// <<< Fase de conteudo de Galar, balde d <<<"
P_INI = "/* >>> Fase de conteudo de Galar, balde d (dev_scripts/treinadores_galar.py) >>> */"
P_FIM = "/* <<< Fase de conteudo de Galar, balde d <<< */"

# Classes do demake que NAO existem neste motor. Decisao escrita uma a uma:
# a classe mais proxima do motor, no espirito da de-para de sprite que Sinnoh
# usou. Nenhuma delas vira classe nova; ver CLASSES_NOVAS_GALAR.md.
MAO = {
    "team yell": ("TRAINER_CLASS_TEAM_AQUA", "gangue de rua; a Aqua e a gangue do motor"),
    "macro cosmos": ("TRAINER_CLASS_MAGMA_ADMIN", "seguranca de corporacao, terno"),
    "membro": ("TRAINER_CLASS_TEAM_AQUA", "capanga generico"),
    "mochileira": ("TRAINER_CLASS_HIKER_FRLG", "backpacker feminino"),
    "backpacker": ("TRAINER_CLASS_HIKER_FRLG", "backpacker"),
    "policial": ("TRAINER_CLASS_GENTLEMAN_FRLG", "uniforme, adulto"),
    "beldade": ("TRAINER_CLASS_BEAUTY_FRLG", "e 'beauty' em portugues"),
    "model": ("TRAINER_CLASS_BEAUTY_FRLG", "modelo"),
    "madame": ("TRAINER_CLASS_LADY_FRLG", "senhora rica"),
    "doctor": ("TRAINER_CLASS_SCIENTIST_FRLG", "jaleco"),
    "dancer": ("TRAINER_CLASS_GUITARIST", "artista de palco"),
    "musician": ("TRAINER_CLASS_GUITARIST", "musico"),
    "cabbie": ("TRAINER_CLASS_SAILOR_FRLG", "trabalhador de uniforme"),
    "poke kid": ("TRAINER_CLASS_YOUNGSTER_FRLG", "crianca"),
    "poke pkid": ("TRAINER_CLASS_YOUNGSTER_FRLG", "crianca"),
    "office worke": ("TRAINER_CLASS_GENTLEMAN_FRLG", "escritorio, terno"),
    "cook derek": ("TRAINER_CLASS_KINDLER", "cozinheiro"),
    "trainer star": ("TRAINER_CLASS_COOLTRAINER_FRLG", "estrela de liga"),
    "dojo master": ("TRAINER_CLASS_BLACK_BELT_FRLG", "mestre de dojo"),
    "worker": ("TRAINER_CLASS_HIKER_FRLG", "operario"),
    "scoemtost": ("TRAINER_CLASS_SCIENTIST_FRLG", "'Scientist' escrito torto na fonte"),
    "troathlete": ("TRAINER_CLASS_TRIATHLETE", "'Triathlete' escrito torto na fonte"),
    "ruin mamoac": ("TRAINER_CLASS_RUIN_MANIAC_FRLG", "'Ruin Maniac' escrito torto na fonte"),
    "boss": ("TRAINER_CLASS_BOSS_FRLG", "chefe de equipe"),
    "rival": ("TRAINER_CLASS_RIVAL_LATE_FRLG", "rival"),
    "interviewer": ("TRAINER_CLASS_INTERVIEWER", "reporter"),
    "expert": ("TRAINER_CLASS_EXPERT", "expert"),
    "gambler": ("TRAINER_CLASS_GAMER_FRLG", "'Gambler' e o 'Gamer' do FireRed"),
    "pokemaniac": ("TRAINER_CLASS_POKEMANIAC_FRLG", "acento na fonte"),
    "sr and jr": ("TRAINER_CLASS_SR_AND_JR", "irmaos"),
    "sis and bro": ("TRAINER_CLASS_SIS_AND_BRO_FRLG", "irmaos"),
    "cool couple": ("TRAINER_CLASS_COOL_COUPLE_FRLG", "casal"),
    # Os cinco abaixo entraram na segunda passada, olhando o proprio
    # CLASSES_NOVAS_GALAR.md: eram placeholder por causa de caractere que a
    # normalizacao come (o simbolo de genero) ou de mojibake da fonte
    # (`ウエ` e o `PKMN` do FireRed lido com a tabela errada).
    "ace trainer": ("TRAINER_CLASS_COOLTRAINER_FRLG",
                    "'Ace Trainer' e o nome moderno do Cooltrainer do FRLG"),
    "swimmer": ("TRAINER_CLASS_SWIMMER_M_FRLG", "swimmer sem simbolo de genero"),
    "ranger": ("TRAINER_CLASS_PKMN_RANGER_FRLG",
               "'ウエ Ranger' e `PKMN Ranger` com a tabela de nome errada"),
    "trainter": ("TRAINER_CLASS_COOLTRAINER_FRLG",
                 "'ウエ Trainter' e `PKMN Trainer` torto na fonte"),
    "trainer": ("TRAINER_CLASS_COOLTRAINER_FRLG", "PKMN Trainer generico"),
}
# Classe sem casamento nem MAO: placeholder DECLARADO, nunca silencioso.
PLACEHOLDER = "TRAINER_CLASS_COOLTRAINER_FRLG"

# Pic por classe, quando o nome da classe nao acha pic do mesmo nome.
PIC_MAO = {
    "TRAINER_CLASS_TEAM_AQUA": ("TRAINER_PIC_AQUA_GRUNT_M", "TRAINER_PIC_AQUA_GRUNT_F"),
    "TRAINER_CLASS_MAGMA_ADMIN": ("TRAINER_PIC_MAGMA_ADMIN", "TRAINER_PIC_MAGMA_ADMIN"),
    "TRAINER_CLASS_COOLTRAINER_FRLG": ("TRAINER_PIC_COOLTRAINER_M_FRLG",
                                       "TRAINER_PIC_COOLTRAINER_F_FRLG"),
    "TRAINER_CLASS_RIVAL_LATE_FRLG": ("TRAINER_PIC_RIVAL_LATE_FRLG",
                                      "TRAINER_PIC_RIVAL_LATE_FRLG"),
    "TRAINER_CLASS_RIVAL_EARLY_FRLG": ("TRAINER_PIC_RIVAL_EARLY_FRLG",
                                       "TRAINER_PIC_RIVAL_EARLY_FRLG"),
    "TRAINER_CLASS_BOSS_FRLG": ("TRAINER_PIC_LEADER_GIOVANNI_FRLG",
                                "TRAINER_PIC_LEADER_GIOVANNI_FRLG"),
    "TRAINER_CLASS_LEADER_FRLG": ("TRAINER_PIC_LEADER_BROCK_FRLG",
                                  "TRAINER_PIC_LEADER_MISTY_FRLG"),
    "TRAINER_CLASS_CHAMPION_FRLG": ("TRAINER_PIC_CHAMPION_RIVAL_FRLG",
                                    "TRAINER_PIC_CHAMPION_RIVAL_FRLG"),
    "TRAINER_CLASS_ELITE_FOUR_FRLG": ("TRAINER_PIC_ELITE_FOUR_BRUNO_FRLG",
                                      "TRAINER_PIC_ELITE_FOUR_LORELEI_FRLG"),
    "TRAINER_CLASS_HIKER_FRLG": ("TRAINER_PIC_HIKER_FRLG", "TRAINER_PIC_HIKER_FRLG"),
    "TRAINER_CLASS_GENTLEMAN_FRLG": ("TRAINER_PIC_GENTLEMAN_FRLG",
                                     "TRAINER_PIC_GENTLEMAN_FRLG"),
    "TRAINER_CLASS_SCIENTIST_FRLG": ("TRAINER_PIC_SCIENTIST_FRLG",
                                     "TRAINER_PIC_SCIENTIST_FRLG"),
    "TRAINER_CLASS_GUITARIST": ("TRAINER_PIC_GUITARIST", "TRAINER_PIC_GUITARIST"),
    "TRAINER_CLASS_KINDLER": ("TRAINER_PIC_KINDLER", "TRAINER_PIC_KINDLER"),
    "TRAINER_CLASS_BLACK_BELT_FRLG": ("TRAINER_PIC_BLACK_BELT_FRLG",
                                      "TRAINER_PIC_BLACK_BELT_FRLG"),
    "TRAINER_CLASS_TRIATHLETE": ("TRAINER_PIC_RUNNING_TRIATHLETE_M",
                                 "TRAINER_PIC_RUNNING_TRIATHLETE_F"),
    "TRAINER_CLASS_EXPERT": ("TRAINER_PIC_EXPERT_M", "TRAINER_PIC_EXPERT_F"),
    "TRAINER_CLASS_INTERVIEWER": ("TRAINER_PIC_INTERVIEWER", "TRAINER_PIC_INTERVIEWER"),
    "TRAINER_CLASS_SR_AND_JR": ("TRAINER_PIC_SR_AND_JR", "TRAINER_PIC_SR_AND_JR"),
    "TRAINER_CLASS_PSYCHIC_FRLG": ("TRAINER_PIC_PSYCHIC_M_FRLG",
                                   "TRAINER_PIC_PSYCHIC_F_FRLG"),
    "TRAINER_CLASS_SWIMMER_M_FRLG": ("TRAINER_PIC_SWIMMER_M_FRLG",
                                     "TRAINER_PIC_SWIMMER_M_FRLG"),
    "TRAINER_CLASS_SWIMMER_F_FRLG": ("TRAINER_PIC_SWIMMER_F_FRLG",
                                     "TRAINER_PIC_SWIMMER_F_FRLG"),
    "TRAINER_CLASS_TUBER_FRLG": ("TRAINER_PIC_TUBER_M", "TRAINER_PIC_TUBER_F_FRLG"),
    "TRAINER_CLASS_PKMN_BREEDER_FRLG": ("TRAINER_PIC_POKEMON_BREEDER_FRLG",
                                        "TRAINER_PIC_POKEMON_BREEDER_FRLG"),
    "TRAINER_CLASS_PKMN_RANGER_FRLG": ("TRAINER_PIC_POKEMON_RANGER_M_FRLG",
                                       "TRAINER_PIC_POKEMON_RANGER_F_FRLG"),
    "TRAINER_CLASS_TWINS_FRLG": ("TRAINER_PIC_TWINS_FRLG", "TRAINER_PIC_TWINS_FRLG"),
    "TRAINER_CLASS_YOUNG_COUPLE_FRLG": ("TRAINER_PIC_YOUNG_COUPLE_FRLG",
                                        "TRAINER_PIC_YOUNG_COUPLE_FRLG"),
    "TRAINER_CLASS_CRUSH_KIN_FRLG": ("TRAINER_PIC_CRUSH_KIN_FRLG",
                                     "TRAINER_PIC_CRUSH_KIN_FRLG"),
    "TRAINER_CLASS_COOL_COUPLE_FRLG": ("TRAINER_PIC_COOL_COUPLE_FRLG",
                                       "TRAINER_PIC_COOL_COUPLE_FRLG"),
    "TRAINER_CLASS_SIS_AND_BRO_FRLG": ("TRAINER_PIC_SIS_AND_BRO_FRLG",
                                       "TRAINER_PIC_SIS_AND_BRO_FRLG"),
    "TRAINER_CLASS_BIRD_KEEPER_FRLG": ("TRAINER_PIC_BIRD_KEEPER_FRLG",
                                       "TRAINER_PIC_BIRD_KEEPER_FRLG"),
    "TRAINER_CLASS_LADY_FRLG": ("TRAINER_PIC_LADY_FRLG", "TRAINER_PIC_LADY_FRLG"),
    "TRAINER_CLASS_BEAUTY_FRLG": ("TRAINER_PIC_BEAUTY_FRLG", "TRAINER_PIC_BEAUTY_FRLG"),
    "TRAINER_CLASS_GAMER_FRLG": ("TRAINER_PIC_GAMER_FRLG", "TRAINER_PIC_GAMER_FRLG"),
    "TRAINER_CLASS_AROMA_LADY_FRLG": ("TRAINER_PIC_AROMA_LADY_FRLG",
                                      "TRAINER_PIC_AROMA_LADY_FRLG"),
    "TRAINER_CLASS_RUIN_MANIAC_FRLG": ("TRAINER_PIC_RUIN_MANIAC_FRLG",
                                       "TRAINER_PIC_RUIN_MANIAC_FRLG"),
    "TRAINER_CLASS_CRUSH_GIRL_FRLG": ("TRAINER_PIC_CRUSH_GIRL_FRLG",
                                      "TRAINER_PIC_CRUSH_GIRL_FRLG"),
    "TRAINER_CLASS_CHANNELER_FRLG": ("TRAINER_PIC_CHANNELER_FRLG",
                                     "TRAINER_PIC_CHANNELER_FRLG"),
}

# Nomes que o demake DIGITOU ERRADO na propria tabela de nomes. Nao e forma nem
# ambiguidade: e erro de digitacao da fonte, conferido letra a letra contra o
# nosso species.h. Sem esta tabela, quatro times inteiros caem.
ERRO_DE_DIGITACAO = {
    "SPECIES_POLTEGEIST": "SPECIES_POLTEAGEIST",
    "SPECIES_BARASKEWDA": "SPECIES_BARRASKEWDA",
    "SPECIES_CORVSQUIRE": "SPECIES_CORVISQUIRE",
    "SPECIES_STONJORNER": "SPECIES_STONJOURNER",
    "SPECIES_CENTSKORCH": "SPECIES_CENTISKORCH",
}

# `trainerbattle` da fonte: tipo -> (quantos ponteiros, molde de emissao).
# Molde: 'single'  = trainerbattle_single T, intro, derrota
#        'nointro' = trainerbattle_no_intro T, derrota
#        'double'  = trainerbattle_double T, intro, derrota, poucos
#        'rival'   = trainerbattle_earlyrival T, 0, derrota, vitoria
# (quantos ponteiros a macro emite, molde, quantos deles sao TEXTO).
# O terceiro numero importa: nos tipos CONTINUE_SCRIPT o ULTIMO ponteiro e um
# EVENT SCRIPT, nao texto, e tentar decodifica-lo como cadeia derruba a linha
# com "byte 0xF9 fora do charmap" (foi assim que a Opal ficou de fora numa
# rodada). A continuacao em si nao e portada: ela cai fora com a batalha.
TIPOS = {0: (2, "single", 2), 1: (3, "single", 2), 2: (3, "single", 2),
         3: (1, "nointro", 1), 4: (3, "double", 3), 5: (2, "single", 2),
         6: (4, "double", 3), 7: (3, "double", 3), 8: (4, "double", 3),
         9: (2, "rival", 2)}


# ------------------------------------------------------------------ leitura --
def _norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def classes_da_fonte(rom, base=CLASSES_OFF):
    """{indice: nome} de gTrainerClassNames do demake, conferida pela ancora."""
    cm, _ = EST._inverso_do_charmap()

    def nome(i):
        fora = []
        for b in rom[base + i * CLASSE_STRIDE:base + (i + 1) * CLASSE_STRIDE]:
            if b == 0xFF:
                break
            fora.append(cm.get(b, "?"))
        return "".join(fora).strip()

    alvo, idx = ANCORA_CLASSE
    if nome(idx) != alvo:
        raise SystemExit("gTrainerClassNames: a ancora %r nao esta no indice %d "
                         "(base 0x%X devolveu %r). A ROM da fonte mudou?"
                         % (alvo, idx, base, nome(idx)))
    return {i: nome(i) for i in range(107)}


def treinadores_da_fonte(rom, mon=None):
    """{id: dict} de gTrainers, com o molde de party MEDIDO.

    `mon` existe so para o --demo plantar o molde 6/14 do FireRed e provar que
    o portao reprova; em producao ele e sempre MON.
    """
    mon = MON if mon is None else mon
    cm, _ = EST._inverso_do_charmap()
    fora = {}
    for i in range(TRAINERS_N):
        o = TRAINERS_OFF + i * STRIDE
        pf, cls = rom[o], rom[o + 1]
        genero = rom[o + 2] & 0x80
        psz = rom[o + 0x20]
        p = struct.unpack_from("<I", rom, o + 0x24)[0]
        nome = []
        for b in rom[o + 4:o + 16]:
            if b == 0xFF:
                break
            nome.append(cm.get(b, "?"))
        d = dict(id=i, classe=cls, genero=1 if genero else 0,
                 duplo=bool(rom[o + 0x18]), nome="".join(nome).strip(),
                 party=None, falha=None)
        fora[i] = d
        if not (BASE <= p < BASE + len(rom)):
            d["falha"] = "ponteiro de party fora da ROM"
            continue
        if not 1 <= psz <= 6:
            d["falha"] = "partySize %d" % psz
            continue
        if pf & ~3:
            d["falha"] = "partyFlags 0x%02X" % pf
            continue
        sz = mon[pf & 3]
        po, time, ruim = p - BASE, [], None
        for j in range(psz):
            m = po + j * sz
            iv, lvl, sp, item = struct.unpack_from("<HHHH", rom, m)
            if not 1 <= lvl <= 100 or not 1 <= sp <= 1300 or iv > 255:
                ruim = ("Pokemon %d fora de faixa (iv %d, nivel %d, especie %d)"
                        % (j, iv, lvl, sp))
                break
            time.append(dict(especie_fonte=sp, nivel_fonte=lvl))
        if ruim:
            d["falha"] = ruim
        else:
            d["party"] = time
    return fora


def stride_medido(rom):
    """(stride, quantos deltas casaram). Mede, nao acredita no cabecalho."""
    ptrs = []
    for off in range(TRAINERS_OFF, TRAINERS_OFF + 0x10000, 4):
        v = struct.unpack_from("<I", rom, off)[0]
        if BASE <= v < BASE + len(rom):
            ptrs.append(off)
    delta = collections.Counter(b - a for a, b in zip(ptrs, ptrs[1:]))
    (melhor, quantos), = delta.most_common(1)
    return melhor, quantos, len(ptrs)


# --------------------------------------------------------------- percurso ---
def primeira_batalha(rom, tab, inicio, maxi=400):
    """(tipo, id, ponteiros) da PRIMEIRA batalha num percurso LINEAR.

    Linear de proposito: seguir `goto_if` misturaria os ramos de um rival de
    tres iniciais e o gerador escolheria por acaso. `goto`/`call` incondicional
    E seguido, porque ali nao ha escolha nenhuma.
    """
    off, saltos = inicio, 0
    while saltos < 16:
        for _ in range(maxi):
            if not 0 <= off < len(rom):
                return None, "fim de rom"
            op = rom[off]
            if op not in tab:
                return None, "opcode 0x%02X" % op
            nome, tams = tab[op]
            if nome == "trainerbattle":
                t = rom[off + 1]
                if t not in TIPOS:
                    return None, "trainerbattle tipo %d" % t
                tid = int.from_bytes(rom[off + 2:off + 4], "little")
                n = TIPOS[t][0]
                ptrs = [int.from_bytes(rom[off + 6 + 4 * i:off + 10 + 4 * i],
                                       "little") for i in range(n)]
                return (t, tid, ptrs), None
            if tams is None:
                return None, "macro de tamanho variavel: " + nome
            args, p = [], off + 1
            for s in tams:
                args.append(int.from_bytes(rom[p:p + s], "little"))
                p += s
            if nome in ("goto", "call") and args and BASE <= args[0] < BASE + len(rom):
                off = args[0] - BASE
                saltos += 1
                break
            if nome in ("end", "return"):
                return None, "acabou sem trainerbattle"
            off = p
        else:
            return None, "script longo demais"
    return None, "saltos demais"


def conta_batalhas(rom, tab, inicio, maxi=400, cheio=False):
    """Os `trainerbattle` do script, SEGUINDO os ramos.

    Com `cheio`, devolve (tipo, id, ponteiros) em ordem de offset crescente,
    que e o que o desempate de "todos os ramos apontam para o mesmo treinador"
    precisa. Sem ele, devolve so (tipo, id), que e o que a contagem precisa.
    """
    vistos, pilha, achados = set(), [inicio], []
    while pilha:
        off = pilha.pop()
        if off in vistos or not 0 <= off < len(rom):
            continue
        vistos.add(off)
        for _ in range(maxi):
            op = rom[off]
            if op not in tab:
                break
            nome, tams = tab[op]
            if nome == "trainerbattle":
                t = rom[off + 1]
                if t not in TIPOS:
                    break
                tid = int.from_bytes(rom[off + 2:off + 4], "little")
                if cheio:
                    n = TIPOS[t][0]
                    achados.append((off, t, tid,
                                    [int.from_bytes(rom[off + 6 + 4 * i:
                                                        off + 10 + 4 * i], "little")
                                     for i in range(n)]))
                else:
                    achados.append((t, tid))
                off += FALA.TRAINERBATTLE[t]
                continue
            if tams is None:
                break
            args, p = [], off + 1
            for s in tams:
                args.append(int.from_bytes(rom[p:p + s], "little"))
                p += s
            for a in (args[:1] if nome in ("goto", "call") else
                      args[1:2] if nome in ("goto_if", "call_if") else []):
                if BASE <= a < BASE + len(rom):
                    pilha.append(a - BASE)
            if nome in ("end", "return", "goto"):
                break
            off = p
    return sorted(achados) if cheio else achados


def batalha_da_linha(rom, tab, inicio, quem=None):
    """(tipo, id, ponteiros, colapsadas) ou (None, motivo, 0).

    Tres degraus, nesta ordem, e cada um so entra quando o de cima nao responde:

    1. **Percurso LINEAR.** Nao depende de condicao nenhuma, entao e o unico
       que responde sem interpretar nada.
    2. **Ramos com UM id so.** O `trainerbattle` atras de um `goto_if` de "ja
       venci" e um treinador so por varios caminhos: nao ha escolha a fazer.
    3. **Ramos com varios ids da MESMA PESSOA.** O rival de Galar tem tres
       entradas de `gTrainers` (uma por inicial do jogador) com o MESMO nome e
       a MESMA classe: `Hop`, `Hop`, `Hop`. Escolher entre elas nao e escolher
       entre pessoas, e o inicial do jogador nao muda o time depois que a Fase
       F reescreve o chefe. Pega-se o MENOR id e conta-se quantas colapsaram.
       Ramo com nomes DIFERENTES continua recusado: ali sim ha escolha.
    """
    achado, motivo = primeira_batalha(rom, tab, inicio)
    if achado is not None:
        return achado + (0,), None
    ramos = conta_batalhas(rom, tab, inicio, cheio=True)
    if not ramos:
        return None, motivo
    ids = sorted({t for _, _, t, _ in ramos})
    if len(ids) > 1:
        pessoas = {(quem[i]["nome"], quem[i]["classe"]) for i in ids
                   if quem and i in quem}
        if not quem or len(pessoas) != 1:
            return None, ("%d treinadores diferentes atras de ramo condicional"
                          % len(ids))
        escolhido = ids[0]
        for _, t, tid, ptrs in ramos:
            if tid == escolhido:
                return (t, tid, ptrs, len(ids) - 1), None
    _, t, tid, ptrs = ramos[0]
    return (t, tid, ptrs, 0), None


# ------------------------------------------------------------------ plano ---
def de_para_classe(nomes_fonte):
    """{indice do demake: (TRAINER_CLASS_*, motivo)}. Por NOME, nunca por id."""
    fonte = open(f"{RAIZ}/include/constants/trainers.h").read()
    nossas = re.findall(r"^\s*(TRAINER_CLASS_[A-Z0-9_]+),", fonte, re.M)
    nossas = [c for c in nossas if c != "TRAINER_CLASS_COUNT"]
    por_nome = {}
    for c in nossas:                       # _FRLG primeiro: e o mesmo elenco
        chave = _norm(c[len("TRAINER_CLASS_"):].replace("_", " "))
        por_nome.setdefault(chave, c)
        if chave.endswith(" frlg"):
            por_nome[chave[:-5]] = c
    fora, novas = {}, {}
    for i, nome in nomes_fonte.items():
        n = _norm(nome)
        if not n:
            fora[i] = (PLACEHOLDER, "nome vazio na fonte")
            continue
        if n in por_nome:
            fora[i] = (por_nome[n], "casou por nome")
        elif n in MAO:
            fora[i] = (MAO[n][0], "de-para a mao: " + MAO[n][1])
        else:
            fora[i] = (PLACEHOLDER, "sem equivalente: placeholder")
            novas[nome] = i
    return fora, novas


def pic_de(classe, genero):
    if classe in PIC_MAO:
        return PIC_MAO[classe][genero]
    stem = classe[len("TRAINER_CLASS_"):]
    fonte = open(f"{RAIZ}/include/constants/trainers.h").read()
    pics = set(re.findall(r"\bTRAINER_PIC_[A-Z0-9_]+\b", fonte))
    for tent in ("TRAINER_PIC_%s" % stem,
                 "TRAINER_PIC_%s_%s" % (stem, "MF"[genero]),
                 "TRAINER_PIC_%s" % stem.replace("_FRLG", "")):
        if tent in pics:
            return tent
    return PIC_MAO[PLACEHOLDER][genero]


def rotulo(chave):
    """Mesmo padrao de `fala_galar.rotulo`: GalarTrn_<MAPA DA FONTE>_o<N>.

    Nao e estetica: `dev_scripts/fila_galar.py` mede o que ESTA feito lendo o
    rotulo do `.inc` com uma expressao unica para todos os baldes. Rotulo fora
    do padrao ficaria eternamente "pendente" numa fila que le a arvore.
    """
    mapa, tipo, i = chave.split("/")
    return "GalarTrn_%s_%s%d" % (mapa.upper(),
                                 "bg" if tipo == "bg" else "o", int(i))


def const_id(fonte_id, nome, classe_nome):
    limpo = re.sub(r"[^A-Z0-9]+", "_", (nome or classe_nome or "X").upper()).strip("_")
    return "TRAINER_GALAR_%s_%d" % (limpo or "X", fonte_id)


def plano():
    """(aceitas, treinadores, recusa, novas_classes, extra)."""
    rom, tab, cmap, fila = FALA.carrega()
    linhas = FALA.varre(rom, tab, cmap, fila)
    nomes_cls = classes_da_fonte(rom)
    cls_map, novas = de_para_classe(nomes_cls)
    fonte_tr = treinadores_da_fonte(rom)
    esp = EST.de_para_especie(rom)
    nomes_esp = EST.nomes_da_fonte(rom)
    base_do_nome = {}
    for i in sorted(nomes_esp):
        base_do_nome.setdefault(nomes_esp[i], i)

    def traduz_especie(sid):
        """(SPECIES_*, None) ou (None, motivo). Forma cai para a forma BASE.

        `de_para_especie` recusa id de nome REPETIDO de proposito: no MAPA,
        devolver a forma errada mentiria a especie do encontro. Em time de
        TREINADOR a conta e outra: a tabela de nomes da fonte nao distingue
        forma nenhuma (o `Charizard` do Gigantamax se chama `Charizard`), entao
        o unico dado que atravessa e o nome, e o que o nome diz e a forma BASE.
        Um Charizard Gigantamax vira um Charizard. Fica declarado aqui, e vale
        SO para party de treinador.
        """
        nome, motivo = esp.get(sid, (None, "id fora da tabela de nomes"))
        if nome is None and sid in nomes_esp:
            b = base_do_nome.get(nomes_esp[sid])
            if b is not None and b != sid:
                nome, motivo = esp.get(b, (None, motivo))
        if nome is None and motivo:
            m = re.match(r"^(SPECIES_[A-Z0-9_]+) nao existe", motivo)
            if m and m.group(1) in ERRO_DE_DIGITACAO:
                return ERRO_DE_DIGITACAO[m.group(1)], None
        return nome, motivo

    d = [l for l in linhas if l["balde"] == "d_treinador"]
    aceitas, recusa, usados = [], collections.Counter(), {}
    extra = collections.Counter()
    por_ginasio = collections.defaultdict(list)

    for l in sorted(d, key=lambda z: z["chave"]):
        if l["tipo"] == "script_objeto" and not l["no_mapa"]:
            recusa["objeto nao esta no mapa (descarte da condutora, 21/08)"] += 1
            continue
        achado, motivo = batalha_da_linha(rom, tab,
                                          int(l["ponteiro_fonte"], 16), fonte_tr)
        if achado is None:
            recusa["nao da para afirmar qual batalha: " + motivo] += 1
            continue
        tipo, fid, ptrs, colapsadas = achado
        extra["variantes da mesma pessoa colapsadas"] += colapsadas
        tr = fonte_tr.get(fid)
        if tr is None:
            recusa["id de treinador %d fora da tabela da fonte" % fid] += 1
            continue
        if tr["falha"]:
            recusa["time da fonte ilegivel: " + tr["falha"]] += 1
            continue
        time, ruim = [], None
        for m in tr["party"]:
            nome, mot = traduz_especie(m["especie_fonte"])
            if nome is None:
                ruim = mot
                break
            time.append(nome)
        if ruim:
            recusa["especie sem equivalente: " + ruim] += 1
            continue
        textos, ruim = [], None
        for p in ptrs[:TIPOS[tipo][2]]:
            if not BASE <= p < BASE + len(rom):
                ruim = "ponteiro de texto fora da ROM"
                break
            t, mot = FALA.texto(rom, cmap, p - BASE)
            if mot:
                ruim = mot
                break
            textos.append(t)
        if ruim:
            recusa["texto recusado: " + ruim] += 1
            continue
        molde = TIPOS[tipo][1]
        if molde == "double" and len(textos) < 3:
            recusa["batalha dupla sem os tres textos"] += 1
            continue
        classe, mot_cls = cls_map[tr["classe"]]
        if fid not in usados:
            usados[fid] = dict(
                fonte_id=fid, nome=tr["nome"] or "Trainer",
                classe=classe, motivo_classe=mot_cls,
                classe_fonte=nomes_cls[tr["classe"]],
                genero=tr["genero"], duplo=tr["duplo"], time=time)
        todas = conta_batalhas(rom, tab, int(l["ponteiro_fonte"], 16))
        extra["batalhas alem da primeira"] += max(0, len(todas) - 1)
        aceitas.append(dict(l, rotulo=rotulo(l["chave"]), fonte_id=fid,
                            tipo_tb=tipo, molde=molde, textos=textos,
                            n_batalhas=len(todas)))
        if "Gym" in l["mapa"] or nomes_cls[tr["classe"]] == "Leader":
            por_ginasio[l["mapa"]].append((tr["nome"], len(todas)))
    return aceitas, usados, recusa, novas, extra, por_ginasio


# ---------------------------------------------------------------- escrita ---
def numera(usados):
    """{fonte_id: (id nosso, constante)}, estavel: ordem do id da fonte."""
    fora = {}
    for n, fid in enumerate(sorted(usados)):
        nid = ID_BASE + n
        if nid >= ID_TETO:
            raise SystemExit("faixa 3000-3399 estourou em %d treinadores" % n)
        u = usados[fid]
        fora[fid] = (nid, const_id(fid, u["nome"], u["classe_fonte"]))
    return fora


def bloco_opponents(usados, num):
    out = [MARCA_INI,
           "// Um id por treinador de Galar CITADO por script de objeto ou placa.",
           "// Faixa exclusiva desta frente: %d a %d (o maior id fora dela era"
           % (ID_BASE, ID_TETO - 1),
           "// 2536, e o proximo livre e onde as outras frentes apendem).",
           "// Custo ZERO de save: a flag de 'ja venci' e TRAINER_FLAGS_START + id,",
           "// e a faixa inteira ja esta dimensionada por MAX_TRAINERS_COUNT (4000).",
           "// Gerado por dev_scripts/treinadores_galar.py; nao editar a mao."]
    larg = max((len(c) for _, c in num.values()), default=10) + 2
    for fid in sorted(num):
        nid, const = num[fid]
        u = usados[fid]
        out.append("#define %-*s %d  // fonte %d, %s %s"
                   % (larg, const, nid, fid, u["classe_fonte"], u["nome"]))
    out.append(MARCA_FIM)
    return "\n".join(out) + "\n"


def bloco_party(usados, num):
    out = [P_INI,
           "/* Treinadores de Galar, importados do demake Ultimate Plus v1.2.1.2.",
           "   Nivel 255 em TODOS por decisao do Gui (22/08/2026): Galar e regiao",
           "   plana de pos-jogo. O nivel da fonte foi lido (mediana 48) e",
           "   descartado de proposito. Golpe, item, IV, EV e natureza NAO vem da",
           "   fonte: ver o cabecalho de dev_scripts/treinadores_galar.py.",
           "   Os chefes que a Fase F cobre tem o time REESCRITO por",
           "   dev_scripts/fase_f_chefes.py depois deste gerador. */",
           ""]
    for fid in sorted(num):
        nid, const = num[fid]
        u = usados[fid]
        out.append("=== %s ===" % const)
        out.append("Name: %s" % (u["nome"] or "Trainer")[:NOME_MAX])
        out.append("Class: %s" % u["classe"])
        out.append("Pic: %s" % pic_de(u["classe"], u["genero"]))
        out.append("Gender: %s" % ("Female" if u["genero"] else "Male"))
        out.append("Double Battle: %s" % ("Yes" if u["duplo"] else "No"))
        for e in u["time"]:
            out += ["", e, "Level: %d" % NIVEL]
        out.append("")
    out.append(P_FIM)
    return "\n".join(out) + "\n"


def corpo_inc(aceitas, num):
    out = ["@ Treinadores de Galar, balde d da fase de conteudo.",
           "@ Gerado por dev_scripts/treinadores_galar.py; NAO editar a mao.",
           "@ Uma batalha por objeto: a PRIMEIRA de um percurso linear.", ""]
    por_mapa = collections.defaultdict(list)
    for l in aceitas:
        por_mapa[l["mapa"]].append(l)
    for mapa in sorted(por_mapa):
        out.append("@ ---- %s ----" % mapa)
        for l in sorted(por_mapa[mapa], key=lambda z: z["chave"]):
            r, const = l["rotulo"], num[l["fonte_id"]][1]
            out.append("%s::" % r)
            # PORTAO DE "JA VENCI", E ELE E OBRIGATORIO NOS DOIS MOLDES SEM INTRO.
            # Medido no emulador em 22/08/2026 pelo T147.8, que nasceu VERMELHO:
            # `trainerbattle_no_intro` (TRAINER_BATTLE_SINGLE_NO_INTRO_TEXT) e
            # `trainerbattle_earlyrival` caem os dois em
            # `EventScript_DoNoIntroTrainerBattle`, que vai DIRETO para o
            # `dotrainerbattle` sem passar pelo `specialvar GetTrainerFlag` que
            # o `EventScript_TryDoNormalTrainerBattle` tem na linha 16. Isso e
            # do motor vanilla e esta certo LA: no FireRed esses dois moldes so
            # sao alcancados depois de o treinador AVISTAR o jogador, e a flag
            # ja foi conferida antes. Aqui o objeto e falado, nao avista, entao
            # sem este portao o treinador rebriga para sempre.
            # A flag e a mesma que o motor usaria, TRAINER_FLAGS_START + id, e
            # por isso continua custando ZERO de save.
            if l["molde"] in ("nointro", "rival"):
                out.append("\tlock")
                out.append("\tfaceplayer")
                out.append("\tgoto_if_set TRAINER_FLAGS_START + %s, %s_Fim"
                           % (const, r))
            if l["molde"] == "nointro":
                out.append("\ttrainerbattle_no_intro %s, %s_Derrota" % (const, r))
            elif l["molde"] == "double":
                out.append("\ttrainerbattle_double %s, %s_Intro, %s_Derrota, "
                           "%s_Poucos" % (const, r, r, r))
            elif l["molde"] == "rival":
                out.append("\ttrainerbattle_earlyrival %s, 0, %s_Derrota, "
                           "%s_Vitoria" % (const, r, r))
            else:
                out.append("\ttrainerbattle_single %s, %s_Intro, %s_Derrota"
                           % (const, r, r))
            out.append("\tend")
            out.append("")
            if l["molde"] in ("nointro", "rival"):
                out.append("%s_Fim:" % r)
                out.append("\trelease")
                out.append("\tend")
                out.append("")
            sufixos = {"nointro": ["Derrota"], "double": ["Intro", "Derrota", "Poucos"],
                       "rival": ["Derrota", "Vitoria"],
                       "single": ["Intro", "Derrota"]}[l["molde"]]
            for suf, txt in zip(sufixos, l["textos"]):
                out.append("%s_%s:" % (r, suf))
                out.append('\t.string "%s$"' % txt)
                out.append("")
    return "\n".join(out) + "\n"


def substitui(texto, ini, fim, bloco, antes_de=None):
    """Troca o bloco marcado. Sem marca, entra ANTES de `antes_de`, nunca no fim.

    `opponents.h` acaba com `#endif` de include guard: apendar no fim poria os
    `#define` FORA do guard e eles seriam reprocessados a cada include.
    """
    i = texto.find(ini)
    if i < 0:
        if antes_de:
            k = texto.find(antes_de)
            if k < 0:
                raise SystemExit("ancora %r sumiu de %s" % (antes_de, "opponents.h"))
            return texto[:k] + bloco + "\n" + texto[k:]
        return texto.rstrip("\n") + "\n\n" + bloco
    j = texto.find(fim, i)
    j = len(texto) if j < 0 else j + len(fim) + 1
    return texto[:i] + bloco + texto[j:]


def aplica(aceitas, usados, num, gravar):
    mudou, recusa = collections.Counter(), []
    por_mapa = collections.defaultdict(list)
    for l in aceitas:
        por_mapa[l["mapa"]].append(l)
    for mapa, lista in sorted(por_mapa.items()):
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, mapa)
        if not os.path.exists(caminho):
            recusa.append({"chave": mapa, "motivo": "map.json nao existe"})
            continue
        doc = json.load(open(caminho))
        antes = json.dumps(doc, sort_keys=True)
        ja_bg = {b.get("script") for b in doc.get("bg_events", [])}
        for l in sorted(lista, key=lambda z: z["chave"]):
            if l["tipo"] == "placa":
                if l["rotulo"] in ja_bg:
                    continue
                doc.setdefault("bg_events", []).append({
                    "type": "sign", "x": l["x"], "y": l["y"], "elevation": 0,
                    "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                    "script": l["rotulo"]})
                mudou["placa"] += 1
                continue
            i, motivo = FALA.casa_objeto(doc, l["x"], l["y"])
            if i is None:
                recusa.append({"chave": l["chave"], "motivo": motivo})
                continue
            # PRECEDENCIA: batalha vence fala e vence cena. Um objeto de
            # treinador que so falasse seria o unico NPC de Galar que promete
            # briga e nao entrega.
            doc["object_events"][i]["script"] = l["rotulo"]
            mudou["objeto"] += 1
        if json.dumps(doc, sort_keys=True) != antes:
            mudou["mapa"] += 1
            if gravar:
                with open(caminho, "w") as f:
                    json.dump(doc, f, indent=2, ensure_ascii=False)
                    f.write("\n")
    if gravar:
        open(INC, "w").write(corpo_inc(aceitas, num))
        s = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_treinadores.inc"'
        if linha not in s:
            open(EVENT_S, "w").write(s.rstrip("\n") + "\n" + linha + "\n")
        t = open(OPPS).read()
        novo = substitui(t, MARCA_INI, MARCA_FIM, bloco_opponents(usados, num),
                         antes_de="#define MAX_TRAINERS_COUNT_EMERALD 4000")
        if novo != t:
            open(OPPS, "w").write(novo)
        t = open(PARTY).read()
        novo = substitui(t, P_INI, P_FIM, bloco_party(usados, num))
        if novo != t:
            open(PARTY, "w").write(novo)
    return mudou, recusa


def escreve_classes_md(novas, usados, gravar):
    linhas = ["# Classes de treinador que Galar tem e este motor nao",
              "",
              "Gerado por `dev_scripts/treinadores_galar.py`. O demake reescreveu",
              "os nomes de `gTrainerClassNames` para o elenco de Galar; as classes",
              "abaixo NAO existem entre as 117 deste motor (RSE + FRLG) e por isso",
              "entraram por de-para escrito a mao ou, quando nem isso havia, com o",
              "placeholder `%s`." % PLACEHOLDER,
              "",
              "Criar classe nova custa sprite, nome, musica de encontro e uma",
              "entrada em `trainer_class_lookups.h`: e obra propria, nao desta",
              "onda. A lista existe para o Gui decidir se quer pagar.",
              "",
              "| classe da fonte | indice | classe usada aqui | por que |",
              "|---|---|---|---|"]
    vistas = {}
    for u in usados.values():
        if u["motivo_classe"] != "casou por nome":
            vistas[u["classe_fonte"]] = u
    for nome in sorted(vistas):
        u = vistas[nome]
        linhas.append("| %s | %s | `%s` | %s |"
                      % (nome, novas.get(nome, "-"), u["classe"], u["motivo_classe"]))
    corpo = "\n".join(linhas) + "\n"
    if gravar:
        open(CLASSES_MD, "w").write(corpo)
    return corpo


# ------------------------------------------------------------------- demo ---
def demo():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-62s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and cond

    rom = open(FALA.ROM_FONTE, "rb").read()
    st, quantos, total = stride_medido(rom)
    caso("o stride medido de gTrainers e 40", st == STRIDE)
    caso("e ele domina (>90%% dos %d ponteiros)" % total, quantos > 0.9 * total)

    bons = treinadores_da_fonte(rom)
    passam = sum(1 for t in bons.values() if t["party"])
    caso("com o molde 8/16 passam mais de 700 times de 741", passam > 700)
    # PAR NEGATIVO: o molde do FireRed (6/8/14/16) e o que reprovava 576.
    ruins = treinadores_da_fonte(rom, mon={0: 6, 1: 14, 2: 8, 3: 16})
    passam_fr = sum(1 for t in ruins.values() if t["party"])
    # O molde do FireRed reprova 358 times; o medido reprova 6. Vinte vezes
    # mais: nao ha como confundir os dois moldes por acaso.
    caso("o molde 6/14 do FireRed reprova 10x mais times que o 8/16",
         (TRAINERS_N - passam_fr) > 10 * (TRAINERS_N - passam))

    cls = classes_da_fonte(rom)
    caso("a ancora de classe devolve 'Youngster' no 57", cls[57] == "Youngster")
    caso("e 'Leader' no 84 (segunda conferencia)", cls[84] == "Leader")
    try:
        classes_da_fonte(rom, base=CLASSES_OFF + 13)
        caso("base de classe deslocada REPROVA", False)
    except SystemExit:
        caso("base de classe deslocada REPROVA", True)

    mapa, novas = de_para_classe(cls)
    caso("'Youngster' casa por nome", mapa[57][1] == "casou por nome")
    caso("'Macro Cosmos' entra pelo de-para a mao",
         mapa[55][0] == "TRAINER_CLASS_MAGMA_ADMIN")
    nossas = open(f"{RAIZ}/include/constants/trainers.h").read()
    caso("toda classe escolhida existe em trainers.h",
         all(("    %s," % c) in nossas for c, _ in mapa.values()))

    aceitas, usados, recusa, novas, extra, gin = plano()
    caso("o plano aceita mais de 240 linhas", len(aceitas) > 240)
    caso("nenhum treinador aceito passa de 6 Pokemon",
         all(len(u["time"]) <= 6 for u in usados.values()))
    num = numera(usados)
    caso("todo id fica na faixa 3000-3399",
         all(ID_BASE <= n < ID_TETO for n, _ in num.values()))
    caso("as constantes de id nao repetem",
         len({c for _, c in num.values()}) == len(num))
    esp_h = open(f"{RAIZ}/include/constants/species.h").read()
    caso("toda especie escrita existe em species.h",
         all(("%s " % e) in esp_h or ("%s\n" % e) in esp_h
             for u in usados.values() for e in u["time"]))
    caso("todo pic escolhido existe em trainers.h",
         all(pic_de(u["classe"], u["genero"]) in nossas for u in usados.values()))
    caso("nenhum Name: passa de %d caracteres" % NOME_MAX,
         all(len(ln) - 6 <= NOME_MAX for ln in bloco_party(usados, num).split("\n")
             if ln.startswith("Name: ")))
    caso("todo nivel escrito e 255", "Level: 255" in bloco_party(usados, num)
         and "Level: %d" % (NIVEL - 1) not in bloco_party(usados, num))
    mudou, rec = aplica(aceitas, usados, num, gravar=False)
    caso("a aplicacao seca nao recusa mais de 5%% dos objetos",
         len(rec) <= 0.05 * len(aceitas))
    print("\n%s" % ("demo verde" if ok else "DEMO REPROVOU"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    rom = open(FALA.ROM_FONTE, "rb").read()
    st, quantos, total = stride_medido(rom)
    print("stride medido de gTrainers: %d B (%d de %d deltas)"
          % (st, quantos, total))
    aceitas, usados, recusa, novas, extra, gin = plano()
    num = numera(usados)
    print("batalhas portadas: %d em %d mapas; treinadores novos: %d (ids %d-%d)"
          % (len(aceitas), len({l["mapa"] for l in aceitas}), len(num),
             ID_BASE, ID_BASE + len(num) - 1))
    print("de fora: %d linhas" % sum(recusa.values()))
    for m, n in recusa.most_common():
        print("  %5d  %s" % (n, m))
    print("batalhas alem da primeira, deixadas de fora: %d"
          % extra["batalhas alem da primeira"])
    if novas:
        print("classes da fonte sem equivalente aqui: %d (CLASSES_NOVAS_GALAR.md)"
              % len(novas))
    print("\nginasio / lider: missao com quantas batalhas no mesmo objeto")
    for mapa in sorted(gin):
        for nome, n in gin[mapa]:
            print("  %-28s %-12s %d batalha(s) no script" % (mapa, nome, n))
    mudou, rec = aplica(aceitas, usados, num, gravar=a.aplicar)
    escreve_classes_md(novas, usados, gravar=a.aplicar)
    print("\nmudaria: %s | recusas de colocacao: %d" % (dict(mudou), len(rec)))
    for r in rec[:10]:
        print("   %s: %s" % (r["chave"], r["motivo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
