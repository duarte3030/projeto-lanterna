@ RustboroPart2: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 0.4) por dev_scripts/copia_planta_ex.py.

RustboroPart2_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 0.4), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
RustboroPart2_EventScript_ExNpc0::
	msgbox RustboroPart2_Text_ExNpc0, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc0:
	.string "Shhhh...\p"
	.string "Don’t tell anyone I’m here..\p"
	.string "I’m supposed to be in school right now!$"

RustboroPart2_EventScript_ExNpc1::
	msgbox RustboroPart2_Text_ExNpc1, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc1:
	.string "Apparently there is a GYM hidden in the\n"
	.string "depths of PETALBERG WOODS.\p"
	.string "When I graduate from school I’m going\n"
	.string "to find that gym and defeat it!$"

RustboroPart2_EventScript_ExNpc2::
	msgbox RustboroPart2_Text_ExNpc2, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc2:
	.string "I moved here to go to school.$"

RustboroPart2_EventScript_ExNpc5::
	msgbox RustboroPart2_Text_ExNpc5, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc5:
	.string "Man, ROXANNE’s so cool!\p"
	.string "I wish I could join her GYM.$"

RustboroPart2_EventScript_ExNpc6::
	msgbox RustboroPart2_Text_ExNpc6, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc6:
	.string "I’m going to catch you!$"

RustboroPart2_EventScript_ExNpc7::
	msgbox RustboroPart2_Text_ExNpc7, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc7:
	.string "Wait. Who’s chasing who?$"

RustboroPart2_EventScript_ExNpc8::
	msgbox RustboroPart2_Text_ExNpc8, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc8:
	.string "This corner of the city has is so green\n"
	.string "compared to the rest.\p"
	.string "I try to come here when I get free time.$"

RustboroPart2_EventScript_ExNpc9::
	msgbox RustboroPart2_Text_ExNpc9, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc9:
	.string "Diffrent places have unique ITEMS sold\n"
	.string "at POKéMARTs.\p"
	.string "You should check every POKéMART you\n"
	.string "come across.$"

RustboroPart2_EventScript_ExNpc10::
	msgbox RustboroPart2_Text_ExNpc10, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc10:
	.string "Most of these buildings were made with\n"
	.string "the help of POKéMON.\p"
	.string "The city would be half the size without\n"
	.string "their help!$"

RustboroPart2_EventScript_ExNpc11::
	msgbox RustboroPart2_Text_ExNpc11, MSGBOX_NPC
	end

RustboroPart2_Text_ExNpc11:
	.string "Lots of people in town work for DEVON\n"
	.string "INDUSTRIES.\p"
	.string "I do too, but I’m just saving up to\n"
	.string "become a POKéMON CONTEST idol!$"

RustboroPart2_EventScript_ExSign0::
	msgbox RustboroPart2_Text_ExSign0, MSGBOX_SIGN
	end

RustboroPart2_Text_ExSign0:
	.string "POKéMON TRAINER’S SCHOOL\p"
	.string "“We’ll teach you anything about\n"
	.string "POKéMON!”$"

RustboroPart2_EventScript_ExSign1::
	msgbox RustboroPart2_Text_ExSign1, MSGBOX_SIGN
	end

RustboroPart2_Text_ExSign1:
	.string "“Selected items for your convenience!”\n"
	.string "POKéMON MART$"

RustboroPart2_EventScript_ExSign2::
	msgbox RustboroPart2_Text_ExSign2, MSGBOX_SIGN
	end

RustboroPart2_Text_ExSign2:
	.string "“Selected items for your convenience!”\n"
	.string "POKéMON MART$"


@ Decisão 7: presentes do EX em RustboroPart2, reescritos.
RustboroPart2_EventScript_ExWideLens::
	lock
	faceplayer
	msgbox RustboroPart2_Text_HeyKid, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_HOENNEX_RUSTBORO_WIDE_LENS, RustboroPart2_EventScript_ExWideLensDepois
	msgbox RustboroPart2_Text_WantWideLens, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustboroPart2_EventScript_ExWideLensNao
	giveitem ITEM_WIDE_LENS
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_HOENNEX_RUSTBORO_WIDE_LENS
RustboroPart2_EventScript_ExWideLensDepois::
	msgbox RustboroPart2_Text_WideLensHits, MSGBOX_DEFAULT
	release
	end

RustboroPart2_EventScript_ExWideLensNao::
	msgbox RustboroPart2_Text_GoodLuckWithout, MSGBOX_DEFAULT
	release
	end

RustboroPart2_Text_HeyKid:
	.string "Hey kid.$"

RustboroPart2_Text_WantWideLens:
	.string "You’re a POKéMON TRAINER right?\n"
	.string "I’ve got a cool item called a WIDE LENSE.\p"
	.string "Do ya want it?$"

RustboroPart2_Text_WideLensHits:
	.string "That WIDE LENS maked moves more likely\n"
	.string "to hit.\p"
	.string "Gives ya a real competitive edge.$"

RustboroPart2_Text_GoodLuckWithout:
	.string "OK then. Good luck getting strong\n"
	.string "without it.$"

@ O EX tirou a OLD ROD do pescador de Dewford e pôs aqui, pedindo a insígnia da Roxanne
@ (0x4F0 = FLAG_DEFEATED_RUSTBORO_GYM). A flag do presente é a MESMA do de Dewford
@ (FLAG_RECEIVED_OLD_ROD, 0x101 no EX e no nosso): quem der primeiro dá, o outro só conversa.
RustboroPart2_EventScript_ExOldRod::
	lock
	faceplayer
	msgbox RustboroPart2_Text_LikeFishing, MSGBOX_DEFAULT
	goto_if_unset FLAG_DEFEATED_RUSTBORO_GYM, RustboroPart2_EventScript_ExOldRodSemInsignia
	goto_if_set FLAG_RECEIVED_OLD_ROD, RustboroPart2_EventScript_ExOldRodFim
	msgbox RustboroPart2_Text_TakeOldRod, MSGBOX_DEFAULT
	giveitem ITEM_OLD_ROD
	setflag FLAG_RECEIVED_OLD_ROD
RustboroPart2_EventScript_ExOldRodFim::
	msgbox RustboroPart2_Text_WayOfLife, MSGBOX_DEFAULT
	release
	end

RustboroPart2_EventScript_ExOldRodSemInsignia::
	msgbox RustboroPart2_Text_ComeBackBadge, MSGBOX_DEFAULT
	release
	end

RustboroPart2_Text_LikeFishing:
	.string "Do you like fishing?$"

RustboroPart2_Text_TakeOldRod:
	.string "Oh you have a GYM BADGE! Take this OLD\n"
	.string "ROD.$"

RustboroPart2_Text_WayOfLife:
	.string "Fishing is a way of life.$"

RustboroPart2_Text_ComeBackBadge:
	.string "Come back with a GYM BADGE and I’ll\n"
	.string "teach you how to fish!$"

