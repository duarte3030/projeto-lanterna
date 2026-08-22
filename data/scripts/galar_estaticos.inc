@ Encontros estaticos de Galar (bloco c5 da fase de conteudo).
@ Gerado por dev_scripts/estaticos_galar.py; NAO editar a mao.
@ COMUM: uma cena por (especie, nivel, item), compartilhada por todos
@ os objetos daquele encontro, porque `removeobject` resolve
@ VAR_LAST_TALKED em tempo de execucao. UNICO: uma cena por objeto,
@ com flag propria acesa so em vitoria ou captura.

GalarEstatico_G11M10_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MELTAN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MELTAN, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G11M10_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G11M10_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G11M10_O7_Some
	release
	end

GalarEstatico_G11M10_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G11M10_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SLOWPOKE_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SLOWPOKE_GALAR, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O2_Some
	release
	end

GalarEstatico_G38M04_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SLOWPOKE_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SLOWPOKE_GALAR, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O3_Some
	release
	end

GalarEstatico_G38M04_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SLOWPOKE_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SLOWPOKE_GALAR, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O4_Some
	release
	end

GalarEstatico_G38M04_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarSelvagem_APPLIN_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_APPLIN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_APPLIN, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_APPLIN_L22::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_APPLIN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_APPLIN, 22
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_APPLIN_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_APPLIN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_APPLIN, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_BLACEPHALON_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BLACEPHALON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_BLACEPHALON, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_BUZZWOLE_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BUZZWOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_BUZZWOLE, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CELEBI_L60::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CELEBI, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CELEBI, 60
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CELESTEELA_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CELESTEELA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CELESTEELA, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CHEWTLE_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHEWTLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CHEWTLE, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CHEWTLE_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHEWTLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CHEWTLE, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CHEWTLE_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHEWTLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CHEWTLE, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CLOBBOPUS_L18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CLOBBOPUS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CLOBBOPUS, 18
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CLOBBOPUS_L39::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CLOBBOPUS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CLOBBOPUS, 39
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CLOBBOPUS_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CLOBBOPUS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CLOBBOPUS, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_COMBEE_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_COMBEE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_COMBEE, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_COPPERAJAH_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_COPPERAJAH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_COPPERAJAH, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_COPPERAJAH_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_COPPERAJAH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_COPPERAJAH, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CORVIKNIGHT_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CORVIKNIGHT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CORVIKNIGHT, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CORVIKNIGHT_L73::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CORVIKNIGHT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CORVIKNIGHT, 73
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_COSMOEM_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_COSMOEM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_COSMOEM, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_COSMOG_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_COSMOG, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_COSMOG, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CRAMORANT_L18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CRAMORANT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CRAMORANT, 18
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CRAMORANT_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CRAMORANT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CRAMORANT, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_CRAMORANT_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CRAMORANT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_CRAMORANT, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DARKRAI_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARKRAI, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DARKRAI, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DARUMAKA_GALAR_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARUMAKA_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DARUMAKA_GALAR, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DARUMAKA_GALAR_L39::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARUMAKA_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DARUMAKA_GALAR, 39
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DARUMAKA_GALAR_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARUMAKA_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DARUMAKA_GALAR, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DARUMAKA_GALAR_L71::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARUMAKA_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DARUMAKA_GALAR, 71
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DIALGA_L70::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DIALGA, 70
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DIANCIE_L65::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DIANCIE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DIANCIE, 65
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DRAMPA_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRAMPA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DRAMPA, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DREEPY_L22::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DREEPY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DREEPY, 22
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DREEPY_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DREEPY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DREEPY, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DURALUDON_L28::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DURALUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DURALUDON, 28
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DURALUDON_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DURALUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DURALUDON, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DURALUDON_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DURALUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DURALUDON, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_DURALUDON_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DURALUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DURALUDON, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_FALINKS_L39::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FALINKS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_FALINKS, 39
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_FALINKS_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FALINKS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_FALINKS, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_FALINKS_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FALINKS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_FALINKS, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_FARFETCHD_GALAR_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FARFETCHD_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_FARFETCHD_GALAR, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_FARFETCHD_GALAR_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FARFETCHD_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_FARFETCHD_GALAR, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_FLABEBE_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FLABEBE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_FLABEBE, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_FROSMOTH_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FROSMOTH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_FROSMOTH, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GARBODOR_L25::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GARBODOR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GARBODOR, 25
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GARBODOR_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GARBODOR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GARBODOR, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GARBODOR_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GARBODOR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GARBODOR, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GIBLE_L25::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GIBLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GIBLE, 25
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GOGOAT_L25::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GOGOAT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GOGOAT, 25
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GOGOAT_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GOGOAT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GOGOAT, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GOSSIFLEUR_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GOSSIFLEUR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GOSSIFLEUR, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GUZZLORD_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GUZZLORD, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GUZZLORD, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_HOUNDOUR_L28::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_HOUNDOUR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_HOUNDOUR, 28
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_HOUNDOUR_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_HOUNDOUR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_HOUNDOUR, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_HOUNDOUR_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_HOUNDOUR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_HOUNDOUR, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_IMPIDIMP_L35::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_IMPIDIMP, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_IMPIDIMP, 35
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_KARTANA_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KARTANA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_KARTANA, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MAMOSWINE_L36::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MAMOSWINE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MAMOSWINE, 36
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MAMOSWINE_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MAMOSWINE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MAMOSWINE, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MARSHADOW_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MARSHADOW, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MARSHADOW, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MARSHADOW_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MARSHADOW, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MARSHADOW, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MELOETTA_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MELOETTA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MELOETTA, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MEOWTH_GALAR_L18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEOWTH_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MEOWTH_GALAR, 18
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MEOWTH_GALAR_L37::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEOWTH_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MEOWTH_GALAR, 37
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MEOWTH_GALAR_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEOWTH_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MEOWTH_GALAR, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MEOWTH_GALAR_L9::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEOWTH_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MEOWTH_GALAR, 9
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MEWTWO_L70::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MEWTWO, 70
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MOLTRES_GALAR_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MOLTRES_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MOLTRES_GALAR, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MORPEKO_L37::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MORPEKO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MORPEKO, 37
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MORPEKO_L39::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MORPEKO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MORPEKO, 39
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MORPEKO_L5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MORPEKO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MORPEKO, 5
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MORPEKO_L60::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MORPEKO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MORPEKO, 60
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MUDSDALE_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MUDSDALE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MUDSDALE, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MUDSDALE_L25::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MUDSDALE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MUDSDALE, 25
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_MUDSDALE_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MUDSDALE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_MUDSDALE, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NICKIT_L37::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NICKIT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NICKIT, 37
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NICKIT_L39::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NICKIT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NICKIT, 39
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NICKIT_L4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NICKIT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NICKIT, 4
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NICKIT_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NICKIT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NICKIT, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NICKIT_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NICKIT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NICKIT, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NICKIT_L73::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NICKIT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NICKIT, 73
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NIHILEGO_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIHILEGO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NIHILEGO, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_NOCTOWL_L73::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NOCTOWL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_NOCTOWL, 73
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ONIX_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ONIX, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ONIX, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ONIX_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ONIX, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ONIX, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PALKIA_L70::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PALKIA, 70
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PALOSSAND_L30::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PALOSSAND, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PALOSSAND, 30
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PALOSSAND_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PALOSSAND, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PALOSSAND, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PELIPPER_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PELIPPER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PELIPPER, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PHEROMOSA_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PHEROMOSA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PHEROMOSA, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PIDGEOT_L60::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PIDGEOT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PIDGEOT, 60
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_POIPOLE_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_POIPOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_POIPOLE, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PYROAR_L34::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PYROAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PYROAR, 34
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_PYROAR_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PYROAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_PYROAR, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_REGICE_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_REGICE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_REGICE, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_REGIROCK_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_REGIROCK, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_REGIROCK, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ROCKRUFF_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROCKRUFF, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ROCKRUFF, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ROCKRUFF_L18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROCKRUFF, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ROCKRUFF, 18
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ROCKRUFF_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROCKRUFF, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ROCKRUFF, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ROLYCOLY_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROLYCOLY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ROLYCOLY, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ROLYCOLY_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROLYCOLY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ROLYCOLY, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ROLYCOLY_L8::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROLYCOLY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ROLYCOLY, 8
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ROOKIDEE_L4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROOKIDEE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ROOKIDEE, 4
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SANDSLASH_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SANDSLASH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SANDSLASH, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SCRAGGY_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SCRAGGY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SCRAGGY, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SCRAGGY_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SCRAGGY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SCRAGGY, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SHARPEDO_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SHARPEDO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SHARPEDO, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SILICOBRA_L22::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SILICOBRA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SILICOBRA, 22
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SILICOBRA_L30::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SILICOBRA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SILICOBRA, 30
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SILICOBRA_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SILICOBRA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SILICOBRA, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SKWOVET_L4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SKWOVET, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SKWOVET, 4
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SKWOVET_L7_AGUAV_BERRY::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SKWOVET, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SKWOVET, 7, ITEM_AGUAV_BERRY
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SNOM_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SNOM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SNOM, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SNOM_L39::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SNOM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SNOM, 39
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SNOM_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SNOM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SNOM, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SNOVER_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SNOVER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SNOVER, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SNOVER_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SNOVER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SNOVER, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_SNOVER_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SNOVER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SNOVER, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_STAKATAKA_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STAKATAKA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_STAKATAKA, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_STUNFISK_GALAR_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STUNFISK_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_STUNFISK_GALAR, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_STUNFISK_GALAR_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STUNFISK_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_STUNFISK_GALAR, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_STUNFISK_GALAR_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STUNFISK_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_STUNFISK_GALAR, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_TAILLOW_L20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_TAILLOW, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_TAILLOW, 20
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_TAILLOW_L8::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_TAILLOW, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_TAILLOW, 8
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_TAPU_LELE_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_TAPU_LELE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_TAPU_LELE, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_TRAPINCH_L30::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_TRAPINCH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_TRAPINCH, 30
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_TRUBBISH_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_TRUBBISH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_TRUBBISH, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_VESPIQUEN_L10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_VESPIQUEN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_VESPIQUEN, 10
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_VESPIQUEN_L24::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_VESPIQUEN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_VESPIQUEN, 24
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_WAILORD_L50::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_WAILORD, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_WAILORD, 50
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_WOOLOO_L22::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_WOOLOO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_WOOLOO, 22
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_WOOLOO_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_WOOLOO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_WOOLOO, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_XURKITREE_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_XURKITREE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_XURKITREE, 80
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_YAMASK_GALAR_L22::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_YAMASK_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_YAMASK_GALAR, 22
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_YAMASK_GALAR_L30::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_YAMASK_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_YAMASK_GALAR, 30
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_YAMASK_GALAR_L63::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_YAMASK_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_YAMASK_GALAR, 63
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_YAMPER_L4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_YAMPER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_YAMPER, 4
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_YAMPER_L73::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_YAMPER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_YAMPER, 73
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ZERAORA_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZERAORA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ZERAORA, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ZIGZAGOON_GALAR_L4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ZIGZAGOON_GALAR, 4
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_ZIGZAGOON_GALAR_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ZIGZAGOON_GALAR, 40
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

