@ LentimasGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_LentimasGym_MapScripts::
	.byte 0

Unova_LentimasGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_SHAUNTAL, Unova_LentimasGym_Text_ShauntalGymIntroText2, Unova_LentimasGym_Text_ShauntalWinLossText, Unova_LentimasGym_EventScript_Insignia0
	end

Unova_LentimasGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_LENTIMAS
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_LentimasGym_EventScript_Npc1::
	msgbox Unova_LentimasGym_Text_LentimasGymGuyText, MSGBOX_NPC
	end

Unova_LentimasGym_EventScript_Npc2::
	msgbox Unova_LentimasGym_Text_HexManiacLentimasGym1AfterText, MSGBOX_NPC
	end

Unova_LentimasGym_EventScript_Npc3::
	msgbox Unova_LentimasGym_Text_HexManiacLentimasGym2AfterText, MSGBOX_NPC
	end

Unova_LentimasGym_EventScript_Npc4::
	msgbox Unova_LentimasGym_Text_HexManiacLentimasGym3AfterText, MSGBOX_NPC
	end

Unova_LentimasGym_EventScript_Npc5::
	msgbox Unova_LentimasGym_Text_HexManiacLentimasGym4AfterText, MSGBOX_NPC
	end


Unova_LentimasGym_Text_ShauntalGymIntroText2::
	.string "…Oh, sorry. I"
	.string "\ndidn't see you"
	.string "\lthere."
	.string "\pI'm working on a"
	.string "\ndraft of my new"
	.string "\lnovel."
	.string "\pMy name is"
	.string "\nSHAUNTAL."
	.string "\pI used to be a"
	.string "\nmember of the"
	.string "\lELITE FOUR."
	.string "\pI moved to this"
	.string "\nsleepy little town"
	.string "\pto work on my"
	.string "\nwriting, but I"
	.string "\pstill run this"
	.string "\nGYM in my spare"
	.string "\ltime."
	.string "\pWould you like to"
	.string "\nchallenge me? I"
	.string "\lwon't hold back.$"

Unova_LentimasGym_Text_ShauntalWinLossText::
	.string "Impressive…"
	.string "\pYour skills will"
	.string "\nmake a great"
	.string "\lstory.$"

Unova_LentimasGym_Text_LentimasGymGuyText::
	.string "Yo, challenger!"
	.string "\pSHAUNTAL may look"
	.string "\nlike a bookworm,"
	.string "\pbut she's got"
	.string "\nserious knowledge"
	.string "\lof ghosts!"
	.string "\pIt's going to be"
	.string "\ntough without my"
	.string "\ladvice."
	.string "\pLet's see… Ghost"
	.string "\nPOKéMON don't like"
	.string "\lbeing hit by"
	.string "\lother ghosts."
	.string "\pDark-type moves"
	.string "\nare super-effec-"
	.string "\ltive too.$"

Unova_LentimasGym_Text_HexManiacLentimasGym1AfterText::
	.string "Ghost type POKéMON"
	.string "\ncannot be harmed"
	.string "\pby normal type"
	.string "\nattacks!$"

Unova_LentimasGym_Text_HexManiacLentimasGym2AfterText::
	.string "We hide in the"
	.string "\nshadows and wait"
	.string "\pto scare passers-"
	.string "\nby. Just like a"
	.string "\lghost!$"

Unova_LentimasGym_Text_HexManiacLentimasGym3AfterText::
	.string "I need more guid-"
	.string "\nance from SHAUNTAL"
	.string "\pif I want to get"
	.string "\nstronger…"
	.string "\pShe should hurry"
	.string "\nup and put out the"
	.string "\lnext book already!$"

Unova_LentimasGym_Text_HexManiacLentimasGym4AfterText::
	.string "I came to this"
	.string "\ntown to search for"
	.string "\pghosts. It's great"
	.string "\nif you're into the"
	.string "\lsupernatural!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd gymstatue1 do BW3G: nome do mapa + "#MON GYM"
Unova_LentimasGym_EventScript_EstatuaGinasio::
	msgbox Unova_LentimasGym_Text_EstatuaGinasio, MSGBOX_SIGN
	end

Unova_LentimasGym_Text_EstatuaGinasio::
	.string "LENTIMAS TOWN\n"
	.string "POKéMON GYM$"
