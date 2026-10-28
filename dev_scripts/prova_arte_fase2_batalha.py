#!/usr/bin/env python3
"""Batalha forçada de verdade com retrato novo da fase 2 (parte B de prova_arte_fase2.sh).

Copia a ROM construída (nunca a altera), troca em `gTrainers[TRAINER_UNOVA_CHAMPION_GENESIS].trainerPic` o retrato
para o pedido, e roda o caso T116.5 (duelo com o campeão Genesis) no emulador com `testa_critico.py`, que guarda
um PNG por passo do roteiro. Os offsets (offsetof, sizeof, valor da constante) vêm de um probe compilado com o
mesmo gcc, nunca de número chutado.

Uso: python3 dev_scripts/prova_arte_fase2_batalha.py ROM SAIDA CONSTANTE [CONSTANTE ...]
     (CONSTANTE sem o prefixo TRAINER_PIC_, ex.: KALOS_DIANTHA)
"""
import os
import re
import shutil
import struct
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEVKIT = os.environ.get("DEVKITARM", os.path.expanduser("~/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi"))


def probe(consts, tmp):
    os.makedirs(tmp, exist_ok=True)
    c, o = os.path.join(tmp, "p.c"), os.path.join(tmp, "p.o")
    with open(c, "w") as f:
        f.write('#include "global.h"\n#include "data.h"\n#include "constants/trainers.h"\n#include "constants/opponents.h"\n')
        f.write("const unsigned gP[] = {offsetof(struct Trainer, trainerPic), sizeof(struct Trainer), sizeof(enum TrainerPicID), TRAINER_UNOVA_CHAMPION_GENESIS,\n")
        f.write(",\n".join("TRAINER_PIC_" + k for k in consts) + "};\n")
    r = subprocess.run([DEVKIT + "/bin/arm-none-eabi-gcc", "-c", "-iquote", "include", "-Wno-trigraphs", "-DMODERN=1", "-DTESTING=0",
                        "-DEMERALD", "-std=gnu17", "-mthumb", "-mabi=apcs-gnu", "-march=armv4t", "-O0", "-o", o, c],
                       cwd=RAIZ, capture_output=True, text=True)
    if r.returncode:
        sys.exit("probe não compilou:\n" + r.stderr[-1500:])
    d = subprocess.run([DEVKIT + "/bin/arm-none-eabi-objdump", "-s", "-j", ".rodata", o], capture_output=True, text=True).stdout
    cru = bytearray()
    for linha in d.splitlines():
        m = re.match(r"^ [0-9a-f]{4} ((?:[0-9a-f]{2,8} ?){1,4})", linha)
        if m:
            cru.extend(bytes.fromhex(m.group(1).replace(" ", "")))
    return struct.unpack("<%dI" % (len(cru) // 4), bytes(cru))


def main():
    rom, saida, consts = sys.argv[1], sys.argv[2], sys.argv[3:]
    v = probe(consts, "/tmp/claude-501/prova_f2_probe")
    off_pic, tam, tam_enum, id_genesis, valores = v[0], v[1], v[2], v[3], v[4:]
    mapa = open(os.path.splitext(rom)[0] + ".map").read()
    m = re.search(r"^\s+0x([0-9a-f]+)\s+gTrainers\n", mapa, re.M)
    if not m:
        sys.exit("gTrainers não está no .map")
    base = int(m.group(1), 16) - 0x08000000
    pos = base + id_genesis * tam + off_pic
    print("gTrainers 0x%X sizeof %d offsetof(trainerPic) %d enum %d B  Genesis id %d -> offset ROM 0x%X" % (base + 0x08000000, tam, off_pic, tam_enum, id_genesis, pos))
    os.makedirs(saida, exist_ok=True)
    for k, val in zip(consts, valores):
        nome = "batalha_" + k.lower()
        rom_novo = os.path.join(saida, nome + ".gba")
        shutil.copyfile(rom, rom_novo)
        shutil.copyfile(os.path.splitext(rom)[0] + ".map", os.path.join(saida, nome + ".map"))
        with open(rom_novo, "r+b") as f:
            f.seek(pos)
            antes = int.from_bytes(f.read(tam_enum), "little")
            f.seek(pos)
            f.write(val.to_bytes(tam_enum, "little"))
        print("%s: trainerPic %d -> %d (TRAINER_PIC_%s)" % (nome, antes, val, k))
        env = dict(os.environ, TESTA_SAIDA=os.path.join(saida, nome))
        subprocess.run([sys.executable, os.path.join(RAIZ, "dev_scripts", "testa_critico.py"), "T116.5", "--rom", rom_novo],
                       cwd=RAIZ, env=env)


main()
