@ DriftveilShelter do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_DriftveilShelter_MapScripts::
	.byte 0

Unova_DriftveilShelter_EventScript_Npc0::
	msgbox Unova_DriftveilShelter_Text_DriftveilShelterPostgameRoodInitialText, MSGBOX_NPC
	end

Unova_DriftveilShelter_EventScript_Npc3::
	msgbox Unova_DriftveilShelter_Text_DriftveilShelterGrannyIntroText, MSGBOX_NPC
	end

Unova_DriftveilShelter_EventScript_Npc4::
	goto Unova_DriftveilShelter_EventScript_HUGH_TEPIG


Unova_DriftveilShelter_Text_DriftveilShelterPostgameRoodInitialText::
	.string "Ah, {PLAYER}! It's"
	.string "\ngood to see you."
	.string "\pI want to thank"
	.string "\nyou for your help."
	.string "\pINFER came back"
	.string "\nhome the other"
	.string "\pday. We may not"
	.string "\nhave reconciled"
	.string "\pall of our differ-"
	.string "\nences yet, but at"
	.string "\pleast I know she"
	.string "\nis safe."
	.string "\pFor that, I owe"
	.string "\nyou my deepest"
	.string "\lgratitude.$"

Unova_DriftveilShelter_Text_DriftveilShelterGrannyIntroText::
	.string "Why hello there,"
	.string "\nyoung trainer."
	.string "\pHere at the POKé-"
	.string "\nMON SHELTER, we"
	.string "\ptry to find homes"
	.string "\nfor abandoned"
	.string "\lPOKéMON."
	.string "\pI know you must be"
	.string "\na kind trainer if"
	.string "\lROOD trusts you."
	.string "\pThere's a POKéMON"
	.string "\nhere that we've"
	.string "\phad a hard time"
	.string "\nfinding a home"
	.string "\lfor."
	.string "\pHow would you like"
	.string "\nto take it with"
	.string "\lyou?$"

Unova_DriftveilShelter_Text_DriftveilShelterHughRematchText::
	.string "Hey, {PLAYER}!"
	.string "\pI've been thinking"
	.string "\non what I need to"
	.string "\pbecome stronger,"
	.string "\nand I'm ready to"
	.string "\ptest out what I've"
	.string "\ncome up with. Come"
	.string "\lon, let's go!$"

@ >>> cena importada por dev_scripts/importa_chefes_faltantes.py >>>
Unova_DriftveilShelter_EventScript_HUGH_TEPIG::
	trainerbattle_single TRAINER_UNOVA_HUGH_TEPIG, Unova_DriftveilShelter_Text_DriftveilShelterHughRematchText, Unova_DriftveilShelter_Text_HUGH_TEPIGBeaten
	msgbox Unova_DriftveilShelter_Text_HUGH_TEPIGDepois, MSGBOX_DEFAULT
	release
	end

Unova_DriftveilShelter_Text_HUGH_TEPIGBeaten::
	.string "Ugh… This power.$"

Unova_DriftveilShelter_Text_HUGH_TEPIGDepois::
	.string "Hmph… You really\n"
	.string "are strong enough\l"
	.string "to have bested\l"
	.string "TEAM PLASMA.\p"
	.string "You and I should\n"
	.string "have a rematch\l"
	.string "someday.$"
@ <<< cena importada por dev_scripts/importa_chefes_faltantes.py <<<
