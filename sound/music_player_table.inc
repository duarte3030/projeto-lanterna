@ NUM_TRACKS_BGM e NUM_TRACKS_SE2 subiram em 06/09/2026 (onda 5, cartucho 1).
@ Motivo: o pacote de faixas de HGSS e de DPPt tem 72 sequencias que pedem de
@ 11 a 16 trilhas simultaneas (mus_hg_violet 14, mus_hg_route30 14,
@ mus_hg_vs_gym_leader 14). Com o antigo NUM_TRACKS_BGM = 10 elas tocariam com
@ instrumento faltando SEM UMA LINHA DE ERRO no build, porque o driver corta a
@ trilha excedente em silencio. O teto do driver e MAX_MUSICPLAYER_TRACKS = 16
@ (include/gba/m4a_internal.h). SE2 e o player dos jingles (mus_level_up e
@ companhia, ver sound/song_table.inc) e os jingles de HGSS pedem ate 11.
@ Custo: (16-10 + 11-9) * TRACK_SIZE = 8 * 0x50 = 640 B de .bss em IWRAM.
@ Medido no link: IWRAM 28.396 B antes, 29.036 B depois.

	.equiv TRACK_SIZE, 0x50
	.equiv NUM_TRACKS_BGM, 16
	.equiv NUM_TRACKS_SE1, 3
	.equiv NUM_TRACKS_SE2, 11
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
