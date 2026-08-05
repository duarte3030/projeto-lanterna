@ Rt4 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt4_MapScripts::
	.byte 0

Unova_Rt4_EventScript_Placa0::
	msgbox Unova_Rt4_Text_R4DesertSignText, MSGBOX_SIGN
	end

Unova_Rt4_EventScript_Placa1::
	msgbox Unova_Rt4_Text_R4CasteliaSignText, MSGBOX_SIGN
	end

Unova_Rt4_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_RICH_BOY_R4, Unova_Rt4_Text_RichBoyR4SeenText, Unova_Rt4_Text_RichBoyR4BeatenText
	end

Unova_Rt4_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_ROUGHNECK_R4, Unova_Rt4_Text_RoughneckR4SeenText, Unova_Rt4_Text_RoughneckR4BeatenText
	end

Unova_Rt4_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_FISHER_R4_1, Unova_Rt4_Text_Fisher1R4SeenText, Unova_Rt4_Text_Fisher1R4BeatenText
	end

Unova_Rt4_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_FISHER_R4_2, Unova_Rt4_Text_Fisher2R4SeenText, Unova_Rt4_Text_Fisher2R4BeatenText
	end

Unova_Rt4_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_LADY_R4, Unova_Rt4_Text_LadyR4SeenText, Unova_Rt4_Text_LadyR4BeatenText
	end

Unova_Rt4_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_POLICEMAN_R4_1, Unova_Rt4_Text_Policeman1R4SeenText, Unova_Rt4_Text_Policeman1R4BeatenText
	end

Unova_Rt4_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_POLICEMAN_R4_2, Unova_Rt4_Text_Policeman2R4SeenText, Unova_Rt4_Text_Policeman2R4BeatenText
	end

Unova_Rt4_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_POKEFANM_R4, Unova_Rt4_Text_PokefanMR4SeenText, Unova_Rt4_Text_PokefanMR4BeatenText
	end

Unova_Rt4_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_POKEFANF_R4, Unova_Rt4_Text_PokefanFR4SeenText, Unova_Rt4_Text_PokefanFR4BeatenText
	end

Unova_Rt4_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_BIKER_R4, Unova_Rt4_Text_BikerR4SeenText, Unova_Rt4_Text_BikerR4BeatenText
	end


Unova_Rt4_Text_R4DesertSignText::
	.string "DESERT RESORT"
	.string "\nahead.$"

Unova_Rt4_Text_R4CasteliaSignText::
	.string "Access to"
	.string "\nCASTELIA CITY.$"

Unova_Rt4_Text_RichBoyR4SeenText::
	.string "I'll see if you're"
	.string "\nworthy to stand on"
	.string "\pthe same stage as"
	.string "\nme!$"

Unova_Rt4_Text_RichBoyR4BeatenText::
	.string "You've got what"
	.string "\nit takes!$"

Unova_Rt4_Text_RoughneckR4SeenText::
	.string "This ain't no"
	.string "\nplace for kids"
	.string "\llike you!$"

Unova_Rt4_Text_RoughneckR4BeatenText::
	.string "Just who are you?"
	.string "\nYou looked pretty"
	.string "\ltimid.$"

Unova_Rt4_Text_Fisher1R4SeenText::
	.string "You've been caught"
	.string "\nby a powerful"
	.string "\lhook, which is me!$"

Unova_Rt4_Text_Fisher1R4BeatenText::
	.string "That one got away!$"

Unova_Rt4_Text_Fisher2R4SeenText::
	.string "Check out my"
	.string "\nlively POKéMON,"
	.string "\pwhich I've"
	.string "\ngathered from all"
	.string "\laround UNOVA!$"

Unova_Rt4_Text_Fisher2R4BeatenText::
	.string "Mm hm… Looks like"
	.string "\nyou're even more"
	.string "\llively and fresh!$"

Unova_Rt4_Text_LadyR4SeenText::
	.string "A stylish POKéMON"
	.string "\nbattle is starting"
	.string "\lnow!$"

Unova_Rt4_Text_LadyR4BeatenText::
	.string "…What? It's over"
	.string "\nalready?$"

Unova_Rt4_Text_Policeman1R4SeenText::
	.string "What's a kid like"
	.string "\nyou doing around"
	.string "\lthese parts?$"

Unova_Rt4_Text_Policeman1R4BeatenText::
	.string "To have bested an"
	.string "\nofficer like me…"
	.string "\pWhat kind of a kid"
	.string "\nare you?$"

Unova_Rt4_Text_Policeman2R4SeenText::
	.string "Ah, that smell?"
	.string "\pMy POKéMON here"
	.string "\nseems to say that"
	.string "\pyou've got a"
	.string "\ndangerous smell"
	.string "\labout you!$"

Unova_Rt4_Text_Policeman2R4BeatenText::
	.string "I see…"
	.string "\nYour strength is"
	.string "\pcertainly quite"
	.string "\ndangerous…$"

Unova_Rt4_Text_PokefanMR4SeenText::
	.string "What? You're a"
	.string "\ntrainer? Awesome!$"

Unova_Rt4_Text_PokefanMR4BeatenText::
	.string "Oh well… Time for"
	.string "\nmy POKéMON to"
	.string "\lreturn…$"

Unova_Rt4_Text_PokefanFR4SeenText::
	.string "Now dance grace-"
	.string "\nfully! Bring forth"
	.string "\pyour beautiful"
	.string "\nmoves! Let us"
	.string "\pperform, my lovely"
	.string "\nPOKéMON!$"

Unova_Rt4_Text_PokefanFR4BeatenText::
	.string "Even though they"
	.string "\nlost, my POKéMON"
	.string "\lare still cute!$"

Unova_Rt4_Text_BikerR4SeenText::
	.string "A motorcycle in"
	.string "\nthe desert! It"
	.string "\pdoesn't get much"
	.string "\nmore wild than"
	.string "\lthis, eh?$"

Unova_Rt4_Text_BikerR4BeatenText::
	.string "Motorcycles aren't"
	.string "\ncomptible with"
	.string "\psand, and I'm not"
	.string "\ncompatible with"
	.string "\lyou!$"
