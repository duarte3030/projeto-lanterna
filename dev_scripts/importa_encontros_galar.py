#!/usr/bin/env python3
"""ENCONTROS SELVAGENS DE GALAR, lidos da ROM do demake e escritos no repo.

    python3 dev_scripts/importa_encontros_galar.py            # so mede e relata
    python3 dev_scripts/importa_encontros_galar.py --aplicar   # escreve o JSON
    python3 dev_scripts/importa_encontros_galar.py --valida    # so a regua
    python3 dev_scripts/importa_encontros_galar.py --demo      # autoteste

## Por que este arquivo existe

Ate 06/09/2026 Galar tinha ZERO tabela de encontro selvagem no repo:
`src/data/wild_encounters.json` tem 679 entradas e nenhuma aponta para mapa
`Galar_*`, enquanto Sinnoh tem 117 e Unova 87. Sem tabela, nenhuma especie
consegue Galar como fonte, e por isso o `censo_dex.py` imprime "Galar 0".

A fonte usada aqui NAO e o datamine de `preparados/wild_encounters_galar.json`
(13 areas, rotas 1 a 10 mais Slumbering Weald, slots preenchidos por
maior-resto sobre taxa do Serebii, com `MAP_GALAR_*` de mentira). A fonte e a
PROPRIA ROM do demake, que traz 107 mapas de Galar com tabela de verdade,
incluindo Wild Area, Galar Mine, Glimwood Tangle e as cavernas. O datamine
continua servindo de conferencia cruzada, nao de fonte.

## Como a tabela e achada, e por que nao ha offset digitado

`gWildMonHeaders` do FireRed e um vetor de registros de 20 bytes
(`u8 grupo; u8 mapa; u16 padding; 4 ponteiros`) terminado por `0xFF`. A
varredura aqui aceita UMA base so quando ela tem mais de 100 registros
seguidos bem formados, termina em `0xFF`, e mais de 100 desses registros caem
num mapa de Galar do `de_para` do `galar_mundo.json`. As duas outras corridas
longas da ROM (0x45B9F0 e 0x45BB68) nao passam nessa terceira conferencia.

Contagem de slot: 12 grama, 5 agua, 5 rock smash, 10 pesca. E exatamente o
formato do `src/data/wild_encounters.json` deste repo (`fields`), o que e
esperado, porque os dois descendem do mesmo FireRed. O `checa_schema` reprova
se o `fields` mudar, porque slot a menos faz o motor sortear fora do vetor.

## Especie: por NOME, nunca por id

Mesmo motivo escrito em `estaticos_galar.py`: o id do demake nao e o nosso nem
o nacional. A traducao reusa `estaticos_galar.de_para_especie`, que le
`gSpeciesNames` da ROM por ancora, e acrescenta duas coisas medidas AQUI:

1. **O ponto da frente.** 12 nomes da tabela do demake comecam com o caractere
   `.` (byte 0xAD): `.Rattata`, `.Vulpix`, `.Diglett`, `.Geodude`, `.Graveler`,
   `.Grimer`, `.Exeggcute`, `.Cubone`, `.Marowak`, `.Koffing`, `.Yamask`,
   `.Stunfisk` (e mais `.Meowth`, `.Slowpoke`, `.Farfetch'd`, `.Weezing`,
   `.Mr. Mime`). O ponto e a marca que o demake poe na especie que TEM forma
   regional; a forma regional em si mora nos ids 1200 e acima. O filtro de nome
   do `estaticos_galar.py` joga essas entradas fora, e com elas 30 slots de
   encontro. Aqui o ponto da frente e retirado e o nome vale, o que mantem a
   regra da PRIMEIRA ocorrencia: o id baixo continua sendo a forma base.
2. **Cinco grafias tortas da fonte**, no mesmo espirito do `GRAFIA` de
   `estaticos_galar.py`: `Baraskewda` (nosso `BARRASKEWDA`), `Stonjorner`
   (`STONJOURNER`), `Fletchindr` (`FLETCHINDER`), `Centskorch`
   (`CENTISKORCH`) e `Crabminble` (`CRABOMINABLE`). Mais `Nidoran♀` /
   `Nidoran♂`, que sem tratamento viram `SPECIES_NIDORAN` e nao existe, e
   `Unown ?`, que tem constante propria (`SPECIES_UNOWN_QUESTION`) e cujo `?`
   o filtro de nome derruba.

Estas correcoes ficam SO aqui de proposito. Mexer no `GRAFIA` do
`estaticos_galar.py` mudaria os estaticos ja gravados em
`data/scripts/galar_estaticos.inc` e nos `map.json` de Galar, que sao arquivos
de outro dono nesta onda.

## O slot que nao traduz, e por que ele nao vira buraco

Depois de tudo acima ainda sobra um punhado de slots sem especie nossa (forma
de nome repetido sem decisao medida, e id fora da tabela de nomes). Slot nao
pode virar buraco: o motor sorteia por macro `ENCOUNTER_CHANCE_*_SLOT_n` e
tabela curta faz ele ler fora do vetor. Entao o slot recusado recebe a especie
do slot VALIDO ANTERIOR da mesma tabela (ou do proximo, se o recusado for o
primeiro), com os niveis do proprio slot recusado. Isso nunca traz bicho de
fora para o mapa: a especie ja estava naquela mesma tabela.

## A tabela sem nivel

14 tabelas da fonte tem ESPECIE em todos os slots e NIVEL 0 em todos eles (o
demake nao preencheu; a de pesca do mesmo mapa costuma estar preenchida). Nivel
0 nao pode ser gravado, e nivel inventado nao e dado lido. A regra e: a tabela
sem nivel herda a faixa (menor minimo, maior maximo) das OUTRAS tabelas do
MESMO mapa na MESMA fonte; se o mapa nao tiver nenhuma tabela com nivel, ela e
descartada. Medido: 11 herdam, 3 caem (Galar_WildArea12, Galar_IsleOfArmor35 e
Galar_IsleOfArmor36, que so tinham essa tabela), e por isso a conta sai de 107
mapas para 104.

## Idempotencia

`--aplicar` apaga do `gWildMonHeaders` toda entrada cujo `map` seja mapa de
Galar e regrava a lista inteira, ordenada por id de mapa. Rodar duas vezes da
o mesmo arquivo, byte a byte.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import fala_galar as FALA                      # noqa: E402
import estaticos_galar as EG                   # noqa: E402

ALVO = os.path.join(RAIZ, "src/data/wild_encounters.json")
MUNDO = os.path.join(RAIZ, "dev_scripts/galar_mundo.json")
SPECIES_H = os.path.join(RAIZ, "include/constants/species.h")

# Ordem dos quatro ponteiros dentro do registro, e quantos slots cada um tem.
TIPOS = (("land_mons", 12), ("water_mons", 5),
         ("rock_smash_mons", 5), ("fishing_mons", 10))
SLOTS = dict(TIPOS)

# Grafia torta da fonte -> constante nossa. Medido nesta sessao, nome a nome.
GRAFIA_EXTRA = {
    "Baraskewda": "SPECIES_BARRASKEWDA",   # a fonte come um `r`
    "Stonjorner": "SPECIES_STONJOURNER",   # a fonte troca `our` por `or`
    "Fletchindr": "SPECIES_FLETCHINDER",   # a fonte come o `e`
    "Centskorch": "SPECIES_CENTISKORCH",   # a fonte come o `i`
    "Crabminble": "SPECIES_CRABOMINABLE",  # a fonte encurta o nome inteiro
    "Nidoran♀": "SPECIES_NIDORAN_F",
    "Nidoran♂": "SPECIES_NIDORAN_M",
    "Unown ?": "SPECIES_UNOWN_QUESTION",   # a forma `?` tem constante propria
}

# O teto vem do `MAX_LEVEL` do repo, nunca de 100 decorado: `curva_selvagem.py`
# ja remapeou as cinco regioes e ha slot de nivel 146 em Hoenn hoje. Cravar 100
# aqui faria a regua reprovar 5.188 slots que nao sao desta obra.
NIVEL_MIN = 1
NIVEL_MAX = int(re.search(r"#define MAX_LEVEL\s+(\d+)",
                          open(os.path.join(RAIZ, "include/constants/pokemon.h"))
                          .read()).group(1))


# ------------------------------------------------------------------ fonte ---
def _ponteiro(rom, o):
    return struct.unpack_from("<I", rom, o)[0]


def _ponteiro_ok(rom, v):
    return v == 0 or 0x08000000 <= v < 0x08000000 + len(rom)


def _registro_ok(rom, o):
    if rom[o] > 60 or rom[o + 1] > 250:
        return False
    if rom[o + 2] or rom[o + 3]:
        return False
    ps = [_ponteiro(rom, o + 4 + 4 * i) for i in range(4)]
    if not all(_ponteiro_ok(rom, p) for p in ps):
        return False
    return any(ps)


def acha_tabela(rom, de_para_fonte):
    """Offset de `gWildMonHeaders` na ROM do demake, por ANCORA.

    Aceita a base so se ela tiver mais de 100 registros seguidos, terminar em
    `0xFF` e mais de 100 deles cairem em mapa de Galar. Sem offset digitado.
    """
    n, o, melhor = len(rom), 0, None
    while o < n - 20:
        if not _registro_ok(rom, o):
            o += 4
            continue
        inicio, k = o, 0
        while o < n - 20 and _registro_ok(rom, o):
            k += 1
            o += 20
        if k < 100 or rom[inicio + 20 * k] != 0xFF:
            continue
        casam = sum(1 for i in range(k)
                    if (rom[inicio + 20 * i], rom[inicio + 20 * i + 1])
                    in de_para_fonte)
        if casam > 100 and (melhor is None or casam > melhor[1]):
            melhor = (inicio, casam, k)
    if melhor is None:
        raise SystemExit("PARE: gWildMonHeaders do demake nao foi achada pela "
                         "ancora. A ROM da fonte mudou?")
    return melhor


def _tabela_de_slots(rom, p, quantos):
    """(taxa, [(min, max, id)]) ou None se o ponteiro for nulo ou torto."""
    if not p:
        return None
    o = p - 0x08000000
    taxa = rom[o]
    q = _ponteiro(rom, o + 4)
    if not (0x08000000 <= q < 0x08000000 + len(rom)):
        return None
    b = q - 0x08000000
    return taxa, [(rom[b + 4 * i], rom[b + 4 * i + 1],
                   struct.unpack_from("<H", rom, b + 4 * i + 2)[0])
                  for i in range(quantos)]


def de_para_especie(rom):
    """{id do demake: (SPECIES_* nosso, None)} ou {id: (None, motivo)}.

    Base: `estaticos_galar.de_para_especie`. Acrescenta o resgate do ponto da
    frente e as grafias tortas descritas no docstring do modulo.
    """
    fora = dict(EG.de_para_especie(rom))
    nossos = set(re.findall(r"\bSPECIES_[A-Z0-9_]+\b", open(SPECIES_H).read()))
    nomes = EG.nomes_da_fonte(rom)

    # `nomes_da_fonte` ja jogou fora tudo que comeca com `.` e tudo que tem
    # `?`, entao o resgate tem que reler a tabela crua. A ancora e a mesma.
    crus = _nomes_crus(rom)
    limpo = re.compile(r"[A-Za-z][A-Za-z0-9 .:’\-éö♂♀]*")
    # A regra da PRIMEIRA ocorrencia continua valendo, agora sobre a uniao dos
    # nomes limpos e dos resgatados.
    todos = dict(nomes)
    resgatados = {}
    for i, n in crus.items():
        if i in todos:
            continue
        sem = n[1:] if n.startswith(".") else n
        if n in GRAFIA_EXTRA or (n.startswith(".") and limpo.fullmatch(sem)):
            todos[i] = sem if n.startswith(".") else n
            resgatados[i] = todos[i]
    primeiro = {}
    for i in sorted(todos):
        primeiro.setdefault(todos[i], i)

    for i, n in todos.items():
        if primeiro[n] != i:
            continue
        alvo = GRAFIA_EXTRA.get(n)
        if alvo is None and i in resgatados:
            alvo = EG.GRAFIA.get(n) or (
                "SPECIES_" + re.sub(r"[^A-Z0-9]+", "_", n.upper()).strip("_"))
        if alvo is None:
            continue
        fora[i] = (alvo, None) if alvo in nossos else (
            None, "%s nao existe no nosso species.h" % alvo)
    return fora


def _nomes_crus(rom):
    """{id: nome} SEM o filtro de limpeza, para enxergar o `.` da frente."""
    cm, inv = EG._inverso_do_charmap()

    def nome(base, i):
        fora = []
        for b in rom[base + i * 11:base + i * 11 + 11]:
            if b == 0xFF:
                break
            fora.append(cm.get(b, "?"))
        return "".join(fora)

    alvo = bytes(inv[c] for c in "Bulbasaur")
    for m in re.finditer(re.escape(alvo), rom):
        base = m.start() - 11
        if (nome(base, 10) == "Caterpie" and nome(base, 25) == "Pikachu"
                and nome(base, 151) == "Mew" and nome(base, 1102) == "Grookey"):
            return {i: nome(base, i) for i in range(1, 1300)}
    raise SystemExit("PARE: tabela de nomes do demake nao achada pela ancora.")


# ------------------------------------------------------------------ plano ---
def mapas_do_repo():
    """{MAP_ID} lido do proprio `data/maps/*/map.json`, sem depender do make."""
    fora = set()
    base = os.path.join(RAIZ, "data/maps")
    for pasta in os.listdir(base):
        p = os.path.join(base, pasta, "map.json")
        if os.path.exists(p):
            mid = json.load(open(p)).get("id")
            if mid:
                fora.add(mid)
    return fora


def especies_validas():
    return set(re.findall(r"\bSPECIES_[A-Z0-9_]+\b", open(SPECIES_H).read()))


def rotulo(pasta, usados):
    """`g` + nome da pasta sem separador. Mesma regra do `encontros_b7.py`."""
    base = "g" + re.sub(r"[^A-Za-z0-9]", "", pasta)
    n, saida = 1, base
    while saida in usados:
        n += 1
        saida = f"{base}{n}"
    usados.add(saida)
    return saida


def plano():
    """(entradas, recusa, resumo). `entradas` ja no formato do JSON do repo."""
    rom = open(FALA.ROM_FONTE, "rb").read()
    de_para = json.load(open(MUNDO))["de_para"]
    por_fonte = {(v["fonte_grupo"], v["fonte_indice"]): v
                 for v in de_para.values()}
    inicio, casam, quantos = acha_tabela(rom, por_fonte)
    especies = de_para_especie(rom)
    no_repo = mapas_do_repo()
    validas = especies_validas()

    recusa = collections.Counter()
    resumo = {"offset": hex(inicio), "registros": quantos,
              "registros_galar": casam, "tabelas_sem_nivel_herdadas": 0,
              "tabelas_sem_nivel_descartadas": 0,
              "slots_costurados": 0, "mapas_fora_do_repo": 0}
    bruto = []
    for i in range(quantos):
        o = inicio + 20 * i
        alvo = por_fonte.get((rom[o], rom[o + 1]))
        if alvo is None:
            continue
        if alvo["mapa"] not in no_repo:
            resumo["mapas_fora_do_repo"] += 1
            recusa["mapa da fonte nao tem map.json no repo"] += 1
            continue
        tabelas, sem_nivel = {}, {}
        for j, (tipo, quant) in enumerate(TIPOS):
            t = _tabela_de_slots(rom, _ponteiro(rom, o + 4 + 4 * j), quant)
            if t is None:
                continue
            taxa, mons = t
            if all(a == 0 and b == 0 for a, b, _s in mons):
                sem_nivel[tipo] = (taxa, mons)
                continue
            tabelas[tipo] = (taxa, mons)
        # Tabela com TODOS os niveis em 0: a especie existe, o nivel nao. Ela
        # herda a faixa das OUTRAS tabelas do mesmo mapa, na mesma fonte; se o
        # mapa nao tiver nenhuma tabela com nivel, ela cai fora, porque nivel 0
        # e Pokemon de nivel 0 e nivel inventado nao e dado lido.
        if sem_nivel:
            faixa = [(a, b) for _t, (_r, ms) in tabelas.items()
                     for a, b, _s in ms]
            for tipo, (taxa, mons) in sem_nivel.items():
                if not faixa:
                    resumo["tabelas_sem_nivel_descartadas"] += 1
                    recusa["tabela sem nivel na fonte e sem irma para herdar"] += 1
                    continue
                lo, hi = min(x for x, _ in faixa), max(y for _, y in faixa)
                resumo["tabelas_sem_nivel_herdadas"] += 1
                tabelas[tipo] = (taxa, [(lo, hi, s) for _a, _b, s in mons])
        if tabelas:
            bruto.append((alvo, tabelas))

    bruto.sort(key=lambda z: z[0]["mapa"])
    usados = set()
    entradas = []
    for alvo, tabelas in bruto:
        e = {"map": alvo["mapa"], "base_label": rotulo(alvo["nome"], usados)}
        for tipo, _quant in TIPOS:
            if tipo not in tabelas:
                continue
            taxa, mons = tabelas[tipo]
            traduzidos = []
            for a, b, s in mons:
                nome, motivo = especies.get(
                    s, (None, "id %d fora da tabela de nomes da fonte" % s))
                if nome is not None and nome not in validas:
                    nome, motivo = None, "%s nao existe no species.h" % nome
                if nome is None:
                    recusa[motivo] += 1
                lo, hi = (a, b) if a <= b else (b, a)
                lo = min(max(lo, NIVEL_MIN), NIVEL_MAX)
                hi = min(max(hi, NIVEL_MIN), NIVEL_MAX)
                traduzidos.append([lo, hi, nome])
            traduzidos = _costura(traduzidos, resumo)
            if traduzidos is None:
                recusa["tabela sem nenhuma especie traduzivel"] += 1
                continue
            e[tipo] = {"encounter_rate": taxa,
                       "mons": [{"min_level": lo, "max_level": hi,
                                 "species": sp} for lo, hi, sp in traduzidos]}
        if any(t in e for t, _q in TIPOS):
            entradas.append(e)
    return entradas, recusa, resumo


def _costura(traduzidos, resumo):
    """Slot sem especie recebe a do slot valido vizinho da MESMA tabela."""
    validos = [i for i, (_lo, _hi, sp) in enumerate(traduzidos) if sp]
    if not validos:
        return None
    for i, (lo, hi, sp) in enumerate(traduzidos):
        if sp:
            continue
        antes = [j for j in validos if j < i]
        vizinho = antes[-1] if antes else validos[0]
        traduzidos[i] = (lo, hi, traduzidos[vizinho][2])
        resumo["slots_costurados"] += 1
    return traduzidos


# ---------------------------------------------------------------- gravacao ---
def carrega():
    with open(ALVO, encoding="utf-8") as f:
        return json.load(f)


def grupo_principal(d):
    for g in d["wild_encounter_groups"]:
        if g.get("for_maps") and "fields" in g:
            return g
    raise SystemExit("wild_encounters.json sem grupo for_maps com fields")


def checa_schema(g):
    vistos = {f["type"]: len(f["encounter_rates"]) for f in g["fields"]}
    assert vistos == SLOTS, f"fields mudou: {vistos} != {SLOTS}"


def mapas_de_galar():
    return {v["mapa"] for v in json.load(open(MUNDO))["de_para"].values()}


def aplica(entradas):
    d = carrega()
    g = grupo_principal(d)
    checa_schema(g)
    galar = mapas_de_galar()
    antes = len(g["encounters"])
    g["encounters"] = [e for e in g["encounters"] if e.get("map") not in galar]
    tirados = antes - len(g["encounters"])
    g["encounters"].extend(entradas)
    with open(ALVO, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return tirados, len(g["encounters"])


# ----------------------------------------------------------------- regua ----
def valida():
    """[] se passou. Regua do PRD: zero especie invalida, zero mapa orfao."""
    falhas = []
    d = carrega()
    g = grupo_principal(d)
    checa_schema(g)
    validas = especies_validas()
    no_repo = mapas_do_repo()
    rotulos = collections.Counter()
    for e in g["encounters"]:
        rotulos[e["base_label"]] += 1
        if e.get("map") and e["map"] not in no_repo:
            falhas.append(f"{e['base_label']}: map {e['map']} nao existe")
        for tipo, quant in TIPOS:
            if tipo not in e:
                continue
            mons = e[tipo]["mons"]
            if len(mons) != quant:
                falhas.append(f"{e['base_label']}.{tipo}: {len(mons)} slots, "
                              f"o motor sorteia {quant}")
            for m in mons:
                if m["species"] not in validas:
                    falhas.append(f"{e['base_label']}.{tipo}: especie "
                                  f"{m['species']} nao existe no species.h")
                if not (NIVEL_MIN <= m["min_level"] <= m["max_level"]
                        <= NIVEL_MAX):
                    falhas.append(f"{e['base_label']}.{tipo}: nivel "
                                  f"{m['min_level']}-{m['max_level']} fora de "
                                  f"{NIVEL_MIN}-{NIVEL_MAX}")
    for r, n in rotulos.items():
        if n > 1:
            falhas.append(f"base_label repetido {n} vezes: {r}")
    return falhas


def relata(entradas, recusa, resumo):
    galar = mapas_de_galar()
    especies = collections.Counter()
    slots = 0
    por_tipo = collections.Counter()
    for e in entradas:
        for tipo, _q in TIPOS:
            if tipo in e:
                por_tipo[tipo] += 1
                for m in e[tipo]["mons"]:
                    especies[m["species"]] += 1
                    slots += 1
    print(f"gWildMonHeaders do demake em {resumo['offset']}, "
          f"{resumo['registros']} registros, "
          f"{resumo['registros_galar']} deles em mapa de Galar")
    print(f"entradas geradas: {len(entradas)} mapas Galar_* "
          f"({len(entradas) / len(galar) * 100:.1f}% dos {len(galar)})")
    print(f"tabelas por tipo: {dict(por_tipo)}")
    print(f"slots: {slots}   especies distintas: {len(especies)}")
    print(f"tabelas sem nivel na fonte: {resumo['tabelas_sem_nivel_herdadas']} "
          f"herdaram a faixa do proprio mapa, "
          f"{resumo['tabelas_sem_nivel_descartadas']} descartadas")
    print(f"slots costurados (sem traducao, herdaram o vizinho): "
          f"{resumo['slots_costurados']}")
    if recusa:
        print("motivos de recusa de slot:")
        for m, n in recusa.most_common():
            print(f"  {n:>4}  {m}")


def demo():
    rom = open(FALA.ROM_FONTE, "rb").read()
    de_para = json.load(open(MUNDO))["de_para"]
    por_fonte = {(v["fonte_grupo"], v["fonte_indice"]): v
                 for v in de_para.values()}
    inicio, casam, quantos = acha_tabela(rom, por_fonte)
    assert casam > 100, casam
    esp = de_para_especie(rom)
    # O resgate do ponto tem que devolver a forma BASE, nao a regional.
    for nome_esperado, idf in (("SPECIES_RATTATA", 19), ("SPECIES_MEOWTH", 52),
                               ("SPECIES_MR_MIME", 122),
                               ("SPECIES_YAMASK", 615)):
        assert esp.get(idf, (None,))[0] == nome_esperado, (idf, esp.get(idf))
    # As grafias tortas.
    nomes = _nomes_crus(rom)
    for grafia, alvo in GRAFIA_EXTRA.items():
        ids = [i for i, n in nomes.items() if n == grafia]
        assert ids, grafia
        assert esp.get(min(ids), (None,))[0] == alvo, (grafia, esp.get(min(ids)))
    entradas, _recusa, resumo = plano()
    assert len(entradas) > 90, len(entradas)
    validas = especies_validas()
    no_repo = mapas_do_repo()
    for e in entradas:
        assert e["map"] in no_repo, e["map"]
        for tipo, quant in TIPOS:
            if tipo in e:
                assert len(e[tipo]["mons"]) == quant, (e["base_label"], tipo)
                for m in e[tipo]["mons"]:
                    assert m["species"] in validas, m
                    assert 1 <= m["min_level"] <= m["max_level"] <= 100, m
    # Idempotencia: o plano nao depende do que ja esta gravado.
    entradas2, _r2, _s2 = plano()
    assert entradas == entradas2
    print("demo: OK")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--aplicar", action="store_true")
    a.add_argument("--valida", action="store_true")
    a.add_argument("--demo", action="store_true")
    args = a.parse_args()
    if args.demo:
        return demo()
    if args.valida:
        falhas = valida()
        for f in falhas[:40]:
            print("FALHA:", f)
        print(f"{len(falhas)} falhas" if falhas else "regua: PASSOU")
        return 1 if falhas else 0
    entradas, recusa, resumo = plano()
    relata(entradas, recusa, resumo)
    if args.aplicar:
        tirados, total = aplica(entradas)
        print(f"gravado {ALVO}: {tirados} entradas de Galar antigas removidas, "
              f"{len(entradas)} escritas, {total} entradas no grupo")
        falhas = valida()
        for f in falhas[:40]:
            print("FALHA:", f)
        print(f"{len(falhas)} falhas" if falhas else "regua: PASSOU")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
