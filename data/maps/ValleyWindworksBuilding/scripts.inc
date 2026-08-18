ValleyWindworksBuilding_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte, rotulo ValleyWindworksBuilding_CoordEvent_Mars >>>
@ CONFLITO ACHADO, NAO INVENTADO: na fonte esta cena e a luta contra a MARS
@ (o comandante entra pelo grunt que avisa em OnFrame_FirstEntry, VAR_VALLEY_
@ WINDWORKS_TEAM_GALACTIC_STATE vira 1, e so entao este gatilho a poe pra
@ lutar). Mas data/maps/ValleyWindworks/scripts.inc (leva anterior, S2) JA
@ escreveu a luta inteira contra a MARS do LADO DE FORA
@ (ValleyWindworks_EventScript_Mars, TRAINER_SINNOH_COMMANDER_MARS_VALLEY_
@ WINDWORKS, flag FLAG_GALACTICA_WINDWORKS), com comentario explicito "o
@ interior da usina NAO existe neste hack, a cena inteira acontece do lado de
@ fora". So que o mapa ValleyWindworksBuilding EXISTE de verdade aqui (porta
@ em ValleyWindworks/map.json linha ~104, layout proprio, o Papa/cientista ja
@ importado). Escrever a MARS de novo aqui duplicaria o mesmo TRAINER_SINNOH_
@ COMMANDER_MARS_VALLEY_WINDWORKS derrotavel duas vezes (regra dura: id de
@ treinador nao duplica entre mapas). NAO fiz: fica bloqueado ate a condutora
@ decidir se o interior morre (remover a porta em ValleyWindworks) ou vira o
@ dono canonico da luta (e a exterior e quem some).
@ BLOQUEADO: cena da MARS ja existe em outro mapa (ValleyWindworks), decisao
@ de condutora necessaria antes de escrever esta.
ValleyWindworksBuilding_EventScript_CoordEvent_Mars::
	end

@ <<< B6 Sinnoh S4: cena da fonte <<<

ValleyWindworksBuilding_EventScript_Npc1::
	msgbox ValleyWindworksBuilding_Text_Npc1, MSGBOX_NPC
	end

ValleyWindworksBuilding_Text_Npc1:
	.string "Papa: Oh, yes, a balloon Pokémon\nappears in front of the windworks.\pIt's always a certain day of the week,\nbut I'm not sure which day.\pCould its appearance have something\nto do with this windworks using\pwind-generated energy?$"

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
