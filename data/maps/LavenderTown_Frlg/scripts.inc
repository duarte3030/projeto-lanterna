LavenderTown_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTown_OnTransition
	.byte 0

LavenderTown_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_LAVENDER_TOWN
	setvar VAR_MAP_SCENE_S_S_ANNE_2F_CORRIDOR, 1
	setflag FLAG_HIDE_SS_ANNE_RIVAL
	end

LavenderTown_EventScript_LittleGirl::
	lock
	faceplayer
	msgbox LavenderTown_Text_DoYouBelieveInGhosts, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LavenderTown_EventScript_LittleGirlBelieve
	msgbox LavenderTown_Text_JustImaginingWhiteHand
	release
	end

LavenderTown_EventScript_LittleGirlBelieve::
	msgbox LavenderTown_Text_SoThereAreBelievers
	release
	end

LavenderTown_EventScript_WorkerM::
	msgbox LavenderTown_Text_TownKnownAsMonGraveSite, MSGBOX_NPC
	end

LavenderTown_EventScript_Boy::
	msgbox LavenderTown_Text_GhostsAppearedInTower, MSGBOX_NPC
	end

LavenderTown_EventScript_TownSign::
	msgbox LavenderTown_Text_TownSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_SilphScopeNotice::
	msgbox LavenderTown_Text_SilphScopeNotice, MSGBOX_SIGN
	end

LavenderTown_EventScript_VolunteerHouseSign::
	msgbox LavenderTown_Text_VolunteerPokemonHouse, MSGBOX_SIGN
	end

LavenderTown_EventScript_PokemonTowerSign::
	msgbox LavenderTown_Text_PokemonTowerSign, MSGBOX_SIGN
	end

LavenderTown_Text_DoYouBelieveInGhosts::
	.string "Do you believe in ghosts?$"

LavenderTown_Text_SoThereAreBelievers::
	.string "Really?\n"
	.string "So there are believers…$"

LavenderTown_Text_JustImaginingWhiteHand::
	.string "Hahaha, I guess not.\p"
	.string "That white hand on your shoulder…\n"
	.string "I'm just imagining it.$"

LavenderTown_Text_TownKnownAsMonGraveSite::
	.string "This town is known as the grave\n"
	.string "site of POKéMON.\p"
	.string "Memorial services are held in\n"
	.string "POKéMON TOWER.$"

LavenderTown_Text_GhostsAppearedInTower::
	.string "Ghosts appeared in POKéMON TOWER.\p"
	.string "I think they're the spirits of\n"
	.string "POKéMON that the ROCKETS killed.$"

LavenderTown_Text_TownSign::
	.string "LAVENDER TOWN\n"
	.string "The Noble Purple Town$"

LavenderTown_Text_SilphScopeNotice::
	.string "New SILPH SCOPE!\n"
	.string "Make the Invisible Plain to See!\p"
	.string "SILPH CO.$"

LavenderTown_Text_VolunteerPokemonHouse::
	.string "LAVENDER VOLUNTEER\n"
	.string "POKéMON HOUSE$"

LavenderTown_Text_PokemonTowerSign::
	.string "POKéMON TOWER\n"
	.string "Becalm the Spirits of POKéMON$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

LavenderTown_EventScript_Povoa1::
	lock
	faceplayer
	msgbox LavenderTown_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_Povoa1:
	.string "The TOWER is a grave, not a\nlandmark. Walk quietly in there.$"

LavenderTown_EventScript_Povoa2::
	lock
	faceplayer
	msgbox LavenderTown_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_Povoa2:
	.string "MR. FUJI takes in Pokémon that\nlost their trainers.$"

LavenderTown_EventScript_Povoa3::
	lock
	faceplayer
	msgbox LavenderTown_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_Povoa3:
	.string "My friend says the tower is\nhaunted. I say he is scared.$"

LavenderTown_EventScript_Povoa4::
	lock
	faceplayer
	msgbox LavenderTown_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_Povoa4:
	.string "Ghost types ignore Normal moves.\nBring something else.$"

LavenderTown_EventScript_Povoa5::
	lock
	faceplayer
	msgbox LavenderTown_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_Povoa5:
	.string "Three roads meet here: ROUTE 8,\nROUTE 10 and ROUTE 12.$"

LavenderTown_EventScript_Povoa6::
	lock
	faceplayer
	msgbox LavenderTown_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_Povoa6:
	.string "This town is small and sad,\nand it does not pretend otherwise.$"

LavenderTown_EventScript_Povoa7::
	lock
	faceplayer
	msgbox LavenderTown_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

LavenderTown_Text_Povoa7:
	.string "I leave flowers at the tower\nevery week. It helps.$"

@ <<< Povoamento: fim do bloco gerado <<<
