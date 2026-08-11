JubilifeCity_PokemonSchool_MapScripts::
	.byte 0

JubilifeCity_PokemonSchool_EventScript_Teacher::
	lock
	faceplayer
	msgbox JubilifeCity_PokemonSchool_Text_Teacher, MSGBOX_DEFAULT
	release
	end

JubilifeCity_PokemonSchool_EventScript_Kid1::
	msgbox JubilifeCity_PokemonSchool_Text_Kid1, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_EventScript_Kid2::
	msgbox JubilifeCity_PokemonSchool_Text_Kid2, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_EventScript_Kid3::
	msgbox JubilifeCity_PokemonSchool_Text_Kid3, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Teacher:
	.string "Welcome! This is where young\n"
	.string "TRAINERS learn the basics.\p"
	.string "Feel free to look around the\n"
	.string "classroom.$"

JubilifeCity_PokemonSchool_Text_Kid1:
	.string "Today we're learning about TYPE\n"
	.string "match-ups!$"

JubilifeCity_PokemonSchool_Text_Kid2:
	.string "I want to be just like the POKéMON\n"
	.string "Professor someday.$"

JubilifeCity_PokemonSchool_Text_Kid3:
	.string "Psst! Don't tell the teacher, but I'd\n"
	.string "rather be battling right now.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_PokemonSchool_EventScript_Npc1::
	msgbox JubilifeCity_PokemonSchool_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Npc1:
	.string "It's perfectly fine for Trainers and\nPokémon to develop at their own pace.\pIf there is anything you're not familiar\nwith, you can look it up here.$"

JubilifeCity_PokemonSchool_EventScript_Npc2::
	msgbox JubilifeCity_PokemonSchool_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Npc2:
	.string "We learned about Pokémon types\ntoday. Umm...\pGrass is weak to Fire,\pFire is weak to Water,\pand Water is weak to Grass!$"

JubilifeCity_PokemonSchool_EventScript_Npc3::
	msgbox JubilifeCity_PokemonSchool_Text_Npc3, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Npc3:
	.string "Pokémon are smart enough to use\nitems they're holding.\pBut they won't know what to do with\nman-made items like Potions and\pAntidotes.$"

JubilifeCity_PokemonSchool_EventScript_Npc4::
	msgbox JubilifeCity_PokemonSchool_Text_Npc4, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Npc4:
	.string "I wrote an essay in my notebook on \nwhat makes a true Pokémon Trainer.$"

JubilifeCity_PokemonSchool_EventScript_Npc5::
	msgbox JubilifeCity_PokemonSchool_Text_Npc5, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Npc5:
	.string "Doing it is the best way to learn!\nCan we get a battle with you?$"

JubilifeCity_PokemonSchool_EventScript_Npc6::
	msgbox JubilifeCity_PokemonSchool_Text_Npc6, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Npc6:
	.string "I just became friends with my\nPokémon.\pI'm not sure if we can do this\nproperly, but may we battle?$"

JubilifeCity_PokemonSchool_EventScript_Placa7::
	msgbox JubilifeCity_PokemonSchool_Text_Placa7, MSGBOX_SIGN
	end

JubilifeCity_PokemonSchool_Text_Placa7:
	.string "The blackboard lists status changes\nthat may affect Pokémon in battle.$"

JubilifeCity_PokemonSchool_EventScript_Placa8::
	msgbox JubilifeCity_PokemonSchool_Text_Placa8, MSGBOX_SIGN
	end

JubilifeCity_PokemonSchool_Text_Placa8:
	.string "The blackboard lists status changes\nthat may affect Pokémon in battle.$"
