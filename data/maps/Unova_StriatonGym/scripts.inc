@ StriatonGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_StriatonGym_MapScripts::
	.byte 0

Unova_StriatonGym_EventScript_Placa2::
	msgbox Unova_StriatonGym_Text_StriatonGymPressSwitchText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa3::
	msgbox Unova_StriatonGym_Text_Waiter1StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa4::
	msgbox Unova_StriatonGym_Text_Waiter2StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa5::
	msgbox Unova_StriatonGym_Text_Waitress1StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa6::
	msgbox Unova_StriatonGym_Text_Waitress1StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa7::
	msgbox Unova_StriatonGym_Text_Waitress2StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa8::
	msgbox Unova_StriatonGym_Text_Waitress2StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa9::
	msgbox Unova_StriatonGym_Text_StriatonGymPressSwitchText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa10::
	msgbox Unova_StriatonGym_Text_StriatonGymTableNothingText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa11::
	msgbox Unova_StriatonGym_Text_StriatonGymTableNothingText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_CILAN, Unova_StriatonGym_Text_CilanGymIntroText, Unova_StriatonGym_Text_CilanWinLossText, Unova_StriatonGym_EventScript_Insignia0
	end

Unova_StriatonGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_STRIATON
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_StriatonGym_EventScript_Npc1::
	msgbox Unova_StriatonGym_Text_StriatonGymGuyText, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc2::
	msgbox Unova_StriatonGym_Text_StriatonGymBartender1Text, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc3::
	msgbox Unova_StriatonGym_Text_StriatonGymBartender2Text, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc4::
	msgbox Unova_StriatonGym_Text_Waiter1StriatonGymAfterText, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc5::
	msgbox Unova_StriatonGym_Text_Waiter2StriatonGymAfterText, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc6::
	msgbox Unova_StriatonGym_Text_Waitress1StriatonGymAfterText, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc7::
	msgbox Unova_StriatonGym_Text_Waitress2StriatonGymAfterText, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc8::
	msgbox Unova_StriatonGym_Text_StriatonGymBartender2Text, MSGBOX_NPC
	end


Unova_StriatonGym_Text_StriatonGymPressSwitchText::
	.string "A secret switch!"
	.string "\nLet's press it!$"

Unova_StriatonGym_Text_Waiter1StriatonGymSeenText::
	.string "Aha! You thought"
	.string "\nthere was a switch"
	.string "\pin here, but it"
	.string "\nwas me!$"

Unova_StriatonGym_Text_Waiter2StriatonGymSeenText::
	.string "Aha! I'm a WAITER"
	.string "\nwho's also a POKé-"
	.string "\lMON trainer!$"

Unova_StriatonGym_Text_Waitress1StriatonGymSeenText::
	.string "Welcome! Would you"
	.string "\nlike a water with"
	.string "\lyour battle?$"

Unova_StriatonGym_Text_Waitress2StriatonGymSeenText::
	.string "Battling makes us"
	.string "\nthirsty, right?"
	.string "\pIf you can win"
	.string "\nagainst me, I'll"
	.string "\lgive you a drink!$"

Unova_StriatonGym_Text_StriatonGymTableNothingText::
	.string "There's nothing"
	.string "\nunderneath.$"

Unova_StriatonGym_Text_CilanGymIntroText::
	.string "Welcome to the"
	.string "\nSTRIATON CITY"
	.string "\lPOKéMON GYM."
	.string "\pMy grass POKéMON"
	.string "\nand I have taken"
	.string "\pthe resolve to"
	.string "\nrun this GYM."
	.string "\pSo, no hard"
	.string "\nfeelings, we'll"
	.string "\pbattle whatever"
	.string "\ncomes our way.$"

Unova_StriatonGym_Text_CilanWinLossText::
	.string "Er… Is it over"
	.string "\nnow?$"

Unova_StriatonGym_Text_StriatonGymGuyText::
	.string "Yo, challenger!"
	.string "\pCILAN is the"
	.string "\nleader of this"
	.string "\lGYM. Find the"
	.string "\phidden switches"
	.string "\nto open his door."
	.string "\pHe's going to be"
	.string "\ntough without my"
	.string "\ladvice."
	.string "\pLet's see…"
	.string "\nCILAN's POKéMON"
	.string "\pare all grass"
	.string "\ntype. They have"
	.string "\pmany weaknesses,"
	.string "\nbut also many"
	.string "\lstrengths."
	.string "\pFire and flying"
	.string "\nwould be your best"
	.string "\lbets!$"

Unova_StriatonGym_Text_StriatonGymBartender1Text::
	.string "Welcome to the"
	.string "\nSTRIATON CITY GYM."
	.string "\pIf you want to"
	.string "\nreach the LEADER,"
	.string "\pyou'll need to"
	.string "\nfind the three"
	.string "\psecret switches"
	.string "\nin the gym."
	.string "\pTry checking under"
	.string "\nthe tables.$"

Unova_StriatonGym_Text_StriatonGymBartender2Text::
	.string "Welcome to the"
	.string "\nSTRIATON CITY GYM."
	.string "\pOh? Did you think"
	.string "\nI have one of the"
	.string "\lsecret switches?$"

Unova_StriatonGym_Text_Waiter1StriatonGymAfterText::
	.string "It was kind of"
	.string "\nsmelly in that"
	.string "\lcan…$"

Unova_StriatonGym_Text_Waiter2StriatonGymAfterText::
	.string "Our specialty is"
	.string "\nthe best POKéMON"
	.string "\lbattles.$"

Unova_StriatonGym_Text_Waitress1StriatonGymAfterText::
	.string "I had a feeling"
	.string "\nyou would check"
	.string "\lunder there.$"

Unova_StriatonGym_Text_Waitress2StriatonGymAfterText::
	.string "At a place like"
	.string "\nthis, it's good to"
	.string "\lstay hydrated!$"
