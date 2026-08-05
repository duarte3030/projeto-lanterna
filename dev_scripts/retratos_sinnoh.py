#!/usr/bin/env python3
"""Levanta e conserta os retratos provisorios de treinador.

    python3 dev_scripts/retratos_sinnoh.py            # so mede
    python3 dev_scripts/retratos_sinnoh.py --gravar   # aplica o conserto

O QUE FOI MEDIDO (05/08/2026, contado no arquivo, nao lembrado)
--------------------------------------------------------------
Primeiro a pergunta que a tarefa fez, "quantos apontam para retrato que nao
existe nesta build": **zero**. Os 549 `TRAINER_PIC_*` citados em
`src/data/trainers.party` sao 91 constantes distintas, todas com entrada em
`gTrainerPicInfo` (`src/data/graphics/trainers.h`), e nenhuma dessas entradas
esta atras de `#if`. Retrato faltando daria erro de compilacao, e nao da.

O buraco real e outro, e maior: 2346 treinadores, **382 com retrato que nao e da
classe** (ja descontando sufixo de genero e diferenca de grafia tipo
"Pkmn Ranger" contra "Pokemon Ranger M"). Desses 382:

- **218 sao substituicao plausivel e proposital**, e ficam como estao: grunt da
  Rocket com cara de grunt da Rocket, grunt da Galactica com cara de grunt da
  Magma, rival com cara de Brendan/May/Wally, e os lideres de Johto e Unova ja
  mapeados por TEMA para um retrato de Hoenn (Bugsy -> Bug Catcher, Morty ->
  Phoebe que e fantasma, Pryce e Clair -> Glacia que e gelo, Drayden -> Drake
  que e dragao).
- **164 sao "Hiker", o padrao cego da importacao de Sinnoh**, e sao o unico caso
  absurdo. 163 deles sao de Sinnoh (o outro e TRAINER_NONE, que nao se toca):
  as oito lideres, os quatro da Elite dos Quatro, a CYNTHIA campea, 56 ace
  trainers, 36 grunts da Galactica, 18 psiquicos, 13 ciclistas, e por ai. Um
  ginasio inteiro de Sinnoh abre a batalha com cara de montanhista.

O CONSERTO, e o que ele NAO faz
-------------------------------
Nenhuma arte nova. Todo retrato usado aqui ja esta na ROM, entao o conserto
custa zero byte: e so trocar a linha `Pic:` de 163 blocos.

Classe generica vai por classe mais genero. Nome proprio vai por TEMA, que e o
mesmo criterio que Johto ja usava, e cada escolha esta anotada com o motivo.
Repetir retrato e permitido de proposito (Johto ja dava Glacia para Pryce e para
Clair): o alvo aqui e sair do absurdo, nao acertar o rosto.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(REPO, "src/data/trainers.party")
GRAVAR = "--gravar" in sys.argv

# classe + genero -> retrato. So vale para bloco que hoje esta em "Hiker".
POR_CLASSE = {
    ("Cooltrainer", "Male"): "Cooltrainer M",
    ("Cooltrainer", "Female"): "Cooltrainer F",
    ("Cooltrainer 2", "Male"): "Cooltrainer M",
    ("Cooltrainer 2", "Female"): "Cooltrainer F",
    ("Team Magma", "Male"): "Magma Grunt M",      # grunt da Galactica
    ("Team Magma", "Female"): "Magma Grunt F",
    ("Triathlete", "Male"): "Cycling Triathlete M",   # os de Sinnoh sao ciclistas
    ("Triathlete", "Female"): "Cycling Triathlete F",
    ("Psychic", "Male"): "Psychic M",
    ("Psychic", "Female"): "Psychic F",
    ("Expert", "Male"): "Expert M",               # veterano
    ("Expert", "Female"): "Expert F",
    ("Pkmn Ranger", "Male"): "Pokemon Ranger M",
    ("Pkmn Ranger", "Female"): "Pokemon Ranger F",
    ("Pkmn Breeder", "Male"): "Pokemon Breeder M",
    ("Pkmn Breeder", "Female"): "Pokemon Breeder F",
    ("School Kid", "Male"): "School Kid M",
    ("School Kid", "Female"): "School Kid F",
    ("Pokefan", "Male"): "Pokefan M",
    ("Pokefan", "Female"): "Pokefan F",
}

# Nome proprio manda mais que a classe, e mais que o campo Gender, que veio
# errado da importacao (a CYNTHIA esta como Male, o AARON como Female).
POR_NOME = {
    "TRAINER_SINNOH_LEADER_ROARK": ("Leader Roxanne", "pedra, e ela e a lider de pedra de Hoenn"),
    "TRAINER_SINNOH_LEADER_GARDENIA": ("TRAINER_PIC_LEADER_ERIKA_FRLG", "planta, mesma especialidade da Erika"),
    "TRAINER_SINNOH_LEADER_MAYLENE": ("Battle Girl", "lutadora e menina; nao ha lider de luta feminina no repo"),
    "TRAINER_SINNOH_LEADER_FANTINA": ("Elite Four Phoebe", "fantasma, a mesma troca que Johto fez para o Morty"),
    "TRAINER_SINNOH_LEADER_WAKE": ("Leader Juan", "agua, e o unico lider de agua masculino do repo"),
    "TRAINER_SINNOH_LEADER_BYRON": ("TRAINER_PIC_LEADER_BROCK_FRLG", "aco, e o mais perto e o lider de pedra masculino"),
    "TRAINER_SINNOH_LEADER_CANDICE": ("Elite Four Glacia", "gelo, e Glacia e o gelo feminino"),
    "TRAINER_SINNOH_LEADER_VOLKNER": ("TRAINER_PIC_LEADER_LT_SURGE_FRLG", "eletrico e masculino"),
    "TRAINER_SINNOH_ELITE_FOUR_AARON": ("Elite Four Sidney", "Elite dos Quatro, homem jovem"),
    "TRAINER_SINNOH_ELITE_FOUR_BERTHA": ("TRAINER_PIC_ELITE_FOUR_AGATHA_FRLG", "Elite dos Quatro, senhora idosa"),
    "TRAINER_SINNOH_ELITE_FOUR_FLINT": ("TRAINER_PIC_ELITE_FOUR_BRUNO_FRLG", "Elite dos Quatro, homem forte"),
    "TRAINER_SINNOH_ELITE_FOUR_LUCIAN": ("Elite Four Drake", "Elite dos Quatro, homem de terno"),
    "TRAINER_SINNOH_CHAMPION_CYNTHIA": ("Elite Four Glacia", "mulher loira de sobretudo, o retrato feminino de chefe mais proximo"),
}


def blocos(txt):
    """Devolve [(nome, corpo)] preservando o texto original de cada corpo."""
    partes = re.split(r"^=== (TRAINER_[A-Z0-9_]+) ===$", txt, flags=re.M)
    return partes[0], list(zip(partes[1::2], partes[2::2]))


def campo(corpo, chave):
    m = re.search(r"^%s: (.+)$" % chave, corpo, re.M)
    return m.group(1).strip() if m else ""


def main():
    txt = open(ARQ).read()
    cabeca, bs = blocos(txt)
    trocas, sem_regra = [], []
    saida = [cabeca]
    for nome, corpo in bs:
        pic, classe, genero = campo(corpo, "Pic"), campo(corpo, "Class"), campo(corpo, "Gender")
        novo = None
        if pic == "Hiker" and classe != "Hiker" and nome != "TRAINER_NONE":
            if nome in POR_NOME:
                novo = POR_NOME[nome][0]
            elif (classe, genero) in POR_CLASSE:
                novo = POR_CLASSE[(classe, genero)]
            else:
                sem_regra.append((nome, classe, genero))
        if novo:
            trocas.append((nome, classe, novo))
            corpo = re.sub(r"^Pic: Hiker$", "Pic: " + novo, corpo, count=1, flags=re.M)
        saida.append("=== %s ===" % nome)
        saida.append(corpo)

    print(f"blocos de treinador: {len(bs)}")
    print(f"com 'Pic: Hiker' e classe diferente de Hiker: {len(trocas) + len(sem_regra)}")
    print(f"  com regra: {len(trocas)}")
    print(f"  SEM regra (ficam como estao): {len(sem_regra)}")
    for n, c, g in sem_regra:
        print(f"    {n}  Class {c}  Gender {g}")
    for n, c, novo in trocas[:14]:
        print(f"  {n:46s} {c:16s} -> {novo}")
    if len(trocas) > 14:
        print(f"  ... mais {len(trocas) - 14}")

    if GRAVAR:
        open(ARQ, "w").write("".join(saida))
        print("gravado")
    else:
        print("nada gravado (use --gravar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
