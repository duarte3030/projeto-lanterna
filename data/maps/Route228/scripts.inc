@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route228_MapScripts::
	.byte 0

Route228_EventScript_AceTrainerJose::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_JOSE, Route228_Text_AceTrainerJoseIntro, Route228_Text_AceTrainerJoseDefeat
	msgbox Route228_Text_AceTrainerJosePost, MSGBOX_AUTOCLOSE
	end

Route228_EventScript_RangerKyler::
	trainerbattle_single TRAINER_SINNOH_RANGER_KYLER, Route228_Text_RangerKylerIntro, Route228_Text_RangerKylerDefeat
	msgbox Route228_Text_RangerKylerPost, MSGBOX_AUTOCLOSE
	end

Route228_EventScript_DragonTamerKeegan::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_KEEGAN, Route228_Text_DragonTamerKeeganIntro, Route228_Text_DragonTamerKeeganDefeat
	msgbox Route228_Text_DragonTamerKeeganPost, MSGBOX_AUTOCLOSE
	end

Route228_EventScript_BlackBeltDavon::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_DAVON, Route228_Text_BlackBeltDavonIntro, Route228_Text_BlackBeltDavonDefeat
	msgbox Route228_Text_BlackBeltDavonPost, MSGBOX_AUTOCLOSE
	end

Route228_EventScript_AceTrainerMoira::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MOIRA, Route228_Text_AceTrainerMoiraIntro, Route228_Text_AceTrainerMoiraDefeat
	msgbox Route228_Text_AceTrainerMoiraPost, MSGBOX_AUTOCLOSE
	end

Route228_EventScript_RangerKrista::
	trainerbattle_single TRAINER_SINNOH_RANGER_KRISTA, Route228_Text_RangerKristaIntro, Route228_Text_RangerKristaDefeat
	msgbox Route228_Text_RangerKristaPost, MSGBOX_AUTOCLOSE
	end

Route228_EventScript_PsychicCorbin::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_CORBIN, Route228_Text_PsychicCorbinIntro, Route228_Text_PsychicCorbinDefeat
	msgbox Route228_Text_PsychicCorbinPost, MSGBOX_AUTOCLOSE
	end

Route228_EventScript_AceTrainerMeagan::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MEAGAN, Route228_Text_AceTrainerMeaganIntro, Route228_Text_AceTrainerMeaganDefeat
	msgbox Route228_Text_AceTrainerMeaganPost, MSGBOX_AUTOCLOSE
	end

Route228_Text_AceTrainerJoseIntro:
	.string "Have you any knowledge of levels\n"
	.string "or the stats of Pokémon? Well, I do!$"

Route228_Text_AceTrainerJoseDefeat:
	.string "Hmm. I like how you attack.$"

Route228_Text_AceTrainerJosePost:
	.string "Pokémon and numbers...\n"
	.string "Who cares about that stuff?\p"
	.string "Winning is what's important.\n"
	.string "Numbers aren't everything.$"

Route228_Text_RangerKylerIntro:
	.string "People! Nature! Pokémon!\n"
	.string "Harmony is essential!$"

Route228_Text_RangerKylerDefeat:
	.string "You're A-OK!$"

Route228_Text_RangerKylerPost:
	.string "Protecting Pokémon and nature.\n"
	.string "Think of what that means.$"

Route228_Text_DragonTamerKeeganIntro:
	.string "Dragon Pokémon are sacred beings...\n"
	.string "That's what my master taught me.\p"
	.string "And now I'll prove it to you!$"

Route228_Text_DragonTamerKeeganDefeat:
	.string "Not good enough!\n"
	.string "We're still not strong enough!$"

Route228_Text_DragonTamerKeeganPost:
	.string "It's not good enough for a Pokémon\n"
	.string "to just be tough.\p"
	.string "It's not good enough for a Trainer\n"
	.string "to just work hard.\p"
	.string "Both have to grow together!$"

Route228_Text_BlackBeltDavonIntro:
	.string "My quest for power brought me here.\p"
	.string "It was beneath the desert sand that\n"
	.string "I toughened my body and soul.\p"
	.string "Accept my challenge! Uraah!$"

Route228_Text_BlackBeltDavonDefeat:
	.string "My spirit is broken...$"

Route228_Text_BlackBeltDavonPost:
	.string "I thought I couldn't win before it\n"
	.string "became a fact...\p"
	.string "I've let down my Pokémon...\p"
	.string "They go to battle with faith in\n"
	.string "their Trainer...$"

Route228_Text_AceTrainerMoiraIntro:
	.string "Please don't hold anything back.$"

Route228_Text_AceTrainerMoiraDefeat:
	.string "Hmm...$"

Route228_Text_AceTrainerMoiraPost:
	.string "I feel invigorated from that battle,\n"
	.string "even though we lost.\p"
	.string "After all, we gave it everything we\n"
	.string "had.$"

Route228_Text_RangerKristaIntro:
	.string "Are you getting worn out from all\n"
	.string "the running you've done?$"

Route228_Text_RangerKristaDefeat:
	.string "You're not tired at all?!$"

Route228_Text_RangerKristaPost:
	.string "The world is full of Pokémon and all\n"
	.string "sorts of Trainers.$"

Route228_Text_PsychicCorbinIntro:
	.string "You're going to win!\n"
	.string "That's the future I saw!$"

Route228_Text_PsychicCorbinDefeat:
	.string "What I saw in the future turned out\n"
	.string "to be true...$"

Route228_Text_PsychicCorbinPost:
	.string "I lost, but my vision of the future\n"
	.string "came true...$"

Route228_Text_AceTrainerMeaganIntro:
	.string "What sort of moves have you taught?\n"
	.string "That tells me how good you are!$"

Route228_Text_AceTrainerMeaganDefeat:
	.string "Yowch!$"

Route228_Text_AceTrainerMeaganPost:
	.string "I heard that somewhere there's\n"
	.string "someone who teaches Pokémon moves.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route228_EventScript_Placa1::
	msgbox Route228_Text_Placa1, MSGBOX_SIGN
	end

Route228_Text_Placa1:
	.string "Rt. 228\nRt. 226$"

Route228_EventScript_Placa2::
	msgbox Route228_Text_Placa2, MSGBOX_SIGN
	end

Route228_Text_Placa2:
	.string "Rt. 228\nRt. 229$"
