Route209LostTower5F_MapScripts::
	.byte 0

Route209LostTower5F_EventScript_Npc1::
	msgbox Route209LostTower5F_Text_Npc1, MSGBOX_NPC
	end

Route209LostTower5F_Text_Npc1:
	.string "Oh! The fog is gone and, with it, all\ndoubt in my heart!\pThis is my thanks.\nDon't be shy! Take it!$"

Route209LostTower5F_EventScript_Npc2::
	msgbox Route209LostTower5F_Text_Npc2, MSGBOX_NPC
	end

Route209LostTower5F_Text_Npc2:
	.string "Let me make your journey out of this\nplace less frightening. Take this.$"

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
Route209LostTower5F_EventScript_Darkrai::
	lockall
	msgbox Route209LostTower5F_Text_DarkraiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_DARKRAI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_DARKRAI, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_ROUTE209_LOST_TOWER5_F_DARKRAI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Route209LostTower5F_EventScript_DarkraiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Route209LostTower5F_EventScript_DarkraiPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
Route209LostTower5F_EventScript_DarkraiPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_ROUTE209_LOST_TOWER5_F_DARKRAI
	setflag FLAG_HIDE_DARKRAI_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Route209LostTower5F_EventScript_DarkraiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_ROUTE209_LOST_TOWER5_F_DARKRAI
	setflag FLAG_HIDE_DARKRAI_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox Route209LostTower5F_Text_DarkraiSome, MSGBOX_DEFAULT
	return

Route209LostTower5F_Text_DarkraiIntro:
	.string "A shadow with no one to cast it\nwaits at the top of the tower...$"

Route209LostTower5F_Text_DarkraiSome:
	.string "DARKRAI melted away into the\ndarkness...$"

@ <<< Lendarios de Sinnoh <<<
