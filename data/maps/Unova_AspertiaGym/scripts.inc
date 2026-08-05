@ AspertiaGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_AspertiaGym_MapScripts::
	.byte 0

Unova_AspertiaGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_CHEREN, Unova_AspertiaGym_Text_CherenGymIntroText, Unova_AspertiaGym_Text_CherenWinLossText, Unova_AspertiaGym_EventScript_Insignia0
	end

Unova_AspertiaGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_ASPERTIA
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_AspertiaGym_EventScript_Npc1::
	msgbox Unova_AspertiaGym_Text_AspertiaGymGuyText, MSGBOX_NPC
	end

Unova_AspertiaGym_EventScript_Npc2::
	msgbox Unova_AspertiaGym_Text_YoungsterAspertiaGymAfterText, MSGBOX_NPC
	end

Unova_AspertiaGym_EventScript_Npc3::
	msgbox Unova_AspertiaGym_Text_LassAspertiaGymAfterText, MSGBOX_NPC
	end


Unova_AspertiaGym_Text_CherenGymIntroText::
	.string "{PLAYER}! Welcome"
	.string "\nto ASPERTIA CITY"
	.string "\lPOKéMON GYM."
	.string "\pI'm grateful for"
	.string "\nyour help before,"
	.string "\pbut this is"
	.string "\ndifferent."
	.string "\pHere, I accept"
	.string "\nyour challenge as"
	.string "\pthe ASPERTIA CITY"
	.string "\nGYM LEADER."
	.string "\pLet's both do our"
	.string "\nbest and have a"
	.string "\pbattle we can be"
	.string "\nproud of.$"

Unova_AspertiaGym_Text_CherenWinLossText::
	.string "This! This is what"
	.string "\na real POKéMON"
	.string "\lbattle is!$"

Unova_AspertiaGym_Text_AspertiaGymGuyText::
	.string "Yo, challenger!"
	.string "\pCHEREN is the"
	.string "\nleader of this"
	.string "\lGYM. He teaches"
	.string "\pstudents how to"
	.string "\ntrain POKéMON."
	.string "\pHe's going to be"
	.string "\ntough without my"
	.string "\ladvice."
	.string "\pLet's see…"
	.string "\nCHEREN's POKéMON"
	.string "\pare all normal"
	.string "\ntype. Their only"
	.string "\pweakness is the"
	.string "\nfighting type.$"

Unova_AspertiaGym_Text_YoungsterAspertiaGymAfterText::
	.string "The reason he saw"
	.string "\npotential in me"
	.string "\pwas that there was"
	.string "\nno one else?"
	.string "\pNo way! Even if"
	.string "\nthat's true, I"
	.string "\pjust have to get"
	.string "\nstronger!$"

Unova_AspertiaGym_Text_LassAspertiaGymAfterText::
	.string "I have to learn"
	.string "\neven more about"
	.string "\lmy POKéMON!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd gymstatue1 do BW3G: nome do mapa + "#MON GYM"
Unova_AspertiaGym_EventScript_EstatuaGinasio::
	msgbox Unova_AspertiaGym_Text_EstatuaGinasio, MSGBOX_SIGN
	end

Unova_AspertiaGym_Text_EstatuaGinasio::
	.string "ASPERTIA CITY\n"
	.string "POKéMON GYM$"
