@ HumilauGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_HumilauGym_MapScripts::
	.byte 0

Unova_HumilauGym_EventScript_Npc0::
	msgbox Unova_HumilauGym_Text_MarlonGymIntroText, MSGBOX_NPC
	end

Unova_HumilauGym_EventScript_Npc1::
	msgbox Unova_HumilauGym_Text_HumilauGymGuyText, MSGBOX_NPC
	end

Unova_HumilauGym_EventScript_Npc2::
	msgbox Unova_HumilauGym_Text_SwimmerMHumilauGymSeenText, MSGBOX_NPC
	end

Unova_HumilauGym_EventScript_Npc3::
	msgbox Unova_HumilauGym_Text_SwimmerFHumilauGymSeenText, MSGBOX_NPC
	end


Unova_HumilauGym_Text_MarlonGymIntroText::
	.string "MARLON: {PLAYER}!"
	.string "\pHow's your"
	.string "\ntrainin' coming?"
	.string "\pYou're finally"
	.string "\nready to take"
	.string "\lon my GYM"
	.string "\lchallenge?"
	.string "\pSweet! I won't"
	.string "\nhold back,"
	.string "\l{PLAYER}!"
	.string "\pCome on!$"

Unova_HumilauGym_Text_HumilauGymGuyText::
	.string "Hey! I'm no train-"
	.string "\ner but I can give"
	.string "\lsome advice!"
	.string "\pBelieve me!"
	.string "\nIf you believe, a"
	.string "\pchampionship dream"
	.string "\ncan come true."
	.string "\pYou believe?"
	.string "\nThen listen."
	.string "\pThe fire-type is"
	.string "\nweak against the"
	.string "\pwater-type. Keep"
	.string "\nthis in mind.$"

Unova_HumilauGym_Text_SwimmerMHumilauGymSeenText::
	.string "To be as clear as"
	.string "\nwater… That is the"
	.string "\lstyle that I seek!$"

Unova_HumilauGym_Text_SwimmerFHumilauGymSeenText::
	.string "If you can beat"
	.string "\nme, you'll get to"
	.string "\pface MARLON. Don't"
	.string "\nlet your guard"
	.string "\ldown yet!$"
