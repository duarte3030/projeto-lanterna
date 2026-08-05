@ CelestialTower1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CelestialTower1F_MapScripts::
	.byte 0

Unova_CelestialTower1F_EventScript_Npc0::
	msgbox Unova_CelestialTower1F_Text_CelestialTowerSkylaText, MSGBOX_NPC
	end

Unova_CelestialTower1F_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_NURSE_CELESTIAL_TOWER, Unova_CelestialTower1F_Text_CelestialTowerNurseIntroText, Unova_CelestialTower1F_Text_CelestialTowerNurseWinText
	end


Unova_CelestialTower1F_Text_CelestialTowerSkylaText::
	.string "Hi, I'm SKYLA!"
	.string "\nI'm the MISTRALTON"
	.string "\lCITY GYM LEADER."
	.string "\pDid you come to"
	.string "\nhonor the spirits?"
	.string "\pWhenever I'm here,"
	.string "\nI always feel so"
	.string "\lzen."
	.string "\pYou know what I"
	.string "\nmean?"
	.string "\pWhat?"
	.string "\pOh! You wanted to"
	.string "\nbattle me at the"
	.string "\lGYM?"
	.string "\pHee hee, I guess I"
	.string "\nlost track of"
	.string "\ltime. Whoops!"
	.string "\pI'd better get"
	.string "\nback to town."
	.string "\pCome by if you"
	.string "\nwant to challenge"
	.string "\lme!$"

Unova_CelestialTower1F_Text_CelestialTowerNurseIntroText::
	.string "I'm a nurse, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_CelestialTower1F_Text_CelestialTowerNurseWinText::
	.string "Ah, I see.$"
