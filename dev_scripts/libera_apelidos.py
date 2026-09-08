#!/usr/bin/env python3
"""Devolve ao pool os apelidos de flag, var e MAPSEC de Unova e Galar.

    python3 dev_scripts/libera_apelidos.py            # tabela, nao escreve
    python3 dev_scripts/libera_apelidos.py --demo     # autoteste
    python3 dev_scripts/libera_apelidos.py --aplicar  # escreve

Por que so na quebra unica de save
----------------------------------
- Apagar apelido de FLAG/VAR nao muda numero nenhum (o apelido e so um nome para
  uma vaga `FLAG_UNUSED_0xNNN` que ja existe), mas `guarda_save.py` acusa uma
  quebra por nome apagado: a save guarda o BIT, e a vaga passa a ter outro dono.
- Apagar `MAPSEC_RESERVADO_01` a `09` ANDA indice de MAPSEC: `MAPSEC_SS_AQUA`
  desce 3 e `MAPSEC_NONE` desce 9. `regionMapSectionId` e gravado na save como
  local de captura do Pokemon, entao isso e quebra de verdade.
- Apagar a reserva de itens de Unova (467 flags) encolhe `FLAGS_COUNT` e move
  todo o `flags[]` do SaveBlock1.

A regra que separa apelido de Unova de nome que so PARECE de Unova
------------------------------------------------------------------
Nome nao serve como criterio: `FLAG_HIDE_DEX_ARTICUNO_GALAR`,
`FLAG_HIDE_DEX_ZAPDOS_GALAR` e `FLAG_HIDE_DEX_MOLTRES_GALAR` tem "GALAR" no
nome porque a FORMA do passaro e galariana, e os tres estao plantados em mapa
VIVO (AncientTomb em Hoenn, CanalaveCity em Sinnoh, RuinsOfAlph_Outside em
Johto) pela redistribuicao da Dex. Sai apelido que:

  1. tem Unova ou Galar no nome, E
  2. tem como valor exatamente um rotulo de pool (`FLAG_UNUSED_0xNNN` ou
     `VAR_UNUSED_0xNNN`), e nao uma conta de cadeia de orcamento, E
  3. nao e citado em NENHUM arquivo compilado (`src/`, `include/`, `data/`,
     `test/`, `tools/`).

As 39 `FLAG_HIDE_DEX_*` que a onda 1 guardou "porque a onda da Dex vai precisar
delas" FICAM TODAS, e isso foi medido, nao suposto: as 106 `FLAG_HIDE_DEX_*`
declaradas sao as 106 usadas por mapa vivo depois da redistribuicao da onda 2.
Nenhuma sobrou para devolver.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAGS = "include/constants/flags.h"
VARS = "include/constants/vars.h"
MAPSECS = "src/data/region_map/region_map_sections.json"
COMPILADO = ("src", "include", "data", "test", "tools", "asm")

APELIDO = re.compile(
    r"^#define\s+((?:FLAG|VAR)_\w*(?:UNOVA|GALAR)\w*)\s+((?:FLAG|VAR)_UNUSED_0x[0-9A-Fa-f]+)\s*(?://.*)?$"
)

# Reserva de flag que so existia para os itens de Unova, aberta em 05/08/2026 e
# nunca usada: 467 vagas que ninguem no cartucho 1 vai ocupar, e que so podem
# sair em dia de quebra de save.
RESERVA_VELHA = """// Reserva para os itens de Unova (334 item balls + 133 escondidos = 467).
// Reservado agora mesmo sem estar em uso, porque so ha uma janela barata.
#define FLAG_ITEMS_UNOVA_START                      (FLAG_HIDDEN_ITEMS_FRLG_START + NUM_HIDDEN_ITEMS_FRLG)
#define NUM_ITEMS_UNOVA                             0x1D3 // 467
"""
RESERVA_NOVA = """// A reserva de 467 flags para os itens de Unova, aberta em 05/08/2026, saiu em
// 08/09/2026 na quebra unica de save do cartucho 1: Unova nao volta aqui, e uma
// reserva so pode ser devolvida em dia de quebra. Sao 467 flags, 58 B de
// SaveBlock1. Quem quiser ver como ela era: git show da tag
// pre-remocao-unova-galar.
"""
RESERVA_HISTORIA_VELHA = \
    "#define FLAG_RESERVA_HISTORIA_START                 (FLAG_ITEMS_UNOVA_START + NUM_ITEMS_UNOVA)"
RESERVA_HISTORIA_NOVA = \
    "#define FLAG_RESERVA_HISTORIA_START                 (FLAG_HIDDEN_ITEMS_FRLG_START + NUM_HIDDEN_ITEMS_FRLG)"


def candidatos():
    saida = {}
    for arq in (FLAGS, VARS):
        for i, linha in enumerate(open(os.path.join(RAIZ, arq)).read().splitlines()):
            m = APELIDO.match(linha)
            if m:
                saida[m.group(1)] = (arq, i, m.group(2))
    return saida


def usados_no_compilado(nomes):
    padrao = re.compile(r"\b((?:FLAG|VAR)_\w+)\b")
    ignora = {os.path.join(RAIZ, FLAGS), os.path.join(RAIZ, VARS)}
    achados = {}
    for pasta in COMPILADO:
        raiz_pasta = os.path.join(RAIZ, pasta)
        if not os.path.isdir(raiz_pasta):
            continue
        for raiz, dirs, arquivos in os.walk(raiz_pasta):
            dirs[:] = [d for d in dirs if d not in (".git", "build", "build.nosync")]
            for arquivo in arquivos:
                caminho = os.path.join(raiz, arquivo)
                if caminho in ignora:
                    continue
                if not arquivo.endswith((".c", ".h", ".inc", ".json", ".s",
                                         ".party", ".cpp", ".txt")):
                    continue
                texto = open(caminho, errors="ignore").read()
                for nome in set(padrao.findall(texto)):
                    if nome in nomes:
                        achados.setdefault(nome, []).append(
                            os.path.relpath(caminho, RAIZ))
    return achados


def escreve_apelidos(a_sair):
    for arq in (FLAGS, VARS):
        caminho = os.path.join(RAIZ, arq)
        linhas = open(caminho).read().splitlines()
        fora = {i for nome, (a, i, _) in a_sair.items() if a == arq}
        open(caminho, "w").write(
            "\n".join(l for i, l in enumerate(linhas) if i not in fora) + "\n")


def escreve_reserva():
    caminho = os.path.join(RAIZ, FLAGS)
    texto = open(caminho).read()
    assert RESERVA_VELHA in texto, "bloco da reserva de itens de Unova mudou"
    assert RESERVA_HISTORIA_VELHA in texto, "FLAG_RESERVA_HISTORIA_START mudou"
    texto = texto.replace(RESERVA_VELHA, RESERVA_NOVA)
    texto = texto.replace(RESERVA_HISTORIA_VELHA, RESERVA_HISTORIA_NOVA)
    open(caminho, "w").write(texto)


def escreve_mapsecs():
    caminho = os.path.join(RAIZ, MAPSECS)
    dado = json.load(open(caminho))
    dado["map_sections"] = [s for s in dado["map_sections"]
                            if not s["id"].startswith("MAPSEC_RESERVADO_")]
    json.dump(dado, open(caminho, "w"), indent=2, ensure_ascii=False)
    open(caminho, "a").write("\n")


def main():
    aplicar = "--aplicar" in sys.argv
    demo = "--demo" in sys.argv

    todos = candidatos()
    usados = usados_no_compilado(set(todos))
    a_sair = {n: v for n, v in todos.items() if n not in usados}

    dado = json.load(open(os.path.join(RAIZ, MAPSECS)))
    reservados = [s["id"] for s in dado["map_sections"]
                  if s["id"].startswith("MAPSEC_RESERVADO_")]
    posicoes = {s["id"]: i for i, s in enumerate(dado["map_sections"])}

    flags = sum(1 for n, (a, _, _) in a_sair.items() if a == FLAGS)
    vars_ = sum(1 for n, (a, _, _) in a_sair.items() if a == VARS)
    print(f"apelidos com Unova ou Galar no nome: {len(todos)}")
    print(f"a apagar: {len(a_sair)} ({flags} flags, {vars_} vars)")
    print(f"a manter por uso em codigo compilado: {len(usados)}")
    for nome, onde in sorted(usados.items()):
        print(f"    {nome}: {sorted(set(onde))[:3]}")
    print(f"MAPSEC_RESERVADO_* a apagar: {len(reservados)}")
    print(f"  MAPSEC_SS_AQUA sai da posicao {posicoes.get('MAPSEC_SS_AQUA')} "
          f"e desce 3; MAPSEC_NONE desce {len(reservados)}")
    print("reserva de 467 flags de item de Unova: sai (58 B de SaveBlock1)")

    # a checagem das FLAG_HIDE_DEX, medida e nao suposta
    declaradas = set(re.findall(r"^#define\s+(FLAG_HIDE_DEX_\w+)",
                                open(os.path.join(RAIZ, FLAGS)).read(), re.M))
    usadas = set()
    for raiz, dirs, arquivos in os.walk(os.path.join(RAIZ, "data/maps")):
        for arquivo in arquivos:
            texto = open(os.path.join(raiz, arquivo), errors="ignore").read()
            usadas |= set(re.findall(r"\b(FLAG_HIDE_DEX_\w+)\b", texto))
    sobrando = sorted(declaradas - usadas)
    print(f"FLAG_HIDE_DEX_*: {len(declaradas)} declaradas, "
          f"{len(declaradas & usadas)} usadas por mapa vivo, "
          f"{len(sobrando)} sobrando para devolver")
    if sobrando:
        print(f"    {sobrando[:10]}")

    erros = []
    if len(usados) != 3:
        erros.append(f"esperava 3 apelidos vivos (as tres aves galarianas da Dex), "
                     f"achei {len(usados)}")
    if len(reservados) != 9:
        erros.append(f"esperava 9 MAPSEC_RESERVADO_*, achei {len(reservados)}")
    if erros:
        print("\nRECUSADO:")
        for erro in erros:
            print("   ", erro)
        return 1
    print("\ncontagens batem com o que a onda 1 deixou registrado.")

    if demo:
        falso = dict(todos)
        falso["FLAG_UNOVA_INVENTADA"] = (FLAGS, -1, "FLAG_UNUSED_0xFFF")
        if "FLAG_UNOVA_INVENTADA" in usados_no_compilado({"FLAG_UNOVA_INVENTADA"}):
            print("DEMO REPROVOU: nome inventado apareceu como usado")
            return 1
        vivos = usados_no_compilado({"FLAG_HIDE_DEX_ARTICUNO_GALAR"})
        if "FLAG_HIDE_DEX_ARTICUNO_GALAR" not in vivos:
            print("DEMO REPROVOU: a ave galariana viva nao foi vista em codigo compilado")
            return 1
        print("DEMO OK: a lente ve o apelido vivo e nao inventa uso para o morto")
        return 0

    if not aplicar:
        print("\n(nada foi escrito; use --aplicar)")
        return 0

    escreve_apelidos(a_sair)
    escreve_reserva()
    escreve_mapsecs()
    print("\nAPLICADO em flags.h, vars.h e region_map_sections.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
