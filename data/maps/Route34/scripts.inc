@ Treinadores de rota de Route34, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route34_MapScripts::
	.byte 0

Route34_EventScript_YoungsterSamuel::
	trainerbattle_single TRAINER_JOHTO_SAMUEL, Route34_Text_YoungsterSamuelSeen, Route34_Text_YoungsterSamuelBeaten
	msgbox Route34_Text_YoungsterSamuelAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_YoungsterIan::
	trainerbattle_single TRAINER_JOHTO_IAN, Route34_Text_YoungsterIanSeen, Route34_Text_YoungsterIanBeaten
	msgbox Route34_Text_YoungsterIanAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_CamperTodd::
	trainerbattle_single TRAINER_JOHTO_TODD, Route34_Text_CamperToddSeen, Route34_Text_CamperToddBeaten
	msgbox Route34_Text_CamperToddAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_PicnickerGina::
	trainerbattle_single TRAINER_JOHTO_GINA, Route34_Text_PicnickerGinaSeen, Route34_Text_PicnickerGinaBeaten
	msgbox Route34_Text_PicnickerGinaAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_OfficerKeith::
	trainerbattle_single TRAINER_JOHTO_KEITH, Route34_Text_OfficerKeithSeen, Route34_Text_OfficerKeithBeaten
	msgbox Route34_Text_OfficerKeithAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_PokefanMBrandon::
	trainerbattle_single TRAINER_JOHTO_BRANDON, Route34_Text_PokefanMBrandonSeen, Route34_Text_PokefanMBrandonBeaten
	msgbox Route34_Text_PokefanMBrandonAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_Irene::
	trainerbattle_single TRAINER_JOHTO_IRENE, Route34_Text_IreneSeen, Route34_Text_IreneBeaten
	msgbox Route34_Text_IreneAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_Jenn::
	trainerbattle_single TRAINER_JOHTO_JENN, Route34_Text_JennSeen, Route34_Text_JennBeaten
	msgbox Route34_Text_JennAfter, MSGBOX_AUTOCLOSE
	end

Route34_EventScript_Kate::
	trainerbattle_single TRAINER_JOHTO_KATE, Route34_Text_KateSeen, Route34_Text_KateBeaten
	msgbox Route34_Text_KateAfter, MSGBOX_AUTOCLOSE
	end

Route34_Text_YoungsterSamuelSeen:
	.string "Hey! I'm looking for MANKEY!$"

Route34_Text_YoungsterSamuelBeaten:
	.string "Beaten by a passing stranger!$"

Route34_Text_YoungsterSamuelAfter:
	.string "I'm going to train even harder.\p"
	.string "After all, I'm trying to become\n"
	.string "a GYM LEADER.$"

Route34_Text_YoungsterIanSeen:
	.string "I'm the best in my class at\n"
	.string "POKéMON.$"

Route34_Text_YoungsterIanBeaten:
	.string "No! There are better trainers…$"

Route34_Text_YoungsterIanAfter:
	.string "I'm trying hard so I can be the\n"
	.string "star in my class.$"

Route34_Text_CamperToddSeen:
	.string "I'm confident in my ability to\n"
	.string "raise POKéMON.\p"
	.string "Want to see?$"

Route34_Text_CamperToddBeaten:
	.string "Did I screw up my training?$"

Route34_Text_CamperToddAfter:
	.string "Maybe I should take one to DAY-CARE,\n"
	.string "or maybe use some items…$"

Route34_Text_PicnickerGinaSeen:
	.string "Are you a TRAINER?\p"
	.string "Let's have a practice battle.$"

Route34_Text_PicnickerGinaBeaten:
	.string "Oh, no! I just can't win…$"

Route34_Text_PicnickerGinaAfter:
	.string "You're too strong to be a\n"
	.string "practice partner.$"

Route34_Text_OfficerKeithSeen:
	.string "Who goes there?\n"
	.string "What are you up to?$"

Route34_Text_OfficerKeithBeaten:
	.string "You're a tough little kid.$"

Route34_Text_OfficerKeithAfter:
	.string "Yep, nothing wrong today.\p"
	.string "Be good and stay out of trouble.$"

Route34_Text_PokefanMBrandonSeen:
	.string "I just got my POKéMON back from\n"
	.string "DAY-CARE.\p"
	.string "Let's see how much stronger it got!$"

Route34_Text_PokefanMBrandonBeaten:
	.string "Why does it end this way?$"

Route34_Text_PokefanMBrandonAfter:
	.string "My POKéMON came back with new moves.\p"
	.string "That confounded me to no end!$"

Route34_Text_IreneSeen:
	.string "IRENE: Who are you?!$"

Route34_Text_IreneBeaten:
	.string "IRENE: Ohhh! You're too strong!$"

Route34_Text_IreneAfter:
	.string "IRENE: Isn't this beach great?\p"
	.string "It's our secret little getaway!$"

Route34_Text_JennSeen:
	.string "JENN: What the...?\n"
	.string "What are you doing?$"

Route34_Text_JennBeaten:
	.string "JENN: So sorry, IRENE! Dear Sis!$"

Route34_Text_JennAfter:
	.string "JENN: Sunlight makes your body\n"
	.string "stronger.$"

Route34_Text_KateSeen:
	.string "KATE: I must pay you back for\n"
	.string "taking care of my sisters!$"

Route34_Text_KateBeaten:
	.string "KATE: No! I can't believe I lost.$"

Route34_Text_KateAfter:
	.string "KATE: I'm sorry we jumped you.\p"
	.string "We never expected anyone to find\n"
	.string "us here. You sure startled us.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route34_EventScript_Sign1::
	lock
	msgbox Route34_Text_Sign_Route34, MSGBOX_SIGN
	closemessage
	release
	end

Route34_EventScript_Sign2::
	lock
	msgbox Route34_Text_Sign_DayCare, MSGBOX_SIGN
	closemessage
	release
	end

Route34_EventScript_Sign3::
	lock
	msgbox Route34_Text_TrainerTips, MSGBOX_SIGN
	closemessage
	release
	end

Route34_Text_Sign_DayCare::
	.string "DAY-CARE\p"
	.string "LET US RAISE YOUR POKéMON FOR YOU!$"

Route34_Text_Sign_Route34::
	.string "ROUTE 34\n"
	.string "GOLDENROD CITY - AZALEA TOWN\p"
	.string "ILEX FOREST SOMEWHERE BETWEEN$"

Route34_Text_TrainerTips::
	.string "TRAINER TIPS\p"
	.string "BERRY trees grow new BERRIES\n"
	.string "several times a day.\p"
	.string "Note which trees bear which\n"
	.string "BERRIES.$"
