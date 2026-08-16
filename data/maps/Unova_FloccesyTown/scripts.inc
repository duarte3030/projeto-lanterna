@ FloccesyTown do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ A JUNIPER (EVENT_FLOCCESY_TOWN_JUNIPER na fonte) nao veio importada: e um
@ NPC so desta cena, gfx OBJ_EVENT_GFX_WOMAN_3 (mesmo placeholder do B5/B6 em
@ Unova_ChampionsRoom), acrescentado no FIM da lista de object_events
@ (indice 5, local id 5).
@
@ EVENT_FLOCCESY_TOWN_JUNIPER e so campo de esconde-objeto na fonte (nunca
@ aparece em checkevent/setevent/clearevent dentro de script), entao a
@ varredura de flags do PLANO-OBRAS-UNOVA.md nao o capturou e nao ha flag
@ reservada pra ele nesta leva. Zero flag nova (janela de save fechada):
@ ON_LOAD some com ela permanentemente usando a PROPRIA var da cena
@ (VAR_UNOVA_FLOCCESY_CENA já != 0 depois que a cena roda), sem precisar de
@ bit novo. `removeobject` dentro da cena cobre o "disappear" imediato.
Unova_FloccesyTown_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_FloccesyTown_EventScript_AoCarregar
	.byte 0

Unova_FloccesyTown_EventScript_AoCarregar::
	goto_if_eq VAR_UNOVA_FLOCCESY_CENA, 0, Unova_FloccesyTown_EventScript_AoCarregarFim
	removeobject 5
Unova_FloccesyTown_EventScript_AoCarregarFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Chegada da JUNIPER, quatro variantes conforme a fileira em que o jogador
@ entrou (fonte usa `jump`/fallthrough pro roteiro comum).
Unova_FloccesyTown_EventScript_FloccesyTownJuniperScript1::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	goto Unova_FloccesyTown_EventScript_FloccesyTownJuniperComum

Unova_FloccesyTown_EventScript_FloccesyTownJuniperScript2::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkUp
	waitmovement 0
	goto Unova_FloccesyTown_EventScript_FloccesyTownJuniperComum

Unova_FloccesyTown_EventScript_FloccesyTownJuniperScript3::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkUp2
	waitmovement 0
	goto Unova_FloccesyTown_EventScript_FloccesyTownJuniperComum

Unova_FloccesyTown_EventScript_FloccesyTownJuniperScript4::
	lockall
	applymovement LOCALID_PLAYER, Unova_FloccesyTown_Movement_JogadorTresPassos
	waitmovement 0
	@ cai no comum

Unova_FloccesyTown_EventScript_FloccesyTownJuniperComum::
	msgbox Unova_FloccesyTown_Text_FloccesyTownJuniperText, MSGBOX_DEFAULT
	closemessage
	applymovement 5, Unova_FloccesyTown_Movement_Juniper
	waitmovement 0
	removeobject 5
	setvar VAR_UNOVA_FLOCCESY_CENA, 1
	releaseall
	end

Unova_FloccesyTown_Movement_JogadorTresPassos:
	walk_up
	walk_up
	walk_up
	step_end

Unova_FloccesyTown_Movement_Juniper:
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	step_end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_FloccesyTown_EventScript_Placa0::
	msgbox Unova_FloccesyTown_Text_FloccesyTownSignText, MSGBOX_SIGN
	end

Unova_FloccesyTown_EventScript_Npc2::
	msgbox Unova_FloccesyTown_Text_FloccesyTownTwinText, MSGBOX_NPC
	end

Unova_FloccesyTown_EventScript_Npc3::
	msgbox Unova_FloccesyTown_Text_FloccesyTownPokefanMText, MSGBOX_NPC
	end

Unova_FloccesyTown_EventScript_Npc4::
	msgbox Unova_FloccesyTown_Text_FloccesyTownBlockerText, MSGBOX_NPC
	end


Unova_FloccesyTown_Text_FloccesyTownSignText::
	.string "FLOCCESY TOWN"
	.string "\pProphecy flocks"
	.string "\nhere!$"

Unova_FloccesyTown_Text_FloccesyTownTwinText::
	.string "I want to go to"
	.string "\nthe ranch! I want"
	.string "\lto get some milk!$"

Unova_FloccesyTown_Text_FloccesyTownPokefanMText::
	.string "Welcome to our"
	.string "\nlittle town. It"
	.string "\pain't much, but"
	.string "\nthe ranch outside"
	.string "\pof town delivers"
	.string "\nmilk all over"
	.string "\lUNOVA.$"

Unova_FloccesyTown_Text_FloccesyTownBlockerText::
	.string "Mister ALDER isn't"
	.string "\nhome right now."
	.string "\pAw man, I wanted"
	.string "\nto train with him!$"

Unova_FloccesyTown_Text_FloccesyTownJuniperText::
	.string "You there,"
	.string "\ntrainer!"
	.string "\pYou're {PLAYER},"
	.string "\nright?"
	.string "\pMy name is AUREA"
	.string "\nJUNIPER. I'm a"
	.string "\lfriend of PROF."
	.string "\lBIANCA."
	.string "\pIn fact, she used"
	.string "\nto be my pupil."
	.string "\pI was the PROF who"
	.string "\ngave her and"
	.string "\lCHEREN their first"
	.string "\lPOKéMON."
	.string "\pThey've both told"
	.string "\nme good things"
	.string "\labout you."
	.string "\pCHEREN's gone to"
	.string "\nthe COMPLEX in"
	.string "\lVIRBANK CITY."
	.string "\pHe believes TEAM"
	.string "\nPLASMA may be up"
	.string "\lto something"
	.string "\lthere."
	.string "\pI'm sure he'd"
	.string "\nappreciate if you"
	.string "\lhelped."
	.string "\pI'm eager to see"
	.string "\nhow far you'll go,"
	.string "\l{PLAYER}.$"
