WaywardCave1F_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

WaywardCave1F_EventScript_CamperDiego::
	trainerbattle_single TRAINER_SINNOH_CAMPER_DIEGO, WaywardCave1F_Text_CamperDiegoIntro, WaywardCave1F_Text_CamperDiegoDefeat
	msgbox WaywardCave1F_Text_CamperDiegoPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_CamperDiegoIntro:
	.string "Humph! You're lost, aren't you?\nI'll guide you if you can beat me.$"

WaywardCave1F_Text_CamperDiegoDefeat:
	.string "You didn't really have to win!\nI'm not going to guide you now!$"

WaywardCave1F_Text_CamperDiegoPost:
	.string "I'm not lost, I tell you!\nI'm camping! That's my story!$"

WaywardCave1F_EventScript_PicnickerTori::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_TORI, WaywardCave1F_Text_PicnickerToriIntro, WaywardCave1F_Text_PicnickerToriDefeat
	msgbox WaywardCave1F_Text_PicnickerToriPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_PicnickerToriIntro:
	.string "Where am I? Am I lost? Who are you?\nAre you a Pokémon Trainer?$"

WaywardCave1F_Text_PicnickerToriDefeat:
	.string "OK, so we're both Trainers.\nThat's a start, right?$"

WaywardCave1F_Text_PicnickerToriPost:
	.string "I just wanted to have a picnic under\nthe Cycling Road.\pI didn't think I would get lost\nin a place like this...$"

WaywardCave1F_EventScript_LassCassidy::
	trainerbattle_single TRAINER_SINNOH_LASS_CASSIDY, WaywardCave1F_Text_LassCassidyIntro, WaywardCave1F_Text_LassCassidyDefeat
	msgbox WaywardCave1F_Text_LassCassidyPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_LassCassidyIntro:
	.string "Hush now, lost little Pokémon, don't\nyou cry.\pI'm here to take care of you!$"

WaywardCave1F_Text_LassCassidyDefeat:
	.string "Sniffle... W-who's crying now?$"

WaywardCave1F_Text_LassCassidyPost:
	.string "Speaking of crying, I'm positive I\nheard crying from deeper in the cave.$"

WaywardCave1F_EventScript_YoungsterWayne::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_WAYNE, WaywardCave1F_Text_YoungsterWayneIntro, WaywardCave1F_Text_YoungsterWayneDefeat
	msgbox WaywardCave1F_Text_YoungsterWaynePost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_YoungsterWayneIntro:
	.string "Did you come to play, too?\nWanna play battle with me?$"

WaywardCave1F_Text_YoungsterWayneDefeat:
	.string "You were just toying with me!$"

WaywardCave1F_Text_YoungsterWaynePost:
	.string "I'm playing hide-and-seek here.\nI like some underground tag, too.$"

WaywardCave1F_EventScript_HikerReginald::
	trainerbattle_single TRAINER_SINNOH_HIKER_REGINALD, WaywardCave1F_Text_HikerReginaldIntro, WaywardCave1F_Text_HikerReginaldDefeat
	msgbox WaywardCave1F_Text_HikerReginaldPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_HikerReginaldIntro:
	.string "Look! A Trainer lost in Wayward Cave!$"

WaywardCave1F_Text_HikerReginaldDefeat:
	.string "I strayed from the battle plan!$"

WaywardCave1F_Text_HikerReginaldPost:
	.string "Me? No, I'm not lost.\nI live here!$"

WaywardCave1F_EventScript_CollectorTerry::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_TERRY, WaywardCave1F_Text_CollectorTerryIntro, WaywardCave1F_Text_CollectorTerryDefeat
	msgbox WaywardCave1F_Text_CollectorTerryPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_CollectorTerryIntro:
	.string "You look like you might just have\nthe Pokémon I've been looking for!$"

WaywardCave1F_Text_CollectorTerryDefeat:
	.string "You didn't have a single Pokémon\nI wanted... You're no Collector!$"

WaywardCave1F_Text_CollectorTerryPost:
	.string "I'm very picky, so I want to collect\nevery Pokémon without anyone's help.\p...I do have friends, though.\nNo, seriously! I do!$"

WaywardCave1F_EventScript_PicnickerAna::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_ANA, WaywardCave1F_Text_PicnickerAnaIntro, WaywardCave1F_Text_PicnickerAnaDefeat
	msgbox WaywardCave1F_Text_PicnickerAnaPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_PicnickerAnaIntro:
	.string "What every good picnic needs is a\ncute setting, good food, and a fun\pbattle!$"

WaywardCave1F_Text_PicnickerAnaDefeat:
	.string "That wasn't any fun for me!$"

WaywardCave1F_Text_PicnickerAnaPost:
	.string "Why have a picnic here? I don't know.\nThere's no deep meaning to it.$"

WaywardCave1F_EventScript_CamperParker::
	trainerbattle_single TRAINER_SINNOH_CAMPER_PARKER, WaywardCave1F_Text_CamperParkerIntro, WaywardCave1F_Text_CamperParkerDefeat
	msgbox WaywardCave1F_Text_CamperParkerPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_CamperParkerIntro:
	.string "Huh? Are you lost too?\nNo? It doesn't matter.\pLet's have a quick Pokémon battle!$"

WaywardCave1F_Text_CamperParkerDefeat:
	.string "Lost?\nThere's nothing lost about this kid!$"

WaywardCave1F_Text_CamperParkerPost:
	.string "I got separated from my friends...\pI've got my Pokémon with me, so I'm\nOK, but...$"

WaywardCave1F_EventScript_RuinManiacGerald::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_GERALD, WaywardCave1F_Text_RuinManiacGeraldIntro, WaywardCave1F_Text_RuinManiacGeraldDefeat
	msgbox WaywardCave1F_Text_RuinManiacGeraldPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_RuinManiacGeraldIntro:
	.string "In deep tunnels and caves, there're\na couple things you're sure to see.\pZUBAT and Ruin Maniacs!$"

WaywardCave1F_Text_RuinManiacGeraldDefeat:
	.string "Your awesome power...\nIt's mystifying.$"

WaywardCave1F_Text_RuinManiacGeraldPost:
	.string "I've scoured every inch of this\nplace... Most of it while I was lost.\pAnyway, if there's one thing I can\nsay, this place can't be called ruins!$"

WaywardCave1F_EventScript_HikerLorenzo::
	trainerbattle_single TRAINER_SINNOH_HIKER_LORENZO, WaywardCave1F_Text_HikerLorenzoIntro, WaywardCave1F_Text_HikerLorenzoDefeat
	msgbox WaywardCave1F_Text_HikerLorenzoPost, MSGBOX_AUTOCLOSE
	end

WaywardCave1F_Text_HikerLorenzoIntro:
	.string "Wandering around, I got hungry, so\nI ate some wild mushrooms...\pThey gave me gas, and now I can't\nstop burping! Bluurrf!$"

WaywardCave1F_Text_HikerLorenzoDefeat:
	.string "Bleff! Hurk!\nI think...I'm getting better...$"

WaywardCave1F_Text_HikerLorenzoPost:
	.string "I hear there's a Pokémon that has\nmushrooms growing on its back.\pNot around here, somewhere far away.\nI wonder if they taste any good?$"
