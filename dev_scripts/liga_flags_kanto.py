#!/usr/bin/env python3
"""Da numero de verdade as FLAG_HIDE_* de Kanto que estao valendo 0.

Kanto entrou com 530 flags stub: `#define FLAG_HIDE_ALGUMA_COISA 0`. Flag 0 nao
e uma flag: GetFlagPointer(0) devolve NULL (src/event_data.c:229), entao setflag
vira no-op e FlagGet e sempre FALSE. Efeito no jogo: Pokebola do laboratorio
volta depois de pega, fossil renasce, Rocket derrotado continua no lugar.

CRITERIO, revisado em 16/08/2026: a flag esta zerada E aparece em algum lugar de
`data/` ou `src/`. Basta ser referenciada; nao importa como.

O criterio antigo era a INTERSECAO de tres coisas (zerada + campo `flag` de um
objeto + mexida por setflag/clearflag/goto_if_set num script), e deixou 425 flags
para tras porque as duas pontas do E sao facies de furar:

- Pokebola de item nunca aparece na perna "mexida por script". O `finditem` acende
  a flag do PROPRIO objeto em tempo de execucao (asm/macros/event.inc:2157 ->
  STD_FIND_ITEM), pelo campo `flag` do template, sem citar o nome dela em lugar
  nenhum. Resultado: TM45 de Route 24 renascia a cada troca de tela, infinitas
  vezes, e o mesmo para toda item ball de Kanto.
- Flag de historia nunca aparece na perna "campo flag de um objeto".
  FLAG_GOT_SS_TICKET e FLAG_HELPED_BILL_IN_SEA_COTTAGE so vivem dentro de script,
  entao ficaram em 0: o Bill nunca registrava a cena do separador de celulas,
  nunca entregava o S.S. Ticket, e o policial de Cerulean nunca saia da frente.

Dar numero a uma flag zerada nunca esconde nada por conta propria: ela nasce
zerada do mesmo jeito, e so passa a valer quando um script a acende. O unico
custo e consumir do pool, e o pool sobra.

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


def grep(padrao, *dirs):
    """git grep e ordens de grandeza mais rapido que andar a arvore em python."""
    r = subprocess.run(["git", "grep", "-hoE", padrao, "--"] + list(dirs),
                       cwd=REPO, capture_output=True, text=True)
    return r.stdout.split("\n")


def precisam():
    fonte = open(FLAGS_H, encoding="utf-8").read()
    zeradas = set(ZERADA.findall(fonte))
    # Referencia em qualquer forma: campo `flag` de object_event, setflag num
    # script, checagem em C. Quem nao aparece em canto nenhum nao ganha numero,
    # porque flag que ninguem le nem escreve nao muda nada valendo 0 ou 0x1A37.
    citadas = {m for l in grep(r"FLAG_[A-Z0-9_]+", "data", "src")
               for m in re.findall(r"FLAG_[A-Z0-9_]+", l)}
    return sorted(zeradas & citadas), zeradas


def main():
    alvo, zeradas = precisam()
    nums, _, _ = flags_livres.livres()
    print(f"flags stub em 0: {len(zeradas)}")
    print(f"precisam de numero (citadas em data/ ou src/): {len(alvo)}")
    print(f"nunca citadas, ficam em 0: {sorted(zeradas - set(alvo))}")
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
    """A regra: zerada E citada em algum lugar. Citada de qualquer jeito serve."""
    txt = "#define FLAG_A 0\n#define FLAG_B 0\n#define FLAG_C (0x1)\n"
    assert set(ZERADA.findall(txt)) == {"FLAG_A", "FLAG_B"}
    # `#define FLAG_C (0x1)` ja tem numero: parenteses nao casam com `\s+0\s*$`.
    assert "FLAG_C" not in ZERADA.findall(txt)

    zeradas = {"FLAG_A", "FLAG_B", "FLAG_ORFA"}
    # FLAG_A so no campo `flag` de um objeto (caso da item ball: nenhum script
    # cita o nome dela, quem acende e o finditem pelo template).
    # FLAG_B so dentro de script (caso da flag de historia, tipo o S.S. Ticket).
    # As duas TEM que entrar; era exatamente aqui que o criterio velho furava.
    citadas = {"FLAG_A", "FLAG_B"}
    assert sorted(zeradas & citadas) == ["FLAG_A", "FLAG_B"]
    assert "FLAG_ORFA" not in citadas  # ninguem le nem escreve, fica em 0
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
