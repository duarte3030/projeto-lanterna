@ LentimasGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 12/08/2026 (B5): as quatro EMBOSCADAS, o quebra-cabeca daqui.
@
@ Mesma historia do ginasio de Aspertia: as quatro HEX_MANIAC estavam no mapa so
@ com o texto de DEPOIS da batalha, porque no BW3G elas sao OBJECTTYPE_SCRIPT com
@ `loadtrainer` dentro de script de `coord_event`, e a varredura do B4 so via
@ OBJECTTYPE_TRAINER. Constantes novas 2456 a 2459, times de
@ fontes-mapas/bw3g/data/trainers/parties.asm.
@
@ Nove coord_events, nas coordenadas exatas da fonte, todos conferidos contra a
@ grade de colisao deste layout (16x20): 3 tiles para a primeira (a coluna 1,
@ linhas 6 a 8), 3 para a segunda (a linha 7, colunas 8 a 10), 2 para a terceira
@ (a linha 10, colunas 4 e 5) e 1 para a quarta (11,11). O numero de tiles nao e
@ enfeite: e a largura da passagem naquele ponto, e um tile a menos deixa um
@ desvio por onde o jogador escapa sem lutar.
@
@ Custo: ZERO var e ZERO flag. Gatilho VAR_TEMP_0 valor 0 (tecnica 1 do
@ SINNOH-PADRAO.md) e a memoria do "ja perdeu" e a flag de treinador do motor,
@ lida por goto_if_defeated.

Unova_LentimasGym_MapScripts::
	.byte 0

Unova_LentimasGym_EventScript_Emboscada1::
	lock
	goto_if_defeated TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_1, Unova_LentimasGym_EventScript_EmboscadaFim
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_1, Unova_LentimasGym_Text_Hex1Seen, Unova_LentimasGym_Text_Hex1Beaten
	release
	end

Unova_LentimasGym_EventScript_Emboscada2::
	lock
	goto_if_defeated TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_2, Unova_LentimasGym_EventScript_EmboscadaFim
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_2, Unova_LentimasGym_Text_Hex2Seen, Unova_LentimasGym_Text_Hex2Beaten
	release
	end

Unova_LentimasGym_EventScript_Emboscada3::
	lock
	goto_if_defeated TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_3, Unova_LentimasGym_EventScript_EmboscadaFim
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_3, Unova_LentimasGym_Text_Hex3Seen, Unova_LentimasGym_Text_Hex3Beaten
	release
	end

Unova_LentimasGym_EventScript_Emboscada4::
	lock
	goto_if_defeated TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_4, Unova_LentimasGym_EventScript_EmboscadaFim
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_LENTIMAS_GYM_4, Unova_LentimasGym_Text_Hex4Seen, Unova_LentimasGym_Text_Hex4Beaten
	release
	end

Unova_LentimasGym_EventScript_EmboscadaFim::
	release
	end

Unova_LentimasGym_Text_Hex1Seen::
	.string "Eh he he… We have"
	.string "\ntrained with the"
	.string "\lspirits."
	.string "\pCan you even"
	.string "\ndamage our"
	.string "\lPOKéMON?$"

Unova_LentimasGym_Text_Hex1Beaten::
	.string "Ack! I've been"
	.string "\nbeaten!$"

Unova_LentimasGym_Text_Hex2Seen::
	.string "Aha! How can you"
	.string "\ndefeat that which"
	.string "\pyou cannot even"
	.string "\nsee?$"

Unova_LentimasGym_Text_Hex2Beaten::
	.string "You've found my"
	.string "\nweakness!$"

Unova_LentimasGym_Text_Hex3Seen::
	.string "I have been a"
	.string "\ndisciple of"
	.string "\pSHAUNTAL since I"
	.string "\nwas young."
	.string "\pThere's no way you"
	.string "\ncan beat me!$"

Unova_LentimasGym_Text_Hex3Beaten::
	.string "Okay, I admit it!"
	.string "\nI'm just a fan of"
	.string "\lher books!$"

Unova_LentimasGym_Text_Hex4Seen::
	.string "A spooky mountain"
	.string "\ntown with a spooky"
	.string "\lghost type GYM?"
	.string "\pThat's just"
	.string "\nperfect for a"
	.string "\lspooky girl"
	.string "\llike me!$"

Unova_LentimasGym_Text_Hex4Beaten::
	.string "Ah! You're scary!$"

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
