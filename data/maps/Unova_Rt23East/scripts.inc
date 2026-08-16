@ Rt23East do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt23East_MapScripts::
	.byte 0

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Os seis crachas: cada oficial barra a passagem ate o jogador ja ter mostrado
@ a insignia certa. `buttonsound`/`waitsfx` da fonte (o "ding" antes do texto de
@ insignia aceita) foi DESCARTADO: nao ha equivalente de SFX de confirmacao no
@ motor daqui e msgbox ja pausa por conta propria.
Unova_Rt23East_EventScript_R23Badge1Script::
	lockall
	turnobject LOCALID_PLAYER, DIR_WEST
	turnobject 1, DIR_EAST
	msgbox Unova_Rt23East_Text_R23Officer1StopText, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_BADGE_UNOVA_LENTIMAS, Unova_Rt23East_EventScript_R23Badge1SemInsignia
	msgbox Unova_Rt23East_Text_R23Officer1HaveBadgeText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R23_LESTE_CENA, 1
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge1SemInsignia::
	applymovement LOCALID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge2Script::
	lockall
	turnobject LOCALID_PLAYER, DIR_EAST
	turnobject 2, DIR_WEST
	msgbox Unova_Rt23East_Text_R23Officer2StopText, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_BADGE_UNOVA_CASTELIA, Unova_Rt23East_EventScript_R23Badge2SemInsignia
	msgbox Unova_Rt23East_Text_R23Officer2HaveBadgeText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R23_LESTE_CENA, 2
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge2SemInsignia::
	applymovement LOCALID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge3Script::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	turnobject 3, DIR_SOUTH
	msgbox Unova_Rt23East_Text_R23Officer3StopText, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_BADGE_UNOVA_VIRBANK, Unova_Rt23East_EventScript_R23Badge3SemInsignia
	msgbox Unova_Rt23East_Text_R23Officer3HaveBadgeText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R23_LESTE_CENA, 3
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge3SemInsignia::
	applymovement LOCALID_PLAYER, Common_Movement_WalkLeft
	waitmovement 0
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge4Script::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	turnobject 4, DIR_SOUTH
	msgbox Unova_Rt23East_Text_R23Officer4StopText, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_BADGE_UNOVA_ASPERTIA, Unova_Rt23East_EventScript_R23Badge4SemInsignia
	msgbox Unova_Rt23East_Text_R23Officer4HaveBadgeText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R23_LESTE_CENA, 4
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge4SemInsignia::
	applymovement LOCALID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge5Script::
	lockall
	turnobject LOCALID_PLAYER, DIR_WEST
	turnobject 5, DIR_EAST
	msgbox Unova_Rt23East_Text_R23Officer5StopText, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_BADGE_UNOVA_STRIATON, Unova_Rt23East_EventScript_R23Badge5SemInsignia
	msgbox Unova_Rt23East_Text_R23Officer5HaveBadgeText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R23_LESTE_CENA, 5
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge5SemInsignia::
	applymovement LOCALID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge6Script::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	turnobject 6, DIR_SOUTH
	msgbox Unova_Rt23East_Text_R23Officer6StopText, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_BADGE_UNOVA_MISTRALTON, Unova_Rt23East_EventScript_R23Badge6SemInsignia
	msgbox Unova_Rt23East_Text_R23Officer6HaveBadgeText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R23_LESTE_CENA, 6
	releaseall
	end

Unova_Rt23East_EventScript_R23Badge6SemInsignia::
	applymovement LOCALID_PLAYER, Common_Movement_WalkRight
	waitmovement 0
	releaseall
	end

@ R23LowerScript/R23UpperScript (fonte): `changeblock` gatilhado por
@ EVENT_R_23_LOWER, VAR_TEMP_0. Isto e Obra 2 (changeblock), e Rt23East NAO
@ esta entre os 12 mapas da fila da Obra 2 (decisao 3 do PLANO-OBRAS-UNOVA.md).
@ Sem var/flag reservada para EVENT_R_23_LOWER nesta leva, ficam como stub de
@ propósito ate essa frente rodar.
Unova_Rt23East_EventScript_R23LowerScript::
	end

Unova_Rt23East_EventScript_R23UpperScript::
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_Rt23East_EventScript_Npc0::
	msgbox Unova_Rt23East_Text_R23Officer1StopText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc1::
	msgbox Unova_Rt23East_Text_R23Officer2StopText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc2::
	msgbox Unova_Rt23East_Text_R23Officer3HaveBadgeText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc3::
	msgbox Unova_Rt23East_Text_R23Officer4HaveBadgeText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc4::
	msgbox Unova_Rt23East_Text_R23Officer5HaveBadgeText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc5::
	msgbox Unova_Rt23East_Text_R23Officer6StopText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_R23_1, Unova_Rt23East_Text_AceTrainerM1R23SeenText, Unova_Rt23East_Text_AceTrainerM1R23BeatenText
	end

Unova_Rt23East_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_R23_1, Unova_Rt23East_Text_AceTrainerF1R23SeenText, Unova_Rt23East_Text_AceTrainerF1R23BeatenText
	end


Unova_Rt23East_Text_R23Officer1StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nSPOOKYBADGE.$"

Unova_Rt23East_Text_R23Officer1HaveBadgeText::
	.string "Oh, that is the"
	.string "\nSPOOKYBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer2StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nINSECTBADGE.$"

Unova_Rt23East_Text_R23Officer2HaveBadgeText::
	.string "Oh, that is the"
	.string "\nINSECTBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer3StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nTOXICBADGE.$"

Unova_Rt23East_Text_R23Officer3HaveBadgeText::
	.string "Oh, that is the"
	.string "\nTOXICBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer4StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nBASICBADGE.$"

Unova_Rt23East_Text_R23Officer4HaveBadgeText::
	.string "Oh, that is the"
	.string "\nBASICBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer5StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nGARNISHBADGE.$"

Unova_Rt23East_Text_R23Officer5HaveBadgeText::
	.string "Oh, that is the"
	.string "\nGARNISHBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer6StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nJETBADGE.$"

Unova_Rt23East_Text_R23Officer6HaveBadgeText::
	.string "Oh, that is the"
	.string "\nJETBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_AceTrainerM1R23SeenText::
	.string "Our battle will"
	.string "\nsurely be worth a"
	.string "\ppage in the book"
	.string "\nof your journey!$"

Unova_Rt23East_Text_AceTrainerM1R23BeatenText::
	.string "If only I could've"
	.string "\nwon, I would have"
	.string "\pmade an impression"
	.string "\non you.$"

Unova_Rt23East_Text_AceTrainerF1R23SeenText::
	.string "I can see the plea"
	.string "\nin my POKéMON's"
	.string "\peyes. To fight!"
	.string "\nAnd to win!$"

Unova_Rt23East_Text_AceTrainerF1R23BeatenText::
	.string "The eyes of your"
	.string "\nPOKéMON are"
	.string "\pglimmering with"
	.string "\nstrength!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 3). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt23East_EventScript_Gruta4C2::
	goto_if_set FLAG_UNOVA_GRUTA_R23, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R23
	goto Unova_EventScript_GrutaTier3
