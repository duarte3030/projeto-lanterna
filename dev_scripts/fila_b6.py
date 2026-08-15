#!/usr/bin/env python3
"""Regenera a FILA do bloco B6 (cenas de história das três regiões portadas).

    python3 dev_scripts/fila_b6.py            # só o resumo por região e tipo
    python3 dev_scripts/fila_b6.py --gravar   # escreve dev_scripts/fila_b6.json
    python3 dev_scripts/fila_b6.py --demo     # autoteste (não escreve nada)

## Por que este arquivo existe

Até 15/08/2026 o B6 não tinha fila: `ESTADO.md`, `PLANO-UNOVA.md`,
`PENDENCIAS-JOHTO.md` e `PENDENCIAS-NPC-SINNOH.md` guardavam só NÚMEROS
AGREGADOS, escritos à mão em datas diferentes, e por isso divergiam entre si
(104 x 107 x 40 cenas de `changeblock`; 348/176 x 230/84 objetos e gatilhos de
Sinnoh). Número agregado escrito à mão envelhece calado: ninguém consegue
conferir de onde ele veio, e quem for executar não sabe QUAL cena falta, só
quantas.

A fila aqui é a **saída de uma varredura**, nunca um texto digitado. Base nova
(mapa novo importado, cena portada, item criado), roda de novo e o JSON conta a
verdade daquele dia. `fila_b6.json` é artefato gerado: não editar à mão.

## O critério de classificação, e por que é o mesmo da casa

Uma "cena" do gen 2 não é um script só: o `coord_event` aponta para um rótulo
que salta para outros rótulos, e o comando que decide o QUANTO de trabalho a
cena dá (o `changeblock`, o `callasm`) quase sempre mora dois ou três saltos
adiante. Medir só o corpo do primeiro rótulo mente para baixo: a varredura
anterior achou **8 `callasm` literais em 5 arquivos** de `bw3g/maps/`, enquanto
a cadeia inteira mostra **16 cenas** que chegam a `callasm`, porque quase todos
estão em `engine/events/` e são alcançados por `jumpstd`/`farsjump`.

Por isso a travessia usa o MESMO regex que o inventário da casa já usa para
saber se um NPC fala: `SEGUE_GEN2` em `dev_scripts/inventario.py` (linha ~468),
que é `sjump|jump|callasm|scall|farsjump`, mais o `JUMPSTD` da linha seguinte
(que leva para `engine/events/std_scripts.asm`). Os dois são IMPORTADOS daqui,
não copiados: duas cópias do critério divergiriam no dia em que uma fosse
ajustada, e o preço seria uma fila que discorda do inventário sobre o que é
cena. A profundidade é 6 saltos (o inventário usa 3 porque só quer saber se há
texto; aqui o interesse é o fecho inteiro).

**Cena x chamada x arquivo, que é a origem das três divergências:**

- **cena** = um `coord_event` de um mapa que foi importado. É a unidade da fila,
  porque é o que o jogador dispara. Unova tem **209**.
- **chamada** = uma linha `changeblock` dentro do fecho de uma cena. A MESMA
  linha conta de novo se duas cenas chegam nela, e é por isso que as 1226
  chamadas cabem em 884 linhas de fonte.
- **arquivo** = um `.asm` de `bw3g/maps/`. São **40** os que citam `changeblock`
  em qualquer lugar, inclusive em script que nenhum `coord_event` alcança. Esse
  40 nunca foi contagem de cena, e comparar com 107 é comparar coisas
  diferentes.

O tipo de cada cena sai por PRIORIDADE, não por soma: uma cena que tem
`changeblock` e `setscene` entra uma vez só, como `changeblock`, que é o
trabalho mais caro. Os totais por tipo dos documentos são SOBREPOSTOS (somam
250 para 209 cenas), e o JSON guarda os dois: `tipo` é o exclusivo, `tem` lista
todos os comandos caros que a cena alcança.

## Sinnoh: a fila sai da MESMA recusa do importador

`dev_scripts/importa_npcs_sinnoh.py` recusa, de propósito, objeto com
`hidden_flag` (decisão 2 do cabeçalho dele) e todo `coord_event` (a var do
Platinum não existe aqui). Este script IMPORTA aquele módulo e repete a recusa
na mesma ordem (mobília -> nome próprio -> hidden_flag), sobre todos os mapas
casados, com uma diferença que é o ponto:

**o atalho `ja_importado` fica de fora.** Lá ele existe para não dobrar a
população da cidade ao rodar `--aplicar` duas vezes, e por isso o `resumo:` que
o importador imprime encolhe a cada rodada: em 15/08/2026 ele diz 78/46 porque
pula 360 mapas já marcados. Esse número mede "o que sobrou de não visitado",
não "quanto falta de cena", e foi ele que produziu os 348/176 do `ESTADO.md`.
A população é invariante e não depende de quantas vezes alguém rodou o
importador.

A unidade da fila de Sinnoh não é o objeto: é a **`FLAG_HIDE_*`**, porque o que
falta é a CENA que apaga a flag, e uma cena apaga a flag de todos os objetos
dela de uma vez (regra escrita em `PENDENCIAS-NPC-SINNOH.md` seção 3). Para os
gatilhos, a unidade é `(mapa, var, script)`.

## Johto: transcrição, e isto está declarado

Johto é a única região cuja fila NÃO sai de varredura: a fonte dela é a seção 6
de `PENDENCIAS-JOHTO.md`, escrita à mão por quem fechou a primeira leva, e não
existe artefato de máquina que a reproduza. O que este script faz é transcrever
aquela seção para o mesmo formato e **conferir os bloqueios contra o repo**
(`ITEM_TIDAL_BELL` existe? `OBJ_EVENT_GFX_RED_NORMAL` existe? sobrou id de
treinador na faixa 2462-2499?), para que o bloqueio pare de ser memória de
documento e vire leitura de `include/`.
"""
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import inventario as INV                # noqa: E402  SEGUE_GEN2/JUMPSTD/corpos_gen2
import importa_unova as U               # noqa: E402  le_grupos/le_eventos/indice_asm
import importa_npcs_sinnoh as S         # noqa: E402  a régua de recusa de Sinnoh

SAIDA = os.path.join(REPO, "dev_scripts/fila_b6.json")
PROFUNDIDADE = 6

# Comandos que decidem o custo de uma cena de gen 2, em ORDEM DE PRIORIDADE.
# A ordem é a do PLANO-UNOVA.md: o `changeblock` primeiro porque é o único que
# obriga a traduzir id de bloco do gen 2 para metatile daqui, um por um.
COMANDOS = [
    ("changeblock", re.compile(r"^\s*changeblock\b", re.M)),
    ("setscene",    re.compile(r"^\s*(?:setscene|setmapscene)\b", re.M)),
    ("batalha",     re.compile(r"^\s*(?:loadtrainer|startbattle|loadwildmon"
                               r"|winlosstext)\b", re.M)),
    ("special",     re.compile(r"^\s*special\b", re.M)),
    ("callasm",     re.compile(r"^\s*callasm\b", re.M)),
]
# Cena que empurra o jogador. É o sinal do "bloqueio" de PLANO-UNOVA.md: o NPC
# vira, fala e devolve o jogador, e como o enredo nunca avança aqui, portar isso
# planta parede permanente (a armadilha das 39 pedras de Strength).
MOVE_JOGADOR = re.compile(r"^\s*applymovement\s+PLAYER\b", re.M)


def indice_de_rotulos():
    """rótulo -> corpo, em TODO o bw3g, não só em maps/.

    O `callasm` indireto mora em `engine/events/`; sem varrer a árvore inteira a
    cadeia morre no primeiro salto para fora de maps/ e a fila mente para baixo.
    """
    corpos = {}
    for raiz, _, arquivos in os.walk(U.BW3G):
        if os.sep + ".git" in raiz:
            continue
        for a in sorted(arquivos):
            if not a.endswith(".asm"):
                continue
            txt = open(os.path.join(raiz, a), encoding="utf-8",
                       errors="replace").read()
            for k, v in INV.corpos_gen2(txt).items():
                corpos.setdefault(k, v)
    return corpos, INV.corpos_std_gen2(U.BW3G)


def fecho(rot, corpos, std, prof=0, visto=None):
    """Corpos alcançados a partir de `rot`, seguindo SEGUE_GEN2 e JUMPSTD."""
    if visto is None:
        visto = set()
    if not rot or rot in visto or prof > PROFUNDIDADE:
        return []
    visto.add(rot)
    corpo = corpos.get(rot)
    if corpo is None:
        return []
    saida = [corpo]
    for m in INV.SEGUE_GEN2.finditer(corpo):
        saida += fecho(m.group(1), corpos, std, prof + 1, visto)
    for m in INV.JUMPSTD.finditer(corpo):
        alvo, chave = std.get(m.group(1).lower()), "jumpstd:" + m.group(1).lower()
        if alvo is not None and chave not in visto:
            visto.add(chave)
            saida.append(alvo)
            for mm in INV.SEGUE_GEN2.finditer(alvo):
                saida += fecho(mm.group(1), corpos, std, prof + 1, visto)
    return saida


# ------------------------------------------------------------------- unova

def fila_unova():
    corpos, std = indice_de_rotulos()
    idx = U.indice_asm()
    itens, chamadas = [], collections.Counter()
    for _, mapas in U.le_grupos():
        for camel, const, *_ in mapas:
            p = idx.get(camel) or f"{U.BW3G}/maps/{camel}.asm"
            if not os.path.exists(p):
                continue
            asm = open(p, encoding="utf-8", errors="replace").read()
            for x, y, cena, rot in U.le_eventos(asm, camel)["coord"]:
                corpo = "\n".join(fecho(rot, corpos, std))
                tem = [n for n, rx in COMANDOS if rx.search(corpo)]
                for n, rx in COMANDOS:
                    chamadas[n] += len(rx.findall(corpo))
                empurra = bool(MOVE_JOGADOR.search(corpo))
                tipo = tem[0] if tem else ("portavel_bloqueio" if empurra
                                           else "portavel")
                itens.append({
                    "regiao": "unova",
                    "id": f"{camel}.asm:{rot}@{x},{y}",
                    "mapa_destino": U.PREFIXO + camel,
                    "tipo": tipo,
                    "tem": tem,
                    "tamanho": len(corpo.splitlines()),
                    "bloqueio": BLOQUEIO_UNOVA[tipo],
                    "status": "pendente",
                })
    return itens, chamadas


BLOQUEIO_UNOVA = {
    "changeblock": "traduzir id de bloco do gen 2 para metatile, um por um, "
                   "mais uma flag por estado",
    "setscene": "a máquina de estados do enredo da Plasma não existe nesta ROM",
    "batalha": "treinador da cena precisa de id em opponents.h e time em "
               "trainers.party",
    "special": "o `special` do gen 2 não tem equivalente aqui",
    "callasm": "callasm é código do gen 2 chamado da cena; sem equivalente",
    # O detector é `applymovement PLAYER`, e é MAIS LARGO que a contagem à mão
    # de PLANO-UNOVA.md (17): ele pega também a segunda metade de cena, que move
    # o jogador sem empurrá-lo. Larga de propósito: cena que mexe no jogador sem
    # o enredo por trás é sempre revisão humana, nunca trabalho de executor.
    "portavel_bloqueio": "cena mexe no jogador (applymovement PLAYER); sem o "
                         "enredo por trás vira parede permanente ou movimento "
                         "sem motivo, precisa de revisão humana",
    "portavel": "nenhum",
}


# ------------------------------------------------------------------ sinnoh

# As cenas da Galáctica fechadas em 12/08/2026 por
# `dev_scripts/cena_galactica_sinnoh.py`. A chave é a `FLAG_HIDE_*` da fonte,
# que é o que a cena passou a apagar; lida do próprio script, nunca digitada.
#
# Sai daqui um par, e a diferença entre os dois importa para quem executa:
#   `flags`  = a FLAG_HIDE_* ganhou cena, então o bloqueio dela acabou;
#   `mapas`  = o mapa onde os objetos já foram postos.
# Flag com cena mas mapa não visitado (os andares do QG que a cena não usa)
# continua PENDENTE, com bloqueio "nenhum": o caro (a cena) está feito e sobra
# só pôr o objeto. Marcar isso como feito esconderia trabalho barato e pronto.
def galactica_feito():
    try:
        import cena_galactica_sinnoh as G
    except Exception:
        return set(), set()
    flags, mapas = set(), set()
    for c in list(getattr(G, "CENAS", [])) + list(getattr(G, "HORARIO", [])):
        if c.get("hidden_flag"):
            flags.add(c["hidden_flag"])
        mapas.update(c.get("mapas") or ([c["mapa"]] if c.get("mapa") else []))
    for c in getattr(G, "ROTEIRO", []):
        if c.get("mapa"):
            mapas.add(c["mapa"])
    return flags, mapas


def mapas_casados_sinnoh():
    heads = S.headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(S.chave(h), (h, ev, mx))
    saida = []
    for m in S.mapas_editaveis_sinnoh():
        h = S.APELIDOS.get(m)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(S.chave(m))
        if alvo:
            saida.append((m,) + alvo)
    return saida


def vars_do_repo():
    p = os.path.join(REPO, "include/constants/vars.h")
    return set(re.findall(r"#define\s+(VAR_\w+)", open(p).read()))


def fila_sinnoh():
    com_cena, ja_postos = galactica_feito()
    conhecidas = vars_do_repo()
    hid = collections.Counter()      # (mapa, FLAG_HIDE_*) -> objetos
    gat = collections.Counter()      # (mapa, var, script) -> tiles
    for meu, _header, arq, _mx in mapas_casados_sinnoh():
        p = os.path.join(S.PLAT, "res/field/events", arq + ".json")
        if not os.path.exists(p):
            continue
        fonte = json.load(open(p))
        for e in fonte.get("object_events", []):
            classe = e.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
            # MESMA ordem do importador: mobília sai como mobília, e só o que
            # sobra é medido pela hidden_flag.
            if any(t in classe for t in S.GRAFICOS_PROIBIDOS):
                continue
            if any(t in classe for t in S.NOMES_PROPRIOS):
                continue
            hf = str(e.get("hidden_flag", "0"))
            if hf not in ("0", "0x0"):
                hid[(meu, hf)] += 1
        for ce in fonte.get("coord_events", []):
            gat[(meu, str(ce.get("var")), str(ce.get("script")))] += 1

    itens = []
    for (mapa, flag), n in sorted(hid.items()):
        itens.append({
            "regiao": "sinnoh", "id": f"{mapa}:{flag}", "mapa_destino": mapa,
            "tipo": "hidden_flag", "tem": [], "tamanho": n,
            "bloqueio": "nenhum" if flag in com_cena else
                        f"{flag} não existe aqui; trazer o objeto sem a cena que "
                        "a apaga planta bloqueio permanente",
            "status": "feita" if (flag in com_cena and mapa in ja_postos)
                      else "pendente",
        })
    for (mapa, var, script), n in sorted(gat.items()):
        itens.append({
            "regiao": "sinnoh", "id": f"{mapa}:coord:{var}:{script}",
            "mapa_destino": mapa, "tipo": "coord_event", "tem": [],
            "tamanho": n,
            "bloqueio": "nenhum" if var in conhecidas else
                        f"{var} não existe nesta ROM, e o script da fonte é "
                        "índice de narc, não rótulo",
            "status": "pendente",
        })
    return itens


# ------------------------------------------------------------------- johto

def existe(simbolo, arquivos=("include/constants/items.h",
                              "include/constants/event_objects.h",
                              "include/constants/opponents.h")):
    for a in arquivos:
        p = os.path.join(REPO, a)
        if os.path.exists(p) and re.search(rf"\b{simbolo}\b", open(p).read()):
            return True
    return False


def ids_livres_johto():
    """Quanto sobra da faixa 2460-2499, que `opponents.h` reserva para Johto."""
    p = os.path.join(REPO, "include/constants/opponents.h")
    usados = {int(n) for n in re.findall(r"^#define\s+TRAINER_\w+\s+(\d+)\s*$",
                                         open(p).read(), re.M)}
    return sorted(set(range(2460, 2500)) - usados)


# A seção 6 de PENDENCIAS-JOHTO.md, item a item. `bloqueio` é RECALCULADO contra
# o repo por `fila_johto()`; o texto aqui é só o motivo escrito lá.
JOHTO = [
    dict(id="johto:arco_dos_sinos:kimono_girls", tipo="duelo",
         mapa_destino="EcruteakCity_DanceTheater", tamanho=5,
         precisa=["ITEM_TIDAL_BELL", "ITEM_CLEAR_BELL"],
         motivo="5 batalhas das Kimono Girls; o presente que fecha o desafio é "
                "um dos dois sinos"),
    dict(id="johto:arco_dos_sinos:lugia_hooh", tipo="arco_sinos",
         mapa_destino="TinTower_Roof / WhirlIslands_LugiaChamber", tamanho=5,
         precisa=["ITEM_TIDAL_BELL", "ITEM_CLEAR_BELL"],
         motivo="cadeia Route39 -> EcruteakCity -> Trigger_Silver -> teatro -> "
                "torre; o fim do arco lendário"),
    dict(id="johto:duelo:eusine_suicune", tipo="duelo",
         mapa_destino="Johto (cena de EUSINE)", tamanho=1, precisa=[],
         motivo="duelo de cena"),
    dict(id="johto:duelo:giovanni_celebi", tipo="duelo",
         mapa_destino="Johto (cena de GIOVANNI)", tamanho=1, precisa=[],
         motivo="duelo de cena"),
    dict(id="johto:duelo:red2_mt_silver", tipo="duelo",
         mapa_destino="MtSilver", tamanho=1, precisa=["__RED_2_SPRITE__"],
         motivo="OBJ_EVENT_GFX_RED já é o rival de Johto (seção 3); RED_2 não "
                "tem sprite próprio honesto"),
    dict(id="johto:duelo:grunt_subterraneo", tipo="duelo",
         mapa_destino="GoldenrodCity_Underground", tamanho=1, precisa=[],
         motivo="duelo de cena"),
    dict(id="johto:rival:4o_duelo", tipo="duelo",
         mapa_destino="GoldenrodCity_UndergroundSwitches", tamanho=1,
         precisa=[],
         motivo="mapa e vaga de objeto (índice 6, em 35,2) já existem; sai por "
                "flag, sem apagar objeto"),
    dict(id="johto:ginasio:whitney", tipo="setscene",
         mapa_destino="GoldenrodCity_Gym", tamanho=1, precisa=[],
         motivo="autocontida na fonte (põe VAR_GOLDENROD_CITY_STATE em 3); "
                "custa reescrever ginásio que hoje funciona"),
    dict(id="johto:ginasio:olivine", tipo="setscene",
         mapa_destino="OlivineCity_Gym", tamanho=1, precisa=[],
         motivo="depende de VAR_OLIVINE_CITY_STATE em 5, que só o farol põe"),
    dict(id="johto:npcs:44_pares_ambiguos", tipo="portavel",
         mapa_destino="vários", tamanho=44, precisa=[],
         motivo="duas coisas da fonte na mesma coordenada; restaura_npcs_johto.py "
                "recusa de propósito, resolver exige tabela à mão"),
    dict(id="johto:npcs:8_sem_par", tipo="portavel",
         mapa_destino="vários", tamanho=8, precisa=[],
         motivo="sem par na fonte; mesma tabela à mão"),
    dict(id="johto:arte:4_graficos", tipo="portavel",
         mapa_destino="vários", tamanho=4, precisa=[],
         motivo="TRAIN_FRONT, SHINY_GYARADOS e dois WHIRLPOOL; o GYARADOS tem "
                "saída barata em OBJ_EVENT_GFX_SPECIES_SHINY(GYARADOS)"),
    dict(id="johto:torres_farol:18_treinadores", tipo="batalha",
         mapa_destino="SproutTower / BurnedTower / OlivineCity_Lighthouse",
         tamanho=18, precisa=["__IDS_JOHTO__"],
         motivo="seção 4.1: 18 TRAINER_* sem id desde 05/08. O 'zero vaga' de lá "
                "ENVELHECEU: medido em 15/08/2026, a faixa reservada 2462-2499 "
                "está inteira livre (38 ids) e MAX_TRAINERS_COUNT_EMERALD é 4000 "
                "contra 2522 de maior id usado, então não sobe teto nem mexe no "
                "saveblock"),
]


def fila_johto():
    livres = ids_livres_johto()
    itens = []
    for j in JOHTO:
        faltando = []
        for s in j["precisa"]:
            if s == "__RED_2_SPRITE__":
                faltando.append("RED_2 sem sprite próprio (decisão de arte)")
            elif s == "__IDS_JOHTO__":
                if len(livres) < j["tamanho"]:
                    faltando.append(f"faixa 2462-2499: só {len(livres)} ids livres")
            elif not existe(s):
                faltando.append(f"{s} não existe nesta ROM")
        itens.append({
            "regiao": "johto", "id": j["id"], "mapa_destino": j["mapa_destino"],
            "tipo": j["tipo"], "tem": [], "tamanho": j["tamanho"],
            "bloqueio": "; ".join(faltando) if faltando else "nenhum",
            "status": "pendente", "motivo": j["motivo"],
        })
    return itens, livres


# ------------------------------------------------------- o que já foi feito

# A leva de 12/08/2026, para a fila não repropor trabalho fechado. Cada linha
# aponta a ferramenta que a fechou, que é onde se confere.
FEITAS = [
    dict(regiao="sinnoh", id="sinnoh:galactica:10_cenas",
         mapa_destino="MtCoronet, GalacticHQ, Eterna, Celestic, Route218, "
                      "LakeVerity, LakeAcuity, CanalaveCity, Route210_South, "
                      "Route212_South",
         tipo="hidden_flag", tamanho=13,
         bloqueio="nenhum", status="feita",
         motivo="dev_scripts/cena_galactica_sinnoh.py: 3 CENAS + 5 ROTEIRO + "
                "2 HORARIO, 12 treinadores escondidos e 1 grunt mudo"),
    dict(regiao="unova", id="unova:juniper_campea", mapa_destino="Unova (Liga)",
         tipo="batalha", tamanho=1, bloqueio="nenhum", status="feita",
         motivo="fim de Unova fechado em 12/08/2026"),
    dict(regiao="johto", id="johto:teatro_ecruteak",
         mapa_destino="EcruteakCity_DanceTheater", tipo="setscene", tamanho=1,
         bloqueio="nenhum", status="feita",
         motivo="dev_scripts/porta_cenas_johto.py, leva de 12/08/2026"),
    dict(regiao="johto", id="johto:18_heal_locations", mapa_destino="vários",
         tipo="portavel", tamanho=18, bloqueio="nenhum", status="feita",
         motivo="18 heal locations da leva de 12/08/2026"),
]


# --------------------------------------------------------------------- main

def gera():
    unova, chamadas = fila_unova()
    sinnoh = fila_sinnoh()
    johto, livres = fila_johto()
    itens = unova + sinnoh + johto + [dict(tem=[], **f) for f in FEITAS]
    return itens, chamadas, livres


def resumo(itens, chamadas, livres):
    print(f"{'região':8} {'tipo':20} {'pend.':>6} {'feitas':>6} {'linhas':>8}")
    conta = collections.Counter()
    for i in itens:
        conta[(i["regiao"], i["tipo"], i["status"])] += 1
    tam = collections.Counter()
    for i in itens:
        tam[(i["regiao"], i["tipo"])] += i["tamanho"]
    for reg, tipo in sorted({(r, t) for r, t, _ in conta}):
        print(f"{reg:8} {tipo:20} {conta[(reg, tipo, 'pendente')]:6} "
              f"{conta[(reg, tipo, 'feita')]:6} {tam[(reg, tipo)]:8}")
    pend = [i for i in itens if i["status"] == "pendente"]
    print(f"\npendentes: {len(pend)}   sem bloqueio: "
          f"{sum(1 for i in pend if i['bloqueio'] == 'nenhum')}")
    print("chamadas alcançadas em Unova:", dict(chamadas))
    print(f"ids de treinador livres na faixa 2460-2499: {len(livres)} "
          f"({livres[0]}-{livres[-1]})" if livres else "faixa 2460-2499 cheia")


def grava(itens):
    linhas = ",\n".join(json.dumps(i, ensure_ascii=False, sort_keys=True)
                        for i in itens)
    open(SAIDA, "w", encoding="utf-8").write("[\n" + linhas + "\n]\n")
    print("escrito:", SAIDA, f"({len(itens)} linhas)")


def demo():
    """Autoteste: o que quebraria calado se a travessia parasse de andar."""
    corpos, std = indice_de_rotulos()
    assert len(corpos) > 20000, len(corpos)
    assert std, "std_scripts.asm não foi lido; jumpstd morreria calado"

    unova, chamadas = fila_unova()
    assert len(unova) == 209, f"cenas de Unova: {len(unova)} (esperado 209)"
    # A trava do bug que este arquivo existe para não repetir: sem seguir a
    # cadeia, `callasm` aparece 8 vezes em 5 arquivos e a fila diria 8.
    ca = sum(1 for i in unova if "callasm" in i["tem"])
    assert ca == 16, f"cenas que chegam a callasm: {ca} (esperado 16)"
    cb = sum(1 for i in unova if "changeblock" in i["tem"])
    assert cb == 107, f"cenas de changeblock: {cb} (esperado 107)"
    assert chamadas["changeblock"] > 1000, chamadas["changeblock"]

    sinnoh = fila_sinnoh()
    obj = sum(i["tamanho"] for i in sinnoh if i["tipo"] == "hidden_flag")
    tri = sum(i["tamanho"] for i in sinnoh if i["tipo"] == "coord_event")
    assert obj == 371, f"objetos com hidden_flag: {obj} (esperado 371)"
    assert tri == 177, f"coord_events de Sinnoh: {tri} (esperado 177)"
    # Nenhuma das 70 vars do Platinum existe aqui: gatilho sem bloqueio seria
    # sinal de que `vars_do_repo()` casou por engano.
    assert all(i["bloqueio"] != "nenhum" for i in sinnoh
               if i["tipo"] == "coord_event")

    johto, livres = fila_johto()
    assert len(livres) == 38, f"ids livres em 2460-2499: {len(livres)}"
    sinos = [i for i in johto if "sinos" in i["id"] or "kimono" in i["id"]]
    assert all("TIDAL_BELL" in i["bloqueio"] for i in sinos), sinos
    print("demo ok:", len(unova), "cenas de Unova,", len(sinnoh),
          "unidades de Sinnoh,", len(johto), "itens de Johto")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        itens, chamadas, livres = gera()
        resumo(itens, chamadas, livres)
        if "--gravar" in sys.argv:
            grava(itens)
        else:
            print("\nnada escrito (use --gravar)")
