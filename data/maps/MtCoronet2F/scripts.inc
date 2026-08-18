MtCoronet2F_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ rotulo da fonte: MtCoronet2F_CoordEvent_Looker (script 2, mesmo indice de
@ MtCoronet2F_CavePainting: os dois sao o MESMO bloco de codigo na fonte).
@ LOCALID_MT_CORONET_2F_LOOKER ja fica de pe la (sempre visivel, sem flag: a
@ fonte faz SetObjectEventPos+ClearFlag+AddObject na propria cena porque ele
@ nao existia antes, mas aqui e mais simples nascer plantado no ponto de
@ chegada e pular a coreografia de aparecer). O quadro rupestre que vira
@ cacos (FLAG_HIDE_MT_CORONET_2F_CAVE_PAINTING/_SHARDS) fica de fora: e
@ mobiliario (GRAFICOS_PROIBIDOS de importa_npcs_sinnoh.py), nunca virou
@ objeto aqui. FLAG_RECEIVED_MT_CORONET_2F_BLACK_FLUTE tambem fica de fora:
@ e o diario de itens recebidos do Platinum, mecanica que nao existe aqui.
@ VAR_SINNOH_CORONET_2F_ESTADO vira 2 (SetVar no TOPO da cena, literal da
@ fonte); quem escreve o var=1 que destrava este gatilho e o fecho do Saturn
@ em GalacticHQ_ControlRoom_EventScript_SaturnDefeated.
MtCoronet2F_EventScript_CoordEvent_Looker::
	lockall
	setvar VAR_SINNOH_CORONET_2F_ESTADO, 2
	applymovement LOCALID_MT_CORONET_2F_LOOKER, MtCoronet2F_Movement_LookerNoticePlayer
	waitmovement 0
	msgbox MtCoronet2F_Text_ObserveThatHole, MSGBOX_DEFAULT
	applymovement LOCALID_MT_CORONET_2F_LOOKER, MtCoronet2F_Movement_LookerWalkOnSpotSouth
	waitmovement 0
	msgbox MtCoronet2F_Text_AreYouEnoughToAdvance, MSGBOX_DEFAULT
	applymovement LOCALID_MT_CORONET_2F_LOOKER, MtCoronet2F_Movement_LookerWalkOnSpotWest
	waitmovement 0
	msgbox MtCoronet2F_Text_YouAreFarSuperiorToMe, MSGBOX_DEFAULT
	giveitem ITEM_BLACK_FLUTE
	msgbox MtCoronet2F_Text_YouMustStopTeamGalactic, MSGBOX_DEFAULT
	releaseall
	end

@ Script de CLIQUE no objeto (o map.json aponta o Looker para ca; o rotulo
@ acima e o do coord_event, sao dois scripts diferentes na fonte tambem:
@ ScriptEntry 2 = MtCoronet2F_CoordEvent_Looker, ScriptEntry 3 =
@ MtCoronet2F_Looker, e o objeto usa `"script": 3`).
@ A fonte (res/field/scripts/scripts_mt_coronet_2f.s:131) ramifica em
@ FLAG_RECEIVED_MT_CORONET_2F_BLACK_FLUTE: sem a flag, tenta entregar a Black
@ Flute de novo; com a flag, so repete a fala. Aqui a flag NAO existe de
@ proposito (e o diario de itens recebidos do Platinum, mecanica que nao
@ existe neste motor, ja anotado no cabecalho acima), e a Black Flute ja e
@ entregue uma vez so pelo proprio coord_event, entao sobra o ramo "ja
@ recebeu": repetir a fala. PlaySE SEQ_SE_CONFIRM da fonte cai junto (e o bipe
@ de abrir caixa do DS, que este motor toca sozinho).
MtCoronet2F_EventScript_Looker::
	lock
	faceplayer
	msgbox MtCoronet2F_Text_YouMustStopTeamGalactic, MSGBOX_DEFAULT
	release
	end

MtCoronet2F_Movement_LookerNoticePlayer:
	emote_exclamation_mark
	walk_in_place_left
	step_end

MtCoronet2F_Movement_LookerWalkOnSpotSouth:
	walk_in_place_down
	step_end

MtCoronet2F_Movement_LookerWalkOnSpotWest:
	walk_in_place_left
	step_end

@ Texto literal de res/text/mt_coronet_2f.json, requebrado para a largura daqui.
MtCoronet2F_Text_ObserveThatHole:
	.string "Looker: Observe, if you will, that\n"
	.string "hole.\p"
	.string "There was once a cave painting\n"
	.string "that had blocked the way to the\l"
	.string "summit.\p"
	.string "But the wall, it is no longer\n"
	.string "there. It lies in pieces. Do you\l"
	.string "see?\p"
	.string "Ever since the three Pokémon of\n"
	.string "the lakes have been captured...\p"
	.string "Something terrible is happening,\n"
	.string "but what exactly, I do not know.$"

MtCoronet2F_Text_AreYouEnoughToAdvance:
	.string "There is but one cause!\n"
	.string "Team Galactic's Cyrus!\p"
	.string "And now, we are all caught up.\n"
	.string "Now, to the next step.\p"
	.string "Are you Trainer enough to\n"
	.string "advance? Show me, if you will!$"

MtCoronet2F_Text_YouAreFarSuperiorToMe:
	.string "...\n"
	.string "...\p"
	.string "Hahaha!\n"
	.string "You can relax now.\p"
	.string "You see, I understand.\n"
	.string "You are far superior to me.\p"
	.string "As are the Commanders.\n"
	.string "Cyrus, too, naturally.\p"
	.string "Team Galactic is beyond my\n"
	.string "reach...\p"
	.string "Please, you must stop them!\n"
	.string "For only you are able!\p"
	.string "All I can do now is give you\n"
	.string "this.\p"
	.string "It is a little something I\n"
	.string "obtained in an investigation\l"
	.string "long ago.$"

MtCoronet2F_Text_YouMustStopTeamGalactic:
	.string "Looker: Please!\n"
	.string "You must stop Team Galactic!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<
