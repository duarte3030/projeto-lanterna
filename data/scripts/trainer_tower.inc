@ TÚMULO do script compartilhado da Trainer Tower de Sevii (decisão 28 do Gui,
@ cartucho 1 onda 4). Os onze mapas da torre viraram túmulo e os `scripts.inc`
@ deles ficaram só com o rótulo, então as 392 linhas que moravam aqui perderam
@ todos os textos e todos os `LOCALID_*` que citavam: eram eles os símbolos que
@ o linker acusou.
@
@ SOBROU UM RÓTULO, e ele não é decorativo. `src/field_control_avatar.c:557`
@ devolve `TrainerTower_EventScript_ShowTime` quando o jogador aperta A no
@ metatile `MB_TRAINER_TOWER_MONITOR`, e `include/event_scripts.h:767` declara o
@ símbolo. Esse metatile só existe DENTRO da torre, ou seja em mapa que virou
@ túmulo 1x1 e vazio, então o caminho está morto; mas tirar o rótulo obrigaria a
@ mexer no C, e mexer no C por causa de um caminho morto é trabalho a mais com
@ risco a mais. O rótulo fica, e não faz nada.

TrainerTower_EventScript_ShowTime::
	end
