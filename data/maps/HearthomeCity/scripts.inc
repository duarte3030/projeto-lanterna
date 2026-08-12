@ Textos vindos de pret/pokeplatinum (res/text/hearthome_city.json), em ingles.
@ Pokefan_M_2, Hiker_2, Hiker_3, Buneary, Keira e o Gym_Guide ficaram de fora:
@ dependem de flag de historia (FLAG_HIDE_HEARTHOME_CITY_*), que este agente
@ nao pode inventar.

HearthomeCity_MapScripts::
	.byte 0

HearthomeCity_EventScript_PokefanM::
	msgbox HearthomeCity_Text_PokefanM, MSGBOX_NPC
	end

HearthomeCity_EventScript_BreederF::
	msgbox HearthomeCity_Text_BreederF, MSGBOX_NPC
	end

HearthomeCity_EventScript_BlackBelt::
	msgbox HearthomeCity_Text_BlackBelt, MSGBOX_NPC
	end

HearthomeCity_EventScript_ContestHallSign::
	msgbox HearthomeCity_Text_ContestHallSign, MSGBOX_SIGN
	end

HearthomeCity_EventScript_GymSign::
	msgbox HearthomeCity_Text_GymSign, MSGBOX_SIGN
	end

HearthomeCity_Text_PokefanM:
	.string "HEARTHOME CITY is famous for its\n"
	.string "POKéMON Contests. Have you seen\l"
	.string "the CONTEST HALL yet?$"

HearthomeCity_Text_BreederF:
	.string "I raise my POKéMON right here in\n"
	.string "the city square. They love all\l"
	.string "the attention.$"

HearthomeCity_Text_BlackBelt:
	.string "Strength of body, strength of\n"
	.string "spirit. That's the way here in\l"
	.string "HEARTHOME.$"

HearthomeCity_Text_ContestHallSign:
	.string "POKéMON CONTEST HALL$"

HearthomeCity_Text_GymSign:
	.string "HEARTHOME CITY POKéMON GYM\p"
	.string "The Normal-Type Beauty Style!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

HearthomeCity_EventScript_Placa1::
	msgbox HearthomeCity_Text_Placa1, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa1:
	.string "Rt. 208\nRt. 212$"

HearthomeCity_EventScript_Placa2::
	msgbox HearthomeCity_Text_Placa2, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa2:
	.string "Rt. 209\nSolaceon Town$"

HearthomeCity_EventScript_Placa3::
	msgbox HearthomeCity_Text_Placa3, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa3:
	.string "Amity Square West Gate\nStroll with Your Pokémon!$"

HearthomeCity_EventScript_Placa4::
	msgbox HearthomeCity_Text_Placa4, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa4:
	.string "Pokémon Contest Hall\nCalling All Enthusiasts!$"

HearthomeCity_EventScript_Placa5::
	msgbox HearthomeCity_Text_Placa5, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa5:
	.string "Amity Square East Gate\nStroll with Your Pokémon!$"

HearthomeCity_EventScript_Placa6::
	msgbox HearthomeCity_Text_Placa6, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa6:
	.string "Pokémon Fan Club\nAll Trainers Welcome$"

HearthomeCity_EventScript_Placa7::
	msgbox HearthomeCity_Text_Placa7, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa7:
	.string "Hearthome City Pokémon Gym\nLeader: Fantina\pThe Alluring, Soulful Dancer!$"

HearthomeCity_EventScript_Placa9::
	msgbox HearthomeCity_Text_Placa9, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa9:
	.string "The Poffin House\nDelicious Poffins--Smiles for All$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

HearthomeCity_EventScript_Npc1::
	msgbox HearthomeCity_Text_Npc1, MSGBOX_NPC
	end

HearthomeCity_Text_Npc1:
	.string "I'm visiting here all the way from\nthe Hoenn region.\pI had been hoping to find the Contest\nHall, but being new, I lost my way.\pFortunately, the local people very\nkindly led me to my destination.\pI was impressed by their kindness and\ngenerosity to a complete stranger.\pNow, may I offer you the courtesy\nof showing you to the Contest Hall?$"

HearthomeCity_EventScript_Npc2::
	msgbox HearthomeCity_Text_Npc2, MSGBOX_NPC
	end

HearthomeCity_Text_Npc2:
	.string "You're a Trainer, are you?\pYou've got two choices of challenges,\neither the Gym or a Contest, right?$"

HearthomeCity_EventScript_Npc3::
	msgbox HearthomeCity_Text_Npc3, MSGBOX_NPC
	end

HearthomeCity_Text_Npc3:
	.string "When I take my baby out in his stroller,\nI see the town in a different way.\pI notice things like stairs and bumps\nin the sidewalk.$"

HearthomeCity_EventScript_Npc4::
	msgbox HearthomeCity_Text_Npc4, MSGBOX_NPC
	end

HearthomeCity_Text_Npc4:
	.string "Apapapu!$"

HearthomeCity_EventScript_Npc5::
	msgbox HearthomeCity_Text_Npc5, MSGBOX_NPC
	end

HearthomeCity_Text_Npc5:
	.string "At the Lost Tower, people unburden\nthemselves of unbearable sorrow...\pYou'll understand what I mean if you\nvisit the Lost Tower on Route 209.$"

HearthomeCity_EventScript_Npc6::
	msgbox HearthomeCity_Text_Npc6, MSGBOX_NPC
	end

HearthomeCity_Text_Npc6:
	.string "I get to see Pokémon all day long,\nbut there sure are many kinds.\pHow many are there now?$"

HearthomeCity_EventScript_Npc7::
	msgbox HearthomeCity_Text_Npc7, MSGBOX_NPC
	end

HearthomeCity_Text_Npc7:
	.string "They call me Mr. Goods.\pNo one knows my real name.\nNo, not even I do...\pI dedicate myself to seeking rarities.\nIt's what I live for.$"

HearthomeCity_EventScript_Npc8::
	msgbox HearthomeCity_Text_Npc8, MSGBOX_NPC
	end

HearthomeCity_Text_Npc8:
	.string "I can't decide what Accessories I\nshould dress up Pokémon with.\pThere are just so many kinds.$"

HearthomeCity_EventScript_Npc9::
	msgbox HearthomeCity_Text_Npc9, MSGBOX_NPC
	end

HearthomeCity_Text_Npc9:
	.string "I used a Fire Stone on my Pokémon,\nand it evolved!$"

HearthomeCity_EventScript_Npc10::
	msgbox HearthomeCity_Text_Npc10, MSGBOX_NPC
	end

HearthomeCity_Text_Npc10:
	.string "I went for a stroll in Amity Square\nwith my PACHIRISU today.\pWe came across a Pokémon feather\nwhile we walked.\pDo you think it'd make my PACHIRISU\nlook any cuter?$"

HearthomeCity_EventScript_Npc11::
	msgbox HearthomeCity_Text_Npc11, MSGBOX_NPC
	end

HearthomeCity_Text_Npc11:
	.string "I'd like to live in Hearthome when\nI get married.\pBut my boyfriend wants to live in\nVeilstone 'cause of its Game Corner...$"

HearthomeCity_EventScript_Npc12::
	msgbox HearthomeCity_Text_Npc12, MSGBOX_NPC
	end

HearthomeCity_Text_Npc12:
	.string "I lived in total seclusion up in\nthe mountains for thirty years!\pI'm going to clean up some Contests\nwith a dance move I came up with!$"

HearthomeCity_EventScript_Npc13::
	msgbox HearthomeCity_Text_Npc13, MSGBOX_NPC
	end

HearthomeCity_Text_Npc13:
	.string "Papa! Mama!$"

HearthomeCity_EventScript_Npc14::
	msgbox HearthomeCity_Text_Npc14, MSGBOX_NPC
	end

HearthomeCity_Text_Npc14:
	.string "I can feel the baby stroller getting\nheavier each and every day.\pI wonder what kind of Pokémon my\nchild will become friends with first?$"

HearthomeCity_EventScript_Npc15::
	msgbox HearthomeCity_Text_Npc15, MSGBOX_NPC
	end

HearthomeCity_Text_Npc15:
	.string "This place is beautiful.\nPerhaps even too much so.\pPokémon, people, and nature are in\nperfect harmony here.$"

HearthomeCity_EventScript_Npc16::
	msgbox HearthomeCity_Text_Npc16, MSGBOX_NPC
	end

HearthomeCity_Text_Npc16:
	.string "I put my Vs. Seeker through its paces\na lot.\pI battled this one intriguing Trainer\nover and over using it.\pShe asked me, 'Do you like me?'\nLike, oops! Hahahahah!$"

HearthomeCity_EventScript_Placa17::
	msgbox HearthomeCity_Text_Placa17, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa17:
	.string "Hearthome City\nWarm & Kind$"
