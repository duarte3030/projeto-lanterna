@ ONDA 2, LOTE I: a fala de resgate de Galar (07/09/2026).
@ Gerado por dev_scripts/objetos_galar.py --lote-i; NAO editar a mao.
@
@ Cada rotulo aqui e um NPC que estava MUDO porque a cena inteira
@ dele foi recusada pelo bloco c4a. A cena continua devendo (a
@ linha segue aberta em dev_scripts/fila_galar.json); o que entra e
@ a fala que a FONTE tem, traduzida para o ingles pela decisao 32.
@ O de-para do texto esta em dev_scripts/resgate_galar_texto.json.
@
@ `GalarFalaI_` nao e reconhecido por fila_galar.feitas() de
@ proposito: a fila tem de continuar cobrando a cena.
@
@ O campo `script` de cada object_event esta pedido em
@ dev_scripts/onda2_lote_i_pedidos_mapjson.json.

@ ---- Galar_Postwick10 ----
@ g01m110/objeto/20, objeto local 5 em (31,54)
GalarFalaI_G01M110_o20::
	lock
	faceplayer
	msgbox GalarFalaI_G01M110_o20_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G01M110_o20_Text:
	.string "Would you like to trade your Houndour\n"
	.string "for my Oshawott?$"

@ ---- Galar_Postwick169 ----
@ g40m12/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M12_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M12_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M12_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Postwick35 ----
@ g06m08/objeto/0, objeto local 1 em (6,5)
GalarFalaI_G06M08_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G06M08_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M08_o0_Text:
	.string "Welcome to the S.S. Anne!$"

@ g06m08/objeto/1, objeto local 2 em (11,6)
GalarFalaI_G06M08_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G06M08_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M08_o1_Text:
	.string "Hi, there!\n"
	.string "May I help you?$"

@ ---- Galar_SlumberingWeald01 ----
@ g01m00/objeto/2, objeto local 1 em (8,27)
GalarFalaI_G01M00_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G01M00_o2_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G01M00_o2_Text:
	.string "Hop: What is up with this fog!\n"
	.string "It's even worse than the first time\l"
	.string "we came here...$"

@ ---- Galar_Route0101 ----
@ g03m19/objeto/14, objeto local 2 em (62,12)
GalarFalaI_G03M19_o14::
	lock
	faceplayer
	msgbox GalarFalaI_G03M19_o14_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G03M19_o14_Text:
	.string "Would you like to trade your Eevee\n"
	.string "for my Piplup?$"

@ ---- Galar_Wedgehurst04 ----
@ g05m05/objeto/0, objeto local 1 em (6,2)
GalarFalaI_G05M05_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M05_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M05_o0_Text:
	.string " elcome to the Pokémon Wireless\n"
	.string "Club Union Room.\p"
	.string "You may interact directly with\n"
	.string "other Trainers here, some of\l"
	.string "whom you may not even know.\p"
	.string "Would you like to enter the Room?$"

@ g05m05/objeto/1, objeto local 2 em (2,2)
GalarFalaI_G05M05_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G05M05_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M05_o1_Text:
	.string "Hello, {PLAYER}!\p"
	.string "It’s me, Teala, the Pokémon\n"
	.string "Center 2F attendant.\p"
	.string "Is there something you needed to\n"
	.string "ask me about linking?$"

@ g05m05/objeto/2, objeto local 3 em (10,2)
GalarFalaI_G05M05_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G05M05_o2_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M05_o2_Text:
	.string "Welcome to the Pokémon Wireless Club\n"
	.string "Direct Corner.\p"
	.string "You may interact directly with your\n"
	.string "friends here.\p"
	.string "Which room would you like to enter?$"

@ g05m05/objeto/3, objeto local 4 em (1,2)
GalarFalaI_G05M05_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G05M05_o3_Text, MSGBOX_NPC
	release
	end

GalarFalaI_G05M05_o3_Text:
	.string "Thank you for accessing the Mystery\n"
	.string "Gift System.$"

@ ---- Galar_Wedgehurst05 ----
@ g05m06/objeto/22, objeto local 6 em (27,25)
GalarFalaI_G05M06_o22::
	lock
	faceplayer
	msgbox GalarFalaI_G05M06_o22_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M06_o22_Text:
	.string "Would you like to trade your Eldegoss\n"
	.string "for my Chikorita?$"

@ g05m06/objeto/5, objeto local 4 em (32,25)
GalarFalaI_G05M06_o5::
	lock
	faceplayer
	msgbox GalarFalaI_G05M06_o5_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M06_o5_Text:
	.string "Hello, {PLAYER}, this is Sonia's lab.\p"
	.string "Could you deliver this to her?\p"
	.string "I'm sure she'll reward you!$"

@ ---- Galar_Wedgehurst06 ----
@ g05m08/objeto/0, objeto local 1 em (6,3)
GalarFalaI_G05M08_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M08_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M08_o0_Text:
	.string "OAK: Now, {PLAYER}.\p"
	.string "Inside these Poké Balls\n"
	.string "there are Pokémon.\p"
	.string "Which one will you choose\n"
	.string "for yourself?$"

@ g05m08/objeto/1, objeto local 2 em (5,4)
GalarFalaI_G05M08_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G05M08_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M08_o1_Text:
	.string "Leon: How is the great Champion\n"
	.string "doing? Still buzzing about it all,\l"
	.string "I bought you a present!\l"
	.string "Have you heard of the Isle of Armor?\l"
	.string "It's an amazing island full of\l"
	.string "challenges. I went there when I was\l"
	.string "younger and I think you should go\l"
	.string "there too. Just show this pass to\l"
	.string "the guard at the Train Station!$"

@ ---- Galar_Wedgehurst07 ----
@ g05m11/objeto/0, objeto local 1 em (16,12)
GalarFalaI_G05M11_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M11_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M11_o0_Text:
	.string "Welcome to the Train Station!!!$"

@ ---- Galar_Wedgehurst08 ----
@ g05m16/objeto/3, objeto local 3 em (6,4)
GalarFalaI_G05M16_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G05M16_o3_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M16_o3_Text:
	.string "Jean Stars: Hello, player, I'm Jean\n"
	.string "stars, I made this Ultimate version!\l"
	.string "When you beat Leon, come back to\l"
	.string "have a Pokémon battle with me!$"

@ g05m16/objeto/4, objeto local 4 em (1,3)
GalarFalaI_G05M16_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G05M16_o4_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M16_o4_Text:
	.string "KJ: Hello, my name is KJ, come and\n"
	.string "battle me once you have beaten\l"
	.string "Leon!$"

@ g05m16/objeto/5, objeto local 5 em (4,5)
GalarFalaI_G05M16_o5::
	lock
	faceplayer
	msgbox GalarFalaI_G05M16_o5_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M16_o5_Text:
	.string "FNeto: I came a long way to battle\n"
	.string "you, but I can only do that after\l"
	.string "you beat Leon first.$"

@ g05m16/objeto/6, objeto local 6 em (0,3)
GalarFalaI_G05M16_o6::
	lock
	faceplayer
	msgbox GalarFalaI_G05M16_o6_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M16_o6_Text:
	.string "Sisu: Battle me when you beat Leon.$"

@ ---- Galar_Wedgehurst10 ----
@ g21m01/objeto/0, objeto local 1 em (6,2)
GalarFalaI_G21M01_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G21M01_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G21M01_o0_Text:
	.string " elcome to the Pokémon Wireless\n"
	.string "Club Union Room.\p"
	.string "You may interact directly with\n"
	.string "other Trainers here, some of\l"
	.string "whom you may not even know.\p"
	.string "Would you like to enter the Room?$"

@ g21m01/objeto/1, objeto local 2 em (2,2)
GalarFalaI_G21M01_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G21M01_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G21M01_o1_Text:
	.string "Hello, {PLAYER}!\p"
	.string "It’s me, Teala, the Pokémon\n"
	.string "Center 2F attendant.\p"
	.string "Is there something you needed to\n"
	.string "ask me about linking?$"

@ g21m01/objeto/2, objeto local 3 em (10,2)
GalarFalaI_G21M01_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G21M01_o2_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G21M01_o2_Text:
	.string "Welcome to the Pokémon Wireless Club\n"
	.string "Direct Corner.\p"
	.string "You may interact directly with your\n"
	.string "friends here.\p"
	.string "Which room would you like to enter?$"

@ g21m01/objeto/3, objeto local 4 em (1,2)
GalarFalaI_G21M01_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G21M01_o3_Text, MSGBOX_NPC
	release
	end

GalarFalaI_G21M01_o3_Text:
	.string "Thank you for accessing the Mystery\n"
	.string "Gift System.$"

@ ---- Galar_Wedgehurst11 ----
@ g40m07/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M07_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M07_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M07_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Wedgehurst12 ----
@ g03m01/objeto/6, objeto local 4 em (32,25)
GalarFalaI_G03M01_o6::
	lock
	faceplayer
	msgbox GalarFalaI_G03M01_o6_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G03M01_o6_Text:
	.string "Hello, {PLAYER}, this is Sonia's lab.\p"
	.string "Could you deliver this to her?\p"
	.string "I'm sure she'll reward you!$"

@ ---- Galar_Wedgehurst13 ----
@ g05m03/objeto/0, objeto local 1 em (2,3)
GalarFalaI_G05M03_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M03_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M03_o0_Text:
	.string "Hi, there!\n"
	.string "May I help you?$"

@ g05m03/objeto/1, objeto local 2 em (8,2)
GalarFalaI_G05M03_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G05M03_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M03_o1_Text:
	.string "You look tired. You should take a quick\n"
	.string "nap.$"

@ ---- Galar_Wedgehurst17 ----
@ g40m08/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M08_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M08_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M08_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Route0201 ----
@ g05m09/objeto/0, objeto local 1 em (7,15)
GalarFalaI_G05M09_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M09_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M09_o0_Text:
	.string "Hello, {PLAYER}, how is your journey\n"
	.string "going?$"

@ ---- Galar_Route0202 ----
@ g05m12/objeto/0, objeto local 1 em (43,24)
GalarFalaI_G05M12_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M12_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M12_o0_Text:
	.string "Hop: Look! There's the Professor!$"

@ g05m12/objeto/48, objeto local 10 em (48,48)
GalarFalaI_G05M12_o48::
	lock
	faceplayer
	msgbox GalarFalaI_G05M12_o48_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M12_o48_Text:
	.string "Would you like to trade your Carkol\n"
	.string "for my Cyndaquil?$"

@ ---- Galar_Route0203 ----
@ g05m13/objeto/0, objeto local 1 em (11,15)
GalarFalaI_G05M13_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M13_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M13_o0_Text:
	.string "PROF.MAG: Feel free to look at some\n"
	.string "rare Pokémon on the PC?\p"
	.string "Go ahead, take a look on my PC.$"

@ ---- Galar_Route0301 ----
@ g06m17/objeto/25, objeto local 9 em (36,3)
GalarFalaI_G06M17_o25::
	lock
	faceplayer
	msgbox GalarFalaI_G06M17_o25_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M17_o25_Text:
	.string "Would you like to trade your Boltund\n"
	.string "for my Mudkip?$"

@ ---- Galar_Motostoke01 ----
@ g00m06/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G00M06_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ g00m06/objeto/4, objeto local 4 em (9,7)
GalarFalaI_G00M06_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G00M06_o4_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G00M06_o4_Text:
	.string "Would you like to trade your Rockruff\n"
	.string "for my Chespin?$"

@ ---- Galar_Motostoke02 ----
@ g03m66/objeto/1, objeto local 2 em (11,6)
GalarFalaI_G03M66_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G03M66_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G03M66_o1_Text:
	.string "Hi, there!\n"
	.string "May I help you?$"

@ ---- Galar_Motostoke04 ----
@ g06m05/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G06M05_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_Motostoke05 ----
@ g06m10/objeto/0, objeto local 1 em (48,9)
GalarFalaI_G06M10_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G06M10_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M10_o0_Text:
	.string "Hop: You came too?!\p"
	.string "Ah, the Motostoke Stadium. This is\n"
	.string "where the Opening Ceremony will be!\p"
	.string "Everyone is going to watch it.\n"
	.string "My mum...your mum...everyone!\p"
	.string "It makes me nervous, honestly!\n"
	.string "Actually, I'm really excited!\p"
	.string "Let's go, {PLAYER}!\n"
	.string "It's time for the world to learn\l"
	.string "our names.$"

@ g06m10/objeto/1, objeto local 2 em (28,8)
GalarFalaI_G06M10_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G06M10_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M10_o1_Text:
	.string "The Budew Hotel is reserved for\n"
	.string "those taking part in the\p"
	.string "Gym Challenge!$"

@ g06m10/objeto/25, objeto local 15 em (31,44)
GalarFalaI_G06M10_o25::
	lock
	faceplayer
	msgbox GalarFalaI_G06M10_o25_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M10_o25_Text:
	.string "Would you like to trade your Diglett\n"
	.string "for my Torchic?$"

@ g06m10/objeto/36, objeto local 19 em (0,40)
GalarFalaI_G06M10_o36::
	lock
	faceplayer
	msgbox GalarFalaI_G06M10_o36_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M10_o36_Text:
	.string "Would you like to buy Z-Crystals?$"

@ g06m10/objeto/40, objeto local 22 em (0,43)
GalarFalaI_G06M10_o40::
	lock
	faceplayer
	msgbox GalarFalaI_G06M10_o40_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M10_o40_Text:
	.string "Would you like to buy Mega Stones?$"

@ g06m10/objeto/41, objeto local 23 em (1,65)
GalarFalaI_G06M10_o41::
	lock
	faceplayer
	msgbox GalarFalaI_G06M10_o41_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M10_o41_Text:
	.string "Jean Stars: Hello, player, I'm Jean\n"
	.string "stars, I made this Ultimate version!\l"
	.string "When you beat Leon, come back to\l"
	.string "have a Pokémon battle with me!$"

@ ---- Galar_Motostoke06 ----
@ g06m12/objeto/7, objeto local 8 em (1,6)
GalarFalaI_G06M12_o7::
	lock
	faceplayer
	msgbox GalarFalaI_G06M12_o7_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M12_o7_Text:
	.string "You're Gym Challengers, right?\p"
	.string "You can rest for today. Tomorrow will be\n"
	.string "the Opening Ceremony.$"

@ ---- Galar_Motostoke09 ----
@ g06m19/objeto/0, objeto local 1 em (7,5)
GalarFalaI_G06M19_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G06M19_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M19_o0_Text:
	.string "Hello, young one, I have a very good\n"
	.string "Pokémon for beginner Trainers.\l"
	.string "Do you want it?$"

@ g06m19/objeto/1, objeto local 2 em (2,6)
GalarFalaI_G06M19_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G06M19_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M19_o1_Text:
	.string "Would you like to trade your Greedent\n"
	.string "for my Fennekin?$"

@ ---- Galar_Motostoke17 ----
@ g06m32/objeto/2, objeto local 1 em (16,33)
GalarFalaI_G06M32_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G06M32_o2_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M32_o2_Text:
	.string "Would you like to trade your Dubwool\n"
	.string "for my Turtwig?$"

@ ---- Galar_Motostoke20 ----
@ g06m35/objeto/3, objeto local 4 em (14,2)
GalarFalaI_G06M35_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G06M35_o3_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M35_o3_Text:
	.string "You need two Badges to get through!$"

@ ---- Galar_Motostoke22 ----
@ g40m02/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M02_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M02_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M02_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Motostoke23 ----
@ g03m02/objeto/0, objeto local 1 em (48,9)
GalarFalaI_G03M02_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G03M02_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M02_o0_Text:
	.string "Hop: You came too?!\p"
	.string "Ah, the Motostoke Stadium. This is\n"
	.string "where the Opening Ceremony will be!\p"
	.string "Everyone is going to watch it.\n"
	.string "My mum...your mum...everyone!\p"
	.string "It makes me nervous, honestly!\n"
	.string "Actually, I'm really excited!\p"
	.string "Let's go, {PLAYER}!\n"
	.string "It's time for the world to learn\l"
	.string "our names.$"

@ g03m02/objeto/1, objeto local 2 em (28,8)
GalarFalaI_G03M02_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G03M02_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M02_o1_Text:
	.string "The Budew Hotel is reserved for\n"
	.string "those taking part in the\p"
	.string "Gym Challenge!$"

@ g03m02/objeto/14, objeto local 11 em (5,14)
GalarFalaI_G03M02_o14::
	lock
	faceplayer
	msgbox GalarFalaI_G03M02_o14_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M02_o14_Text:
	.string "I cannot let you through!$"

@ g03m02/objeto/2, objeto local 3 em (5,13)
GalarFalaI_G03M02_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G03M02_o2_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M02_o2_Text:
	.string "I cannot let you through!$"

@ g03m02/objeto/3, objeto local 4 em (5,12)
GalarFalaI_G03M02_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G03M02_o3_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M02_o3_Text:
	.string "I cannot let you through!$"

@ ---- Galar_WildArea01 ----
@ g03m35/objeto/0, objeto local 1 em (39,8)
GalarFalaI_G03M35_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G03M35_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M35_o0_Text:
	.string "Guard: Ah, a Gym Challenger!\n"
	.string "Let me check your Badges!\p"
	.string "The Grass Badge, the Water Badge\n"
	.string "and the Fire Badge,\p"
	.string "it is confirmed that you have beaten\n"
	.string "the three Gym Leaders, including\p"
	.string "the Gym Leader of Motostoke!\n"
	.string "I wish you good luck in your\p"
	.string "future battles!$"

@ g03m35/objeto/16, objeto local 9 em (40,8)
GalarFalaI_G03M35_o16::
	lock
	faceplayer
	msgbox GalarFalaI_G03M35_o16_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G03M35_o16_Text:
	.string "Hello, how can I help you?$"

@ g03m35/objeto/18, objeto local 10 em (37,28)
GalarFalaI_G03M35_o18::
	lock
	faceplayer
	msgbox GalarFalaI_G03M35_o18_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M35_o18_Text:
	.string "The Flying Taxi is available now.$"

@ g03m35/objeto/30, objeto local 11 em (43,25)
GalarFalaI_G03M35_o30::
	lock
	faceplayer
	msgbox GalarFalaI_G03M35_o30_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M35_o30_Text:
	.string "Hello, this is Wild Area 4, also\n"
	.string "called Huge Hill. It has 2 parts.\l"
	.string "Here you can find these Pokémon.$"

@ ---- Galar_WildArea03 ----
@ g06m27/objeto/29, objeto local 11 em (33,11)
GalarFalaI_G06M27_o29::
	lock
	faceplayer
	msgbox GalarFalaI_G06M27_o29_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G06M27_o29_Text:
	.string "Hello, young one, I am too tired to\n"
	.string "walk, and my Mudsdale ran off.\l"
	.string "Have you seen it?$"

@ ---- Galar_WildArea05 ----
@ g06m30/objeto/27, objeto local 5 em (40,12)
GalarFalaI_G06M30_o27::
	lock
	faceplayer
	msgbox GalarFalaI_G06M30_o27_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M30_o27_Text:
	.string "Would you like to trade your Girafarig\n"
	.string "for my Treecko?$"

@ ---- Galar_WildArea06 ----
@ g06m31/objeto/20, objeto local 7 em (18,30)
GalarFalaI_G06M31_o20::
	lock
	faceplayer
	msgbox GalarFalaI_G06M31_o20_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M31_o20_Text:
	.string "Would you like to trade your Drednaw\n"
	.string "for my Totodile?$"

@ g06m31/objeto/24, objeto local 9 em (37,20)
GalarFalaI_G06M31_o24::
	lock
	faceplayer
	msgbox GalarFalaI_G06M31_o24_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G06M31_o24_Text:
	.string "Would you like to trade your Drakloak\n"
	.string "for my Chespin?$"

@ ---- Galar_WildArea10 ----
@ g42m02/objeto/4, objeto local 2 em (40,17)
GalarFalaI_G42M02_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G42M02_o4_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G42M02_o4_Text:
	.string "{COLOR RED}Ah, my Morpeko got stuck up there, I\n"
	.string "can't get it down.\p"
	.string "I'm so worried...$"

@ ---- Galar_WildArea15 ----
@ g42m08/objeto/10, objeto local 1 em (24,31)
GalarFalaI_G42M08_o10::
	lock
	faceplayer
	msgbox GalarFalaI_G42M08_o10_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G42M08_o10_Text:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"

@ ---- Galar_WildArea17 ----
@ g42m10/objeto/39, objeto local 4 em (41,33)
GalarFalaI_G42M10_o39::
	lock
	faceplayer
	msgbox GalarFalaI_G42M10_o39_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G42M10_o39_Text:
	.string "{COLOR BLUE}What can I do for you?$"

@ ---- Galar_WildArea19 ----
@ g42m12/objeto/32, objeto local 3 em (19,27)
GalarFalaI_G42M12_o32::
	lock
	faceplayer
	msgbox GalarFalaI_G42M12_o32_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G42M12_o32_Text:
	.string "{COLOR BLUE}What can I do for you?$"

@ ---- Galar_WildArea22 ----
@ g42m15/objeto/0, objeto local 1 em (39,8)
GalarFalaI_G42M15_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G42M15_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G42M15_o0_Text:
	.string "Guard: Ah, a Gym Challenger!\n"
	.string "Let me check your Badges!\p"
	.string "The Grass Badge, the Water Badge\n"
	.string "and the Fire Badge,\p"
	.string "it is confirmed that you have beaten\n"
	.string "the three Gym Leaders, including\p"
	.string "the Gym Leader of Motostoke!\n"
	.string "I wish you good luck in your\p"
	.string "future battles!$"

@ ---- Galar_WildAreaIndoor02 ----
@ g39m25/objeto/0, objeto local 1 em (6,2)
GalarFalaI_G39M25_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G39M25_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G39M25_o0_Text:
	.string " elcome to the Pokémon Wireless\n"
	.string "Club Union Room.\p"
	.string "You may interact directly with\n"
	.string "other Trainers here, some of\l"
	.string "whom you may not even know.\p"
	.string "Would you like to enter the Room?$"

@ g39m25/objeto/1, objeto local 2 em (2,2)
GalarFalaI_G39M25_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G39M25_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G39M25_o1_Text:
	.string "Hello, {PLAYER}!\p"
	.string "It’s me, Teala, the Pokémon\n"
	.string "Center 2F attendant.\p"
	.string "Is there something you needed to\n"
	.string "ask me about linking?$"

@ g39m25/objeto/2, objeto local 3 em (10,2)
GalarFalaI_G39M25_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G39M25_o2_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G39M25_o2_Text:
	.string "Welcome to the Pokémon Wireless Club\n"
	.string "Direct Corner.\p"
	.string "You may interact directly with your\n"
	.string "friends here.\p"
	.string "Which room would you like to enter?$"

@ g39m25/objeto/3, objeto local 4 em (1,2)
GalarFalaI_G39M25_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G39M25_o3_Text, MSGBOX_NPC
	release
	end

GalarFalaI_G39M25_o3_Text:
	.string "Thank you for accessing the Mystery\n"
	.string "Gift System.$"

@ ---- Galar_Route0501 ----
@ g08m06/objeto/2, objeto local 2 em (33,13)
GalarFalaI_G08M06_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G08M06_o2_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G08M06_o2_Text:
	.string "I’m the Day-Care Man.\p"
	.string "I help take care of the precious\n"
	.string "Pokémon of Trainers.\p"
	.string "If you’d like me to raise your\n"
	.string "Pokémon, have a word with my wife.$"

@ g08m06/objeto/30, objeto local 4 em (21,14)
GalarFalaI_G08M06_o30::
	lock
	faceplayer
	msgbox GalarFalaI_G08M06_o30_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G08M06_o30_Text:
	.string "Would you like to trade your\n"
	.string "Corvisquire for my Froakie?$"

@ g08m06/objeto/33, objeto local 7 em (39,33)
GalarFalaI_G08M06_o33::
	lock
	faceplayer
	msgbox GalarFalaI_G08M06_o33_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G08M06_o33_Text:
	.string "Would you like to trade your Thievul\n"
	.string "for my Mudkip?$"

@ ---- Galar_Turffield02 ----
@ g07m03/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G07M03_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_Turffield08 ----
@ g07m19/objeto/0, objeto local 1 em (3,2)
GalarFalaI_G07M19_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G07M19_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G07M19_o0_Text:
	.string "Hey, Trainer, I have a Pokémon here\n"
	.string "that's quite different from the\l"
	.string "usual. Why don't you keep it?$"

@ ---- Galar_Turffield11 ----
@ g40m15/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M15_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M15_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M15_o1_Text:
	.string "What do you want?$"

@ ---- Galar_TurffieldIndoor15 ----
@ g35m14/objeto/11, objeto local 1 em (8,4)
GalarFalaI_G35M14_o11::
	lock
	faceplayer
	msgbox GalarFalaI_G35M14_o11_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G35M14_o11_Text:
	.string "Prepare for trouble, and we're warning\n"
	.string "you it will be double. To protect the\l"
	.string "world from devastation! To unite the\l"
	.string "people of our nation! To denounce the\l"
	.string "evils of truth and love! To extend our\l"
	.string "power to the stars! Jessie! James! Team\l"
	.string "Rocket blasting off at the speed of\l"
	.string "light! Surrender now or prepare to\l"
	.string "fight! Meowth, that's right!$"

@ g35m14/objeto/12, objeto local 2 em (8,5)
GalarFalaI_G35M14_o12::
	lock
	faceplayer
	msgbox GalarFalaI_G35M14_o12_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G35M14_o12_Text:
	.string "Prepare for trouble, and we're warning\n"
	.string "you it will be double. To protect the\l"
	.string "world from devastation! To unite the\l"
	.string "people of our nation! To denounce the\l"
	.string "evils of truth and love! To extend our\l"
	.string "power to the stars! Jessie! James! Team\l"
	.string "Rocket blasting off at the speed of\l"
	.string "light! Surrender now or prepare to\l"
	.string "fight! Meowth, that's right!$"

@ ---- Galar_TurffieldIndoor59 ----
@ g39m11/objeto/12, objeto local 1 em (8,5)
GalarFalaI_G39M11_o12::
	lock
	faceplayer
	msgbox GalarFalaI_G39M11_o12_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G39M11_o12_Text:
	.string "I'm going to fight with all I've got!!!$"

@ ---- Galar_Route0601 ----
@ g10m20/objeto/32, objeto local 9 em (17,24)
GalarFalaI_G10M20_o32::
	lock
	faceplayer
	msgbox GalarFalaI_G10M20_o32_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G10M20_o32_Text:
	.string "{COLOR DARK_GRAY}Hello, my name is {COLOR RED}Mudle{COLOR DARK_GRAY}.\p"
	.string "I'm the region's university student and\n"
	.string "I specialize in reviving {COLOR RED}Fossils{COLOR DARK_GRAY}.\p"
	.string "If you bring me one, I can do that for\n"
	.string "you.$"

@ ---- Galar_Hulbury01 ----
@ g00m08/objeto/1, objeto local 2 em (12,25)
GalarFalaI_G00M08_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G00M08_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G00M08_o1_Text:
	.string "Hop: Did you get the Gym Badge,\n"
	.string "{PLAYER}? Nice!$"

@ ---- Galar_Hulbury02 ----
@ g08m00/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G08M00_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ g08m00/objeto/1, objeto local 2 em (5,4)
GalarFalaI_G08M00_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G08M00_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G08M00_o1_Text:
	.string "{COLOR LIGHT_RED}Joy:Hello, welcome to the Pokémon\n"
	.string "Center.\p"
	.string "Here you can heal your Pokémon and get\n"
	.string "different items for them.$"

@ ---- Galar_Hulbury03 ----
@ g08m02/objeto/0, objeto local 1 em (4,3)
GalarFalaI_G08M02_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G08M02_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G08M02_o0_Text:
	.string "Mr. Fuji: {PLAYER}…\p"
	.string "Your Pokédex quest is one that\n"
	.string "requires strong dedication.\p"
	.string "Without deep love for Pokémon,\n"
	.string "your quest may fail.\p"
	.string "I’m not sure if this will help you,\n"
	.string "but I’d like you to have it.$"

@ ---- Galar_Hulbury06 ----
@ g08m07/objeto/10, objeto local 8 em (83,11)
GalarFalaI_G08M07_o10::
	lock
	faceplayer
	msgbox GalarFalaI_G08M07_o10_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G08M07_o10_Text:
	.string "Nessa: you must be the challenger,\n"
	.string "right? You are one of Leon's\l"
	.string "endorsees. You have become a very\l"
	.string "hot topic among the Leaders, so,\l"
	.string "mister famous, I am ready for you.\l"
	.string "So get to know me better and follow\l"
	.string "me to the stadium. I love fishing,\l"
	.string "but I love Pokémon battles more,\l"
	.string "and I am interested in a battle\l"
	.string "against you.$"

@ g08m07/objeto/21, objeto local 14 em (31,40)
GalarFalaI_G08M07_o21::
	lock
	faceplayer
	msgbox GalarFalaI_G08M07_o21_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G08M07_o21_Text:
	.string "{COLOR DARK_GRAY}Hey, this guy doesn't look well!\p"
	.string "HEY! He's choking!\p"
	.string "Could the Vespiquen have done this to\n"
	.string "him?\p"
	.string "I need to get help.$"

@ g08m07/objeto/30, objeto local 15 em (24,39)
GalarFalaI_G08M07_o30::
	lock
	faceplayer
	msgbox GalarFalaI_G08M07_o30_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G08M07_o30_Text:
	.string "{COLOR BLUE}Welcome to my shop, how can I help\n"
	.string "you?$"

@ ---- Galar_Hulbury14 ----
@ g40m00/objeto/0, objeto local 1 em (6,11)
GalarFalaI_G40M00_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G40M00_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M00_o0_Text:
	.string "What do you want?$"

@ ---- Galar_Hulbury15 ----
@ g40m10/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M10_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M10_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M10_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Hammerlocke01 ----
@ g03m05/objeto/13, objeto local 9 em (29,23)
GalarFalaI_G03M05_o13::
	lock
	faceplayer
	msgbox GalarFalaI_G03M05_o13_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G03M05_o13_Text:
	.string "Go ahead! Laugh!\n"
	.string "I'm flat-out busted!\p"
	.string "No more slots for me!\n"
	.string "I'm going straight!\p"
	.string "Here!\n"
	.string "I won't be needing this anymore!$"

@ g03m05/objeto/23, objeto local 19 em (38,8)
GalarFalaI_G03M05_o23::
	lock
	faceplayer
	msgbox GalarFalaI_G03M05_o23_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G03M05_o23_Text:
	.string "SONIA:Hello, player! You gave Raihan a\n"
	.string "real beating, and that means you've\l"
	.string "completed the Gym Challenge!\l"
	.string "Congratulations, from the bottom of my\l"
	.string "heart! I'd really love it if we could\l"
	.string "celebrate, but I think there are some\l"
	.string "things we should talk about. That light\l"
	.string "that covered Hammerlocke... It was like\l"
	.string "the Darkest Day, when they say giant\l"
	.string "Pokémon exploded and almost destroyed\l"
	.string "the whole Galar region.$"

@ ---- Galar_Hammerlocke03 ----
@ g09m09/objeto/2, objeto local 2 em (11,6)
GalarFalaI_G09M09_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G09M09_o2_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G09M09_o2_Text:
	.string "Hi, there!\n"
	.string "May I help you?$"

@ ---- Galar_Hammerlocke04 ----
@ g09m10/objeto/13, objeto local 11 em (17,16)
GalarFalaI_G09M10_o13::
	lock
	faceplayer
	msgbox GalarFalaI_G09M10_o13_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G09M10_o13_Text:
	.string "AM?If you want to play at the casino,\n"
	.string "then you're going to need this!$"

@ g09m10/objeto/22, objeto local 20 em (38,8)
GalarFalaI_G09M10_o22::
	lock
	faceplayer
	msgbox GalarFalaI_G09M10_o22_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G09M10_o22_Text:
	.string "SONIA:Hello, player! You gave Raihan a\n"
	.string "real beating, and that means you've\l"
	.string "completed the Gym Challenge!\l"
	.string "Congratulations, from the bottom of my\l"
	.string "heart! I'd really love it if we could\l"
	.string "celebrate, but I think there are some\l"
	.string "things we should talk about. That light\l"
	.string "that covered Hammerlocke... It was like\l"
	.string "the Darkest Day, when they say giant\l"
	.string "Pokémon exploded and almost destroyed\l"
	.string "the whole Galar region.$"

@ ---- Galar_Hammerlocke06 ----
@ g09m12/objeto/0, objeto local 1 em (54,27)
GalarFalaI_G09M12_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G09M12_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G09M12_o0_Text:
	.string "Opal: Hammerlocke is always a dusty\n"
	.string "city.\p"
	.string "Though I suppose some Pokémon\n"
	.string "prefer it that way.$"

@ g09m12/objeto/4, objeto local 5 em (69,30)
GalarFalaI_G09M12_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G09M12_o4_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G09M12_o4_Text:
	.string "Hop: First that forest, then that\n"
	.string "crazy test...I got lost in every\l"
	.string "sense of the word!\l"
	.string "But it looks like I finally found\l"
	.string "it again.\p"
	.string "Come with me to Route 7! I could use\n"
	.string "a bit of competition to keep me\l"
	.string "motivated!$"

@ ---- Galar_Hammerlocke07 ----
@ g09m14/objeto/12, objeto local 1 em (8,5)
GalarFalaI_G09M14_o12::
	lock
	faceplayer
	msgbox GalarFalaI_G09M14_o12_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G09M14_o12_Text:
	.string "I'm going to beat the Champion, win the\n"
	.string "whole tournament and prove to the\l"
	.string "world just how strong the great Raihan\l"
	.string "really is!$"

@ ---- Galar_Hammerlocke08 ----
@ g09m15/objeto/0, objeto local 1 em (8,4)
GalarFalaI_G09M15_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G09M15_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G09M15_o0_Text:
	.string "Those tapestries tell of the heroes of\n"
	.string "Galar from the past. Raihan:I suppose if\l"
	.string "we had a modern hero, he would be like\l"
	.string "Champion Leon. Listen, {PLAYER}\p"
	.string "Raihan:Your challenge is to defeat the\n"
	.string "superstar Leon. So head for Route 6 and\l"
	.string "train the whole way there!$"

@ ---- Galar_Hammerlocke09 ----
@ g09m16/objeto/0, objeto local 1 em (13,14)
GalarFalaI_G09M16_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G09M16_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G09M16_o0_Text:
	.string "Sonia: Ah, you're here. Brilliant, aren't\n"
	.string "they? It's great that there are still\l"
	.string "precious tapestries that can tell us\l"
	.string "about Galar's history.$"

@ ---- Galar_Hammerlocke15 ----
@ g10m12/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G10M12_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ g10m12/objeto/3, objeto local 4 em (4,7)
GalarFalaI_G10M12_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G10M12_o3_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M12_o3_Text:
	.string "Hello! Would you like to buy all of\n"
	.string "Rotom's forms for ¥10000?$"

@ ---- Galar_Hammerlocke16 ----
@ g10m14/objeto/0, objeto local 1 em (5,2)
GalarFalaI_G10M14_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G10M14_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M14_o0_Text:
	.string "Welcome to Rocket Game Corner!\p"
	.string "Do you need some game Coins? Would you\n"
	.string "like to buy some?$"

@ g10m14/objeto/3, objeto local 4 em (4,7)
GalarFalaI_G10M14_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G10M14_o3_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M14_o3_Text:
	.string "Kid, do you want to play?$"

@ g10m14/objeto/4, objeto local 5 em (7,10)
GalarFalaI_G10M14_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G10M14_o4_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M14_o4_Text:
	.string "Hey!\p"
	.string "You have better things to do,\n"
	.string "champ in the making!\p"
	.string "Celadon Gym’s Leader is Erika.\p"
	.string "She is a user of Grass-type\n"
	.string "Pokémon, and at one with nature.\p"
	.string "She might appear docile because of\n"
	.string "her flower arranging…\p"
	.string "But she’s not one to be taken\n"
	.string "lightly!$"

@ g10m14/objeto/7, objeto local 8 em (13,7)
GalarFalaI_G10M14_o7::
	lock
	faceplayer
	msgbox GalarFalaI_G10M14_o7_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M14_o7_Text:
	.string "What's up? Want some Coins?$"

@ g10m14/objeto/8, objeto local 9 em (16,10)
GalarFalaI_G10M14_o8::
	lock
	faceplayer
	msgbox GalarFalaI_G10M14_o8_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M14_o8_Text:
	.string "Hey, what? You’re throwing me off!\n"
	.string "Here are some Coins, so shoo!$"

@ ---- Galar_Hammerlocke17 ----
@ g10m15/objeto/0, objeto local 1 em (4,2)
GalarFalaI_G10M15_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G10M15_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M15_o0_Text:
	.string "We exchange your Coins for prizes.$"

@ g10m15/objeto/1, objeto local 2 em (6,2)
GalarFalaI_G10M15_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G10M15_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M15_o1_Text:
	.string "We exchange your Coins for prizes.$"

@ g10m15/objeto/2, objeto local 3 em (2,2)
GalarFalaI_G10M15_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G10M15_o2_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M15_o2_Text:
	.string "We exchange your Coins for prizes.$"

@ ---- Galar_Hammerlocke22 ----
@ g40m03/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M03_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M03_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M03_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Route0803 ----
@ g20m00/objeto/0, objeto local 1 em (4,4)
GalarFalaI_G20M00_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G20M00_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G20M00_o0_Text:
	.string "{COLOR RED}{PLAYER}:{COLOR DARK_GRAY}What the?... this man is dead!\p"
	.string "Those Pokémon... those {COLOR RED}Trubbish{COLOR DARK_GRAY} and\n"
	.string "that {COLOR RED}Garbodor{COLOR DARK_GRAY} were eating him?\p"
	.string "Arceus...\p"
	.string "Then again, he looks like he has been\n"
	.string "dead for a long time, but what exactly\l"
	.string "happened?\p"
	.string "Wait, what is this?$"

@ ---- Galar_StowOnSide04 ----
@ g09m01/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G09M01_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_StowOnSide06 ----
@ g09m18/objeto/0, objeto local 1 em (7,4)
GalarFalaI_G09M18_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G09M18_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G09M18_o0_Text:
	.string "I love this Falinks, but I'm not a\n"
	.string "very good Trainer. Please train\l"
	.string "it for me!$"

@ ---- Galar_StowOnSide07 ----
@ g09m19/objeto/0, objeto local 1 em (7,4)
GalarFalaI_G09M19_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G09M19_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G09M19_o0_Text:
	.string "{COLOR BLUE}Let me guess!\p"
	.string "You want me to teach {COLOR RED}Dragon Ascent{COLOR BLUE}\n"
	.string "to your Pokémon.\p"
	.string "Am I right?\p"
	.string "The only Pokémon that can learn that\n"
	.string "move is {COLOR RED}Rayquaza{COLOR BLUE}.\p"
	.string "Have you caught that legendary?$"

@ ---- Galar_StowOnSide08 ----
@ g10m21/objeto/16, objeto local 10 em (24,33)
GalarFalaI_G10M21_o16::
	lock
	faceplayer
	msgbox GalarFalaI_G10M21_o16_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M21_o16_Text:
	.string "Would you like to trade your Meowth\n"
	.string "for my Snivy?$"

@ g10m21/objeto/18, objeto local 12 em (26,66)
GalarFalaI_G10M21_o18::
	lock
	faceplayer
	msgbox GalarFalaI_G10M21_o18_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G10M21_o18_Text:
	.string "Would you like to trade your Eevee\n"
	.string "for my Tepig?$"

@ ---- Galar_StowOnSide11 ----
@ g21m00/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G21M00_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_StowOnSide12 ----
@ g40m01/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M01_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M01_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M01_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Route0901 ----
@ g14m11/objeto/15, objeto local 14 em (41,66)
GalarFalaI_G14M11_o15::
	lock
	faceplayer
	msgbox GalarFalaI_G14M11_o15_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G14M11_o15_Text:
	.string "I’m the Fishing Guru’s younger\n"
	.string "brother.\p"
	.string "I simply looove fishing!\n"
	.string "I can’t bear to go without.\p"
	.string "Tell me, do you like to fish?$"

@ ---- Galar_Ballonlea01 ----
@ g11m05/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G11M05_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_Ballonlea03 ----
@ g11m08/objeto/0, objeto local 1 em (6,5)
GalarFalaI_G11M08_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G11M08_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G11M08_o0_Text:
	.string "I’m the Fishing Guru’s older\n"
	.string "brother.\p"
	.string "I simply looove fishing!\n"
	.string "I can’t bear to go without.\p"
	.string "Tell me, do you like to fish?$"

@ ---- Galar_Ballonlea04 ----
@ g11m09/objeto/0, objeto local 1 em (5,4)
GalarFalaI_G11M09_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G11M09_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G11M09_o0_Text:
	.string "Uh... Ah, yes, I'm the Move Deleter.\p"
	.string "I can make a Pokémon forget its moves.\p"
	.string "Would you like me to do that?$"

@ ---- Galar_Ballonlea05 ----
@ g11m10/objeto/3, objeto local 3 em (16,27)
GalarFalaI_G11M10_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G11M10_o3_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G11M10_o3_Text:
	.string "Would you like to trade your Leafeon\n"
	.string "for my Rowlet?$"

@ g11m10/objeto/4, objeto local 4 em (28,37)
GalarFalaI_G11M10_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G11M10_o4_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G11M10_o4_Text:
	.string "Would you like to trade your Galarian\n"
	.string "Zigzagoon for my Litten?$"

@ ---- Galar_Ballonlea07 ----
@ g11m12/objeto/4, objeto local 5 em (4,8)
GalarFalaI_G11M12_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G11M12_o4_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G11M12_o4_Text:
	.string "Marnie: Hello, {PLAYER}, I have just\n"
	.string "faced Opal.\p"
	.string "I won her League Card too. Do you\n"
	.string "already have one of hers?\p"
	.string "{PLAYER}: Yes!\p"
	.string "Marnie: Cool!\p"
	.string "I have loads of them, from lots of\n"
	.string "people. Take a few for yourself!$"

@ ---- Galar_Ballonlea09 ----
@ g40m05/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M05_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M05_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M05_o1_Text:
	.string "What do you want?$"

@ ---- Galar_GlimwoodTangle01 ----
@ g01m109/objeto/30, objeto local 6 em (13,6)
GalarFalaI_G01M109_o30::
	lock
	faceplayer
	msgbox GalarFalaI_G01M109_o30_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G01M109_o30_Text:
	.string "Would you like to trade your Houndour\n"
	.string "for my Oshawott?$"

@ ---- Galar_Circhester03 ----
@ g12m00/objeto/7, objeto local 8 em (24,20)
GalarFalaI_G12M00_o7::
	lock
	faceplayer
	msgbox GalarFalaI_G12M00_o7_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G12M00_o7_Text:
	.string "Yo! Champ in the making!\p"
	.string "The hotheaded Blaine is a Fire Pokémon\n"
	.string "pro.\p"
	.string "Douse his spirits with water!\p"
	.string "You'd better take some Burn Heals, too.$"

@ ---- Galar_Circhester05 ----
@ g12m05/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G12M05_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_Circhester06 ----
@ g12m10/objeto/27, objeto local 19 em (22,58)
GalarFalaI_G12M10_o27::
	lock
	faceplayer
	msgbox GalarFalaI_G12M10_o27_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G12M10_o27_Text:
	.string "Would you like to trade your Galarian\n"
	.string "Yamask for my Popplio?$"

@ g12m10/objeto/33, objeto local 22 em (0,68)
GalarFalaI_G12M10_o33::
	lock
	faceplayer
	msgbox GalarFalaI_G12M10_o33_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G12M10_o33_Text:
	.string "Hello, would you like to trade your\n"
	.string "Pokémon for my Hawlucha?$"

@ ---- Galar_Circhester07 ----
@ g12m11/objeto/8, objeto local 7 em (13,12)
GalarFalaI_G12M11_o8::
	lock
	faceplayer
	msgbox GalarFalaI_G12M11_o8_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G12M11_o8_Text:
	.string "Hop: Arghhh! I lost! It was all for\n"
	.string "nothing!\p"
	.string "Something must have been wrong with\n"
	.string "my strategy, but I did exactly what\l"
	.string "Lee would have done in the battle!\p"
	.string "Here! Take it! It's the Gym Leader's\n"
	.string "League Card.\l"
	.string "You can see some information about\l"
	.string "them on it$"

@ ---- Galar_Circhester15 ----
@ g40m06/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M06_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M06_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M06_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Circhester16 ----
@ g03m08/objeto/28, objeto local 20 em (16,56)
GalarFalaI_G03M08_o28::
	lock
	faceplayer
	msgbox GalarFalaI_G03M08_o28_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G03M08_o28_Text:
	.string "Hello, would you like to trade your\n"
	.string "Pokémon for my Hawlucha?$"

@ ---- Galar_Route1002 ----
@ g13m06/objeto/1, objeto local 2 em (11,6)
GalarFalaI_G13M06_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G13M06_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G13M06_o1_Text:
	.string "Hi, there!\n"
	.string "May I help you?$"

@ ---- Galar_Spikemuth05 ----
@ g14m06/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G14M06_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_Spikemuth07 ----
@ g14m10/objeto/7, objeto local 8 em (72,23)
GalarFalaI_G14M10_o7::
	lock
	faceplayer
	msgbox GalarFalaI_G14M10_o7_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G14M10_o7_Text:
	.string "I'm going to fire up the crowd, even\n"
	.string "without using Dynamax!$"

@ ---- Galar_Spikemuth08 ----
@ g40m09/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M09_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M09_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M09_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Wyndon01 ----
@ g03m09/objeto/21, objeto local 21 em (53,48)
GalarFalaI_G03M09_o21::
	lock
	faceplayer
	msgbox GalarFalaI_G03M09_o21_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G03M09_o21_Text:
	.string "{COLOR DARK_GRAY}This woman is playing a song.\p"
	.string "Would you like to donate ¥1000?$"

@ ---- Galar_Wyndon02 ----
@ g13m00/objeto/1, objeto local 2 em (13,11)
GalarFalaI_G13M00_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G13M00_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G13M00_o1_Text:
	.string "Welcome back, Champion! Now we have\n"
	.string "more tournament options for you\l"
	.string "to take part in.$"

@ ---- Galar_Wyndon03 ----
@ g13m07/objeto/0, objeto local 1 em (6,2)
GalarFalaI_G13M07_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G13M07_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G13M07_o0_Text:
	.string "No battles for now!$"

@ ---- Galar_Wyndon06 ----
@ g33m02/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G33M02_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_Wyndon07 ----
@ g40m11/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M11_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M11_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M11_o1_Text:
	.string "What do you want?$"

@ ---- Galar_Wyndon08 ----
@ g13m10/objeto/1, objeto local 2 em (11,17)
GalarFalaI_G13M10_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G13M10_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G13M10_o1_Text:
	.string "HOP: This is absurd... Even Lee is\n"
	.string "never this late. Something isn't\l"
	.string "right.\p"
	.string "He always does what he says he'll do.\n"
	.string "When we were kids, he promised me\l"
	.string "he'd become Champion one day, and\l"
	.string "he went and did exactly that!\p"
	.string "He ought to be able to keep his own\n"
	.string "dinner plans!$"

@ ---- Galar_IsleOfArmor02 ----
@ g01m34/objeto/17, objeto local 9 em (22,4)
GalarFalaI_G01M34_o17::
	lock
	faceplayer
	msgbox GalarFalaI_G01M34_o17_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G01M34_o17_Text:
	.string "I'm a specialist in all sorts of\n"
	.string "Pokémon moves. Which one would you\l"
	.string "like me to teach your Pokémon?$"

@ ---- Galar_IsleOfArmor03 ----
@ g05m14/objeto/0, objeto local 1 em (6,5)
GalarFalaI_G05M14_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M14_o0_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G05M14_o0_Text:
	.string "Welcome to the S.S. Anne!$"

@ ---- Galar_IsleOfArmor04 ----
@ g34m01/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G34M01_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_IsleOfArmor07 ----
@ g38m03/objeto/21, objeto local 1 em (48,24)
GalarFalaI_G38M03_o21::
	lock
	faceplayer
	msgbox GalarFalaI_G38M03_o21_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G38M03_o21_Text:
	.string "I'm a little worn out by the\n"
	.string "musician's life... would you\l"
	.string "consider buying my Poké Flute?\l"
	.string "I'm offering it at a special price\l"
	.string "of just ¥5000.$"

@ ---- Galar_IsleOfArmor09 ----
@ g38m05/objeto/0, objeto local 1 em (53,69)
GalarFalaI_G38M05_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G38M05_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G38M05_o0_Text:
	.string "Hey, {PLAYER}, there's a good view of\n"
	.string "the Isle of Armor from here. Want to\l"
	.string "take a look with Kubfu?\p"
	.string "{PLAYER}: Sure!$"

@ ---- Galar_IsleOfArmor10 ----
@ g38m06/objeto/1, objeto local 1 em (45,6)
GalarFalaI_G38M06_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G38M06_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G38M06_o1_Text:
	.string "My daughter will not stop crying.\p"
	.string "I do not know what to do...$"

@ g38m06/objeto/2, objeto local 2 em (43,7)
GalarFalaI_G38M06_o2::
	lock
	faceplayer
	msgbox GalarFalaI_G38M06_o2_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G38M06_o2_Text:
	.string "Waaah\p"
	.string "{PLAYER}:This girl is crying a lot!$"

@ ---- Galar_IsleOfArmor12 ----
@ g38m08/objeto/0, objeto local 1 em (2,37)
GalarFalaI_G38M08_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G38M08_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G38M08_o0_Text:
	.string "Hey, {PLAYER}, there's a good view of\n"
	.string "the Isle of Armor from here. Want to\l"
	.string "take a look with Kubfu?\p"
	.string "{PLAYER}: Sure!$"

@ ---- Galar_IsleOfArmor37 ----
@ g40m13/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M13_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M13_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M13_o1_Text:
	.string "What do you want?$"

@ ---- Galar_CrownTundra01 ----
@ g00m13/objeto/1, objeto local 1 em (18,12)
GalarFalaI_G00M13_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G00M13_o1_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G00M13_o1_Text:
	.string "{COLOR DARK_GRAY}Sorry, sir, you can't...$"

@ g00m13/objeto/3, objeto local 2 em (18,11)
GalarFalaI_G00M13_o3::
	lock
	faceplayer
	msgbox GalarFalaI_G00M13_o3_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G00M13_o3_Text:
	.string "{COLOR DARK_GRAY}Sorry, sir, you can't...$"

@ ---- Galar_CrownTundra05 ----
@ g05m15/objeto/0, objeto local 1 em (11,6)
GalarFalaI_G05M15_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G05M15_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G05M15_o0_Text:
	.string "Hello, how can I help you?$"

@ ---- Galar_CrownTundra06 ----
@ g36m00/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G36M00_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_CrownTundra07 ----
@ g37m00/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G37M00_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_CrownTundra08 ----
@ g37m05/objeto/27, objeto local 9 em (52,1)
GalarFalaI_G37M05_o27::
	lock
	faceplayer
	msgbox GalarFalaI_G37M05_o27_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G37M05_o27_Text:
	.string "Would you like to buy Beast Balls?$"

@ g37m05/objeto/4, objeto local 4 em (49,1)
GalarFalaI_G37M05_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G37M05_o4_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G37M05_o4_Text:
	.string "Do not get in my way, I am in the\n"
	.string "middle of a battle!$"

@ g37m05/objeto/6, objeto local 5 em (3,37)
GalarFalaI_G37M05_o6::
	lock
	faceplayer
	msgbox GalarFalaI_G37M05_o6_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G37M05_o6_Text:
	.string "What can Freezingtong offer you,\n"
	.string "young one?$"

@ ---- Galar_CrownTundra19 ----
@ g40m14/objeto/1, objeto local 2 em (6,11)
GalarFalaI_G40M14_o1::
	lock
	faceplayer
	msgbox GalarFalaI_G40M14_o1_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G40M14_o1_Text:
	.string "What do you want?$"

@ ---- Galar_CrownTundra20 ----
@ g35m28/objeto/0, objeto local 1 em (7,2)
GalarFalaI_G35M28_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ ---- Galar_CrownTundraIndoor01 ----
@ g00m16/objeto/0, objeto local 1 em (2,4)
GalarFalaI_G00M16_o0::
	lock
	faceplayer
	msgbox GalarFalaI_G00M16_o0_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G00M16_o0_Text:
	.string "Mayor: So you're interested in some\n"
	.string "books about seeds, young man. Since you\l"
	.string "want to study this subject, I think\l"
	.string "you'd better have this.$"

@ ---- Galar_DynamaxAdventure01 ----
@ g34m04/objeto/4, objeto local 2 em (25,37)
GalarFalaI_G34M04_o4::
	lock
	faceplayer
	msgbox GalarFalaI_G34M04_o4_Text, MSGBOX_AUTOCLOSE
	release
	end

GalarFalaI_G34M04_o4_Text:
	.string "{COLOR RED}Peony: Niaaa!\p"
	.string "Niaaaaa!\p"
	.string "Where are you?\p"
	.string "Have you seen Nia around?$"

@ ---- Galar_DynamaxAdventure02 ----
@ g00m17/objeto/5, objeto local 2 em (60,18)
GalarFalaI_G00M17_o5::
	lock
	faceplayer
	msgbox GalarFalaI_G00M17_o5_Text, MSGBOX_DEFAULT
	release
	end

GalarFalaI_G00M17_o5_Text:
	.string "OAK: Now, {PLAYER}.\p"
	.string "Inside these Poké Balls\n"
	.string "there are Pokémon.\p"
	.string "Which one will you choose\n"
	.string "for yourself?$"

@ ---- Galar_TrainerTower01 ----
@ g02m10/objeto/0, objeto local 1 em (4,9)
GalarFalaI_G02M10_o0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

