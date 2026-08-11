@ Ginasio de Sinnoh com interior reaproveitado de Hoenn.

VeilstoneCity_Gym_MapScripts::
	.byte 0

VeilstoneCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_3, VeilstoneCity_Gym_EventScript_JaVenceu
	msgbox VeilstoneCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_MAYLENE, VeilstoneCity_Gym_Text_Defeat
	msgbox VeilstoneCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_3
	release
	end

VeilstoneCity_Gym_EventScript_JaVenceu::
	msgbox VeilstoneCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

VeilstoneCity_Gym_Text_Intro:
	.string "...$"

VeilstoneCity_Gym_Text_Defeat:
	.string "I shall admit defeat...\nYou are much too strong.$"

VeilstoneCity_Gym_Text_Post:
	.string "...$"

VeilstoneCity_Gym_Text_JaVenceu:
	.string "The COBBLE BADGE is already yours.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneCity_Gym_EventScript_Npc1::
	msgbox VeilstoneCity_Gym_Text_Npc1, MSGBOX_NPC
	end

VeilstoneCity_Gym_Text_Npc1:
	.string "Hey, there!\nHow's it going, Champ-to-be?\pThe Gym Leader is a user of\nFighting-type Pokémon.\pShe'd be a terror against Normal-type\nPokémon.\pBut! And it's a big but!\nJust between you and me...\pMaylene, the Gym Leader, said Flying-\nand Psychic-type Pokémon could be\preal trouble for her!\pIf you want to battle her, smack the\npunching bags along the rails.\pYou have to hit those bags hard!$"

VeilstoneCity_Gym_EventScript_Placa2::
	msgbox VeilstoneCity_Gym_Text_Placa2, MSGBOX_SIGN
	end

VeilstoneCity_Gym_Text_Placa2:
	.string "One day at a time.$"

VeilstoneCity_Gym_EventScript_Placa3::
	msgbox VeilstoneCity_Gym_Text_Placa3, MSGBOX_SIGN
	end

VeilstoneCity_Gym_Text_Placa3:
	.string "A good deed for every day.$"

VeilstoneCity_Gym_EventScript_Placa4::
	msgbox VeilstoneCity_Gym_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneCity_Gym_Text_Placa4:
	.string "Treasure every encounter,\nfor it is unique.$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

VeilstoneCity_Gym_EventScript_BlackBeltColby::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_COLBY, VeilstoneCity_Gym_Text_BlackBeltColbyIntro, VeilstoneCity_Gym_Text_BlackBeltColbyDefeat
	msgbox VeilstoneCity_Gym_Text_BlackBeltColbyPost, MSGBOX_AUTOCLOSE
	end

VeilstoneCity_Gym_Text_BlackBeltColbyIntro:
	.string "We're the Karate Quads!\pI will strike a blow for love with my\nfist! Hiyah, looooooooove!$"

VeilstoneCity_Gym_Text_BlackBeltColbyDefeat:
	.string "Argh! Crunched!$"

VeilstoneCity_Gym_Text_BlackBeltColbyPost:
	.string "Your Pokémon sure are tough!\pBut our Gym Leader Maylene will\nbreak you like a stack of bricks!$"

VeilstoneCity_Gym_EventScript_BlackBeltDarren::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_DARREN, VeilstoneCity_Gym_Text_BlackBeltDarrenIntro, VeilstoneCity_Gym_Text_BlackBeltDarrenDefeat
	msgbox VeilstoneCity_Gym_Text_BlackBeltDarrenPost, MSGBOX_AUTOCLOSE
	end

VeilstoneCity_Gym_Text_BlackBeltDarrenIntro:
	.string "We're the Karate Quads!\pI will strike a blow for courage with\nmy fist! Hiyah, couraaaaaaaaaaage!$"

VeilstoneCity_Gym_Text_BlackBeltDarrenDefeat:
	.string "I couldn't force my way to victory...$"

VeilstoneCity_Gym_Text_BlackBeltDarrenPost:
	.string "To overwhelm by force...\nThat is my ideal beat-down style.\pIt doesn't seem to work that way\nwith Pokémon, however.$"

VeilstoneCity_Gym_EventScript_BlackBeltJeffery::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_JEFFERY, VeilstoneCity_Gym_Text_BlackBeltJefferyIntro, VeilstoneCity_Gym_Text_BlackBeltJefferyDefeat
	msgbox VeilstoneCity_Gym_Text_BlackBeltJefferyPost, MSGBOX_AUTOCLOSE
	end

VeilstoneCity_Gym_Text_BlackBeltJefferyIntro:
	.string "We're the Karate Quads!\pI will strike a blow for tears with\nmy fist! Hiyah, teeeeeeaaaaaaaaars!$"

VeilstoneCity_Gym_Text_BlackBeltJefferyDefeat:
	.string "I'm so hungry, kid...\nI don't have any strength left...$"

VeilstoneCity_Gym_Text_BlackBeltJefferyPost:
	.string "I lost because I didn't eat\nenough pizza.\p...No. Anything I say will sound\nlike I'm making excuses.$"

VeilstoneCity_Gym_EventScript_BlackBeltRafael::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_RAFAEL, VeilstoneCity_Gym_Text_BlackBeltRafaelIntro, VeilstoneCity_Gym_Text_BlackBeltRafaelDefeat
	msgbox VeilstoneCity_Gym_Text_BlackBeltRafaelPost, MSGBOX_AUTOCLOSE
	end

VeilstoneCity_Gym_Text_BlackBeltRafaelIntro:
	.string "We're the Karate Quads!\pI will strike a blow for hope with my\nfist! Hiyah, hoooooooooooooope!$"

VeilstoneCity_Gym_Text_BlackBeltRafaelDefeat:
	.string "We came up short, but not by much.$"

VeilstoneCity_Gym_Text_BlackBeltRafaelPost:
	.string "I'll have to redo my training, though.\nMaylene's gonna trample me again...$"
