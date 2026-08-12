Route209_MapScripts::
	.byte 0

Route209_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BREEDER_ALBERT, Route209_Text_Trainer1Intro, Route209_Text_Trainer1Defeat
	msgbox Route209_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer1Intro:
	.string "Let me see how much you've raised\n"
	.string "your Pokémon.$"

Route209_Text_Trainer1Defeat:
	.string "Good stuff! Your Pokémon are in\n"
	.string "impeccable condition.$"

Route209_Text_Trainer1Post:
	.string "It's obvious you raise your Pokémon\n"
	.string "with a lot of love.$"

Route209_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_BREEDER_JENNIFER, Route209_Text_Trainer2Intro, Route209_Text_Trainer2Defeat
	msgbox Route209_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer2Intro:
	.string "Please, let me battle the Pokémon\n"
	.string "you've raised!$"

Route209_Text_Trainer2Defeat:
	.string "Giggle...\n"
	.string "They're raised with a lot of care!$"

Route209_Text_Trainer2Post:
	.string "Raise your Pokémon with lots of love,\n"
	.string "and they'll bond closely with you.$"

Route209_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_COWGIRL_SHELLEY, Route209_Text_Trainer3Intro, Route209_Text_Trainer3Defeat
	msgbox Route209_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer3Intro:
	.string "Say, honey, where'd you come from?\n"
	.string "What kinds of Pokémon are you with?$"

Route209_Text_Trainer3Defeat:
	.string "Fancy folks like you have fancy\n"
	.string "Pokémon too, it looks like.$"

Route209_Text_Trainer3Post:
	.string "While working the ranch, I get to raise\n"
	.string "my Pokémon, too.\pI'd say it's the best of both worlds!$"

Route209_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_JOGGER_RICHARD, Route209_Text_Trainer4Intro, Route209_Text_Trainer4Defeat
	msgbox Route209_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer4Intro:
	.string "I jog every morning to keep my\n"
	.string "Pokémon fit.$"

Route209_Text_Trainer4Defeat:
	.string "Oops!\n"
	.string "You threw off my running rhythm.$"

Route209_Text_Trainer4Post:
	.string "Nothing beats being fit and healthy!\pCome on, won't you run with me?\n"
	.string "To a better tomorrow!$"

Route209_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_JOGGER_RAUL, Route209_Text_Trainer5Intro, Route209_Text_Trainer5Defeat
	msgbox Route209_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer5Intro:
	.string "Jogging is about rhythm.\n"
	.string "Battling is about rhythm, too!$"

Route209_Text_Trainer5Defeat:
	.string "It's a goal of sorts, I'd say!$"

Route209_Text_Trainer5Post:
	.string "If I get out of rhythm, I can't get my\n"
	.string "act together.$"

Route209_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_POKE_KID_DANIELLE, Route209_Text_Trainer6Intro, Route209_Text_Trainer6Defeat
	msgbox Route209_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer6Intro:
	.string "Hi, hi!\n"
	.string "I'm a Pokémon!$"

Route209_Text_Trainer6Defeat:
	.string "So sad...\n"
	.string "So bitter...$"

Route209_Text_Trainer6Post:
	.string "I don't want to be a Trainer.\n"
	.string "I want to be a Pokémon!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route209_EventScript_Placa1::
	msgbox Route209_Text_Placa1, MSGBOX_SIGN
	end

Route209_Text_Placa1:
	.string "Rt. 209\nHearthome City$"

Route209_EventScript_Placa2::
	msgbox Route209_Text_Placa2, MSGBOX_SIGN
	end

Route209_Text_Placa2:
	.string "Rt. 209\nSolaceon Town$"

Route209_EventScript_Placa3::
	msgbox Route209_Text_Placa3, MSGBOX_SIGN
	end

Route209_Text_Placa3:
	.string "Trainer Tips\pYou may register one of the Key\nItems in your Bag for instant use.\pSimply press the Y Button to use the\nregistered item instantly.$"

Route209_EventScript_Placa6::
	msgbox Route209_Text_Placa6, MSGBOX_SIGN
	end

Route209_Text_Placa6:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

Route209_EventScript_Placa7::
	msgbox Route209_Text_Placa7, MSGBOX_SIGN
	end

Route209_Text_Placa7:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

Route209_EventScript_Placa8::
	msgbox Route209_Text_Placa8, MSGBOX_SIGN
	end

Route209_Text_Placa8:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

Route209_EventScript_Placa9::
	msgbox Route209_Text_Placa9, MSGBOX_SIGN
	end

Route209_Text_Placa9:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route209_EventScript_Npc1::
	msgbox Route209_Text_Npc1, MSGBOX_NPC
	end

Route209_Text_Npc1:
	.string "Where departed Pokémon sleep...\nThis is the Lost Tower.$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route209_EventScript_TwinEmma::
	trainerbattle_double TRAINER_SINNOH_TWINS_EMMA_AND_LIL, Route209_Text_TwinEmmaIntro, Route209_Text_TwinEmmaDefeat, Route209_Text_TwinEmmaNoPartner
	msgbox Route209_Text_TwinEmmaPost, MSGBOX_AUTOCLOSE
	end

Route209_Text_TwinEmmaIntro:
	.string "Emma: We're tough because we battle\ntogether!$"

Route209_Text_TwinEmmaDefeat:
	.string "Emma: Waaah!$"

Route209_Text_TwinEmmaPost:
	.string "Emma: That was awesome!\nAre you maybe a Pokémon genius?\pYou're well deserving of respect!$"

Route209_Text_TwinEmmaNoPartner:
	.string "We won't talk to people who have only\none Pokémon!$"

Route209_EventScript_YoungCoupleTrainerSue::
	trainerbattle_double TRAINER_SINNOH_YOUNG_COUPLE_TY_AND_SUE, Route209_Text_YoungCoupleTrainerSueIntro, Route209_Text_YoungCoupleTrainerSueDefeat, Route209_Text_YoungCoupleTrainerSueNoPartner
	msgbox Route209_Text_YoungCoupleTrainerSuePost, MSGBOX_AUTOCLOSE
	end

Route209_Text_YoungCoupleTrainerSueIntro:
	.string "Sue: Huh?\nYou want to battle with me?\pI will if I can team with Ty!$"

Route209_Text_YoungCoupleTrainerSueDefeat:
	.string "Sue: I'm sorry, Ty!$"

Route209_Text_YoungCoupleTrainerSuePost:
	.string "Sue: We lost... Ty, I need a hug\nto make it all better!$"

Route209_Text_YoungCoupleTrainerSueNoPartner:
	.string "Sue: I only want to battle next to my\nsweet Ty.\pDon't you have two Pokémon?$"

Route209_EventScript_YoungCoupleTrainerTy::
	trainerbattle_double TRAINER_SINNOH_YOUNG_COUPLE_TY_AND_SUE, Route209_Text_YoungCoupleTrainerTyIntro, Route209_Text_YoungCoupleTrainerTyDefeat, Route209_Text_YoungCoupleTrainerTyNoPartner
	msgbox Route209_Text_YoungCoupleTrainerTyPost, MSGBOX_AUTOCLOSE
	end

Route209_Text_YoungCoupleTrainerTyIntro:
	.string "Ty: You're not supposed to intrude\non my time with Sue!$"

Route209_Text_YoungCoupleTrainerTyDefeat:
	.string "Ty: I only have eyes for Sue.\nMaybe that's why we lost?$"

Route209_Text_YoungCoupleTrainerTyPost:
	.string "Ty: Sue, even in defeat, you're\nso beautiful...!$"

Route209_Text_YoungCoupleTrainerTyNoPartner:
	.string "Ty: I don't want to do anything\nwithout Sue...\pBring two Pokémon at least, OK?$"

Route209_EventScript_TwinLil::
	trainerbattle_double TRAINER_SINNOH_TWINS_EMMA_AND_LIL, Route209_Text_TwinLilIntro, Route209_Text_TwinLilDefeat, Route209_Text_TwinLilNoPartner
	msgbox Route209_Text_TwinLilPost, MSGBOX_AUTOCLOSE
	end

Route209_Text_TwinLilIntro:
	.string "Lil: We're gonna crunch and\nmunch you all up!$"

Route209_Text_TwinLilDefeat:
	.string "Lil: Hwaaah!$"

Route209_Text_TwinLilPost:
	.string "Lil: We're going to be super-strong\nTrainers like you!\pI just decided now!\nPlease cheer for us!$"

Route209_Text_TwinLilNoPartner:
	.string "We don't talk to people who have only\none Pokémon!$"

@ Good Rod da Route 209, cena portada do pokeplatinum
@ (scripts_route_209.s:132 Route209_Fisherman, textos de res/text/route_209.json).
@ Piloto do bloco B6: primeira cena de Sinnoh que nao e so fala.
@
@ O que muda de forma em relacao a fonte, e por que:
@ - o menu sim/nao dela (`ShowYesNoMenu VAR_RESULT`) vira `MSGBOX_YESNO`, e o
@   `Common_GiveItemQuantity` vira `giveitem`, que ja mostra a fanfarra e o
@   "obtained", e ja devolve FALSE com a mochila cheia.
@ - `BufferItemNameWithArticle` + `CapitalizeFirstLetter` nao existem aqui. Em
@   ingles o resultado deles para este item e exatamente "The Good Rod", entao o
@   artigo fica escrito no texto e a var carrega so o nome.
@ - a flag e FLAG_RECEBEU_GOOD_ROD_SINNOH, da faixa nova, e NAO a
@   FLAG_RECEIVED_GOOD_ROD do vanilla, que e do pescador da Route 118 de Hoenn.
@   O `checkitem` ao lado dela e o que impede a cena de tentar dar uma segunda
@   vara a quem ja pegou a de Hoenn (seria mochila cheia na cara do jogador).
Route209_EventScript_FishermanGoodRod::
	lock
	faceplayer
	bufferitemname STR_VAR_1, ITEM_GOOD_ROD
	goto_if_set FLAG_RECEBEU_GOOD_ROD_SINNOH, Route209_EventScript_GoodRodExplainAsk
	checkitem ITEM_GOOD_ROD
	goto_if_eq VAR_RESULT, TRUE, Route209_EventScript_GoodRodExplainAsk
	msgbox Route209_Text_GoodRodIsReallyGood, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route209_EventScript_GoodRodRefused
	msgbox Route209_Text_GoodRodTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_GOOD_ROD
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEBEU_GOOD_ROD_SINNOH
	goto Route209_EventScript_GoodRodExplainAsk

Route209_EventScript_GoodRodExplainAsk::
	msgbox Route209_Text_GoodRodExplainAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route209_EventScript_GoodRodReel
	msgbox Route209_Text_GoodRodExplain, MSGBOX_DEFAULT
	release
	end

Route209_EventScript_GoodRodReel::
	msgbox Route209_Text_GoodRodReel, MSGBOX_DEFAULT
	release
	end

Route209_EventScript_GoodRodRefused::
	msgbox Route209_Text_GoodRodRefused, MSGBOX_DEFAULT
	release
	end

Route209_Text_GoodRodIsReallyGood:
	.string "Hmm!\nThe {STR_VAR_1} is really good!\pWouldn't you agree?$"

Route209_Text_GoodRodTakeThis:
	.string "Hmm!\nWe're of identical minds!\pHmm!\nTake this {STR_VAR_1}!$"

Route209_Text_GoodRodExplainAsk:
	.string "Try fishing wherever there is\na body of water.\pOh, incidentally, do you need me to\nexplain how to use that fishing rod?$"

Route209_Text_GoodRodExplain:
	.string "First, you face any body of water,\nthen you use your fishing rod.\pNext, you must focus!\nIf a Pokémon bites, '!' appears.\pThat's your cue to reel it in!$"

Route209_Text_GoodRodReel:
	.string "When you're fishing for Pokémon,\nthe first hurdle is getting a bite.\pWhen you start to reel that Pokémon\nin, you've got to battle it.\pSo, fishing gives you twice the fun!$"

Route209_Text_GoodRodRefused:
	.string "You don't like to fish?$"
