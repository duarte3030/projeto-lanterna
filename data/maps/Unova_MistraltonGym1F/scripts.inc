@ MistraltonGym1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MistraltonGym1F_MapScripts::
	.byte 0

Unova_MistraltonGym1F_EventScript_Npc4::
	msgbox Unova_MistraltonGym1F_Text_Pilot1MistraltonGym1FSeenText, MSGBOX_NPC
	end

Unova_MistraltonGym1F_EventScript_Npc5::
	msgbox Unova_MistraltonGym1F_Text_Pilot2MistraltonGym1FSeenText, MSGBOX_NPC
	end

Unova_MistraltonGym1F_EventScript_Npc6::
	msgbox Unova_MistraltonGym1F_Text_Pilot3MistraltonGym1FSeenText, MSGBOX_NPC
	end

Unova_MistraltonGym1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_LEADER_SKYLA, Unova_MistraltonGym1F_Text_SkylaGymIntroText, Unova_MistraltonGym1F_Text_SkylaWinLossText
	end

Unova_MistraltonGym1F_EventScript_Npc8::
	msgbox Unova_MistraltonGym1F_Text_MistraltonGymGuyText, MSGBOX_NPC
	end


Unova_MistraltonGym1F_Text_Pilot1MistraltonGym1FSeenText::
	.string "The strong winds"
	.string "\nrepresent the"
	.string "\pstrength of us and"
	.string "\nour GYM LEADER!$"

Unova_MistraltonGym1F_Text_Pilot2MistraltonGym1FSeenText::
	.string "Right side clear!"
	.string "\nLeft side clear!"
	.string "\pBattle flight is"
	.string "\nready for takeout!"
	.string "\pErr… I mean"
	.string "\ntakeoff!$"

Unova_MistraltonGym1F_Text_Pilot3MistraltonGym1FSeenText::
	.string "Sometimes you need"
	.string "\nto be bold, while"
	.string "\pother times you"
	.string "\nneed to be"
	.string "\pcareful. React"
	.string "\naccordingly!$"

Unova_MistraltonGym1F_Text_SkylaGymIntroText::
	.string "Hee-hee! I've been"
	.string "\nwaiting for you!"
	.string "\pDid you enjoy"
	.string "\nflying with the"
	.string "\lhelp of the fans?"
	.string "\pThey're my pride"
	.string "\nand joy!"
	.string "\pNow let's try a"
	.string "\nbattle!$"

Unova_MistraltonGym1F_Text_SkylaWinLossText::
	.string "I'm walking on"
	.string "\nair!$"

Unova_MistraltonGym1F_Text_MistraltonGymGuyText::
	.string "Yo, challenger!"
	.string "\pSKYLA is the"
	.string "\nleader of this"
	.string "\lGYM. If you want"
	.string "\pto reach her,"
	.string "\nyou'll need to use"
	.string "\lthe fans to reach"
	.string "\lthe upper floor."
	.string "\pThey're heavy, so"
	.string "\nbring a strong"
	.string "\lPOKéMON!"
	.string "\pLet's see…"
	.string "\nSKYLA's POKéMON"
	.string "\pare all flying"
	.string "\ntype. Use ELECTRIC"
	.string "\pmoves to knock"
	.string "\nthem out of the"
	.string "\lsky!"
	.string "\pRocks and ice"
	.string "\nwill work too.$"
