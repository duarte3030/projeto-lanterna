@ Sandgem Town. Ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever script novo.
@ sinnoh-dados/sandgem_town.json nao trouxe falas em ingles para estes NPCs
@ (lista "falas_em_ingles" vazia); falas abaixo escritas no mesmo tom da regiao.

SandgemTown_MapScripts::
	.byte 0

SandgemTown_EventScript_Youngster::
	msgbox SandgemTown_Text_Youngster, MSGBOX_NPC
	end

SandgemTown_EventScript_BreederM::
	lock
	faceplayer
	msgbox SandgemTown_Text_BreederM, MSGBOX_DEFAULT
	release
	end

SandgemTown_EventScript_BreederF::
	lock
	faceplayer
	msgbox SandgemTown_Text_BreederF, MSGBOX_DEFAULT
	release
	end

SandgemTown_EventScript_Professor::
	lock
	faceplayer
	msgbox SandgemTown_Text_Professor, MSGBOX_DEFAULT
	release
	end

SandgemTown_EventScript_Rival::
	lock
	faceplayer
	msgbox SandgemTown_Text_Rival, MSGBOX_DEFAULT
	release
	end

SandgemTown_EventScript_TownSign::
	msgbox SandgemTown_Text_TownSign, MSGBOX_SIGN
	end

SandgemTown_Text_Youngster:
	.string "This is SANDGEM TOWN.\n"
	.string "PROFESSOR ROWAN's lab is right there!$"

SandgemTown_Text_BreederM:
	.string "I raise POKéMON here in SANDGEM.\p"
	.string "A calm town by the sea is the best\n"
	.string "place to raise them healthy and strong.$"

SandgemTown_Text_BreederF:
	.string "Have you been to the lab yet?\p"
	.string "The PROFESSOR studies POKéMON\n"
	.string "evolution. Fascinating stuff!$"

@ Fala do Platinum, sandgem_town.json (SandgemTown_Text_RowansComeBack). Este
@ NPC era um segundo ROWAN na rua, com o sprite do professor, enquanto o ROWAN
@ de verdade esta no laboratorio; virou morador comentando a volta dele.
SandgemTown_Text_Professor:
	.string "PROFESSOR ROWAN's come back to town!\p"
	.string "It must be, like, four years since\n"
	.string "he left.\p"
	.string "They say he was doing his research\n"
	.string "somewhere else all this time.$"

SandgemTown_Text_Rival:
	.string "Hey! You're heading to the lab too?\p"
	.string "Race you there!$"

SandgemTown_Text_TownSign:
	.string "SANDGEM TOWN\n"
	.string "Where the Winds of New Beginnings Blow$"
