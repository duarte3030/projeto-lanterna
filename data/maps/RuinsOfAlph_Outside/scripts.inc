@ Treinadores de rota de RuinsOfAlph_Outside, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

RuinsOfAlph_Outside_MapScripts::
	.byte 0

RuinsOfAlph_Outside_EventScript_Stan::
	trainerbattle_single TRAINER_JOHTO_STAN, RuinsOfAlph_Outside_Text_StanSeen, RuinsOfAlph_Outside_Text_StanBeaten
	msgbox RuinsOfAlph_Outside_Text_StanAfter, MSGBOX_AUTOCLOSE
	end

RuinsOfAlph_Outside_EventScript_Nathan::
	trainerbattle_single TRAINER_JOHTO_NATHAN, RuinsOfAlph_Outside_Text_NathanSeen, RuinsOfAlph_Outside_Text_NathanBeaten
	msgbox RuinsOfAlph_Outside_Text_NathanAfter, MSGBOX_AUTOCLOSE
	end

RuinsOfAlph_Outside_Text_StanSeen:
	.string "What do you want? I'm studying--\n"
	.string "don't disturb me!$"

RuinsOfAlph_Outside_Text_StanBeaten:
	.string "Sorry…\n"
	.string "I'm frustrated by our lack of\p"
	.string "real understanding…$"

RuinsOfAlph_Outside_Text_StanAfter:
	.string "The RUINS are from about 1500\n"
	.string "years ago.\p"
	.string "Nobody knows who built them.\p"
	.string "It's also not known if the POKéMON\n"
	.string "statues have any meaning.\p"
	.string "It's all one big mystery…$"

RuinsOfAlph_Outside_Text_NathanSeen:
	.string "Hmmm… This is a strange place.$"

RuinsOfAlph_Outside_Text_NathanBeaten:
	.string "…$"

RuinsOfAlph_Outside_Text_NathanAfter:
	.string "I like thinking here.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

RuinsOfAlph_Outside_EventScript_Sign1::
	lock
	msgbox RuinsOfAlph_Outside_Text_MainSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Sign2::
	lock
	msgbox RuinsOfAlph_Outside_Text_ResearchSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Sign3::
	lock
	msgbox RuinsOfAlph_Outside_Text_MysteryChamberSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_Text_MainSign::
	.string "RUINS OF ALPH\n"
	.string "VISITORS WELCOME$"

RuinsOfAlph_Outside_Text_MysteryChamberSign::
	.string "MYSTERY STONE PANEL CHAMBER$"

RuinsOfAlph_Outside_Text_ResearchSign::
	.string "RUINS OF ALPH RESEARCH CENTER\p"
	.string "THE AUTHORITY ON THE\n"
	.string "RUINS OF ALPH$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

RuinsOfAlph_Outside_EventScript_Youngster1::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Youngster1, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_Text_Youngster1::
	.string "There are many kinds of UNOWN, so\n"
	.string "we use them for our secret codes.$"

RuinsOfAlph_Outside_EventScript_Fisher1::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Fisher1, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_Text_Fisher1::
	.string "While exploring the RUINS, we\n"
	.string "suddenly noticed an odd presence.\p"
	.string "We all got scared and ran away.\n"
	.string "You should be careful too.$"

RuinsOfAlph_Outside_EventScript_Fisher2::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Fisher2, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_Text_Fisher2::
	.string "The RUINS hide a huge secret!\p"
	.string "…I think…$"

RuinsOfAlph_Outside_EventScript_Youngster2::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Youngster2, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_Text_Youngster2::
	.string "A… H… E… A… D… Hmm…\p"
	.string "What?\p"
	.string "I'm decoding this message!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
RuinsOfAlph_Outside_EventScript_DexMoltresGalar::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexMoltresGalarIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MOLTRES_GALAR, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MOLTRES_GALAR, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MOLTRES_GALAR
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexMoltresGalarSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexMoltresGalarSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexMoltresGalarSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MOLTRES_GALAR
	setflag FLAG_HIDE_DEX_MOLTRES_GALAR
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexMoltresGalarIntro:
	.string "MOLTRES_GALAR appeared!$"

RuinsOfAlph_Outside_EventScript_DexYveltal::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexYveltalIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_YVELTAL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_YVELTAL, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_YVELTAL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexYveltalSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexYveltalSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexYveltalSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_YVELTAL
	setflag FLAG_HIDE_DEX_YVELTAL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexYveltalIntro:
	.string "YVELTAL appeared!$"

RuinsOfAlph_Outside_EventScript_DexCosmoem::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexCosmoemIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_COSMOEM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_COSMOEM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_COSMOEM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexCosmoemSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexCosmoemSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexCosmoemSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_COSMOEM
	setflag FLAG_HIDE_DEX_COSMOEM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexCosmoemIntro:
	.string "COSMOEM appeared!$"

RuinsOfAlph_Outside_EventScript_DexCalyrexIce::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexCalyrexIceIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX_ICE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX_ICE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CALYREX_ICE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexCalyrexIceSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexCalyrexIceSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexCalyrexIceSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CALYREX_ICE
	setflag FLAG_HIDE_DEX_CALYREX_ICE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexCalyrexIceIntro:
	.string "CALYREX_ICE appeared!$"

RuinsOfAlph_Outside_EventScript_DexWoChien::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexWoChienIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_WO_CHIEN, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_WO_CHIEN, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_WO_CHIEN
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexWoChienSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexWoChienSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexWoChienSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_WO_CHIEN
	setflag FLAG_HIDE_DEX_WO_CHIEN
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexWoChienIntro:
	.string "WO_CHIEN appeared!$"

RuinsOfAlph_Outside_EventScript_DexChienPao::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexChienPaoIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CHIEN_PAO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CHIEN_PAO, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CHIEN_PAO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexChienPaoSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexChienPaoSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexChienPaoSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CHIEN_PAO
	setflag FLAG_HIDE_DEX_CHIEN_PAO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexChienPaoIntro:
	.string "CHIEN_PAO appeared!$"

RuinsOfAlph_Outside_EventScript_DexTingLu::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexTingLuIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_TING_LU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_TING_LU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_TING_LU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexTingLuSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexTingLuSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexTingLuSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_TING_LU
	setflag FLAG_HIDE_DEX_TING_LU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexTingLuIntro:
	.string "TING_LU appeared!$"

RuinsOfAlph_Outside_EventScript_DexChiYu::
	lockall
	msgbox RuinsOfAlph_Outside_Text_DexChiYuIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CHI_YU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CHI_YU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CHI_YU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_Outside_EventScript_DexChiYuSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_Outside_EventScript_DexChiYuSome
	releaseall
	end

RuinsOfAlph_Outside_EventScript_DexChiYuSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CHI_YU
	setflag FLAG_HIDE_DEX_CHI_YU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_Outside_Text_DexChiYuIntro:
	.string "CHI_YU appeared!$"

@ <<< Dex completa <<<
