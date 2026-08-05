@ HumilauGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_HumilauGym_MapScripts::
	.byte 0

Unova_HumilauGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_MARLON, Unova_HumilauGym_Text_MarlonGymIntroText, Unova_HumilauGym_Text_MarlonWinLossText, Unova_HumilauGym_EventScript_Insignia0
	end

Unova_HumilauGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_HUMILAU
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_HumilauGym_EventScript_Npc1::
	msgbox Unova_HumilauGym_Text_HumilauGymGuyText, MSGBOX_NPC
	end

Unova_HumilauGym_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_SWIMMER_M_HUMILAU_GYM, Unova_HumilauGym_Text_SwimmerMHumilauGymSeenText, Unova_HumilauGym_Text_SwimmerMHumilauGymBeatenText
	end

Unova_HumilauGym_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_SWIMMER_F_HUMILAU_GYM, Unova_HumilauGym_Text_SwimmerFHumilauGymSeenText, Unova_HumilauGym_Text_SwimmerFHumilauGymBeatenText
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

Unova_HumilauGym_Text_MarlonWinLossText::
	.string "Wow, sweet moves,"
	.string "\n{PLAYER}!"
	.string "\pYou've gotten"
	.string "\neven better than"
	.string "\lI expected!"
	.string "\pGo ahead, take"
	.string "\nthis. You've"
	.string "\learned it!$"

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

Unova_HumilauGym_Text_SwimmerMHumilauGymBeatenText::
	.string "When I lose, I"
	.string "\nfeel like I might"
	.string "\ljust disappear…$"

Unova_HumilauGym_Text_SwimmerFHumilauGymSeenText::
	.string "If you can beat"
	.string "\nme, you'll get to"
	.string "\pface MARLON. Don't"
	.string "\nlet your guard"
	.string "\ldown yet!$"

Unova_HumilauGym_Text_SwimmerFHumilauGymBeatenText::
	.string "How can this be?"
	.string "\nI wasn't being"
	.string "\lcareless at all!$"
