#!/usr/bin/env python3
"""Mede a lacuna de treinador do bloco B4 em Kanto, Johto, Hoenn e Unova.

Uso:
    python3 dev_scripts/treinadores_faltantes_b4.py            # mede tudo
    python3 dev_scripts/treinadores_faltantes_b4.py Johto      # so uma regiao
    python3 dev_scripts/treinadores_faltantes_b4.py --demo

## O metodo, copiado do que fechou Sinnoh em 12/08/2026

`dev_scripts/treinadores_faltantes_sinnoh.py` definiu a regua e ela e a mesma
aqui, so muda o formato da fonte:

- **batalhavel aqui** = constante citada por `trainerbattle*` num `scripts.inc`
  NOSSO **e** com bloco `=== TRAINER_X ===` num `.party` COMPILADO
  (`trainers.party` e `trainers_frlg.party`; os `.party` de Johto e de Sinnoh
  sao acervo e nao entram na ROM, ver `trainer_rules.mk`).
- **lacuna** = treinador que a fonte declara e que nao tem par batalhavel aqui.

A conta e por CONSTANTE, nao por objeto: um treinador pode ter dois bonecos (as
duas metades de uma dupla) e continua sendo uma pessoa com uma flag de "ja
venci".

## O prefixo de regiao, e por que ele nao pode ser adivinhado

Kanto e Hoenn reusam a constante crua da fonte (`TRAINER_CALVIN`), porque a
numeracao veio junto com o decomp. Johto, Sinnoh e Unova entraram DEPOIS, num
espaco de nome ja ocupado, e ganharam prefixo (`TRAINER_JOHTO_BETH`), senao
`TRAINER_BETH`, que ja e de Hoenn, ganharia dois times e duas flags.

Entao a comparacao normaliza os dois lados: tira `TRAINER_` e o prefixo de
regiao, e compara o resto. `TRAINER_JOHTO_BETH` casa com `TRAINER_BETH` da
fonte; `TRAINER_BETH` daqui (que e de Hoenn) tambem casaria, e e por isso que a
busca e feita DENTRO da regiao, mapa a mapa, e nunca no repo inteiro.

## Unova e gen 2, e la treinador nao tem constante

No BW3G o treinador do mapa e um `object_event` de `OBJECTTYPE_TRAINER`, cuja
identidade e o par (classe, id) que o script dele carrega:

    object_event x, y, SPRITE_X, MOVE, rx, ry, hr, tod, PAL, OBJECTTYPE_TRAINER,
                 <trainer_class>, <rotulo do script>, <flag>

e o rotulo cai num bloco `TrainerX:` que comeca com a macro `trainer` do
pokecrystal. A identidade estavel, e a unica que sobrevive a renomeacao do
importador, e **(classe, nome do treinador)** que a macro `trainer` declara.
"""
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.abspath(os.path.join(REPO, "..", "fontes-mapas"))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import completude as C          # noqa: E402
import importa_npcs_sinnoh as I  # noqa: E402

# ARMADILHA medida em 12/08/2026, e ela e a razao de Hoenn aparecer com 4 de
# divida no INVENTARIO.md: em `pokeemerald` o `trainerbattle` cru leva o MODO na
# frente do treinador (`trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT,
# TRAINER_COLE, ...`). Regex que pega o primeiro `TRAINER_*` da linha colhe
# `TRAINER_BATTLE_CONTINUE_SCRIPT`, `TRAINER_BATTLE_SET_TRAINER_A` e
# `TRAINER_BATTLE_PYRAMID` como se fossem gente, dos dois lados. Aqui o modo e
# descartado por nome e o treinador e o proximo simbolo da linha.
#
# `multi_2_vs_2` entra junto porque o expansion trocou por ele o par
# Maxie/Tabitha do Space Center, e sem isso os dois apareciam como divida de
# Hoenn, que e a regua de controle e tem que dar zero.
RE_LINHA_BATALHA = re.compile(
    r"^[ \t]*(?:[a-z_]*trainerbattle\w*|multi_\d_vs_\d)[ \t]+(.*)$", re.M)
RE_CONST = re.compile(r"\bTRAINER_\w+")
# `TRAINER_NONE` e o sentinela do segundo slot do `trainerbattle` longo do
# expansion, nao e gente.
MODO = re.compile(r"^TRAINER_BATTLE_|^TRAINER_NONE$")

# EXCECAO DELIBERADA, decidida pelo Gui em 12/08/2026 e registrada na secao 9 do
# PRD-ROM-COMPLETA.md. Nao e trabalho pendente e nao entra em fila: e feature que
# esta ROM nao tem, nao porte que faltou fazer.
#
#  - escala de lider do hns: la o lider tem tres times, escolhidos por quantas
#    insignias o jogador ja tem. Aqui cada lider tem UM time.
#  - ramo do rival por inicial: o hns tem um time de rival para cada inicial de
#    Johto. Aqui existe um ramo so, `RIVAL_SILVER_1..4`.
#
# **Reabre se os iniciais de Johto virarem escolhiveis.** Ate la, quem rodar esta
# ferramenta ve os 15 marcados e nao precisa remedir o motivo.
EXCECAO_JOHTO = {
    "CHUCK_1_2", "CHUCK_1_3", "PRYCE_1_2", "PRYCE_1_3",
    "JASMINE_1_2", "JASMINE_1_3",
    "RIVAL_CYNDAQUIL_1", "RIVAL_CYNDAQUIL_2", "RIVAL_CYNDAQUIL_3",
    "RIVAL_CYNDAQUIL_4", "RIVAL_TOTODILE_1", "RIVAL_TOTODILE_2",
    "RIVAL_TOTODILE_3", "RIVAL_TOTODILE_4", "RIVAL_CHIKORITA_4",
}


def trainerbattles(texto):
    """Constantes de TREINADOR citadas por comando de batalha, sem os modos.

    `multi_2_vs_2` cita DOIS treinadores na mesma linha, entao a colheita nao
    para no primeiro; o que para no primeiro seria o `trainerbattle` cru, e la o
    primeiro simbolo e o modo, que ja sai por nome.
    """
    fora = set()
    for resto in RE_LINHA_BATALHA.findall(texto):
        fora |= {c for c in RE_CONST.findall(resto) if not MODO.match(c)}
    return fora
PREFIXOS = ("JOHTO_", "SINNOH_", "UNOVA_", "KANTO_")

REGIOES_GEN3 = {
    "Kanto": ("Frlg", f"{FONTES}/pokefirered"),
    "Johto": ("Johto", f"{FONTES}/hns"),
    "Hoenn": ("TownsAndRoutes", f"{FONTES}/pokeemerald"),
}


def le(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def times_declarados():
    """TRAINER_* com bloco `=== TRAINER_X ===` em .party COMPILADO."""
    fora = set()
    for nome in ("trainers.party", "trainers_frlg.party"):
        p = os.path.join(REPO, "src/data", nome)
        if os.path.exists(p):
            fora |= set(re.findall(r"^===\s*(TRAINER_\w+)\s*===", le(p), re.M))
    return fora


def nu(const):
    """`TRAINER_JOHTO_BETH` -> `BETH`. Chave de comparacao com a fonte."""
    s = const[len("TRAINER_"):] if const.startswith("TRAINER_") else const
    for p in PREFIXOS:
        if s.startswith(p):
            return s[len(p):]
    return s


def batalhavel_por_mapa(raiz, mapas):
    """{mapa: {constante citada por trainerbattle}}."""
    fora = {}
    for m in mapas:
        p = f"{raiz}/data/maps/{m}/scripts.inc"
        fora[m] = trainerbattles(le(p)) if os.path.exists(p) else set()
    return fora


def sinnoh_set():
    return set(I.nossos_mapas_sinnoh())


def mede_gen3(regiao):
    """(nossos_por_mapa, fonte_por_mapa, pares_de_mapa, ausentes)."""
    chave, fonte = REGIOES_GEN3[regiao]
    mg = C.todos_os_mapas(REPO)
    sinnoh = sinnoh_set()
    nossos = [m for m in C.nossos_da_regiao(mg, chave) if m not in sinnoh]
    deles = {C.normaliza(m): m for m in C.todos_os_mapas(fonte)}
    pares = {m: deles.get(C.normaliza(m)) for m in nossos}
    meus = batalhavel_por_mapa(REPO, nossos)
    seus = batalhavel_por_mapa(fonte, [v for v in pares.values() if v])
    ausentes = C.mapas_so_na_fonte(deles, mg, fonte)
    return meus, seus, pares, sorted(ausentes), fonte


def nucleo(s):
    """`CHUCK_1` -> `CHUCK`. Sufixo numerico da fonte nao e nome."""
    return re.sub(r"(_\d+)+$", "", s)


def casa(nosso, seu):
    """O nosso rotulo E o treinador `seu` da fonte?

    Tres formas, medidas nos tres importadores que criaram esses nomes:
    igualdade (`ABE` == `ABE`), classe na frente (`BIRD_KEEPER_ABE` para `ABE`,
    que e o padrao de `importa_treinadores_johto.py`) e sufixo numerico da fonte
    que aqui virou variante unica (`LEADER_CHUCK` para `CHUCK_1`).
    """
    n, k = nu(nosso), nucleo(seu)
    return n == seu or n.endswith("_" + seu) or n == k or n.endswith("_" + k)


def relatorio_gen3(regiao):
    meus, seus, pares, ausentes, fonte = mede_gen3(regiao)
    times = times_declarados()
    citado = {c for s in meus.values() for c in s}
    sem_time = {c for c in citado if c not in times}

    falta, por_contagem, excesso = {}, {}, {}
    fonte_total = 0
    for meu, seu in sorted(pares.items()):
        if not seu:
            continue
        deles = sorted(nu(c) for c in seus.get(seu, ()))
        nossos = sorted(c for c in meus.get(meu, ()) if c in times)
        fonte_total += len(deles)
        livres = list(nossos)
        sobra_fonte = []
        for s in deles:
            achou = next((o for o in livres if casa(o, s)), None)
            if achou:
                livres.remove(achou)
            else:
                sobra_fonte.append(s)
        # Sobra dos dois lados no MESMO mapa: e o mesmo capanga anonimo com
        # outro nome (a fonte diz `GRUNT_21`, o importador chamou de
        # `ROCKET_GRUNT_WELL_1`). Pareia por contagem e mostra o par, para
        # conferencia a mao; o que nao pareia e lacuna de verdade.
        n = min(len(sobra_fonte), len(livres))
        if n:
            por_contagem[meu] = (sobra_fonte[:n], livres[:n])
        if sobra_fonte[n:]:
            falta[meu] = sobra_fonte[n:]
        if livres[n:]:
            excesso[meu] = livres[n:]

    # Ultima passada: o mesmo treinador, casado em OUTRO mapa. Acontece por dois
    # motivos reais e nenhum e divida. (1) A fonte declara o script num mapa e
    # poe o boneco em outro: a Beth mora no `Route26/scripts.inc` do hns e o
    # boneco dela esta na `Route26North`, entao aqui ela e "sobra" de um e
    # "falta" de outro. (2) A cena foi portada para outro mapa: o quarto duelo
    # com o rival esta na `GoldenrodCity` aqui e no `..._UndergroundSwitches` la.
    # Nos dois casos o treinador EXISTE e e batalhavel, que e o que B4 mede;
    # onde ele esta e assunto do bloco B6.
    noutro_mapa = {}
    for m, v in list(falta.items()):
        for s in list(v):
            dono = next((mm for mm, ex in excesso.items()
                         if any(casa(o, s) for o in ex)), None)
            if not dono:
                continue
            ex = excesso[dono]
            achou = next(o for o in ex if casa(o, s))
            ex.remove(achou)
            if not ex:
                del excesso[dono]
            v.remove(s)
            noutro_mapa.setdefault(m, []).append((s, dono, nu(achou)))
        if not v:
            del falta[m]

    so_fonte = {}
    for m in ausentes:
        p = f"{fonte}/data/maps/{m}/scripts.inc"
        if os.path.exists(p):
            v = sorted({nu(c) for c in trainerbattles(le(p))})
            if v:
                so_fonte[m] = v
                fonte_total += len(v)
    return {
        "regiao": regiao, "fonte": fonte, "fonte_total": fonte_total,
        "aqui": len(citado - sem_time), "citado_sem_time": sem_time,
        "falta": falta, "por_contagem": por_contagem, "excesso": excesso,
        "noutro_mapa": noutro_mapa,
        "so_em_mapa_ausente": so_fonte, "pares": pares, "ausentes": ausentes,
    }


# ------------------------------------------------------------------ Unova

# `trainer CLASSE, NOME, ...` dentro do bloco de script do mapa.
RE_TRAINER_MACRO = re.compile(r"^\s*trainer\s+(\w+),\s*(\w+)", re.M)
RE_OBJ_TRAINER = re.compile(
    r"^\s*object_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+),\s*(-?\d+),"
    r"\s*(-?\d+),\s*(-?\w+),\s*(-?\w+),\s*(\w+),\s*OBJECTTYPE_TRAINER,"
    r"\s*(-?\w+),\s*(\w+)", re.M)


def corpos_gen2(asm):
    corte = re.compile(r"^(\w+):+\s*$", re.M)
    marcas = list(corte.finditer(asm))
    fora = {}
    for n, m in enumerate(marcas):
        fim = marcas[n + 1].start() if n + 1 < len(marcas) else len(asm)
        fora[m.group(1)] = asm[m.end():fim]
    return fora


def mede_unova():
    """{NOME_DO_TREINADOR: [(mapa, x, y, sprite, raio, rotulo)]} na fonte.

    A chave e o SEGUNDO argumento da macro `trainer` (`HARLEQUIN_CASTELIA_GYM_1`),
    porque foi exatamente ele que `gera_treinadores_unova.py` prefixou com
    `TRAINER_UNOVA_` para criar a constante daqui. Casamento sem heuristica.
    """
    fonte = f"{FONTES}/bw3g"
    deles = {}
    for p in sorted(glob.glob(f"{fonte}/maps/*.asm")):
        mapa = os.path.basename(p)[:-4]
        if C.LIXO.search(mapa):
            continue
        asm = le(p)
        corpos = corpos_gen2(asm)
        m = re.search(rf"^{re.escape(mapa)}_MapEvents:", asm, re.M)
        if not m:
            continue
        for o in RE_OBJ_TRAINER.findall(asm[m.end():]):
            rot = o[10]
            mac = RE_TRAINER_MACRO.search(corpos.get(rot, ""))
            chave = mac.group(2) if mac else f"?{mapa}:{rot}"
            deles.setdefault(chave, []).append(
                (mapa, int(o[0]), int(o[1]), o[2], o[9], rot))
    mg = C.todos_os_mapas(REPO)
    nossos = [m for m in C.nossos_da_regiao(mg, "Unova") if m not in sinnoh_set()]
    return deles, nossos, fonte


# `loadtrainer CLASSE, ID` e a OUTRA forma de declarar treinador em gen 2, e sem
# ela a medida de Unova mente dos dois lados. Lider de ginasio e Elite dos Quatro
# do BW3G NAO sao `OBJECTTYPE_TRAINER`: o boneco e um NPC de script comum e a
# batalha e aberta por `loadtrainer BURGH, BURGH1` dentro do script da sala.
# Contar so objeto dava "348 na fonte contra 360 aqui", e os 12 de excesso eram
# exatamente os 8 lideres e os 4 da Elite. Medido em 12/08/2026.
RE_LOADTRAINER = re.compile(r"^\s*loadtrainer\s+(\w+),\s*(\w+)", re.M)


def lideres_gen2(fonte):
    """{CLASSE: [(mapa, id)]} de todo `loadtrainer` dos mapas do BW3G."""
    fora = {}
    for p in sorted(glob.glob(f"{fonte}/maps/*.asm")):
        mapa = os.path.basename(p)[:-4]
        for cl, idn in RE_LOADTRAINER.findall(le(p)):
            fora.setdefault(cl, []).append((mapa, idn))
    return fora


def relatorio_unova():
    deles, nossos, fonte = mede_unova()
    times = times_declarados()
    meus = batalhavel_por_mapa(REPO, nossos)
    aqui = {c for s in meus.values() for c in s}
    com_time = {c for c in aqui if c in times}
    chaves_aqui = {nu(c) for c in com_time}
    carga = lideres_gen2(fonte)
    # `LEADER_BURGH` daqui casa com a classe `BURGH` do `loadtrainer`; o nome que
    # o importador usou e `LEADER_`/`E4_` mais a classe da fonte.
    por_carga = {k for k in chaves_aqui
                 if k.split("_", 1)[-1] in carga
                 and k.split("_")[0] in ("LEADER", "E4")}
    # Mapa da fonte que nao e de Unova (o BW3G e hack de pokecrystal e ainda
    # carrega mapa de Johto, como o NationalPark): fica fora da conta, senao os
    # apanhadores de inseto do National Park viram divida de Unova.
    nossos_norm = {C.normaliza(m) for m in nossos}
    fora_da_regiao = {k for k, v in deles.items()
                      if all(C.normaliza(m) not in nossos_norm for m, *_ in v)}
    return {
        "regiao": "Unova", "fonte": fonte,
        "fonte_chaves": deles, "meus_por_mapa": meus, "loadtrainer": carga,
        "aqui": aqui, "com_time": com_time, "chaves_aqui": chaves_aqui,
        "citado_sem_time": aqui - com_time, "nossos": nossos,
        "falta": sorted(set(deles) - chaves_aqui - fora_da_regiao),
        "fora_da_regiao": sorted(fora_da_regiao),
        "excesso": sorted(chaves_aqui - set(deles) - por_carga),
        "por_carga": sorted(por_carga),
    }


def main():
    alvos = [a for a in sys.argv[1:] if not a.startswith("-")] or \
        ["Kanto", "Johto", "Hoenn", "Unova"]
    for r in alvos:
        if r == "Unova":
            d = relatorio_unova()
            print(f"\n=== Unova (fonte bw3g) ===")
            print(f"  fonte: {len(d['fonte_chaves'])} treinadores distintos "
                  f"em {sum(len(v) for v in d['fonte_chaves'].values())} objetos")
            print(f"  aqui:  {len(d['aqui'])} citados, {len(d['com_time'])} com time")
            print(f"  LACUNA: {len(d['falta'])}")
            print(f"  EXCESSO (aqui e nao na fonte): {len(d['excesso'])}")
            print(f"  lider/E4 provados por `loadtrainer`: {len(d['por_carga'])}")
            print(f"  fonte fora de Unova (mapa de Johto do BW3G): "
                  f"{len(d['fora_da_regiao'])}: {', '.join(d['fora_da_regiao'])}")
            if d["citado_sem_time"]:
                print(f"  citados SEM time: {sorted(d['citado_sem_time'])[:10]}")
            for k in d["falta"]:
                print(f"    FALTA  {k:44s} "
                      f"{', '.join(o[0] for o in d['fonte_chaves'][k])}")
            for k in d["excesso"]:
                print(f"    SOBRA  {k}")
            continue
        d = relatorio_gen3(r)
        nf = sum(len(v) for v in d["falta"].values())
        na = sum(len(v) for v in d["so_em_mapa_ausente"].values())
        nx = sum(len(v) for v in d["excesso"].values())
        nc = sum(len(a) for a, _b in d["por_contagem"].values())
        nm = sum(len(v) for v in d["noutro_mapa"].values())
        print(f"\n=== {r} (fonte {os.path.basename(d['fonte'])}) ===")
        print(f"  fonte: {d['fonte_total']} treinadores citados")
        print(f"  aqui:  {d['aqui']} batalhaveis")
        print(f"  LACUNA em mapa que existe aqui: {nf}")
        print(f"  lacuna em mapa AUSENTE aqui:    {na}")
        print(f"  pareados por contagem (mesmo mapa, nome trocado): {nc}")
        print(f"  casados em OUTRO mapa nosso:    {nm}")
        print(f"  excesso (aqui e nao na fonte):  {nx}")
        if d["citado_sem_time"]:
            print(f"  citados sem time: {sorted(d['citado_sem_time'])}")
        exc = EXCECAO_JOHTO if r == "Johto" else set()
        ne = sum(1 for v in d["falta"].values() for c in v if c in exc)
        if ne:
            print(f"  destes, EXCECAO DELIBERADA (secao 9 do PRD): {ne}")
        for m, v in sorted(d["falta"].items()):
            fica = [c for c in v if c not in exc]
            if fica:
                print(f"    FALTA {m:36s} {', '.join(fica)}")
            for c in v:
                if c in exc:
                    print(f"    (excecao) {m:32s} {c}")
        for m, v in sorted(d["excesso"].items()):
            print(f"    SOBRA {m:36s} {', '.join(nu(x) for x in v)}")
        for m, v in sorted(d["noutro_mapa"].items()):
            for s0, dono, nome in v:
                print(f"    NOUTRO {m:35s} {s0} esta em {dono} como {nome}")
        for m, v in sorted(d["so_em_mapa_ausente"].items()):
            print(f"    AUSENTE {m:34s} {len(v)}: {', '.join(v[:8])}")
    return 0


def demo():
    # 1. normalizacao de prefixo nos dois sentidos.
    assert nu("TRAINER_JOHTO_BETH") == "BETH"
    assert nu("TRAINER_BETH") == "BETH"
    assert nu("TRAINER_SINNOH_WORKER_COLIN") == "WORKER_COLIN"
    # 2. Hoenn e o controle: fonte intocada, entao a lacuna tem que ser pequena
    #    e o excesso ZERO. Se Hoenn der lacuna grande, a regua esta errada.
    d = relatorio_gen3("Hoenn")
    assert d["fonte_total"] > 500, d["fonte_total"]
    assert not d["excesso"], f"Hoenn nao pode ter excesso: {d['excesso']}"
    # A unica ausencia legitima de Hoenn e o PHILLIP da Pirâmide de Batalha, que
    # o expansion trocou por `facilitytrainerbattle FACILITY_BATTLE_PYRAMID`: la
    # o adversario e sorteado pelo motor e nao ha `trainerbattle` para achar.
    assert {c for v in d["falta"].values() for c in v} == {"PHILLIP"}, d["falta"]
    # 3. MUTACAO PLANTADA: sem descartar o MODO do `trainerbattle` cru, os tres
    #    pseudo-treinadores `TRAINER_BATTLE_*` de Hoenn voltam a contar como
    #    gente. Se este assert ficar verde, a armadilha do topo do arquivo
    #    voltou e o INVENTARIO cobra divida que nao existe.
    cru = ("\ttrainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_COLE, "
           "LOCALID_COLE, T1, T2, S, OBJ_ID_NONE, TRAINER_NONE\n")
    assert trainerbattles(cru) == {"TRAINER_COLE"}, trainerbattles(cru)
    # 4. Unova: os 12 "de excesso" que o INVENTARIO acusa (360 aqui contra 348 na
    #    fonte) sao os 8 lideres e os 4 da Elite dos Quatro, e cada um esta na
    #    fonte, provado por `loadtrainer`. Sem essa prova o veredito seria
    #    "treinador inventado" e 12 pessoas legitimas seriam apagadas.
    u = relatorio_unova()
    assert len(u["por_carga"]) == 12, u["por_carga"]
    assert not u["excesso"], f"Unova com excesso de verdade: {u['excesso']}"
    assert not u["falta"], f"Unova com lacuna: {u['falta']}"
    carga = u["loadtrainer"]
    for k in u["por_carga"]:
        assert k.split("_", 1)[1] in carga, k
    # 4b. e os 4 que sobram na fonte sao do National Park, que e mapa de JOHTO
    #     dentro do BW3G (hack de pokecrystal), nao divida de Unova.
    assert u["fora_da_regiao"] == ["BEVERLY1", "JACK1", "KRISE", "WILLIAM"], \
        u["fora_da_regiao"]

    # 5. a excecao deliberada tem que continuar sendo excecao, e nada alem dela.
    #    Se alguem ligar um dos 15 (ou se a fonte deixar de te-lo), este assert
    #    cai e a nota do PRD e revisitada em vez de envelhecer calada.
    j = relatorio_gen3("Johto")
    abertos = {c for v in j["falta"].values() for c in v}
    assert EXCECAO_JOHTO <= abertos, \
        f"excecao ja resolvida, atualize a secao 9 do PRD: {EXCECAO_JOHTO - abertos}"
    assert len(abertos - EXCECAO_JOHTO) == 10, sorted(abertos - EXCECAO_JOHTO)

    # 6. unicidade de rotulo e de id em opponents.h.
    txt = le(os.path.join(REPO, "include/constants/opponents.h"))
    pares = re.findall(r"#define\s+(TRAINER_\w+)\s+(\d+)", txt)
    nomes = [a for a, _ in pares]
    ids = [int(b) for _, b in pares]
    assert len(set(nomes)) == len(nomes), "rotulo repetido em opponents.h"
    assert len(set(ids)) == len(ids), "id repetido em opponents.h"
    teto = int(re.search(r"MAX_TRAINERS_COUNT_EMERALD\s+(\d+)", txt).group(1))
    assert max(ids) < teto
    print(f"demo ok (maior id {max(ids)}, teto {teto}, "
          f"livres {teto - max(ids) - 1})")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
