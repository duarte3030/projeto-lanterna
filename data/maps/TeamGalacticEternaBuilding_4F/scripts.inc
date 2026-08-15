@ Predio da Equipe Galactica em Eterna, 4F: a Comandante Jupiter.
@ Texto de pret/pokeplatinum, res/text/team_galactic_eterna_building_4f.json.
@ Layout emprestado do Mt. Pyre 5F.
@
@ TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING NAO existe ainda: esta tarefa
@ nao pode mexer em include/constants/opponents.h nem em src/data/trainers*.party.
@ A cena esta montada com o nome que o treinador DEVE ter, e o time sugerido esta
@ em PENDENCIAS-GALACTICA.md. Sem essa entrada o link falha, de proposito, em vez
@ de reusar um treinador errado so para compilar.
@
@ O Clefairy roubado do dono da Loja de Bicicletas nao vira objeto: nao existe
@ sprite de Clefairy fora de #if IS_FRLG nesta build. O dono aparece livre e a
@ fala de agradecimento cobre a cena.

TeamGalacticEternaBuilding_4F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TeamGalacticEternaBuilding_4F_OnTransition
	.byte 0

@ ponytail: a cena e a flag sao a mesma coisa. Os reféns (LOCALID_CLEFAIRY,
@ LOCALID_POKEFAN_M e LOCALID_BUNEARY na fonte, hidden_flag
@ FLAG_HIDE_TEAM_GALACTIC_ETERNA_BUILDING_4F_HOSTAGES) nascem enquanto a Jupiter
@ nao caiu, e somem depois; mesma FLAG_GALACTICA_ETERNA que o 1F/2F/3F e a rua de
@ Eterna ja usam, porque e o mesmo marco. Zero var. LOCALID_BUNEARY ficou de fora:
@ OBJ_EVENT_GFX_BUNEARY nao existe em object_event_graphics_info_pointers.h nesta
@ ROM e a tabela de trocas nao tem substituto.
TeamGalacticEternaBuilding_4F_OnTransition:
	call_if_defeated TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING, TeamGalacticEternaBuilding_4F_EventScript_HideGalactica_eterna
	end

TeamGalacticEternaBuilding_4F_EventScript_HideGalactica_eterna::
	setflag FLAG_GALACTICA_ETERNA
	return

TeamGalacticEternaBuilding_4F_EventScript_Jupiter::
	trainerbattle_single TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING, TeamGalacticEternaBuilding_4F_Text_IWillDealWithYou, TeamGalacticEternaBuilding_4F_Text_WellArentYouTough, TeamGalacticEternaBuilding_4F_EventScript_JupiterDefeated
	msgbox TeamGalacticEternaBuilding_4F_Text_LastWarning, MSGBOX_AUTOCLOSE
	end

TeamGalacticEternaBuilding_4F_EventScript_JupiterDefeated::
	msgbox TeamGalacticEternaBuilding_4F_Text_LastWarning, MSGBOX_DEFAULT
	release
	end

TeamGalacticEternaBuilding_4F_EventScript_CycleShopMan::
	lock
	faceplayer
	goto_if_defeated TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING, TeamGalacticEternaBuilding_4F_EventScript_CycleShopManFree
	msgbox TeamGalacticEternaBuilding_4F_Text_WhatsWithTeamGalactic, MSGBOX_DEFAULT
	release
	end

TeamGalacticEternaBuilding_4F_EventScript_CycleShopManFree::
	msgbox TeamGalacticEternaBuilding_4F_Text_ThankYouCruiseByCycleShop, MSGBOX_DEFAULT
	release
	end

TeamGalacticEternaBuilding_4F_EventScript_HostageClefairy::
	lock
	faceplayer
	playmoncry SPECIES_CLEFAIRY, CRY_MODE_NORMAL
	msgbox TeamGalacticEternaBuilding_4F_Text_HostageClefairy, MSGBOX_DEFAULT
	waitmoncry
	release
	end

TeamGalacticEternaBuilding_4F_Text_HostageClefairy:
	.string "CLEFAIRY: Pi...$"

TeamGalacticEternaBuilding_4F_EventScript_HostagePokefan::
	msgbox TeamGalacticEternaBuilding_4F_Text_HostagePokefan, MSGBOX_NPC
	end

TeamGalacticEternaBuilding_4F_Text_HostagePokefan:
	.string "What is it with this Team\n"
	.string "Galactic?\p"
	.string "Why did they take our Pokémon?\n"
	.string "What are they trying to\l"
	.string "accomplish?$"

TeamGalacticEternaBuilding_4F_EventScript_PeaceSign::
	msgbox TeamGalacticEternaBuilding_4F_Text_WorkingForWorldPeace, MSGBOX_SIGN
	end

TeamGalacticEternaBuilding_4F_Text_IWillDealWithYou:
	.string "Eh? Did you want something?\p"
	.string "How silly of me to even ask.\n"
	.string "You want to free the Pokémon.\p"
	.string "Fine!\n"
	.string "I, Jupiter, will deal with you.$"

TeamGalacticEternaBuilding_4F_Text_WellArentYouTough:
	.string "Well, aren't you tough...?$"

TeamGalacticEternaBuilding_4F_Text_LastWarning:
	.string "It's OK, though. Our official\n"
	.string "Pokémon-statue investigation is\l"
	.string "finished.\p"
	.string "Mars has collected energy from\n"
	.string "the Valley Windworks.\p"
	.string "We're pretty much finished here.\n"
	.string "I'll let you in on one little\l"
	.string "thing.\p"
	.string "Our boss is researching the myths\n"
	.string "of ancient Pokémon.\p"
	.string "With the power of mythical\n"
	.string "Pokémon, he will become the ruler\l"
	.string "of Sinnoh...\p"
	.string "I suggest you keep out of Team\n"
	.string "Galactic's affairs from now on.\p"
	.string "This is your last warning!$"

TeamGalacticEternaBuilding_4F_Text_WhatsWithTeamGalactic:
	.string "What is it with this Team\n"
	.string "Galactic?\p"
	.string "Why did they take our Pokémon?\n"
	.string "What are they trying to\l"
	.string "accomplish?$"

TeamGalacticEternaBuilding_4F_Text_ThankYouCruiseByCycleShop:
	.string "I got my CLEFAIRY back, and it's\n"
	.string "all thanks to you!\p"
	.string "But that Team Galactic...\p"
	.string "They said, “CLEFAIRY came from\n"
	.string "space. Hand it over!”\p"
	.string "Their logic baffles me still.\n"
	.string "It's like they are from space!\p"
	.string "Anyway, they're gone now.\n"
	.string "Thank you very much!\p"
	.string "I can't thank you enough right\n"
	.string "now, but cruise by my Cycle Shop,\l"
	.string "OK?$"

TeamGalacticEternaBuilding_4F_Text_WorkingForWorldPeace:
	.string "Working for world peace.\p"
	.string "              Team Galactic$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TeamGalacticEternaBuilding_4F_EventScript_Placa1::
	msgbox TeamGalacticEternaBuilding_4F_Text_Placa1, MSGBOX_SIGN
	end

TeamGalacticEternaBuilding_4F_Text_Placa1:
	.string "Working for world peace.\n              Team Galactic$"
