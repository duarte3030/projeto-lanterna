#ifndef GUARD_CHAPTER_JUMP_H
#define GUARD_CHAPTER_JUMP_H

// Seletor de capítulo. Ver src/chapter_jump.c para a tabela e o porquê de cada
// decisão, e data/scripts/chapter_jump.inc para o roteiro dos dois menus.

extern const u8 ChapterJump_EventScript_Abrir[];

// Por onde o seletor foi aberto. Mora FORA da save de propósito: jogo novo e a
// primeira entrada no overworld acontecem no MESMO boot, então nenhum bit
// precisa sobreviver a um desligamento, e carregar save existente nunca passa
// por NewGameInitData. Zero flag e zero var de save gastas.
//
//   NADA       nunca foi pedido, ou já foi atendido (é o valor da save antiga)
//   PENDENTE   NewGameInitData acabou de rodar e o seletor ainda não apareceu
//   JOGO_NOVO  o seletor aberto agora é o do jogo novo, e a última entrada da
//              lista de regiões se chama "START FROM BEGINNING" em vez de "EXIT"
#define CHAPTER_JUMP_NADA      0
#define CHAPTER_JUMP_PENDENTE  1
#define CHAPTER_JUMP_JOGO_NOVO 2

extern u8 gChapterJumpModo;

#endif // GUARD_CHAPTER_JUMP_H
