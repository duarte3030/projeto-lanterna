#!/usr/bin/env python3
"""Prova que nenhuma suíte roda com gba_runner velho (dívida da fila de bugs 3).

Uso:
    python3 dev_scripts/testa_runner_velho.py [caminho/do/testa_critico.py]

Monta uma árvore descartável com `dev_scripts/testa_critico.py` e
`dev_scripts/gba_runner.c` (cópias das desta árvore, ou do testa_critico dado no
argumento, para medir uma versão antiga) e confere, importando o módulo como as
suítes importam:

1. binário MAIS VELHO que o .c: é recompilado (vira outro arquivo, mais novo);
2. binário que FALTA: é compilado ali, e não emprestado da pasta de ferramentas;
3. binário velho e compilador quebrado (`CC=false`): recusa, com RUNNER_RECUSA
   preenchido e RUNNER fora do binário velho;
4. binário em dia: fica como está (nada de recompilar a cada import).

Na versão de antes do conserto os casos 1, 2 e 3 reprovam: ela usava o binário
velho como estava e, sem binário, caía no da pasta de ferramentas.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))


def importa(raiz, env_extra=None):
    """Importa o testa_critico da árvore `raiz` num processo novo."""
    env = dict(os.environ)
    env.pop("GBA_RUNNER", None)
    env.update(env_extra or {})
    codigo = ("import sys, json; sys.path.insert(0, %r); import testa_critico as T; "
              "print(json.dumps({'runner': T.RUNNER, "
              "'recusa': getattr(T, 'RUNNER_RECUSA', 'SEM-ATRIBUTO')}))"
              % os.path.join(raiz, "dev_scripts"))
    p = subprocess.run([sys.executable, "-c", codigo], capture_output=True,
                       text=True, env=env, timeout=300)
    if p.returncode != 0:
        return {"erro": p.stderr[-400:]}
    import json
    return json.loads(p.stdout.strip().splitlines()[-1])


def arvore(tc):
    raiz = tempfile.mkdtemp(prefix="runner-velho-")
    os.makedirs(os.path.join(raiz, "dev_scripts"))
    shutil.copy(tc, os.path.join(raiz, "dev_scripts", "testa_critico.py"))
    shutil.copy(os.path.join(AQUI, "gba_runner.c"),
                os.path.join(raiz, "dev_scripts", "gba_runner.c"))
    return raiz


def binario_falso(caminho, idade):
    with open(caminho, "w") as f:
        f.write("#!/bin/sh\necho runner velho\n")
    os.chmod(caminho, 0o755)
    t = time.time() - idade
    os.utime(caminho, (t, t))


def main():
    tc = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "testa_critico.py")
    falhas = []

    # 1. velho
    raiz = arvore(tc)
    b = os.path.join(raiz, "dev_scripts", "gba_runner")
    binario_falso(b, 3600)
    r = importa(raiz)
    novo = os.path.exists(b) and open(b, "rb").read(4) != b"#!/b"
    if r.get("runner") != b or not novo:
        falhas.append(f"1. binário velho não foi recompilado: {r}")
    shutil.rmtree(raiz)

    # 2. falta
    raiz = arvore(tc)
    b = os.path.join(raiz, "dev_scripts", "gba_runner")
    r = importa(raiz)
    if r.get("runner") != b or not os.path.exists(b):
        falhas.append(f"2. sem binário, não compilou na árvore: {r}")
    shutil.rmtree(raiz)

    # 3. velho e compilador quebrado
    raiz = arvore(tc)
    b = os.path.join(raiz, "dev_scripts", "gba_runner")
    binario_falso(b, 3600)
    r = importa(raiz, {"CC": "false"})
    if r.get("runner") == b or not r.get("recusa") or r.get("recusa") == "SEM-ATRIBUTO":
        falhas.append(f"3. compilação falhou e o binário velho não foi recusado: {r}")
    shutil.rmtree(raiz)

    # 4. em dia
    raiz = arvore(tc)
    b = os.path.join(raiz, "dev_scripts", "gba_runner")
    binario_falso(b, -60)          # um minuto no futuro: mais novo que o .c
    antes = os.path.getmtime(b)
    r = importa(raiz)
    if r.get("runner") != b or os.path.getmtime(b) != antes:
        falhas.append(f"4. binário em dia foi trocado: {r}")
    shutil.rmtree(raiz)

    for f in falhas:
        print("FALHA", f)
    print(f"{4 - len(falhas)}/4 passaram")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
