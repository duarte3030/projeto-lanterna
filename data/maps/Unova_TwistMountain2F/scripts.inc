@ TwistMountain2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_TwistMountain2F_MapScripts::
	.byte 0

Unova_TwistMountain2F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_4, Unova_TwistMountain2F_Text_WorkerTwistMountain2FSeenText, Unova_TwistMountain2F_Text_WorkerTwistMountain2FBeatenText
	end

Unova_TwistMountain2F_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_HIKER_TWIST_MOUNTAIN_1, Unova_TwistMountain2F_Text_HikerTwistMountain2FSeenText, Unova_TwistMountain2F_Text_HikerTwistMountain2FBeatenText
	end

Unova_TwistMountain2F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_VETERANF_TWIST_MOUNTAIN_2, Unova_TwistMountain2F_Text_VeteranFTwistMountain2FSeenText, Unova_TwistMountain2F_Text_VeteranFTwistMountain2FBeatenText
	end


Unova_TwistMountain2F_Text_WorkerTwistMountain2FSeenText::
	.string "Hold up there,"
	.string "\nyoungster!"
	.string "\pA battle will help"
	.string "\nyou warm up!$"

Unova_TwistMountain2F_Text_WorkerTwistMountain2FBeatenText::
	.string "Ha! Battling gets"
	.string "\nme so warm, I've"
	.string "\lstarted sweating!$"

Unova_TwistMountain2F_Text_HikerTwistMountain2FSeenText::
	.string "When I'm surrounded"
	.string "\nby rocks, my"
	.string "\lspirit goes up!$"

Unova_TwistMountain2F_Text_HikerTwistMountain2FBeatenText::
	.string "When I lose, my"
	.string "\nspirits sink…$"

Unova_TwistMountain2F_Text_VeteranFTwistMountain2FSeenText::
	.string "In battles, it's"
	.string "\nalso important to"
	.string "\pknow what moves"
	.string "\nnot to make.$"

Unova_TwistMountain2F_Text_VeteranFTwistMountain2FBeatenText::
	.string "I've been training"
	.string "\nfor years now, but"
	.string "\pit's still not"
	.string "\nenough…$"
