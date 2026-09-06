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
o nacional. A traducao INTEIRA mora la (`de_para_especie`, que le
`gSpeciesNames` da ROM por ancora), e desde 07/09/2026 ela inclui o que ate a
onda 1 vivia duplicado aqui:

1. **O ponto da frente.** 27 nomes da tabela do demake comecam com o caractere
   `.` (byte 0xAD): `.Rattata`, `.Ponyta`, `.Corsola`, `.Mr. Mime` e companhia.
   O ponto e a marca que o demake poe na especie que TEM forma regional, e ele
   fica na entrada BASE. Retirado o ponto, o id baixo volta a ser a forma base,
   e a regra da PRIMEIRA ocorrencia para de apontar para a forma regional.
2. **As grafias tortas** (`Baraskewda`, `Stonjorner`, `Fletchindr`,
   `Centskorch`, `Crabminble`, `Nidoran♀/♂`, `Unown ?` e o `Farfetch’`
   truncado pelo campo de 11 bytes).
3. **O bloco de Alola** (ids 1020 a 1039) e as formas cosmeticas de gen 4 no
   `AJUSTE`, que e o que impede o Rattata de Alola de ser gravado como Rattata
   comum.

Aqui nao ha mais tabela de traducao nenhuma: um id, uma decisao, um arquivo.

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
0 nao pode ser gravado, e nivel inventado nao e dado lido. A regra e herdar a
faixa (menor minimo, maior maximo) de uma tabela IRMA, e "irma" tem tres
degraus, nesta ordem (ver `_faixa_de_vizinho`):

  1. outra tabela do MESMO mapa (11 casos);
  2. o mapa mais perto no grafo de warps e conexoes de Galar
     (`Galar_IsleOfArmor35` e `36`);
  3. o mapa da mesma familia de nome com o numero mais perto
     (`Galar_WildArea12`, que nao tem warp nem conexao nenhuma no repo).

O terceiro degrau entrou em 07/09/2026, por decisao da condutora da onda 2, e
com ele os 14 herdam e NENHUMA cai: a conta vai de 104 para 107 mapas. Antes
disso as tres de degrau 2 e 3 eram descartadas.

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

# GRAFIA TORTA E FORMA DA FONTE: a decisão mora toda em `estaticos_galar.py`
# desde 07/09/2026 (onda 2, lote H). Até a onda 1 ela morava aqui, duplicada,
# porque mexer no `GRAFIA`/`AJUSTE` de lá mudava estático já gravado em arquivo
# de outro dono; a duplicata custou o que duplicata sempre custa (o mesmo id
# traduzido de dois jeitos, dependendo de qual gerador rodasse) e saiu. Este
# apelido fica só para quem lia o nome antigo.
GRAFIA_EXTRA = EG.GRAFIA

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

    É `estaticos_galar.de_para_especie` e nada mais. O resgate do `.` da frente
    e as grafias tortas passaram para lá na onda 2, junto com o bloco de Alola
    do `AJUSTE`; conferido nesta rodada que os dois mapas são iguais id a id.
    """
    return EG.de_para_especie(rom)


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
              "slots_costurados": 0, "mapas_fora_do_repo": 0,
              "faixa_herdada_de_vizinho": []}
    bruto, orfas, faixa_por_pasta = [], [], {}
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
            if faixa:
                lo, hi = min(x for x, _ in faixa), max(y for _, y in faixa)
                for tipo, (taxa, mons) in sem_nivel.items():
                    resumo["tabelas_sem_nivel_herdadas"] += 1
                    tabelas[tipo] = (taxa, [(lo, hi, s) for _a, _b, s in mons])
            else:
                # Mapa em que TODA tabela veio sem nivel: a irma tem de vir de
                # fora, e isso so da para resolver quando as faixas de todos os
                # mapas ja estiverem medidas. Fica para a segunda passada.
                orfas.append((alvo, sem_nivel))
        if tabelas:
            bruto.append((alvo, tabelas))
            faixa_por_pasta[alvo["nome"]] = (
                min(a for _t, (_r, ms) in tabelas.items() for a, _b, _s in ms),
                max(b for _t, (_r, ms) in tabelas.items() for _a, b, _s in ms))

    # SEGUNDA PASSADA: as tabelas cujo mapa inteiro veio sem nivel.
    for alvo, sem_nivel in orfas:
        vizinho = _faixa_de_vizinho(alvo["nome"], faixa_por_pasta)
        if vizinho is None:
            resumo["tabelas_sem_nivel_descartadas"] += len(sem_nivel)
            recusa["tabela sem nivel na fonte e sem irma para herdar"] += len(sem_nivel)
            continue
        (lo, hi), de_onde, como = vizinho
        resumo["tabelas_sem_nivel_herdadas"] += len(sem_nivel)
        resumo["faixa_herdada_de_vizinho"].append(
            "%s %d-%d de %s (%s)" % (alvo["nome"], lo, hi, de_onde, como))
        bruto.append((alvo, {tipo: (taxa, [(lo, hi, s) for _a, _b, s in mons])
                             for tipo, (taxa, mons) in sem_nivel.items()}))

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


def _faixa_de_vizinho(pasta, faixa_por_pasta):
    """((menor, maior), de_qual_mapa, por_qual_regra) para um mapa sem nível.

    DECISÃO DA CONDUTORA, 07/09/2026: a tabela cujo mapa inteiro veio com nível
    0 na fonte herda a faixa da tabela IRMÃ MAIS PRÓXIMA, e "mais próxima" tem
    duas medidas, nesta ordem, porque nenhuma das duas sozinha cobre os três
    mapas que sobraram:

      1. VIZINHANÇA DE VERDADE: busca em largura no grafo de warps e conexões
         de Galar (o mesmo `estaticos_galar.grafo_de_mapas`). Empate na mesma
         distância resolve pelo nome, para a segunda rodada dar o mesmo
         resultado. É o que resolve `Galar_IsleOfArmor35` e `36`.
      2. VIZINHANÇA DE NOME: o mapa da mesma família com o número mais perto
         (`Galar_WildArea12` -> `Galar_WildArea11`), empate pelo menor número.
         Existe porque `Galar_WildArea12` não tem UM warp nem UMA conexão no
         repo: pela regra 1 ele ficaria órfão para sempre, e ele é justamente
         um dos três que a rodada foi consertar.

    Nível continua sendo dado LIDO: o que se herda é a faixa de um mapa que a
    fonte preencheu, e nunca um número escolhido a dedo.
    """
    grafo = EG.grafo_de_mapas()
    vistos, borda = {pasta}, {pasta}
    for _passo in range(8):
        nova = set()
        for m in borda:
            nova |= grafo.get(m, set()) - vistos
        if not nova:
            break
        achados = sorted(m for m in nova if m in faixa_por_pasta)
        if achados:
            return faixa_por_pasta[achados[0]], achados[0], "warp/conexão"
        vistos |= nova
        borda = nova

    m = re.match(r"^(.*?)(\d+)$", pasta)
    if m:
        familia, n = m.group(1), int(m.group(2))
        cand = []
        for outra, faixa in faixa_por_pasta.items():
            o = re.match(r"^(.*?)(\d+)$", outra)
            if o and o.group(1) == familia:
                cand.append((abs(int(o.group(2)) - n), int(o.group(2)), outra))
        if cand:
            _d, _n, outra = min(cand)
            return faixa_por_pasta[outra], outra, "família de nome"
    return None


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
          f"herdaram a faixa, "
          f"{resumo['tabelas_sem_nivel_descartadas']} descartadas")
    for linha in resumo["faixa_herdada_de_vizinho"]:
        print(f"  faixa herdada de fora do mapa: {linha}")
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
    # As grafias tortas. O id que o `AJUSTE` decide sai da conta: ele tem
    # decisao escrita e ela GANHA da grafia (o `Farfetch’d` de menor id e o
    # 1217, que e o de Galar, e nao o comum).
    nomes = _nomes_crus(rom)
    for grafia, alvo in EG.GRAFIA.items():
        todos = [i for i, n in nomes.items()
                 if (n[1:] if n.startswith(".") else n) == grafia]
        assert todos, "grafia que nao existe na fonte: " + grafia
        ids = [i for i in todos if i not in EG.AJUSTE]
        # `Farfetch’d` so aparece no 1217, que e o de Galar e tem AJUSTE: nao
        # ha id livre para cobrar, e cobrar o do AJUSTE seria cobrar a decisao
        # errada. O `assert todos` acima ja garante que a chave nao envelheceu.
        if not ids:
            continue
        assert esp.get(min(ids), (None,))[0] == alvo, (grafia, esp.get(min(ids)))
    # O bloco de Alola do `AJUSTE`: o id 1020 e o Rattata DE ALOLA, e o 19,
    # que a fonte escreve `.Rattata`, continua sendo o comum.
    for idf, alvo in ((1020, "SPECIES_RATTATA_ALOLA"),
                      (1039, "SPECIES_MAROWAK_ALOLA"),
                      (712, "SPECIES_GASTRODON_EAST"),
                      (1203, "SPECIES_INDEEDEE_F")):
        assert esp.get(idf, (None,))[0] == alvo, (idf, esp.get(idf))
    entradas, _recusa, resumo = plano()
    assert len(entradas) > 90, len(entradas)
    # Os tres mapas cuja faixa vem de FORA do proprio mapa (decisao da
    # condutora, 07/09/2026). Se algum voltar a cair, a regra dos tres degraus
    # quebrou e o `--aplicar` levaria 3 mapas a menos sem avisar.
    de_para_pasta = {v["mapa"]: v["nome"]
                     for v in json.load(open(MUNDO))["de_para"].values()}
    tem = {de_para_pasta.get(e["map"]) for e in entradas}
    for pasta in ("Galar_WildArea12", "Galar_IsleOfArmor35",
                  "Galar_IsleOfArmor36"):
        assert pasta in tem, "tabela sem nivel voltou a ser descartada: " + pasta
    assert resumo["tabelas_sem_nivel_descartadas"] == 0, resumo
    assert len(resumo["faixa_herdada_de_vizinho"]) == 3, resumo
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
