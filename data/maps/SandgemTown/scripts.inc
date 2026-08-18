@ Sandgem Town. Ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever script novo.
@ sinnoh-dados/sandgem_town.json nao trouxe falas em ingles para estes NPCs
@ (lista "falas_em_ingles" vazia); falas abaixo escritas no mesmo tom da regiao.

SandgemTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SandgemTown_OnTransition
	.byte 0

SandgemTown_OnTransition::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, SandgemTown_SetCounterpartFemale
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	end

SandgemTown_SetCounterpartFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	end

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Fonte: SandgemTown_CoordEvent_CounterpartLeadToLab. A contraparte nota o
@ jogador e leva ate a porta do laboratorio, avisando que o professor esta
@ esperando.
@
@ ponytail, cortado da fonte: o "big thud" do rival saindo do laboratorio
@ (SandgemTown_RivalExitLab) e o presente do TM27 (SandgemTown_OnFrame_
@ ExitLab) nao entram. O RIVAL desta cidade ja e um objeto sempre visivel
@ (LOCALID_SANDGEM_RIVAL, flag "0", plantado antes desta leva); repetir o
@ hidden_flag FLAG_HIDE_SANDGEM_TOWN_RIVAL duplicaria o mesmo personagem no
@ mapa. E o proprio ROWAN ja entrega a escolha do inicial inteira, sozinha e
@ testada, dentro de SandgemTown_RowanLab (sem contraparte, sem TM). Reabrir
@ a "excursao pela cidade" da fonte (PokeCenter/Mart, contraparte saindo da
@ cidade) duplicaria conteudo que ja funciona e nao tem var aliasada para o
@ estado seguinte. FLAG_HIDE_SANDGEM_TOWN_RIVAL e FLAG_HIDE_SANDGEM_TOWN_
@ PROF_ROWAN ficam SEM objeto plantado por isso (reportado, nao inventado).
SandgemTown_EventScript_CoordEvent_CounterpartLeadToLab::
	lockall
	applymovement LOCALID_SANDGEM_COUNTERPART, SandgemTown_Movement_CounterpartNoticePlayer
	waitmovement 0
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, SandgemTown_EventScript_DawnProfessorWaiting
	msgbox SandgemTown_Text_LucasTheProfsWaitingToSeeYou, MSGBOX_DEFAULT
	goto SandgemTown_EventScript_CounterpartWalkToLab

SandgemTown_EventScript_DawnProfessorWaiting::
	msgbox SandgemTown_Text_DawnTheProfessorIsWaiting, MSGBOX_DEFAULT

SandgemTown_EventScript_CounterpartWalkToLab::
	applymovement LOCALID_SANDGEM_COUNTERPART, SandgemTown_Movement_CounterpartWalkToLab
	waitmovement 0
	@ `set_invisible` no fim do movimento so apaga o sprite ate a proxima
	@ entrada no mapa: sem esta dupla a contraparte reaparecia andando na
	@ praca toda vez que o jogador voltasse. A flag e a do proprio
	@ object_event (FLAG_HIDE_SANDGEM_TOWN_COUNTERPART na fonte). Mesma nota
	@ de Route202: a fonte nao acende porque la ela volta pelo reveza-mapa da
	@ cena de PokeRadar, que e Poketch e nao existe aqui (decisao 3).
	setflag FLAG_SINNOH_ESCONDE_SANDGEM_TOWN_COUNTERPART
	removeobject LOCALID_SANDGEM_COUNTERPART
	setvar VAR_SINNOH_SANDGEM_ESTADO, 1
	releaseall
	end

	.balign 4, 0
SandgemTown_Movement_CounterpartNoticePlayer:
	emote_exclamation_mark
	step_end

	.balign 4, 0
SandgemTown_Movement_CounterpartWalkToLab:
	walk_up
	walk_up
	set_invisible
	step_end

SandgemTown_Text_DawnTheProfessorIsWaiting:
	.string "{RIVAL}: Oh! There you are!\n"
	.string "Please, come with me!\p"
	.string "The professor is waiting!$"

SandgemTown_Text_LucasTheProfsWaitingToSeeYou:
	.string "{RIVAL}: Hi! I've been waiting for you!\n"
	.string "Please, come with me.\p"
	.string "The prof's waiting to see you.$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

SandgemTown_EventScript_Professor::
	lock
	faceplayer
	msgbox SandgemTown_Text_Professor, MSGBOX_DEFAULT
	release
	end

SandgemTown_EventScript_Rival::
	lock
	faceplayer
	msgbox SandgemTown_Text_Rival, MSGBOX_DEFAULT
	release
	end

SandgemTown_EventScript_TownSign::
	msgbox SandgemTown_Text_TownSign, MSGBOX_SIGN
	end

@ Fala do Platinum, sandgem_town.json (SandgemTown_Text_RowansComeBack). Este
@ NPC era um segundo ROWAN na rua, com o sprite do professor, enquanto o ROWAN
@ de verdade esta no laboratorio; virou morador comentando a volta dele.
SandgemTown_Text_Professor:
	.string "PROFESSOR ROWAN's come back to town!\p"
	.string "It must be, like, four years since\n"
	.string "he left.\p"
	.string "They say he was doing his research\n"
	.string "somewhere else all this time.$"

SandgemTown_Text_Rival:
	.string "Hey! You're heading to the lab too?\p"
	.string "Race you there!$"

SandgemTown_Text_TownSign:
	.string "SANDGEM TOWN\n"
	.string "Where the Winds of New Beginnings Blow$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

SandgemTown_EventScript_Placa1::
	msgbox SandgemTown_Text_Placa1, MSGBOX_SIGN
	end

SandgemTown_Text_Placa1:
	.string "Pokémon Research Lab$"

SandgemTown_EventScript_Placa4::
	msgbox SandgemTown_Text_Placa4, MSGBOX_SIGN
	end

SandgemTown_Text_Placa4:
	.string "Heal Your Pokémon!\nPokémon Center$"

SandgemTown_EventScript_Placa5::
	msgbox SandgemTown_Text_Placa5, MSGBOX_SIGN
	end

SandgemTown_Text_Placa5:
	.string "All Your Item Needs Fulfilled!\nPokémon Mart$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SandgemTown_EventScript_Npc1::
	msgbox SandgemTown_Text_Npc1, MSGBOX_NPC
	end

SandgemTown_Text_Npc1:
	.string "Oh, wow!\nPokémon are so cool!\pYou can make yours battle and make\nthem stronger!\pI wish I had some!\nIt's so cool!$"

SandgemTown_EventScript_Npc2::
	msgbox SandgemTown_Text_Npc2, MSGBOX_NPC
	end

SandgemTown_Text_Npc2:
	.string "That thing you have!\pIt's a Pokédex, isn't it?!\pYou're off to see all kinds of\nPokémon now! Lucky you!$"

SandgemTown_EventScript_Npc3::
	msgbox SandgemTown_Text_Npc3, MSGBOX_NPC
	end

SandgemTown_Text_Npc3:
	.string "So I don't forget what's happened,\ntill now, I'd better save this...\pThere!\nNow I can take a break.$"

SandgemTown_EventScript_Placa2::
	msgbox SandgemTown_Text_Placa2, MSGBOX_SIGN
	end

SandgemTown_Text_Placa2:
	.string "Sandgem Town\nTown of Sand!$"
