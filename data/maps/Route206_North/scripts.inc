Route206_North_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte >>>
@ A fonte tranca este portao pra so passar de bicicleta e forca o jogador a
@ pedalar dentro dele (FLAG_FORCE_BIKING_IN_GATE + CheckPlayerOnBike). Esse
@ mecanismo NAO existe neste motor (nenhum FLAG_FORCE_BIKING_IN_GATE, nenhum
@ special de checar bicicleta em cena; grep em asm/macros/event.inc e
@ include/constants/flags.h, zero ocorrencia). Descartado sem substituto,
@ mesma regra da decisao 3 do plano: o jogador so atravessa a pe, sem trava.
@ VAR_TEMP_2 (VAR_MAP_LOCAL_0x02 da fonte) fica so de passagem, marca visita.
Route206_North_EventScript_CoordEvent_OnlyBicycles::
	lockall
	msgbox Route206_North_Text_CyclingRoadFlavor, MSGBOX_SIGN
	setvar VAR_TEMP_2, 1
	releaseall
	end

Route206_North_EventScript_CoordEvent_ClearFlagForceBikingInGate::
	setvar VAR_TEMP_2, 0
	end

Route206_North_Text_CyclingRoadFlavor:
	.string "CYCLING ROAD\n"
	.string "Built for speed on two wheels.$"

@ Grupo de hidden_flag FLAG_HIDE_ROUTE_206_CYCLING_ROAD_NORTH_GATE_SCIENTIST_M
@ (nao ligado aos dois coord_events acima). Da um EXP SHARE uma unica vez e
@ some para sempre, igual a fonte (SetFlag na propria hidden_flag depois do
@ presente, sem var nem flag nova: reusa o campo "flag" do object_event).
@ Simplificacao anotada: a fonte so libera depois de 35 especies vistas na
@ Pokedex (GetNationalDexSeenCount); nao ha special equivalente neste motor
@ (grep em data/specials.inc, zero contagem de vistos). Da incondicional na
@ unica conversa possivel.
Route206_North_EventScript_Scientist::
	lock
	faceplayer
	msgbox Route206_North_Text_SomethingForYou, MSGBOX_DEFAULT
	giveitem ITEM_EXP_SHARE
	setflag FLAG_SINNOH_ESCONDE_ROUTE_206_CYCLING_ROAD_NORTH_GATE_SCIENTIST_M
	release
	end

Route206_North_Text_SomethingForYou:
	.string "You've met so many different\n"
	.string "Pokémon already!\p"
	.string "Here, I have something for you.$"
@ <<< B6 Sinnoh S4: cena da fonte <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route206_North_EventScript_Npc1::
	msgbox Route206_North_Text_Npc1, MSGBOX_NPC
	end

Route206_North_Text_Npc1:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"

Route206_North_EventScript_Npc2::
	msgbox Route206_North_Text_Npc2, MSGBOX_NPC
	end

Route206_North_Text_Npc2:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"
