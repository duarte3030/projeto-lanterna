BlackthornCity_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

BlackthornCitySignText::
	.string "BLACKTHORN CITY\p"
	.string "A Quiet Mountain Retreat$"

BlackthornCity_EventScript_CitySign::
	msgbox BlackthornCitySignText, MSGBOX_SIGN
	end

BlackthornCity_EventScript_DragonsDenSign::
	msgbox BlackthornCity_Text_DragonDenSign, MSGBOX_SIGN
	end

BlackthornCity_EventScript_GymSign::
	msgbox BlackthornGymSignText, MSGBOX_SIGN
	end

BlackthornCity_EventScript_MoveHouseSign::
	msgbox BlackthornCity_Text_MoveDeletersHouseSign, MSGBOX_SIGN
	end

BlackthornCity_Text_DragonDenSign::
	.string "DRAGON'S DEN AHEAD$"

BlackthornCity_Text_MoveDeletersHouseSign::
	.string "MOVE BROS' HOUSE$"

BlackthornGymSignText::
	.string "BLACKTHORN CITY POKéMON GYM\n"
	.string "LEADER: CLAIR\p"
	.string "The Blessed User of Dragon POKéMON$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

BlackthornCity_EventScript_Youngster::
	msgbox BlackthornYoungsterText, MSGBOX_NPC
	end

BlackthornYoungsterText::
	.string "Dragon masters all come from the city\n"
	.string "of BLACKTHORN.$"

BlackthornCity_EventScript_CoolTrainerF2::
	msgbox BlackthornCooltrainerF2Text, MSGBOX_NPC
	end

BlackthornCooltrainerF2Text::
	.string "Wow, you came through the ICE PATH?\p"
	.string "You must be a real hotshot trainer!$"

BlackthornCity_EventScript_CoolTrainerF::
	msgbox BlackthornCooltrainerF1Text, MSGBOX_NPC
	end

BlackthornCooltrainerF1Text::
	.string "Are you going to make your POKéMON\n"
	.string "remember some moves?$"

BlackBeltText_VoicesInMyHead::
	.string "Arooo! Voices in my head!\p"
	.string "Huh? I'm listening to my radio!$"

BlackthornCity_EventScript_BlackBelt::
	msgbox BlackBeltText_VoicesInMyHead, MSGBOX_NPC
	end

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

BlackthornCity_EventScript_Povoa1::
	lock
	faceplayer
	msgbox BlackthornCity_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

BlackthornCity_Text_Povoa1:
	.string "DRAGON'S DEN is behind the GYM.\nOnly the clan goes down there.$"

BlackthornCity_EventScript_Povoa2::
	lock
	faceplayer
	msgbox BlackthornCity_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

BlackthornCity_Text_Povoa2:
	.string "The ICE PATH is the only way\nnorth, and it is slippery.$"

BlackthornCity_EventScript_Povoa3::
	lock
	faceplayer
	msgbox BlackthornCity_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

BlackthornCity_Text_Povoa3:
	.string "Dragon moves are answered by\nIce, and by other dragons.$"

BlackthornCity_EventScript_Povoa4::
	lock
	faceplayer
	msgbox BlackthornCity_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

BlackthornCity_Text_Povoa4:
	.string "This city sits in a crater.\nThe lava never comes up here.$"

@ <<< Povoamento: fim do bloco gerado <<<
