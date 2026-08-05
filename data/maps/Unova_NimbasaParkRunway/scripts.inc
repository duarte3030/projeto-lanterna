@ NimbasaParkRunway do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaParkRunway_MapScripts::
	.byte 0

Unova_NimbasaParkRunway_EventScript_Placa0::
	msgbox Unova_NimbasaParkRunway_Text_NimbasaParkOldGymText, MSGBOX_SIGN
	end

Unova_NimbasaParkRunway_EventScript_Placa1::
	msgbox Unova_NimbasaParkRunway_Text_NimbasaParkOldGymText, MSGBOX_SIGN
	end

Unova_NimbasaParkRunway_EventScript_Npc0::
	msgbox Unova_NimbasaParkRunway_Text_NimbasaParkCherenRunwayText, MSGBOX_NPC
	end

Unova_NimbasaParkRunway_EventScript_Npc1::
	msgbox Unova_NimbasaParkRunway_Text_GruntMNimbasaPark5SeenText, MSGBOX_NPC
	end

Unova_NimbasaParkRunway_EventScript_Npc2::
	msgbox Unova_NimbasaParkRunway_Text_GruntFNimbasaPark4SeenText, MSGBOX_NPC
	end

Unova_NimbasaParkRunway_EventScript_Npc3::
	msgbox Unova_NimbasaParkRunway_Text_GruntFNimbasaPark5SeenText, MSGBOX_NPC
	end


Unova_NimbasaParkRunway_Text_NimbasaParkOldGymText::
	.string "N--BASA --TY GY-"
	.string "\nLea--r: E--sa$"

Unova_NimbasaParkRunway_Text_NimbasaParkCherenRunwayText::
	.string "CHEREN: Oh,"
	.string "\n{PLAYER}. I trust"
	.string "\pthose PLASMA"
	.string "\nGRUNTS didn't give"
	.string "\lyou any trouble."
	.string "\pUnfortunately, I"
	.string "\nwasn't able to get"
	.string "\pany useful infor-"
	.string "\nmation out of"
	.string "\lthem."
	.string "\pI'm going to keep"
	.string "\ninvestigating this"
	.string "\larea for now.$"

Unova_NimbasaParkRunway_Text_GruntMNimbasaPark5SeenText::
	.string "Here I come!"
	.string "\nPlasmaaa!$"

Unova_NimbasaParkRunway_Text_GruntFNimbasaPark4SeenText::
	.string "In my own way, I'm"
	.string "\na strong part of"
	.string "\pthis TEAM PLASMA"
	.string "\ngroup!$"

Unova_NimbasaParkRunway_Text_GruntFNimbasaPark5SeenText::
	.string "Intruder sighted!$"
