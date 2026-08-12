Route32_PokemonCenter_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route32_Pokecenter_Text_CooltrainerF::
	.string "What should I make my POKéMON hold?\p"
	.string "Maybe an item that increases\n"
	.string "ATTACK power…$"

Route32_PokemonCenter_EventScript_Lass::
	lock
	faceplayer
	msgbox Route32_Pokecenter_Text_CooltrainerF, MSGBOX_DEFAULT
	closemessage
	release
	end
