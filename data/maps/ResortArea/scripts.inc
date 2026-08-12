ResortArea_MapScripts::
	.byte 0

ResortArea_EventScript_CoolTrainerF::
	lock
	faceplayer
	msgbox ResortArea_Text_CoolTrainerF, MSGBOX_DEFAULT
	release
	end

ResortArea_EventScript_MapSign::
	msgbox ResortArea_Text_MapSign, MSGBOX_SIGN
	end

ResortArea_EventScript_VillaSign::
	msgbox ResortArea_Text_VillaSign, MSGBOX_SIGN
	end

ResortArea_Text_CoolTrainerF:
	.string "Oh, how I long to become a member\n"
	.string "of the Ribbon Syndicate. My dearest\p"
	.string "Pokémon will be treated to dreamy\n"
	.string "experiences!$"

ResortArea_Text_MapSign:
	.string "RESORT AREA\n"
	.string "Where Pokémon Rest in Style$"

ResortArea_Text_VillaSign:
	.string "VILLA\n"
	.string "A getaway for trainers and their\n"
	.string "Pokémon.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

ResortArea_EventScript_Placa2::
	msgbox ResortArea_Text_Placa2, MSGBOX_SIGN
	end

ResortArea_Text_Placa2:
	.string "The Ribbon Syndicate\nMembers Only$"

ResortArea_EventScript_Placa3::
	msgbox ResortArea_Text_Placa3, MSGBOX_SIGN
	end

ResortArea_Text_Placa3:
	.string "A Somewhat Impressive Villa$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

ResortArea_EventScript_Npc1::
	msgbox ResortArea_Text_Npc1, MSGBOX_NPC
	end

ResortArea_Text_Npc1:
	.string "I've traveled a long way to make my\nbeloved Pokémon even more beautiful.\pThat will make it love me even more.\nGiggle!$"

ResortArea_EventScript_Npc2::
	msgbox ResortArea_Text_Npc2, MSGBOX_NPC
	end

ResortArea_Text_Npc2:
	.string "Nothing is too good for my Pokémon.\nThere's no mountain too high to climb.\pThat's how I look at it.$"

ResortArea_EventScript_Npc3::
	msgbox ResortArea_Text_Npc3, MSGBOX_NPC
	end

ResortArea_Text_Npc3:
	.string "You know how you can dig up cool\nstuff in the Underground?\pPeople are saying they're digging up\nnew, different stuff.$"

ResortArea_EventScript_Npc4::
	msgbox ResortArea_Text_Npc4, MSGBOX_NPC
	end

ResortArea_Text_Npc4:
	.string "Nobody believes me, but something\nlurks in the Resort Area.\pIt's the hidden ruler of the area!\nYou have to believe me!\pIf you believe me, whip out your\nSuper Rod and go fishing.\pWho knows, you may just catch the\nmind-blowing ruler!$"

ResortArea_EventScript_Placa5::
	msgbox ResortArea_Text_Placa5, MSGBOX_SIGN
	end

ResortArea_Text_Placa5:
	.string "Resort Area\nRelax & Play!$"
