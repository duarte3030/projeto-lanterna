@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route227_MapScripts::
	.byte 0

Route227_EventScript_AceTrainerSaul::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SAUL, Route227_Text_AceTrainerSaulIntro, Route227_Text_AceTrainerSaulDefeat
	msgbox Route227_Text_AceTrainerSaulPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_RangerFelicia::
	trainerbattle_single TRAINER_SINNOH_RANGER_FELICIA, Route227_Text_RangerFeliciaIntro, Route227_Text_RangerFeliciaDefeat
	msgbox Route227_Text_RangerFeliciaPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_BlackBeltGriffin::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_GRIFFIN, Route227_Text_BlackBeltGriffinIntro, Route227_Text_BlackBeltGriffinDefeat
	msgbox Route227_Text_BlackBeltGriffinPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_AceTrainerMikayla::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MIKAYLA, Route227_Text_AceTrainerMikaylaIntro, Route227_Text_AceTrainerMikaylaDefeat
	msgbox Route227_Text_AceTrainerMikaylaPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_SignArrow::
	msgbox Route227_Text_SignArrow, MSGBOX_SIGN
	end

Route227_Text_AceTrainerSaulIntro:
	.string "I've got the urge to battle with you.\n"
	.string "Hope you're willing to oblige!$"

Route227_Text_AceTrainerSaulDefeat:
	.string "I shouldn't have paid attention\n"
	.string "to my urge...$"

Route227_Text_AceTrainerSaulPost:
	.string "So long as my partner's alongside me,\n"
	.string "I'm willing to take on the world!$"

Route227_Text_RangerFeliciaIntro:
	.string "We've grown strong together in\n"
	.string "nature and in the concrete jungle.\p"
	.string "We make everywhere we go our\n"
	.string "playground!$"

Route227_Text_RangerFeliciaDefeat:
	.string "You're really tough, aren't you?!$"

Route227_Text_RangerFeliciaPost:
	.string "Look around you at this wildly\n"
	.string "contorted terrain.\p"
	.string "It's no wonder that Pokémon would\n"
	.string "grow tough in a place like this.$"

Route227_Text_BlackBeltGriffinIntro:
	.string "I have meditated under a waterfall\n"
	.string "to temper my spirit.\p"
	.string "Allow me to demonstrate its strength!$"

Route227_Text_BlackBeltGriffinDefeat:
	.string "Ha-choo! Sniffle...$"

Route227_Text_BlackBeltGriffinPost:
	.string "All that time under the waterfall...\n"
	.string "Seems I've caught a cold.$"

Route227_Text_AceTrainerMikaylaIntro:
	.string "The world is huge, and there are\n"
	.string "so many different Pokémon!\p"
	.string "What kinds of Pokémon are with you?\n"
	.string "Please, I want to have a look!$"

Route227_Text_AceTrainerMikaylaDefeat:
	.string "Wow, there are Pokémon that\n"
	.string "wonderful!$"

Route227_Text_AceTrainerMikaylaPost:
	.string "There is always something to like\n"
	.string "about any Pokémon.\p"
	.string "It's so hard to decide which ones\n"
	.string "I should raise.$"

Route227_Text_SignArrow:
	.string "ROUTE 226\n"
	.string "This way, to the south.$"
