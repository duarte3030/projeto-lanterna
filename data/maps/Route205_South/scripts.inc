Route205_South_MapScripts::
	.byte 0

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route205_South_EventScript_Placa1::
	msgbox Route205_South_Text_Placa1, MSGBOX_SIGN
	end

Route205_South_Text_Placa1:
	.string "Rt. 205\nFloaroma Town$"

Route205_South_EventScript_Placa2::
	msgbox Route205_South_Text_Placa2, MSGBOX_SIGN
	end

Route205_South_Text_Placa2:
	.string "Rt. 205\nEterna Forest$"

Route205_South_EventScript_Placa3::
	msgbox Route205_South_Text_Placa3, MSGBOX_SIGN
	end

Route205_South_Text_Placa3:
	.string "Trainer Tips!\pThe items placed in your Bag are\nautomatically sorted to the\pappropriate pockets.\pIt's very convenient!\nIt's a Trainer's best friend!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route205_South_EventScript_Npc1::
	msgbox Route205_South_Text_Npc1, MSGBOX_NPC
	end

Route205_South_Text_Npc1:
	.string "Many Poison-type Pokémon make the\nEterna Forest their home.\pBut I didn't buy any Antidotes.\nWhat should I do?\pDo I press on, or do I go back?$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route205_South_EventScript_HikerDaniel::
	trainerbattle_single TRAINER_SINNOH_HIKER_DANIEL, Route205_South_Text_HikerDanielIntro, Route205_South_Text_HikerDanielDefeat
	msgbox Route205_South_Text_HikerDanielPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_HikerDanielIntro:
	.string "There's no mountain here, but I'm\ndressed to hike! Gahaha! Here goes!$"

Route205_South_Text_HikerDanielDefeat:
	.string "Oh, yeah!\nA refreshing battle that was!$"

Route205_South_Text_HikerDanielPost:
	.string "You can find the same kinds of\nPokémon in all sorts of places.\pThere's no law saying a Hiker can't\ngo searching off in the mountains!$"

Route205_South_EventScript_AromaLadyElizabeth::
	trainerbattle_single TRAINER_SINNOH_AROMA_LADY_ELIZABETH, Route205_South_Text_AromaLadyElizabethIntro, Route205_South_Text_AromaLadyElizabethDefeat
	msgbox Route205_South_Text_AromaLadyElizabethPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_AromaLadyElizabethIntro:
	.string "I love Pokémon that smell sweet.\nLike this one--get a whiff of this!$"

Route205_South_Text_AromaLadyElizabethDefeat:
	.string "Did you understand what I meant?\nDidn't my Pokémon smell nice?$"

Route205_South_Text_AromaLadyElizabethPost:
	.string "If you plant lots of Berries, you\ncan be surrounded by sweet scents.$"

Route205_South_EventScript_CamperJacob::
	trainerbattle_single TRAINER_SINNOH_CAMPER_JACOB, Route205_South_Text_CamperJacobIntro, Route205_South_Text_CamperJacobDefeat
	msgbox Route205_South_Text_CamperJacobPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_CamperJacobIntro:
	.string "Hey, how about you and me battle before\nI go into Eterna Forest?$"

Route205_South_Text_CamperJacobDefeat:
	.string "That really dampened my spirits.$"

Route205_South_Text_CamperJacobPost:
	.string "I heard that really tough Pokémon\nappear in Eterna Forest.\pI need to be more prepared than this!$"

Route205_South_EventScript_PicnickerSiena::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_SIENA, Route205_South_Text_PicnickerSienaIntro, Route205_South_Text_PicnickerSienaDefeat
	msgbox Route205_South_Text_PicnickerSienaPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_PicnickerSienaIntro:
	.string "What kinds of Pokémon live around\nhere, I wonder?$"

Route205_South_Text_PicnickerSienaDefeat:
	.string "I'm shocked!\nHow did I lose?$"

Route205_South_Text_PicnickerSienaPost:
	.string "I know all sorts of things about\nPokémon!\pLet's see... There are males and\nfemales, and some aren't either!$"

Route205_South_EventScript_HikerNicholas::
	trainerbattle_single TRAINER_SINNOH_HIKER_NICHOLAS, Route205_South_Text_HikerNicholasIntro, Route205_South_Text_HikerNicholasDefeat
	msgbox Route205_South_Text_HikerNicholasPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_HikerNicholasIntro:
	.string "I've lost my way...\nHere of all places...$"

Route205_South_Text_HikerNicholasDefeat:
	.string "Having lost his way, the Trainer lost\nthe battle too...$"

Route205_South_Text_HikerNicholasPost:
	.string "From being lost in the mountains so\nlong, I became a Hiker...$"

Route205_South_EventScript_BattleGirlKelsey::
	trainerbattle_single TRAINER_SINNOH_BATTLE_GIRL_KELSEY, Route205_South_Text_BattleGirlKelseyIntro, Route205_South_Text_BattleGirlKelseyDefeat
	msgbox Route205_South_Text_BattleGirlKelseyPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_BattleGirlKelseyIntro:
	.string "Hiyah!\nThere's no holding anything back!$"

Route205_South_Text_BattleGirlKelseyDefeat:
	.string "I... I concede!\nI think you're on a different level...$"

Route205_South_Text_BattleGirlKelseyPost:
	.string "Hiyah! You put me in my place!\nI appreciate it!$"

Route205_South_EventScript_PicnickerKarina::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_KARINA, Route205_South_Text_PicnickerKarinaIntro, Route205_South_Text_PicnickerKarinaDefeat
	msgbox Route205_South_Text_PicnickerKarinaPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_PicnickerKarinaIntro:
	.string "Oh, I don't know.\nShould I play a little?$"

Route205_South_Text_PicnickerKarinaDefeat:
	.string "Oh, boo!\nHow insulting!$"

Route205_South_Text_PicnickerKarinaPost:
	.string "Listen very closely...\nCan you hear the cries of Pokémon?$"

Route205_South_EventScript_CamperZackary::
	trainerbattle_single TRAINER_SINNOH_CAMPER_ZACKARY, Route205_South_Text_CamperZackaryIntro, Route205_South_Text_CamperZackaryDefeat
	msgbox Route205_South_Text_CamperZackaryPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_CamperZackaryIntro:
	.string "It's a long way between Floaroma\nand Eterna City. So, let's battle!$"

Route205_South_Text_CamperZackaryDefeat:
	.string "Wawawaah!\nI'm out of Pokémon that can go!$"

Route205_South_Text_CamperZackaryPost:
	.string "Camping with Pokémon!\nDo you have any idea how fun that is?$"
