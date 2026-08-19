#!/usr/bin/env python3
"""Reescala SÓ os treinadores do S.S. Aqua para dentro da faixa de Johto.

Uso:
    python3 dev_scripts/curva_ss_aqua.py            # só mede, censo linha a linha
    python3 dev_scripts/curva_ss_aqua.py --aplicar  # grava
    python3 dev_scripts/curva_ss_aqua.py --demo     # autotestes, inclui mutação plantada

O DEFEITO
---------
`import_ssaqua.py` cravou `ORIGEM_NIVEL = (7, 45)`, que é a faixa de origem do
RESTO de Johto no hns, medida por `importa_treinadores_johto.py`. Só que os
treinadores do navio, no hns, vivem em **53..64**: eles são conteúdo de depois
do Hall da Fama lá. Com origem (7, 45) e destino (45, 100), a reta de
`curva_de_nivel.transforma` não interpolou, **extrapolou**, e o navio saiu em
112..128. Confere na mão: 64 -> 45 + (64-7)*55/38 = 127,5 -> 128, que é
exatamente o nível do Garrett hoje.

A RÉGUA NOVA, E POR QUE ELA É ESSA
----------------------------------
A régua é a mesma função do gerador (`curva_de_nivel.transforma`), que mapeia
linearmente uma faixa de origem numa de destino preservando a FORMA (o fraco
continua sendo o fraco). Muda só o par de faixas:

- **origem**: `(53, 64)`, a faixa que estes 23 treinadores têm **no hns**,
  medida na fonte a cada execução, nunca cravada. Foi cravar essa faixa que
  criou o defeito.
- **destino**: `(ALVO["Johto"][0], ALVO["Kanto"][1])`, ou seja **45 a 50**.
  Nenhum número novo é inventado: os dois saem da tabela `ALVO` que já existe.

O nível de destino é calculado a partir do nível da FONTE, e não do nível
estragado que está no arquivo, e isso não é preciosismo. Remapear
`(112,128) -> (45,50)` por cima do estrago daria quase o mesmo resultado, mas
arredondaria duas vezes, e em 2 dos 12 níveis de origem (61 e 63) a diferença
aparece: o hns 61 daria 48 por esse caminho e 49 pelo caminho da fonte. Como
`import_ssaqua.py` (consertado junto) emite direto da fonte, os dois caminhos
divergiriam, e um re-import mexeria em níveis que já estão certos. Um deles é o
CLYDE, que é justamente o treinador que o caso T118.1 crava.

Para achar a fonte de cada `Level:` do arquivo, monto a tabela
`nível de hoje -> nível do hns` a partir dos times do hns. Ela também resolve
sozinha os Pokémon que o `gens69_treinadores.py` acrescentou depois e que não
existem na fonte (o Garrett tem 2 mons aqui e 1 no hns): eles herdaram um nível
que já está na tabela.

O destino é o piso de Johto porque a POSIÇÃO NA HISTÓRIA aqui é o piso. No hns
o navio só zarpa depois do Hall da Fama (`OlivinePort_Text_SailorBeforeHOF`,
o portão `NoCredentials`), então lá ele é o conteúdo mais forte de Johto. **Aqui
a ordem cronológica é outra**: Kanto é a primeira região, e o jogador embarca em
Vermilion depois de `FLAG_SYS_GAME_CLEAR` e do PASSE TRI (caso T4.2), rumo a
Olivine. O navio é a ENTRADA de Johto, não a saída. Quem sobe a bordo é campeão
de Kanto, com time no teto de Kanto (50), e o gerador diz em texto o que quer
disso: "quem desembarca numa região nova chega mais forte que os primeiros
treinadores dela". Então o navio é exatamente a sobreposição das duas faixas.

Custo assumido: 12 níveis de fonte (53..64) espremidos em 6 (45..50) criam
empates. A alternativa era um teto inventado por gosto; empate medido é melhor
do que número chutado.

ESCOPO
------
Só os treinadores citados por `trainerbattle*` dentro de
`data/maps/SSAqua_*/scripts.inc`. `TRAINER_JOHTO_RED` (Mt. Silver, 149) e
`TRAINER_JOHTO_GIOVANNI` (Tohjo Falls, 111..114) não estão nesses arquivos e
por isso não são tocados, mesmo estando acima do teto. O `--demo` prova isso.
"""
import argparse
import glob
import hashlib
import importlib.util
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTY = os.path.join(RAIZ, "src", "data", "trainers.party")
CAB = re.compile(r"^=== (TRAINER_[A-Z0-9_]+) ===\s*$")
NIVEL = re.compile(r"^(\s*Level:\s*)(\d+)\s*$")
BATALHA = re.compile(r"trainerbattle\w*\s+(TRAINER_[A-Z0-9_]+)")


def _curva():
    """O gerador de curva, importado como módulo. A régua é dele, não minha."""
    caminho = os.path.join(RAIZ, "dev_scripts", "curva_de_nivel.py")
    spec = importlib.util.spec_from_file_location("curva", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CURVA = _curva()
DESTINO = (CURVA.ALVO["Johto"][0], CURVA.ALVO["Kanto"][1])   # (45, 50)


def nomes_do_barco(raiz=RAIZ):
    """{TRAINER_...: mapa}. O barco é o que os scripts do barco chamam."""
    achados = {}
    for pasta in sorted(glob.glob(os.path.join(raiz, "data", "maps", "SSAqua_*"))):
        script = os.path.join(pasta, "scripts.inc")
        if not os.path.exists(script):
            continue
        with open(script) as f:
            for nome in BATALHA.findall(f.read()):
                achados[nome] = os.path.basename(pasta)
    return achados


def varre(linhas, nomes):
    """[(nome, indice_da_linha, nivel)] só dos treinadores pedidos."""
    atual, achados = None, []
    for i, linha in enumerate(linhas):
        m = CAB.match(linha)
        if m:
            atual = m.group(1)
            continue
        m = NIVEL.match(linha)
        if m and atual in nomes:
            achados.append((atual, i, int(m.group(2))))
    return achados


def niveis_do_hns(nomes, raiz=RAIZ):
    """{TRAINER_JOHTO_X: [níveis no hns]}. A fonte, lida, não lembrada."""
    spec = importlib.util.spec_from_file_location(
        "it", os.path.join(raiz, "dev_scripts", "importa_treinadores_johto.py"))
    it = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(it)
    imp = importlib.util.spec_from_file_location(
        "imp", os.path.join(raiz, "dev_scripts", "import_ssaqua.py"))
    ssaqua = importlib.util.module_from_spec(imp)
    ssaqua.__dict__["__name__"] = "imp"
    imp.loader.exec_module(ssaqua)
    times = it.times_do_hns(ssaqua.HNS)
    saida = {}
    for nome in nomes:
        t = times.get("TRAINER_" + nome[len("TRAINER_JOHTO_"):])
        if t:
            saida[nome] = [int(m["lvl"] or 5) for m in t["mons"]]
    return saida


def de_para(linhas, nomes, fonte, destino=DESTINO):
    """{nível de hoje: nível novo}, com o nível do hns no meio como régua.

    Casa por POSTO: os níveis distintos de um treinador aqui estão na mesma
    ordem dos níveis distintos dele no hns, porque o valor de hoje é uma imagem
    monótona do valor de lá. Divergência de contagem é erro dito, não palpite.
    """
    origem = (min(n for v in fonte.values() for n in v),
              max(n for v in fonte.values() for n in v))
    hoje_para_hns = {}
    por_treinador = {}
    for nome, _, nivel in varre(linhas, nomes):
        por_treinador.setdefault(nome, []).append(nivel)
    for nome, aqui in por_treinador.items():
        la = sorted(set(fonte.get(nome, [])))
        cá = sorted(set(aqui))
        if len(la) != len(cá):
            raise ValueError(
                f"{nome}: {len(cá)} níveis distintos aqui {cá} e {len(la)} no "
                f"hns {la}. Não sei qual vira qual, e chutar isso é inventar "
                "curva. Confira o acervo antes de reescalar.")
        for h, f in zip(cá, la):
            if hoje_para_hns.setdefault(h, f) != f:
                raise ValueError(
                    f"nível {h} vem de {hoje_para_hns[h]} num treinador e de "
                    f"{f} em {nome}: a tabela não é função, não dá para usar.")
    return ({h: CURVA.transforma(f, origem, destino)
             for h, f in hoje_para_hns.items()}, origem)


def recurva(linhas, nomes, fonte, destino=DESTINO):
    """Devolve (linhas_novas, censo, origem). censo = [(nome, ordem, velho, novo)].

    origem None quer dizer "já está na faixa, não mexi" (idempotência).
    Levanta ValueError se o barco estiver MISTURADO, metade convertido e metade
    não: isso não é estado válido, é mutação, e mutação é reprovada, não
    absorvida por uma régua nova tirada da média da bagunça.
    """
    achados = varre(linhas, nomes)
    if not achados:
        raise ValueError("nenhum treinador do barco achado em trainers.party")
    niveis = [n for _, _, n in achados]
    d_min, d_max = destino
    dentro = [n for n in niveis if d_min <= n <= d_max]
    if len(dentro) == len(niveis):
        return linhas, [], None
    if dentro:
        fora = sorted({n for n in niveis if not d_min <= n <= d_max})
        raise ValueError(
            f"barco MISTURADO: {len(dentro)} níveis já em {d_min}..{d_max} e "
            f"{len(niveis) - len(dentro)} fora ({fora}). Não reescalo por cima "
            "de estado meio convertido; conserte a mão suja primeiro.")

    tabela, origem = de_para(linhas, nomes, fonte, destino)
    linhas = list(linhas)
    censo, ordem = [], {}
    for nome, i, velho in achados:
        ordem[nome] = ordem.get(nome, 0) + 1
        novo = tabela[velho]
        censo.append((nome, ordem[nome], velho, novo))
        if novo != velho:
            m = NIVEL.match(linhas[i])
            linhas[i] = f"{m.group(1)}{novo}\n"
    return linhas, censo, origem


def demo():
    """Autotestes. O que decide o resultado, e a trava contra mutação."""
    # 1. O destino sai da tabela do gerador, não de gosto meu, e cabe em Johto.
    assert DESTINO == (45, 50), DESTINO
    j_min, j_max = CURVA.ALVO["Johto"]
    assert j_min <= DESTINO[0] < DESTINO[1] <= j_max

    # 2. Escopo: o barco não puxa o RED nem o GIOVANNI, que também estão acima
    #    do teto e são de OUTROS mapas. Lido dos mapas de verdade.
    barco = nomes_do_barco()
    assert barco, "nenhum mapa SSAqua_* com trainerbattle"
    assert "TRAINER_JOHTO_RED" not in barco
    assert "TRAINER_JOHTO_GIOVANNI" not in barco
    assert all(m.startswith("SSAqua_") for m in barco.values())

    # 3. A forma é preservada: o mais fraco continua o mais fraco, e o nível
    #    novo sai do nível do hns, não do nível estragado.
    falso = ["=== TRAINER_JOHTO_A ===\n", "Level: 112\n",
             "=== TRAINER_JOHTO_B ===\n", "Level: 123\n",
             "=== TRAINER_JOHTO_C ===\n", "Level: 128\n",
             "=== TRAINER_JOHTO_FORA ===\n", "Level: 149\n"]
    alvo = {"TRAINER_JOHTO_A": "m", "TRAINER_JOHTO_B": "m", "TRAINER_JOHTO_C": "m"}
    fonte = {"TRAINER_JOHTO_A": [53], "TRAINER_JOHTO_B": [61],
             "TRAINER_JOHTO_C": [64]}
    novas, censo, origem = recurva(falso, alvo, fonte)
    assert origem == (53, 64), origem
    saiu = [n for _, _, _, n in censo]
    assert saiu == sorted(saiu)
    # 123 vem do hns 61: pela fonte dá 49, e pelo atalho (112,128)->(45,50)
    # daria 48. É esta linha que trava a divergência com o import_ssaqua.py.
    assert saiu == [45, 49, 50], saiu
    assert CURVA.transforma(123, (112, 128), DESTINO) == 48
    # e o de fora do escopo não foi tocado, apesar de estar acima do teto
    assert novas[7] == "Level: 149\n", novas[7]

    # 4. Idempotência: segunda passada não muda nada.
    novas2, censo2, origem2 = recurva(novas, alvo, fonte)
    assert origem2 is None and censo2 == [] and novas2 == novas

    # 5. MUTAÇÃO PLANTADA: um único nível empurrado de volta para 128 no meio de
    #    um barco já convertido. Régua nova por cima disso achataria os bons.
    #    Tem que ser REPROVADO, não absorvido.
    mutado = list(novas)
    mutado[3] = "Level: 128\n"
    try:
        recurva(mutado, alvo, fonte)
    except ValueError as e:
        assert "MISTURADO" in str(e), e
    else:
        raise AssertionError("mutação plantada foi absorvida em silêncio")

    # 6. Sem barco nenhum é erro, não é sucesso vazio.
    try:
        recurva(["=== TRAINER_X ===\n", "Level: 9\n"], alvo, fonte)
    except ValueError as e:
        assert "nenhum treinador" in str(e), e
    else:
        raise AssertionError("arquivo sem barco passou como se estivesse pronto")

    # 7. Contagem de níveis distintos que não bate com a fonte é ERRO dito, não
    #    palpite: sem isso a tabela casaria postos errados em silêncio.
    try:
        de_para(["=== TRAINER_JOHTO_A ===\n", "Level: 112\n", "Level: 120\n"],
                {"TRAINER_JOHTO_A": "m"}, {"TRAINER_JOHTO_A": [53]})
    except ValueError as e:
        assert "níveis distintos" in str(e), e
    else:
        raise AssertionError("contagem torta passou como se fosse casável")

    print("demo: 7 travas, todas passaram")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        return demo()

    barco = nomes_do_barco()
    bruto = open(PARTY).read()
    impressao = hashlib.sha256(bruto.encode()).hexdigest()
    linhas = bruto.splitlines(keepends=True)
    try:
        fonte = niveis_do_hns(barco)
        novas, censo, origem = recurva(linhas, barco, fonte)
    except ValueError as e:
        print(f"ABORTADO: {e}")
        return 1

    mapas = sorted(set(barco.values()))
    print(f"barco: {len(barco)} treinadores em {len(mapas)} mapas ({', '.join(mapas)})")
    if origem is None:
        print(f"JÁ NA FAIXA {DESTINO[0]}..{DESTINO[1]}, nada a fazer.")
        return 0
    print(f"régua: curva_de_nivel.transforma, origem {origem} (níveis do hns) -> "
          f"destino {DESTINO} (ALVO['Johto'][0] .. ALVO['Kanto'][1])")
    fonte_de = {}
    for nome in barco:
        for h, f in zip(sorted({n for _, _, n in varre(linhas, {nome: 1})}),
                        sorted(set(fonte.get(nome, [])))):
            fonte_de[(nome, h)] = f
    print(f"\n{'treinador':30} {'mon':>3} {'hns':>4} {'velho':>6} {'novo':>5}  mapa")
    for nome, ordem, velho, novo in censo:
        print(f"{nome:30} {ordem:3d} {fonte_de[(nome, velho)]:4d} {velho:6d} "
              f"{novo:5d}  {barco[nome]}")
    trocas = sum(1 for _, _, v, n in censo if v != n)
    print(f"\n{trocas} níveis alterados de {len(censo)}")

    if not args.aplicar:
        print("(sem --aplicar: nada escrito)")
        return 0
    if hashlib.sha256(open(PARTY).read().encode()).hexdigest() != impressao:
        print("ABORTADO: trainers.party mudou embaixo de mim. Rode de novo.")
        return 1
    with open(PARTY, "w") as f:
        f.writelines(novas)
    print(f"escrito em {PARTY}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
