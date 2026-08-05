@ Treinadores de rota de Route41, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route41_MapScripts::
	.byte 0

Route41_EventScript_Charlie::
	trainerbattle_single TRAINER_JOHTO_CHARLIE, Route41_Text_CharlieSeen, Route41_Text_CharlieBeaten
	msgbox Route41_Text_CharlieAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_George::
	trainerbattle_single TRAINER_JOHTO_GEORGE, Route41_Text_GeorgeSeen, Route41_Text_GeorgeBeaten
	msgbox Route41_Text_GeorgeAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Berke::
	trainerbattle_single TRAINER_JOHTO_BERKE, Route41_Text_BerkeSeen, Route41_Text_BerkeBeaten
	msgbox Route41_Text_BerkeAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Kirk::
	trainerbattle_single TRAINER_JOHTO_KIRK, Route41_Text_KirkSeen, Route41_Text_KirkBeaten
	msgbox Route41_Text_KirkAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Mathew::
	trainerbattle_single TRAINER_JOHTO_MATHEW, Route41_Text_MathewSeen, Route41_Text_MathewBeaten
	msgbox Route41_Text_MathewAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Kaylee::
	trainerbattle_single TRAINER_JOHTO_KAYLEE, Route41_Text_KayleeSeen, Route41_Text_KayleeBeaten
	msgbox Route41_Text_KayleeAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Susie::
	trainerbattle_single TRAINER_JOHTO_SUSIE, Route41_Text_SusieSeen, Route41_Text_SusieBeaten
	msgbox Route41_Text_SusieAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Denise::
	trainerbattle_single TRAINER_JOHTO_DENISE, Route41_Text_DeniseSeen, Route41_Text_DeniseBeaten
	msgbox Route41_Text_DeniseAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Kara::
	trainerbattle_single TRAINER_JOHTO_KARA, Route41_Text_KaraSeen, Route41_Text_KaraBeaten
	msgbox Route41_Text_KaraAfter, MSGBOX_AUTOCLOSE
	end

Route41_EventScript_Wendy::
	trainerbattle_single TRAINER_JOHTO_WENDY, Route41_Text_WendySeen, Route41_Text_WendyBeaten
	msgbox Route41_Text_WendyAfter, MSGBOX_AUTOCLOSE
	end

Route41_Text_CharlieSeen:
	.string "The water's warm here.\n"
	.string "I'm loose and limber.\p"
	.string "Sure, I'll take you on!$"

Route41_Text_CharlieBeaten:
	.string "Yikes! I've got prune skin!$"

Route41_Text_CharlieAfter:
	.string "Isn't it relaxing just floating\n"
	.string "like this?$"

Route41_Text_GeorgeSeen:
	.string "I'm a bit tired.\n"
	.string "If I win, lend me your POKéMON.$"

Route41_Text_GeorgeBeaten:
	.string "Pant, pant…$"

Route41_Text_GeorgeAfter:
	.string "It's so far to CIANWOOD.\p"
	.string "But it's no easy return trip\n"
	.string "to OLIVINE either.\p"
	.string "What should I do?$"

Route41_Text_BerkeSeen:
	.string "See those islands that are\n"
	.string "blocked by whirlpools?\p"
	.string "There just has to be a secret!$"

Route41_Text_BerkeBeaten:
	.string "What's the secret to your\n"
	.string "strength?$"

Route41_Text_BerkeAfter:
	.string "It was a dark and stormy night…\p"
	.string "I saw this giant POKéMON flying\n"
	.string "from the islands.\p"
	.string "It was scattering feathers\n"
	.string "from its silver wings.$"

Route41_Text_KirkSeen:
	.string "The waves are wild here.\p"
	.string "They tire you out while\n"
	.string "you swim.$"

Route41_Text_KirkBeaten:
	.string "I'm beat!$"

Route41_Text_KirkAfter:
	.string "The currents keep me from\n"
	.string "reaching that island.$"

Route41_Text_MathewSeen:
	.string "Are you seeking the secrets\n"
	.string "of WHIRL ISLANDS?$"

Route41_Text_MathewBeaten:
	.string "Ooh, you've got great endurance!$"

Route41_Text_MathewAfter:
	.string "A secret about WHIRL ISLANDS…\p"
	.string "It's pitch-black inside!$"

Route41_Text_KayleeSeen:
	.string "I'm on my way to WHIRL ISLANDS.\p"
	.string "I'm going exploring with friends.$"

Route41_Text_KayleeBeaten:
	.string "Is that how you do it?$"

Route41_Text_KayleeAfter:
	.string "There's supposed to be a big\n"
	.string "POKéMON deep beneath WHIRL ISLANDS.\p"
	.string "I wonder what it could be?$"

Route41_Text_SusieSeen:
	.string "You look so elegant,\n"
	.string "riding your POKéMON.$"

Route41_Text_SusieBeaten:
	.string "I'm crushed…$"

Route41_Text_SusieAfter:
	.string "Wasn't there a hit song about\n"
	.string "a boy riding a LAPRAS?$"

Route41_Text_DeniseSeen:
	.string "The weather is so beautiful,\n"
	.string "I'm in a daze!$"

Route41_Text_DeniseBeaten:
	.string "Ohhh!$"

Route41_Text_DeniseAfter:
	.string "A sunburn is the worst for skin.\p"
	.string "But I don't use a sunblock.\p"
	.string "I won't pollute the water.$"

Route41_Text_KaraSeen:
	.string "If you need to rest,\n"
	.string "just tread water.\p"
	.string "You'll get your wind back,\n"
	.string "so you can keep on going strong.$"

Route41_Text_KaraBeaten:
	.string "Oh! You have more energy than I do.$"

Route41_Text_KaraAfter:
	.string "I heard roars from deep inside\n"
	.string "the ISLANDS.$"

Route41_Text_WendySeen:
	.string "At night, STARYU gather near\n"
	.string "the water's surface.$"

Route41_Text_WendyBeaten:
	.string "Oh, dear…$"

Route41_Text_WendyAfter:
	.string "The clusters of STARYU light up\n"
	.string "at the same time.\p"
	.string "It's so beautiful, it's scary.$"
