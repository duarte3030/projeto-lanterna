@ O Distortion World em 2D, com gravidade normal.
@
@ A grade 2D do Platinum para MAP_HEADER_DISTORTION_WORLD_GIRATINA_ROOM tem
@ SEIS tiles ocupados e nenhum chao: a geometria de verdade e o modelo 3D com
@ gravidade variavel, que este motor nao tem. O tamanho e a coluna do corredor
@ vem da fonte; o piso e invencao declarada (dev_scripts/distortion_world.py).
@ Os outros nove andares NAO foram desenhados de proposito: seria desenhar, e
@ nao converter.
@
@ ponytail: o Giratina e object_event e nao bg_event, ao contrario do Dialga e
@ do Palkia do Spear Pillar. A diferenca nao e gosto: graphics/pokemon/giratina
@ TEM overworld.png, entao o sprite existe nesta build, e so objeto SOLIDO
@ prova a trava (o jogador para um tile antes dele). Foi por nao existir sprite
@ que o Dialga virou placa.

DistortionWorld_MapScripts::
	.byte 0

@ LOCALID_DISTORTION_WORLD_GIRATINA nao e declarado aqui de proposito: quem o
@ declara e o mapjson, a partir do campo `local_id` do map.json. Um `.set` ao
@ lado disso vira `.set 1, 1` depois do pre-processador e o `as` responde
@ "expected symbol name" (medido em 21/08/2026). O WhirlIslands_LugiaChamber
@ declara porque os objetos DELE nao tem `local_id` no map.json.

DistortionWorld_EventScript_Giratina::
	lockall
	playmoncry SPECIES_GIRATINA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	setwildbattle SPECIES_GIRATINA, 47
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, DistortionWorld_EventScript_GiratinaSumiu
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, DistortionWorld_EventScript_GiratinaSumiu
	releaseall
	end

@ ponytail: so some em vitoria ou captura, a mesma regra que o
@ SpearPillar_Dialga ja escreveu. Fugir, perder ou ser teleportado deixa o
@ Giratina onde esta, senao uma Poke Ball errada apagaria o lendario do save.
DistortionWorld_EventScript_GiratinaSumiu::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DISTORTION_WORLD_GIRATINA
	setflag FLAG_HIDE_GIRATINA
	fadescreenswapbuffers FADE_FROM_BLACK
	releaseall
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
DistortionWorld_EventScript_DexGiratinaAltered::
	lockall
	msgbox DistortionWorld_Text_DexGiratinaAlteredIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GIRATINA_ALTERED, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GIRATINA_ALTERED, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GIRATINA_ALTERED
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, DistortionWorld_EventScript_DexGiratinaAlteredSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, DistortionWorld_EventScript_DexGiratinaAlteredSome
	releaseall
	end

DistortionWorld_EventScript_DexGiratinaAlteredSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GIRATINA_ALTERED
	setflag FLAG_HIDE_DEX_GIRATINA_ALTERED
	fadescreenswapbuffers FADE_FROM_BLACK
	return

DistortionWorld_Text_DexGiratinaAlteredIntro:
	.string "GIRATINA_ALTERED appeared!$"

@ <<< Dex completa <<<
