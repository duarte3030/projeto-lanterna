@ Route137: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 0.61) por dev_scripts/copia_planta_ex.py.

Route137_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 0.61), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route137_EventScript_ExNpc8::
	msgbox Route137_Text_ExNpc8, MSGBOX_NPC
	end

Route137_Text_ExNpc8:
	.string "I think there are some kids out there\n"
	.string "up to something.\p"
	.string "Be careful.$"

Route137_EventScript_ExNpc9::
	msgbox Route137_Text_ExNpc9, MSGBOX_NPC
	end

Route137_Text_ExNpc9:
	.string "There are flower POKéMON on this ROUTE.\p"
	.string "But, be careful they’ve got sharp\n"
	.string "thorns on em...\p"
	.string "SNIFF...$"

Route137_EventScript_ExNpc10::
	msgbox Route137_Text_ExNpc10, MSGBOX_NPC
	end

Route137_Text_ExNpc10:
	.string "Hrnn...\p"
	.string "Someones building something up there!$"

Route137_EventScript_ExTrainer11::
	trainerbattle_single TRAINER_HOENNEX_ROUTE137_GARTH, Route137_Text_ExTrainer11Intro, Route137_Text_ExTrainer11Defeat
	msgbox Route137_Text_ExTrainer11PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer11Intro:
	.string "Well well well, a big kid on my turf!\p"
	.string "I’ll show you why no one can stand\n"
	.string "against the EVIL FOREST GANG!$"

Route137_Text_ExTrainer11Defeat:
	.string "You’re a bully!$"

Route137_Text_ExTrainer11PostBattle:
	.string "Tsk!\n"
	.string "This is still our turf.\l"
	.string "We have the upper hand here!$"

Route137_EventScript_ExTrainer12::
	trainerbattle_single TRAINER_HOENNEX_ROUTE137_THEO, Route137_Text_ExTrainer12Intro, Route137_Text_ExTrainer12Defeat
	msgbox Route137_Text_ExTrainer12PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer12Intro:
	.string "Our BOSS is the one that taught us how\n"
	.string "to train POKéMON.$"

Route137_Text_ExTrainer12Defeat:
	.string "Wow your good at this.$"

Route137_Text_ExTrainer12PostBattle:
	.string "Hey go easy on the BOSS ok.\n"
	.string "He gets upset easily.$"

Route137_EventScript_ExTrainer13::
	trainerbattle_single TRAINER_HOENNEX_ROUTE137_COOPER, Route137_Text_ExTrainer13Intro, Route137_Text_ExTrainer13Defeat
	msgbox Route137_Text_ExTrainer13PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer13Intro:
	.string "Haha!\p"
	.string "You have fallen into our trap!$"

Route137_Text_ExTrainer13Defeat:
	.string "Oh no!$"

Route137_Text_ExTrainer13PostBattle:
	.string "You have bested us this time,\n"
	.string "but you will never stop the EVIL FOREST\l"
	.string "GANG!$"

Route137_EventScript_ExTrainer14::
	trainerbattle_single TRAINER_HOENNEX_ROUTE137_ALICE, Route137_Text_ExTrainer14Intro, Route137_Text_ExTrainer14Defeat
	msgbox Route137_Text_ExTrainer14PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer14Intro:
	.string "En garde!\n"
	.string "Hand over your treasure!$"

Route137_Text_ExTrainer14Defeat:
	.string "Oy vey!\n"
	.string "That didn’t go well...$"

Route137_Text_ExTrainer14PostBattle:
	.string "You’re not getting any of my treasure!\p"
	.string "Because I don’t have any...\n"
	.string "Our BOSS has much-o treasure!$"

Route137_EventScript_ExTrainer15::
	trainerbattle_single TRAINER_HOENNEX_ROUTE137_MAURICE, Route137_Text_ExTrainer15Intro, Route137_Text_ExTrainer15Defeat
	msgbox Route137_Text_ExTrainer15PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer15Intro:
	.string "Go! My creepie crawlies!$"

Route137_Text_ExTrainer15Defeat:
	.string "Jeepers creepers!$"

Route137_Text_ExTrainer15PostBattle:
	.string "There’s nothing more intimidating than\n"
	.string "BUGS!$"

Route137_EventScript_ExTrainer16::
	trainerbattle_single TRAINER_HOENNEX_ROUTE137_NORM, Route137_Text_ExTrainer16Intro, Route137_Text_ExTrainer16Defeat
	msgbox Route137_Text_ExTrainer16PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer16Intro:
	.string "WAH-HA-HA!\n"
	.string "So you’ve defeated my EVIL FOREST\l"
	.string "GANG! You’ve come far but be prepared\l"
	.string "to fall here!$"

Route137_Text_ExTrainer16Defeat:
	.string "But I had so many types of POKéMON...\n"
	.string "SNIFF...$"

Route137_Text_ExTrainer16PostBattle:
	.string "SNIFF... SNIFF...\p"
	.string "You beat us...$"

Route137_EventScript_ExNpc17::
	msgbox Route137_Text_ExNpc17, MSGBOX_NPC
	end

Route137_Text_ExNpc17:
	.string "BwaHaHa!!!\n"
	.string "Beware this is the EVIL FOREST GANG’S\l"
	.string "SECRET HIDEOUT!\p"
	.string "At the end of this dangerous path, a\n"
	.string "fantastic prize awaits.\p"
	.string "Enter...\n"
	.string "If you dare...\l"
	.string "Bwa Ha Ha Ha!!!$"

Route137_EventScript_ExNpc19::
	msgbox Route137_Text_ExNpc19, MSGBOX_NPC
	end

Route137_Text_ExNpc19:
	.string "Grumble...\p"
	.string "These kids cut down all these trees!\n"
	.string "’And what for!’ you ask?\p"
	.string "A silly club!$"

Route137_EventScript_ExNpc20::
	msgbox Route137_Text_ExNpc20, MSGBOX_NPC
	end

Route137_Text_ExNpc20:
	.string "We’re secretly building ships here!\p"
	.string "Don’t tell anybody!$"

Route137_EventScript_ExTrainer21::
	trainerbattle_single TRAINER_HOENNEX_ROUTE137_MICKEY, Route137_Text_ExTrainer21Intro, Route137_Text_ExTrainer21Defeat
	msgbox Route137_Text_ExTrainer21PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer21Intro:
	.string "Yeeaaarrrgggghhhhh!\p"
	.string "What ARR ya doing here!$"

Route137_Text_ExTrainer21Defeat:
	.string "What a bombardment!$"

Route137_Text_ExTrainer21PostBattle:
	.string "I’ll let yar pass if ye become a cabin\n"
	.string "boy!$"

Route137_EventScript_ExSign0::
	msgbox Route137_Text_ExSign0, MSGBOX_SIGN
	end

Route137_Text_ExSign0:
	.string "ROUTE 137\n"
	.string "{DOWN_ARROW} SLATEPORT CITY$"

Route137_EventScript_ExSign1::
	msgbox Route137_Text_ExSign1, MSGBOX_SIGN
	end

Route137_Text_ExSign1:
	.string "ROUTE 137\n"
	.string "{UP_ARROW} ROUTE 110$"


@ Eventos novos do Pokémon Emerald EX (mapa 0.61), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route137_EventScript_ExTrainer5::
	trainerbattle_double TRAINER_HOENNEX_ROUTE137_LILY_JEN, Route137_Text_ExTrainer5Intro, Route137_Text_ExTrainer5Defeat, Route137_Text_ExTrainer5NotEnough
	msgbox Route137_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ExTrainer5NotEnough:
	.string "I’d battle you if you had more POKéMON.$"

Route137_Text_ExTrainer5Intro:
	.string "Were gonna meet our friends in our\n"
	.string "clearing.$"

Route137_Text_ExTrainer5Defeat:
	.string "JEN: No fair!\p"
	.string "LILY: Wow, your strong!$"

Route137_Text_ExTrainer5PostBattle:
	.string "Don’t even try to battle our friends!$"

