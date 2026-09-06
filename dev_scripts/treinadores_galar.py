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

# ---------------------------------------------------------- fala que falta ---
# FALA PADRAO POR CLASSE, e ela existe por dois buracos DA FONTE, nao por
# escolha nossa:
#
#   - `trainerbattle` do tipo 3 guarda UM ponteiro so, o de derrota. Sem fala de
#     abertura nao dava para usar `trainerbattle_single`, que e o unico molde
#     que consulta a flag de vitoria por dentro E devolve o jogador pelo
#     `EventScript_TryGetTrainerScript` (`releaseall`). Foi por isso que os 127
#     saiam em `trainerbattle_no_intro`, que cai em
#     `EventScript_DoNoIntroTrainerBattle` -> `gotopostbattlescript` e volta
#     direto para o `end`, com o objeto do JOGADOR ainda congelado pelo `lock`
#     (`ScrCmd_release` e o unico que chama `UnfreezeObjectEvents`; o `end` so
#     destrava `sLockFieldControls`). Ganhar a batalha travava o jogo.
#   - NENHUM tipo da fonte guarda fala de POS-BATALHA, e no idioma vanilla e ela
#     que carrega a soltura (`msgbox ..., MSGBOX_AUTOCLOSE` chama
#     `Std_MsgboxAutoclose`, que termina em `release`). Ela tambem e o caminho
#     de quem RE-FALA com um treinador ja vencido: `trainerbattle_single`,
#     `_double` e `_no_intro` vao todos para `gotopostbattlescript` nesse caso,
#     ou seja para a linha seguinte ao comando.
#
# As cadeias sao COMPARTILHADAS por classe, uma por classe e nao uma por
# treinador: 40 classes contra 268 objetos, e o texto e generico de qualquer
# jeito. Linha curta de proposito (teto de 208 px da caixa, medido por
# qa/checa_texto.py) e no maximo DUAS linhas por caixa.
TEXTO_CLASSE = {
    "TRAINER_CLASS_LEADER_FRLG": (
        "Sou o líder daqui.\nMostre o seu valor!",
        "Você lutou muito bem."),
    "TRAINER_CLASS_CHAMPION_FRLG": (
        "O topo de Galar é aqui.\nVenha me buscar!",
        "Você chegou ao topo."),
    "TRAINER_CLASS_ELITE_FOUR_FRLG": (
        "Aqui a estrada aperta.\nMostre o seu time!",
        "Siga em frente,\ntreinador."),
    "TRAINER_CLASS_BOSS_FRLG": (
        "Ninguém passa por mim.",
        "Isso não vai ficar assim."),
    "TRAINER_CLASS_RIVAL": (
        "De novo você? Então\nvamos resolver isso!",
        "Da próxima eu ganho!"),
    "TRAINER_CLASS_TEAM_AQUA": (
        "Some daqui, moleque!",
        "Tá, tá... eu já vou."),
    "TRAINER_CLASS_MAGMA_ADMIN": (
        "Área restrita.\nVolte por onde veio.",
        "Meu turno acabou mal."),
    "TRAINER_CLASS_HIKER_FRLG": (
        "Subi essa trilha inteira!\nBora batalhar?",
        "Que fôlego o seu!"),
    "TRAINER_CLASS_BEAUTY_FRLG": (
        "Você tem estilo.\nMas eu tenho time.",
        "Perdi com elegância."),
    "TRAINER_CLASS_GENTLEMAN_FRLG": (
        "Com licença. Aceita\numa batalha?",
        "Foi um prazer."),
    "TRAINER_CLASS_CHANNELER_FRLG": (
        "Eu vi o seu futuro...\ne ele é uma batalha.",
        "O futuro me enganou."),
    "TRAINER_CLASS_LASS_FRLG": (
        "Oi! Quer batalhar\ncomigo?",
        "Você é forte mesmo!"),
    "TRAINER_CLASS_YOUNGSTER_FRLG": (
        "Meu time é novo, mas\né bom. Vem!",
        "Preciso treinar mais."),
    "TRAINER_CLASS_CAMPER_FRLG": (
        "Acampei aqui só pra\nachar um bom duelo.",
        "Valeu pela batalha!"),
    "TRAINER_CLASS_BLACK_BELT_FRLG": (
        "Força e treino!\nEncare-me!",
        "Você treinou mais."),
    "TRAINER_CLASS_SWIMMER_M_FRLG": (
        "A água é minha casa.\nVamos nessa!",
        "Boa, você nada bem."),
    "TRAINER_CLASS_SAILOR_FRLG": (
        "Marujo não recusa\nbriga boa!",
        "Ancorei de vez."),
    "TRAINER_CLASS_SCIENTIST_FRLG": (
        "Minha hipótese:\neu venço. Vamos ver.",
        "Hipótese refutada."),
    "TRAINER_CLASS_GUITARIST": (
        "Toca aí! Digo,\nbatalha aí!",
        "Você afinou melhor."),
    "TRAINER_CLASS_BUG_CATCHER_FRLG": (
        "Peguei muito inseto\nhoje. Quer ver?",
        "Meus insetos cansaram."),
    "TRAINER_CLASS_COOLTRAINER_FRLG": (
        "Um duelo de verdade,\nque tal?",
        "Foi um bom duelo."),
}
# Classe sem linha propria: fala neutra, e ela e DECLARADA, nunca silenciosa.
TEXTO_PADRAO = ("Que tal uma batalha\nrápida?", "Boa batalha. Obrigado!")


def rotulos_classe(classe):
    """(rotulo do texto de abertura, rotulo do texto de pos-batalha)."""
    curto = classe.replace("TRAINER_CLASS_", "")
    return "GalarTrn_Intro_%s" % curto, "GalarTrn_Depois_%s" % curto

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
    # MOTIVO POR LINHA DA FILA, e nao so a contagem. Acrescentado em
    # 06/09/2026 pelo lote C da onda 1, pela mesma razao e no mesmo formato do
    # `por_mapa_motivo` de cenas_galar.py: a fila cobra linha a linha, e sem o
    # motivo dela a linha volta pendente e sem nada escrito a cada varredura.
    motivos_de_linha = {}
    extra = collections.Counter()
    por_ginasio = collections.defaultdict(list)

    for l in sorted(d, key=lambda z: z["chave"]):
        if l["tipo"] == "script_objeto" and not l["no_mapa"]:
            recusa["objeto nao esta no mapa (descarte da condutora, 21/08)"] += 1
            motivos_de_linha[l["chave"]] = "objeto nao esta no mapa (descarte da condutora, 21/08)"
            continue
        achado, motivo = batalha_da_linha(rom, tab,
                                          int(l["ponteiro_fonte"], 16), fonte_tr)
        if achado is None:
            recusa["nao da para afirmar qual batalha: " + motivo] += 1
            motivos_de_linha[l["chave"]] = "nao da para afirmar qual batalha: " + motivo
            continue
        tipo, fid, ptrs, colapsadas = achado
        extra["variantes da mesma pessoa colapsadas"] += colapsadas
        tr = fonte_tr.get(fid)
        if tr is None:
            recusa["id de treinador %d fora da tabela da fonte" % fid] += 1
            motivos_de_linha[l["chave"]] = "id de treinador %d fora da tabela da fonte" % fid
            continue
        if tr["falha"]:
            recusa["time da fonte ilegivel: " + tr["falha"]] += 1
            motivos_de_linha[l["chave"]] = ("time da fonte ilegivel: "
                                            + tr["falha"])
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
            motivos_de_linha[l["chave"]] = "especie sem equivalente: " + ruim
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
            motivos_de_linha[l["chave"]] = "texto recusado: " + ruim
            continue
        molde = TIPOS[tipo][1]
        if molde == "double" and len(textos) < 3:
            recusa["batalha dupla sem os tres textos"] += 1
            motivos_de_linha[l["chave"]] = "batalha dupla sem os tres textos"
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
    return (aceitas, usados, recusa, novas, extra, por_ginasio,
            motivos_de_linha)


# ---------------------------------------------------------------- escrita ---
def ids_gravados(texto=None):
    """({chave de objeto: id}, {fonte_id: id}) JA GRAVADOS em opponents.h.

    Fonte da verdade do de-para. O header e o lado velho porque e ele que a
    ROM publicada e as saves conhecem; guardar a mesma tabela num JSON ao lado
    so criaria dois donos do mesmo numero.

    Duas tabelas porque o comentario mudou de forma em 23/08/2026: ate entao
    ele so dizia `// fonte N`, e o id era do TREINADOR DA FONTE; hoje ele diz
    tambem `obj <chave>`, e o id e do OBJETO. A tabela velha continua sendo
    lida para nenhum id ja publicado se mexer.
    """
    t = texto if texto is not None else open(OPPS, encoding="utf-8").read()
    i, j = t.find(MARCA_INI), t.find(MARCA_FIM)
    if i < 0 or j < 0:
        return {}, {}
    por_obj, por_fonte = {}, {}
    for m in re.finditer(
            # `[^\s,]+` e nao `\S+`: a chave termina em virgula no comentario
            # (`// fonte 509, obj g39m02/objeto/12, Youngster Chad`), e `\S+`
            # engolia a virgula. O de-para saia com chave que nunca casava,
            # todo objeto virava novo e o `--aplicar` estourava a faixa na
            # SEGUNDA rodada. Medido em 23/08/2026.
            r"#define\s+\S+\s+(\d+)\s*//\s*fonte\s+(\d+)(?:,\s*obj\s+([^\s,]+))?",
            t[i:j]):
        nid, fid, chave = int(m.group(1)), int(m.group(2)), m.group(3)
        if chave:
            por_obj[chave] = nid
        else:
            por_fonte.setdefault(fid, nid)
    return por_obj, por_fonte


def numera(aceitas, usados, ja=None):
    """{chave do objeto: (id nosso, constante, fonte_id)}. UM ID POR OBJETO.

    Duas regras moram aqui, e as duas nasceram de defeito medido:

    1. APPEND-ONLY. Ate 23/08/2026 esta funcao numerava `ID_BASE + n` sobre
       `sorted(usados)`, e a rodada 9 mostrou o preco: dois treinadores novos
       (fonte 686 e 733) entraram com id de fonte MENOR que o da dupla Leon
       (736/739) e empurraram os dois de 3204/3205 para 3206/3207. A flag de
       "ja venci" e `TRAINER_FLAGS_START + id`, entao um id que anda leva a
       vitoria do jogador junto.
    2. UM ID POR OBJETO. Um mesmo treinador da fonte e citado por 2 ou 3
       objetos de mapas diferentes (38 casos, 40 batalhas). Como a flag de
       vitoria e uma por ID, vencer um deles apagava a batalha dos gemeos:
       eles nasciam vencidos. Agora cada objeto tem id proprio e o TIME e
       copiado. O primeiro objeto de cada treinador (em ordem de chave) herda
       o id que ja estava publicado; os gemeos entram em APPEND.
    """
    por_obj, por_fonte = ids_gravados() if ja is None else ja
    pares = sorted({l["chave"]: l["fonte_id"] for l in aceitas}.items())
    # Nome da constante: o PRIMEIRO objeto de cada treinador fica com o nome
    # que ja esta publicado; os gemeos ganham sufixo _2, _3. A ordem e a de
    # chave, que e a da fonte, para a rodada ser reproduzivel.
    nomes, vistos = {}, collections.Counter()
    for chave, fid in pares:
        u = usados[fid]
        base = const_id(fid, u["nome"], u["classe_fonte"])
        vistos[fid] += 1
        nomes[chave] = base if vistos[fid] == 1 else "%s_%d" % (base, vistos[fid])
    fora, tomados = {}, set()
    prox = max(list(por_obj.values()) + list(por_fonte.values()),
               default=ID_BASE - 1) + 1

    def poe(chave, fid, nid):
        if not ID_BASE <= nid < ID_TETO:
            raise SystemExit("faixa %d-%d estourou no objeto %s"
                             % (ID_BASE, ID_TETO - 1, chave))
        fora[chave] = (nid, nomes[chave], fid)
        tomados.add(nid)

    for chave, fid in pares:                      # 1) id ja gravado por OBJETO
        if chave in por_obj:
            poe(chave, fid, por_obj[chave])
    for chave, fid in pares:                      # 2) id legado do TREINADOR
        if chave in fora:
            continue
        nid = por_fonte.get(fid)
        if nid is not None and nid not in tomados:
            poe(chave, fid, nid)
    for chave, fid in pares:                      # 3) APPEND
        if chave in fora:
            continue
        while prox in tomados:
            prox += 1
        poe(chave, fid, prox)
        prox += 1
    return fora


def bloco_opponents(usados, num):
    out = [MARCA_INI,
           "// Um id por OBJETO de Galar que abre batalha (script de objeto ou placa).",
           "// Faixa exclusiva desta frente: %d a %d (o maior id fora dela era"
           % (ID_BASE, ID_TETO - 1),
           "// 2536, e o proximo livre e onde as outras frentes apendem).",
           "// Custo ZERO de save: a flag de 'ja venci' e TRAINER_FLAGS_START + id,",
           "// e a faixa inteira ja esta dimensionada por MAX_TRAINERS_COUNT (4000).",
           "// Gerado por dev_scripts/treinadores_galar.py; nao editar a mao."]
    larg = max((len(v[1]) for v in num.values()), default=10) + 2
    # Ordem de ESCRITA pelo id nosso, para o arquivo ler como o que ele e:
    # uma lista append-only. Ordenar pelo id da fonte esconderia a insercao no
    # meio, que foi o defeito de 23/08/2026.
    for chave in sorted(num, key=lambda c: num[c][0]):
        nid, const, fid = num[chave]
        u = usados[fid]
        out.append("#define %-*s %d  // fonte %d, obj %s, %s %s"
                   % (larg, const, nid, fid, chave, u["classe_fonte"], u["nome"]))
    out.append(MARCA_FIM)
    return "\n".join(out) + "\n"


def chefes_da_fase_f():
    """Constantes cujo TIME pertence a dev_scripts/fase_f_chefes.json.

    38 dos 236 chefes da Fase F sao de Galar e portanto moram DENTRO do bloco
    que `bloco_party` regera do zero. Ate 23/08/2026 um `--aplicar` sozinho
    apagava os 38 times de chefe e so a memoria de quem rodava mandava chamar
    `fase_f_chefes.py --aplicar` em seguida. Agora nao regera o que nao e dele.
    """
    caminho = f"{RAIZ}/dev_scripts/fase_f_chefes.json"
    if not os.path.exists(caminho):
        return set()
    return {c["id"] for c in json.load(open(caminho, encoding="utf-8"))["chefes"]}


def times_preservados(texto=None):
    """{constante: linhas do bloco a partir do 'AI:'} para os chefes da Fase F
    que JA estao no .party.

    O cabecalho (Name/Class/Pic/Gender/Double Battle) continua vindo deste
    gerador, que e o dono dele; o AI e os Pokemon continuam vindo da Fase F,
    que e a dona deles. E a mesma divisao que `fase_f_chefes.escreve` faz do
    outro lado, so que vista daqui.
    """
    chefes = chefes_da_fase_f()
    if not chefes:
        return {}
    t = texto if texto is not None else open(PARTY, encoding="utf-8").read()
    ms = list(re.finditer(r"(?m)^=== (\S+) ===[ \t]*$", t))
    fora = {}
    for k, m in enumerate(ms):
        if m.group(1) not in chefes:
            continue
        fim = ms[k + 1].start() if k + 1 < len(ms) else len(t)
        linhas = t[m.end() + 1:fim].split("\n")
        for i, ln in enumerate(linhas):
            if ln.startswith("AI:") or not ln.strip():
                rabo = linhas[i:]
                # O ULTIMO bloco do arquivo vai ate o fim dele, e o fim dele e
                # o P_FIM: sem este corte o marcador entrava no time e saia
                # duplicado, medido em 23/08/2026. (O `fatia_bloco` da Fase F
                # chama isso de "rabeira" e preserva pelo mesmo motivo.)
                for j, x in enumerate(rabo):
                    if P_FIM in x:
                        rabo = rabo[:j]
                        break
                while rabo and not rabo[-1].strip():
                    rabo.pop()
                fora[m.group(1)] = rabo
                break
    return fora


def nomes_base(const):
    """`TRAINER_GALAR_ALLISTER_310_2` -> `TRAINER_GALAR_ALLISTER_310`."""
    return re.sub(r"_\d+$", "", const) if re.search(r"_\d+_\d+$", const) else const


def bloco_party(usados, num, preservar=None):
    preservar = times_preservados() if preservar is None else preservar
    out = [P_INI,
           "/* Treinadores de Galar, importados do demake Ultimate Plus v1.2.1.2.",
           "   Nivel 255 em TODOS por decisao do Gui (22/08/2026): Galar e regiao",
           "   plana de pos-jogo. O nivel da fonte foi lido (mediana 48) e",
           "   descartado de proposito. Golpe, item, IV, EV e natureza NAO vem da",
           "   fonte: ver o cabecalho de dev_scripts/treinadores_galar.py.",
           "   Os chefes que a Fase F cobre tem o time REESCRITO por",
           "   dev_scripts/fase_f_chefes.py depois deste gerador.",
           "   Um bloco por OBJETO: dois objetos do mesmo treinador da fonte tem",
           "   ids diferentes e times IGUAIS, porque a flag de ja-venci e uma por",
           "   id e antes disso o gemeo nascia vencido. */",
           ""]
    for chave in sorted(num, key=lambda c: num[c][0]):
        nid, const, fid = num[chave]
        u = usados[fid]
        out.append("=== %s ===" % const)
        out.append("Name: %s" % (u["nome"] or "Trainer")[:NOME_MAX])
        out.append("Class: %s" % u["classe"])
        out.append("Pic: %s" % pic_de(u["classe"], u["genero"]))
        out.append("Gender: %s" % ("Female" if u["genero"] else "Male"))
        out.append("Double Battle: %s" % ("Yes" if u["duplo"] else "No"))
        # O gemeo de um chefe da Fase F leva o MESMO time escrito a mao: sem
        # isto, o Allister de Galar_Wyndon01 teria o time cru da fonte e o de
        # Galar_StowOnSide09 o da Fase F, dois lideres com a mesma cara e
        # times diferentes.
        rabo = preservar.get(const, preservar.get(nomes_base(const)))
        if rabo is not None:
            out += rabo
            out.append("")
            continue
        for e in u["time"]:
            out += ["", e, "Level: %d" % NIVEL]
        out.append("")
    out.append(P_FIM)
    return "\n".join(out) + "\n"


def corpo_inc(aceitas, usados, num):
    out = ["@ Treinadores de Galar, balde d da fase de conteudo.",
           "@ Gerado por dev_scripts/treinadores_galar.py; NAO editar a mao.",
           "@ Uma batalha por objeto: a PRIMEIRA de um percurso linear.",
           "@",
           "@ O RABO DE TODO BLOCO E `msgbox ..., MSGBOX_AUTOCLOSE` + `release` +",
           "@ `end`, e ele NAO e enfeite: e por ali que volta quem ganhou a batalha",
           "@ (`gotopostbattlescript` cai na linha seguinte ao `trainerbattle`) e",
           "@ tambem quem RE-FALA com um treinador ja vencido. Sem ele o objeto do",
           "@ JOGADOR fica congelado pelo `lock` que o proprio molde poe, porque so",
           "@ `ScrCmd_release` chama `UnfreezeObjectEvents`; o `end` sozinho apenas",
           "@ solta `sLockFieldControls`. Era esta a trava dos 127 blocos de 23/08.",
           "@",
           "@ Bloco de PLACA (rótulo *_bgN) é outro molde: placa não tem objeto",
           "@ selecionado, então `trainerbattle_single` bate no assert de",
           "@ src/battle_setup.c:1258 e dá tela azul. Placa usa `lock` +",
           "@ `goto_if_defeated` + `msgbox` + `setvar VAR_LAST_TALKED, LOCALID_PLAYER`",
           "@ + `trainerbattle_no_intro`, que não chama `SetTrainerFacingDirection`.",
           ""]
    # Cadeias compartilhadas por classe, uma vez cada, no topo do arquivo.
    usadas = sorted({usados[num[l["chave"]][2]]["classe"] for l in aceitas})
    out.append("@ ---- fala padrao por classe (ver TEXTO_CLASSE no gerador) ----")
    for classe in usadas:
        r_in, r_dep = rotulos_classe(classe)
        intro, depois = TEXTO_CLASSE.get(classe, TEXTO_PADRAO)
        # A tabela guarda quebra de linha DE VERDADE; o `.string` quer a
        # sequencia `\n` de dois caracteres, que e o comando de nova linha do
        # charmap. Escapa aqui, e nao na tabela, para a tabela ficar legivel.
        esc = lambda t: t.replace("\n", "\\n")
        out += ["%s:" % r_in, '\t.string "%s$"' % esc(intro), "",
                "%s:" % r_dep, '\t.string "%s$"' % esc(depois), ""]
    por_mapa = collections.defaultdict(list)
    for l in aceitas:
        por_mapa[l["mapa"]].append(l)
    for mapa in sorted(por_mapa):
        out.append("@ ---- %s ----" % mapa)
        for l in sorted(por_mapa[mapa], key=lambda z: z["chave"]):
            r = l["rotulo"]
            nid, const, fid = num[l["chave"]]
            r_in, r_dep = rotulos_classe(usados[fid]["classe"])
            out.append("%s::" % r)
            # PORTAO DE "JA VENCI" para o molde que NAO o tem por dentro.
            # Medido no emulador em 22/08/2026 pelo T147.8, que nasceu VERMELHO:
            # `trainerbattle_earlyrival` cai em
            # `EventScript_DoNoIntroTrainerBattle`, que vai DIRETO para o
            # `dotrainerbattle` sem passar pelo `specialvar GetTrainerFlag` que
            # o `EventScript_TryDoNormalTrainerBattle` tem na linha 16. Isso e
            # do motor vanilla e esta certo LA: no FireRed esse molde so e
            # alcancado depois de o treinador AVISTAR o jogador, e a flag ja
            # foi conferida antes. Aqui o objeto e falado, nao avista.
            # O molde `nointro` tinha o mesmo problema e saiu de cena em
            # 23/08/2026: ele virou `trainerbattle_single` com fala de abertura
            # padrao por classe, que e o idioma vanilla e resolve as duas
            # coisas de uma vez (flag por dentro e soltura no fim).
            #
            # PLACA (bg_event) é o segundo portão, aberto em 06/09/2026: o
            # script de uma placa NÃO tem objeto selecionado.
            # `ProcessPlayerFieldInput` zera `gSelectedObjectEvent`
            # (src/field_control_avatar.c:169) e só o caminho de OBJETO o
            # reatribui (linha 420); a placa cai em
            # `GetInteractedBackgroundEventScript`, que não mexe nele. Com
            # isso o `special SetTrainerFacingDirection` que
            # `EventScript_TryDoNormalTrainerBattle` chama bate no assert de
            # src/battle_setup.c:1258 ("trainer script that needs to be used
            # from an object event was called from player") e o cartucho para
            # na tela azul. Placa então usa o caminho SEM intro
            # (`trainerbattle_no_intro` -> `EventScript_DoNoIntroTrainerBattle`,
            # que não toca no special), com o texto de abertura por `msgbox` e
            # o `lock` explícito, porque esse molde também não tranca sozinho.
            e_placa = l.get("tipo") == "placa"
            if e_placa and l["molde"] == "double":
                raise SystemExit(
                    "placa com batalha DUPLA (%s): não há molde sem intro para "
                    "dupla, e o molde com intro trava no assert de "
                    "SetTrainerFacingDirection. Decida o desenho antes de "
                    "gravar." % l["chave"])
            if l["molde"] == "rival":
                out.append("\tlock")
                out.append("\tfaceplayer")
                out.append("\tgoto_if_set TRAINER_FLAGS_START + %s, %s_Fim"
                           % (const, r))
                out.append("\ttrainerbattle_earlyrival %s, 0, %s_Derrota, "
                           "%s_Vitoria" % (const, r, r))
            elif e_placa:
                r_abre = r_in if l["molde"] == "nointro" else "%s_Intro" % r
                out.append("\tlock")
                out.append("\tgoto_if_defeated %s, %s_Depois" % (const, r))
                out.append("\tmsgbox %s, MSGBOX_DEFAULT" % r_abre)
                # `EventScript_DoNoIntroTrainerBattle` faz `applymovement
                # VAR_LAST_TALKED, Movement_RevealTrainer` sem perguntar, e
                # numa placa `gSpecialVar_LastTalked` vale LOCALID_NONE (0),
                # que não é local id de objeto nenhum: `GetObjectEventIdByLocalId`
                # devolve OBJECT_EVENTS_COUNT e o `applymovement` escreve UM
                # elemento depois do fim de `gObjectEvents`. Apontar para o
                # objeto do JOGADOR resolve sem efeito visível, porque
                # `reveal_trainer` em objeto que não é BURIED nem disfarce é
                # no-op (src/event_object_movement.c:8769). É o mesmo remendo
                # que o FireRed usa em `Route24_EventScript_BattleRocket`, só
                # que lá existe NPC para apontar.
                out.append("\tsetvar VAR_LAST_TALKED, LOCALID_PLAYER")
                out.append("\ttrainerbattle_no_intro %s, %s_Derrota"
                           % (const, r))
                out.append("%s_Depois:" % r)
            elif l["molde"] == "double":
                out.append("\ttrainerbattle_double %s, %s_Intro, %s_Derrota, "
                           "%s_Poucos" % (const, r, r, r))
            elif l["molde"] == "nointro":
                out.append("\ttrainerbattle_single %s, %s, %s_Derrota"
                           % (const, r_in, r))
            else:
                out.append("\ttrainerbattle_single %s, %s_Intro, %s_Derrota"
                           % (const, r, r))
            out.append("\tmsgbox %s, MSGBOX_AUTOCLOSE" % r_dep)
            out.append("\trelease")
            out.append("\tend")
            out.append("")
            if l["molde"] == "rival":
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
        open(INC, "w").write(corpo_inc(aceitas, usados, num))
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
        novo = substitui(t, P_INI, P_FIM,
                         bloco_party(usados, num, times_preservados(t)))
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

    aceitas, usados, recusa, novas, extra, gin, motivos_linha = plano()
    caso("o plano aceita mais de 240 linhas", len(aceitas) > 240)
    caso("nenhum treinador aceito passa de 6 Pokemon",
         all(len(u["time"]) <= 6 for u in usados.values()))
    num = numera(aceitas, usados)
    caso("todo id fica na faixa 3000-3399",
         all(ID_BASE <= v[0] < ID_TETO for v in num.values()))
    caso("as constantes de id nao repetem",
         len({v[1] for v in num.values()}) == len(num))
    # UM ID POR OBJETO, com o defeito de 23/08/2026 medido dos dois lados.
    caso("todo objeto que abre batalha tem id proprio",
         len({v[0] for v in num.values()}) == len(aceitas) == len(num))
    caso("e ha treinador da fonte servindo a MAIS DE UM objeto (senao o caso "
         "acima e vazio)",
         max(collections.Counter(v[2] for v in num.values()).values()) > 1)
    # APPEND-ONLY, com mutacao plantada. O lado velho e o header de verdade;
    # a mutacao TIRA dele o menor id, que e exatamente a forma do defeito de
    # 23/08/2026 (um treinador novo com id de fonte pequeno).
    por_obj, por_fonte = ids_gravados()
    velho = {c: num[c][0] for c in num}
    caso("o header ja tem de-para gravado (senao o caso abaixo e vazio)",
         len(por_obj) + len(por_fonte) > 100)
    n_id = numera(aceitas, usados, (por_obj, por_fonte))
    caso("com o header inteiro, NENHUM id se move",
         all(n_id[c][0] == velho[c] for c in velho))
    base = {c: v[0] for c, v in n_id.items()}
    sem_um = ({c: i for c, i in base.items() if i != min(base.values())}, {})
    n2 = numera(aceitas, usados, sem_um)
    caso("tirar o menor do lado velho NAO empurra os outros",
         all(n2[c][0] == base[c] for c in sem_um[0]))
    caso("e o que voltou entra DEPOIS do maior que existia",
         max(n2[c][0] for c in n2 if c not in sem_um[0]) > max(sem_um[0].values()))
    # PAR NEGATIVO: a regra velha (ID_BASE + posicao na ordem da fonte)
    # move sim, e por isso o caso acima nao e vacuo.
    antiga = {f: ID_BASE + i for i, f in enumerate(sorted(usados))}
    caso("a regra velha MOVERIA ids (o caso acima nao e vacuo)",
         any(antiga[v[2]] != v[0] for v in num.values()))
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
    # A ORDEM VIRA GUARDA. `--aplicar` sozinho nao pode mais encostar no time
    # de nenhum chefe da Fase F; o PAR NEGATIVO abaixo roda o mesmo gerador com
    # a preservacao desligada (que e o comportamento de ate 23/08/2026) e exige
    # que ele estrague, senao o caso de cima seria vacuo.
    import guarda_party as GP  # noqa: E402  (mesma pasta, sem custo no import)
    t_real = open(PARTY, encoding="utf-8").read()
    chefes = chefes_da_fase_f()
    # so os chefes que moram DENTRO do bloco de Galar; os outros 198 estao fora
    # do alcance deste gerador e ficariam iguais mesmo com o defeito ligado,
    # o que faria o par negativo mentir.
    dentro = set(re.findall(r"(?m)^=== (\S+) ===[ \t]*$",
                            t_real[t_real.find(P_INI):t_real.find(P_FIM)]))
    # `GP.blocos` cola o marcador de fim no ULTIMO bloco do arquivo, e o ultimo
    # muda de dono quando um id novo entra em append. Sem tirar o marcador, o
    # caso acusaria diferenca onde nao ha nenhuma.
    def limpo(d):
        return {k: "\n".join(ln for ln in v.split("\n") if P_FIM not in ln
                             ).rstrip() for k, v in d.items()}

    antes = {k: v for k, v in limpo(GP.blocos(t_real)).items()
             if k in chefes and k in dentro}
    com = limpo(GP.blocos(substitui(
        t_real, P_INI, P_FIM,
        bloco_party(usados, num, times_preservados(t_real)))))
    sem = limpo(GP.blocos(substitui(t_real, P_INI, P_FIM,
                                    bloco_party(usados, num, {}))))
    caso("ha chefe da Fase F dentro do bloco de Galar (senao o caso e vazio)",
         len(antes) > 30)
    caso("--aplicar nao muda um byte de nenhum chefe da Fase F",
         all(com.get(k) == v for k, v in antes.items()))
    caso("sem a preservacao ele estragaria (par negativo)",
         sum(1 for k, v in antes.items() if sem.get(k) != v) == len(antes))
    caso("e rodar duas vezes da a mesma coisa (idempotente)",
         substitui(t_real, P_INI, P_FIM,
                   bloco_party(usados, num, times_preservados(
                       substitui(t_real, P_INI, P_FIM,
                                 bloco_party(usados, num,
                                             times_preservados(t_real))))))
         == substitui(t_real, P_INI, P_FIM,
                      bloco_party(usados, num, times_preservados(t_real))))
    mudou, rec = aplica(aceitas, usados, num, gravar=False)
    caso("a aplicacao seca nao recusa mais de 5%% dos objetos",
         len(rec) <= 0.05 * len(aceitas))
    print("\n%s" % ("demo verde" if ok else "DEMO REPROVOU"))
    return 0 if ok else 1


# Motivo que nao muda sozinho. Mesma lei do bloco c6 em cenas_galar.py.
MOTIVO_TERMINAL_TRN = (
    "objeto nao esta no mapa (descarte da condutora",
    "nao da para afirmar qual batalha",
    "id de treinador",
    "time da fonte ilegivel",
    "texto recusado",
)


def devolve_para_fila(motivos_linha, gravar):
    """Escreve na fila o motivo MEDIDO de cada linha de treinador recusada."""
    fila = "%s/dev_scripts/fila_galar.json" % RAIZ
    doc = json.load(open(fila))
    n, quadro = 0, collections.Counter()
    for l in doc["linhas"]:
        if l["status"] != "pendente":
            continue
        m = motivos_linha.get(l["chave"])
        if not m:
            continue
        st = ("descartada" if any(t in m for t in MOTIVO_TERMINAL_TRN)
              else "adiada")
        novo = st, ("balde d, lote C da onda 1, 06/09/2026: " + m)
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
        quadro[st] += 1
    if gravar and n:
        with open(fila, "w") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return n, quadro


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--fila", action="store_true",
                    help="devolve o motivo medido de cada linha recusada para "
                         "dev_scripts/fila_galar.json (com --aplicar, grava)")
    a = ap.parse_args()
    if a.demo:
        return demo()
    rom = open(FALA.ROM_FONTE, "rb").read()
    st, quantos, total = stride_medido(rom)
    print("stride medido de gTrainers: %d B (%d de %d deltas)"
          % (st, quantos, total))
    aceitas, usados, recusa, novas, extra, gin, motivos_linha = plano()
    num = numera(aceitas, usados)
    ids = [v[0] for v in num.values()]
    print("batalhas portadas: %d em %d mapas; treinadores novos: %d (ids %d-%d)"
          % (len(aceitas), len({l["mapa"] for l in aceitas}), len(num),
             min(ids), max(ids)))
    gemeos = collections.Counter(v[2] for v in num.values())
    print("objetos que dividiam id de treinador com outro objeto: %d em %d "
          "treinadores da fonte (cada um ganhou id proprio e time copiado)"
          % (sum(n for n in gemeos.values() if n > 1),
             sum(1 for n in gemeos.values() if n > 1)))
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
    if a.fila:
        # `--fila` GRAVA a fila e NAO chama `aplica`, de proposito. O
        # `--aplicar` deste arquivo reescreve `src/data/trainers.party`
        # inteiro, inclusive os chefes, e tem ordem obrigatoria com o
        # `fase_f_chefes.py` (ver a ARMADILHA DE ORDEM no
        # PLANO-CONTEUDO-GALAR.md). Devolver motivo para a fila nao pode
        # arrastar isso junto.
        n, quadro = devolve_para_fila(motivos_linha, True)
        print("fila: %d linhas ganharam motivo medido (gravado)" % n)
        for st, c in sorted(quadro.items()):
            print("   %-12s %d" % (st, c))
        return 0
    mudou, rec = aplica(aceitas, usados, num, gravar=a.aplicar)
    escreve_classes_md(novas, usados, gravar=a.aplicar)
    print("\nmudaria: %s | recusas de colocacao: %d" % (dict(mudou), len(rec)))
    for r in rec[:10]:
        print("   %s: %s" % (r["chave"], r["motivo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
