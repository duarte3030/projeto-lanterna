@ NUM_TRACKS_BGM subiu de 10 para 16 em 28/10/2026 (fase 0 do PRD de assets),
@ o mesmo valor que o master usa desde d2c016b6f8 (06/09/2026). O driver corta
@ em silêncio a trilha que passa do número reservado, sem uma linha de erro no
@ build, e as faixas que as frentes de música vão trazer (Cloud White de Unova
@ e as conversões das regiões 3D) pedem até 16. O teto do driver é
@ MAX_MUSICPLAYER_TRACKS = 16 (include/gba/m4a_internal.h). Hoje nenhuma das
@ 530 faixas desta branch passa de 10 trilhas, então nada muda no que toca.
@ Custo: (16 - 10) * TRACK_SIZE = 6 * 0x50 = 480 B de .bss em IWRAM.
@ O NUM_TRACKS_SE2 (jingles) ficou em 9: o master subiu para 11 por causa dos
@ jingles de HGSS, que esta branch não tem.

	.equiv TRACK_SIZE, 0x50
	.equiv NUM_TRACKS_BGM, 16
	.equiv NUM_TRACKS_SE1, 3
	.equiv NUM_TRACKS_SE2, 9
	.equiv NUM_TRACKS_SE3, 1

	.bss
	.align 2

gMPlayTrack_BGM::
	.space TRACK_SIZE * NUM_TRACKS_BGM
	.size gMPlayTrack_BGM, .-gMPlayTrack_BGM

gMPlayTrack_SE1::
	.space TRACK_SIZE * NUM_TRACKS_SE1
	.size gMPlayTrack_SE1, .-gMPlayTrack_SE1

gMPlayTrack_SE2::
	.space TRACK_SIZE * NUM_TRACKS_SE2
	.size gMPlayTrack_SE2, .-gMPlayTrack_SE2

gMPlayTrack_SE3::
	.space TRACK_SIZE * NUM_TRACKS_SE3
	.size gMPlayTrack_SE3, .-gMPlayTrack_SE3

	.section .rodata

	.align 2
gMPlayTable::
	music_player gMPlayInfo_BGM, gMPlayTrack_BGM, NUM_TRACKS_BGM, 0
	music_player gMPlayInfo_SE1, gMPlayTrack_SE1, NUM_TRACKS_SE1, 1
	music_player gMPlayInfo_SE2, gMPlayTrack_SE2, NUM_TRACKS_SE2, 1
	music_player gMPlayInfo_SE3, gMPlayTrack_SE3, NUM_TRACKS_SE3, 0
