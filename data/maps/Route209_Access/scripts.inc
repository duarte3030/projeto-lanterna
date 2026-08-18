Route209_Access_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ S5: rotulo da fonte Route209GateToHearthomeCity_CoordEvent_Rival. O
@ gatilho so dispara com VAR_SINNOH_R209_PORTAO_HEARTHOME==1, e quem grava
@ esse 1 (e revela LOCALID_ROUTE209_ACCESS_RIVAL, ClearFlag na fonte) e o
@ script de vitoria do lider de Hearthome (decisao 2 do Gui: fiacao de cena
@ de fecho de lider, nao polimento de time; feito nesta onda 4).
@ DESBLOQUEADO em 18/08/2026: TRAINER_SINNOH_RIVAL_ROUTE_209_TURTWIG/
@ _CHIMCHAR/_PIPLUP (2511-2513, ids pre-atribuidos pela condutora) ja
@ existem. Molde igual ao de Route203_EventScript_CoordEvent_Rival: `switch
@ VAR_STARTER_MON`, `trainerbattle_no_intro` com `setvar VAR_LAST_TALKED`
@ manual (emboscada por coordevent, nao clique em objeto), `setflag` ANTES
@ do `removeobject` no fecho (senao o objeto renasce na proxima entrada).
@ Simplificacao igual a de Route203: a fonte ramifica a aproximacao em 5
@ (uma por tile do gatilho, z5 a z9) com um passo de walk por variante; sem
@ colisao no NPC os 5 colapsam num so, e os 5 coord_events do map.json (S1)
@ ja apontam todos para este mesmo rotulo.
Route209_Access_EventScript_CoordEvent_Rival::
	lockall
	applymovement LOCALID_ROUTE209_ACCESS_RIVAL, Route209_Access_Movement_RivalNoticePlayer
	waitmovement 0
	msgbox Route209_Access_Text_RivalLetsGetTheShowStarted, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_ROUTE209_ACCESS_RIVAL
	call_if_eq VAR_STARTER_MON, 0, Route209_Access_EventScript_RivalBattleTurtwig
	call_if_eq VAR_STARTER_MON, 1, Route209_Access_EventScript_RivalBattleChimchar
	call_if_eq VAR_STARTER_MON, 2, Route209_Access_EventScript_RivalBattlePiplup
	setflag FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_ROUTE_209_GATE_RIVAL
	removeobject LOCALID_ROUTE209_ACCESS_RIVAL
	setvar VAR_SINNOH_R209_PORTAO_HEARTHOME, 2
	releaseall
	end

Route209_Access_EventScript_RivalBattleTurtwig::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_ROUTE_209_TURTWIG, Route209_Access_Text_RivalMyStrategyDoesntWork
	return

Route209_Access_EventScript_RivalBattleChimchar::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_ROUTE_209_CHIMCHAR, Route209_Access_Text_RivalMyStrategyDoesntWork
	return

Route209_Access_EventScript_RivalBattlePiplup::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_ROUTE_209_PIPLUP, Route209_Access_Text_RivalMyStrategyDoesntWork
	return

Route209_Access_Movement_RivalNoticePlayer:
	delay_8
	emote_exclamation_mark
	delay_8
	step_end

Route209_Access_Text_RivalLetsGetTheShowStarted:
	.string "BARRY: Ta-daah!\p"
	.string "Kept me waiting again, {PLAYER}!\p"
	.string "Let's see how much tougher you and I\n"
	.string "have gotten, right here and now!\p"
	.string "No whining! No waiting!\n"
	.string "Let's get the show started!$"

Route209_Access_Text_RivalMyStrategyDoesntWork:
	.string "BARRY: Waaah!\p"
	.string "I guess my surefire winning strategy\n"
	.string "doesn't work after all...\p"
	.string "Anyway! I'm off to Solaceon Town!\n"
	.string "See ya, {PLAYER}!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route209_Access_EventScript_Npc1::
	msgbox Route209_Access_Text_Npc1, MSGBOX_NPC
	end

Route209_Access_Text_Npc1:
	.string "There's a wrecked stone pillar up\nahead.\pI wonder what it is?\nIt's got me very curious.$"
