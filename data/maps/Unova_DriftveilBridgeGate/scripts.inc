@ DriftveilBridgeGate do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_DriftveilBridgeGate_MapScripts::
	.byte 0

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Abre a ponte sem checar cracha (irma de Unova_Rt5BridgeGate, que abre so
@ com FLAG_UNOVA_DRIFTVEIL_BLOQUEIO). `playsound SFX_ELEVATOR`+`earthquake 60`
@ -> mesma receita ja usada em Unova_VirbankComplexElevator (VAR_0x8004-0x8007
@ + `special ShakeScreen`). `setmapscene R_5_BRIDGE_GATE, SCENE_FINISHED` ->
@ setvar na var do mapa alvo (tabela do PLANO).
Unova_DriftveilBridgeGate_EventScript_DriftveilBridgeGateBridgeScript::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	msgbox Unova_DriftveilBridgeGate_Text_DriftveilBridgeGateOfficerRaiseBridgeText, MSGBOX_DEFAULT
	closemessage
	playse SE_ELEVATOR
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 0
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeScreen
	delay 60
	waitse
	msgbox Unova_DriftveilBridgeGate_Text_DriftveilBridgeGateOfficerText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_DRIFTVEIL_PORTAO_PONTE_CENA, 1
	setvar VAR_UNOVA_R5_PORTAO_PONTE_CENA, 1
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_DriftveilBridgeGate_EventScript_Npc0::
	msgbox Unova_DriftveilBridgeGate_Text_DriftveilBridgeGateOfficerText, MSGBOX_NPC
	end


Unova_DriftveilBridgeGate_Text_DriftveilBridgeGateOfficerRaiseBridgeText::
	.string "Whew! Finally got"
	.string "\nback to my post!"
	.string "\pWhat? You want to"
	.string "\ncross the bridge?"
	.string "\pHere, let me lower"
	.string "\nit for you!$"

Unova_DriftveilBridgeGate_Text_DriftveilBridgeGateOfficerText::
	.string "The BRIDGE takes"
	.string "\nyou straight to"
	.string "\lNIMBASA CITY.$"
