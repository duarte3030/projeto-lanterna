FightArea_MapScripts::
	.byte 0

FightArea_EventScript_Sailor::
	lock
	faceplayer
@ ponytail: par da viagem que abre em Snowpoint depois da Liga. Sem esta volta o
@ jogador ficava preso na Battle Zone, que e o mesmo bug que Johto tinha antes de
@ o marinheiro de Olivine existir.
	msgbox FightArea_Text_SailorOferece, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FightArea_EventScript_SailorRecusa
	msgbox FightArea_Text_SailorZarpa, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SNOWPOINT_CITY, 20, 40
	waitstate
	release
	end

FightArea_EventScript_SailorRecusa::
	msgbox FightArea_Text_Sailor, MSGBOX_DEFAULT
	release
	end

FightArea_EventScript_Fisherman::
	msgbox FightArea_Text_Fisherman, MSGBOX_NPC
	end

FightArea_EventScript_Camper::
	msgbox FightArea_Text_Camper, MSGBOX_NPC
	end

FightArea_EventScript_AceTrainerM::
	msgbox FightArea_Text_AceTrainerM, MSGBOX_NPC
	end

FightArea_EventScript_AceTrainerF::
	msgbox FightArea_Text_AceTrainerF, MSGBOX_NPC
	end

FightArea_EventScript_Twin::
	msgbox FightArea_Text_Twin, MSGBOX_NPC
	end

FightArea_Text_Sailor:
	.string "Ahoy! Ships leave from the harbor\n"
	.string "near here for SNOWPOINT CITY.$"

FightArea_Text_Fisherman:
	.string "Hmm! A Super Rod is really good!\n"
	.string "Wouldn't you agree?$"

FightArea_Text_Camper:
	.string "I bring my POKéMON here to train\n"
	.string "against tough opponents.$"

FightArea_Text_AceTrainerM:
	.string "TRAINERS from all over SINNOH\n"
	.string "gather at the FIGHT AREA.$"

FightArea_Text_AceTrainerF:
	.string "I've fought here a dozen times.\n"
	.string "Still haven't won it all!$"

FightArea_Text_Twin:
	.string "My sister and I love watching the\n"
	.string "tough TRAINERS battle here!$"

FightArea_Text_SailorOferece:
	.string "Want me to take you back to\n"
	.string "SNOWPOINT CITY?$"

FightArea_Text_SailorZarpa:
	.string "Setting sail for SNOWPOINT CITY!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

FightArea_EventScript_Placa2::
	msgbox FightArea_Text_Placa2, MSGBOX_SIGN
	end

FightArea_Text_Placa2:
	.string "Rt. 225 Ahead\nA Road of Challenges$"

FightArea_EventScript_Placa3::
	msgbox FightArea_Text_Placa3, MSGBOX_SIGN
	end

FightArea_Text_Placa3:
	.string "Battle Frontier Ahead\nAim to Win Glory with Pokémon!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FightArea_EventScript_Npc1::
	msgbox FightArea_Text_Npc1, MSGBOX_NPC
	end

FightArea_Text_Npc1:
	.string "Whenever I go to a new place, I get\nexcited over what I might discover.\pBut places I've visited before...\pEven those places thrill me with\nnew discoveries!$"

FightArea_EventScript_Npc2::
	msgbox FightArea_Text_Npc2, MSGBOX_NPC
	end

FightArea_Text_Npc2:
	.string "Hmm!\nA Super Rod is really good!\pWouldn't you agree?$"

FightArea_EventScript_Npc3::
	msgbox FightArea_Text_Npc3, MSGBOX_NPC
	end

FightArea_Text_Npc3:
	.string "Because of the volcano, the land\naround here is craggy.\pThe rough terrain and all the ups\nand downs make it hard to hike.$"

FightArea_EventScript_Npc4::
	msgbox FightArea_Text_Npc4, MSGBOX_NPC
	end

FightArea_Text_Npc4:
	.string "The way the Battle Tower looms...\pIt really is a wall that stands\nbefore every Trainer.$"

FightArea_EventScript_Npc5::
	msgbox FightArea_Text_Npc5, MSGBOX_NPC
	end

FightArea_Text_Npc5:
	.string "I've battled many Trainers over\nthe years.\pI've gained some confidence in my\nskill levels, too.\pBut the world is still a huge place.\nIt's not easy to win in life!$"

FightArea_EventScript_Npc6::
	msgbox FightArea_Text_Npc6, MSGBOX_NPC
	end

FightArea_Text_Npc6:
	.string "The Pokémon League's Elite Four\ncome here sometimes!$"

FightArea_EventScript_Npc7::
	msgbox FightArea_Text_Npc7, MSGBOX_NPC
	end

FightArea_Text_Npc7:
	.string "Your Pokémon are from Sinnoh,\naren't they?\pThey're not what we're used to\nseeing around here.$"

FightArea_EventScript_Npc8::
	msgbox FightArea_Text_Npc8, MSGBOX_NPC
	end

FightArea_Text_Npc8:
	.string "What's up? Do you want to sail to\nSnowpoint City?$"

FightArea_EventScript_Npc9::
	msgbox FightArea_Text_Npc9, MSGBOX_NPC
	end

FightArea_Text_Npc9:
	.string "There's no end to becoming tough!\pI just made that up, but it sounds\nkind of cool, huh?$"

FightArea_EventScript_Placa10::
	msgbox FightArea_Text_Placa10, MSGBOX_SIGN
	end

FightArea_Text_Placa10:
	.string "Fight Area\nBattles Galore$"
