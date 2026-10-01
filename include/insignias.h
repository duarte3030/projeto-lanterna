#ifndef GUARD_INSIGNIAS_H
#define GUARD_INSIGNIAS_H

// As 40 insígnias do cartucho 1, por região (decisão do Gui de 30/09/2026).
// Kanto são FLAG_BADGE01_GET..08 (as do motor: golpes de campo e o seletor de
// capítulo continuam lendo só elas); Johto, Hoenn (16, com as do Hoenn EX) e
// Sinnoh são as FLAG_INSIGNIA_* de include/constants/flags.h. Nenhuma flag nova:
// este arquivo só junta as que já existem, então o save não muda.

enum RegiaoInsignia
{
    REGIAO_INSIGNIA_KANTO,
    REGIAO_INSIGNIA_JOHTO,
    REGIAO_INSIGNIA_HOENN,
    REGIAO_INSIGNIA_SINNOH,
    REGIAO_INSIGNIA_COUNT,
};

#define INSIGNIAS_MAX_POR_REGIAO 16
#define INSIGNIAS_TOTAL          40
// Quantas insígnias de UMA região liberam a obediência total.
#define INSIGNIAS_OBEDIENCIA_TOTAL 8

u32 NumInsigniasDaRegiao(enum RegiaoInsignia regiao);
u16 FlagDaInsignia(enum RegiaoInsignia regiao, u32 indice);
u32 ContaInsigniasDaRegiao(enum RegiaoInsignia regiao);
u32 ContaTodasAsInsignias(void);
u32 InsigniasDaMelhorRegiao(void);

#endif // GUARD_INSIGNIAS_H
