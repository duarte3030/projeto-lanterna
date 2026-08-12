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
