Route204_MapScripts::
	.byte 0

Route204_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BUG_CATCHER_BRANDON, Route204_Text_Trainer1Intro, Route204_Text_Trainer1Defeat
	msgbox Route204_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route204_Text_Trainer1Intro:
	.string "Hey, hey, let me show off my bug\n"
	.string "Pokémon!$"

Route204_Text_Trainer1Defeat:
	.string "I'm not going to be able to explain\n"
	.string "the charms of bug Pokémon this way!$"

Route204_Text_Trainer1Post:
	.string "Bug Pokémon grow quickly, and they do\n"
	.string "stuff like poison and paralyze, and\pthey're cute and yet cool.\pYou gotta believe me. They're good!$"

Route204_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_AROMA_LADY_TAYLOR, Route204_Text_Trainer2Intro, Route204_Text_Trainer2Defeat
	msgbox Route204_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route204_Text_Trainer2Intro:
	.string "What kind of person are you, to be\n"
	.string "drawn here by the scent of flowers?$"

Route204_Text_Trainer2Defeat:
	.string "It was a strong Trainer who was drawn\n"
	.string "here by the scent of flowers!$"

Route204_Text_Trainer2Post:
	.string "By the way, have you collected new\n"
	.string "apps from the Pokétch Company?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route204_EventScript_Npc1::
	msgbox Route204_Text_Npc1, MSGBOX_NPC
	end

Route204_Text_Npc1:
	.string "There are boulders blocking the way\ninside the cavern...\pI think a Pokémon's hidden move will be\nable to smash those boulders, though.$"

Route204_EventScript_Placa2::
	msgbox Route204_Text_Placa2, MSGBOX_SIGN
	end

Route204_Text_Placa2:
	.string "Rt. 204\nJubilife City$"

Route204_EventScript_Placa3::
	msgbox Route204_Text_Placa3, MSGBOX_SIGN
	end

Route204_Text_Placa3:
	.string "Ravaged Path$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route204_EventScript_LassSarah::
	trainerbattle_single TRAINER_SINNOH_LASS_SARAH, Route204_Text_LassSarahIntro, Route204_Text_LassSarahDefeat
	msgbox Route204_Text_LassSarahPost, MSGBOX_AUTOCLOSE
	end

Route204_Text_LassSarahIntro:
	.string "Oh, a weak-looking Trainer...\nDo you want to have a go?$"

Route204_Text_LassSarahDefeat:
	.string "Aww...\nI should have said no.$"

Route204_Text_LassSarahPost:
	.string "Oh, you're so mean!\nI just started training Pokémon!$"

Route204_EventScript_LassSamantha::
	trainerbattle_single TRAINER_SINNOH_LASS_SAMANTHA, Route204_Text_LassSamanthaIntro, Route204_Text_LassSamanthaDefeat
	msgbox Route204_Text_LassSamanthaPost, MSGBOX_AUTOCLOSE
	end

Route204_Text_LassSamanthaIntro:
	.string "May I please trouble you for a\nbattle?$"

Route204_Text_LassSamanthaDefeat:
	.string "Oh...\nYou're so strong...$"

Route204_Text_LassSamanthaPost:
	.string "Maybe I could have won if my Pokémon\nwas holding a Berry...$"

Route204_EventScript_YoungsterTyler::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_TYLER, Route204_Text_YoungsterTylerIntro, Route204_Text_YoungsterTylerDefeat
	msgbox Route204_Text_YoungsterTylerPost, MSGBOX_AUTOCLOSE
	end

Route204_Text_YoungsterTylerIntro:
	.string "I'll beat you with the MAGIKARP my dad\ngave me!$"

Route204_Text_YoungsterTylerDefeat:
	.string "But they're Pokémon I got from my\ndad...$"

Route204_Text_YoungsterTylerPost:
	.string "Who gave you your first Pokémon?\pYour first Pokémon is the one with\nthe most fond memories, I think.$"

@ Treinador do pokeplatinum que os dois scripts irmaos nao alcancam
@ (dev_scripts/treinadores_faltantes_sinnoh.py)

Route204_EventScript_TwinLiv::
	trainerbattle_double TRAINER_SINNOH_TWINS_LIV_AND_LIZ, Route204_Text_TwinLivIntro, Route204_Text_TwinLivDefeat, Route204_Text_TwinLivNoPartner
	msgbox Route204_Text_TwinLivPost, MSGBOX_AUTOCLOSE
	end

Route204_Text_TwinLivIntro:
	.string "Liv: We can one-shot this Trainer,\ncan't we, Liz?$"

Route204_Text_TwinLivDefeat:
	.string "Liv: Oh, oh, oh?$"

Route204_Text_TwinLivPost:
	.string "Liv: This Trainer...will brag about\nbeating us, Liz.$"

Route204_Text_TwinLivNoPartner:
	.string "Liv: You only have one Pokémon?\nThat's so boring!$"

Route204_EventScript_TwinLiz::
	trainerbattle_double TRAINER_SINNOH_TWINS_LIV_AND_LIZ, Route204_Text_TwinLizIntro, Route204_Text_TwinLizDefeat, Route204_Text_TwinLizNoPartner
	msgbox Route204_Text_TwinLizPost, MSGBOX_AUTOCLOSE
	end

Route204_Text_TwinLizIntro:
	.string "Liz: We're the strongest in our\nclass!$"

Route204_Text_TwinLizDefeat:
	.string "Liz: Oh, but, wait!$"

Route204_Text_TwinLizPost:
	.string "Liz: This Trainer...is really happy about\nbeating us, Liv.$"

Route204_Text_TwinLizNoPartner:
	.string "Liz: Um, will you battle with us?\nMe and Liv?$"
