#!/usr/bin/env python3
"""Gera a tabela de estádio por treinador de Galar (fundos de batalha).

Uso:
    python3 dev_scripts/fundos_galar.py          # escreve src/data/battle_environment_galar.h
    python3 dev_scripts/fundos_galar.py --demo   # confere sem escrever; sai 1 se algo cair

Por que existe
--------------
Os 13 `BATTLE_ENVIRONMENT_GALAR_*` (arte da fase 1, do Ultimate Plus) entraram
sem nada que os selecionasse. Em Galar o FUNDO passa a ser o de Galar, por dois
caminhos, os dois em `src/battle_bg.c` (`FundoDeGalar`):

1. Pelo terreno, como o motor já faz para o fundo de Hoenn: o ambiente que
   `BattleSetup_GetEnvironmentId` acha (grama, areia, água, caverna...) vira o
   de Galar mais parecido. `gBattleEnvironment` NÃO muda: Nature Power, Secret
   Power, Camouflage, a forma do Burmy e a animação de entrada continuam lendo o
   terreno de sempre. Só a arte troca.
2. Pelo treinador, para os estádios: líder de ginásio e campeão de Galar lutam
   no estádio da cor do tipo dele. Essa tabela é a que este script gera, a partir
   do `Name:` de cada treinador de Galar em `src/data/trainers.party` (inclui as
   revanches e os times `_2`).

Cor de cada estádio (decisão desta frente, 28/10/2026; o Ultimate Plus tem 5
estádios para 8 ginásios e repete o de grama):
    grama    Milo (planta)
    gelo     Melony (gelo)
    laranja  Kabu (fogo), Bea (lutador), Gordie (pedra)
    vermelho Raihan (dragão), Piers (sombrio)
    Poké Bola Nessa (água), Allister (fantasma), Opal e Bede (fada), e todo
             campeão de Galar (a final da Copa e os convidados da torre)
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = f"{RAIZ}/src/data/battle_environment_galar.h"

ESTADIO_DO_LIDER = {
    "Milo": "GRASS",
    "Melony": "ICE",
    "Kabu": "ORANGE", "Bea": "ORANGE", "Gordie": "ORANGE",
    "Raihan": "RED", "Piers": "RED",
    "Nessa": "POKEBALL", "Allister": "POKEBALL", "Opal": "POKEBALL", "Bede": "POKEBALL",
}
CLASSE_CAMPEAO = "TRAINER_CLASS_CHAMPION_FRLG"
CLASSE_LIDER = "TRAINER_CLASS_LEADER_FRLG"


def treinadores_galar():
    texto = open(f"{RAIZ}/src/data/trainers.party").read()
    for bloco in re.split(r"\n(?==== )", texto):
        m = re.match(r"=== (TRAINER_GALAR_\w+) ===", bloco)
        if not m:
            continue
        nome = re.search(r"^Name: (.*)$", bloco, re.M)
        classe = re.search(r"^Class: (\S+)", bloco, re.M)
        yield m.group(1), nome.group(1).strip() if nome else "", classe.group(1) if classe else ""


def monta():
    tabela = []
    for tid, nome, classe in treinadores_galar():
        # Só a luta de líder (classe Leader): o Bede rival, por exemplo, luta na
        # rota e fica com o fundo do terreno.
        if nome in ESTADIO_DO_LIDER and classe == CLASSE_LIDER:
            tabela.append((tid, ESTADIO_DO_LIDER[nome], nome))
        elif classe == CLASSE_CAMPEAO:
            tabela.append((tid, "POKEBALL", nome))
    return tabela


def texto_do_h(tabela):
    linhas = [
        "// GERADO por dev_scripts/fundos_galar.py. Não editar à mão.",
        "// Estádio de Galar por treinador (líder de ginásio e campeão).",
        "",
        "static const struct { u16 treinador; u8 fundo; } sEstadioGalarPorTreinador[] =",
        "{",
    ]
    for tid, est, nome in tabela:
        linhas.append(f"    {{ {tid}, BATTLE_ENVIRONMENT_GALAR_STADIUM_{est} }}, // {nome}")
    linhas += ["};", ""]
    return "\n".join(linhas)


def main():
    tabela = monta()
    for tid, est, nome in tabela:
        print(f"{tid:<40} {nome:<12} {est}")
    print(f"{len(tabela)} treinadores com estádio")
    if "--demo" in sys.argv:
        ok = True
        lideres = {n for _, _, n in tabela}
        faltam = set(ESTADIO_DO_LIDER) - lideres
        if faltam:
            print("demo: líder sem treinador no trainers.party:", sorted(faltam))
            ok = False
        usados = {e for _, e, _ in tabela}
        if usados != {"GRASS", "ICE", "ORANGE", "RED", "POKEBALL"}:
            print("demo: algum estádio ficou sem treinador:", sorted(usados))
            ok = False
        atual = open(SAIDA).read() if os.path.exists(SAIDA) else ""
        if atual != texto_do_h(tabela):
            print(f"demo: {SAIDA} velho; rode python3 dev_scripts/fundos_galar.py")
            ok = False
        print("demo:", "ok" if ok else "FALHOU")
        sys.exit(0 if ok else 1)
    with open(SAIDA, "w") as f:
        f.write(texto_do_h(tabela))


if __name__ == "__main__":
    main()
