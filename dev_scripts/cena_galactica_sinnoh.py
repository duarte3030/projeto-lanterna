#!/usr/bin/env python3
"""Porta as cenas da Equipe Galáctica que ainda faltavam na espinha de Sinnoh.

Uso:
    python3 dev_scripts/cena_galactica_sinnoh.py           # só relata
    python3 dev_scripts/cena_galactica_sinnoh.py --aplica
    python3 dev_scripts/cena_galactica_sinnoh.py --demo

## O buraco que este arquivo fecha

`importa_npcs_sinnoh.py` recusa, de propósito, todo objeto do Platinum que tenha
`hidden_flag`: quem nasce escondido é gente de história, e trazer isso sem a cena
que a apaga põe um bloqueio permanente no caminho do jogador (a armadilha das
pedras de Strength, regra do PRD). O preço dessa recusa é que **doze treinadores
com constante, time e fala já prontos nesta ROM não estão em mapa nenhum**:
medido em 12/08/2026, são os únicos doze `TRAINER_*` escondidos por `FLAG_HIDE_*`
que passam em constante, bloco de `trainers.party` e tradução de texto.

Este script traz esses doze (mais um grunt mudo que é da mesma cena) **com a cena
junto**: cada um entra com uma flag no campo `flag` do `object_event`, e essa
mesma flag é ACESA por um `MAP_SCRIPT_ON_TRANSITION` que lê o marco da história.
Ou seja, o bloqueio que a cena cria é o mesmo que ela desfaz, e não sobra parede.

## As dez cenas, e o marco de cada uma

As cinco primeiras saem de molde (`CENAS` e `HORARIO`): objeto, batalha e texto
da fonte, sem controle de fluxo próprio. As cinco de baixo são `ROTEIRO`: têm
menu, ramo por inicial do jogador ou cutscene, e por isso o script é escrito à
mão, com o TEXTO ainda vindo da fonte.

| cena | quem entra | fica escondido quando |
|---|---|---|
| Mt. Coronet ocupado | 7 grunts + 1 perdido, em 5 andares | Cyrus cai no Spear Pillar |
| QG de Veilstone | Scientist Fredrick (1F) e Darrius (2F) | Saturn cai na sala de controle |
| Prédio de Eterna | Scientist Travon (3F) | Jupiter cai no 4F |
| Rota 210 sul | Jogger Wyatt | não é de manhã |
| Rota 212 sul | Policeman Danny | não é de noite |
| Celestic Town | grunt da bomba, o ancião e a Cynthia | o grunt cai |
| Rota 218 | o show: guitarrista, 2 Clefairy, 2 Pikachu, pescador | o grunt de Celestic cai |
| Lago Verity | Comandante Mars | ela cai (e leva os 4 grunts junto) |
| Lago Acuity | Jupiter e o rival | a cena roda até o fim |
| Canalave | o rival, com 3 times, um por inicial do jogador | ele cai |

As duas últimas não são história: no Platinum o mesmo NPC tem uma versão que luta
e uma que não, trocadas por `GetTimeOfDay`. Aqui a versão que luta entra atrás de
uma flag que o `ON_TRANSITION` apaga só na faixa de hora certa. A polaridade é
deliberada: **acende primeiro, apaga só no ramo bom**, para que qualquer falha de
leitura de hora deixe o treinador AUSENTE, nunca plantado no meio da rota.

## Por que ON_TRANSITION e não coord_event, var ou special novo

`RunOnTransitionMapScript()` roda ANTES de `InitMap()`, que é quem faz nascer os
`object_events` (`src/overworld.c`), então a flag lida ali já vale para o objeto
daquele mesmo carregamento. Precedente no repo: `EternaCity_OnTransition`, que
já traduz "a Jupiter caiu" em `FLAG_GALACTICA_ETERNA`. Custo: zero var, zero
special novo, zero linha de C.

## Onde cada objeto é posto (medido, não chutado)

- **Mt. Coronet**: os cinco andares têm geometria CONVERTIDA da grade 2D do
  Platinum, então a coordenada da fonte vale tal e qual. Conferido tile a tile
  com `valida_mapas_sinnoh.colisao`: os onze caem em chão andável sem desvio.
- **QG, prédio de Eterna, rotas**: layout EMPRESTADO ou coordenada global da
  matriz. Ali a coordenada da fonte não significa nada, então o alvo é o tile
  livre mais perto do centro de massa dos objetos que o mapa já tem, com os
  warps e a vizinhança deles proibidos: NPC em cima de porta tranca o mapa.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importa_npcs_sinnoh as I  # noqa: E402
import texto_sinnoh as T  # noqa: E402
import treinadores_masmorra_sinnoh as M  # noqa: E402
import valida_mapas_sinnoh as V  # noqa: E402

PLAT = T.PLAT
APLICA = "--aplica" in sys.argv

# Marca gravada em cada objeto que este script cria. O mapjson ignora campo que
# não conhece, então ela é inerte na ROM e serve para uma coisa só: rodar
# --aplica duas vezes não pode duplicar ninguém.
MARCA = "cena_galactica_sinnoh"

# Cena de história: a flag esconde o elenco depois que o marco cai.
# `gatilho` é a constante de treinador cuja flag de derrotado o motor já grava.
CENAS = [
    dict(
        chave="mt_coronet",
        titulo="Mt. Coronet ocupado pela Equipe Galactica",
        flag="FLAG_GALACTICA_MT_CORONET",
        gatilho="TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR",
        hidden_flag="FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS",
        marco="derrotar o Cyrus no Spear Pillar",
        mapas=["MtCoronet1FTunnelRoom", "MtCoronet3F",
               "MtCoronet4FRooms1And2", "MtCoronet5F", "MtCoronet6F"],
        coordenada="direta",
        mudos=True,
    ),
    dict(
        chave="qg_veilstone",
        titulo="QG da Galactica em Veilstone: os dois cientistas",
        flag="FLAG_GALACTICA_QG_TOMADO",
        gatilho="TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ",
        hidden_flag="FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC",
        marco="derrotar o Saturn na sala de controle do QG",
        mapas=["GalacticHQ_1F", "GalacticHQ_2F"],
        coordenada="livre",
        mudos=False,
    ),
    dict(
        chave="eterna",
        titulo="Predio da Galactica em Eterna: o cientista do 3F",
        flag="FLAG_GALACTICA_ETERNA",   # já existe; nenhuma flag nova aqui
        gatilho="TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING",
        hidden_flag="FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS",
        marco="derrotar a Jupiter no 4F do predio de Eterna",
        mapas=["TeamGalacticEternaBuilding_3F"],
        coordenada="livre",
        mudos=False,
    ),
]

# Troca por hora do dia. `hora` é a faixa em que o treinador APARECE.
HORARIO = [
    dict(
        chave="route210_wyatt",
        titulo="Rota 210 sul: o Jogger Wyatt so corre de manha",
        mapa="Route210_South",
        trainer="TRAINER_JOGGER_WYATT",
        flag="FLAG_SINNOH_ROUTE210_WYATT_ESCONDIDO",
        hidden_flag="FLAG_HIDE_ROUTE_210_SOUTH_JOGGER_WYATT",
        hora=[(0, "TIME_MORNING")],
        marco="entrar na Rota 210 sul de manha",
    ),
    dict(
        chave="route212_danny",
        titulo="Rota 212 sul: o Policeman Danny so patrulha de noite",
        mapa="Route212_South",
        trainer="TRAINER_POLICEMAN_DANNY",
        flag="FLAG_SINNOH_ROUTE212_DANNY_ESCONDIDO",
        hidden_flag="FLAG_HIDE_ROUTE_212_SOUTH_POLICEMAN_DANNY",
        hora=[(3, "TIME_NIGHT")],
        marco="entrar na Rota 212 sul de noite",
    ),
]


# ==========================================================================
# ROTEIRO: as quatro cenas que fecham a espinha (12/08/2026)
#
# Diferente de CENAS e HORARIO, aqui o script NAO e gerado por molde: cada uma
# tem controle de fluxo proprio (menu de sim/nao, ramo por inicial do jogador,
# cutscene com movimento), e gerar isso a partir de tabela e onde nasce bug. O
# que continua vindo da FONTE, e nunca do meu teclado, e o TEXTO: cada `{TXT_x}`
# do corpo e trocado pelo rotulo de um `.string` tirado de `res/text/<banco>.json`
# por `texto_sinnoh.resolve`. Texto que exija buffer que este gerador nao emite
# reprova a cena inteira, em vez de chegar ao jogador com `{STR_VAR}` vazio.
#
# `sprite` e obrigatorio em quem esta na lista NOMES_PROPRIOS do importador
# (Mars, Jupiter, Cynthia, Barry): eles nao tem sprite proprio nesta ROM e a
# tabela TROCA_SPRITE nao os cobre de proposito. O emprestimo vai declarado
# aqui, um a um, e sai no relatorio.
# ==========================================================================

# Substituicao unica de texto: `{STRVAR_1 3, 0, 0}` do Platinum e o buffer do
# nome do rival, que esta ROM nao tem. O rival de Sinnoh se chama CEDRIC no
# bloco de `trainers.party` (veio assim do proprio pokeplatinum), entao o nome
# entra cravado. `{STRVAR_1 3, 1, 0}` e o nome do jogador, e esse o charmap
# resolve sozinho com {PLAYER}.
RIVAL = "CEDRIC"

ROTEIRO = [
    dict(
        chave="celestic",
        titulo="Celestic Town: a bomba da Galactica, o anciao e a Cynthia",
        marco="derrotar o grunt da bomba em frente as ruinas",
        mapa="CelesticTown",
        banco="celestic_town",
        objetos=[
            dict(fonte_id="LOCALID_GRUNT_M",
                 local_id="LOCALID_CELESTIC_TOWN_GALACTIC_GRUNT",
                 script="CelesticTown_EventScript_GalacticGrunt",
                 flag="FLAG_GALACTICA_CELESTIC",
                 sprite="OBJ_EVENT_GFX_MAGMA_MEMBER_M",
                 mov="MOVEMENT_TYPE_FACE_DOWN"),
            dict(fonte_id="LOCALID_ELDER",
                 local_id="LOCALID_CELESTIC_TOWN_ELDER",
                 script="CelesticTown_EventScript_Elder",
                 flag="0", sprite="OBJ_EVENT_GFX_EXPERT_F",
                 mov="MOVEMENT_TYPE_FACE_UP"),
            dict(fonte_id="LOCALID_CYNTHIA",
                 local_id="LOCALID_CELESTIC_TOWN_CYNTHIA",
                 script="CelesticTown_EventScript_Cynthia",
                 flag="FLAG_CELESTIC_CYNTHIA_ESCONDIDA",
                 sprite="OBJ_EVENT_GFX_BEAUTY",
                 mov="MOVEMENT_TYPE_FACE_LEFT"),
        ],
        textos={
            "MessWithMe": "CelesticTown_Text_WillYouMessWithMe",
            "VerySmart": "CelesticTown_Text_VerySmart",
            "YouDare": "CelesticTown_Text_YouDareOpposeUs",
            "TooMuch": "CelesticTown_Text_TooMuchToHandle",
            "OldCharm": "CelesticTown_Text_ThatOldCharm",
            "LookAround": "CelesticTown_Text_LookAroundRuins",
            "ExamineRuins": "CelesticTown_Text_ExamineRuins",
            "OddSpaceman": "CelesticTown_Text_OddSpaceman",
            "AllRight": "CelesticTown_Text_WasEverythingAllRight",
            "Harmless": "CelesticTown_Text_ThoughtGalacticWasHarmless",
            "Library": "CelesticTown_Text_LibraryInCanalave",
        },
        corpo="""
@ ponytail: UMA flag para a cena inteira. FLAG_GALACTICA_CELESTIC esconde o
@ grunt E os seis do show da Rota 218, e a mesma derrota APAGA a flag que
@ segurava a Cynthia. No Platinum quem libera a Rota 218 e a fala da Cynthia,
@ um passo depois; aqui e a derrota do grunt, um passo antes. O encurtamento e
@ deliberado: economiza uma flag e nao muda a ordem em que o jogador ve as
@ coisas, porque a Cynthia nasce no mesmo instante.
CelesticTown_EventScript_GalacticGrunt::
\tlock
\tfaceplayer
\tmsgbox {TXT_MessWithMe}, MSGBOX_YESNO
\tgoto_if_eq VAR_RESULT, NO, CelesticTown_EventScript_GruntVerySmart
\ttrainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_CELESTIC_TOWN, {TXT_YouDare}, {TXT_TooMuch}, CelesticTown_EventScript_GruntBeaten
\tend

CelesticTown_EventScript_GruntVerySmart::
\tmsgbox {TXT_VerySmart}, MSGBOX_DEFAULT
\trelease
\tend

CelesticTown_EventScript_GruntBeaten::
\tsetflag FLAG_GALACTICA_CELESTIC
\tclearflag FLAG_CELESTIC_CYNTHIA_ESCONDIDA
\tremoveobject LOCALID_CELESTIC_TOWN_GALACTIC_GRUNT
\taddobject LOCALID_CELESTIC_TOWN_CYNTHIA
\trelease
\tend

CelesticTown_EventScript_Elder::
\tlock
\tfaceplayer
\tgoto_if_set FLAG_GALACTICA_CELESTIC, CelesticTown_EventScript_ElderThanks
\tmsgbox {TXT_OddSpaceman}, MSGBOX_DEFAULT
\trelease
\tend

CelesticTown_EventScript_ElderThanks::
\tmsgbox {TXT_OldCharm}, MSGBOX_DEFAULT
\tmsgbox {TXT_LookAround}, MSGBOX_DEFAULT
\tmsgbox {TXT_ExamineRuins}, MSGBOX_DEFAULT
\trelease
\tend

CelesticTown_EventScript_Cynthia::
\tlock
\tfaceplayer
\tmsgbox {TXT_AllRight}, MSGBOX_DEFAULT
\tmsgbox {TXT_Harmless}, MSGBOX_DEFAULT
\tmsgbox {TXT_Library}, MSGBOX_DEFAULT
\trelease
\tend
""",
    ),
    dict(
        chave="route218",
        titulo="Rota 218: o show que ocupa a estrada ate Celestic acabar",
        marco="a mesma FLAG_GALACTICA_CELESTIC",
        mapa="Route218",
        banco="route_218",
        objetos=[
            dict(fonte_id="LOCALID_GUITARIST", local_id="LOCALID_ROUTE218_GUITARIST",
                 script="Route218_EventScript_ShowGuitarist",
                 flag="FLAG_GALACTICA_CELESTIC", sprite="OBJ_EVENT_GFX_MAN_3",
                 mov="MOVEMENT_TYPE_FACE_DOWN"),
            dict(fonte_id="LOCALID_CLEFAIRY_SOUTH", local_id="LOCALID_ROUTE218_CLEFAIRY_SOUTH",
                 script="Route218_EventScript_ShowClefairySouth",
                 flag="FLAG_GALACTICA_CELESTIC", mov="MOVEMENT_TYPE_FACE_DOWN"),
            dict(fonte_id="LOCALID_CLEFAIRY_NORTH", local_id="LOCALID_ROUTE218_CLEFAIRY_NORTH",
                 script="Route218_EventScript_ShowClefairyNorth",
                 flag="FLAG_GALACTICA_CELESTIC", mov="MOVEMENT_TYPE_FACE_DOWN"),
            dict(fonte_id="LOCALID_PIKACHU_SOUTH", local_id="LOCALID_ROUTE218_PIKACHU_SOUTH",
                 script="Route218_EventScript_ShowPikachu",
                 flag="FLAG_GALACTICA_CELESTIC", mov="MOVEMENT_TYPE_FACE_UP"),
            dict(fonte_id="LOCALID_PIKACHU_NORTH", local_id="LOCALID_ROUTE218_PIKACHU_NORTH",
                 script="Route218_EventScript_ShowPikachu",
                 flag="FLAG_GALACTICA_CELESTIC", mov="MOVEMENT_TYPE_FACE_UP"),
            dict(fonte_id="LOCALID_FISHERMAN", local_id="LOCALID_ROUTE218_FISHERMAN",
                 script="Route218_EventScript_ShowFisherman",
                 flag="FLAG_GALACTICA_CELESTIC", mov="MOVEMENT_TYPE_FACE_UP"),
        ],
        textos={
            "Cuter": "Route218_Text_ClefairyCuterNow",
            "Pippiih": "Route218_Text_ClefairyCryPippiih",
            "Pippippiih": "Route218_Text_ClefairyCryPippippiih",
            "PikaCry": "Route218_Text_PikachuCry",
            "Dazzle": "Route218_Text_PikachuDazzle",
        },
        corpo="""
@ ponytail: MEDIDO, e a medida contradiz o Platinum. La estes seis selam uma
@ ponte de um tile e a estrada para Canalave so abre com a Cynthia. Aqui a
@ geometria convertida e mais larga: medido com busca em largura na grade, para
@ selar a estrada seria preciso tapar as colunas 8, 9 E 10 inteiras das linhas 12
@ a 26 (a contraprova do --demo faz exatamente isso e so entao reprova). Seis
@ objetos nao chegam perto disso: eles OCUPAM a estrada sem tranca-la, e ha
@ desvio pelas fileiras 16 a 21. Fechar o vao a mao seria inventar bloqueio, e bloqueio
@ inventado e exatamente o risco que o PRD proibe: some Celestic da rota do
@ jogador e o hack trava. Ficam como cena que se desfaz, e a medida fica escrita.
Route218_EventScript_ShowGuitarist::
\tmsgbox {TXT_Cuter}, MSGBOX_NPC
\tend

Route218_EventScript_ShowFisherman::
\tmsgbox {TXT_Dazzle}, MSGBOX_NPC
\tend

Route218_EventScript_ShowClefairySouth::
\tlock
\tfaceplayer
\tplaymoncry SPECIES_CLEFAIRY, CRY_MODE_NORMAL
\tmsgbox {TXT_Pippiih}, MSGBOX_DEFAULT
\twaitmoncry
\trelease
\tend

Route218_EventScript_ShowClefairyNorth::
\tlock
\tfaceplayer
\tplaymoncry SPECIES_CLEFAIRY, CRY_MODE_NORMAL
\tmsgbox {TXT_Pippippiih}, MSGBOX_DEFAULT
\twaitmoncry
\trelease
\tend

Route218_EventScript_ShowPikachu::
\tlock
\tfaceplayer
\tplaymoncry SPECIES_PIKACHU, CRY_MODE_NORMAL
\tmsgbox {TXT_PikaCry}, MSGBOX_DEFAULT
\twaitmoncry
\trelease
\tend
""",
    ),
    dict(
        chave="lago_verity",
        titulo="Lago Verity: a Comandante Mars, e a Galactica indo embora",
        marco="derrotar a Mars na margem do Lago Verity",
        mapa="LakeVerity",
        banco="lake_verity",
        objetos=[
            dict(fonte_id="LOCALID_MARS", local_id="LOCALID_LAKE_VERITY_MARS",
                 script="LakeVerity_EventScript_Mars",
                 flag="FLAG_GALACTICA_LAGO_VERITY",
                 sprite="OBJ_EVENT_GFX_MAGMA_MEMBER_F",
                 mov="MOVEMENT_TYPE_FACE_DOWN",
                 # A conversao da coordenada GLOBAL da matriz do Platinum cai em
                 # (47,0), o canto do mapa, a 30 tiles dos quatro grunts dela.
                 # Coordenada de exterior de gen 4 e global e nao ha offset que
                 # alinhe (ESTADO.md, secao dos tres exteriores). Entao a Mars vai
                 # ao lado do grunt 1 dela, em (37,32), que e a POSICAO RELATIVA
                 # que a cena precisa: ela e o fundo da fila.
                 xy=(36, 32)),
        ],
        # Os quatro grunts do lago ja existem neste mapa desde a leva de
        # treinadores; o que faltava era eles IREM EMBORA com a Mars. `flag` nao
        # entra na save (a save guarda indice de objeto, nao o campo), entao
        # mexer nele em objeto que ja existe e seguro.
        ajustes=[dict(local_id=f"LOCALID_LAKE_VERITY_TRAINER{n}",
                      campo="flag", valor="FLAG_GALACTICA_LAGO_VERITY")
                 for n in (1, 2, 3, 4)],
        textos={
            "MarsIntro": "LakeVerity_Text_MarsIntro",
            "MarsDefeat": "LakeVerity_Text_MarsDefeat",
            "PullingOut": "LakeVerity_Text_WerePullingOut",
            "AllLakePokemon": "LakeVerity_Text_NowWeveGotAllLakePokemon",
        },
        corpo="""
@ ponytail: a derrota da Mars faz o que o Platinum faz na mesma linha
@ (scripts_lake_verity.s:200 em diante): a Galactica INTEIRA sai do lago e a
@ Jupiter aparece no Lago Acuity. Os quatro grunts que ja estavam neste mapa
@ ganharam FLAG_GALACTICA_LAGO_VERITY no campo `flag`, entao somem com ela; o
@ `removeobject` de cada um e para saírem na hora, sem precisar sair e voltar.
LakeVerity_EventScript_Mars::
\tlock
\tfaceplayer
\tmsgbox {TXT_MarsIntro}, MSGBOX_DEFAULT
\ttrainerbattle_single TRAINER_SINNOH_COMMANDER_MARS_LAKE_VERITY, {TXT_MarsIntro}, {TXT_MarsDefeat}, LakeVerity_EventScript_MarsBeaten
\tend

LakeVerity_EventScript_MarsBeaten::
\tmsgbox {TXT_PullingOut}, MSGBOX_DEFAULT
\tmsgbox {TXT_AllLakePokemon}, MSGBOX_DEFAULT
\tclosemessage
\tfadescreen FADE_TO_BLACK
\tsetflag FLAG_GALACTICA_LAGO_VERITY
\tremoveobject LOCALID_LAKE_VERITY_MARS
\tremoveobject LOCALID_LAKE_VERITY_TRAINER1
\tremoveobject LOCALID_LAKE_VERITY_TRAINER2
\tremoveobject LOCALID_LAKE_VERITY_TRAINER3
\tremoveobject LOCALID_LAKE_VERITY_TRAINER4
\tfadescreen FADE_FROM_BLACK
\trelease
\tend
""",
    ),
    dict(
        chave="lago_acuity",
        titulo="Lago Acuity: a Jupiter derrota o rival, e o rival cresce",
        marco="a Mars cair no Lago Verity",
        mapa="LakeAcuity",
        banco="lake_acuity",
        objetos=[
            dict(fonte_id="LOCALID_JUPITER", local_id="LOCALID_LAKE_ACUITY_JUPITER",
                 script="LakeAcuity_EventScript_Jupiter",
                 flag="FLAG_ESCONDE_LAGO_ACUITY",
                 sprite="OBJ_EVENT_GFX_MAGMA_MEMBER_F",
                 mov="MOVEMENT_TYPE_FACE_DOWN",
                 xy=(22, 31)),
            dict(fonte_id="LOCALID_RIVAL", local_id="LOCALID_LAKE_ACUITY_RIVAL",
                 script="LakeAcuity_EventScript_Jupiter",
                 flag="FLAG_ESCONDE_LAGO_ACUITY",
                 sprite="OBJ_EVENT_GFX_RICH_BOY",
                 mov="MOVEMENT_TYPE_FACE_LEFT",
                 xy=(23, 31)),
        ],
        # (23,30) e o UNICO tile de acesso a boca da caverna em (23,29): medido
        # na grade, as colunas 20 a 26 sao rocha macica nas linhas 26 a 28, e a
        # linha 29 so abre em x=23. Quem for a caverna PISA nele, entao o gatilho
        # da cena mora ali e nao ha caminho que o contorne.
        #
        # ponytail: a versao anterior punha a JUPITER em cima de (23,30), para
        # trancar a caverna como no Platinum. Medido e desfeito: aquele tile e
        # vizinho do warp, ou seja e onde o jogador CAI ao sair da caverna, e o
        # NPC ali o faz sair por cima do boneco. Bloqueio de verdade valeria a
        # feiura; bloqueio que ainda por cima e contornavel pela fileira 31, nao.
        # Os dois ficam na fileira 31, no caminho, e a caverna segue aberta.
        coord_events=[dict(x=23, y=30, script="LakeAcuity_EventScript_Jupiter")],
        textos={
            "NotGettingAway": "LakeAcuity_Text_YoureNotGettingAway",
            "BackToVeilstone": "LakeAcuity_Text_BackToVeilstoneCity",
            "DontWaste": "LakeAcuity_Text_DontWasteYourTime",
            "CouldntDo": "LakeAcuity_Text_ICouldntDoAnything",
            "UxieSuffering": "LakeAcuity_Text_UxieWasSuffering",
            "BeStronger": "LakeAcuity_Text_IHaveToBeStronger",
        },
        on_transition="""
@ ponytail: as duas pontas da janela desta cena, num ON_TRANSITION so, que roda
@ ANTES de InitMap() e por isso ja vale para este carregamento. A ordem importa:
@ acende PRIMEIRO (par nao existe), e so o ramo bom apaga. Enquanto a Mars nao
@ cai, e depois que a cena roda, os dois nao nascem; a janela em que eles existem
@ e exatamente a da cena, e a propria cena a fecha.
LakeAcuity_OnTransition:
\tsetflag FLAG_ESCONDE_LAGO_ACUITY
\tgoto_if_set FLAG_GALACTICA_ACUITY_VISTO, LakeAcuity_EventScript_CenaJaRodou
\tcall_if_defeated TRAINER_SINNOH_COMMANDER_MARS_LAKE_VERITY, LakeAcuity_EventScript_MostraJupiter
\tend

LakeAcuity_EventScript_MostraJupiter::
\tclearflag FLAG_ESCONDE_LAGO_ACUITY
\treturn

LakeAcuity_EventScript_CenaJaRodou::
\tend
""",
        corpo="""
@ ponytail: gatilho DUPLO de proposito, e nao por indecisao. O coord_event de
@ (23,31) da o disparo automatico do original (VAR_TEMP_0 com valor 0: o motor
@ zera os VAR_TEMP_* a cada entrada de mapa, entao ele esta sempre valendo e
@ quem lembra que a cena ja rodou e a FLAG la dentro, tecnica 1 do
@ SINNOH-PADRAO.md). Falar com qualquer um dos dois roda a MESMA cena, e e essa
@ segunda porta que garante que ninguem fica preso: a Jupiter esta em cima do
@ unico tile de acesso a caverna, e jogador que chegue por um caminho que nao
@ pise em (23,31) ainda assim consegue destravar conversando.
@
@ Cortado do original: a camera livre (AddFreeCamera) e os dois ramos de x=14 e
@ x=15, que existem so porque la o coord_event cobre dois tiles. O que a cena
@ diz e faz e o mesmo.
LakeAcuity_EventScript_Jupiter::
\tlockall
\tgoto_if_set FLAG_GALACTICA_ACUITY_VISTO, LakeAcuity_EventScript_CenaAcabou
\tapplymovement LOCALID_LAKE_ACUITY_RIVAL, LakeAcuity_Movement_RivalOlhaJupiter
\twaitmovement 0
\tmsgbox {TXT_NotGettingAway}, MSGBOX_DEFAULT
\tmsgbox {TXT_BackToVeilstone}, MSGBOX_DEFAULT
\tmsgbox {TXT_DontWaste}, MSGBOX_DEFAULT
\tclosemessage
\tremoveobject LOCALID_LAKE_ACUITY_JUPITER
\tapplymovement LOCALID_LAKE_ACUITY_RIVAL, LakeAcuity_Movement_RivalOlhaJogador
\twaitmovement 0
\tmsgbox {TXT_CouldntDo}, MSGBOX_DEFAULT
\tmsgbox {TXT_UxieSuffering}, MSGBOX_DEFAULT
\tmsgbox {TXT_BeStronger}, MSGBOX_DEFAULT
\tclosemessage
\tremoveobject LOCALID_LAKE_ACUITY_RIVAL
\tsetflag FLAG_GALACTICA_ACUITY_VISTO
\tsetflag FLAG_ESCONDE_LAGO_ACUITY
\treleaseall
\tend

LakeAcuity_EventScript_CenaAcabou::
\treleaseall
\tend

LakeAcuity_Movement_RivalOlhaJupiter:
\tface_left
\tstep_end

LakeAcuity_Movement_RivalOlhaJogador:
\tface_down
\tstep_end
""",
    ),
    dict(
        chave="canalave_rival",
        titulo="Canalave: o rival cobra a revanche antes do ginasio do Byron",
        marco="derrotar o rival, qualquer que seja o inicial do jogador",
        mapa="CanalaveCity",
        banco="canalave_city",
        objetos=[
            dict(fonte_id="LOCALID_RIVAL_BRIDGE", local_id="LOCALID_CANALAVE_CITY_RIVAL",
                 script="CanalaveCity_EventScript_Rival",
                 flag="FLAG_GALACTICA_CANALAVE_RIVAL",
                 sprite="OBJ_EVENT_GFX_RICH_BOY",
                 # ponytail: SEM raio de visao, ao contrario do rival de Johto.
                 # O script dele nao e um `trainerbattle_single` pelado: tem
                 # `lock`, `faceplayer` e um `switch` por inicial ANTES da
                 # batalha, e a aproximacao automatica do motor ja fez essas duas
                 # coisas. Rodar o mesmo corpo pelos dois caminhos e pedir bug de
                 # travamento num script que nao da para testar sem build. Ele
                 # nao esta em gargalo nenhum, entao raio de visao nao compra
                 # nada aqui: falar com ele basta.
                 mov="MOVEMENT_TYPE_FACE_RIGHT"),
        ],
        textos={
            "CheckReady": "CanalaveCity_Text_CheckIfYoureReady",
            "IronIsland": "CanalaveCity_Text_TrainAtIronIsland",
        },
        on_transition="""
@ ponytail: tres `call_if_defeated` e nao um, porque o rival tem TRES ids, um
@ por inicial do jogador, e so um deles chega a ser lutado. Quem ja venceu o seu
@ nao ve o rival de novo ao reentrar no mapa.
CanalaveCity_OnTransition:
\tcall_if_defeated TRAINER_SINNOH_RIVAL_CANALAVE_CITY_TURTWIG, CanalaveCity_EventScript_EsconderRival
\tcall_if_defeated TRAINER_SINNOH_RIVAL_CANALAVE_CITY_CHIMCHAR, CanalaveCity_EventScript_EsconderRival
\tcall_if_defeated TRAINER_SINNOH_RIVAL_CANALAVE_CITY_PIPLUP, CanalaveCity_EventScript_EsconderRival
\tend

CanalaveCity_EventScript_EsconderRival::
\tsetflag FLAG_GALACTICA_CANALAVE_RIVAL
\treturn
""",
        corpo="""
@ ponytail: TRES ids, e nao um, porque os tres ramos EXISTEM nesta ROM. Medido
@ antes de escrever: data/maps/SandgemTown_RowanLab/scripts.inc escreve
@ VAR_STARTER_MON com 0, 1 e 2 (grama, fogo, agua) desde 05/08/2026, entao o
@ triangulo de tipos do rival e verdade aqui. O comentario do rival de JOHTO
@ (data/maps/CherrygroveCity/scripts.inc) diz o contrario e esta VELHO: ele foi
@ escrito quando o laboratorio ainda nao escrevia a var, e aponta para
@ SandgemTown_House1, que nao e o laboratorio.
@
@ O nome de cada constante e o inicial DO JOGADOR, nao o do rival: no Platinum o
@ ramo TURTWIG e o que roda quando o jogador tem Turtwig, e o ace daquele time e
@ Infernape (fogo bate grama). Conferido bloco a bloco em trainers.party.
@
@ Gatilho por RAIO DE VISAO (tecnica 3 do SINNOH-PADRAO.md), precedente do rival
@ de Johto: o motor faz exclamacao, aproximacao e memoria de "ja perdeu" de
@ graca. O `switch` roda DEPOIS da aproximacao e antes da batalha.
CanalaveCity_EventScript_Rival::
\tlock
\tfaceplayer
\tmsgbox {TXT_CheckReady}, MSGBOX_DEFAULT
\tswitch VAR_STARTER_MON
\tcase 0, CanalaveCity_EventScript_RivalTurtwig
\tcase 1, CanalaveCity_EventScript_RivalChimchar
\tgoto CanalaveCity_EventScript_RivalPiplup
\tend

CanalaveCity_EventScript_RivalTurtwig::
\ttrainerbattle_single TRAINER_SINNOH_RIVAL_CANALAVE_CITY_TURTWIG, {TXT_CheckReady}, {TXT_IronIsland}, CanalaveCity_EventScript_RivalBeaten
\tend

CanalaveCity_EventScript_RivalChimchar::
\ttrainerbattle_single TRAINER_SINNOH_RIVAL_CANALAVE_CITY_CHIMCHAR, {TXT_CheckReady}, {TXT_IronIsland}, CanalaveCity_EventScript_RivalBeaten
\tend

CanalaveCity_EventScript_RivalPiplup::
\ttrainerbattle_single TRAINER_SINNOH_RIVAL_CANALAVE_CITY_PIPLUP, {TXT_CheckReady}, {TXT_IronIsland}, CanalaveCity_EventScript_RivalBeaten
\tend

CanalaveCity_EventScript_RivalBeaten::
\tmsgbox {TXT_IronIsland}, MSGBOX_DEFAULT
\tsetflag FLAG_GALACTICA_CANALAVE_RIVAL
\tremoveobject LOCALID_CANALAVE_CITY_RIVAL
\trelease
\tend
""",
    ),
]


# --------------------------------------------------------------------------
# leitura da fonte

def eventos_da_fonte(meu):
    """(objetos do mapa da fonte, header, largura, altura) ou None."""
    for m, header, arq in T.casados():
        if m != meu:
            continue
        p = os.path.join(PLAT, "res/field/events", arq + ".json")
        if not os.path.exists(p):
            return None
        return json.load(open(p, encoding="utf-8")), header
    return None


def layouts():
    return {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"]}


def proibidos_do_mapa(d):
    """Tiles onde NPC não pode ficar: warp e a vizinhança dele.

    NPC em cima de porta é warp morto, e NPC colado na porta rouba o tile de
    onde o jogador cai ao entrar. Os dois já custaram mapa neste repo (os dois
    guardas de insígnia da Liga, ver ESTADO.md).
    """
    fora = set()
    for w in d.get("warp_events") or []:
        x, y = w.get("x"), w.get("y")
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                fora.add((x + dx, y + dy))
    return fora


def ocupados_do_mapa(d):
    return {(o.get("x"), o.get("y")) for o in (d.get("object_events") or [])}


def alvo_livre(lays, lid, ancora, ocupados, proibidos, raio=12):
    """Tile andável, desocupado e longe de porta, mais perto de `ancora`."""
    ax, ay = ancora
    for r in range(0, raio + 1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if r and max(abs(dx), abs(dy)) != r:
                    continue
                p = (ax + dx, ay + dy)
                if p in ocupados or p in proibidos:
                    continue
                if V.colisao(lays, lid, *p) == 0:
                    return p
    return None


def centro_de_massa(d):
    oe = d.get("object_events") or []
    if not oe:
        return None
    return (sum(o["x"] for o in oe) // len(oe), sum(o["y"] for o in oe) // len(oe))


# --------------------------------------------------------------------------
# plano

def plano_das_cenas():
    """[(cena, mapa, [(objeto novo, trecho de scripts.inc)]), ...] + recusas."""
    lays = layouts()
    sprites = V.sprites_utilizaveis()
    consts = M.constantes_de_treinador()
    com_time = M.blocos_com_time()
    ja_citados = M.usados_em_scripts()
    rotulos = set(V.rotulos_da_unidade())
    saida, recusas = [], []

    for cena in CENAS:
        for meu in cena["mapas"]:
            pm = os.path.join(REPO, "data/maps", meu, "map.json")
            if not os.path.exists(pm):
                recusas.append((meu, "mapa nao existe"))
                continue
            par = eventos_da_fonte(meu)
            if par is None:
                recusas.append((meu, "sem par na fonte"))
                continue
            fonte, header = par
            d = json.load(open(pm, encoding="utf-8"))
            lid = d["layout"]
            larg, alt = lays[lid]["width"], lays[lid]["height"]
            ocupados = ocupados_do_mapa(d)
            proibidos = proibidos_do_mapa(d)
            ja_no_mapa = {o.get("fonte_id") for o in (d.get("object_events") or [])}
            ancora = centro_de_massa(d) or (larg // 2, alt // 2)
            conv = (lambda e: (e["x"], e["z"])) if cena["coordenada"] == "direta" \
                else None
            pecas = []
            for e in fonte.get("object_events", []):
                if str(e.get("hidden_flag", "0")) != cena["hidden_flag"]:
                    continue
                if e.get("id") in ja_no_mapa:
                    continue
                s = e.get("script")
                treinador = isinstance(s, str) and s.startswith("TRAINER_")
                if not treinador and not cena["mudos"]:
                    continue
                gfx = V.TROCA_SPRITE.get(e["graphics_id"], e["graphics_id"])
                if gfx not in sprites:
                    recusas.append((meu, f"sprite ausente: {e['graphics_id']}"))
                    continue
                nossa = texto = None
                if treinador:
                    nossa = "TRAINER_SINNOH_" + s[len("TRAINER_"):]
                    if nossa in ja_citados:
                        continue          # já vive em outro mapa; nunca duplicar
                    if nossa not in consts:
                        recusas.append((meu, f"sem constante: {nossa}"))
                        continue
                    if nossa not in com_time:
                        recusas.append((meu, f"sem time: {nossa}"))
                        continue
                    texto = falas(s)
                    if texto is None:
                        recusas.append((meu, f"fala nao traduz: {nossa}"))
                        continue
                    ja_citados.add(nossa)
                else:
                    texto = fala_de_mudo(header, e)
                    if texto is None:
                        recusas.append((meu, f"mudo sem fala: {e.get('id')}"))
                        continue
                if conv:
                    x, y = conv(e)
                    if V.colisao(lays, lid, x, y) != 0 or (x, y) in ocupados:
                        alvo = alvo_livre(lays, lid, (x, y), ocupados, proibidos)
                    else:
                        alvo = (x, y)
                else:
                    alvo = alvo_livre(lays, lid, ancora, ocupados, proibidos)
                if alvo is None:
                    recusas.append((meu, f"sem tile livre: {e.get('id')}"))
                    continue
                ocupados.add(alvo)
                obj, trecho = monta(meu, e, gfx, alvo, nossa, texto,
                                    cena["flag"], rotulos)
                pecas.append((obj, trecho))
            if pecas:
                saida.append((cena, meu, pecas))
    return saida, recusas


def falas(constante_platinum):
    """(intro, derrota, depois, None, False) ja prontas para `.string`.

    NAO e `treinadores_masmorra_sinnoh.falas`. Aquela devolve o que
    `texto_sinnoh.resolve` devolve, que HOJE e a tupla `(texto, comandos de
    buffer)`; escrever isso direto no `.string` grava o repr da tupla dentro das
    aspas, e foi exatamente o que a primeira rodada deste script pos em 37
    linhas de dez `scripts.inc` (consertadas na mesma sessao). Aqui a tupla e
    aberta, e o texto que exigir `bufferitemname`/`bufferplayername` e RECUSADO
    inteiro, porque este gerador nao emite comando de buffer nenhum e a fala
    chegaria ao jogador com um `{STR_VAR}` vazio.
    """
    p = os.path.join(PLAT, "res/trainers/data",
                     constante_platinum[len("TRAINER_"):].lower() + ".json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    msg = {m["type"]: m.get("en_US") for m in d.get("messages", [])}
    if d.get("double_battle"):
        return None      # batalha dupla precisa de parceiro; fora desta leva
    saida = []
    for k in ("TRMSG_PRE_BATTLE", "TRMSG_DEFEAT", "TRMSG_POST_BATTLE"):
        if k not in msg:
            return None
        texto, comandos = T.resolve(msg[k], {})
        if not texto or comandos:
            return None
        saida.append(texto)
    return tuple(saida) + (None, False)


def fala_de_mudo(header, e):
    """Fala do objeto sem batalha, tirada do banco de texto do mapa da fonte.

    O `script` de um evento do Platinum e indice 1-BASED dentro da tabela de
    `ScriptEntry` do mapa; a primeira versao daqui usou 0-based e devolveu None
    para o unico grunt mudo desta leva, que e a licao 4.5 em miniatura (o dado
    existia e a regua e que estava errada). Convencao conferida em
    `texto_sinnoh.py:493` e `mudos_sinnoh.py:153`, que ja usam `ordem[idx - 1]`.
    """
    from texto_placas_sinnoh import (campos_do_header, entradas_de_script,
                                     banco_de_texto)
    campos = campos_do_header(header)
    if not campos:
        return None
    ordem, corpos = entradas_de_script(campos[0])
    banco = banco_de_texto(campos[1])
    idx = e.get("script")
    if not isinstance(idx, int) or not (1 <= idx <= len(ordem)):
        return None
    tid, buffers = T.texto_do_rotulo(corpos, ordem[idx - 1])
    if tid is None or tid not in banco:
        return None
    pronto = T.resolve(banco[tid], buffers)
    if not pronto:
        return None
    return ("", "", pronto, None, False)


def rotulo_livre(rotulos, meu, quem):
    base = f"{meu}_EventScript_{quem}"
    n, cand = 1, base
    while any(c in rotulos for c in (cand, cand.replace("_EventScript_",
                                                        "_Text_"))):
        n += 1
        cand = f"{base}{n}"
    rotulos.add(cand)
    rotulos.add(cand.replace("_EventScript_", "_Text_"))
    return cand


def monta(meu, e, gfx, alvo, nossa, texto, flag, rotulos):
    """(objeto do map.json, trecho do scripts.inc)."""
    # O nome do rotulo sai da constante DO PLATINUM, nao da nossa: `TRAINER_
    # SINNOH_...` daria `SinnohGalacticGruntMtCoronet3f1`, com o prefixo de
    # regiao repetido dentro de um rotulo que ja comeca com o nome do mapa.
    quem = M.camel(e["script"]) if nossa else "GalacticGrunt"
    lab = rotulo_livre(rotulos, meu, quem)
    txt = lab.replace("_EventScript_", "_Text_")
    intro, derrota, depois, _falta, duplo = texto
    if nossa:
        raio = str((e.get("data") or [0])[0])
        trecho = (f"\n{lab}::\n"
                  f"\ttrainerbattle_single {nossa}, {txt}Intro, {txt}Defeat\n"
                  f"\tmsgbox {txt}Post, MSGBOX_AUTOCLOSE\n\tend\n\n"
                  f'{txt}Intro:\n\t.string "{intro}"\n\n'
                  f'{txt}Defeat:\n\t.string "{derrota}"\n\n'
                  f'{txt}Post:\n\t.string "{depois}"\n')
        tipo, mov = "TRAINER_TYPE_NORMAL", M.DIRECAO.get(
            e.get("movement_type"), V.MOVIMENTO_PADRAO)
    else:
        raio = "0"
        trecho = (f"\n{lab}::\n\tmsgbox {txt}, MSGBOX_NPC\n\tend\n\n"
                  f'{txt}:\n\t.string "{depois}"\n')
        tipo, mov = "TRAINER_TYPE_NONE", M.DIRECAO.get(
            e.get("movement_type"), V.MOVIMENTO_PADRAO)
    obj = {
        "graphics_id": gfx,
        "x": alvo[0], "y": alvo[1], "elevation": 3,
        "movement_type": mov,
        "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": tipo,
        "trainer_sight_or_berry_tree_id": raio,
        "script": lab,
        "flag": flag,
        "origem": MARCA,
        # Identidade do objeto NA FONTE. E o que torna o --aplica idempotente
        # para quem nao tem constante de treinador: o grunt mudo do tunel nao
        # e reconhecido por `usados_em_scripts()`, e sem esta chave a segunda
        # rodada o punha de novo, com rotulo e tile novos.
        "fonte_id": e.get("id"),
    }
    return obj, trecho


# --------------------------------------------------------------------------
# ON_TRANSITION

def cabeca_de_transicao(meu, texto, cena):
    """Insere o `map_script MAP_SCRIPT_ON_TRANSITION` e o corpo que acende a flag.

    Idempotente: se o mapa já tem um ON_TRANSITION que acende ESTA flag, devolve
    o texto intacto. Se já tem ON_TRANSITION de outra coisa, acrescenta o
    `call_if_defeated` no corpo existente em vez de declarar um segundo.
    """
    corpo = f"{meu}_OnTransition"
    acende = f"{meu}_EventScript_HideGalactica_{cena['chave']}"
    if acende in texto:
        return texto
    linha_call = f"\tcall_if_defeated {cena['gatilho']}, {acende}\n"
    bloco = (f"\n{acende}::\n\tsetflag {cena['flag']}\n\treturn\n")
    if re.search(rf"^{corpo}:", texto, re.M):
        texto = re.sub(rf"^({corpo}:\n)", r"\1" + linha_call, texto, count=1,
                       flags=re.M)
        return texto + bloco
    cabeca = re.search(rf"^{meu}_MapScripts::\n", texto, re.M)
    if not cabeca:
        raise SystemExit(f"{meu}: sem rotulo {meu}_MapScripts::")
    novo = (f"\tmap_script MAP_SCRIPT_ON_TRANSITION, {corpo}\n")
    texto = texto[:cabeca.end()] + novo + texto[cabeca.end():]
    texto += (f"\n@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos"
              f" nascem enquanto\n@ {cena['marco']} nao aconteceu, e somem"
              f" depois; o motor ja grava a flag de\n@ derrotado do gatilho, e"
              f" este ON_TRANSITION so a traduz. Zero var.\n"
              f"{corpo}:\n{linha_call}\tend\n{bloco}")
    return texto


def transicao_de_horario(meu, texto, item):
    """ON_TRANSITION que revela o treinador so na faixa de hora certa."""
    mostra = f"{meu}_EventScript_Mostra_{item['chave']}"
    if mostra in texto:
        return texto
    corpo = f"{meu}_OnTransition"
    linhas = f"\tcall {meu}_EventScript_Horario_{item['chave']}\n"
    # Numero cru, nao o nome: `enum TimeOfDay` (include/constants/rtc.h:98) e
    # enum de C, e enum nao existe para o montador. O nome vai no comentario.
    testes = "".join(f"\tgoto_if_eq VAR_0x8000, {n}, {mostra}  @ {nome}\n"
                     for n, nome in item["hora"])
    bloco = (f"\n{meu}_EventScript_Horario_{item['chave']}::\n"
             f"\tsetflag {item['flag']}\n"
             f"\tgettimeofday\n"
             f"{testes}"
             f"\treturn\n"
             f"\n{mostra}::\n\tclearflag {item['flag']}\n\treturn\n")
    if re.search(rf"^{corpo}:", texto, re.M):
        texto = re.sub(rf"^({corpo}:\n)", r"\1" + linhas, texto, count=1,
                       flags=re.M)
        return texto + bloco
    cabeca = re.search(rf"^{meu}_MapScripts::\n", texto, re.M)
    if not cabeca:
        raise SystemExit(f"{meu}: sem rotulo {meu}_MapScripts::")
    texto = (texto[:cabeca.end()]
             + f"\tmap_script MAP_SCRIPT_ON_TRANSITION, {corpo}\n"
             + texto[cabeca.end():])
    texto += (f"\n@ ponytail: acende PRIMEIRO e apaga so no ramo bom. Falha de"
              f" leitura de hora\n@ deixa o treinador ausente, nunca plantado no"
              f" meio da rota.\n{corpo}:\n{linhas}\tend\n{bloco}")
    return texto


# --------------------------------------------------------------------------
# escrita

def escreve(saida, horas):
    postos = recusados = 0
    for cena, meu, pecas in saida:
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        d = json.load(open(pm, encoding="utf-8"))          # releitura tardia
        lista = d.setdefault("object_events", [])
        ja = {o.get("script") for o in lista}
        texto = open(ps, encoding="utf-8").read()
        novos = []
        for obj, trecho in pecas:
            if obj["script"] in ja:
                recusados += 1
                continue
            novos.append(obj)
            texto += trecho
            postos += 1
        if not novos:
            continue
        lista.extend(novos)          # SEMPRE no fim: a save guarda indice
        texto = cabeca_de_transicao(meu, texto, cena)
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(ps, "w", encoding="utf-8") as f:
            f.write(texto)
    for item, obj, trecho in horas:
        meu = item["mapa"]
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        d = json.load(open(pm, encoding="utf-8"))
        lista = d.setdefault("object_events", [])
        if any(o.get("script") == obj["script"] for o in lista):
            recusados += 1
            continue
        texto = open(ps, encoding="utf-8").read() + trecho
        lista.append(obj)
        texto = transicao_de_horario(meu, texto, item)
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(ps, "w", encoding="utf-8") as f:
            f.write(texto)
        postos += 1
    return postos, recusados


def plano_do_horario():
    lays = layouts()
    sprites = V.sprites_utilizaveis()
    consts = M.constantes_de_treinador()
    com_time = M.blocos_com_time()
    ja_citados = M.usados_em_scripts()
    rotulos = set(V.rotulos_da_unidade())
    saida, recusas = [], []
    for item in HORARIO:
        meu = item["mapa"]
        par = eventos_da_fonte(meu)
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if par is None or not os.path.exists(pm):
            recusas.append((meu, "sem par na fonte"))
            continue
        fonte, header = par
        d = json.load(open(pm, encoding="utf-8"))
        lid = d["layout"]
        larg, alt = lays[lid]["width"], lays[lid]["height"]
        conv = I.conversor_de_coordenada(
            fonte, larg, alt, header,
            I.headers_do_platinum().get(header, (None, None))[1])
        ocupados = ocupados_do_mapa(d)
        proibidos = proibidos_do_mapa(d)
        for e in fonte.get("object_events", []):
            if str(e.get("hidden_flag", "0")) != item["hidden_flag"]:
                continue
            if e.get("script") != item["trainer"]:
                continue
            nossa = "TRAINER_SINNOH_" + item["trainer"][len("TRAINER_"):]
            if nossa in ja_citados:
                continue          # ja esta em mapa; rodada anterior o pos
            if nossa not in consts or nossa not in com_time:
                recusas.append((meu, f"treinador indisponivel: {nossa}"))
                continue
            texto = falas(item["trainer"])
            if texto is None:
                recusas.append((meu, f"fala nao traduz: {nossa}"))
                continue
            gfx = V.TROCA_SPRITE.get(e["graphics_id"], e["graphics_id"])
            if gfx not in sprites:
                recusas.append((meu, f"sprite ausente: {e['graphics_id']}"))
                continue
            ancora = conv(e) if conv else (larg // 2, alt // 2)
            alvo = ancora if (V.colisao(lays, lid, *ancora) == 0
                              and ancora not in ocupados
                              and ancora not in proibidos) else \
                alvo_livre(lays, lid, ancora, ocupados, proibidos)
            if alvo is None:
                recusas.append((meu, "sem tile livre"))
                continue
            ocupados.add(alvo)
            obj, trecho = monta(meu, e, gfx, alvo, nossa, texto,
                                item["flag"], rotulos)
            saida.append((item, obj, trecho))
    return saida, recusas


# --------------------------------------------------------------------------
# ROTEIRO: cenas com controle de fluxo proprio

# Os dois unicos buffers do Platinum que aparecem no texto destas cenas.
# `3, 0, 0` e o nome do rival e `3, 1, 0` o do jogador. O primeiro nao existe
# nesta ROM e vira o nome cravado; o segundo o charmap resolve com {PLAYER}.
BUFFER_CRU = {"{STRVAR_1 3, 0, 0}": RIVAL, "{STRVAR_1 3, 1, 0}": "{PLAYER}"}


def texto_do_banco(banco, msg_id):
    """String pronta para `.string`, ou None se o charmap ou um buffer barrar."""
    p = os.path.join(PLAT, "res/text", banco + ".json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    for m in d.get("messages", []):
        if m["id"] != msg_id:
            continue
        linhas = m.get("en_US")
        if isinstance(linhas, str):
            linhas = [linhas]
        trocadas = []
        for l in linhas:
            for k, v in BUFFER_CRU.items():
                l = l.replace(k, v)
            trocadas.append(l)
        pronto, comandos = T.resolve(trocadas, {})
        if not pronto or comandos:
            return None
        return pronto
    return None


def plano_do_roteiro():
    """[(entrada, [objetos], corpo pronto)] + recusas."""
    lays = layouts()
    sprites = V.sprites_utilizaveis()
    heads = I.headers_do_platinum()
    saida, recusas = [], []
    for r in ROTEIRO:
        meu = r["mapa"]
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        par = eventos_da_fonte(meu)
        if par is None or not os.path.exists(pm):
            recusas.append((meu, "sem par na fonte"))
            continue
        fonte, header = par
        d = json.load(open(pm, encoding="utf-8"))
        lid = d["layout"]
        larg, alt = lays[lid]["width"], lays[lid]["height"]
        conv = I.conversor_de_coordenada(fonte, larg, alt, header,
                                         heads.get(header, (None, None))[1])
        ocupados = ocupados_do_mapa(d)
        proibidos = proibidos_do_mapa(d)
        ja_no_mapa = {o.get("fonte_id") for o in (d.get("object_events") or [])}
        # Todo texto ANTES de qualquer objeto: cena com uma fala que nao traduz
        # entra pela metade, e meia cena e pior que cena nenhuma.
        textos = {}
        for chave, msg in r["textos"].items():
            pronto = texto_do_banco(r["banco"], msg)
            if pronto is None:
                recusas.append((meu, f"texto nao traduz: {msg}"))
                textos = None
                break
            textos[chave] = pronto
        if textos is None:
            continue
        por_fonte = {e.get("id"): e for e in fonte.get("object_events", [])}
        objetos = []
        for spec in r["objetos"]:
            if spec["fonte_id"] in ja_no_mapa:
                continue
            e = por_fonte.get(spec["fonte_id"])
            if e is None:
                recusas.append((meu, f"objeto ausente na fonte: {spec['fonte_id']}"))
                continue
            gfx = spec.get("sprite") or V.TROCA_SPRITE.get(e["graphics_id"],
                                                           e["graphics_id"])
            if gfx not in sprites:
                recusas.append((meu, f"sprite ausente: {gfx}"))
                continue
            alvo = spec.get("xy") or (conv(e) if conv else None)
            if alvo is None or V.colisao(lays, lid, *alvo) != 0 \
                    or alvo in ocupados or alvo in proibidos:
                alvo = alvo_livre(lays, lid, alvo or (larg // 2, alt // 2),
                                  ocupados, proibidos)
            if alvo is None:
                recusas.append((meu, f"sem tile livre: {spec['fonte_id']}"))
                continue
            ocupados.add(alvo)
            objetos.append({
                "local_id": spec["local_id"],
                "graphics_id": gfx,
                "x": alvo[0], "y": alvo[1], "elevation": 3,
                "movement_type": spec.get("mov", V.MOVIMENTO_PADRAO),
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": ("TRAINER_TYPE_NORMAL" if spec.get("sight")
                                 else "TRAINER_TYPE_NONE"),
                "trainer_sight_or_berry_tree_id": spec.get("sight", "0"),
                "script": spec["script"],
                "flag": spec["flag"],
                "origem": MARCA,
                "fonte_id": spec["fonte_id"],
            })
        corpo = r["corpo"]
        blocos = []
        for chave, pronto in sorted(textos.items()):
            rot = f"{meu}_Text_Cena{chave}"
            corpo = corpo.replace("{TXT_%s}" % chave, rot)
            blocos.append(f'\n{rot}:\n\t.string "{pronto}"\n')
        assert "{TXT_" not in corpo, f"{meu}: placeholder sem texto em {corpo}"
        saida.append((r, objetos, corpo + "".join(blocos)))
    return saida, recusas


def escreve_roteiro(plano):
    postos = 0
    for r, objetos, corpo in plano:
        meu = r["mapa"]
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        d = json.load(open(pm, encoding="utf-8"))       # releitura tardia
        lista = d.setdefault("object_events", [])
        ja = {o.get("fonte_id") for o in lista}
        novos = [o for o in objetos if o["fonte_id"] not in ja]
        texto = open(ps, encoding="utf-8").read()
        # Idempotencia: o PRIMEIRO rotulo do corpo ja estar no arquivo significa
        # que esta cena ja foi aplicada. Basta um teste, e ele e do texto, nao da
        # contagem de objetos: cena pode ter zero objeto novo e corpo novo.
        rot0 = re.search(r"^(\w+)::", corpo, re.M)
        if rot0 and re.search(rf"^{rot0.group(1)}::", texto, re.M):
            continue
        lista.extend(novos)                             # SEMPRE no fim
        postos += len(novos)
        for ajuste in r.get("ajustes", []):
            for o in lista:
                if o.get("local_id") == ajuste["local_id"]:
                    o[ajuste["campo"]] = ajuste["valor"]
        for ce in r.get("coord_events", []):
            lista_ce = d.setdefault("coord_events", [])
            if any(c.get("x") == ce["x"] and c.get("y") == ce["y"]
                   for c in lista_ce):
                continue
            lista_ce.append({"type": "trigger", "x": ce["x"], "y": ce["y"],
                             "elevation": 3, "var": "VAR_TEMP_0",
                             "var_value": "0", "script": ce["script"]})
        texto += corpo
        if r.get("on_transition"):
            corpo_ot = f"{meu}_OnTransition"
            if not re.search(rf"^{corpo_ot}:", texto, re.M):
                cabeca = re.search(rf"^{meu}_MapScripts::\n", texto, re.M)
                if not cabeca:
                    raise SystemExit(f"{meu}: sem rotulo {meu}_MapScripts::")
                texto = (texto[:cabeca.end()]
                         + f"\tmap_script MAP_SCRIPT_ON_TRANSITION, {corpo_ot}\n"
                         + texto[cabeca.end():] + r["on_transition"])
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(ps, "w", encoding="utf-8") as f:
            f.write(texto)
    return postos


# --------------------------------------------------------------------------

def demo():
    """As armadilhas que a primeira versao deste script tinha, cada uma provada.

    Cada assert abaixo falha se a regra sumir. Nada aqui guarda cópia de um
    número medido: as regras são de FORMA (lição 4.11 do ESTADO.md).
    """
    lays = layouts()

    # 1. Nenhuma constante de treinador pode entrar duas vezes no jogo: o motor
    #    grava UMA flag de derrotado por id, e reusar daria a cena por vencida.
    saida, _ = plano_das_cenas()
    horas, _ = plano_do_horario()
    vistos = []
    for _c, _m, pecas in saida:
        for obj, trecho in pecas:
            vistos += re.findall(r"trainerbattle_single (TRAINER_\w+)", trecho)
    for _i, _o, trecho in horas:
        vistos += re.findall(r"trainerbattle_single (TRAINER_\w+)", trecho)
    assert len(vistos) == len(set(vistos)), f"treinador repetido: {vistos}"
    ja = M.usados_em_scripts()
    assert not (set(vistos) & ja), \
        f"treinador que ja vive em outro mapa: {set(vistos) & ja}"

    # 2 e 3. Todo objeto criado, de cena OU de horario, tem que cair em tile
    #    ANDAVEL, fora de porta, e nascer COM flag. Objeto de cena sem flag e
    #    parede permanente, que e a regra do PRD que este script respeita.
    todos = [(meu, obj) for _c, meu, pecas in saida for obj, _t in pecas]
    todos += [(item["mapa"], obj) for item, obj, _t in horas]
    # E tambem o que JA esta na arvore. Depois do --aplica o plano fica vazio, e
    # um demo que so olha o plano vira verde por nao ter o que olhar (licao 4.3:
    # falso positivo e pior que validador nenhum). Estes continuam sendo medidos
    # em toda rodada, entao o demo tambem guarda a leva ja aplicada.
    for meu in ([m for c in CENAS for m in c["mapas"]]
                + [i["mapa"] for i in HORARIO]):
        d = json.load(open(os.path.join(REPO, "data/maps", meu, "map.json"),
                           encoding="utf-8"))
        todos += [(meu, o) for o in (d.get("object_events") or [])
                  if o.get("origem") == MARCA]

    def checa(lista):
        """[] se tudo passa; a lista de queixas se nao."""
        ruim = []
        for meu, obj in lista:
            d = json.load(open(os.path.join(REPO, "data/maps", meu, "map.json"),
                               encoding="utf-8"))
            p = (obj["x"], obj["y"])
            if V.colisao(lays, d["layout"], *p) != 0:
                ruim.append(f"{meu}: {p} nao e andavel")
            if p in proibidos_do_mapa(d):
                ruim.append(f"{meu}: {p} encosta em warp")
            if obj["flag"] in ("0", "0x0", ""):
                ruim.append(f"{meu}: {obj['script']} sem flag")
        return ruim

    assert not checa(todos), checa(todos)

    # 4. A flag que esconde tem que ser ACESA por alguem. Cena sem gatilho e
    #    bloqueio eterno; e o gatilho tem que ser treinador que existe.
    consts = M.constantes_de_treinador()
    for cena in CENAS:
        assert cena["gatilho"] in consts, cena["gatilho"]

    # 5. O ON_TRANSITION nao pode nascer duas vezes. Rodar o gerador de cabeca
    #    sobre a propria saida dele tem que devolver o texto intacto.
    falso = ("Foo_MapScripts::\n\t.byte 0\n")
    cena = dict(CENAS[0], chave="teste")
    uma = cabeca_de_transicao("Foo", falso, cena)
    assert uma != falso and cabeca_de_transicao("Foo", uma, cena) == uma, \
        "cabeca_de_transicao nao e idempotente"
    assert uma.count("MAP_SCRIPT_ON_TRANSITION") == 1, uma

    # 6. A mesma prova para o ramo de horario, e a POLARIDADE: tem que acender
    #    antes de testar a hora, senao falha de leitura planta o treinador.
    item = HORARIO[0]
    duas = transicao_de_horario("Foo", falso, item)
    assert transicao_de_horario("Foo", duas, item) == duas, \
        "transicao_de_horario nao e idempotente"
    i_set = duas.index(f"setflag {item['flag']}")
    i_hora = duas.index("gettimeofday")
    i_clear = duas.index(f"clearflag {item['flag']}")
    assert i_set < i_hora < i_clear, \
        "polaridade errada: tem que acender, ler a hora, e so entao apagar"

    # 7. Contraprova, no plano DE VERDADE: tres mutacoes plantadas em cima do
    #    primeiro objeto real, cada uma tem que ser reprovada. "Nao achou nada"
    #    so vale depois que a checagem mostrou que morde (regra do PRD: boa
    #    noticia e suspeita).
    meu0, obj0 = todos[0]
    d0 = json.load(open(os.path.join(REPO, "data/maps", meu0, "map.json"),
                        encoding="utf-8"))
    porta = sorted(proibidos_do_mapa(d0))[0] if proibidos_do_mapa(d0) else None
    mutacoes = [
        ("flag zerada", dict(obj0, flag="0")),
        ("dentro da parede", dict(obj0, x=0, y=0)),
    ]
    if porta:
        mutacoes.append(("colado na porta",
                         dict(obj0, x=porta[0], y=porta[1])))
    for nome, mutante in mutacoes:
        assert checa([(meu0, mutante)]), \
            f"a checagem NAO mordeu a mutacao {nome!r}"

    # 8. As cenas do ROTEIRO, medidas na ARVORE (o plano fica vazio depois do
    #    --aplica). Tres perguntas que so o arquivo escrito responde:
    #    a) todo local_id citado por removeobject/addobject/applymovement existe
    #       no map.json daquele mapa. local_id errado e erro de montagem, e a
    #       versao anterior desta ferramenta nao olhava;
    #    b) todo objeto do roteiro caiu em chao andavel;
    #    c) as cinco constantes novas existem, tem bloco em trainers.party e
    #       estao dentro da faixa 2500 a 2519 desta frente.
    consts_todas = M.constantes_de_treinador()
    com_time_todas = M.blocos_com_time()
    for r in ROTEIRO:
        meu = r["mapa"]
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        d = json.load(open(pm, encoding="utf-8"))
        locais = {o.get("local_id") for o in (d.get("object_events") or [])}
        txt = open(ps, encoding="utf-8").read()
        citados = set(re.findall(
            r"^\t(?:removeobject|addobject|applymovement)\s+(LOCALID_\w+)",
            txt, re.M))
        assert citados <= locais, \
            f"{meu}: local_id citado e inexistente: {sorted(citados - locais)}"
        for o in (d.get("object_events") or []):
            if o.get("origem") != MARCA:
                continue
            assert V.colisao(lays, d["layout"], o["x"], o["y"]) == 0, \
                f"{meu}: ({o['x']},{o['y']}) nao e andavel"
        for ce in (d.get("coord_events") or []):
            if ce.get("script", "").startswith(f"{meu}_EventScript_"):
                assert V.colisao(lays, d["layout"], ce["x"], ce["y"]) == 0, \
                    f"{meu}: coord_event em ({ce['x']},{ce['y']}) e parede"
    for n in re.findall(r"trainerbattle_single (TRAINER_SINNOH_\w+)",
                        "".join(r["corpo"] for r in ROTEIRO)):
        assert n in consts_todas, f"{n} sem #define"
        assert n in com_time_todas, f"{n} sem bloco em trainers.party"
        assert 2500 <= consts_todas[n] <= 2519, \
            f"{n} = {consts_todas[n]} esta fora da faixa 2500-2519 desta frente"

    # 9. A afirmacao mais perigosa desta leva, provada na CAMADA DELA. O show da
    #    Rota 218 e o unico grupo importado que fica em cima da estrada, e se ele
    #    selasse o caminho o hack travaria: Celestic, que e quem apaga a flag do
    #    show, so se alcanca pelo outro lado do mapa. A afirmacao "nao sela" e
    #    sobre a GRADE DE COLISAO, entao quem responde e uma busca em largura na
    #    grade, com os seis objetos ocupando tile, e nao a minha leitura dela.
    d218 = json.load(open(os.path.join(REPO, "data/maps/Route218/map.json"),
                          encoding="utf-8"))
    lid = d218["layout"]
    larg, alt = lays[lid]["width"], lays[lid]["height"]
    ocup = {(o["x"], o["y"]) for o in (d218.get("object_events") or [])}
    ini, fim = (18, 20), (5, 20)
    assert ini not in ocup and fim not in ocup, "os extremos do teste estao ocupados"
    fila, visto = [ini], {ini}
    while fila:
        x, y = fila.pop()
        if (x, y) == fim:
            break
        for nx, ny in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            if (nx, ny) in visto or not (0 <= nx < larg and 0 <= ny < alt):
                continue
            if (nx, ny) in ocup or V.colisao(lays, lid, nx, ny) != 0:
                continue
            visto.add((nx, ny))
            fila.append((nx, ny))
    assert fim in visto, \
        ("o show da Rota 218 SELOU a estrada: com Celestic do outro lado do mapa "
         "isso e softlock, e nenhum objeto do show pode ficar onde esta")

    print(f"demo ok ({len(vistos)} treinadores unicos no plano, "
          f"{len(todos)} objetos das cinco primeiras cenas, "
          f"{len(ROTEIRO)} cenas de roteiro conferidas na arvore, "
          f"{len(mutacoes)} mutacoes plantadas e todas reprovadas)")


def main():
    if "--demo" in sys.argv:
        return demo()
    saida, recusas = plano_das_cenas()
    horas, r2 = plano_do_horario()
    rot, r3 = plano_do_roteiro()
    recusas += r2 + r3
    total = (sum(len(p) for _c, _m, p in saida) + len(horas)
             + sum(len(o) for _r, o, _c in rot))
    print(f"objetos de cena a criar: {total}")
    for r, objetos, _corpo in rot:
        print(f"  [{r['chave']:12s}] {r['mapa']:28s} {len(objetos)}  "
              f"{r['titulo']}")
        for obj in objetos:
            print(f"      ({obj['x']:3d},{obj['y']:3d}) {obj['graphics_id']:26s}"
                  f" flag={obj['flag']:32s} {obj['script']}")
    for cena, meu, pecas in saida:
        print(f"  [{cena['chave']:12s}] {meu:28s} {len(pecas)} "
              f"flag={cena['flag']}")
        for obj, _t in pecas:
            print(f"      ({obj['x']:3d},{obj['y']:3d}) {obj['graphics_id']:26s}"
                  f" {obj['script']}")
    for item, obj, _t in horas:
        print(f"  [{item['chave']:12s}] {item['mapa']:28s} 1 "
              f"flag={item['flag']}  ({obj['x']},{obj['y']})")
    if recusas:
        print("\nrecusados:")
        for m, por in recusas:
            print(f"  {m:30s} {por}")
    if APLICA:
        postos, rec = escreve(saida, horas)
        postos += escreve_roteiro(rot)
        print(f"\nescrito: {postos} objetos; recusados na releitura: {rec}")
    else:
        print("\n(nada escrito; use --aplica)")


if __name__ == "__main__":
    main()
