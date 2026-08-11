Route209LostTower4F_MapScripts::
	.byte 0

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route209LostTower4F_EventScript_PokefanRebekah::
	trainerbattle_single TRAINER_SINNOH_POKEFAN_REBEKAH, Route209LostTower4F_Text_PokefanRebekahIntro, Route209LostTower4F_Text_PokefanRebekahDefeat
	msgbox Route209LostTower4F_Text_PokefanRebekahPost, MSGBOX_AUTOCLOSE
	end

Route209LostTower4F_Text_PokefanRebekahIntro:
	.string "I need to shake off my sorrow...\nPlease, battle with me!$"

Route209LostTower4F_Text_PokefanRebekahDefeat:
	.string "My sorrow has deepened...$"

Route209LostTower4F_Text_PokefanRebekahPost:
	.string "I won't ever forget the Pokémon that\nI've spent time with, however fleeting.$"

Route209LostTower4F_EventScript_YoungCoupleTrainerMike::
	trainerbattle_double TRAINER_SINNOH_YOUNG_COUPLE_MIKE_AND_NAT, Route209LostTower4F_Text_YoungCoupleTrainerMikeIntro, Route209LostTower4F_Text_YoungCoupleTrainerMikeDefeat, Route209LostTower4F_Text_YoungCoupleTrainerMikeNoPartner
	msgbox Route209LostTower4F_Text_YoungCoupleTrainerMikePost, MSGBOX_AUTOCLOSE
	end

Route209LostTower4F_Text_YoungCoupleTrainerMikeIntro:
	.string "Mike: I can't embarrass myself again.\nNot in front of my girlfriend!$"

Route209LostTower4F_Text_YoungCoupleTrainerMikeDefeat:
	.string "Mike: Awww, jeez.\nMan, that's a downer...$"

Route209LostTower4F_Text_YoungCoupleTrainerMikePost:
	.string "Mike: Coming here again brings back\nall kinds of memories of me and Nat.$"

Route209LostTower4F_Text_YoungCoupleTrainerMikeNoPartner:
	.string "Mike: You can't battle with us.\nNot with one Pokémon, anyway.$"

Route209LostTower4F_EventScript_YoungCoupleTrainerNat::
	trainerbattle_double TRAINER_SINNOH_YOUNG_COUPLE_MIKE_AND_NAT, Route209LostTower4F_Text_YoungCoupleTrainerNatIntro, Route209LostTower4F_Text_YoungCoupleTrainerNatDefeat, Route209LostTower4F_Text_YoungCoupleTrainerNatNoPartner
	msgbox Route209LostTower4F_Text_YoungCoupleTrainerNatPost, MSGBOX_AUTOCLOSE
	end

Route209LostTower4F_Text_YoungCoupleTrainerNatIntro:
	.string "Nat: I don't want to look bad again.\nNot when my boyfriend is watching!$"

Route209LostTower4F_Text_YoungCoupleTrainerNatDefeat:
	.string "Nat: This makes me feel hollow\ninside... Oh, so hollow...$"

Route209LostTower4F_Text_YoungCoupleTrainerNatPost:
	.string "Nat: The Pokémon that brought me and\nMike together is buried here...$"

Route209LostTower4F_Text_YoungCoupleTrainerNatNoPartner:
	.string "Nat: You do have at least two\nPokémon, don't you?$"

Route209LostTower4F_EventScript_PaBob::
	trainerbattle_double TRAINER_SINNOH_BELLE_AND_PA_BETH_AND_BOB, Route209LostTower4F_Text_PaBobIntro, Route209LostTower4F_Text_PaBobDefeat, Route209LostTower4F_Text_PaBobNoPartner
	msgbox Route209LostTower4F_Text_PaBobPost, MSGBOX_AUTOCLOSE
	end

Route209LostTower4F_Text_PaBobIntro:
	.string "It makes no difference where we are.\pIf you have Pokémon with you,\nI reckon you ought to battle.$"

Route209LostTower4F_Text_PaBobDefeat:
	.string "You've got a lot of giddyap and go\nin you!$"

Route209LostTower4F_Text_PaBobPost:
	.string "Over a long life, you'll be certain\nto have some sad farewells.\pBut I reckon there are also some\nnew beginnings.$"

Route209LostTower4F_Text_PaBobNoPartner:
	.string "Hahaha! I'm afraid y'all are no match\nfor us with jus' one of them Pokémon!$"

Route209LostTower4F_EventScript_BelleBeth::
	trainerbattle_double TRAINER_SINNOH_BELLE_AND_PA_BETH_AND_BOB, Route209LostTower4F_Text_BelleBethIntro, Route209LostTower4F_Text_BelleBethDefeat, Route209LostTower4F_Text_BelleBethNoPartner
	msgbox Route209LostTower4F_Text_BelleBethPost, MSGBOX_AUTOCLOSE
	end

Route209LostTower4F_Text_BelleBethIntro:
	.string "My Pokémon is a lively one.\nLemme show you how much!$"

Route209LostTower4F_Text_BelleBethDefeat:
	.string "Well! Aren't you the lively one!$"

Route209LostTower4F_Text_BelleBethPost:
	.string "Them graves here in Lost Tower...\nRight'n here, inside my heart...\pThose are the places where my\nPokémon remain...$"

Route209LostTower4F_Text_BelleBethNoPartner:
	.string "You haven't got yerself two\nPokémon?$"
