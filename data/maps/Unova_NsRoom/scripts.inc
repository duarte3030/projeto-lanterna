@ NsRoom do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NsRoom_MapScripts::
	.byte 0

Unova_NsRoom_EventScript_Npc0::
	goto Unova_NsRoom_EventScript_N


Unova_NsRoom_Text_NsRoomIntroText::
	.string "You…"
	.string "\pYou're the one who"
	.string "\nstopped the PLASMA"
	.string "\pSHADOWs' ill"
	.string "\nconceived plan,"
	.string "\laren't you?"
	.string "\pTheir plot was a"
	.string "\nfoolish one, but I"
	.string "\pwouldn't neces-"
	.string "\nsarily call them"
	.string "\levil…"
	.string "\pI can understand"
	.string "\nthe desire to get"
	.string "\pback someone"
	.string "\nprecious to you,"
	.string "\peven if you know"
	.string "\ndeep down that it"
	.string "\pwill never be the"
	.string "\nsame as it once"
	.string "\lwas…"
	.string "\pBut they put an"
	.string "\ninnocent POKéMON"
	.string "\pin danger, and"
	.string "\nthat, I cannot"
	.string "\lforgive."
	.string "\pThat creature…"
	.string "\pThough it was"
	.string "\ncreated artific-"
	.string "\lially, it is still"
	.string "\la POKéMON."
	.string "\pIt deserves to"
	.string "\nlive a happy life,"
	.string "\pas all POKéMON and"
	.string "\npeople do."
	.string "\pYou… You've come"
	.string "\nin search of the"
	.string "\lPOKéMON, right?"
	.string "\pWell, it's no"
	.string "\nlonger here."
	.string "\pBut before I tell"
	.string "\nyou where it went,"
	.string "\pI need to see what"
	.string "\nkind of a trainer"
	.string "\lyou are."
	.string "\pCome! Show me the"
	.string "\npower of the POKé-"
	.string "\lMON who defeated"
	.string "\lTEAM PLASMA!$"

@ >>> cena importada por dev_scripts/importa_chefes_faltantes.py >>>
Unova_NsRoom_EventScript_N::
	trainerbattle_single TRAINER_UNOVA_N, Unova_NsRoom_Text_NsRoomIntroText, Unova_NsRoom_Text_NBeaten
	msgbox Unova_NsRoom_Text_NDepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_N
	removeobject LOCALID_UNOVA_NS_ROOM_N
	release
	end

Unova_NsRoom_Text_NBeaten::
	.string "I see… So that's\n"
	.string "the kind of\l"
	.string "trainer you are…$"

Unova_NsRoom_Text_NDepois::
	.string "Your POKéMON…\p"
	.string "I can hear them.\p"
	.string "You truly are a\n"
	.string "kind and noble\l"
	.string "trainer.$"
@ <<< cena importada por dev_scripts/importa_chefes_faltantes.py <<<
