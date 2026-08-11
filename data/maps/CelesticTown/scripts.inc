@ Textos vindos de pret/pokeplatinum (res/text/celestic_town.json), em ingles.
@ Grunt_M, Elder e Cynthia ficaram de fora: dependem de flag de historia
@ (FLAG_HIDE_CELESTIC_TOWN_*), que este agente nao pode inventar.

CelesticTown_MapScripts::
	.byte 0

CelesticTown_EventScript_Expert::
	msgbox CelesticTown_Text_Expert, MSGBOX_NPC
	end

CelesticTown_EventScript_NinjaBoy::
	msgbox CelesticTown_Text_NinjaBoy, MSGBOX_NPC
	end

CelesticTown_EventScript_AceTrainer::
	msgbox CelesticTown_Text_AceTrainer, MSGBOX_NPC
	end

CelesticTown_EventScript_TownSign::
	msgbox CelesticTown_Text_TownSign, MSGBOX_SIGN
	end

CelesticTown_Text_Expert:
	.string "This town is one of the oldest in\n"
	.string "SINNOH. Even the ruins nearby are\l"
	.string "older than anyone can remember.$"

CelesticTown_Text_NinjaBoy:
	.string "I heard there's a weird glow inside\n"
	.string "the ruins sometimes. Spooky, huh?$"

CelesticTown_Text_AceTrainer:
	.string "CELESTIC TOWN doesn't get many\n"
	.string "visitors. I like it that way.$"

CelesticTown_Text_TownSign:
	.string "CELESTIC TOWN\n"
	.string "A Timeworn Town$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CelesticTown_EventScript_Npc1::
	msgbox CelesticTown_Text_Npc1, MSGBOX_NPC
	end

CelesticTown_Text_Npc1:
	.string "Howdy!\nStudying up on local history?$"

CelesticTown_EventScript_Npc2::
	msgbox CelesticTown_Text_Npc2, MSGBOX_NPC
	end

CelesticTown_Text_Npc2:
	.string "Hey, do you know what they say?\pThey say a Pokémon created the\nSinnoh region.$"

CelesticTown_EventScript_Npc3::
	msgbox CelesticTown_Text_Npc3, MSGBOX_NPC
	end

CelesticTown_Text_Npc3:
	.string "There's no Pokémon Mart in this\ntown...\pInstead, you can buy and sell items\nin this house here.$"

CelesticTown_EventScript_Placa4::
	msgbox CelesticTown_Text_Placa4, MSGBOX_SIGN
	end

CelesticTown_Text_Placa4:
	.string "Celestic Town\nThe Past Lives$"

CelesticTown_EventScript_Placa5::
	msgbox CelesticTown_Text_Placa5, MSGBOX_SIGN
	end

CelesticTown_Text_Placa5:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pThe flow of time never stops...\nThe past, future, and present...$"

CelesticTown_EventScript_Placa6::
	msgbox CelesticTown_Text_Placa6, MSGBOX_SIGN
	end

CelesticTown_Text_Placa6:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pThe flow of time never stops...\nThe past, future, and present...$"

CelesticTown_EventScript_Placa7::
	msgbox CelesticTown_Text_Placa7, MSGBOX_SIGN
	end

CelesticTown_Text_Placa7:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pThe flow of time never stops...\nThe past, future, and present...$"

CelesticTown_EventScript_Placa8::
	msgbox CelesticTown_Text_Placa8, MSGBOX_SIGN
	end

CelesticTown_Text_Placa8:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pSpace is ever-expanding dimensions...\nOur spirits, too, are as space...$"

CelesticTown_EventScript_Placa9::
	msgbox CelesticTown_Text_Placa9, MSGBOX_SIGN
	end

CelesticTown_Text_Placa9:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pSpace is ever-expanding dimensions...\nOur spirits, too, are as space...$"

CelesticTown_EventScript_Placa10::
	msgbox CelesticTown_Text_Placa10, MSGBOX_SIGN
	end

CelesticTown_Text_Placa10:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pSpace is ever-expanding dimensions...\nOur spirits, too, are as space...$"
