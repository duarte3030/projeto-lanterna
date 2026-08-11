Route215_MapScripts::
	.byte 0

Route215_EventScript_BlackBelt::
	msgbox Route215_Text_BlackBelt, MSGBOX_NPC
	end

Route215_EventScript_Runner::
	msgbox Route215_Text_Runner, MSGBOX_NPC
	end

Route215_EventScript_Cooltrainer::
	msgbox Route215_Text_Cooltrainer, MSGBOX_NPC
	end

Route215_EventScript_Hiker::
	msgbox Route215_Text_Hiker, MSGBOX_NPC
	end

Route215_EventScript_TrainerTipsSign::
	msgbox Route215_Text_TrainerTipsSign, MSGBOX_SIGN
	end

Route215_Text_BlackBelt:
	.string "A steady stance is worth more than\n"
	.string "a strong punch. Remember that.$"

Route215_Text_Runner:
	.string "I run this route every morning.\n"
	.string "Keeps me and my POKéMON in shape\l"
	.string "for VEILSTONE.$"

Route215_Text_Cooltrainer:
	.string "This route sees a lot of TRAINERS\n"
	.string "heading to and from VEILSTONE CITY.\l"
	.string "Hope you're ready.$"

Route215_Text_Hiker:
	.string "The trail west leads back toward\n"
	.string "ROUTE 210. It's an easy walk from\l"
	.string "here on out.$"

Route215_Text_TrainerTipsSign:
	.string "TRAINER TIP:\n"
	.string "POKéMON get tired from battling\l"
	.string "too much. Give them a rest at a\l"
	.string "POKéMON CENTER!$"

Route215_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_DEREK, Route215_Text_Trainer1Intro, Route215_Text_Trainer1Defeat
	msgbox Route215_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer1Intro:
	.string "Check the sharpness of my fighting\nPokémon's moves.\p$"

Route215_Text_Trainer1Defeat:
	.string "You've dulled its sharpness...\n$"

Route215_Text_Trainer1Post:
	.string "Back to training for us!\n$"

Route215_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_GREGORY, Route215_Text_Trainer2Intro, Route215_Text_Trainer2Defeat
	msgbox Route215_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer2Intro:
	.string "You come along with your heart\npounding!\pYou think you can win like that?!\nHiyah!\p$"

Route215_Text_Trainer2Defeat:
	.string "Gurgle...\n$"

Route215_Text_Trainer2Post:
	.string "If I lose here, I wouldn't stand a\nchance at the Battle Frontier.\pNot against those hard-core pros,\nI wouldn't!\n$"

Route215_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_NATHANIEL, Route215_Text_Trainer3Intro, Route215_Text_Trainer3Defeat
	msgbox Route215_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer3Intro:
	.string "Every drop of sweat I shed makes\nme that much stronger!\p$"

Route215_Text_Trainer3Defeat:
	.string "I should be lighter by the amount of\nsweat I just shed!\p$"

Route215_Text_Trainer3Post:
	.string "It's time for another workout.\nThe more I sweat, the tougher I get!\n$"


Route215_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_JOGGER_SCOTT, Route215_Text_Trainer4Intro, Route215_Text_Trainer4Defeat
	msgbox Route215_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer4Intro:
	.string "Hufff-huff, huff-huff.\nWant-huff a battle-huff?\p$"

Route215_Text_Trainer4Defeat:
	.string "Huff-huff, we-huff lose-huff.\n$"

Route215_Text_Trainer4Post:
	.string "Bye-huff now-huff.\nHuff-huff, huff-huff.\n$"

Route215_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_CALVIN, Route215_Text_Trainer5Intro, Route215_Text_Trainer5Defeat
	msgbox Route215_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer5Intro:
	.string "I'm a treasure hunter.\pToday, the loot is a victory from\nyou!\p$"

Route215_Text_Trainer5Defeat:
	.string "I can't win.\nYou're too strong for me to win.\n$"

Route215_Text_Trainer5Post:
	.string "If one's after treasures, maybe the\nUnderground is the better choice.\n$"

Route215_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_DENNIS, Route215_Text_Trainer6Intro, Route215_Text_Trainer6Defeat
	msgbox Route215_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer6Intro:
	.string "I'll take on anyone!\nIt can only make me stronger!\p$"

Route215_Text_Trainer6Defeat:
	.string "You won and I lost, but the both of\nus gained something from this.\n$"

Route215_Text_Trainer6Post:
	.string "In a Pokémon battle, it doesn't\nmatter how old or young you are.\pYour gender doesn't matter, either.\nNothing like that means anything!\n$"

Route215_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MAYA, Route215_Text_Trainer7Intro, Route215_Text_Trainer7Defeat
	msgbox Route215_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer7Intro:
	.string "I'm taking the Veilstone Gym\nchallenge. But first...\p$"

Route215_Text_Trainer7Defeat:
	.string "...My confidence is crushed.\n$"

Route215_Text_Trainer7Post:
	.string "I think about Pokémon all day long.\nI was confident, you know.\n$"

Route215_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_JOGGER_CRAIG, Route215_Text_Trainer8Intro, Route215_Text_Trainer8Defeat
	msgbox Route215_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route215_Text_Trainer8Intro:
	.string "If I battle now, won't it mess up my\nusual pace?\p$"

Route215_Text_Trainer8Defeat:
	.string "My pace is completely off...\n$"

Route215_Text_Trainer8Post:
	.string "Sticking to one's own goal is more\nimportant than it seems.\pIf you match your goal with someone\nelse, you'll lose your identity.\n$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route215_EventScript_Placa1::
	msgbox Route215_Text_Placa1, MSGBOX_SIGN
	end

Route215_Text_Placa1:
	.string "Celestic Town\nSolaceon Town$"

Route215_EventScript_Placa2::
	msgbox Route215_Text_Placa2, MSGBOX_SIGN
	end

Route215_Text_Placa2:
	.string "Rt. 215\nVeilstone City$"

Route215_EventScript_Placa3::
	msgbox Route215_Text_Placa3, MSGBOX_SIGN
	end

Route215_Text_Placa3:
	.string "Trainer Tips\pPokémon attacks are classified as\nbeing either physical or special.\pA physical attack is based on the\nAttack stat of the Pokémon.\pLikewise, a special attack is based\non the Special Attack stat.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route215_EventScript_Npc1::
	msgbox Route215_Text_Npc1, MSGBOX_NPC
	end

Route215_Text_Npc1:
	.string "Do unto others as they do unto\nyou... Yup, it's Payback!\pIt's good for Pokémon battles,\nbut if you do that in real life...\pThere'll be no end to the fighting,\nthat's for sure.$"
