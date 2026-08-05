@ TwistMountain3F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_TwistMountain3F_MapScripts::
	.byte 0

Unova_TwistMountain3F_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_2, Unova_TwistMountain3F_Text_Worker1TwistMountain3FSeenText, Unova_TwistMountain3F_Text_Worker1TwistMountain3FBeatenText
	end

Unova_TwistMountain3F_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_3, Unova_TwistMountain3F_Text_Worker2TwistMountain3FSeenText, Unova_TwistMountain3F_Text_Worker2TwistMountain3FBeatenText
	end

Unova_TwistMountain3F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_VETERANF_TWIST_MOUNTAIN_1, Unova_TwistMountain3F_Text_VeteranFTwistMountain3FSeenText, Unova_TwistMountain3F_Text_VeteranFTwistMountain3FBeatenText
	end


Unova_TwistMountain3F_Text_Worker1TwistMountain3FSeenText::
	.string "TWIST MOUNTAIN has"
	.string "\nchanged over the"
	.string "\pyears, and this"
	.string "\nman changes in"
	.string "\levery battle!$"

Unova_TwistMountain3F_Text_Worker1TwistMountain3FBeatenText::
	.string "Go easy on… This"
	.string "\ngrown man?$"

Unova_TwistMountain3F_Text_Worker2TwistMountain3FSeenText::
	.string "Let's see you take"
	.string "\na powerful attack"
	.string "\pfrom veteran"
	.string "\nWORKERs like us!$"

Unova_TwistMountain3F_Text_Worker2TwistMountain3FBeatenText::
	.string "We've trained by"
	.string "\ndoing physical"
	.string "\pwork, so even if"
	.string "\nwe lose, we're"
	.string "\lstill powerful!$"

Unova_TwistMountain3F_Text_VeteranFTwistMountain3FSeenText::
	.string "TWIST MOUNTAIN's"
	.string "\nnumber one"
	.string "\ptactician! That's"
	.string "\nme!$"

Unova_TwistMountain3F_Text_VeteranFTwistMountain3FBeatenText::
	.string "Maybe I shouldn't"
	.string "\nbe satisfied with"
	.string "\pbeing number one"
	.string "\nonly on TWIST"
	.string "\lMOUNTAIN…$"
