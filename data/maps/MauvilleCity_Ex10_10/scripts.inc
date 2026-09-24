@ MauvilleCity_Ex10_10: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 10.10) por dev_scripts/copia_planta_ex.py.

MauvilleCity_Ex10_10_MapScripts::
	.byte 0

@ Lateral do Pokémon Emerald EX (decisão 7 do Fable), reescrito do script da ROM:
@ a moça dá o Eon Ticket uma vez; depois de encontrar o Latios ou a Latias ela
@ comenta (FLAG_ENCOUNTERED_LATIAS_OR_LATIOS, a mesma flag vanilla que o EX lê).
MauvilleCity_Ex10_10_EventScript_EonTicketLady::
	lock
	faceplayer
	goto_if_unset FLAG_HOENNEX_RECEIVED_EON_TICKET_MAUVILLE, MauvilleCity_Ex10_10_EventScript_EonTicketGift
	goto_if_set FLAG_ENCOUNTERED_LATIAS_OR_LATIOS, MauvilleCity_Ex10_10_EventScript_EonTicketChampion
	msgbox MauvilleCity_Ex10_10_Text_SayHello, MSGBOX_DEFAULT
	closemessage
	release
	end

MauvilleCity_Ex10_10_EventScript_EonTicketChampion::
	msgbox MauvilleCity_Ex10_10_Text_Champion, MSGBOX_DEFAULT
	closemessage
	release
	end

MauvilleCity_Ex10_10_EventScript_EonTicketGift::
	applymovement LOCALID_MAUVILLE_EX10_10_LADY, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox MauvilleCity_Ex10_10_Text_OhHello, MSGBOX_DEFAULT
	applymovement LOCALID_MAUVILLE_EX10_10_LADY, MauvilleCity_Ex10_10_Movement_LookAtBall
	waitmovement 0
	removeobject LOCALID_MAUVILLE_EX10_10_BALL
	applymovement LOCALID_MAUVILLE_EX10_10_LADY, MauvilleCity_Ex10_10_Movement_Pause
	waitmovement 0
	applymovement LOCALID_MAUVILLE_EX10_10_LADY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox MauvilleCity_Ex10_10_Text_LongAgo, MSGBOX_DEFAULT
	giveitem ITEM_EON_TICKET
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_EON_TICKET_MAUVILLE
	msgbox MauvilleCity_Ex10_10_Text_SayHello, MSGBOX_DEFAULT
	closemessage
	release
	end

MauvilleCity_Ex10_10_Movement_LookAtBall:
	delay_16
	face_up
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	step_end

MauvilleCity_Ex10_10_Movement_Pause:
	delay_16
	delay_16
	delay_16
	step_end

MauvilleCity_Ex10_10_Text_OhHello:
	.string "Oh hello!\p"
	.string "You surprised me, visitors are rare in my\n"
	.string "little alcove.\p"
	.string "...Your POKéMON seem to like you a great\n"
	.string "deal. Hmm... Maybe you could be the one...$"

MauvilleCity_Ex10_10_Text_LongAgo:
	.string "Long ago, I befriended a certain\n"
	.string "POKéMON.\p"
	.string "This POKéMON and I traveled the world\n"
	.string "together. But, I’m afraid my days of\l"
	.string "travel are over.\p"
	.string "If you use this ticket, please, take\n"
	.string "good care of them.$"

MauvilleCity_Ex10_10_Text_SayHello:
	.string "Say hello for me.$"

MauvilleCity_Ex10_10_Text_Champion:
	.string "So, the CHAMPION pays me a visit\p"
	.string "Ah, I can sense you met my POKéMON...\p"
	.string "That’s good.\p"
	.string "Don’t tell me what they’re up to.\p"
	.string "It’s your story now.$"

