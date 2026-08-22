@ Gerado por dev_scripts/cenas_galar.py (bloco c3 da fase de
@ conteudo). Rodar dev_scripts/mundo_galar.py apaga este arquivo;
@ rodar cenas_galar.py --aplicar o repoe. Corpo das cenas em
@ data/scripts/galar_cenas.inc.

Galar_Wedgehurst10_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Galar_Wedgehurst10_Tabela4
	.byte 0

Galar_Wedgehurst10_Tabela4:
	map_script_2 VAR_GALAR_G21M01_CENA, 1, GalarCena_G21M01_t4_v1
	map_script_2 VAR_GALAR_G21M01_CENA, 2, GalarCena_G21M01_t4_v2
	map_script_2 VAR_GALAR_G21M01_CENA, 3, GalarCena_G21M01_t4_v3
	map_script_2 VAR_GALAR_G21M01_CENA, 5, GalarCena_G21M01_t4_v5
	map_script_2 VAR_GALAR_G21M01_CENA, 6, GalarCena_G21M01_t4_v6
	map_script_2 VAR_GALAR_G21M01_CENA, 7, GalarCena_G21M01_t4_v7
	map_script_2 VAR_GALAR_G21M01_CENA, 8, GalarCena_G21M01_t4_v8
	.2byte 0
