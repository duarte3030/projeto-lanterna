#!/usr/bin/env python3
"""Portão obrigatório: a save gravada na ROM ANTERIOR entregue abre nesta ROM.

Uso:
    python3 dev_scripts/prova_save_entregue.py [--rom2 ROM_NOVA] [--src2 ARVORE]

Decisão do Gui de 01/10/2026: a save NÃO PODE QUEBRAR NUNCA MAIS. Ele joga e
salva entre as versões. O `guarda_save.py` prova pela FONTE (índices, tamanhos,
SAVE_LAYOUT_REVISION congelado em 3); este portão prova pelo EMULADOR, com o
T11 de `testa_critico.py`: T11.1 grava a save na ROM entregue, T11.2 a relê
nela (controle de que o .sav é lido) e T11.3 a carrega na ROM nova.

As ROMs entregues moram em `dev_scripts/roms_entregues.json`, cada uma com o
md5 e com a FONTE dela (`include/` com os headers gerados pelo build e
`sound/song_table.inc`, que é o que o testa_critico lê para resolver mapa, flag
e offset do SaveBlock1 daquela build). Toda entrega nova ENTRA nessa lista no
mesmo commit que a registra no ESTADO, e a fonte dela é guardada ao lado da ROM
em `roms/` (pasta `<nome da ROM sem .gba>.fonte`).

Reprova (código 1) se faltar ROM, md5 ou fonte de qualquer entrada, ou se o T11
não fechar 3 de 3 contra qualquer uma. Nunca pula calado.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
LISTA = os.path.join(AQUI, "roms_entregues.json")


def md5(caminho):
    h = hashlib.md5()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def main():
    args = sys.argv[1:]
    rom2 = os.path.join(RAIZ, "pokeemerald.gba")
    src2 = RAIZ
    if "--rom2" in args:
        rom2 = args[args.index("--rom2") + 1]
    if "--src2" in args:
        src2 = args[args.index("--src2") + 1]
    entregues = json.load(open(LISTA))
    if not entregues:
        print("RECUSADO: roms_entregues.json vazio; o portão não prova nada")
        return 1
    falhas = []
    for e in entregues:
        nome, rom, fonte = e["nome"], e["rom"], e["fonte"]
        if not os.path.exists(rom):
            falhas.append(f"{nome}: ROM entregue não encontrada em {rom}")
            continue
        if md5(rom) != e["md5"]:
            falhas.append(f"{nome}: md5 de {rom} não é {e['md5']}")
            continue
        if not os.path.isdir(os.path.join(fonte, "include", "constants")):
            falhas.append(f"{nome}: fonte da ROM entregue não encontrada em {fonte}")
            continue
        # O testa_critico lê o .map ao lado da ROM; a pasta de trabalho recebe
        # ROM e .map com o mesmo nome-base, sem espaço no caminho.
        mapa = os.path.splitext(rom)[0] + ".map"
        if not os.path.exists(mapa):
            falhas.append(f"{nome}: falta o .map ao lado de {rom}")
            continue
        tmp = tempfile.mkdtemp(prefix=f"t11-{nome}-")
        base = os.path.join(tmp, "entregue")
        shutil.copy(rom, base + ".gba")
        shutil.copy(mapa, base + ".map")
        env = dict(os.environ, SAV_RAIZ=os.path.join(tmp, "sav"),
                   SAIDA_TESTES=os.path.join(tmp, "png"))
        p = subprocess.run([sys.executable, os.path.join(AQUI, "testa_critico.py"), "T11",
                            "--rom", base + ".gba", "--src", fonte,
                            "--rom2", rom2, "--src2", src2],
                           capture_output=True, text=True, env=env, timeout=1800)
        saida = p.stdout + p.stderr
        ok = p.returncode == 0 and "3/3 passaram" in saida
        print(f"{nome} ({e['md5'][:8]}): T11 {'3 de 3' if ok else 'REPROVOU'}")
        if not ok:
            falhas.append(f"{nome}: T11 não fechou 3 de 3:\n" + saida[-1200:])
        shutil.rmtree(tmp, ignore_errors=True)
    if falhas:
        print("\nA SAVE DE UMA ROM ENTREGUE NÃO ABRE (ou não deu para provar):")
        for f in falhas:
            print("  " + f)
        print("A save não pode quebrar (decisão do Gui de 01/10/2026): conserte, ou "
              "obtenha a aprovação explícita dele.")
        return 1
    print(f"\nSAVE DAS {len(entregues)} ROM(S) ENTREGUE(S) ABRE NESTA ROM.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
