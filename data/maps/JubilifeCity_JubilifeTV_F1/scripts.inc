JubilifeCity_JubilifeTV_F1_MapScripts::
	.byte 0

JubilifeCity_JubilifeTV_F1_EventScript_President::
	lock
	faceplayer
	msgbox JubilifeCity_JubilifeTV_F1_Text_President, MSGBOX_DEFAULT
	release
	end

JubilifeCity_JubilifeTV_F1_EventScript_Lottery::
	lock
	faceplayer
	msgbox JubilifeCity_JubilifeTV_F1_Text_Lottery, MSGBOX_DEFAULT
	release
	end

JubilifeCity_JubilifeTV_F1_Text_President:
	.string "I run the POKÉTCH COMPANY next door.\n"
	.string "Always good publicity, coming here.$"

JubilifeCity_JubilifeTV_F1_Text_Lottery:
	.string "This is the POKéMON Lottery Corner.\p"
	.string "We're not drawing numbers just yet,\n"
	.string "but come back soon!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_JubilifeTV_F1_EventScript_Npc1::
	msgbox JubilifeCity_JubilifeTV_F1_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_Text_Npc1:
	.string "They keep track of official records\nhere.\pThings like winning streaks, or how many\nPokémon you've caught.\pYou can check everyone's records\nup on the third floor.$"

JubilifeCity_JubilifeTV_F1_EventScript_Npc2::
	msgbox JubilifeCity_JubilifeTV_F1_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_Text_Npc2:
	.string "Why don't you try dressing up your\nPokémon now?\pWe have a Fitting Room on\nthe second floor.\pDress up your Pokémon nicely with\nAccessories!$"

JubilifeCity_JubilifeTV_F1_EventScript_Npc3::
	msgbox JubilifeCity_JubilifeTV_F1_Text_Npc3, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_Text_Npc3:
	.string "I'm going to get commercials shown\non TV.\pThey'll attract more customers to\nthe department store.$"

JubilifeCity_JubilifeTV_F1_EventScript_Npc4::
	msgbox JubilifeCity_JubilifeTV_F1_Text_Npc4, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_Text_Npc4:
	.string "This is the Pokémon Lottery Corner.\nI'm Felicity, your attendant today.\pIf your drawn number matches the\nID No. of any of your Pokémon,\pyou could win fabulous gifts.\pWould you like to check today's lucky\nnumber?$"

JubilifeCity_JubilifeTV_F1_EventScript_Npc5::
	msgbox JubilifeCity_JubilifeTV_F1_Text_Npc5, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_Text_Npc5:
	.string "The TV station interviews all sorts of\nTrainers for its shows.\pAfter all, people want to know about\ngood Trainers and what they say.\pPersonally, I'd like to learn more about\nGym Leaders.\pI'd also like to hear about the tough\nElite Four of the Pokémon League.$"
