@ MarineTube do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MarineTube_MapScripts::
	.byte 0

Unova_MarineTube_EventScript_Npc0::
	msgbox Unova_MarineTube_Text_MarineTubeCooltrainerFText, MSGBOX_NPC
	end

Unova_MarineTube_EventScript_Npc1::
	msgbox Unova_MarineTube_Text_MarineTubeCooltrainerMText, MSGBOX_NPC
	end

Unova_MarineTube_EventScript_Npc2::
	msgbox Unova_MarineTube_Text_MarineTubeLassText, MSGBOX_NPC
	end

Unova_MarineTube_EventScript_Npc3::
	msgbox Unova_MarineTube_Text_MarineTubePokefanMText, MSGBOX_NPC
	end

Unova_MarineTube_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_NURSERY_AIDE_MARINE_TUBE, Unova_MarineTube_Text_NurseryAideMarineTubeSeenText, Unova_MarineTube_Text_NurseryAideMarineTubeBeatenText
	end

Unova_MarineTube_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_TWINS_MARINE_TUBE, Unova_MarineTube_Text_TwinsMarineTubeSeenText, Unova_MarineTube_Text_TwinsMarineTubeBeatenText
	end

Unova_MarineTube_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_TWINS_MARINE_TUBE, Unova_MarineTube_Text_TwinsMarineTubeSeenText, Unova_MarineTube_Text_TwinsMarineTubeBeatenText
	end

Unova_MarineTube_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PRESCHOOLERM_MARINE_TUBE, Unova_MarineTube_Text_PreschoolerMMarineTubeSeenText, Unova_MarineTube_Text_PreschoolerMMarineTubeBeatenText
	end

Unova_MarineTube_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_PRESCHOOLERF_MARINE_TUBE, Unova_MarineTube_Text_PreschoolerFMarineTubeSeenText, Unova_MarineTube_Text_PreschoolerFMarineTubeBeatenText
	end


Unova_MarineTube_Text_MarineTubeCooltrainerFText::
	.string "Wow, look at all"
	.string "\nof the POKéMON"
	.string "\lunderwater!$"

Unova_MarineTube_Text_MarineTubeCooltrainerMText::
	.string "The MARINE TUBE"
	.string "\nis a great date"
	.string "\ldestination!$"

Unova_MarineTube_Text_MarineTubeLassText::
	.string "This tube serves"
	.string "\nas a shortcut to"
	.string "\pHUMILAU CITY, but"
	.string "\nthere are so many"
	.string "\ptourists that it's"
	.string "\nhard to get"
	.string "\lthrough!$"

Unova_MarineTube_Text_MarineTubePokefanMText::
	.string "Some people drop"
	.string "\ntheir valuables"
	.string "\pon the floor since"
	.string "\nit's so dark.$"

Unova_MarineTube_Text_NurseryAideMarineTubeSeenText::
	.string "You… are a rather"
	.string "\nadult looking kid…"
	.string "\pA kiddish adult…"
	.string "\nOh, jeez! I'll"
	.string "\pjust find out when"
	.string "\nwe battle!$"

Unova_MarineTube_Text_NurseryAideMarineTubeBeatenText::
	.string "You are an alto-"
	.string "\ngether mysterious"
	.string "\ltrainer!$"

Unova_MarineTube_Text_TwinsMarineTubeSeenText::
	.string "It's so fun to"
	.string "\nbattle along with"
	.string "\lmy sister!$"

Unova_MarineTube_Text_TwinsMarineTubeBeatenText::
	.string "Wow! What a"
	.string "\nsurprise!$"

Unova_MarineTube_Text_PreschoolerMMarineTubeSeenText::
	.string "Teacher?"
	.string "\pOh, you're not"
	.string "\nTeacher! You're a"
	.string "\ltrainer!$"

Unova_MarineTube_Text_PreschoolerMMarineTubeBeatenText::
	.string "It's hard to see"
	.string "\nin here!$"

Unova_MarineTube_Text_PreschoolerFMarineTubeSeenText::
	.string "Roar!"
	.string "\pI'm a POKéMON!$"

Unova_MarineTube_Text_PreschoolerFMarineTubeBeatenText::
	.string "I'm not really a"
	.string "\nPOKéMON!$"
