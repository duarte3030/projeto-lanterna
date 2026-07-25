@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route230_MapScripts::
	.byte 0

Route230_EventScript_SwimmerGlenn::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_GLENN, Route230_Text_SwimmerGlennIntro, Route230_Text_SwimmerGlennDefeat
	msgbox Route230_Text_SwimmerGlennPost, MSGBOX_AUTOCLOSE
	end

Route230_EventScript_SwimmerJoanna::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_JOANNA, Route230_Text_SwimmerJoannaIntro, Route230_Text_SwimmerJoannaDefeat
	msgbox Route230_Text_SwimmerJoannaPost, MSGBOX_AUTOCLOSE
	end

Route230_EventScript_SwimmerKurt::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_KURT, Route230_Text_SwimmerKurtIntro, Route230_Text_SwimmerKurtDefeat
	msgbox Route230_Text_SwimmerKurtPost, MSGBOX_AUTOCLOSE
	end

Route230_EventScript_SwimmerSophia::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_SOPHIA, Route230_Text_SwimmerSophiaIntro, Route230_Text_SwimmerSophiaDefeat
	msgbox Route230_Text_SwimmerSophiaPost, MSGBOX_AUTOCLOSE
	end

Route230_EventScript_SwimmerSam::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_SAM, Route230_Text_SwimmerSamIntro, Route230_Text_SwimmerSamDefeat
	msgbox Route230_Text_SwimmerSamPost, MSGBOX_AUTOCLOSE
	end

Route230_EventScript_SwimmerMallory::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_MALLORY, Route230_Text_SwimmerMalloryIntro, Route230_Text_SwimmerMalloryDefeat
	msgbox Route230_Text_SwimmerMalloryPost, MSGBOX_AUTOCLOSE
	end

Route230_Text_SwimmerGlennIntro:
	.string "A Trainer riding a Pokémon!\n"
	.string "I like that! Let's battle it out!$"

Route230_Text_SwimmerGlennDefeat:
	.string "Awesome!\n"
	.string "You're a real wild child!$"

Route230_Text_SwimmerGlennPost:
	.string "You ride atop the waves while riding on\n"
	.string "a Pokémon!\p"
	.string "And you rode right over me!$"

Route230_Text_SwimmerJoannaIntro:
	.string "People keep coming to us for battles.\n"
	.string "I really don't know why! Teehee!$"

Route230_Text_SwimmerJoannaDefeat:
	.string "OK, we lost.$"

Route230_Text_SwimmerJoannaPost:
	.string "I wanted to be alone, but swatting\n"
	.string "away immature boys on the prowl...\p"
	.string "Well, my Pokémon grew tough without\n"
	.string "me really even trying.$"

Route230_Text_SwimmerKurtIntro:
	.string "Check out my physique! The rough\n"
	.string "seas sculpted this awesome body!$"

Route230_Text_SwimmerKurtDefeat:
	.string "I've got a muscular physique, but\n"
	.string "there's no strength behind it...$"

Route230_Text_SwimmerKurtPost:
	.string "Seeing a Pokémon use Surf to carry you\n"
	.string "out on the sea...\p"
	.string "It strikes an emotional chord with me\n"
	.string "somewhere deep down.$"

Route230_Text_SwimmerSophiaIntro:
	.string "Are your Pokémon growing properly?$"

Route230_Text_SwimmerSophiaDefeat:
	.string "Maybe too grown up!$"

Route230_Text_SwimmerSophiaPost:
	.string "I've grown with my Pokémon, too.\n"
	.string "My swimsuit's getting a little tight...$"

Route230_Text_SwimmerSamIntro:
	.string "Check out my dynamic form!\n"
	.string "Victory is assured!$"

Route230_Text_SwimmerSamDefeat:
	.string "Oh.\n"
	.string "That's how it is.$"

Route230_Text_SwimmerSamPost:
	.string "Being a good swimmer doesn't make\n"
	.string "me any better as a Trainer...$"

Route230_Text_SwimmerMalloryIntro:
	.string "I'm a mermaid drifting among the\n"
	.string "waves...\p"
	.string "And a high-spirited gal who battles with\n"
	.string "Pokémon!$"

Route230_Text_SwimmerMalloryDefeat:
	.string "Losing...\n"
	.string "Makes my tears well up.$"

Route230_Text_SwimmerMalloryPost:
	.string "A mermaid's tears are so salty...$"
