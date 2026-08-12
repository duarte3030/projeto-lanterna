EcruteakCity_SageOffice1_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

EcruteakCity_SageOffice1_EventScript_Sign::
	msgbox EcruteakCity_SageOffice1_Text_Sign, MSGBOX_SIGN
	end

EcruteakCity_SageOffice1_Text_Sign::
	.string "The bell of tin rings clearly for\n"
	.string "those under the tower's wing.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

EcruteakCity_SageOffice2_EventScript_SageC::
	lock
	faceplayer
	msgbox EcruteakTinTowerEntrance_Text_Gramps, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakTinTowerEntrance_Text_Gramps::
	.string "Two towers… Two POKéMON…\p"
	.string "But when one burned down, both\n"
	.string "POKéMON flew away, never to return.$"
