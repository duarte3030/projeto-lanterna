ValleyWindworksBuilding_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte, rotulo ValleyWindworksBuilding_CoordEvent_Mars >>>
@ CONFLITO ACHADO, NAO INVENTADO (nota da leva anterior, mantida por
@ historico): na fonte esta cena e a luta contra a MARS. Mas
@ data/maps/ValleyWindworks/scripts.inc (leva S2) ja escreveu a luta inteira
@ contra a MARS do LADO DE FORA (ValleyWindworks_EventScript_Mars,
@ TRAINER_SINNOH_COMMANDER_MARS_VALLEY_WINDWORKS, flag FLAG_GALACTICA_
@ WINDWORKS), provada em suite. Regra dura: id de treinador nao duplica entre
@ mapas.
@ DESBLOQUEADO em 17/08/2026, decisao da condutora: o interior NAO duplica a
@ luta. A exterior continua dona canonica da batalha; este mapa porta so o
@ que a fonte tem de flavor em volta dela (os dois grunts mudos abaixo, sem
@ TRAINER_ proprio porque a fonte tambem nao os batalha aqui) e referencia o
@ ESTADO da cena externa pela mesma FLAG_GALACTICA_WINDWORKS que ela ja usa.
@ VAR_SINNOH_WINDWORKS_GALACTICA_ESTADO (leva S4, nunca escrita ate aqui) vira
@ o "ja mostrei o desfecho" deste gatilho: fica 0 enquanto a Galactica ainda
@ ocupa a usina (o trigger pode repetir, porque reflete o estado de fora a
@ cada visita) e vai para 1 so depois que FLAG_GALACTICA_WINDWORKS acender,
@ pra nao repetir o desfecho pra sempre (mesmo idioma de var_value 0->1 que
@ Route203_EventScript_CoordEvent_Rival ja usa).
ValleyWindworksBuilding_EventScript_CoordEvent_Mars::
	lockall
	goto_if_set FLAG_GALACTICA_WINDWORKS, ValleyWindworksBuilding_EventScript_MarsAftermath
	msgbox ValleyWindworksBuilding_Text_CommanderStillOutside, MSGBOX_DEFAULT
	releaseall
	end

ValleyWindworksBuilding_EventScript_MarsAftermath::
	msgbox ValleyWindworksBuilding_Text_TurbinesRunningAgain, MSGBOX_DEFAULT
	setvar VAR_SINNOH_WINDWORKS_GALACTICA_ESTADO, 1
	releaseall
	end

ValleyWindworksBuilding_Text_CommanderStillOutside:
	.string "GRUNT: Nobody gets past here!\nOur Commander's dealing with someone\lat the front door right now!$"

ValleyWindworksBuilding_Text_TurbinesRunningAgain:
	.string "The turbines are turning again.\pWith Team Galactic gone, the Valley\nWindworks is back to making clean\lenergy for Sinnoh.$"

@ <<< B6 Sinnoh S4: cena da fonte <<<

@ Os dois grunts mudos de pret/pokeplatinum (LOCALID_GALACTIC_GRUNT_1 e
@ LOCALID_GRUNT_M na fonte). Sem batalha propria: a fonte tambem so os usa
@ pra fala aqui dentro (quem batalha e a exterior). Somem quando
@ FLAG_GALACTICA_WINDWORKS acende (Mars cai), igual ao par GruntM/GruntF de
@ TeamGalacticEternaBuilding_2F/scripts.inc.
ValleyWindworksBuilding_EventScript_Grunt1::
	msgbox ValleyWindworksBuilding_Text_GotToAlertCommander, MSGBOX_NPC
	end

ValleyWindworksBuilding_EventScript_GruntM::
	msgbox ValleyWindworksBuilding_Text_CommanderWillSmooshYou, MSGBOX_NPC
	end

ValleyWindworksBuilding_Text_GotToAlertCommander:
	.string "GRUNT: Hey! An outsider!\nI've got to alert the Commander!$"

ValleyWindworksBuilding_Text_CommanderWillSmooshYou:
	.string "Humph! Just you wait!\nOur Commander will smoosh you!$"

ValleyWindworksBuilding_EventScript_Npc1::
	goto_if_set FLAG_GALACTICA_WINDWORKS, ValleyWindworksBuilding_EventScript_Npc1After
	msgbox ValleyWindworksBuilding_Text_Npc1, MSGBOX_NPC
	end

ValleyWindworksBuilding_EventScript_Npc1After::
	msgbox ValleyWindworksBuilding_Text_Npc1After, MSGBOX_NPC
	end

ValleyWindworksBuilding_Text_Npc1:
	.string "Papa: Oh, yes, a balloon Pokémon\nappears in front of the windworks.\pIt's always a certain day of the week,\nbut I'm not sure which day.\pCould its appearance have something\nto do with this windworks using\pwind-generated energy?$"

ValleyWindworksBuilding_Text_Npc1After:
	.string "Papa: The Valley Windworks uses\nturbines to capture energy from the\lwinds in this canyon.\pWe produce energy from the power of\nnature itself. It's quite wonderful.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

ValleyWindworksBuilding_EventScript_Placa1::
	msgbox ValleyWindworksBuilding_Text_Placa1, MSGBOX_SIGN
	end

ValleyWindworksBuilding_Text_Placa1:
	.string "The bringer of wars...\pYour target is the energy of the power\nplant.\pThe bringer of contentment...\pYour target is the Pokémon statue of\nEterna City.\pThe bringer of aging...\pYour target is the Pokémon that sleeps\non today.\pThe dream energy.\n           Team Galactic$"

ValleyWindworksBuilding_EventScript_Placa2::
	msgbox ValleyWindworksBuilding_Text_Placa2, MSGBOX_SIGN
	end

ValleyWindworksBuilding_Text_Placa2:
	.string "The bringer of wars...\pYour target is the energy of the power\nplant.\pThe bringer of contentment...\pYour target is the Pokémon statue of\nEterna City.\pThe bringer of aging...\pYour target is the Pokémon that sleeps\non today.\pThe dream energy.\n           Team Galactic$"
