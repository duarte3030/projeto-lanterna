@ Treinadores de rota de Route39, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route39_MapScripts::
	.byte 0

Route39_EventScript_Eugene::
	trainerbattle_single TRAINER_JOHTO_EUGENE, Route39_Text_EugeneSeen, Route39_Text_EugeneBeaten
	msgbox Route39_Text_EugeneAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Derek::
	trainerbattle_single TRAINER_JOHTO_DEREK, Route39_Text_DerekSeen, Route39_Text_DerekBeaten
	msgbox Route39_Text_DerekAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Ruth::
	trainerbattle_single TRAINER_JOHTO_RUTH, Route39_Text_RuthSeen, Route39_Text_RuthBeaten
	msgbox Route39_Text_RuthAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Norman::
	trainerbattle_single TRAINER_JOHTO_NORMAN, Route39_Text_NormanSeen, Route39_Text_NormanBeaten
	msgbox Route39_Text_NormanAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Jamie::
	trainerbattle_single TRAINER_JOHTO_JAMIE, Route39_Text_JamieSeen, Route39_Text_JamieBeaten
	msgbox Route39_Text_JamieAfter, MSGBOX_AUTOCLOSE
	end

Route39_Text_EugeneSeen:
	.string "I just got back to OLIVINE.\p"
	.string "So how about a POKéMON battle?$"

Route39_Text_EugeneBeaten:
	.string "Awaaargh!$"

Route39_Text_EugeneAfter:
	.string "My POKéMON were caught and\n"
	.string "raised overseas.\p"
	.string "They're my companions on\n"
	.string "those long voyages.$"

Route39_Text_DerekSeen:
	.string "This is a good time to brag\n"
	.string "about my PIKACHU!$"

Route39_Text_DerekBeaten:
	.string "I had no time to show off\n"
	.string "PIKACHU…$"

Route39_Text_DerekAfter:
	.string "I'm not listening to your\n"
	.string "bragging!\p"
	.string "We POKé FANS have a policy\n"
	.string "of not listening to bragging!$"

Route39_Text_RuthSeen:
	.string "Such darling POKéMON.\p"
	.string "Let's show our POKéMON\n"
	.string "together at the same time.$"

Route39_Text_RuthBeaten:
	.string "I don't mind losing.$"

Route39_Text_RuthAfter:
	.string "Do you know about baby\n"
	.string "POKéMON?\p"
	.string "I bet they're just adorable!$"

Route39_Text_NormanSeen:
	.string "Let me see what your\n"
	.string "POKéMON are capable of.$"

Route39_Text_NormanBeaten:
	.string "Ooh, your POKéMON have\n"
	.string "potential.$"

Route39_Text_NormanAfter:
	.string "You know how POKéMON have\n"
	.string "different abilities?\p"
	.string "People are like that too.\n"
	.string "Everyone has different\l"
	.string "potential.$"

Route39_Text_JamieSeen:
	.string "You came at just the right\n"
	.string "time.\p"
	.string "Let's battle.$"

Route39_Text_JamieBeaten:
	.string "Oh, how disappointing…$"

Route39_Text_JamieAfter:
	.string "I met UMBREON at night right\n"
	.string "here on ROUTE 39.\p"
	.string "I'm not sure why, but it\n"
	.string "seems to like it when I\l"
	.string "train here.\p"
	.string "It seems to become friendlier\n"
	.string "by training here than\l"
	.string "anywhere else.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route39_EventScript_Sign1::
	lock
	msgbox Route39_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

Route39_EventScript_Sign2::
	lock
	msgbox Route39_Text_MoomooFarmSign, MSGBOX_SIGN
	closemessage
	release
	end

Route39_EventScript_Sign3::
	lock
	msgbox Route39_Text_TrainerTips, MSGBOX_SIGN
	closemessage
	release
	end

Route39_Text_MoomooFarmSign::
	.string "MOOMOO FARM\p"
	.string "Enjoy Our Fresh and Tasty Milk$"

Route39_Text_Sign::
	.string "ROUTE 39\p"
	.string "OLIVINE CITY - ECRUTEAK CITY$"

Route39_Text_TrainerTips::
	.string "TRAINER TIPS\p"
	.string "Use HEADBUTT on trees to shake\n"
	.string "POKéMON out.\p"
	.string "Different kinds of POKéMON\n"
	.string "drop out of trees.\p"
	.string "Use HEADBUTT on any tree\n"
	.string "you see!$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route39_EventScript_Woman::
	lock
	faceplayer
	msgbox Route39_Text_Woman, MSGBOX_DEFAULT
	closemessage
	release
	end

Route39_Text_Woman::
	.string "That shadow... Maybe it was a giant\n"
	.string "PIDGEY?$"

@ >>> B6 Johto: cena portada do hns (porta_cenas_johto.py) >>>
@ o BAOBA e a escolha entre LUGIA e HO-OH, que arma o arco inteiro
.set LOCALID_ROUTE39_R39_BAOBA, 2

Route39_EventScript_ChooseLegend::
	msgbox Route39_Text_ChooseLegend, MSGBOX_DEFAULT
	multichoice 20, 8, MULTI_JOHTO_GOLD_SILVER, FALSE
	switch VAR_RESULT
	case 0, Route39_EventScript_LegendaryTriggerGold
	case 1, Route39_EventScript_LegendaryTriggerSilver
	case MULTI_B_PRESSED, Route39_EventScript_ChooseLegend
	release
	end

Route39_EventScript_LegendaryTrigger::
	lock
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_ROUTE39_R39_BAOBA, Common_Movement_QuestionMark
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_QuestionMark
	turnobject LOCALID_ROUTE39_R39_BAOBA DIR_SOUTH
	turnobject OBJ_EVENT_ID_PLAYER DIR_SOUTH
	delay 60

	getplayerxy VAR_TEMP_0, VAR_TEMP_1

	call_if_eq VAR_TEMP_1, 20, Route39_EventScript_BaobaMovement1
	call_if_eq VAR_TEMP_1, 21, Route39_EventScript_BaobaMovement2
	call_if_eq VAR_TEMP_1, 22, Route39_EventScript_BaobaMovement3
	call_if_eq VAR_TEMP_1, 23, Route39_EventScript_BaobaMovement4

	turnobject LOCALID_ROUTE39_R39_BAOBA DIR_EAST
	turnobject OBJ_EVENT_ID_PLAYER, DIR_WEST
	goto Route39_EventScript_ChooseLegend

Route39_EventScript_LegendaryTriggerGold::
	setvar VAR_LUGIA_OR_HOOH, 2
	goto Route39_EventScript_BaobaIntro

Route39_EventScript_LegendaryTriggerSilver::
	setvar VAR_LUGIA_OR_HOOH, 1
	goto Route39_EventScript_BaobaIntro

Route39_Text_ChooseLegend::
	.string "BAOBA: GOOD HEAVENS! Did that\n"
	.string "shadow belong to a POKéMON?\p"
	.string "Did you get a good look at it?\n"
	.string "I can't tell what color it was...$"

Route39_EventScript_BaobaMovement1::
	applymovement LOCALID_ROUTE39_R39_BAOBA, Route39_Movement_Baoba1
	waitmovement 0
	return

Route39_EventScript_BaobaMovement2::
	applymovement LOCALID_ROUTE39_R39_BAOBA, Route39_Movement_Baoba2
	waitmovement 0
	return

Route39_EventScript_BaobaMovement3::
	applymovement LOCALID_ROUTE39_R39_BAOBA, Route39_Movement_Baoba3
	waitmovement 0
	return

Route39_EventScript_BaobaMovement4::
	applymovement LOCALID_ROUTE39_R39_BAOBA, Route39_Movement_Baoba4
	waitmovement 0
	return

Route39_EventScript_BaobaIntro::
	msgbox Route39_Text_BaobaIntro, MSGBOX_DEFAULT
	msgbox Route39_Text_Registered, MSGBOX_DEFAULT
	waitse
	msgbox Route39_Text_WillCall, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE39_R39_BAOBA, Route39_Movement_BaobaLeave
	waitmovement 0
	setflag FLAG_ENABLE_BAOBA_MATCH_CALL
	removeobject LOCALID_ROUTE39_R39_BAOBA
	release
	end

Route39_Movement_Baoba1::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	step_end

Route39_Movement_Baoba2::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	step_end

Route39_Movement_Baoba3::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	step_end

Route39_Movement_Baoba4::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	step_end

Route39_Movement_BaobaLeave::
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Route39_Text_BaobaIntro::
	.string "How strange...\p"
	.string "...Ohh!\n"
	.string "What you are holding is...\l"
	.string "what they call... a POKéDEX!\p"
	.string "Haven't seen one of those in ages.\p"
	.string "My name is BAOBA!\n"
	.string "I used to run a SAFARI ZONE in\l"
	.string "FUCHSIA CITY, but it was becoming\l"
	.string "out of date with new entertainment\l"
	.string "options coming out.\p"
	.string "I decided to go overseas to learn\n"
	.string "the newest technology and open a\l"
	.string "state-of-the-art SAFARI ZONE\l"
	.string "in CIANWOOD.\p"
	.string "It may be more than a coincidence\n"
	.string "that we are chatting.\p"
	.string "Why don't we register each other's\n"
	.string "numbers in the POKéGEAR?\p"
	.string "I can give you a call once the\n"
	.string "SAFARI ZONE is open before I call\l"
	.string "anyone else!$"

Route39_Text_Registered::
	.string "{PLAYER} registered BAOBA\n"
	.string "in the POKéGEAR!$"

Route39_Text_WillCall::
	.string "BAOBA: I'll let you know\n"
	.string "on the POKéGEAR soon!$"

@ <<< B6 Johto: cena portada do hns <<<
