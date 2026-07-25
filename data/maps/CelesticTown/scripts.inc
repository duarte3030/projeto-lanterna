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
