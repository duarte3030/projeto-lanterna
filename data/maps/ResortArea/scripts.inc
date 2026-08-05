ResortArea_MapScripts::
	.byte 0

ResortArea_EventScript_Beauty1::
	msgbox ResortArea_Text_Beauty1, MSGBOX_NPC
	end

ResortArea_EventScript_Beauty2::
	msgbox ResortArea_Text_Beauty2, MSGBOX_NPC
	end

ResortArea_EventScript_BlackBelt::
	msgbox ResortArea_Text_BlackBelt, MSGBOX_NPC
	end

ResortArea_EventScript_CoolTrainerF::
	lock
	faceplayer
	msgbox ResortArea_Text_CoolTrainerF, MSGBOX_DEFAULT
	release
	end

ResortArea_EventScript_SwimmerM::
	msgbox ResortArea_Text_SwimmerM, MSGBOX_NPC
	end

ResortArea_EventScript_MapSign::
	msgbox ResortArea_Text_MapSign, MSGBOX_SIGN
	end

ResortArea_EventScript_VillaSign::
	msgbox ResortArea_Text_VillaSign, MSGBOX_SIGN
	end

ResortArea_Text_Beauty1:
	.string "The Resort Area breeze always\n"
	.string "smells like saltwater and flowers.$"

ResortArea_Text_Beauty2:
	.string "I could spend all day by this\n"
	.string "pool and never get bored.$"

ResortArea_Text_BlackBelt:
	.string "Training in the sun keeps my\n"
	.string "spirit as sharp as my fists.$"

ResortArea_Text_CoolTrainerF:
	.string "Oh, how I long to become a member\n"
	.string "of the Ribbon Syndicate. My dearest\p"
	.string "Pokémon will be treated to dreamy\n"
	.string "experiences!$"

ResortArea_Text_SwimmerM:
	.string "The water here is perfect for\n"
	.string "a swim any time of year.$"

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
