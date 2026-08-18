GalacticHq4F_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ BLOQUEADO (S6, 18/08/2026). GalacticHQ4F_CoordEvent_Cyrus (script 1) e so a
@ aproximacao ("A fala foi uma grande mentira" / "Sei por que voce esta
@ aqui") que abre direto pra GalacticHQ4F_Cyrus: StartTrainerBattle contra
@ TRAINER_GALACTIC_BOSS_CYRUS_GALACTIC_HQ (premio: Master Ball). Esse
@ treinador nao existe em opponents.h e nao e nenhum dos 3 pre-atribuidos da
@ onda 4 (Pastoria); bater esta cena sem a batalha deixava o Cyrus travado no
@ meio da fala, pior que o skeleton. Falta o executor de treinadores desta
@ leva definir TRAINER_GALACTIC_BOSS_CYRUS_GALACTIC_HQ; ai sim a aproximacao
@ (LOCALID_CYRUS a acrescentar ao map.json, sem flag: a fonte nunca esconde
@ este Cyrus por FLAG_HIDE_GALACTIC_HQ_4F_CYRUS, so o campo hidden_flag do
@ objeto aponta pra ela, sem SetFlag/ClearFlag em lugar nenhum) e a batalha
@ entram juntas.
GalacticHq4F_EventScript_CoordEvent_Cyrus::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

GalacticHq4F_EventScript_Placa1::
	msgbox GalacticHq4F_Text_Placa1, MSGBOX_SIGN
	end

GalacticHq4F_Text_Placa1:
	.string "Team Galactic Report$"
