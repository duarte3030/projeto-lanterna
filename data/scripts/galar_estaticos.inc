@ Encontros estaticos de Galar (bloco c5 da fase de conteudo).
@ Gerado por dev_scripts/estaticos_galar.py; NAO editar a mao.
@ COMUM: uma cena por (especie, nivel, item), compartilhada por todos
@ os objetos daquele encontro, porque `removeobject` resolve
@ VAR_LAST_TALKED em tempo de execucao. UNICO: uma cena por objeto,
@ com flag propria acesa so em vitoria ou captura.

GalarEstatico_G00M09_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GENGAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GENGAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M09_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M09_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M09_O0_Some
	release
	end

GalarEstatico_G00M09_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G00M09_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M09_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SABLEYE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SABLEYE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M09_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M09_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M09_O1_Some
	release
	end

GalarEstatico_G00M09_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G00M09_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M09_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRIFBLIM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRIFBLIM, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M09_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M09_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M09_O2_Some
	release
	end

GalarEstatico_G00M09_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G00M09_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M09_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_COFAGRIGUS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_COFAGRIGUS, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M09_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M09_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M09_O3_Some
	release
	end

GalarEstatico_G00M09_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G00M09_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M09_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PALOSSAND, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PALOSSAND, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M09_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M09_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M09_O4_Some
	release
	end

GalarEstatico_G00M09_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G00M09_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M09_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MIMIKYU, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MIMIKYU, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M09_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M09_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M09_O5_Some
	release
	end

GalarEstatico_G00M09_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G00M09_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M09_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DHELMISE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DHELMISE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M09_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M09_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M09_O6_Some
	release
	end

GalarEstatico_G00M09_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G00M09_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M14_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NAGANADEL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NAGANADEL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M14_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M14_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M14_O5_Some
	release
	end

GalarEstatico_G00M14_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G00M14_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M14_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M14_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M14_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M14_O6_Some
	release
	end

GalarEstatico_G00M14_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G00M14_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G00M14_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MR_RIME, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MR_RIME, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G00M14_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G00M14_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G00M14_O7_Some
	release
	end

GalarEstatico_G00M14_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G00M14_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G01M03_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_THIEVUL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_THIEVUL, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G01M03_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G01M03_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G01M03_O0_Some
	release
	end

GalarEstatico_G01M03_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G01M03_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G03M35_O19::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_HERDIER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_HERDIER, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G03M35_O19
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G03M35_O19_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G03M35_O19_Some
	release
	end

GalarEstatico_G03M35_O19_Some::
	setflag FLAG_GALAR_ESTATICO_G03M35_O19
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G03M35_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHARJABUG, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CHARJABUG, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G03M35_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G03M35_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G03M35_O2_Some
	release
	end

GalarEstatico_G03M35_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G03M35_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G03M35_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STEENEE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_STEENEE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G03M35_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G03M35_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G03M35_O3_Some
	release
	end

GalarEstatico_G03M35_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G03M35_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G03M42_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUGTRIO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUGTRIO, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G03M42_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G03M42_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G03M42_O5_Some
	release
	end

GalarEstatico_G03M42_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G03M42_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G03M42_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_EXEGGUTOR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_EXEGGUTOR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G03M42_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G03M42_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G03M42_O6_Some
	release
	end

GalarEstatico_G03M42_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G03M42_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G03M42_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PUPITAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PUPITAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G03M42_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G03M42_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G03M42_O7_Some
	release
	end

GalarEstatico_G03M42_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G03M42_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G06M27_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_HATENNA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_HATENNA, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G06M27_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G06M27_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G06M27_O0_Some
	release
	end

GalarEstatico_G06M27_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G06M27_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G06M29_O15::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PONYTA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PONYTA, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G06M29_O15
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G06M29_O15_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G06M29_O15_Some
	release
	end

GalarEstatico_G06M29_O15_Some::
	setflag FLAG_GALAR_ESTATICO_G06M29_O15
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G06M29_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ZIGZAGOON_GALAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G06M29_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G06M29_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G06M29_O3_Some
	release
	end

GalarEstatico_G06M29_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G06M29_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G06M30_O25::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MIME_JR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MIME_JR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G06M30_O25
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G06M30_O25_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G06M30_O25_Some
	release
	end

GalarEstatico_G06M30_O25_Some::
	setflag FLAG_GALAR_ESTATICO_G06M30_O25
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G06M31_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARUMAKA_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DARUMAKA_GALAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G06M31_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G06M31_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G06M31_O4_Some
	release
	end

GalarEstatico_G06M31_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G06M31_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G08M22_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRACOVISH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRACOVISH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G08M22_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G08M22_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G08M22_O3_Some
	release
	end

GalarEstatico_G08M22_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G08M22_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G08M22_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRAGAPULT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRAGAPULT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G08M22_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G08M22_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G08M22_O4_Some
	release
	end

GalarEstatico_G08M22_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G08M22_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G08M22_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PARASECT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PARASECT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G08M22_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G08M22_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G08M22_O5_Some
	release
	end

GalarEstatico_G08M22_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G08M22_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G08M23_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRAGONITE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRAGONITE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G08M23_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G08M23_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G08M23_O4_Some
	release
	end

GalarEstatico_G08M23_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G08M23_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G08M23_O9::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MASQUERAIN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MASQUERAIN, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G08M23_O9
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G08M23_O9_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G08M23_O9_Some
	release
	end

GalarEstatico_G08M23_O9_Some::
	setflag FLAG_GALAR_ESTATICO_G08M23_O9
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G08M24_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MAGNEZONE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MAGNEZONE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G08M24_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G08M24_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G08M24_O3_Some
	release
	end

GalarEstatico_G08M24_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G08M24_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G08M24_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MAGMORTAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MAGMORTAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G08M24_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G08M24_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G08M24_O7_Some
	release
	end

GalarEstatico_G08M24_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G08M24_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

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

GalarEstatico_G37M05_O10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CALYREX, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CALYREX, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M05_O10
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M05_O10_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M05_O10_Some
	release
	end

GalarEstatico_G37M05_O10_Some::
	setflag FLAG_GALAR_ESTATICO_G37M05_O10
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M05_O20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MARSHADOW, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MARSHADOW, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M05_O20
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M05_O20_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M05_O20_Some
	release
	end

GalarEstatico_G37M05_O20_Some::
	setflag FLAG_GALAR_ESTATICO_G37M05_O20
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M05_O21::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIHILEGO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NIHILEGO, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M05_O21
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M05_O21_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M05_O21_Some
	release
	end

GalarEstatico_G37M05_O21_Some::
	setflag FLAG_GALAR_ESTATICO_G37M05_O21
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M05_O22::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BUZZWOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BUZZWOLE, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M05_O22
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M05_O22_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M05_O22_Some
	release
	end

GalarEstatico_G37M05_O22_Some::
	setflag FLAG_GALAR_ESTATICO_G37M05_O22
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M05_O23::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PHEROMOSA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PHEROMOSA, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M05_O23
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M05_O23_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M05_O23_Some
	release
	end

GalarEstatico_G37M05_O23_Some::
	setflag FLAG_GALAR_ESTATICO_G37M05_O23
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M09_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STAKATAKA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_STAKATAKA, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M09_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M09_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M09_O1_Some
	release
	end

GalarEstatico_G37M09_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G37M09_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M09_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BLACEPHALON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BLACEPHALON, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M09_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M09_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M09_O2_Some
	release
	end

GalarEstatico_G37M09_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G37M09_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M09_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STAKATAKA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_STAKATAKA, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M09_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M09_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M09_O3_Some
	release
	end

GalarEstatico_G37M09_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G37M09_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M09_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BLACEPHALON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BLACEPHALON, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M09_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M09_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M09_O4_Some
	release
	end

GalarEstatico_G37M09_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G37M09_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M09_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIHILEGO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NIHILEGO, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M09_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M09_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M09_O5_Some
	release
	end

GalarEstatico_G37M09_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G37M09_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M09_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BUZZWOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BUZZWOLE, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M09_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M09_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M09_O6_Some
	release
	end

GalarEstatico_G37M09_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G37M09_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PHEROMOSA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PHEROMOSA, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O0_Some
	release
	end

GalarEstatico_G37M11_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STAKATAKA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_STAKATAKA, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O1_Some
	release
	end

GalarEstatico_G37M11_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BLACEPHALON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BLACEPHALON, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O2_Some
	release
	end

GalarEstatico_G37M11_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NIHILEGO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NIHILEGO, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O3_Some
	release
	end

GalarEstatico_G37M11_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BUZZWOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BUZZWOLE, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O4_Some
	release
	end

GalarEstatico_G37M11_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_POIPOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_POIPOLE, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O5_Some
	release
	end

GalarEstatico_G37M11_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_POIPOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_POIPOLE, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O6_Some
	release
	end

GalarEstatico_G37M11_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_POIPOLE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_POIPOLE, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O7_Some
	release
	end

GalarEstatico_G37M11_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M11_O8::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STAKATAKA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_STAKATAKA, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M11_O8
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M11_O8_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M11_O8_Some
	release
	end

GalarEstatico_G37M11_O8_Some::
	setflag FLAG_GALAR_ESTATICO_G37M11_O8
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_VOLCANION, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_VOLCANION, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O0_Some
	release
	end

GalarEstatico_G37M18_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_YVELTAL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_YVELTAL, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O1_Some
	release
	end

GalarEstatico_G37M18_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CASTFORM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CASTFORM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O10
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O10_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O10_Some
	release
	end

GalarEstatico_G37M18_O10_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O10
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O11::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O11
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O11_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O11_Some
	release
	end

GalarEstatico_G37M18_O11_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O11
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O12::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHANDELURE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CHANDELURE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O12
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O12_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O12_Some
	release
	end

GalarEstatico_G37M18_O12_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O12
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O13::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GOURGEIST, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GOURGEIST, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O13
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O13_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O13_Some
	release
	end

GalarEstatico_G37M18_O13_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O13
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O14::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NAGANADEL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NAGANADEL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O14
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O14_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O14_Some
	release
	end

GalarEstatico_G37M18_O14_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O14
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O15::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O15
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O15_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O15_Some
	release
	end

GalarEstatico_G37M18_O15_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O15
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O16::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MR_RIME, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MR_RIME, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O16
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O16_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O16_Some
	release
	end

GalarEstatico_G37M18_O16_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O16
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O17::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MACHAMP, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MACHAMP, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O17
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O17_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O17_Some
	release
	end

GalarEstatico_G37M18_O17_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O17
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CASTFORM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CASTFORM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O18
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O18_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O18_Some
	release
	end

GalarEstatico_G37M18_O18_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O18
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O19::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O19
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O19_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O19_Some
	release
	end

GalarEstatico_G37M18_O19_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O19
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KYUREM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_KYUREM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O2_Some
	release
	end

GalarEstatico_G37M18_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZEKROM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ZEKROM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O3_Some
	release
	end

GalarEstatico_G37M18_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_RESHIRAM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_RESHIRAM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O4_Some
	release
	end

GalarEstatico_G37M18_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O5_Some
	release
	end

GalarEstatico_G37M18_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MR_RIME, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MR_RIME, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O6_Some
	release
	end

GalarEstatico_G37M18_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MACHAMP, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MACHAMP, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O7_Some
	release
	end

GalarEstatico_G37M18_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O8::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CASTFORM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CASTFORM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O8
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O8_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O8_Some
	release
	end

GalarEstatico_G37M18_O8_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O8
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M18_O9::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M18_O9
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M18_O9_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M18_O9_Some
	release
	end

GalarEstatico_G37M18_O9_Some::
	setflag FLAG_GALAR_ESTATICO_G37M18_O9
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_VIRIZION, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_VIRIZION, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O0_Some
	release
	end

GalarEstatico_G37M19_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_REGIGIGAS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_REGIGIGAS, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O1_Some
	release
	end

GalarEstatico_G37M19_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NAGANADEL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NAGANADEL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O10
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O10_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O10_Some
	release
	end

GalarEstatico_G37M19_O10_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O10
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O11::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O11
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O11_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O11_Some
	release
	end

GalarEstatico_G37M19_O11_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O11
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O12::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MR_RIME, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MR_RIME, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O12
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O12_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O12_Some
	release
	end

GalarEstatico_G37M19_O12_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O12
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O13::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MACHAMP, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MACHAMP, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O13
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O13_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O13_Some
	release
	end

GalarEstatico_G37M19_O13_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O13
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O14::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CASTFORM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CASTFORM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O14
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O14_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O14_Some
	release
	end

GalarEstatico_G37M19_O14_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O14
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O15::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O15
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O15_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O15_Some
	release
	end

GalarEstatico_G37M19_O15_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O15
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O16::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHANDELURE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CHANDELURE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O16
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O16_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O16_Some
	release
	end

GalarEstatico_G37M19_O16_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O16
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O17::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GOURGEIST, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GOURGEIST, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O17
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O17_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O17_Some
	release
	end

GalarEstatico_G37M19_O17_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O17
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NAGANADEL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NAGANADEL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O18
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O18_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O18_Some
	release
	end

GalarEstatico_G37M19_O18_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O18
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O19::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O19
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O19_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O19_Some
	release
	end

GalarEstatico_G37M19_O19_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O19
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_HEATRAN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_HEATRAN, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O2_Some
	release
	end

GalarEstatico_G37M19_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PALKIA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O3_Some
	release
	end

GalarEstatico_G37M19_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DIALGA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O4_Some
	release
	end

GalarEstatico_G37M19_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O5_Some
	release
	end

GalarEstatico_G37M19_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHANDELURE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CHANDELURE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O6_Some
	release
	end

GalarEstatico_G37M19_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GOURGEIST, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GOURGEIST, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O7_Some
	release
	end

GalarEstatico_G37M19_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O8::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NAGANADEL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NAGANADEL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O8
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O8_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O8_Some
	release
	end

GalarEstatico_G37M19_O8_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O8
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M19_O9::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M19_O9
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M19_O9_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M19_O9_Some
	release
	end

GalarEstatico_G37M19_O9_Some::
	setflag FLAG_GALAR_ESTATICO_G37M19_O9
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_LATIAS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_LATIAS, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O0_Some
	release
	end

GalarEstatico_G37M20_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_RAYQUAZA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O1_Some
	release
	end

GalarEstatico_G37M20_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CASTFORM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CASTFORM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O10
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O10_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O10_Some
	release
	end

GalarEstatico_G37M20_O10_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O10
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O11::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O11
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O11_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O11_Some
	release
	end

GalarEstatico_G37M20_O11_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O11
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O12::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CHANDELURE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CHANDELURE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O12
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O12_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O12_Some
	release
	end

GalarEstatico_G37M20_O12_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O12
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O13::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GOURGEIST, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GOURGEIST, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O13
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O13_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O13_Some
	release
	end

GalarEstatico_G37M20_O13_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O13
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O14::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NAGANADEL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NAGANADEL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O14
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O14_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O14_Some
	release
	end

GalarEstatico_G37M20_O14_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O14
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O15::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O15
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O15_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O15_Some
	release
	end

GalarEstatico_G37M20_O15_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O15
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O16::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MR_RIME, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MR_RIME, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O16
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O16_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O16_Some
	release
	end

GalarEstatico_G37M20_O16_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O16
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O17::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MACHAMP, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MACHAMP, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O17
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O17_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O17_Some
	release
	end

GalarEstatico_G37M20_O17_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O17
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CASTFORM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CASTFORM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O18
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O18_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O18_Some
	release
	end

GalarEstatico_G37M20_O18_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O18
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O19::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O19
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O19_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O19_Some
	release
	end

GalarEstatico_G37M20_O19_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O19
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GROUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GROUDON, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O2_Some
	release
	end

GalarEstatico_G37M20_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O20::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_KYOGRE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O20
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O20_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O20_Some
	release
	end

GalarEstatico_G37M20_O20_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O20
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O21::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CELEBI, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CELEBI, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O21
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O21_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O21_Some
	release
	end

GalarEstatico_G37M20_O21_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O21
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DUBWOOL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DUBWOOL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O5_Some
	release
	end

GalarEstatico_G37M20_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MR_RIME, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MR_RIME, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O6_Some
	release
	end

GalarEstatico_G37M20_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MACHAMP, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MACHAMP, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O7_Some
	release
	end

GalarEstatico_G37M20_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O8::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CASTFORM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CASTFORM, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O8
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O8_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O8_Some
	release
	end

GalarEstatico_G37M20_O8_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O8
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G37M20_O9::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GALVANTULA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GALVANTULA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G37M20_O9
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G37M20_O9_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G37M20_O9_Some
	release
	end

GalarEstatico_G37M20_O9_Some::
	setflag FLAG_GALAR_ESTATICO_G37M20_O9
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M02_O40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BLAZIKEN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BLAZIKEN, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M02_O40
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M02_O40_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M02_O40_Some
	release
	end

GalarEstatico_G38M02_O40_Some::
	setflag FLAG_GALAR_ESTATICO_G38M02_O40
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M02_O41::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SWAMPERT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SWAMPERT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M02_O41
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M02_O41_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M02_O41_Some
	release
	end

GalarEstatico_G38M02_O41_Some::
	setflag FLAG_GALAR_ESTATICO_G38M02_O41
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M02_O42::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRACOZOLT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRACOZOLT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M02_O42
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M02_O42_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M02_O42_Some
	release
	end

GalarEstatico_G38M02_O42_Some::
	setflag FLAG_GALAR_ESTATICO_G38M02_O42
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M02_O43::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ARCTOZOLT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ARCTOZOLT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M02_O43
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M02_O43_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M02_O43_Some
	release
	end

GalarEstatico_G38M02_O43_Some::
	setflag FLAG_GALAR_ESTATICO_G38M02_O43
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M02_O44::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRACOVISH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRACOVISH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M02_O44
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M02_O44_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M02_O44_Some
	release
	end

GalarEstatico_G38M02_O44_Some::
	setflag FLAG_GALAR_ESTATICO_G38M02_O44
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

GalarEstatico_G38M04_O30::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ARCTOVISH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ARCTOVISH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O30
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O30_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O30_Some
	release
	end

GalarEstatico_G38M04_O30_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O30
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O31::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_RAPIDASH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_RAPIDASH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O31
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O31_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O31_Some
	release
	end

GalarEstatico_G38M04_O31_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O31
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O32::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SLOWBRO_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SLOWBRO_GALAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O32
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O32_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O32_Some
	release
	end

GalarEstatico_G38M04_O32_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O32
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O33::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_WEEZING, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_WEEZING, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O33
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O33_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O33_Some
	release
	end

GalarEstatico_G38M04_O33_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O33
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O34::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARMANITAN_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DARMANITAN_GALAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O34
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O34_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O34_Some
	release
	end

GalarEstatico_G38M04_O34_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O34
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M04_O35::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_STUNFISK_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_STUNFISK_GALAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M04_O35
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M04_O35_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M04_O35_Some
	release
	end

GalarEstatico_G38M04_O35_Some::
	setflag FLAG_GALAR_ESTATICO_G38M04_O35
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

GalarEstatico_G38M05_O33::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEGANIUM, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MEGANIUM, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M05_O33
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M05_O33_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M05_O33_Some
	release
	end

GalarEstatico_G38M05_O33_Some::
	setflag FLAG_GALAR_ESTATICO_G38M05_O33
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M05_O34::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_TYPHLOSION, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_TYPHLOSION, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M05_O34
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M05_O34_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M05_O34_Some
	release
	end

GalarEstatico_G38M05_O34_Some::
	setflag FLAG_GALAR_ESTATICO_G38M05_O34
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M05_O35::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FERALIGATR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_FERALIGATR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M05_O35
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M05_O35_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M05_O35_Some
	release
	end

GalarEstatico_G38M05_O35_Some::
	setflag FLAG_GALAR_ESTATICO_G38M05_O35
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M05_O36::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SCEPTILE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SCEPTILE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M05_O36
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M05_O36_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M05_O36_Some
	release
	end

GalarEstatico_G38M05_O36_Some::
	setflag FLAG_GALAR_ESTATICO_G38M05_O36
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M05_O37::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_BLAZIKEN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_BLAZIKEN, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M05_O37
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M05_O37_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M05_O37_Some
	release
	end

GalarEstatico_G38M05_O37_Some::
	setflag FLAG_GALAR_ESTATICO_G38M05_O37
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M05_O38::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SWAMPERT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SWAMPERT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M05_O38
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M05_O38_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M05_O38_Some
	release
	end

GalarEstatico_G38M05_O38_Some::
	setflag FLAG_GALAR_ESTATICO_G38M05_O38
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M07_O15::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRACOZOLT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRACOZOLT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M07_O15
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M07_O15_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M07_O15_Some
	release
	end

GalarEstatico_G38M07_O15_Some::
	setflag FLAG_GALAR_ESTATICO_G38M07_O15
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M08_O28::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ARCTOZOLT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ARCTOZOLT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M08_O28
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M08_O28_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M08_O28_Some
	release
	end

GalarEstatico_G38M08_O28_Some::
	setflag FLAG_GALAR_ESTATICO_G38M08_O28
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M08_O29::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRACOVISH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRACOVISH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M08_O29
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M08_O29_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M08_O29_Some
	release
	end

GalarEstatico_G38M08_O29_Some::
	setflag FLAG_GALAR_ESTATICO_G38M08_O29
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M08_O30::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ARCTOVISH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ARCTOVISH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M08_O30
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M08_O30_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M08_O30_Some
	release
	end

GalarEstatico_G38M08_O30_Some::
	setflag FLAG_GALAR_ESTATICO_G38M08_O30
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G38M43_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_RAPIDASH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_RAPIDASH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G38M43_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G38M43_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G38M43_O2_Some
	release
	end

GalarEstatico_G38M43_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G38M43_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M02_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DRATINI, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DRATINI, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M02_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M02_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M02_O0_Some
	release
	end

GalarEstatico_G42M02_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G42M02_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M02_O13::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FLAAFFY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_FLAAFFY, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M02_O13
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M02_O13_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M02_O13_Some
	release
	end

GalarEstatico_G42M02_O13_Some::
	setflag FLAG_GALAR_ESTATICO_G42M02_O13
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M02_O14::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MARILL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MARILL, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M02_O14
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M02_O14_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M02_O14_Some
	release
	end

GalarEstatico_G42M02_O14_Some::
	setflag FLAG_GALAR_ESTATICO_G42M02_O14
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M04_O10::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PORYGON2, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PORYGON2, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M04_O10
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M04_O10_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M04_O10_Some
	release
	end

GalarEstatico_G42M04_O10_Some::
	setflag FLAG_GALAR_ESTATICO_G42M04_O10
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M04_O9::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ELECTRIKE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ELECTRIKE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M04_O9
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M04_O9_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M04_O9_Some
	release
	end

GalarEstatico_G42M04_O9_Some::
	setflag FLAG_GALAR_ESTATICO_G42M04_O9
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M05_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROSELIA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ROSELIA, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M05_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M05_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M05_O5_Some
	release
	end

GalarEstatico_G42M05_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G42M05_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M05_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_LAIRON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_LAIRON, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M05_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M05_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M05_O6_Some
	release
	end

GalarEstatico_G42M05_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G42M05_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M06_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KLINK, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_KLINK, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M06_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M06_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M06_O7_Some
	release
	end

GalarEstatico_G42M06_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G42M06_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M06_O9::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KLANG, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_KLANG, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M06_O9
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M06_O9_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M06_O9_Some
	release
	end

GalarEstatico_G42M06_O9_Some::
	setflag FLAG_GALAR_ESTATICO_G42M06_O9
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M07_O12::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DEINO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DEINO, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M07_O12
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M07_O12_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M07_O12_Some
	release
	end

GalarEstatico_G42M07_O12_Some::
	setflag FLAG_GALAR_ESTATICO_G42M07_O12
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M07_O13::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ROCKRUFF, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ROCKRUFF, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M07_O13
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M07_O13_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M07_O13_Some
	release
	end

GalarEstatico_G42M07_O13_Some::
	setflag FLAG_GALAR_ESTATICO_G42M07_O13
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M07_O14::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_FOMANTIS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_FOMANTIS, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M07_O14
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M07_O14_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M07_O14_Some
	release
	end

GalarEstatico_G42M07_O14_Some::
	setflag FLAG_GALAR_ESTATICO_G42M07_O14
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M08_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KLANG, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_KLANG, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M08_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M08_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M08_O5_Some
	release
	end

GalarEstatico_G42M08_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G42M08_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M10_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SIRFETCHD, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SIRFETCHD, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M10_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M10_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M10_O0_Some
	release
	end

GalarEstatico_G42M10_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G42M10_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M10_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PINCURCHIN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PINCURCHIN, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M10_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M10_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M10_O2_Some
	release
	end

GalarEstatico_G42M10_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G42M10_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M10_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_EISCUE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_EISCUE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M10_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M10_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M10_O3_Some
	release
	end

GalarEstatico_G42M10_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G42M10_O3
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M10_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DURALUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DURALUDON, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M10_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M10_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M10_O4_Some
	release
	end

GalarEstatico_G42M10_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G42M10_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M10_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MR_MIME, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MR_MIME, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M10_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M10_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M10_O5_Some
	release
	end

GalarEstatico_G42M10_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G42M10_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M11_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DARMANITAN_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DARMANITAN_GALAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M11_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M11_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M11_O0_Some
	release
	end

GalarEstatico_G42M11_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G42M11_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M11_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_RAICHU, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_RAICHU, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M11_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M11_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M11_O1_Some
	release
	end

GalarEstatico_G42M11_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G42M11_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M12_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_NINETALES, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_NINETALES, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M12_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M12_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M12_O0_Some
	release
	end

GalarEstatico_G42M12_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G42M12_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M12_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ELECTRODE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ELECTRODE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M12_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M12_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M12_O1_Some
	release
	end

GalarEstatico_G42M12_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G42M12_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M12_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GYARADOS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GYARADOS, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M12_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M12_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M12_O2_Some
	release
	end

GalarEstatico_G42M12_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G42M12_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M12_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CROBAT, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CROBAT, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M12_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M12_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M12_O4_Some
	release
	end

GalarEstatico_G42M12_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G42M12_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M12_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SCIZOR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_SCIZOR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M12_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M12_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M12_O5_Some
	release
	end

GalarEstatico_G42M12_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G42M12_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M13_O0::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MAWILE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MAWILE, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M13_O0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M13_O0_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M13_O0_Some
	release
	end

GalarEstatico_G42M13_O0_Some::
	setflag FLAG_GALAR_ESTATICO_G42M13_O0
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M13_O1::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ALTARIA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ALTARIA, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M13_O1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M13_O1_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M13_O1_Some
	release
	end

GalarEstatico_G42M13_O1_Some::
	setflag FLAG_GALAR_ESTATICO_G42M13_O1
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M13_O4::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GARDEVOIR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_GARDEVOIR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M13_O4
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M13_O4_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M13_O4_Some
	release
	end

GalarEstatico_G42M13_O4_Some::
	setflag FLAG_GALAR_ESTATICO_G42M13_O4
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M13_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_LUCARIO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_LUCARIO, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M13_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M13_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M13_O5_Some
	release
	end

GalarEstatico_G42M13_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G42M13_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M13_O6::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_TOGEKISS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_TOGEKISS, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M13_O6
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M13_O6_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M13_O6_Some
	release
	end

GalarEstatico_G42M13_O6_Some::
	setflag FLAG_GALAR_ESTATICO_G42M13_O6
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M13_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PORYGON_Z, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_PORYGON_Z, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M13_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M13_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M13_O7_Some
	release
	end

GalarEstatico_G42M13_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G42M13_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M14_O5::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DURALUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_DURALUDON, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M14_O5
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M14_O5_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M14_O5_Some
	release
	end

GalarEstatico_G42M14_O5_Some::
	setflag FLAG_GALAR_ESTATICO_G42M14_O5
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M14_O7::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ODDISH, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_ODDISH, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M14_O7
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M14_O7_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M14_O7_Some
	release
	end

GalarEstatico_G42M14_O7_Some::
	setflag FLAG_GALAR_ESTATICO_G42M14_O7
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M15_O18::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEOWTH_GALAR, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_MEOWTH_GALAR, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M15_O18
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M15_O18_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M15_O18_Some
	release
	end

GalarEstatico_G42M15_O18_Some::
	setflag FLAG_GALAR_ESTATICO_G42M15_O18
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M15_O2::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KOFFING, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_KOFFING, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M15_O2
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M15_O2_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M15_O2_Some
	release
	end

GalarEstatico_G42M15_O2_Some::
	setflag FLAG_GALAR_ESTATICO_G42M15_O2
	goto Common_EventScript_RemoveStaticPokemon
	end

GalarEstatico_G42M15_O3::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_CORSOLA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	seteventmon SPECIES_CORSOLA, 5
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_GALAR_ESTATICO_G42M15_O3
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GalarEstatico_G42M15_O3_Some
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalarEstatico_G42M15_O3_Some
	release
	end

GalarEstatico_G42M15_O3_Some::
	setflag FLAG_GALAR_ESTATICO_G42M15_O3
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

GalarSelvagem_APPLIN_L26::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_APPLIN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_APPLIN, 26
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

GalarSelvagem_ARROKUDA_L28::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ARROKUDA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_ARROKUDA, 28
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

GalarSelvagem_DREEPY_L26::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_DREEPY, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_DREEPY, 26
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

GalarSelvagem_GIRATINA_L70::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GIRATINA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GIRATINA, 70
	dowildbattle
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_TEMP_1
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

GalarSelvagem_GLASTRIER_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_GLASTRIER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_GLASTRIER, 80
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

GalarSelvagem_KYOGRE_L60::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_KYOGRE, 60
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

GalarSelvagem_SHAYMIN_L40::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SHAYMIN, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SHAYMIN, 40
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

GalarSelvagem_SPECTRIER_L80::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SPECTRIER, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	copyvar VAR_TEMP_1, VAR_LAST_TALKED
	setwildbattle SPECIES_SPECTRIER, 80
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

