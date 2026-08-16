@ PWTOutside do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ CHEREN (local id 1) e BIANCA (local id 2) ja vieram importados. Mesmo caso
@ da JUNIPER em Unova_FloccesyTown: EVENT_PWT_OUTSIDE_CHEREN_BIANCA e so
@ campo de esconde-objeto na fonte, a varredura de flags do PLANO nao o
@ capturou, zero flag nova nesta leva. ON_LOAD some com os dois usando
@ VAR_UNOVA_PWT_FORA_CENA (ja != 0 apos a despedida).
Unova_PWTOutside_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_PWTOutside_EventScript_AoCarregar
	.byte 0

Unova_PWTOutside_EventScript_AoCarregar::
	goto_if_eq VAR_UNOVA_PWT_FORA_CENA, 0, Unova_PWTOutside_EventScript_AoCarregarFim
	removeobject 1
	removeobject 2
Unova_PWTOutside_EventScript_AoCarregarFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Despedida de CHEREN/BIANCA (a divergencia de 1 var do PLANO). `addcellnum
@ PHONE_CHEREN` (registrar o numero no X-TRANSCIEVER) e o `GotCherensNumberText`
@ + `playsound SFX_REGISTER_PHONE_NUMBER` que vem junto foram DESCARTADOS: nao
@ ha sistema de contatos/telefone neste motor. O texto de convite ("register my
@ number...") em CasteliaCherenIntroText fica, e so a confirmacao mecanica sai.
Unova_PWTOutside_EventScript_PwtOutsideScript::
	lockall
	msgbox Unova_PWTOutside_Text_PwtOutsideBianceCherenText, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_PWTOutside_Movement_Saida
	applymovement 2, Unova_PWTOutside_Movement_Saida
	waitmovement 0
	removeobject 1
	removeobject 2
	clearflag FLAG_UNOVA_ASPERTIA_BLOQUEIO
	setvar VAR_UNOVA_PWT_FORA_CENA, 1
	releaseall
	end

Unova_PWTOutside_Movement_Saida:
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_PWTOutside_EventScript_Npc3::
	msgbox Unova_PWTOutside_Text_AskHiddenPowerText, MSGBOX_NPC
	end

Unova_PWTOutside_EventScript_Npc4::
	msgbox Unova_PWTOutside_Text_DVCheckerAskText, MSGBOX_NPC
	end

Unova_PWTOutside_EventScript_Npc5::
	msgbox Unova_PWTOutside_Text_PwtOutsideBugCatcherText, MSGBOX_NPC
	end

Unova_PWTOutside_EventScript_Npc6::
	msgbox Unova_PWTOutside_Text_PwtOutsideCooltrainerFText, MSGBOX_NPC
	end

Unova_PWTOutside_EventScript_Npc7::
	msgbox Unova_PWTOutside_Text_PwtOutsideCooltrainerMText, MSGBOX_NPC
	end

Unova_PWTOutside_EventScript_Npc8::
	msgbox Unova_PWTOutside_Text_PwtOutsideSailorText, MSGBOX_NPC
	end


Unova_PWTOutside_Text_AskHiddenPowerText::
	.string "I can sense the"
	.string "\nhidden potential"
	.string "\lof POKéMON."
	.string "\pWould you like me"
	.string "\nto tell you the"
	.string "\lhidden potential"
	.string "\lof your POKéMON?$"

Unova_PWTOutside_Text_DVCheckerAskText::
	.string "I can sense the"
	.string "\npotential of a"
	.string "\lPOKéMON's stats."
	.string "\pWould you like to"
	.string "\nknow your POKé-"
	.string "\lMON's potential?$"

Unova_PWTOutside_Text_PwtOutsideBugCatcherText::
	.string "Are you going to"
	.string "\ncompete in the"
	.string "\lTOURNAMENT?$"

Unova_PWTOutside_Text_PwtOutsideCooltrainerFText::
	.string "All the best"
	.string "\ntrainers in the"
	.string "\pregion come to"
	.string "\ncompete here."
	.string "\pI'm getting all"
	.string "\nfired up!$"

Unova_PWTOutside_Text_PwtOutsideCooltrainerMText::
	.string "I wonder who's"
	.string "\ngoing to be"
	.string "\lcompeting this"
	.string "\ltime."
	.string "\pSometimes the GYM"
	.string "\nLEADERs even"
	.string "\lcompete!$"

Unova_PWTOutside_Text_PwtOutsideBianceCherenText::
	.string "CHEREN: Ah,"
	.string "\n{PLAYER}. Good to"
	.string "\lsee you."
	.string "\pAre you here to"
	.string "\nenter the POKéMON"
	.string "\lWORLD TOURNAMENT?"
	.string "\pBIANCA: It's where"
	.string "\nall the strongest"
	.string "\ptrainers come to"
	.string "\ntest their"
	.string "\lstrength!"
	.string "\pCHEREN: Well if"
	.string "\nyou do enter, keep"
	.string "\lan eye out. We"
	.string "\pthink something"
	.string "\nsuspicious may be"
	.string "\lgoing on…"
	.string "\pBIANCA: See you"
	.string "\nat the TOURNAMENT,"
	.string "\l{PLAYER}!$"

Unova_PWTOutside_Text_PwtOutsideSailorText::
	.string "Aye! We ship in"
	.string "\nmaterials from"
	.string "\pCASTELIA for the"
	.string "\nTOURNAMENT.$"
