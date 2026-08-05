@ Textos vindos de pret/pokeplatinum (res/text/hearthome_city.json), em ingles.
@ Pokefan_M_2, Hiker_2, Hiker_3, Buneary, Keira e o Gym_Guide ficaram de fora:
@ dependem de flag de historia (FLAG_HIDE_HEARTHOME_CITY_*), que este agente
@ nao pode inventar.

HearthomeCity_MapScripts::
	.byte 0

HearthomeCity_EventScript_Fisherman::
	msgbox HearthomeCity_Text_Fisherman, MSGBOX_NPC
	end

HearthomeCity_EventScript_MrGoods::
	msgbox HearthomeCity_Text_MrGoods, MSGBOX_NPC
	end

HearthomeCity_EventScript_PokefanM::
	msgbox HearthomeCity_Text_PokefanM, MSGBOX_NPC
	end

HearthomeCity_EventScript_BreederF::
	msgbox HearthomeCity_Text_BreederF, MSGBOX_NPC
	end

HearthomeCity_EventScript_BattleGirl1::
	msgbox HearthomeCity_Text_BattleGirl1, MSGBOX_NPC
	end

HearthomeCity_EventScript_BattleGirl2::
	msgbox HearthomeCity_Text_BattleGirl2, MSGBOX_NPC
	end

HearthomeCity_EventScript_Hiker::
	msgbox HearthomeCity_Text_Hiker, MSGBOX_NPC
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

HearthomeCity_Text_Fisherman:
	.string "I'm visiting here all the way from\n"
	.string "the HOENN region.\p"
	.string "I had been hoping to find the\n"
	.string "CONTEST HALL, but being new, I\l"
	.string "lost my way.\p"
	.string "Fortunately, the local people very\n"
	.string "kindly led me to my destination.$"

HearthomeCity_Text_MrGoods:
	.string "They call me Mr. Goods. No one\n"
	.string "knows my real name. No, not even\l"
	.string "I do...\p"
	.string "I dedicate myself to seeking\n"
	.string "rarities. It's what I live for.$"

HearthomeCity_Text_PokefanM:
	.string "HEARTHOME CITY is famous for its\n"
	.string "POKéMON Contests. Have you seen\l"
	.string "the CONTEST HALL yet?$"

HearthomeCity_Text_BreederF:
	.string "I raise my POKéMON right here in\n"
	.string "the city square. They love all\l"
	.string "the attention.$"

HearthomeCity_Text_BattleGirl1:
	.string "I train every day so I can win at\n"
	.string "the POKéMON GYM here.$"

HearthomeCity_Text_BattleGirl2:
	.string "HEARTHOME's GYM LEADER is tough.\n"
	.string "You'll need a solid team.$"

HearthomeCity_Text_Hiker:
	.string "I rode down CYCLING ROAD all the\n"
	.string "way from ETERNA CITY. What a ride!$"

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
