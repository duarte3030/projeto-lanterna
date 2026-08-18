@ CelestialTower1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ >>> B6 Unova, Fase B (portada a mao em 18/08/2026, autorizacao da condutora) >>>
@ `CelestialTowerSkylaScript` da fonte, inteiro. `checkcode VAR_FACING` ->
@ `specialvar VAR_RESULT, GetPlayerFacingDirection` (mesmo molde ja usado em
@ LavaridgeTown/scripts.inc:199-201 e FiveIsland_RocketWarehouse_Frlg).
@ `playsound SFX_ENTER_DOOR` + `waitsfx` -> `playse SE_DOOR` + `waitse`
@ (mesma traducao ja usada em Unova_ChampionsRoom/scripts.inc). `disappear` ->
@ `removeobject` no localid (so nesta visita: sem FLAG_ dedicada pra SKYLA
@ aqui, ela reaparece se o jogador sair e voltar na torre; consertar exige
@ flag nova, fora desta autorizacao). `setmapscene MISTRALTON_CITY,
@ SCENE_FINISHED` -> `setvar VAR_UNOVA_MISTRALTON_CENA, 1` (var nova,
@ VAR_UNUSED_0x417D, autorizada pela condutora em 18/08/2026; ver
@ include/constants/vars.h e a tabela do PLANO-OBRAS-UNOVA.md).
@ Rota da SKYLA conferida contra data/layouts/Unova_CelestialTower1F/map.bin:
@ (5,6)->DOWNx5 e (5,6)->LEFT->(4,6)->DOWNx5, colisao 0 nas duas.
Unova_CelestialTower1F_MapScripts::
	.byte 0

Unova_CelestialTower1F_EventScript_Npc0::
	lock
	faceplayer
	msgbox Unova_CelestialTower1F_Text_CelestialTowerSkylaText, MSGBOX_DEFAULT
	closemessage
	specialvar VAR_RESULT, GetPlayerFacingDirection
	goto_if_eq VAR_RESULT, DIR_NORTH, Unova_CelestialTower1F_EventScript_SkylaRodeia
	applymovement 1, Unova_CelestialTower1F_Movement_SkylaSai
	waitmovement 0
	goto Unova_CelestialTower1F_EventScript_SkylaFim

Unova_CelestialTower1F_EventScript_SkylaRodeia::
	applymovement 1, Unova_CelestialTower1F_Movement_SkylaRodeiaESai
	waitmovement 0

Unova_CelestialTower1F_EventScript_SkylaFim::
	playse SE_DOOR
	waitse
	removeobject 1
	setvar VAR_UNOVA_MISTRALTON_CENA, 1
	release
	end

Unova_CelestialTower1F_Movement_SkylaSai:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Unova_CelestialTower1F_Movement_SkylaRodeiaESai:
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end
@ <<< B6 Unova, Fase B <<<

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
