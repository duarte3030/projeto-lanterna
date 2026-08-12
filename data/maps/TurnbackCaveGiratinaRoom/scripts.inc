TurnbackCaveGiratinaRoom_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TurnbackCave_OnTransitionGiratina
	.byte 0

TurnbackCaveGiratinaRoom_EventScript_Placa1::
	msgbox TurnbackCaveGiratinaRoom_Text_Placa1, MSGBOX_SIGN
	end

TurnbackCaveGiratinaRoom_Text_Placa1:
	.string "It's a portal leading to the\nDistortion World...\pWould you like to leap into the portal\nand go to the Distortion World?$"
