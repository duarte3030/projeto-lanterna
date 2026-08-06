#!/usr/bin/env python3
"""Diz quais flags estao REALMENTE livres, e reserva faixa para um agente.

Uso:
    python3 dev_scripts/flags_livres.py               # lista as faixas livres
    python3 dev_scripts/flags_livres.py --reserva 16  # sugere uma faixa de 16

Existe porque eu distribui cinco faixas de flag para cinco agentes em
05/08/2026 e **as cinco estavam ocupadas**. Olhei `grep -c FLAG_UNUSED`, vi 460,
e cravei 0x020-0x02F, 0x030-0x03F e por aí. Um agente foi usar e descobriu que
0x030-0x037 eram as insignias de Johto, 0x038-0x03C a Galactica e 0x03D-0x03F os
Rockets: a faixa inteira em uso.

O erro e simples e nao aparece no grep. Em flags.h uma flag ocupada continua
existindo como `FLAG_UNUSED_0x030`; o que muda e que ALGUEM apelida ela:

    #define FLAG_BADGE_JOHTO_ZEPHYR   FLAG_UNUSED_0x030

Contar `FLAG_UNUSED` conta o pool inteiro, ocupadas junto. O que vale e contar
quantas NAO tem apelido apontando para elas.

Mesma familia de erro do resto da sessao: medir uma camada mais rasa que a da
afirmacao. "A flag existe como UNUSED" nao e "a flag esta livre".
"""
import re
import sys
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAGS_H = f"{RAIZ}/include/constants/flags.h"

# Faixa que o motor limpa sozinho todo dia. Lida do proprio flags.h por
# `faixa_diaria()` no import; o par abaixo e so o valor de fabrica do
# pokeemerald, usado se a leitura falhar.
DIARIA = (0x920, 0x95F)


def faixa_diaria():
    """Le do flags.h quais FLAG_UNUSED sao definidas como DAILY_FLAGS_START + n.

    Ler em vez de cravar porque a faixa muda se alguem mexer no pool: cravar o
    par seria a mesma classe de erro que este arquivo inteiro existe para evitar.
    """
    s = open(FLAGS_H).read()
    ns = [int(n, 16) for n in re.findall(
        r"^#define\s+FLAG_UNUSED_0x([0-9A-Fa-f]+)\s+\(DAILY_FLAGS_START", s, re.M)]
    return (min(ns), max(ns)) if ns else DIARIA


def livres():
    """Devolve (lista de numeros livres, total definido, total apelidado)."""
    global DIARIA
    DIARIA = faixa_diaria()
    s = open(FLAGS_H).read()
    apelidada = set(re.findall(
        r"^#define\s+FLAG_(?!UNUSED)[A-Z0-9_]+\s+(FLAG_UNUSED_0x[0-9A-Fa-f]+)\b",
        s, re.M))
    todas = set(re.findall(r"^#define\s+(FLAG_UNUSED_0x[0-9A-Fa-f]+)\b", s, re.M))
    nums = sorted(int(n.split("0x")[1], 16) for n in todas - apelidada)
    # SEGUNDA CAMADA DE ARMADILHA, achada em 06/08/2026: existir sem apelido
    # ainda nao e servir. De FLAG_UNUSED_0x920 a 0x95F o proprio flags.h define
    # cada uma como (DAILY_FLAGS_START + n), e `ClearDailyFlags()`
    # (src/event_data.c) da memset na faixa inteira a cada virada de dia do RTC.
    # Flag de estado ali some sozinha durante a noite, sem erro, sem log, e o
    # jogador acorda com a porta destrancada. Eu ja tinha despachado
    # 0x946-0x95F para um agente antes de descobrir; ninguem chegou a gastar.
    nums = [n for n in nums if not (DIARIA[0] <= n <= DIARIA[1])]
    return nums, len(todas), len(apelidada)


def faixas(nums):
    """Agrupa numeros consecutivos em (inicio, fim)."""
    out = []
    ini = ant = None
    for v in nums:
        if ini is None:
            ini = ant = v
        elif v == ant + 1:
            ant = v
        else:
            out.append((ini, ant))
            ini = ant = v
    if ini is not None:
        out.append((ini, ant))
    return out


def main():
    nums, total, ocupadas = livres()
    fs = faixas(nums)
    print(f"FLAG_UNUSED definidas: {total}")
    print(f"  ja apelidadas por outra flag (OCUPADAS): {ocupadas}")
    print(f"  realmente livres: {len(nums)}")

    if "--reserva" in sys.argv:
        n = int(sys.argv[sys.argv.index("--reserva") + 1])
        cabe = [f for f in fs if f[1] - f[0] + 1 >= n]
        if not cabe:
            print(f"\nNAO HA faixa contigua de {n} flags livres.")
            return 1
        # a menor que serve, para nao picotar a maior a toa
        a, b = min(cabe, key=lambda f: f[1] - f[0])
        print(f"\nreserve 0x{a:03X} a 0x{a+n-1:03X} ({n} flags), "
              f"de uma faixa de {b-a+1}")
        return 0

    print("\nfaixas contiguas livres, da maior para a menor:")
    for a, b in sorted(fs, key=lambda f: -(f[1] - f[0]))[:10]:
        print(f"  0x{a:03X} a 0x{b:03X}   {b-a+1:3d} flags")
    return 0


def demo():
    """A regra que importa: apelidada nao e livre."""
    import tempfile
    txt = (
        "#define FLAG_UNUSED_0x030   (0x030)\n"
        "#define FLAG_UNUSED_0x031   (0x031)\n"
        "#define FLAG_UNUSED_0x032   (0x032)\n"
        "#define FLAG_BADGE_JOHTO_ZEPHYR   FLAG_UNUSED_0x030\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".h", delete=False) as f:
        f.write(txt)
        caminho = f.name
    global FLAGS_H
    guardado, FLAGS_H = FLAGS_H, caminho
    try:
        nums, total, ocup = livres()
        assert total == 3, total
        assert ocup == 1, ocup
        # 0x030 esta apelidada por FLAG_BADGE_JOHTO_ZEPHYR, entao NAO e livre
        assert nums == [0x31, 0x32], [hex(x) for x in nums]
        assert faixas(nums) == [(0x31, 0x32)]
    finally:
        FLAGS_H = guardado
        os.unlink(caminho)

    # Segunda regra: flag da faixa que o motor limpa todo dia NAO e livre,
    # mesmo sem apelido nenhum.
    txt = (
        "#define FLAG_UNUSED_0x91F   (0x91F)\n"
        "#define FLAG_UNUSED_0x920   (DAILY_FLAGS_START + 0x0)\n"
        "#define FLAG_UNUSED_0x921   (DAILY_FLAGS_START + 0x1)\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".h", delete=False) as f:
        f.write(txt)
        caminho = f.name
    guardado, FLAGS_H = FLAGS_H, caminho
    try:
        assert faixa_diaria() == (0x920, 0x921)
        nums, _, _ = livres()
        assert nums == [0x91F], [hex(x) for x in nums]
    finally:
        FLAGS_H = guardado
        os.unlink(caminho)
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
