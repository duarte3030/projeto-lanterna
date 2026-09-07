OlivineCity_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

OlivineCity_EventScript_CafeSign::
	msgbox OlivineCity_Text_CafeSign, MSGBOX_SIGN
	end

OlivineCity_EventScript_GymSign::
	lock
	msgbox OlivineCity_Text_GymSign, MSGBOX_SIGN
	end

OlivineCity_EventScript_LighthouseSign::
	lock
	msgbox OlivineCity_Text_LighthouseSign, MSGBOX_SIGN
	end

OlivineCity_EventScript_PortSign::
	lock
	msgbox OlivineCity_Text_PortSign, MSGBOX_SIGN
	end

OlivineCity_EventScript_Sign::
	lock
	msgbox OlivineCity_Text_Sign, MSGBOX_SIGN
	end

OlivineCity_Text_CafeSign::
	.string "OLIVINE CAFE\n"
	.string "WHERE STRONG SAILORS ENJOY\l"
	.string "HEARTY MEALS OF STRENGTH$"

OlivineCity_Text_GymSign::
	.string "OLIVINE CITY POKéMON GYM\n"
	.string "LEADER: JASMINE\p"
	.string "The Steel-Clad Defense Girl$"

OlivineCity_Text_LighthouseSign::
	.string "OLIVINE LIGHTHOUSE\n"
	.string "Also known as the GLITTER\l"
	.string "LIGHTHOUSE$"

OlivineCity_Text_PortSign::
	.string "OLIVINE PORT\n"
	.string "FAST SHIP PIER$"

OlivineCity_Text_Sign::
	.string "OLIVINE CITY\p"
	.string "The Port Closest to Foreign Lands$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

OlivineCity_EventScript_Sailor2::
	lock
	faceplayer
	msgbox OlivineCity_Text_Sailor2, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Text_Sailor2::
	.string "The league has JASMINE\n"
	.string "pegged as the sixth\l"
	.string "strongest GYM LEADER!\p"
	.string "Hah! That's a load of crud.\p"
	.string "There's no way PRYCE could\n"
	.string "hurt JASMINE's STEEL-type\l"
	.string "POKéMON!\p"
	.string "Bureaucracy if you ask me.\p"
	.string "She's something to be feared,\n"
	.string "that's for sure!$"

OlivineCity_EventScript_Sailor1::
	lock
	faceplayer
	msgbox OlivineCity_Text_Sailor1, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Text_Sailor1::
	.string "Dark roads are dangerous\n"
	.string "at night.\p"
	.string "But in the pitch-black of\n"
	.string "night, the sea is even more\l"
	.string "treacherous!\p"
	.string "Without the beacon of the\n"
	.string "LIGHTHOUSE to guide it,\l"
	.string "no ship can sail.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

OlivineCity_EventScript_Youngster::
	lock
	faceplayer
	msgbox OlivineCity_Text_YoungsterPokegear, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Text_YoungsterPokegear::
	.string "That thing you have--\n"
	.string "it's a POKéGEAR, right?\l"
	.string "Wow, that's cool.$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

OlivineCity_EventScript_Povoa1::
	lock
	faceplayer
	msgbox OlivineCity_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

OlivineCity_Text_Povoa1:
	.string "The PORT is south. Ships leave\nfor far coasts from there.$"

OlivineCity_EventScript_Povoa2::
	lock
	faceplayer
	msgbox OlivineCity_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

OlivineCity_Text_Povoa2:
	.string "The LIGHTHOUSE keeps this whole\nharbour alive at night.$"

OlivineCity_EventScript_Povoa3::
	lock
	faceplayer
	msgbox OlivineCity_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

OlivineCity_Text_Povoa3:
	.string "The GYM here is steel.\nFire, Fighting and Ground bite it.$"

OlivineCity_EventScript_Povoa4::
	lock
	faceplayer
	msgbox OlivineCity_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

OlivineCity_Text_Povoa4:
	.string "The CAFE by the water is the\nbest thing in this city.$"

OlivineCity_EventScript_Povoa5::
	lock
	faceplayer
	msgbox OlivineCity_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

OlivineCity_Text_Povoa5:
	.string "ROUTE 40 west is all sea.\nROUTE 39 north is all farmland.$"

@ <<< Povoamento: fim do bloco gerado <<<
