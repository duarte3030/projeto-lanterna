#include "global.h"
#include "event_data.h"
#include "insignias.h"
#include "constants/flags.h"

// Ordem de cada lista = ordem do ginásio na região (a mesma do seletor de
// capítulo e do cartão do treinador).
static const u16 sInsigniasKanto[] =
{
    FLAG_BADGE01_GET, FLAG_BADGE02_GET, FLAG_BADGE03_GET, FLAG_BADGE04_GET,
    FLAG_BADGE05_GET, FLAG_BADGE06_GET, FLAG_BADGE07_GET, FLAG_BADGE08_GET,
};

static const u16 sInsigniasJohto[] =
{
    FLAG_INSIGNIA_JOHTO_1, FLAG_INSIGNIA_JOHTO_2, FLAG_INSIGNIA_JOHTO_3, FLAG_INSIGNIA_JOHTO_4,
    FLAG_INSIGNIA_JOHTO_5, FLAG_INSIGNIA_JOHTO_6, FLAG_INSIGNIA_JOHTO_7, FLAG_INSIGNIA_JOHTO_8,
};

// As 8 do Emerald (1 a 8) e depois as 8 do Hoenn EX (9 a 16), na numeração
// das flags; a ordem de visita no jogo intercala as duas, mas o cartão mostra
// as do Emerald na primeira página e as do EX na segunda.
static const u16 sInsigniasHoenn[] =
{
    FLAG_INSIGNIA_HOENN_1,  FLAG_INSIGNIA_HOENN_2,  FLAG_INSIGNIA_HOENN_3,  FLAG_INSIGNIA_HOENN_4,
    FLAG_INSIGNIA_HOENN_5,  FLAG_INSIGNIA_HOENN_6,  FLAG_INSIGNIA_HOENN_7,  FLAG_INSIGNIA_HOENN_8,
    FLAG_INSIGNIA_HOENN_9,  FLAG_INSIGNIA_HOENN_10, FLAG_INSIGNIA_HOENN_11, FLAG_INSIGNIA_HOENN_12,
    FLAG_INSIGNIA_HOENN_13, FLAG_INSIGNIA_HOENN_14, FLAG_INSIGNIA_HOENN_15, FLAG_INSIGNIA_HOENN_16,
};

static const u16 sInsigniasSinnoh[] =
{
    FLAG_INSIGNIA_SINNOH_1, FLAG_INSIGNIA_SINNOH_2, FLAG_INSIGNIA_SINNOH_3, FLAG_INSIGNIA_SINNOH_4,
    FLAG_INSIGNIA_SINNOH_5, FLAG_INSIGNIA_SINNOH_6, FLAG_INSIGNIA_SINNOH_7, FLAG_INSIGNIA_SINNOH_8,
};

static const struct
{
    const u16 *flags;
    u8 quantas;
} sRegioes[REGIAO_INSIGNIA_COUNT] =
{
    [REGIAO_INSIGNIA_KANTO]  = { sInsigniasKanto,  ARRAY_COUNT(sInsigniasKanto)  },
    [REGIAO_INSIGNIA_JOHTO]  = { sInsigniasJohto,  ARRAY_COUNT(sInsigniasJohto)  },
    [REGIAO_INSIGNIA_HOENN]  = { sInsigniasHoenn,  ARRAY_COUNT(sInsigniasHoenn)  },
    [REGIAO_INSIGNIA_SINNOH] = { sInsigniasSinnoh, ARRAY_COUNT(sInsigniasSinnoh) },
};

STATIC_ASSERT(ARRAY_COUNT(sInsigniasKanto) + ARRAY_COUNT(sInsigniasJohto)
            + ARRAY_COUNT(sInsigniasHoenn) + ARRAY_COUNT(sInsigniasSinnoh) == INSIGNIAS_TOTAL,
              insigniasSomamQuarenta);

u32 NumInsigniasDaRegiao(enum RegiaoInsignia regiao)
{
    return sRegioes[regiao].quantas;
}

u16 FlagDaInsignia(enum RegiaoInsignia regiao, u32 indice)
{
    return sRegioes[regiao].flags[indice];
}

u32 ContaInsigniasDaRegiao(enum RegiaoInsignia regiao)
{
    u32 i, n = 0;

    for (i = 0; i < sRegioes[regiao].quantas; i++)
    {
        if (FlagGet(sRegioes[regiao].flags[i]))
            n++;
    }
    return n;
}

u32 ContaTodasAsInsignias(void)
{
    u32 regiao, n = 0;

    for (regiao = 0; regiao < REGIAO_INSIGNIA_COUNT; regiao++)
        n += ContaInsigniasDaRegiao(regiao);
    return n;
}

// O MAIOR número de insígnias de uma mesma região, limitado a 8. É o que a
// obediência e a penalidade de captura usam no lugar da escada de Kanto:
// 8 de qualquer região (inclusive 8 das 16 de Hoenn) liberam tudo.
u32 InsigniasDaMelhorRegiao(void)
{
    u32 regiao, n, maior = 0;

    for (regiao = 0; regiao < REGIAO_INSIGNIA_COUNT; regiao++)
    {
        n = ContaInsigniasDaRegiao(regiao);
        if (n > maior)
            maior = n;
    }
    return maior > INSIGNIAS_OBEDIENCIA_TOTAL ? INSIGNIAS_OBEDIENCIA_TOTAL : maior;
}
