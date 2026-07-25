LakeAcuity_MapScripts::
	.byte 0

LakeAcuity_EventScript_Hiker::
	msgbox LakeAcuity_Text_Hiker, MSGBOX_NPC
	end

LakeAcuity_EventScript_SwimmerF::
	msgbox LakeAcuity_Text_SwimmerF, MSGBOX_NPC
	end

LakeAcuity_Text_Hiker:
	.string "This snow never seems to melt,\n"
	.string "even when spring comes to Sinnoh.$"

LakeAcuity_Text_SwimmerF:
	.string "Brrr! Too cold to swim here,\n"
	.string "but the view is worth the walk.$"
