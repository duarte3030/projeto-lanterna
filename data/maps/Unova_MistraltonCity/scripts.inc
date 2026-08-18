@ MistraltonCity do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ >>> B6 Unova, Fase B (portada a mao em 18/08/2026, autorizacao da condutora) >>>
@ `MistraltonCityBlockerScript` da fonte: na fonte e um `coord_event` gatilho
@ em (6,6) e (7,6), so ativo em SCENE_DEFAULT (valor 0). Aqui vira gatilho
@ "trigger" no map.json condicionado a VAR_UNOVA_MISTRALTON_CENA == 0 (mesmo
@ molde do trigger de Unova_UndellaTown/scripts.inc, coord_events do
@ map.json). Var nova, VAR_UNOVA_MISTRALTON_CENA = VAR_UNUSED_0x417D,
@ autorizada pela condutora em 18/08/2026 (ver include/constants/vars.h e a
@ tabela do PLANO-OBRAS-UNOVA.md); quem grava 1 e a cena da SKYLA em
@ Unova_CelestialTower1F/scripts.inc. Como o trigger so
@ dispara com a var em 0, ele para de acionar sozinho assim que a cena da
@ torre grava 1: nao precisa de flag pra "esconder" nada, o proprio
@ `var_value` do gatilho ja destrava a porta.
@ `turnobject MISTRALTONCITY_GYM_GUY, RIGHT` -> `turnobject 1, DIR_EAST`
@ (RIGHT do gen2 = leste). `applymovement PLAYER, MistraltonCityGymMovement`
@ (step DOWN, o empurrao) -> `walk_down` x1.
@ Rota conferida contra data/layouts/Unova_MistraltonCity/map.bin: (6,6),
@ (7,6), (6,7) e (7,7) todos colisao 0.
Unova_MistraltonCity_MapScripts::
	.byte 0

Unova_MistraltonCity_EventScript_Blocker::
	lockall
	turnobject 1, DIR_EAST
	msgbox Unova_MistraltonCity_Text_MistraltonCityGymGuyText, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Unova_MistraltonCity_Movement_JogadorEmpurrado
	waitmovement 0
	releaseall
	end

Unova_MistraltonCity_Movement_JogadorEmpurrado:
	walk_down
	step_end
@ <<< B6 Unova, Fase B <<<

Unova_MistraltonCity_EventScript_Placa0::
	msgbox Unova_MistraltonCity_Text_MistraltonCitySignText, MSGBOX_SIGN
	end

Unova_MistraltonCity_EventScript_Placa1::
	msgbox Unova_MistraltonCity_Text_MistraltonAirportSignText, MSGBOX_SIGN
	end

Unova_MistraltonCity_EventScript_Npc0::
	msgbox Unova_MistraltonCity_Text_MistraltonCityGymGuyText, MSGBOX_NPC
	end

Unova_MistraltonCity_EventScript_Npc4::
	msgbox Unova_MistraltonCity_Text_MistraltonCityOfficerText, MSGBOX_NPC
	end

Unova_MistraltonCity_EventScript_Npc5::
	msgbox Unova_MistraltonCity_Text_MistraltonCityYoungsterText, MSGBOX_NPC
	end

Unova_MistraltonCity_EventScript_Npc6::
	msgbox Unova_MistraltonCity_Text_MistraltonCityTeacherText, MSGBOX_NPC
	end

Unova_MistraltonCity_EventScript_Npc7::
	msgbox Unova_MistraltonCity_Text_MistraltonCityTwinText, MSGBOX_NPC
	end


Unova_MistraltonCity_Text_MistraltonCitySignText::
	.string "MISTRALTON CITY."
	.string "\pThe city where"
	.string "\nwinds gather the"
	.string "\lflowers.$"

Unova_MistraltonCity_Text_MistraltonAirportSignText::
	.string "MISTRALTON CITY"
	.string "\nAIRPORT.$"

Unova_MistraltonCity_Text_MistraltonCityGymGuyText::
	.string "Oh, are you here"
	.string "\nto challenge the"
	.string "\lGYM LEADER?"
	.string "\pSorry, she's not"
	.string "\nin right now."
	.string "\pI think she may"
	.string "\nhave gone off to"
	.string "\lCELESTIAL TOWER,"
	.string "\lup on ROUTE 7.$"

Unova_MistraltonCity_Text_MistraltonCityOfficerText::
	.string "MISTRALTON CITY"
	.string "\nhas the biggest"
	.string "\lairport in UNOVA.$"

Unova_MistraltonCity_Text_MistraltonCityYoungsterText::
	.string "I love airplanes!"
	.string "\nI want to be a"
	.string "\ppilot when I grow"
	.string "\nup, just like"
	.string "\lMiss SKYLA!$"

Unova_MistraltonCity_Text_MistraltonCityTeacherText::
	.string "We can grow crops"
	.string "\nin the greenhouses"
	.string "\lall year long!"
	.string "\pWe export them all"
	.string "\nover UNOVA.$"

Unova_MistraltonCity_Text_MistraltonCityTwinText::
	.string "I love playing in"
	.string "\nthe puddles!$"
