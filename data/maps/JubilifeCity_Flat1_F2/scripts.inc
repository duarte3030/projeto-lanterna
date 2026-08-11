JubilifeCity_Flat1_F2_MapScripts::
	.byte 0

JubilifeCity_Flat1_F2_EventScript_BugCatcher::
	msgbox JubilifeCity_Flat1_F2_Text_BugCatcher, MSGBOX_NPC
	end

JubilifeCity_Flat1_F2_EventScript_BreederM::
	msgbox JubilifeCity_Flat1_F2_Text_BreederM, MSGBOX_NPC
	end

JubilifeCity_Flat1_F2_Text_BugCatcher:
	.string "I caught three KRICKETOT today!\p"
	.string "This building's garden is a\n"
	.string "bug-catching paradise.$"

JubilifeCity_Flat1_F2_Text_BreederM:
	.string "Raising POKéMON in an apartment\n"
	.string "isn't easy, but mine don't seem\l"
	.string "to mind.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_Flat1_F2_EventScript_Npc1::
	msgbox JubilifeCity_Flat1_F2_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_Flat1_F2_Text_Npc1:
	.string "I like how Pokémon can use attacks.\nThat makes things fun and different.\pSometimes, when they get stronger,\nPokémon learn new moves.\pThat keeps things fresh and fun when\nusing moves.$"

JubilifeCity_Flat1_F2_EventScript_Npc2::
	msgbox JubilifeCity_Flat1_F2_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_Flat1_F2_Text_Npc2:
	.string "Did you buy some Heal Balls at the\nPoké Mart?\pA Heal Ball completely heals the\nPokémon it captures on the spot.\pThat means you can catch a Pokémon\nand have it battle-ready right away.\pOf course, if your team has six\nPokémon in it, it won't do any good.$"
