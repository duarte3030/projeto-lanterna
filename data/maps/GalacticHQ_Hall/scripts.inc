@ Salao do QG da Galactica, em Veilstone: o discurso do Cyrus.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_hall.json.
@
@ ponytail: layout emprestado do Salao de Concursos de Lilycove, que ja e um
@ auditorio com palco e plateia. As tres saidas do sul sao as mesmas do mapa de
@ Hoenn, entao nenhum warp foi inventado.
@
@ O discurso nao dispara por coord_event: gatilho de coordenada custa uma var
@ para lembrar que ja rodou, e var nao se inventa neste projeto. Falar com o
@ Cyrus ou com o Looker roda a cena inteira, e ela pode ser revista.

GalacticHQ_Hall_MapScripts::
	.byte 0

GalacticHQ_Hall_EventScript_Cyrus::
	lock
	faceplayer
	msgbox GalacticHQ_Hall_Text_TheWorldMustChange, MSGBOX_DEFAULT
	msgbox GalacticHQ_Hall_Text_WeWillChangeIt, MSGBOX_DEFAULT
	msgbox GalacticHQ_Hall_Text_GruntsWroooar, MSGBOX_DEFAULT
	msgbox GalacticHQ_Hall_Text_LetThereBeGlory, MSGBOX_DEFAULT
	msgbox GalacticHQ_Hall_Text_GruntsWroooar, MSGBOX_DEFAULT
	release
	end

GalacticHQ_Hall_EventScript_Looker::
	lock
	faceplayer
	msgbox GalacticHQ_Hall_Text_PsstOverHere, MSGBOX_DEFAULT
	msgbox GalacticHQ_Hall_Text_QuiteThePerformance, MSGBOX_DEFAULT
	release
	end

GalacticHQ_Hall_EventScript_Grunt1::
	msgbox GalacticHQ_Hall_Text_CyrusIsTheGreatest, MSGBOX_NPC
	end

GalacticHQ_Hall_EventScript_Grunt2::
	msgbox GalacticHQ_Hall_Text_GruntsWroooar, MSGBOX_NPC
	end

GalacticHQ_Hall_Text_PsstOverHere:
	.string "Looker: Psst! Here.\n"
	.string "Over here.\p"
	.string "This gathering of the Team\n"
	.string "Galactic...\l"
	.string "What is the meaning of it?$"

GalacticHQ_Hall_Text_TheWorldMustChange:
	.string "Cyrus: Fellow members of Team\n"
	.string "Galactic! Hear me!\p"
	.string "My name, as I appear to you today,\n"
	.string "is Cyrus.\p"
	.string "This world of ours is a crude one.\n"
	.string "In a word, it is incomplete.\p"
	.string "It has been, and always will be, a\n"
	.string "struggle to survive in this world.\p"
	.string "We humans and Pokémon are likewise\n"
	.string "incomplete.\p"
	.string "Because we are all so lacking, we\n"
	.string "fight, we maim... It is ugly.\p"
	.string "I hate the incompleteness.\p"
	.string "That we are all incomplete, I hate\n"
	.string "it with my entire body and being.\p"
	.string "The world should be complete.\n"
	.string "The world must change.$"

GalacticHQ_Hall_Text_WeWillChangeIt:
	.string "Then, who will change it?\p"
	.string "Me, Cyrus. And Team Galactic.\n"
	.string "Yes, all of you.\p"
	.string "Together we pored over myths and\n"
	.string "exposed their secrets.\p"
	.string "Together we captured legendary\n"
	.string "Pokémon.\p"
	.string "And now, Team Galactic has\n"
	.string "obtained the energy to change the\l"
	.string "world!\p"
	.string "The power of dreams is within our\n"
	.string "grasp!$"

GalacticHQ_Hall_Text_LetThereBeGlory:
	.string "Understand it, fellow members!\p"
	.string "My long-held dreamworld is on the\n"
	.string "verge of becoming reality.\p"
	.string "All those headed to Mt. Coronet,\n"
	.string "and those who remain here...\p"
	.string "Though our missions may differ,\n"
	.string "our hearts beat as one.\p"
	.string "Let there be glory for Team\n"
	.string "Galactic!$"

GalacticHQ_Hall_Text_GruntsWroooar:
	.string "Grunts: WROOOAR!!$"

GalacticHQ_Hall_Text_CyrusIsTheGreatest:
	.string "Master Cyrus is the greatest!$"

GalacticHQ_Hall_Text_QuiteThePerformance:
	.string "Looker: ...Whew.\p"
	.string "So, that was Cyrus, the boss of\n"
	.string "the Team Galactic.\p"
	.string "Quite the performance, no?\n"
	.string "Mesmerizing for one only 27 years\l"
	.string "old.\p"
	.string "...But to make a world for Team\n"
	.string "Galactic and none other?\p"
	.string "It is preposterous. So much so\n"
	.string "that it makes my head spin.\p"
	.string "A new world? What is that?\n"
	.string "And what is this incomplete world?\p"
	.string "Very well. To investigate such\n"
	.string "matters is the job of the\l"
	.string "International Police.\p"
	.string "Of which I am a member in good\n"
	.string "stead. And it is my job, therefore.\p"
	.string "We shall part ways here.\n"
	.string "Take extra care, my friend!$"
