#!/usr/bin/env python3
"""Regera src/data/pokemon/experience_tables.h para um MAX_LEVEL qualquer.

Uso: python3 dev_scripts/gen_experience_tables.py 250

As fórmulas oficiais só são válidas até o nível 100. Acima disso, apenas a
curva Erratic quebra: o ramo (160 - n) * n^3 / 100 atinge o pico no nível 120
e fica negativo a partir do 160. Aqui ela passa a seguir n^3 - 400000, que
encosta exatamente nos 600000 do nível 100 e cresce sem quebrar.

CUBE usa (u32) de propósito: em int, ((n / 2) + 32) * n^3 da curva Fluctuating
estoura o sinal a partir do nível 249 e o gcc recusa compilar.
"""
import sys

GROWTH_RATES = ["MEDIUM_FAST", "ERRATIC", "FLUCTUATING", "MEDIUM_SLOW", "FAST", "SLOW"]

# ponytail: só existe pra provar monotonia e ausência de estouro de u32.
# Os valores de verdade quem calcula é o pré-processador C, pelos macros do header.
def exp_at(rate, n):
    if rate == "MEDIUM_FAST":   return n ** 3
    if rate == "FAST":          return 4 * n ** 3 // 5
    if rate == "SLOW":          return 5 * n ** 3 // 4
    if rate == "MEDIUM_SLOW":   return 6 * n ** 3 // 5 - 15 * n * n + 100 * n - 140
    if rate == "FLUCTUATING":
        if n <= 15: return ((n + 1) // 3 + 24) * n ** 3 // 50
        if n <= 36: return (n + 14) * n ** 3 // 50
        return ((n // 2) + 32) * n ** 3 // 50
    if rate == "ERRATIC":
        if n <= 50: return (100 - n) * n ** 3 // 50
        if n <= 68: return (150 - n) * n ** 3 // 100
        if n <= 98: return ((1911 - 10 * n) // 3) * n ** 3 // 500
        if n <= 100: return (160 - n) * n ** 3 // 100
        return n ** 3 - 400000
    raise ValueError(rate)


HEADER = """#define SQUARE(n) ((n) * (n))
#define CUBE(n) ((u32)(n) * (n) * (n))

#define EXP_SLOW(n) ((5 * CUBE(n)) / 4) // (5 * (n)^3) / 4
#define EXP_FAST(n) ((4 * CUBE(n)) / 5) // (4 * (n)^3) / 5
#define EXP_MEDIUM_FAST(n) (CUBE(n)) // (n)^3
#define EXP_MEDIUM_SLOW(n) ((6 * CUBE(n)) / 5 - (15 * SQUARE(n)) + (100 * n) - 140)    // (6 * (n)^3) / 5 - (15 * (n)^2) + (100 * n) - 140
#define EXP_ERRATIC(n)                                      \\
     (n <= 50) ? ((100 - n) * CUBE(n) /  50)                \\
    :(n <= 68) ? ((150 - n) * CUBE(n) / 100)                \\
    :(n <= 98) ? (((1911 - 10 * n) / 3) * CUBE(n) / 500)    \\
    :(n <= 100)? ((160 - n) * CUBE(n) / 100)                \\
    :            (CUBE(n) - 400000)
#define EXP_FLUCTUATING(n)                                  \\
     (n <= 15) ? (((n + 1) / 3 + 24) * CUBE(n) / 50)        \\
    :(n <= 36) ? ((n + 14)           * CUBE(n) / 50)        \\
    :            (((n / 2) + 32)     * CUBE(n) / 50)

const u32 gExperienceTables[][MAX_LEVEL + 1] =
{
"""

NAMES = {"MEDIUM_FAST": "Medium Fast", "ERRATIC": "Erratic", "FLUCTUATING": "Fluctuating",
         "MEDIUM_SLOW": "Medium Slow", "FAST": "Fast", "SLOW": "Slow"}


def check(max_level):
    """Falha alto se alguma curva deixar de ser monotônica ou estourar u32."""
    for rate in GROWTH_RATES:
        prev = 0
        for n in range(2, max_level + 1):
            v = exp_at(rate, n)
            assert v > prev, f"{rate}: nível {n} não cresce ({v} <= {prev})"
            assert v <= 0xFFFFFFFF, f"{rate}: nível {n} estoura u32 ({v})"
            prev = v


def generate(max_level):
    check(max_level)
    out = [HEADER]
    for rate in GROWTH_RATES:
        out.append(f"    {{ // {NAMES[rate]}\n        0, // 0\n        1, // 1\n")
        for n in range(2, max_level + 1):
            out.append(f"        EXP_{rate}({n}),\n")
        out.append("    },\n")
    out.append("};\n")
    return "".join(out)


if __name__ == "__main__":
    max_level = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    assert 100 <= max_level <= 255, "acima de 255 o nivel nao cabe no u8 que 90 assinaturas do codigo usam"
    with open("src/data/pokemon/experience_tables.h", "w") as f:
        f.write(generate(max_level))
    print(f"experience_tables.h regerado para MAX_LEVEL {max_level}")
