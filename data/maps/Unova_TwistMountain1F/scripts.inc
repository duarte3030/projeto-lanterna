@ TwistMountain1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_TwistMountain1F_MapScripts::
	.byte 0

Unova_TwistMountain1F_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_5, Unova_TwistMountain1F_Text_WorkerTwistMountain1FSeenText, Unova_TwistMountain1F_Text_WorkerTwistMountain1FBeatenText
	end

Unova_TwistMountain1F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_VETERANM_TWIST_MOUNTAIN_2, Unova_TwistMountain1F_Text_VeteranMTwistMountain1FSeenText, Unova_TwistMountain1F_Text_VeteranMTwistMountain1FBeatenText
	end


Unova_TwistMountain1F_Text_WorkerTwistMountain1FSeenText::
	.string "Check out the"
	.string "\ncombination of my"
	.string "\pcool POKéMON and"
	.string "\nmy hot fighting"
	.string "\lspirit!$"

Unova_TwistMountain1F_Text_WorkerTwistMountain1FBeatenText::
	.string "It looks like you"
	.string "\nalso have a hot-"
	.string "\land-cool"
	.string "\lcombination!$"

Unova_TwistMountain1F_Text_VeteranMTwistMountain1FSeenText::
	.string "I come here every"
	.string "\nyear to train. The"
	.string "\pcold, harsh envi-"
	.string "\nronment really"
	.string "\pbrings out a POKé-"
	.string "\nMON's strength!$"

Unova_TwistMountain1F_Text_VeteranMTwistMountain1FBeatenText::
	.string "How harsh…$"
