@ ChampionsRoomEntrance do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 12/08/2026 (B5) e reescrito em 12/08/2026 (B6).
@
@ ISTO E A PRIMEIRA METADE DA CENA FINAL. A fonte e `ChampionsRoomEntranceScript`,
@ disparado por `coord_event 7, 6, SCENE_DEFAULT` em ChampionsRoomEntrance.asm.
@ O B5 tinha escondido os cinco figurantes com FLAG_UNOVA_LIGA_ELENCO porque dois
@ deles (JUNIPER e METAGROSS) nascem em (7,5), que e o UNICO warp do mapa; o B6
@ agora ACENDE E APAGA essa mesma flag na hora certa, que era o que o comentario
@ do B5 pedia.
@
@ TRADUCAO DO `setscene`, e nao copia do asm: a fonte tem dois `scene_script`
@ (SCENE_DEFAULT e SCENE_FINISHED) e um MAPCALLBACK_NEWMAP que devolve a cena
@ para SCENE_DEFAULT enquanto o jogador nao tiver batido o GENESIS (para a
@ emboscada rodar de novo se ele perder). Aqui isso e um bit so,
@ FLAG_UNOVA_CENA_ENTRADA_LIGA, e o ON_TRANSITION apaga o bit enquanto
@ FLAG_UNOVA_GENESIS_VENCIDO estiver apagada. Mesmo efeito, zero var.
@
@ O gatilho e `coord_event` com VAR_TEMP_0 valor 0 (tecnica 1 do
@ SINNOH-PADRAO.md): o motor zera os VAR_TEMP_* a cada entrada de mapa, entao o
@ gatilho vale sempre e quem lembra que a cena ja rodou e a flag, dentro do
@ script. Zero var.
@
@ DUAS COISAS QUE NAO SAO COPIA LITERAL DA FONTE, e o motivo:
@ 1. No BW3G os cinco figurantes FICAM no mapa depois da cena (o script que os
@    apagaria, `ChampionsRoomEntranceDisappearObjects`, esta comentado dentro dos
@    bg_events da propria fonte). Aqui eles voltam a ficar escondidos no fim,
@    porque o template da JUNIPER e o do METAGROSS estao em cima do warp (7,5):
@    deixa-los nascer de novo tranca a sala do Campeao, que e a armadilha dos
@    guardas de insignia da Liga de Sinnoh (casos T81.*).
@ 2. `teleport_to`/`teleport_from` do gen 2 nao tem equivalente de movimento
@    aqui; entram como SE_WARP_IN/SE_WARP_OUT mais addobject/removeobject. Som e
@    o mesmo, animacao de subir e descer nao existe.
@
@ Ids locais dos objetos (indice na lista do map.json + 1, que e como o motor
@ numera quando o objeto nao declara `local_id`):
@   1 = SOMBRA 1 (6,6)   2 = SOMBRA 2 (7,7)   3 = SOMBRA 3 (8,6)
@   4 = JUNIPER (7,5)    5 = METAGROSS (7,5)

Unova_ChampionsRoomEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_ChampionsRoomEntrance_OnTransition
	.byte 0

@ `.ResetScene` da fonte, mais o esconde-elenco do B5.
Unova_ChampionsRoomEntrance_OnTransition:
	setflag FLAG_UNOVA_LIGA_ELENCO
	goto_if_set FLAG_UNOVA_GENESIS_VENCIDO, Unova_ChampionsRoomEntrance_EventScript_TransicaoFim
	clearflag FLAG_UNOVA_CENA_ENTRADA_LIGA
Unova_ChampionsRoomEntrance_EventScript_TransicaoFim::
	end

Unova_ChampionsRoomEntrance_EventScript_Emboscada::
	goto_if_set FLAG_UNOVA_CENA_ENTRADA_LIGA, Unova_ChampionsRoomEntrance_EventScript_EmboscadaFim
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	msgbox Unova_ChampionsRoomEntrance_Text_SombrasChegam, MSGBOX_DEFAULT
	closemessage
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	applymovement LOCALID_PLAYER, Unova_ChampionsRoomEntrance_Movement_JogadorRecua
	waitmovement 0
	clearflag FLAG_UNOVA_LIGA_ELENCO
	playse SE_WARP_IN
	addobject 2
	waitse
	playse SE_WARP_IN
	addobject 1
	waitse
	playse SE_WARP_IN
	addobject 3
	waitse
	msgbox Unova_ChampionsRoomEntrance_Text_SombrasSeApresentam, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_ChampionsRoomEntrance_Movement_SombraDesce
	applymovement 3, Unova_ChampionsRoomEntrance_Movement_SombraDesce
	waitmovement 0
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	msgbox Unova_ChampionsRoomEntrance_Text_MetagrossAtaca, MSGBOX_DEFAULT
	closemessage
	addobject 5
	applymovement 1, Common_Movement_WalkInPlaceFasterUp
	applymovement 2, Common_Movement_WalkInPlaceFasterUp
	applymovement 3, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	playmoncry SPECIES_METAGROSS, CRY_MODE_NORMAL
	waitmoncry
	playse SE_M_TAKE_DOWN
	applymovement 5, Unova_ChampionsRoomEntrance_Movement_MetagrossInveste
	applymovement 2, Unova_ChampionsRoomEntrance_Movement_SombraLevaPancada
	waitmovement 0
	delay 30
	playbgm MUS_ENCOUNTER_MAY, FALSE
	playse SE_DOOR
	addobject 4
	waitse
	msgbox Unova_ChampionsRoomEntrance_Text_JuniperChega, MSGBOX_DEFAULT
	closemessage
	playse SE_BALL_OPEN
	removeobject 5
	waitse
	applymovement 4, Unova_ChampionsRoomEntrance_Movement_JuniperSeAproxima
	waitmovement 0
	msgbox Unova_ChampionsRoomEntrance_Text_PlanoDasSombras, MSGBOX_DEFAULT
	closemessage
	applymovement 4, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox Unova_ChampionsRoomEntrance_Text_PrecisamosParar, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_ChampionsRoomEntrance_Movement_SombraSobeEOlhaDireita
	applymovement 3, Unova_ChampionsRoomEntrance_Movement_SombraSobeEOlhaEsquerda
	waitmovement 0
	msgbox Unova_ChampionsRoomEntrance_Text_SegurarAsSombras, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Unova_ChampionsRoomEntrance_Movement_JogadorContorna
	waitmovement 0
	applymovement 4, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Unova_ChampionsRoomEntrance_Text_DeixeMeCurar, MSGBOX_DEFAULT
	closemessage
	playse SE_USE_ITEM
	special HealPlayerParty
	waitse
	msgbox Unova_ChampionsRoomEntrance_Text_VaDepressa, MSGBOX_DEFAULT
	closemessage
	applymovement 4, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	setflag FLAG_UNOVA_CENA_ENTRADA_LIGA
	@ os cinco voltam a ficar escondidos: dois deles moram em cima do warp (7,5)
	setflag FLAG_UNOVA_LIGA_ELENCO
	fadedefaultbgm
	warp MAP_UNOVA_CHAMPIONS_ROOM, 7, 19
	waitstate
	releaseall
	end

Unova_ChampionsRoomEntrance_EventScript_EmboscadaFim::
	end

@ `ChampionsRoomEntrancePlayerBackUpMovement`. O gen 2 anda de costas com
@ fix_facing; aqui o jogador desce virado para baixo e volta a olhar para cima no
@ fim, que e o mais perto que o motor tem sem efeito de campo novo.
Unova_ChampionsRoomEntrance_Movement_JogadorRecua:
	walk_slow_down
	walk_slow_down
	walk_slow_down
	face_up
	step_end

Unova_ChampionsRoomEntrance_Movement_SombraDesce:
	walk_down
	walk_down
	step_end

Unova_ChampionsRoomEntrance_Movement_MetagrossInveste:
	walk_fast_down
	step_end

Unova_ChampionsRoomEntrance_Movement_SombraLevaPancada:
	walk_fast_down
	step_end

Unova_ChampionsRoomEntrance_Movement_JuniperSeAproxima:
	walk_slow_down
	walk_slow_down
	step_end

Unova_ChampionsRoomEntrance_Movement_SombraSobeEOlhaDireita:
	walk_fast_up
	face_right
	step_end

Unova_ChampionsRoomEntrance_Movement_SombraSobeEOlhaEsquerda:
	walk_fast_up
	face_left
	step_end

Unova_ChampionsRoomEntrance_Movement_JogadorContorna:
	walk_fast_right
	walk_fast_right
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_left
	walk_fast_left
	face_down
	step_end

Unova_ChampionsRoomEntrance_Text_SombrasChegam::
	.string "???: You! Don't\n"
	.string "take another step!$"

Unova_ChampionsRoomEntrance_Text_SombrasSeApresentam::
	.string "SHADOW: You've been a thorn in\n"
	.string "the side of our SAGEs…\p"
	.string "SHADOW: And we will not permit\n"
	.string "you to jeopardize our plan\l"
	.string "further…\p"
	.string "SHADOW: We will take care of you\n"
	.string "right here and now!$"

Unova_ChampionsRoomEntrance_Text_MetagrossAtaca::
	.string "???: Hold it!\p"
	.string "METAGROSS, IRON HEAD!$"

Unova_ChampionsRoomEntrance_Text_JuniperChega::
	.string "JUNIPER: Whatever you've got\n"
	.string "planned, it stops now!$"

Unova_ChampionsRoomEntrance_Text_PlanoDasSombras::
	.string "You may have gotten the jump on\n"
	.string "me before, but I have no\l"
	.string "intention of letting you control\l"
	.string "me again!\p"
	.string "SHADOW: Foolish woman, we have\n"
	.string "no need for you. The true king\l"
	.string "of TEAM PLASMA has already\l"
	.string "risen!\p"
	.string "SHADOW: That's right! We've used\n"
	.string "the MIND LINK you so graciously\l"
	.string "brought for us to bring back our\l"
	.string "king!\p"
	.string "SHADOW: By fusing his mind with\n"
	.string "our most powerful artificial\l"
	.string "POKéMON, our king will be\l"
	.string "unstoppable!\p"
	.string "SHADOW: That's right! GHETSIS\n"
	.string "has risen again!\p"
	.string "Lord GHETSIS will once again\n"
	.string "become the king of TEAM PLASMA,\l"
	.string "and soon, all of UNOVA!$"

Unova_ChampionsRoomEntrance_Text_PrecisamosParar::
	.string "JUNIPER: What?! You-you fused\n"
	.string "him with a POKéMON?\p"
	.string "That's insane! There's no way\n"
	.string "that thing could be stable!\p"
	.string "{PLAYER}! We've got to stop this\n"
	.string "thing before it gets out and\l"
	.string "starts causing trouble!$"

Unova_ChampionsRoomEntrance_Text_SegurarAsSombras::
	.string "SHADOW: We will not allow you to\n"
	.string "disturb our plans any further!\p"
	.string "SHADOW: We will hold you both\n"
	.string "while our king reclaims his\l"
	.string "rightful place as the ruler of\l"
	.string "UNOVA!\p"
	.string "JUNIPER: Don't underestimate me!\p"
	.string "I'm plenty strong enough to\n"
	.string "handle all three of you.\p"
	.string "{PLAYER}, quickly!$"

Unova_ChampionsRoomEntrance_Text_DeixeMeCurar::
	.string "Here, let me heal your party.$"

Unova_ChampionsRoomEntrance_Text_VaDepressa::
	.string "{PLAYER}, you've got to stop\n"
	.string "whatever thing they've created\l"
	.string "in there.\p"
	.string "I'll hold them off. Go, quickly!$"
