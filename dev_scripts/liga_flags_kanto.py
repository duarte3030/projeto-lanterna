#!/usr/bin/env python3
"""Da numero de verdade as FLAG_HIDE_* de Kanto que estao valendo 0.

Kanto entrou com 530 flags stub: `#define FLAG_HIDE_ALGUMA_COISA 0`. Flag 0 nao
e uma flag: GetFlagPointer(0) devolve NULL (src/event_data.c:229), entao setflag
vira no-op e FlagGet e sempre FALSE. Efeito no jogo: Pokebola do laboratorio
volta depois de pega, fossil renasce, Rocket derrotado continua no lugar.

NAO precisa de numero quem so aparece no campo `flag` de um objeto e nunca e
mexida por script: sem ninguem para ligar, objeto com flag propria fica visivel
igual a hoje, e gastar flag nisso e desperdicio. O criterio aqui e a INTERSECAO:
a flag esta zerada, algum objeto a usa, E algum script faz setflag/clearflag/
goto_if_set nela. Sao 104 das 530.

Nao mexe em FLAGS_COUNT: os numeros saem do pool FLAG_UNUSED que ja cabe no
SaveBlock1, entao o guarda de save continua verde.

Uso:
    python3 dev_scripts/liga_flags_kanto.py            # so relata
    python3 dev_scripts/liga_flags_kanto.py --aplica
    python3 dev_scripts/liga_flags_kanto.py --demo
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAGS_H = f"{REPO}/include/constants/flags.h"
APLICA = "--aplica" in sys.argv

sys.path.insert(0, f"{REPO}/dev_scripts")
import flags_livres  # noqa: E402

ZERADA = re.compile(r"^#define\s+(FLAG_[A-Z0-9_]+)\s+0\s*$", re.M)
# ponytail: `[[:space:]]`, nao `\s`. git grep -E e POSIX, onde `\s` nao existe:
# o padrao casava zero linhas e o script dizia "0 flags precisam de numero",
# com o jogo inteiro quebrado do mesmo jeito.
MEXE = (r"(setflag|clearflag|goto_if_set|goto_if_unset|call_if_set"
        r"|call_if_unset)[[:space:]]+")


def grep(padrao, *dirs):
    """git grep e ordens de grandeza mais rapido que andar a arvore em python."""
    r = subprocess.run(["git", "grep", "-hoE", padrao, "--"] + list(dirs),
                       cwd=REPO, capture_output=True, text=True)
    return r.stdout.split("\n")


def precisam():
    fonte = open(FLAGS_H, encoding="utf-8").read()
    zeradas = set(ZERADA.findall(fonte))
    usadas = {m for l in grep(r"\"flag\": \"FLAG_[A-Z0-9_]+\"", "data/maps")
              for m in re.findall(r"FLAG_[A-Z0-9_]+", l)}
    mexidas = {m for l in grep(MEXE + r"FLAG_[A-Z0-9_]+", "data", "src")
               for m in re.findall(r"FLAG_[A-Z0-9_]+", l)}
    return sorted(zeradas & usadas & mexidas), zeradas


def main():
    alvo, zeradas = precisam()
    nums, _, _ = flags_livres.livres()
    print(f"flags stub em 0: {len(zeradas)}")
    print(f"precisam de numero (usadas por objeto E mexidas por script): {len(alvo)}")
    print(f"livres no pool: {len(nums)}")
    if len(alvo) > len(nums):
        print("NAO CABE. Ou corta a lista, ou cresce FLAGS_COUNT (quebra save).")
        return 1
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    fonte = open(FLAGS_H, encoding="utf-8").read()
    for nome, n in zip(alvo, nums):
        novo = f"#define {nome.ljust(50)} FLAG_UNUSED_0x{n:03X}"
        fonte, q = re.subn(rf"^#define\s+{nome}\s+0\s*$", novo, fonte, count=1,
                           flags=re.M)
        assert q == 1, nome
    open(FLAGS_H, "w", encoding="utf-8").write(fonte)
    print(f"escrito: {len(alvo)} flags saem do stub, sobram "
          f"{len(nums) - len(alvo)} livres")
    return 0


def demo():
    """A regra: zerada + usada por objeto + mexida por script. Faltando uma, fora."""
    txt = ("#define FLAG_A 0\n#define FLAG_B 0\n#define FLAG_C (0x1)\n")
    assert set(ZERADA.findall(txt)) == {"FLAG_A", "FLAG_B"}
    zer, usa, mexe = {"FLAG_A", "FLAG_B"}, {"FLAG_A", "FLAG_B"}, {"FLAG_A"}
    assert sorted(zer & usa & mexe) == ["FLAG_A"]  # B nao e mexida, fica em 0
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
