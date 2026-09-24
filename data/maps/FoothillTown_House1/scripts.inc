@ FoothillTown_House1: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 17.3) por dev_scripts/copia_planta_ex.py.

FoothillTown_House1_MapScripts::
	.byte 0

@ Presente do EX (0x83516AA), reescrito: a moça dá o DREEPY dela uma vez e sai da casa.
FoothillTown_House1_EventScript_Girl::
	lock
	faceplayer
	msgbox FoothillTown_House1_Text_TakeMyPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, FoothillTown_House1_EventScript_GiveDreepy
	msgbox FoothillTown_House1_Text_Reconsider, MSGBOX_DEFAULT
	release
	end

FoothillTown_House1_EventScript_GiveDreepy::
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_DREEPY
	givemon SPECIES_DREEPY, 107
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, FoothillTown_House1_EventScript_DreepyParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, FoothillTown_House1_EventScript_DreepyPC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

FoothillTown_House1_EventScript_DreepyParty::
	call FoothillTown_House1_EventScript_DreepyFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FoothillTown_House1_EventScript_DreepyGiven
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto FoothillTown_House1_EventScript_DreepyGiven
	end

FoothillTown_House1_EventScript_DreepyPC::
	call FoothillTown_House1_EventScript_DreepyFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FoothillTown_House1_EventScript_DreepyToPC
	call Common_EventScript_NameReceivedBoxMon
	goto FoothillTown_House1_EventScript_DreepyToPC
	end

FoothillTown_House1_EventScript_DreepyToPC::
	call Common_EventScript_TransferredToPC
	goto FoothillTown_House1_EventScript_DreepyGiven
	end

FoothillTown_House1_EventScript_DreepyFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_DREEPY
	playfanfare MUS_OBTAIN_ITEM
	message FoothillTown_House1_Text_ObtainedDreepy
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_DREEPY
	return

FoothillTown_House1_EventScript_DreepyGiven::
	fadescreen FADE_TO_BLACK
	setflag FLAG_RECEIVED_HOENNEX_FOOTHILL_DREEPY
	removeobject LOCALID_FOOTHILL_DREEPY_GIRL
	fadescreen FADE_FROM_BLACK
	release
	end

FoothillTown_House1_Text_TakeMyPokemon:
	.string "Are you a POKéMON TRAINER?\p"
	.string "Please, I can’t take care of my beloved\n"
	.string "POKéMON anymore, would you take it with\l"
	.string "you?$"

FoothillTown_House1_Text_Reconsider:
	.string "Please reconsider...$"

FoothillTown_House1_Text_ObtainedDreepy:
	.string "{PLAYER} obtained a DREEPY!$"

