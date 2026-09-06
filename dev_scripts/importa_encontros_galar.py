#!/usr/bin/env python3
"""ENCONTROS SELVAGENS DE GALAR, lidos da ROM do demake e escritos no repo.

    python3 dev_scripts/importa_encontros_galar.py            # so mede e relata
    python3 dev_scripts/importa_encontros_galar.py --aplicar   # escreve o JSON
    python3 dev_scripts/importa_encontros_galar.py --valida    # so a regua
    python3 dev_scripts/importa_encontros_galar.py --demo      # autoteste

    python3 dev_scripts/importa_encontros_galar.py --aplicar --sem-canonico
        # o demake PURO, sem a sobreposicao canonica de Sword/Shield (AVISO)

## As tres decisoes da condutora (onda 3, lote K2, 06/09/2026)

Fechamento do lote K. As tres duvidas que o executor deixou abertas foram
decididas assim, e o codigo abaixo e a execucao literal delas:

**1. A coluna `overworld` entra.** Numa ROM de gen 3 nao existe encontro de
overworld: o que anda visivel em Sword/Shield vira mato. Para cada area, a
`land_mons` passa a ser a UNIAO das especies das colunas `grama` e `overworld`
dos brutos; a porcentagem de cada especie e a MEDIA das duas colunas (especie
ausente numa coluna conta 0 nela); os niveis sao a UNIAO das faixas (menor
minimo, maior maximo, por especie); e o mesmo maior-resto de sempre distribui
o resultado nos 12 slots. Area com uma coluna so fica como estava.

  *Resultado medido:* das seis especies que a decisao cobrava de volta, CINCO
  voltam (Cubchoo na Rota 10 fundida, Gurdurr na Rota 8, Minccino na Rota 5,
  Perrserker na Rota 7 e Snorunt no Steamdrift Way). AXEW nao volta: os 5% dele
  viram 2,5% na media e empatam com Durant e Torkoal, que vem da `grama` e
  portanto antes na ordem da fonte, para os dois ultimos slots da Rota 6. O
  `--demo` trava a conta.

  *Adaptacao medida, e nao decisao nova:* a decisao diz "cada coluna soma 100",
  e SETE das 26 colunas do Serebii NAO somam (Rota 2 grama 120, Rota 3
  overworld 115, Rota 4 overworld 93, Rota 5 grama 134 e overworld 130, Rota 8
  overworld 115, Steamdrift overworld 105; medido em 06/09/2026).
  Media crua sobre soma torta daria peso diferente a cada coluna, que e o
  contrario do que "media das duas colunas" quer dizer. Entao cada coluna e
  RENORMALIZADA para 100 antes da media, e o `--demo` reprova se alguma coluna
  sair da normalizacao com soma diferente de 100.

**2. White Hill Station entra no `Galar_Route1001`.** A Rota 10 e um mapa so no
GBA. As duas listas canonicas (Rota 10 e Rota 10 (White Hill Station)) se
fundem pela MESMA regra do item 1: uniao das especies, media das porcentagens
das duas areas, niveis por uniao, maior-resto nos 12 slots. Nao e invencao,
porque as duas listas sao as especies canonicas daquela mesma rota. Quem manda
fundir e o campo `funde_com` do de-para, e a fusao esta registrada no
`sem_sub_mapa` com o motivo.

**3. `--canonico` virou o padrao.** `--aplicar` sozinho JA aplica a
sobreposicao canonica. Quem quiser o demake puro pede `--sem-canonico`, e leva
o AVISO junto. A armadilha da onda 3 (rodar `--aplicar` sozinho e apagar a
sobreposicao em silencio) deixou de existir, e por isso a `ordem_de_rodagem`
do `distribui_dex.py` voltou a dizer so `--aplicar`.

## A sobreposicao canonica (onda 3, lote K)

Lei do Gui de 06/09/2026 (resposta 41): **os encontros canonicos de Sword e
Shield SOBREPOEM os do demake nas areas que o datamine cobre; o demake fica
onde o datamine nao chega.** O datamine cobre 13 areas (Rotas 1 a 10, com
Steamdrift Way e White Hill Station separadas por nome, mais a parte inicial do
Slumbering Weald) e vive em
`fontes-mapas/galar-swsh/preparados/wild_encounters_galar.json`, com
`MAP_GALAR_ROUTE_1` e companhia, que sao nomes de area e NAO existem no repo.

Quem casa area canonica com os `Galar_*` do repo e o de-para escrito a mao em
`dev_scripts/galar_areas_canonicas.json`, com a regra inteira no topo dele. O
resumo: casa pelo `region_map_section` do `map.json` (que o
`conserta_mapsec_galar.py` ja corrigiu, e por isso o `galar_mundo.json` nao
serve de de-para sozinho), casa por NOME quando a fonte separa sub-area por
nome (Rota 8 x Steamdrift Way), e da a cada sub-mapa so os metodos cujo
terreno ele TEM no blockdata (sem agua nao ha `water_mons`), com uma excecao
medida para dois mapas cujo tileset saiu da conversao com o comportamento da
grama zerado.

A pesca entra aqui pela primeira vez. O `converte.py` da fonte deixou o campo
`pesca` de fora de proposito, escrito na propria `obs` do arquivo ("mapear para
fishing_mons quando a conversao dos mapas existir"); a conversao existe desde a
onda 1, entao a pesca sai dos brutos pelo MESMO maior-resto, agora sobre os 10
slots de `fishing_mons` do repo. O `--demo` prova que reconstruir `water` dos
brutos com este codigo devolve o arquivo preparado slot a slot, e que
reconstruir `land` pela REGRA VELHA (so `grama`) tambem devolve, ou seja que a
conta do maior-resto aqui continua sendo a mesma do `converte.py`; o que mudou
na decisao 1 foi a ENTRADA da conta, e nao a conta.

Desde a decisao 1 a `land_mons` de todas as 13 areas nasce AQUI, dos brutos, e
nao mais do `land_mons` que o arquivo preparado traz (aquele so olhava a coluna
`grama`). A `water_mons` continua vindo pronta do preparado, porque `agua` tem
uma coluna so e a conta seria a mesma.

A frequencia (`encounter_rate`) NAO vem do datamine, que so tem porcentagem por
especie: ela vem, nesta ordem, do que o demake ja escreveu naquele mapa e
metodo, de um sub-mapa irmao da mesma area, e por ultimo do padrao.

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
FONTES = os.path.dirname(RAIZ)
CANONICAS = os.path.join(RAIZ, "dev_scripts/galar_areas_canonicas.json")
FONTE_CANONICA = os.path.join(
    FONTES, "fontes-mapas/galar-swsh/preparados/wild_encounters_galar.json")
FONTE_BRUTOS = os.path.join(
    FONTES, "fontes-mapas/galar-swsh/preparados/brutos/encontros.json")
# Padrao de frequencia, o ultimo degrau da regra 6 do de-para: land e water sao
# os do proprio arquivo preparado, e fishing e a taxa mais comum do
# `wild_encounters.json` deste repo (30, em 123 das 251 tabelas de pesca).
TAXA_PADRAO = {"land_mons": 20, "water_mons": 4, "fishing_mons": 30}
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


# ------------------------------------------------------ fonte canonica ---
def _norm_especie(nome):
    """`Galarian Zigzagoon` -> `SPECIES_ZIGZAGOON_GALAR`. E o `norm` do
    `converte.py` da fonte, copiado letra a letra: mudar a regra aqui e mudar o
    de-para de especie da fonte inteira, e o `--demo` reprova se divergir."""
    import unicodedata
    if nome.startswith("Galarian "):
        nome = nome[len("Galarian "):] + " Galar"
    t = unicodedata.normalize("NFD", nome)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("'", "").replace(".", "").replace("\u2019", "")
    t = re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_").upper()
    return "SPECIES_" + t


def _maior_resto(lista, taxas, contexto):
    """[(min, max, SPECIES)] nos slots fixos, por maior resto.

    E o `preenche_slots` do `converte.py`: cada slot vai para a especie com a
    maior sobra de taxa, e a sobra dela cai pela taxa daquele slot. Empate sai
    pela ordem da fonte, que e o que `max` faz.
    """
    if not lista:
        return None
    resto = []
    for e in lista:
        sp = _norm_especie(e["species"])
        resto.append({"sp": sp, "min": e["min_level"], "max": e["max_level"],
                      "falta": float(e.get("taxa") or 100 / len(lista)),
                      "cru": e["species"]})
    fora = []
    for taxa in taxas:
        melhor = max(resto, key=lambda r: r["falta"])
        fora.append((melhor["min"], melhor["max"], melhor["sp"]))
        melhor["falta"] -= taxa
    for r in resto:
        if r["sp"] not in especies_validas():
            raise SystemExit("PARE: %s: %s -> %s nao existe no species.h"
                             % (contexto, r["cru"], r["sp"]))
    return fora


def _taxas_do_campo():
    """{tipo: [taxa por slot]} do proprio `wild_encounters.json` do repo."""
    g = grupo_principal(carrega())
    return {f["type"]: f["encounter_rates"] for f in g["fields"]}


def _colunas_normalizadas(area, campos=("grama", "overworld")):
    """As colunas da area, cada uma renormalizada para somar 100.

    Decisao 1 da condutora. Ela diz "cada coluna soma 100", e seis colunas do
    Serebii nao somam (a transcricao arredondou); sem renormalizar, a media
    daria peso maior a coluna de soma maior, que e o contrario de "media das
    duas colunas". Coluna vazia ou ausente nao entra.
    """
    fora = []
    for campo in campos:
        lista = area.get(campo)
        if not lista:
            continue
        bruto = [float(e.get("taxa") or 0) for e in lista]
        soma = sum(bruto)
        if soma <= 0:                      # coluna sem taxa nenhuma: peso igual
            bruto = [100.0 / len(lista)] * len(lista)
            soma = 100.0
        fora.append([{"species": e["species"],
                      "taxa": t * 100.0 / soma,
                      "min_level": e["min_level"],
                      "max_level": e["max_level"]}
                     for e, t in zip(lista, bruto)])
    return fora


def _media_de_colunas(colunas):
    """A media de N distribuicoes que somam 100, e que sai somando 100 tambem.

    Uniao das especies (ordem da primeira aparicao, que e o desempate do
    maior-resto), taxa = media das N colunas contando 0 onde a especie falta, e
    nivel pela uniao das faixas (menor minimo, maior maximo). Serve tanto para
    juntar `grama` com `overworld` (decisao 1) quanto para fundir duas areas
    canonicas na mesma rota (decisao 2), porque a saida tem a forma da entrada.
    """
    if not colunas:
        return None
    if len(colunas) == 1:
        return [dict(e) for e in colunas[0]]
    ordem = []
    for coluna in colunas:
        for e in coluna:
            if e["species"] not in ordem:
                ordem.append(e["species"])
    fora = []
    for sp in ordem:
        onde = [e for coluna in colunas for e in coluna if e["species"] == sp]
        taxa = sum(sum(e["taxa"] for e in coluna if e["species"] == sp)
                   for coluna in colunas) / len(colunas)
        fora.append({"species": sp, "taxa": taxa,
                     "min_level": min(e["min_level"] for e in onde),
                     "max_level": max(e["max_level"] for e in onde)})
    return fora


def _distribuicao_de_terra(area):
    """A distribuicao de mato da area: `grama` unida com `overworld`."""
    return _media_de_colunas(_colunas_normalizadas(area))


def tabelas_canonicas():
    """{area: {tipo: [(min, max, SPECIES)]}} do datamine de Sword/Shield.

    `water_mons` sai pronta do arquivo preparado (o `converte.py` da fonte ja a
    pos em slot do expansion, e `agua` tem uma coluna so). `land_mons` nasce
    AQUI desde a decisao 1 da condutora, da UNIAO de `grama` com `overworld`
    dos brutos, porque o preparado so olhava a `grama`. `fishing_mons` tambem
    nasce aqui, do campo `pesca` dos brutos, pelo mesmo maior resto, porque a
    conversao dos mapas que aquele arquivo esperava ja existe.

    A decisao 2 entra no fim: a area que o de-para marca com `funde_com` recebe
    a `land_mons` da MEDIA da sua distribuicao com a das areas citadas.
    """
    if not os.path.exists(FONTE_CANONICA):
        raise SystemExit("PARE: a fonte canonica nao esta em " + FONTE_CANONICA)
    fora = {}
    doc = json.load(open(FONTE_CANONICA, encoding="utf-8"))
    for e in doc["wild_encounter_groups"][0]["encounters"]:
        t = {}
        if "water_mons" in e:
            t["water_mons"] = [(m["min_level"], m["max_level"], m["species"])
                               for m in e["water_mons"]["mons"]]
        fora[e["map"]] = t
    taxas = _taxas_do_campo()
    dist = {}
    for area in json.load(open(FONTE_BRUTOS, encoding="utf-8"))["areas"]:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", area["nome"]).strip("_").upper()
        chave = "MAP_GALAR_" + slug
        if chave not in fora:
            raise SystemExit("PARE: area dos brutos sem par no preparado: "
                             + chave)
        dist[chave] = _distribuicao_de_terra(area)
        pesca = _maior_resto(area.get("pesca"), taxas["fishing_mons"],
                             area["nome"] + "/pesca")
        if pesca:
            fora[chave]["fishing_mons"] = pesca
    # DECISAO 2: a rota que virou um mapa so no GBA funde as suas listas
    # canonicas antes de ir para os slots. A media e das DISTRIBUICOES, e nao
    # dos slots, senao a especie de taxa baixa some duas vezes.
    de_para = json.load(open(CANONICAS, encoding="utf-8"))
    fundidas = {}
    for area in de_para["areas"]:
        for outra in area.get("funde_com") or []:
            if outra not in dist:
                raise SystemExit("PARE: `funde_com` cita a area %s, que nao "
                                 "existe na fonte canonica" % outra)
            fundidas.setdefault(area["area"], []).append(outra)
    for alvo, outras in fundidas.items():
        if alvo not in dist:
            raise SystemExit("PARE: `funde_com` esta na area %s, que nao "
                             "existe na fonte canonica" % alvo)
        dist[alvo] = _media_de_colunas([dist[alvo]] + [dist[o] for o in outras])
    for chave, d in dist.items():
        terra = _maior_resto(d, taxas["land_mons"], chave + "/terra")
        if terra:
            fora[chave]["land_mons"] = terra
    # CORRECAO DE ESPECIE, com o motivo e as duas testemunhas escritas no
    # `correcao_de_especie` do de-para. Ela existe porque a transcricao do
    # Serebii escreve `Darumaka` sem o `Galarian` nos tres trechos de neve, e
    # aplicar a fonte crua ali PIORARIA a fidelidade: o demake ja tinha a forma
    # certa naqueles dois mapas.
    # A conta de trocas é POR CORREÇÃO, e não acumulada: com um contador só, a
    # segunda correção herdava o placar da primeira e uma linha envelhecida
    # passaria calada, que é justamente o que esta guarda existe para pegar.
    for c in de_para.get("correcao_de_especie", []):
        trocas = 0
        for area in c["onde"]:
            if area not in fora:
                raise SystemExit("PARE: correcao_de_especie cita a area %s, "
                                 "que nao existe na fonte canonica" % area)
            for tipo, mons in fora[area].items():
                for i, (lo, hi, sp) in enumerate(mons):
                    if sp == c["de"]:
                        mons[i] = (lo, hi, c["para"])
                        trocas += 1
        if not trocas:
            raise SystemExit("PARE: a correcao %s -> %s nao achou UM slot; a "
                             "fonte mudou e a correcao envelheceu."
                             % (c["de"], c["para"]))
    validas = especies_validas()
    for area, t in fora.items():
        for tipo, mons in t.items():
            for _lo, _hi, sp in mons:
                if sp not in validas:
                    raise SystemExit("PARE: %s.%s tem %s, que nao existe no "
                                     "species.h" % (area, tipo, sp))
    return fora, trocas


# --------------------------------------------------- terreno do sub-mapa ---
def _pasta_do_tileset(_c={}):
    """{gTileset_X: data/tilesets/.../x}, lido dos headers, sem nome decorado."""
    if _c:
        return _c
    tiles = {}
    pad = re.compile(r'const u32 gTilesetTiles_([A-Za-z0-9_]+)\[\] = '
                     r'INC(?:BIN|GFX)_U32\("(data/tilesets/(?:primary|secondary)'
                     r'/[a-z0-9_/]+?)/tiles')
    for rel in ("src/data/tilesets/graphics.h", "src/graphics.c"):
        caminho = os.path.join(RAIZ, rel)
        if os.path.exists(caminho):
            for rotulo_, pasta in pad.findall(open(caminho).read()):
                tiles[rotulo_] = pasta
    cab = open(os.path.join(RAIZ, "src/data/tilesets/headers.h")).read()
    for m in re.finditer(r"const struct Tileset (gTileset_\w+)\s*=\s*\{(.*?)\n\};",
                         cab, re.S):
        mm = re.search(r"gTilesetTiles_(\w+)", m.group(2))
        if mm and mm.group(1) in tiles:
            _c[m.group(1)] = tiles[mm.group(1)]
    return _c


def _atributos(label, _c={}):
    """[comportamento por metatile]. Formato FRLG: 4 bytes, bits 0-8."""
    if label not in _c:
        pasta = _pasta_do_tileset().get(label)
        caminho = (os.path.join(RAIZ, pasta, "metatile_attributes.bin")
                   if pasta else None)
        if not caminho or not os.path.exists(caminho):
            _c[label] = []
        else:
            b = open(caminho, "rb").read()
            _c[label] = [v & 0x1FF for v in
                         struct.unpack("<%dI" % (len(b) // 4), b)]
    return _c[label]


def _flags_de_comportamento(_c={}):
    """({comportamento: bits}, {comportamentos pescaveis}) lidos do motor.

    Nada decorado: os bits saem do `sTileBitAttributes` de
    `src/metatile_behavior.c` e a lista de agua pescavel sai do
    `MetatileBehavior_IsSurfableFishableWater` do mesmo arquivo.
    """
    if _c:
        return _c["bits"], _c["pesca"]
    cab = open(os.path.join(RAIZ,
                            "include/constants/metatile_behaviors.h")).read()
    corpo = re.search(r"enum \{(.*?)\n\};", cab, re.S).group(1)
    valor = {n: i for i, n in
             enumerate(re.findall(r"^\s*(MB_[A-Z0-9_]+),", corpo, re.M))}
    src = open(os.path.join(RAIZ, "src/metatile_behavior.c")).read()
    tab = re.search(r"sTileBitAttributes\[NUM_METATILE_BEHAVIORS\] =\s*\{"
                    r"(.*?)\n\};", src, re.S).group(1)
    bits = {}
    for nome, flags in re.findall(r"\[(MB_[A-Z0-9_]+)\]\s*=\s*([^,]+),", tab):
        v = 0
        for f in flags.split("|"):
            f = f.strip()
            if f == "TILE_FLAG_HAS_ENCOUNTERS":
                v |= 1
            elif f == "TILE_FLAG_SURFABLE":
                v |= 2
        bits[valor[nome]] = v
    corpo_f = re.search(r"MetatileBehavior_IsSurfableFishableWater\(u8[^)]*\)"
                        r"\s*\{(.*?)\n\}", src, re.S).group(1)
    pesca = {valor[n] for n in re.findall(r"(MB_[A-Z0-9_]+)", corpo_f)
             if n in valor}
    _c["bits"], _c["pesca"] = bits, pesca
    return bits, pesca


def terreno_do_mapa(pasta, _c={}):
    """{'terra': n, 'agua': n, 'pescavel': n} contados no `map.bin` do layout."""
    if pasta in _c:
        return _c[pasta]
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(RAIZ, "data/layouts/layouts.json")))["layouts"]}
    d = json.load(open(os.path.join(RAIZ, "data/maps", pasta, "map.json")))
    L = layouts[d["layout"]]
    W, H = L["width"], L["height"]
    b = open(os.path.join(RAIZ, L["blockdata_filepath"]), "rb").read()
    ap, asec = (_atributos(L["primary_tileset"]),
                _atributos(L["secondary_tileset"]))
    bits, pescaveis = _flags_de_comportamento()
    fora = {"terra": 0, "agua": 0, "pescavel": 0}
    for w in struct.unpack_from("<%dH" % (W * H), b, 0):
        mt = w & 0x3FF
        # NUM_METATILES_IN_PRIMARY_FRLG, include/fieldmap.h. Todo layout de
        # Galar e `layout_version: frlg`, entao o corte e 640 e nao 512.
        t, i = (ap, mt) if mt < 640 else (asec, mt - 640)
        m = t[i] if 0 <= i < len(t) else 0
        f = bits.get(m, 0)
        if f & 1:
            fora["agua" if f & 2 else "terra"] += 1
        if m in pescaveis:
            fora["pescavel"] += 1
    _c[pasta] = fora
    return fora


# ----------------------------------------------------- sobreposicao ---------
def sobrepoe_canonico(entradas):
    """(entradas novas, resumo). Troca as tabelas do de-para pelas do datamine.

    O que NAO esta no de-para nao e tocado: mapa de Galar fora das 13 areas, e
    metodo que a area canonica nao tem (a `water_mons` que o demake deu ao
    `Galar_Route0302`, por exemplo) continuam do jeito que a ROM do demake
    escreveu. Isso e a segunda metade da lei: o demake fica onde o datamine nao
    chega.
    """
    de_para = json.load(open(CANONICAS, encoding="utf-8"))
    canon, corrigidos = tabelas_canonicas()
    por_mapa = {e["map"]: e for e in entradas}
    no_repo = mapas_do_repo()
    # A frequencia do demake, lida ANTES de qualquer troca (regra 6 do de-para).
    taxa_demake = {(e["map"], t): e[t]["encounter_rate"]
                   for e in entradas for t, _q in TIPOS if t in e}
    usados = {e["base_label"] for e in entradas}
    galar = mapas_de_galar()
    usados |= {e["base_label"] for e in grupo_principal(carrega())["encounters"]
               if e.get("map") not in galar}

    resumo = {"areas": 0, "sub_mapas": 0, "tabelas_trocadas": 0,
              "slots_corrigidos_na_fonte": corrigidos,
              "tabelas_criadas": 0, "mapas_novos": 0, "por_area": [],
              "taxa_de_irmao": [], "taxa_padrao": []}
    for area in de_para["areas"]:
        if area["area"] not in canon:
            raise SystemExit("PARE: o de-para cita a area %s, que nao existe na "
                             "fonte canonica" % area["area"])
        tem = set(canon[area["area"]])
        if set(area["metodos_na_fonte"]) != tem:
            raise SystemExit("PARE: %s: o de-para diz %s e a fonte tem %s"
                             % (area["area"], sorted(area["metodos_na_fonte"]),
                                sorted(tem)))
        resumo["areas"] += 1
        trocadas = criadas = 0
        for sub in area["sub_mapas"]:
            resumo["sub_mapas"] += 1
            if sub["mapa"] not in no_repo:
                raise SystemExit("PARE: o de-para cita %s, que nao tem map.json"
                                 % sub["mapa"])
            medido = terreno_do_mapa(sub["pasta"])
            if medido != sub["blockdata"]:
                raise SystemExit(
                    "PARE: %s: o blockdata de hoje e %s e o de-para diz %s. "
                    "Alguem mexeu no mapa ou no tileset; releia o de-para antes "
                    "de sobrepor." % (sub["pasta"], medido, sub["blockdata"]))
            if not sub["recebe"]:
                continue
            e = por_mapa.get(sub["mapa"])
            if e is None:
                e = {"map": sub["mapa"],
                     "base_label": rotulo(sub["pasta"], usados)}
                por_mapa[sub["mapa"]] = e
                entradas.append(e)
                resumo["mapas_novos"] += 1
            for tipo in sub["recebe"]:
                if tipo not in canon[area["area"]]:
                    raise SystemExit("PARE: %s pede %s e a area %s nao tem"
                                     % (sub["mapa"], tipo, area["area"]))
                if tipo in e:
                    trocadas += 1
                else:
                    criadas += 1
                taxa = taxa_demake.get((sub["mapa"], tipo))
                if taxa is None:
                    irmaos = [taxa_demake[(o["mapa"], tipo)]
                              for o in area["sub_mapas"]
                              if (o["mapa"], tipo) in taxa_demake]
                    if irmaos:
                        taxa = irmaos[0]
                        resumo["taxa_de_irmao"].append(
                            "%s.%s = %d" % (sub["mapa"], tipo, taxa))
                    else:
                        taxa = TAXA_PADRAO[tipo]
                        resumo["taxa_padrao"].append(
                            "%s.%s = %d" % (sub["mapa"], tipo, taxa))
                e[tipo] = {"encounter_rate": taxa,
                           "mons": [{"min_level": lo, "max_level": hi,
                                     "species": sp}
                                    for lo, hi, sp in canon[area["area"]][tipo]]}
        resumo["tabelas_trocadas"] += trocadas
        resumo["tabelas_criadas"] += criadas
        resumo["por_area"].append("%s: %d sub-mapa(s), %d tabela(s) trocada(s), "
                                  "%d criada(s)" % (area["area"],
                                                    len(area["sub_mapas"]),
                                                    trocadas, criadas))
    citadas = {a["area"] for a in de_para["areas"]}
    citadas |= {a["area"] for a in de_para["sem_sub_mapa"]}
    if citadas != set(canon):
        raise SystemExit("PARE: o de-para cobre %s e a fonte tem %s"
                         % (sorted(citadas), sorted(canon)))
    resumo["sem_sub_mapa"] = [a["area"] for a in de_para["sem_sub_mapa"]]
    # DECISAO 2: a area sem sub-mapa proprio que foi FUNDIDA em outra nao esta
    # sem casa; ela entrou pela `funde_com` de quem tem casa.
    resumo["fundidas"] = ["%s -> %s" % (o, a["area"])
                          for a in de_para["areas"]
                          for o in (a.get("funde_com") or [])]
    entradas.sort(key=lambda e: e["map"])
    return entradas, resumo


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


def relata_canonico(r):
    print("sobreposicao canonica: %d area(s) do datamine, %d sub-mapa(s) no "
          "de-para" % (r["areas"], r["sub_mapas"]))
    print("  tabelas trocadas: %d   criadas: %d   mapas novos: %d"
          % (r["tabelas_trocadas"], r["tabelas_criadas"], r["mapas_novos"]))
    for linha in r["por_area"]:
        print("  " + linha)
    if r["taxa_de_irmao"]:
        print("  frequencia herdada de sub-mapa irmao: "
              + ", ".join(r["taxa_de_irmao"]))
    if r["taxa_padrao"]:
        print("  frequencia no padrao (nem demake nem irmao): "
              + ", ".join(r["taxa_padrao"]))
    for linha in r.get("fundidas", []):
        print("  FUNDIDA (decisao 2 da condutora): " + linha)
    fundidas = {l.split(" -> ")[0] for l in r.get("fundidas", [])}
    for a in r["sem_sub_mapa"]:
        if a in fundidas:
            continue
        print("  SEM CASA: %s (ver `sem_sub_mapa` no de-para)" % a)


def demo_canonico():
    """Autoteste da sobreposicao. Nao toca em arquivo nenhum."""
    canon, corrigidos = tabelas_canonicas()
    assert len(canon) == 13, len(canon)
    # A correcao de especie do de-para. Eram 6 slots ate o lote K; depois das
    # decisoes 1 e 2 sao 2, e a queda tem conta: os 5% de Darumaka viraram 2,5%
    # ao dividir com a coluna `overworld`, que nao o tem, e 2,5% so alcanca UM
    # slot em vez de dois. Sobraram o Steamdrift Way e a Rota 10 fundida; a
    # White Hill Station perdeu o seu (2,5% nao chega aos 12 slots dela), mas
    # continua no `onde` porque e dela que a Rota 10 fundida herda o bicho.
    # ONDA 3, FECHAMENTO (06/09/2026): virou 3 com a correcao de Mr. Mime, que
    # a condutora pediu pelo MESMO motivo do Darumaka. O slot a mais e um so, e
    # ele e da Rota 10 fundida: o Serebii escreve `Mr. Mime` nas DUAS listas da
    # rota (a principal com 40 no `overworld`, a White Hill Station com 30), e a
    # media das duas alcanca UM slot depois do maior-resto.
    assert corrigidos == 3, corrigidos
    for a in ("MAP_GALAR_ROUTE_8_STEAMDRIFT_WAY", "MAP_GALAR_ROUTE_10"):
        sp = [x[2] for x in canon[a]["land_mons"]]
        assert "SPECIES_DARUMAKA_GALAR" in sp, a
        assert "SPECIES_DARUMAKA" not in sp, a
    sp = [x[2] for x in canon["MAP_GALAR_ROUTE_10"]["land_mons"]]
    assert "SPECIES_MR_MIME_GALAR" in sp, sp
    assert "SPECIES_MR_MIME" not in sp, sp
    # 1. A CONTA daqui e a do `converte.py` da fonte, e continuou sendo depois
    #    da decisao 1: o que mudou foi a ENTRADA, e nao o maior-resto. A prova
    #    e refazer o preparado com a REGRA VELHA (so `grama`, mais `overworld`
    #    quando so um dos dois existe) e cobrar o arquivo slot a slot.
    taxas = _taxas_do_campo()
    LAND = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
    WATER = [60, 30, 5, 4, 1]
    assert taxas["land_mons"] == LAND and taxas["water_mons"] == WATER
    doc = json.load(open(FONTE_CANONICA, encoding="utf-8"))
    preparado = {e["map"]: e for e in doc["wild_encounter_groups"][0]["encounters"]}
    brutos = json.load(open(FONTE_BRUTOS, encoding="utf-8"))["areas"]
    for area in brutos:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", area["nome"]).strip("_").upper()
        e = preparado["MAP_GALAR_" + slug]
        fonte_de = {"land_mons": area.get("grama") or area.get("overworld"),
                    "water_mons": area.get("agua")}
        for tipo, tx in (("land_mons", LAND), ("water_mons", WATER)):
            refeito = _maior_resto(fonte_de[tipo], tx, area["nome"])
            if tipo not in e:
                assert refeito is None, (area["nome"], tipo)
                continue
            esperado = [(m["min_level"], m["max_level"], m["species"])
                        for m in e[tipo]["mons"]]
            assert refeito == esperado, (area["nome"], tipo, refeito, esperado)
    # 1b. DECISAO 1: cada coluna renormalizada soma 100 (com folga de ponto
    #     flutuante), e a media das duas tambem, senao o maior-resto receberia
    #     uma distribuicao torta e daria peso a mais para a coluna maior.
    por_nome = {a["nome"]: a for a in brutos}
    assert len(por_nome) == 13, len(por_nome)
    tortas = 0
    for nome, area in por_nome.items():
        cruas = [sum(float(x.get("taxa") or 0) for x in area[c])
                 for c in ("grama", "overworld") if area.get(c)]
        assert len(cruas) == 2, nome     # as 13 areas tem as DUAS colunas
        tortas += sum(1 for s in cruas if abs(s - 100) > 1e-9)
        for coluna in _colunas_normalizadas(area):
            assert abs(sum(x["taxa"] for x in coluna) - 100) < 1e-9, nome
        d = _distribuicao_de_terra(area)
        assert abs(sum(x["taxa"] for x in d) - 100) < 1e-9, nome
        # Uniao de verdade: nenhuma especie das duas colunas fica de fora, e
        # nenhuma entra duas vezes.
        das_duas = {x["species"] for c in ("grama", "overworld")
                    for x in area[c]}
        assert {x["species"] for x in d} == das_duas, nome
        assert len(d) == len(das_duas), nome
        # Nivel pela uniao das faixas.
        for x in d:
            faixas = [(y["min_level"], y["max_level"])
                      for c in ("grama", "overworld") for y in area[c]
                      if y["species"] == x["species"]]
            assert x["min_level"] == min(f[0] for f in faixas), (nome, x)
            assert x["max_level"] == max(f[1] for f in faixas), (nome, x)
    assert tortas == 7, tortas           # as sete colunas que nao somam 100
    # 1c. A META MEDIDA da decisao 1: as seis especies que so a coluna
    #     `overworld` tem deviam voltar a ter fonte direta de mato em Galar.
    #     CINCO voltam. Axew NAO volta, e o motivo tem conta fechada, escrita
    #     aqui para ninguem "consertar" por engano: os 5% dele na `overworld`
    #     viram 2,5% na media, e na Rota 6 ha um empate de TRES especies em
    #     2,5% (Durant e Torkoal, que vem da `grama`, e Axew) para os DOIS
    #     ultimos slots. O desempate do maior-resto e a ordem da fonte, que e a
    #     regra do `converte.py` e nao se mexe aqui; a `grama` vem antes, e Axew
    #     e o terceiro. Nenhuma leitura da decisao 1 muda isso, porque as duas
    #     colunas da Rota 6 ja somam 100 e a renormalizacao nao altera nada
    #     nela. Fica para o Gui decidir se quer Axew por outro caminho.
    for nome, especie in (("Route 10", "SPECIES_CUBCHOO"),
                          ("Route 8", "SPECIES_GURDURR"),
                          ("Route 5", "SPECIES_MINCCINO"),
                          ("Route 7", "SPECIES_PERRSERKER"),
                          ("Route 8 (Steamdrift Way)", "SPECIES_SNORUNT")):
        slug = re.sub(r"[^A-Za-z0-9]+", "_", nome).strip("_").upper()
        sp = [x[2] for x in canon["MAP_GALAR_" + slug]["land_mons"]]
        assert especie in sp, (nome, especie, sp)
        # e a mesma especie NAO estava na coluna `grama`, que era a unica fonte
        # antes da decisao 1: e isso que prova que ela veio do `overworld`.
        antes_de = {_norm_especie(x["species"])
                    for x in por_nome[nome]["grama"]}
        assert especie not in antes_de, (nome, especie)
    # O caso do Axew, medido e travado: ele ENTRA na distribuicao da Rota 6 com
    # 2,5%, e perde os dois ultimos slots para Durant e Torkoal, que tem os
    # mesmos 2,5% e vem antes na fonte. Se algum dos tres numeros mudar, este
    # `assert` cai e alguem le a conta de novo em vez de descobrir sozinho.
    r6 = {x["species"]: x["taxa"] for x in _distribuicao_de_terra(
        por_nome["Route 6"])}
    for bicho in ("Axew", "Durant", "Torkoal"):
        assert abs(r6[bicho] - 2.5) < 1e-9, (bicho, r6[bicho])
    r6_slots = [x[2] for x in canon["MAP_GALAR_ROUTE_6"]["land_mons"]]
    assert "SPECIES_AXEW" not in r6_slots, r6_slots
    assert r6_slots[-2:] == ["SPECIES_DURANT", "SPECIES_TORKOAL"], r6_slots
    # 1d. E o preparado, que so olhava a `grama`, JA NAO e mais a fonte de
    #     `land_mons`: a Rota 6 do preparado nao tem Axew e a nossa tem.
    velho = [m["species"]
             for m in preparado["MAP_GALAR_ROUTE_6"]["land_mons"]["mons"]]
    assert "SPECIES_AXEW" not in velho, velho
    # 1e. DECISAO 2: o `Galar_Route1001` recebe as DUAS listas canonicas da
    #     Rota 10, e nao so a principal. Klang e Rhydon so existem em White
    #     Hill Station; Vanillish e Snom estao nas duas.
    rota10 = [x[2] for x in canon["MAP_GALAR_ROUTE_10"]["land_mons"]]
    so_da_white_hill = {_norm_especie(x["species"])
                        for c in ("grama", "overworld")
                        for x in por_nome["Route 10 (White Hill Station)"][c]}
    so_da_white_hill -= {_norm_especie(x["species"])
                         for c in ("grama", "overworld")
                         for x in por_nome["Route 10"][c]}
    for especie in ("SPECIES_KLANG", "SPECIES_RHYDON"):
        assert especie in so_da_white_hill and especie in rota10, especie
    for especie in ("SPECIES_CUBCHOO", "SPECIES_ABOMASNOW", "SPECIES_BEARTIC"):
        assert especie in rota10, (especie, rota10)
    assert len(rota10) == 12, rota10
    # 2. Pesca: as cinco areas que a fonte pescou, com 10 slots cada.
    com_pesca = sorted(a for a, t in canon.items() if "fishing_mons" in t)
    assert com_pesca == ["MAP_GALAR_ROUTE_2", "MAP_GALAR_ROUTE_4",
                         "MAP_GALAR_ROUTE_5", "MAP_GALAR_ROUTE_6",
                         "MAP_GALAR_ROUTE_9"], com_pesca
    for a in com_pesca:
        assert len(canon[a]["fishing_mons"]) == 10, a
    # 3. A sobreposicao em si, sobre o plano do demake.
    entradas, _r, _s = plano()
    antes = {e["map"]: json.dumps(e, sort_keys=True) for e in entradas}
    novas, resumo = sobrepoe_canonico([json.loads(v) for v in
                                       (json.dumps(e) for e in entradas)])
    por_mapa = {e["map"]: e for e in novas}
    # 3a. A prova de fidelidade do lote: o Weald deixa de ser um matagal de
    #     Caterpie e volta a ser Skwovet/Rookidee/Hoothoot/Blipbug/Grubbin.
    weald = [m["species"] for m in
             por_mapa["MAP_GALAR_SLUMBERING_WEALD_01"]["land_mons"]["mons"]]
    for exigido in ("SPECIES_ROOKIDEE", "SPECIES_BLIPBUG", "SPECIES_SKWOVET"):
        assert exigido in weald, (exigido, weald)
    assert "SPECIES_CATERPIE" not in weald, weald
    # 3b. O demake FICA onde o datamine nao chega: a agua do Route0302, a pesca
    #     do Route0802 e a do Route1001 nao sao tocadas.
    for mapa, tipo in (("MAP_GALAR_ROUTE03_02", "water_mons"),
                       ("MAP_GALAR_ROUTE08_02", "fishing_mons"),
                       ("MAP_GALAR_ROUTE10_01", "fishing_mons")):
        assert (json.dumps(por_mapa[mapa][tipo], sort_keys=True)
                == json.dumps(json.loads(antes[mapa])[tipo], sort_keys=True)), \
            (mapa, tipo)
    # 3c. Nenhum mapa de fora do de-para mudou.
    de_para = json.load(open(CANONICAS, encoding="utf-8"))
    tocados = {s["mapa"] for a in de_para["areas"] for s in a["sub_mapas"]
               if s["recebe"]}
    for m, texto in antes.items():
        if m not in tocados:
            assert json.dumps(por_mapa[m], sort_keys=True) == texto, m
    # 3d. Regua do PRD, no proprio resultado: especie que existe e mapa que
    #     existe, com o numero de slots que o motor sorteia.
    validas, no_repo = especies_validas(), mapas_do_repo()
    for e in novas:
        assert e["map"] in no_repo, e["map"]
        for tipo, quant in TIPOS:
            if tipo in e:
                assert len(e[tipo]["mons"]) == quant, (e["base_label"], tipo)
                for m in e[tipo]["mons"]:
                    assert m["species"] in validas, m
                    assert 1 <= m["min_level"] <= m["max_level"] <= NIVEL_MAX, m
    rotulos = collections.Counter(e["base_label"] for e in novas)
    assert max(rotulos.values()) == 1, rotulos.most_common(3)
    # 3e. Idempotente: sobrepor de novo devolve o mesmo, byte a byte.
    de_novo, _r2 = sobrepoe_canonico([json.loads(json.dumps(e)) for e in novas])
    assert (json.dumps(de_novo, sort_keys=True)
            == json.dumps(novas, sort_keys=True))
    assert resumo["sem_sub_mapa"] == ["MAP_GALAR_ROUTE_10_WHITE_HILL_STATION"], \
        resumo["sem_sub_mapa"]
    print("demo canonico: OK (%d tabelas trocadas, %d criadas, %d mapas novos)"
          % (resumo["tabelas_trocadas"], resumo["tabelas_criadas"],
             resumo["mapas_novos"]))


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
    a.add_argument("--canonico", action="store_true",
                   help="NAO FAZ NADA desde a decisao 3 da condutora "
                        "(06/09/2026): a sobreposicao canonica virou o padrao. "
                        "A opcao fica aceita so para nao quebrar quem ja tinha "
                        "a linha escrita.")
    a.add_argument("--sem-canonico", action="store_true",
                   help="grava o demake PURO, sem a sobreposicao canonica de "
                        "Sword/Shield. Sai com AVISO, porque contraria a lei do "
                        "Gui de 06/09/2026; ver "
                        "dev_scripts/galar_areas_canonicas.json")
    args = a.parse_args()
    if args.demo:
        demo()
        return demo_canonico()
    if args.valida:
        falhas = valida()
        for f in falhas[:40]:
            print("FALHA:", f)
        print(f"{len(falhas)} falhas" if falhas else "regua: PASSOU")
        return 1 if falhas else 0
    entradas, recusa, resumo = plano()
    canonico = None
    # DECISAO 3 da condutora (06/09/2026): a sobreposicao canonica e o PADRAO.
    # Ate a onda 3 ela era `--canonico`, e `--aplicar` sozinho apagava a
    # sobreposicao sem uma linha de erro (a regua nao acusava, porque a tabela
    # do demake tambem e valida). Invertido o padrao, a armadilha sumiu: quem
    # quer o demake puro precisa dizer `--sem-canonico` e ainda leva o AVISO.
    if args.sem_canonico:
        print("AVISO: `--sem-canonico` grava o demake PURO e deixa Galar sem a "
              "sobreposicao canonica de Sword/Shield, o que contraria a lei do "
              "Gui de 06/09/2026. O padrao e `--aplicar` sozinho, e depois "
              "`distribui_dex.py --galar --aplica`.")
    else:
        entradas, canonico = sobrepoe_canonico(entradas)
    relata(entradas, recusa, resumo)
    if canonico:
        relata_canonico(canonico)
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
