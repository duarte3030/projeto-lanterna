#ifndef GUARD_DIFFICULTY_CONSTANTS_H
#define GUARD_DIFFICULTY_CONSTANTS_H

#include "config/battle.h"

// ponytail: com B_VAR_DIFFICULTY == 0 (include/config/battle.h), a funcao
// GetCurrentDifficultyLevel() (src/difficulty.c:9) devolve DIFFICULTY_NORMAL
// SEMPRE, sem ler var nenhuma, e o trainerproc so emite [DIFFICULTY_NORMAL].
// As fatias EASY e HARD de gTrainers eram 277.160 B de zeros INALCANCAVEIS em
// ROM. Com uma dificuldade so, o designador [DIFFICULTY_NORMAL] vira [0] e o
// array encolhe sozinho: nenhum acessor, nenhum gerador e nenhum .party mudam,
// e a save nao guarda dificuldade. Dar um var a B_VAR_DIFFICULTY devolve as
// tres na hora. A suite (TESTING) continua com as tres, porque
// test/battle/trainer_control.h cadastra times em EASY e HARD.
// Os dois corpos ficam FORA do `enum` de proposito: tools/preproc/asm_file.cpp
// (linha 678) recusa um enum cujo primeiro elemento e uma diretiva `#`.
#if B_VAR_DIFFICULTY || TESTING
enum DifficultyLevel
{
    DIFFICULTY_EASY,
    DIFFICULTY_NORMAL, //If you rename this, the word "Normal" in fprint_trainers must be replaced with the new difficulty name.
    DIFFICULTY_HARD,
#if TESTING
    DIFFICULTY_TEST,
#endif
    DIFFICULTY_COUNT,
};
#else
enum DifficultyLevel
{
    DIFFICULTY_NORMAL,
    DIFFICULTY_COUNT,
};
#endif

#define DIFFICULTY_MIN 0
#define DIFFICULTY_MAX (DIFFICULTY_COUNT - 1)

#endif // GUARD_DIFFICULTY_CONSTANTS_H
