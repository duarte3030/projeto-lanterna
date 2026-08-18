@ Armazem da Galactica, atras do QG de Veilstone.
@ Texto de pret/pokeplatinum, res/text/veilstone_city_galactic_warehouse.json.
@ Layout: o saguao de concurso descartado de Fallarbor, que estava sobrando no
@ repo sem nenhum mapa apontando para ele.
@
@ ponytail: a Storage Key e a HM Fly entraram, e nenhuma das duas custou flag ou
@ item novo.
@ - A chave e ITEM_STORAGE_KEY, a de Hoenn: ja existe, ja se chama Storage Key e
@   ja e item-chave. Criar uma segunda com o mesmo nome so encheria a mochila.
@   Efeito colateral conhecido: quem guardou a chave do Navio Abandonado abre a
@   porta enferrujada antes de falar com o Looker. Chave e chave, fica assim.
@ - "Ja peguei a HM" e FLAG_RECEIVED_HM_FLY, que o jogo ja tem e ninguem le em
@   lugar nenhum (so Route119 a liga). Quem ganhou Fly em Hoenn acha o armazem
@   vazio, que e a resposta certa: ele ja voa.
@ - "Ja ganhei a chave" nao precisa de flag: checkitem responde sozinho.

VeilstoneCity_GalacticWarehouse_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
VeilstoneCity_GalacticWarehouse_EventScript_CoordEvent_LookerOpenDoor::
	@ TODO S5: cena da fonte, rotulo VeilstoneCityGalacticWarehouse_CoordEvent_LookerOpenDoor
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

VeilstoneCity_GalacticWarehouse_EventScript_Looker::
	lock
	faceplayer
	checkitem ITEM_STORAGE_KEY
	goto_if_eq VAR_RESULT, TRUE, VeilstoneCity_GalacticWarehouse_EventScript_LookerAfter
	msgbox VeilstoneCity_GalacticWarehouse_Text_IHaveKeptYouWaiting, MSGBOX_DEFAULT
	msgbox VeilstoneCity_GalacticWarehouse_Text_IWillUseTheStorageKey, MSGBOX_DEFAULT
	giveitem ITEM_STORAGE_KEY
	goto_if_eq VAR_RESULT, FALSE, VeilstoneCity_GalacticWarehouse_EventScript_NoRoomForKey
	msgbox VeilstoneCity_GalacticWarehouse_Text_YouHadBetterKeepIt, MSGBOX_DEFAULT
	msgbox VeilstoneCity_GalacticWarehouse_Text_WeDidntLearnMuch, MSGBOX_DEFAULT
	release
	end

VeilstoneCity_GalacticWarehouse_EventScript_LookerAfter::
	msgbox VeilstoneCity_GalacticWarehouse_Text_WeDidntLearnMuch, MSGBOX_DEFAULT
	release
	end

VeilstoneCity_GalacticWarehouse_EventScript_NoRoomForKey::
	msgbox VeilstoneCity_GalacticWarehouse_Text_YourBagIsFull, MSGBOX_DEFAULT
	release
	end

VeilstoneCity_GalacticWarehouse_EventScript_RustyDoor::
	lockall
	goto_if_set FLAG_RECEIVED_HM_FLY, VeilstoneCity_GalacticWarehouse_EventScript_DoorIsEmpty
	checkitem ITEM_STORAGE_KEY
	goto_if_eq VAR_RESULT, FALSE, VeilstoneCity_GalacticWarehouse_EventScript_DoorIsLocked
	msgbox VeilstoneCity_GalacticWarehouse_Text_UsedTheStorageKey, MSGBOX_DEFAULT
	giveitem ITEM_HM_FLY
	goto_if_eq VAR_RESULT, FALSE, VeilstoneCity_GalacticWarehouse_EventScript_NoRoomForHM
	setflag FLAG_RECEIVED_HM_FLY
	msgbox VeilstoneCity_GalacticWarehouse_Text_FlyExplained, MSGBOX_DEFAULT
	releaseall
	end

VeilstoneCity_GalacticWarehouse_EventScript_DoorIsLocked::
	msgbox VeilstoneCity_GalacticWarehouse_Text_ItNeedsASpecialKey, MSGBOX_DEFAULT
	releaseall
	end

VeilstoneCity_GalacticWarehouse_EventScript_DoorIsEmpty::
	msgbox VeilstoneCity_GalacticWarehouse_Text_NothingLeftInside, MSGBOX_DEFAULT
	releaseall
	end

VeilstoneCity_GalacticWarehouse_EventScript_NoRoomForHM::
	msgbox VeilstoneCity_GalacticWarehouse_Text_YourBagIsFull, MSGBOX_DEFAULT
	releaseall
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

VeilstoneCity_GalacticWarehouse_Text_YouHadBetterKeepIt:
	.string "Looker: The rusted door at the back,\n"
	.string "that one I cannot manage.\p"
	.string "You had better keep the key.\n"
	.string "My hands are full as they are.$"

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

VeilstoneCity_GalacticWarehouse_Text_UsedTheStorageKey:
	.string "{PLAYER} used the Storage Key on\n"
	.string "the rust-encrusted door.\p"
	.string "There is a single crate inside.$"

VeilstoneCity_GalacticWarehouse_Text_FlyExplained:
	.string "Fly carries a Pokémon and its\n"
	.string "Trainer to any town they have\l"
	.string "already visited, in one hop.$"

VeilstoneCity_GalacticWarehouse_Text_NothingLeftInside:
	.string "The rust-encrusted door stands\n"
	.string "open. The crate inside is empty.$"

VeilstoneCity_GalacticWarehouse_Text_YourBagIsFull:
	.string "There is no room left in the Bag.$"
