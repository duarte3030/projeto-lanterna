#!/usr/bin/env python3
"""B8, lado do TREINADOR: gerações 6 a 9 nos times, lendas em líder e Elite Four.

    python3 dev_scripts/gens69_treinadores.py             # só mede
    python3 dev_scripts/gens69_treinadores.py --aplicar
    python3 dev_scripts/gens69_treinadores.py --aplicar --seco   # sem escrever
    python3 dev_scripts/gens69_treinadores.py --demo      # asserts

Escreve UM arquivo: `src/data/trainers.party`. Não cria treinador, não cria id,
não mexe em `MAX_TRAINERS_COUNT`: só ACRESCENTA Pokémon a time que tem vaga.
Portanto `guarda_save.py` continua verde por construção, e é rodado no fim.

## O que entra, e onde

Medido em 12/08/2026: **nenhuma espécie de gen 6 a 9 aparecia em treinador
nenhum**, nas cinco regiões. A curva de nível já ia de 3 a 255, mas o elenco
parava na gen 5.

Duas populações, duas regras:

**1. Lenda, mítica, ultra beast e paradox de gen 6 a 9 -> líder, Elite Four e
campeão.** Decisão do Gui (12/08, pergunta 15): "míticos e lendários em líder e
E4 são permitidos e desejados". A escolha não é sorteio: cada casa recebe a
lenda que compartilha TIPO com o time que ela já tem, e o time diz o tipo dele
(o ginásio de Pedra tem time de Pedra). Empate desempata pela soma de stats
base, mais forte para a casa de nível mais alto, e cada lenda entra em uma casa
só, para que a Pokédex não dependa de derrotar o mesmo duelo duas vezes.

**2. O resto da gen 6 a 9 -> treinador comum.** Mesma fatia por força que o
`curva_selvagem.py` usa no mato (as 290 bases sem lenda ordenadas por soma de
stats, cortadas em cinco), então a espécie que aparece na grama de Sinnoh é a
mesma que aparece no time dos treinadores de Sinnoh. Coerência de graça.

## As três coisas que este script nunca faz

- **Não passa de 6.** `PARTY_SIZE` é 6; time cheio não recebe nada e é contado
  no relatório. É por isso que o campeão de Sinnoh (6 mons) fica sem lenda.
- **Não substitui Pokémon da fonte.** Só acrescenta, e um assert confere que
  toda espécie que estava num bloco continua nele.
- **Não escolhe nível.** O acrescentado entra no nível do ACE do time (o maior
  nível do bloco), que é o que mantém a curva 3-255 que o
  `curva_de_nivel.py` já aplicou. Nenhum nível existente é tocado.

## Dynamax

`B_FLAG_DYNAMAX_BATTLE` só porteira o LADO DO JOGADOR (`CanDynamax`,
`src/battle_dynamax.c`); o treinador precisa é de `shouldDynamax`, que no
formato de time vem da linha `Dynamax Level`. Então dar Dynamax a líder e Elite
Four é uma linha por ACE, e custa zero flag. A flag em si (que o jogador usa)
saiu de `FLAG_UNUSED_0x020` para `FLAG_B8_DYNAMAX_LIBERADO` porque a do upstream
colidia com `FLAG_HIDE_ARTICUNO`.
"""
import argparse
import collections
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import catalogo_especies as CAT      # noqa: E402
import curva_de_nivel as CN          # noqa: E402
import curva_selvagem as CS          # noqa: E402
import encontros_b7 as B7            # noqa: E402

ALVO = os.path.join(RAIZ, "src", "data", "trainers.party")
PARTY_SIZE = 6
# Quantos treinadores comuns cada espécie de gen 6-9 ganha, por região.
RODADAS = 2
# De quantas lendas (as mais fracas que sobraram) cada casa pode escolher.
# Larga o bastante para o casamento de tipo achar alguém, estreita o bastante
# para a força da lenda acompanhar a força da casa.
JANELA_LENDA = 15

# `Class:` de quem manda numa região. O casamento é por classe e não por lista
# de nomes de propósito: pega as revanches (`TRAINER_JUAN_5` e afins) sem que
# ninguém precise mantê-las numa lista que apodrece.
CLASSES_CHEFE = ("Leader", "Elite Four", "Champion",
                 "TRAINER_CLASS_LEADER", "TRAINER_CLASS_LEADER_FRLG",
                 "TRAINER_CLASS_ELITE_FOUR", "TRAINER_CLASS_ELITE_FOUR_FRLG",
                 "TRAINER_CLASS_CHAMPION", "TRAINER_CLASS_CHAMPION_FRLG")


# ------------------------------------------------------------------ parser

class Bloco:
    """Um `=== TRAINER_X ===` inteiro, partido em cabeçalho e mons."""

    def __init__(self, texto):
        partes = texto.split("\n\n")
        self.cabeca = partes[0]
        # Nem todo trecho separado por linha em branco é Pokémon: o arquivo tem
        # blocos de comentário C (`/* >>> treinadores de rota de Unova >>> */`)
        # pendurados no fim de um treinador. Contá-los como mon dava 7 Pokémon
        # ao campeão de Unova e um "8º" ao exemplo do cabeçalho. `cauda` guarda
        # esses trechos para que a reescrita devolva o arquivo intacto.
        self.mons, self.cauda = [], []
        for p in partes[1:]:
            if not p.strip():
                continue
            (self.cauda if p.lstrip().startswith(("/*", "*", "//"))
             else self.mons).append(p)
        self.nome = re.match(r"=== (TRAINER_[A-Z0-9_]+) ===", texto).group(1)

    @property
    def classe(self):
        m = re.search(r"^Class: (.+)$", self.cabeca, re.M)
        return m.group(1).strip() if m else ""

    @property
    def chefe(self):
        return self.classe in CLASSES_CHEFE

    def especies(self):
        """Nome de espécie de cada mon, como aparece na primeira linha dele."""
        fora = []
        for m in self.mons:
            linha = m.strip().splitlines()[0]
            # "Alfred (Abra) (M) @ Eviolite" / "Garchomp @ Sitrus Berry"
            apelido = re.search(r"\(([A-Za-z0-9_' \.\-]+)\)", linha)
            crua = apelido.group(1) if apelido else linha.split("@")[0].strip()
            fora.append(crua.strip())
        return fora

    def nivel_ace(self):
        n = [int(x) for x in re.findall(r"^Level: (\d+)$", "\n".join(self.mons), re.M)]
        return max(n) if n else 100

    def texto(self):
        return "\n\n".join([self.cabeca] + self.mons + self.cauda)


def carrega():
    txt = open(ALVO, encoding="utf-8").read()
    # O corte é o primeiro `=== TRAINER_` NO COMEÇO DE UMA LINHA. Sem a âncora
    # `^` ele cai dentro do comentário de documentação do topo do arquivo, que
    # cita `=== TRAINER_XXXX ===` como exemplo: isso fabricava um 2399º
    # treinador de 8 Pokémon, com uma linha `Dynamax Level` que era só texto.
    corte = re.search(r"^=== TRAINER_", txt, re.M).start()
    cabecalho, corpo = txt[:corte], txt[corte:]
    blocos = [Bloco(b) for b in re.split(r"^(?==== TRAINER_)", corpo, flags=re.M)
              if b.strip()]
    return cabecalho, blocos


def nome_showdown(esp):
    """SPECIES_MR_RIME -> "SPECIES_MR_RIME". O formato aceita a constante crua,
    e usar a constante é o que deixa a validação contra `species.h` ser exata."""
    return esp.nome


# ------------------------------------------------------- tipo de cada time

def tipos_do_time(bloco, cat, apelido):
    fora = collections.Counter()
    for nome in bloco.especies():
        esp = apelido.get(nome.upper().replace(" ", "_").replace("'", "")
                          .replace(".", "").replace("-", "_"))
        if esp:
            for t in esp.tipos:
                fora[t] += 1
    return fora


def tabela_de_apelido(cat):
    """{'GARCHOMP': Especie, 'SPECIES_GARCHOMP': Especie}. O arquivo de times
    usa o nome bonito ("Mr. Mime"), o catálogo usa a constante."""
    fora = {}
    for e in cat.values():
        fora[e.nome] = e
        fora[e.nome[len("SPECIES_"):]] = e
    return fora


# ----------------------------------------------------------------- escrita

def novo_mon(esp, nivel, dynamax=False):
    linhas = [f"{nome_showdown(esp)} @ None", f"Level: {nivel}"]
    if dynamax:
        linhas.append("Dynamax Level: 10")
    return "\n".join(linhas)


def marca_dynamax(mon):
    """Acrescenta `Dynamax Level: 10` logo depois do `Level:` do mon."""
    if "Dynamax Level" in mon:
        return mon, False
    linhas = mon.splitlines()
    for i, l in enumerate(linhas):
        if l.startswith("Level: "):
            linhas.insert(i + 1, "Dynamax Level: 10")
            return "\n".join(linhas), True
    return mon, False


# ------------------------------------------------------------------ ações

def aplica(seco=False):
    cat = CAT.carrega()
    validas = CAT.validas()
    apelido = tabela_de_apelido(cat)
    ids = CN.tabela_de_ids() if hasattr(CN, "tabela_de_ids") else _ids()
    cabecalho, blocos = carrega()
    antes = {b.nome: list(b.especies()) for b in blocos}

    chefes = [b for b in blocos if b.chefe]
    comuns = [b for b in blocos if not b.chefe]

    # 1. Lendas de gen 6-9 nos chefes, a mais forte na casa de nível mais alto.
    # Lenda fraca para casa fraca: as duas listas sobem juntas, e cada casa só
    # enxerga as `JANELA_LENDA` mais fracas que ainda sobraram. Sem isso o
    # Brock, que é o ginásio 1 de 40 e fecha em nível 9, podia sacar um
    # lendário de 700 de stat porque foi o que sobrou na hora dele.
    lendas = sorted((x for x in cat.values()
                     if x.gen >= 6 and x.base and x.lenda),
                    key=lambda x: (x.bst, x.nome))
    casas = sorted(chefes, key=lambda b: b.nivel_ace())
    postas, cheios, dyn = [], [], 0
    for b in casas:
        # Dynamax no ACE, sempre, mesmo quando o time está cheio.
        if b.mons:
            b.mons[-1], mudou = marca_dynamax(b.mons[-1])
            dyn += mudou
        if len(b.mons) >= PARTY_SIZE:
            cheios.append(b.nome)
            continue
        tipos = tipos_do_time(b, cat, apelido)
        # Primeiro critério: quantos Pokémon do time dividem tipo com a lenda,
        # que é o que faz o ginásio de Pedra receber lenda de Pedra. Empate vai
        # para a mais forte, e como as casas são visitadas em ordem decrescente
        # de nível, a lenda mais forte cai na casa mais alta.
        if not lendas:
            break
        janela = lendas[:JANELA_LENDA]
        melhor = max(janela, key=lambda e: (sum(tipos[t] for t in e.tipos),
                                            -e.bst, e.nome))
        nota = sum(tipos[t] for t in melhor.tipos)
        lendas.remove(melhor)
        b.mons.append(novo_mon(melhor, b.nivel_ace(), dynamax=True))
        postas.append((b.nome, b.classe, melhor.nome, nota))
        if not lendas:
            break

    # 2. O resto da gen 6-9 nos treinadores comuns, pela mesma fatia do mato.
    fatias = CS.fatias_por_forca(cat)
    porregiao = collections.defaultdict(list)
    sem_regiao = 0
    for b in comuns:
        r = CN.regiao(b.nome, ids)
        if r is None:
            sem_regiao += 1
            continue
        if len(b.mons) < PARTY_SIZE and b.mons:
            porregiao[r].append(b)
    acrescentados = []
    for r in B7.ORDEM:
        pool = porregiao[r]
        if not pool:
            continue
        k = 0
        for _ in range(RODADAS):
            for esp in fatias[r]:
                # passo maior que 1 espalha a espécie pelo mapa inteiro da
                # região em vez de amontoar tudo nos primeiros treinadores
                passo = max(1, len(pool) // max(1, len(fatias[r]) * RODADAS))
                achou = None
                for _ in range(len(pool)):
                    b = pool[k % len(pool)]
                    k += passo
                    if len(b.mons) < PARTY_SIZE and esp.nome not in b.especies():
                        achou = b
                        break
                if achou is None:
                    continue
                achou.mons.append(novo_mon(esp, achou.nivel_ace()))
                acrescentados.append((r, achou.nome, esp.nome))

    # 3. O que nunca pode ter acontecido
    for b in blocos:
        assert len(b.mons) <= PARTY_SIZE, (b.nome, len(b.mons))
        agora = b.especies()
        sumiu = [x for x in antes[b.nome] if x not in agora]
        assert not sumiu, (b.nome, sumiu)
        for nome in agora:
            if nome.startswith("SPECIES_"):
                assert nome in validas, (b.nome, nome)

    print(f"CHEFES: {len(chefes)} blocos de líder/E4/campeão")
    print(f"  lenda de gen 6-9 acrescentada: {len(postas)}")
    print(f"  Dynamax no ace: {dyn}")
    print(f"  time já cheio (6), só ganhou Dynamax: {len(cheios)}")
    print(f"  lendas de gen 6-9 que sobraram sem casa: {len(lendas)}")
    print(f"\nCOMUNS: {len(acrescentados)} Pokémon de gen 6-9 acrescentados, "
          f"{len({a[2] for a in acrescentados})} espécies distintas")
    print(f"{'região':<8} {'treinadores':>12} {'espécies':>9}")
    for r in B7.ORDEM:
        a = [x for x in acrescentados if x[0] == r]
        print(f"{r:<8} {len({x[1] for x in a}):>12} {len({x[2] for x in a}):>9}")
    if sem_regiao:
        print(f"treinador sem região reconhecida (intocado): {sem_regiao}")

    if seco:
        print("\n--seco: nada foi escrito")
        return 0
    with open(ALVO, "w", encoding="utf-8") as f:
        f.write(cabecalho + "\n\n".join(b.texto() for b in blocos))
        f.write("\n")
    print(f"\nescrito: {ALVO}")
    return 0


def _ids():
    tabela = {}
    for arq in ("opponents.h", "opponents_frlg.h"):
        caminho = os.path.join(RAIZ, "include/constants", arq)
        if not os.path.exists(caminho):
            continue
        tabela.update({n: int(v) for n, v in re.findall(
            r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)", open(caminho).read(), re.M)})
    return tabela


def mede():
    cat = CAT.carrega()
    apelido = tabela_de_apelido(cat)
    _, blocos = carrega()
    ids = _ids()
    novas = collections.defaultdict(set)
    dyn = 0
    for b in blocos:
        r = CN.regiao(b.nome, ids) or "?"
        for nome in b.especies():
            e = apelido.get(nome.upper().replace(" ", "_").replace("'", "")
                            .replace(".", "").replace("-", "_"))
            if e and e.gen >= 6:
                novas[r].add(e.nome)
        dyn += sum("Dynamax Level" in m for m in b.mons)
    print(f"blocos: {len(blocos)}, chefes: {sum(b.chefe for b in blocos)}")
    print(f"mons com Dynamax Level: {dyn}")
    print(f"{'região':<8} {'espécies gen 6-9':>17}")
    for r in B7.ORDEM:
        print(f"{r:<8} {len(novas[r]):>17}")
    if novas["?"]:
        print(f"sem região: {len(novas['?'])}")
    return 0


def demo():
    """Asserts com MUTAÇÃO no parser, que é onde um erro passa despercebido."""
    b = Bloco("=== TRAINER_X ===\nName: A\nClass: Leader\n\n"
              "Garchomp @ Sitrus Berry\nLevel: 200\n- Earthquake\n\n"
              "Alfred (Abra) (M) @ Eviolite\nLevel: 3\n")
    assert b.nome == "TRAINER_X" and b.chefe
    assert b.especies() == ["Garchomp", "Abra"], b.especies()
    assert b.nivel_ace() == 200, "o ace e o MAIOR nivel, nao o ultimo mon"
    assert len(b.mons) == 2
    # Mutação: se o parser perder o apelido, "Alfred" viraria espécie.
    assert "Alfred" not in b.especies()

    m, mudou = marca_dynamax(b.mons[0])
    assert mudou and "Dynamax Level: 10" in m
    assert m.splitlines()[1] == "Level: 200", "a linha tem que vir DEPOIS do Level"
    assert marca_dynamax(m)[1] is False, "nao pode duplicar a linha"

    # Ida e volta: o bloco tem que sair igual ao que entrou.
    t = "=== TRAINER_Y ===\nName: B\nClass: Hiker\n\nOnix @ None\nLevel: 9\n"
    assert Bloco(t).texto().rstrip("\n") == t.rstrip("\n")

    cat = CAT.carrega()
    lendas = [x for x in cat.values() if x.gen >= 6 and x.base and x.lenda]
    assert len(lendas) > 50, len(lendas)
    assert cat["SPECIES_XERNEAS_NEUTRAL"] in lendas
    assert cat["SPECIES_GRENINJA"] not in lendas

    esp = cat["SPECIES_XERNEAS_NEUTRAL"]
    novo = novo_mon(esp, 253, dynamax=True)
    assert novo.startswith("SPECIES_XERNEAS_NEUTRAL @ None")
    assert "Level: 253" in novo and "Dynamax Level: 10" in novo
    assert esp.nome in CAT.validas()
    print(f"demo OK: {len(lendas)} lendas de gen 6-9 disponiveis para chefes")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--seco", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    if a.aplicar:
        return aplica(seco=a.seco)
    return mede()


if __name__ == "__main__":
    sys.exit(main())
