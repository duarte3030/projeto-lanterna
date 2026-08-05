@ ponytail: a subida para o Spear Pillar. O map.bin deste corredor so tem chao de
@ caverna, entao o ON_LOAD troca o tile (15,3) pelo metatile de escada 575, que e
@ exatamente o mesmo que este layout ja usa na escada de (8,12). Sem isso o
@ warp_def 2 ficaria inerte: warp so dispara em tile com behavior de warp
@ (src/field_control_avatar.c, IsWarpMetatileBehavior).
@
@ A escada e incondicional. Tranca-la ate a hora certa da historia pediria uma
@ flag ou uma var, e esta tarefa nao pode criar nenhuma das duas.

MtCoronet_1F_North_Room2_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MtCoronet_1F_North_Room2_OnLoad
	.byte 0

MtCoronet_1F_North_Room2_OnLoad:
	setmetatile 15, 3, 575, FALSE
	end
