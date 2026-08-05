@ Armazem da Galactica, atras do QG de Veilstone.
@ Texto de pret/pokeplatinum, res/text/veilstone_city_galactic_warehouse.json.
@ Layout: o saguao de concurso descartado de Fallarbor, que estava sobrando no
@ repo sem nenhum mapa apontando para ele.
@
@ ponytail: a Storage Key e a HM Fly do original ficaram de fora. Item-chave novo
@ e flag de "ja peguei" nao cabem nesta tarefa (nao posso criar flag), entao o
@ Looker abre a porta de graca na fala e o item nao e dado. Pendencia registrada.

VeilstoneCity_GalacticWarehouse_MapScripts::
	.byte 0

VeilstoneCity_GalacticWarehouse_EventScript_Looker::
	lock
	faceplayer
	msgbox VeilstoneCity_GalacticWarehouse_Text_IHaveKeptYouWaiting, MSGBOX_DEFAULT
	msgbox VeilstoneCity_GalacticWarehouse_Text_IWillUseTheStorageKey, MSGBOX_DEFAULT
	msgbox VeilstoneCity_GalacticWarehouse_Text_WeDidntLearnMuch, MSGBOX_DEFAULT
	release
	end

VeilstoneCity_GalacticWarehouse_EventScript_RustyDoor::
	msgbox VeilstoneCity_GalacticWarehouse_Text_ItNeedsASpecialKey, MSGBOX_SIGN
	end

VeilstoneCity_GalacticWarehouse_Text_IHaveKeptYouWaiting:
	.string "Looker: Ah, hello!\n"
	.string "I have kept you waiting.$"

VeilstoneCity_GalacticWarehouse_Text_IWillUseTheStorageKey:
	.string "Looker: I will use this Storage Key\n"
	.string "I have obtained from the Team\l"
	.string "Galactic...\p"
	.string "...Ker-chunk!\p"
	.string "Yes!\n"
	.string "It is opened!$"

VeilstoneCity_GalacticWarehouse_Text_WeDidntLearnMuch:
	.string "Looker: So, we did not learn very\n"
	.string "much from this exercise...\l"
	.string "No matter.\p"
	.string "What concerns me is what I have\n"
	.string "overheard in the Game Corner.\p"
	.string "The Team Galactic has transported\n"
	.string "something to Pastoria City.\p"
	.string "What they are up to, I do not\n"
	.string "know, but I have bad feelings\l"
	.string "about it.$"

VeilstoneCity_GalacticWarehouse_Text_ItNeedsASpecialKey:
	.string "The rust-encrusted door is locked.\n"
	.string "It appears to take a special key.$"
