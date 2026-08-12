JubilifeCity_Flat1_F1_MapScripts::
	.byte 0

JubilifeCity_Flat1_F1_EventScript_Beauty::
	msgbox JubilifeCity_Flat1_F1_Text_Beauty, MSGBOX_NPC
	end

JubilifeCity_Flat1_F1_Text_Beauty:
	.string "Oh, your POKéMON is quite\n"
	.string "adorable! Here, try making it\l"
	.string "hold a Quick Claw.\p"
	.string "A POKéMON holding that can\n"
	.string "sometimes attack first, even if\l"
	.string "it's normally a little slow.\p"
	.string "There are other items that are\n"
	.string "only useful when held. Try\l"
	.string "finding some yourself...\p"
	.string "I sound like a teacher or\n"
	.string "something.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_Flat1_F1_EventScript_Npc1::
	msgbox JubilifeCity_Flat1_F1_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_Flat1_F1_Text_Npc1:
	.string "Oh, hello, darlings.\nIsn't my Pokétch quite fetching?\pIt's the latest design that just came\nout. I obtained it instantly, of course.\pA Trainer would be simply lost without\na Pokétch, after all.$"

JubilifeCity_Flat1_F1_EventScript_Npc2::
	msgbox JubilifeCity_Flat1_F1_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_Flat1_F1_Text_Npc2:
	.string "PIKACHU: Piika pi!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_Flat1_F1_EventScript_Npc3::
	bufferitemname STR_VAR_1, ITEM_QUICK_CLAW
	msgbox JubilifeCity_Flat1_F1_Text_Npc3, MSGBOX_NPC
	end

JubilifeCity_Flat1_F1_Text_Npc3:
	.string "Oh, your Pokémon is quite adorable!\pHere, try making it hold this\n{STR_VAR_1}.$"
