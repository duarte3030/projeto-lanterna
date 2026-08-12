#!/usr/bin/env python3
"""Inventário por região e por mapa, medido CONTRA A FONTE, gerando INVENTARIO.md.

    python3 dev_scripts/inventario.py           # escreve INVENTARIO.md na raiz
    python3 dev_scripts/inventario.py --resumo  # só o resumo na tela
    python3 dev_scripts/inventario.py --demo    # asserts

Bloco B0 do `PRD-ROM-COMPLETA.md`. Existe porque o projeto já errou várias vezes
por confiar em número escrito à mão em documento. Aqui **nada é escrito à mão**:
cada linha sai de um arquivo da fonte, e o caminho desse arquivo vai impresso na
própria linha, para que qualquer número possa ser conferido abrindo o arquivo.

## A régua: "existe" nunca é a mesma coluna que "tem conteúdo"

Esta é a lição que custou caro (`completude.py` deu 98% para Unova, que é maquete
de colisão). `completude.py` conta PRESENÇA: mapa existe, objeto existe, placa
existe. Presença é barata de fabricar e não é jogo.

Por isso toda medida aqui sai em duas colunas:

    existe            tem conteúdo
    ------            ------------
    pessoa            pessoa com fala
    placa             placa com texto próprio
    treinador         treinador com time em trainers.party
    mapa              (não se aplica; mapa é medido pelas outras colunas)

Mudo é contado em dois baldes, porque a diferença muda o trabalho:

- **sem script**: o campo `script` do objeto é `"0"`. Ninguém escreveu nada.
- **script sem texto**: existe rótulo, mas o corpo dele não tem comando de
  texto. Parte disso é legítima (balconista chama a rotina de loja, enfermeira
  chama a de cura) e parte é NPC pela metade. O inventário não decide qual é
  qual; ele separa o balde para que a decisão seja tomada olhando o caso.

## De onde sai cada número, por geração

O formato de fonte muda por geração e nenhum deles é reescrito aqui: este
arquivo reusa os leitores que os outros scripts do repo já provaram.

- **gen 3 decomp** (Kanto/pokefirered, Johto/hns, Hoenn/pokeemerald, e o nosso
  próprio repo): `data/maps/<Mapa>/map.json` para os eventos e
  `data/maps/<Mapa>/scripts.inc` mais `data/scripts/*.inc` para os rótulos.
  Casamento de nome por `completude.normaliza`.
- **gen 4** (Sinnoh/pokeplatinum): `include/data/map_headers.h` liga o
  MAP_HEADER ao `events_*.json`, ao `scripts_*.s` e ao `encounters_*.json`.
  Leitores reusados de `importa_npcs_sinnoh` (`headers_do_platinum`, `chave`,
  `APELIDOS`, `GRAFICOS_*`), `texto_placas_sinnoh` (`entradas_de_script`) e
  `texto_sinnoh` (`MOSTRA`, `CRY`, `ITEM_ESCONDIDO`). Treinador na fonte é
  objeto cujo `script` é a string `TRAINER_*`, achado de
  `treinadores_rota_sinnoh.py`.
- **gen 2 asm** (Unova/bw3g): `maps/<Mapa>.asm`, com `object_event`, `bg_event`
  e `warp_event` como macro. Treinador é `OBJECTTYPE_TRAINER`, que é o mesmo
  critério de `gera_treinadores_unova.le_objetos`.

## Quatro medidas erradas que este arquivo cometeu e como cada uma foi pega

Ficam registradas porque a próxima versão vai ser tentada a repetir todas:

1. **Régua que reprova o vanilla.** Contar "NPC mudo" contra zero dava 795
   mudos em HOENN, que é o pokeemerald intocado. Lacuna é sempre `nosso menos
   fonte`, mapa a mapa.
2. **Comando renomeado pelo expansion.** `braillemessage` virou `braillemsgbox`
   e `trainerbattle` do Frontier virou `facilitytrainerbattle`. Nos dois casos o
   texto está lá e o inventário dizia que não.
3. **Fala que não usa `msgbox`.** Treinador de gen 3 passa a fala como argumento
   do `trainerbattle`, e o de gen 4 guarda em `res/trainers`. Sem isso, os 360
   treinadores de Unova saíam mudos e a fila inventava 328 falas a escrever.
4. **Sufixo de região quebrando a comparação de nome.** `CeruleanCity_Frlg` com
   rótulo `CeruleanCity_BikeShop_EventScript_Bicycle`: a MESMA placa contava
   como própria na fonte e genérica aqui, inventando 31 placas de dívida.

Todas as quatro apareceram como número alto numa região que não deveria ter
dívida, e todas foram fechadas abrindo UM caso à mão. Número que só piora numa
região intocada é defeito de régua, não trabalho a fazer.

## O que NÃO é medido aqui, de propósito

Desenho de mapa (`blockdata`). Esse é o buraco de Unova e ele já tem medida
própria em `completude.py` e no bloco B12; medir de novo aqui só duplicaria
número. O inventário mede POVOAMENTO e CONTEÚDO ESCRITO.

Teto conhecido: "tem fala" é uma pergunta de sim ou não sobre o script chegar a
um comando de texto. Ela não julga se a fala é BOA nem se é a fala da fonte.
Placa com texto próprio idem: mede que o texto é daquele mapa, não que ele diz a
coisa certa.

Idempotente: só lê o repo e as fontes, e reescreve `INVENTARIO.md` inteiro.
Nenhum arquivo do jogo é tocado.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(os.path.dirname(RAIZ), "fontes-mapas")
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import completude as C           # noqa: E402  normaliza(), nossos_da_regiao()
import importa_npcs_sinnoh as I  # noqa: E402  headers_do_platinum(), APELIDOS
import texto_placas_sinnoh as TP  # noqa: E402  entradas_de_script()
import texto_sinnoh as TS        # noqa: E402  texto_do_rotulo()

SAIDA = os.path.join(RAIZ, "INVENTARIO.md")

# ---------------------------------------------------------------- pessoa

# Objeto de mapa que NÃO é gente, com o nome já sem o prefixo `OBJ_EVENT_GFX_`.
#
# ARMADILHA que `importa_npcs_sinnoh.py` documentou e que eu confirmei medindo:
# comparar por substring contra o nome INTEIRO faz "VENT" casar com
# "OBJ_EVENT_GFX_ACE_TRAINER_F" (e-VENT-o) e joga o mapa inteiro no lixo. Aqui a
# comparação é por PALAVRA: o nome é quebrado no `_` e o pedaço tem que ser igual
# ao token, então "ROCK" pega `ROCK_SMASH_ROCK` e `BREAKABLE_ROCK` mas não pega
# `ROCKER` nem `ROCKET_M`, que são gente.
#
# `MON_BASE+SPECIES_*` e `LIGHT_SPRITE` existem só no hns: são o Pokémon andando
# no overworld e o efeito de luz. Contar os 1390 Pokémon do hns como "pessoas de
# Johto que faltam" inventaria uma dívida que não existe.
TOKENS_NAO_PESSOA = frozenset("""
BALL ROCK TREE BOULDER TRUCK DOLL CUSHION FOSSIL AMBER METEORITE MAP POKEDEX
BAG STATUE SHADOW BOAT SEAGALLOP CLIPBOARD TRIANGLE SPRITE
""".split())
EXATOS_NAO_PESSOA = frozenset({"CABLE_CAR", "MOVING_BOX"})


def eh_pessoa_gen3(gfx):
    c = (gfx or "").replace("OBJ_EVENT_GFX_", "")
    if c in EXATOS_NAO_PESSOA or c.startswith(("SS_", "MON_BASE")):
        return False
    return not (set(c.split("_")) & TOKENS_NAO_PESSOA)


def eh_pessoa_gen4(gfx):
    """Mesma pergunta no vocabulário do Platinum, com os leitores já existentes.

    Reusa as duas listas de `importa_npcs_sinnoh`: mobiliário (canteiro de
    berry, respiradouro, pedra de Strength) e placa. Elas são substring, mas só
    depois de tirar o prefixo comum, que é o cuidado que o arquivo original
    documenta.
    """
    c = (gfx or "").replace("OBJ_EVENT_GFX_", "")
    return not any(t in c for t in I.GRAFICOS_PROIBIDOS + I.GRAFICOS_PLACA)


# ---------------------------------------------------- rótulos de script gen 3

# Todo comando desta build que põe texto na tela. `msgbox` cobre as variantes
# geradas por macro (`msgbox_npc` e afins) porque a checagem é por prefixo.
#
# `trainerbattle` está aqui e o motivo custou uma medida errada: em gen 3 o
# treinador não usa `msgbox`, ele passa os ponteiros de fala como ARGUMENTO
# (`trainerbattle_single TRAINER_X, Text_Visto, Text_Derrotado`). Sem esta
# alternativa, os 360 treinadores de Unova saíam como mudos e a fila de trabalho
# inventava 328 falas a escrever que já estão escritas. Conferido à mão em
# `data/maps/Unova_CelestialTower/scripts.inc` em 12/08/2026.
# O prefixo livre em `[a-z_]*trainerbattle` também não é enfeite: o expansion
# renomeou o comando do Battle Frontier para `facilitytrainerbattle`, e sem ele
# as 78 batalhas das salas da Pirâmide apareciam como fala perdida em HOENN, que
# é a região intocada. Régua que reprova o vanilla está errada, lição 4.10.
# `braille\w*` pelo mesmo motivo: o expansion trocou `braillemessage` por
# `braillemsgbox`, e as 26 pedras em braile de `MtEmber_RubyPath_B4F` viravam
# placa sem texto num mapa que é cópia byte a byte do pokefirered.
TEM_TEXTO = re.compile(
    r"^\s*(msgbox|message|braille\w*|vmessage|multichoice|[a-z_]*trainerbattle"
    r"|showpokemonpic|bufferstring\w*|preparemsg)", re.M)
# Desvio incondicional ou chamada: o texto pode estar no rótulo de destino.
SEGUE = re.compile(r"^\s*(?:goto|call|goto_if\w*|call_if\w*)\s+([A-Za-z_]\w*)", re.M)


def indice_rotulos(raiz):
    """rótulo -> corpo (o texto até o próximo rótulo), de todo .inc de um repo.

    Um índice global, e não um por mapa, porque metade das placas do jogo aponta
    para rótulo compartilhado (`Common_EventScript_ShowPokemonCenterSign` mora em
    `data/scripts/`). Índice por mapa contaria essas placas como genéricas e a
    coluna mentiria para baixo.
    """
    corte = re.compile(r"^([A-Za-z_]\w*)::?\s*$", re.M)
    idx = {}
    for p in glob.glob(f"{raiz}/data/**/*.inc", recursive=True):
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                s = f.read()
        except OSError:
            continue
        marcas = list(corte.finditer(s))
        for n, m in enumerate(marcas):
            fim = marcas[n + 1].start() if n + 1 < len(marcas) else len(s)
            idx[m.group(1)] = s[m.end():fim]
    return idx


def fala_gen3(rotulo, idx, visto=None, prof=0):
    """O rótulo (ou algum destino dele) chega a pôr texto na tela?"""
    if not rotulo or rotulo in ("0", "0x0") or prof > 4:
        return False
    visto = visto if visto is not None else set()
    if rotulo in visto:
        return False
    visto.add(rotulo)
    corpo = idx.get(rotulo)
    if corpo is None:
        return False
    if TEM_TEXTO.search(corpo):
        return True
    return any(fala_gen3(d, idx, visto, prof + 1) for d in SEGUE.findall(corpo))


TRAINERBATTLE = re.compile(r"^\s*trainerbattle\w*\s+(TRAINER_\w+)", re.M)


def treinadores_do_scripts_inc(caminho):
    if not os.path.exists(caminho):
        return set()
    with open(caminho, encoding="utf-8", errors="replace") as f:
        return set(TRAINERBATTLE.findall(f.read()))


def times_declarados():
    """TRAINER_* que tem bloco `=== TRAINER_X ===` em .party COMPILADO.

    Só `trainers.party` e `trainers_frlg.party` viram .h (ver
    `trainer_rules.mk`); `trainers_johto.party` e `trainers_sinnoh.party` são
    acervo e NÃO estão na ROM. Contar o acervo daria treinador que não existe.
    """
    fora = set()
    for nome in ("trainers.party", "trainers_frlg.party"):
        p = os.path.join(RAIZ, "src/data", nome)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as f:
            fora |= set(re.findall(r"^===\s*(TRAINER_\w+)\s*===", f.read(), re.M))
    return fora


# ---------------------------------------------------------------- encontros

def mapas_com_encontro(caminho_json):
    """MAP_* que têm tabela de encontro selvagem num wild_encounters.json."""
    if not os.path.exists(caminho_json):
        return set()
    d = json.load(open(caminho_json))
    return {e["map"] for g in d.get("wild_encounter_groups", [])
            if g.get("for_maps") for e in g.get("encounters", [])
            if any(k.endswith("_mons") for k in e)}


# ---------------------------------------------------------------- gen 3

def placas_por_rotulo(raiz):
    """rótulo de placa -> em quantos mapas DIFERENTES daquele repo ele é usado.

    É o que separa "texto próprio" de "placa genérica" sem lista escrita à mão.
    `Sinnoh_EventScript_PlacaImportada` aparece em 101 mapas e é o rótulo único
    que o importador deixou; `EventScript_BookShelf` aparece em 99 e é estante
    compartilhada do vanilla. Os dois são genéricos pelo MESMO motivo, e a fonte
    é medida com a mesma régua, então estante compartilhada não conta a favor de
    ninguém dos dois lados.
    """
    conta = defaultdict(set)
    for p in glob.glob(f"{raiz}/data/maps/*/map.json"):
        mapa = os.path.basename(os.path.dirname(p))
        try:
            d = json.load(open(p))
        except (OSError, ValueError):
            continue
        for b in d.get("bg_events") or []:
            if b.get("script"):
                conta[str(b["script"])].add(mapa)
    return {k: len(v) for k, v in conta.items()}


DONO_DO_ROTULO = re.compile(r"_(?:EventScript|MapScript|Text|Movement)_")


def rotulo_do_mapa(rotulo, mapa):
    """O rótulo foi escrito PARA este mapa (ou para um irmão de mesmo prédio)?

    A comparação passa por `completude.normaliza` porque o nosso mapa carrega
    sufixo de região e o da fonte não: `CeruleanCity_Frlg` e o rótulo
    `CeruleanCity_BikeShop_EventScript_Bicycle` são a mesma cidade, e comparar a
    grafia crua fazia a MESMA placa contar como própria no pokefirered e como
    genérica aqui, inventando 31 placas de dívida em Kanto (conferido à mão em
    `CeruleanCity_Frlg` em 12/08/2026, onde os dois `map.json` são idênticos).
    """
    dono = DONO_DO_ROTULO.split(rotulo)[0]
    a, b = C.normaliza(dono), C.normaliza(mapa)
    return bool(a) and (a.startswith(b) or b.startswith(a))


def le_gen3(raiz, mapa, idx, compartilhadas):
    """Uma linha de inventário para um mapa de repo decomp de gen 3."""
    pj = f"{raiz}/data/maps/{mapa}/map.json"
    if not os.path.exists(pj):
        return None
    d = json.load(open(pj))
    pessoas = [o for o in (d.get("object_events") or [])
               if eh_pessoa_gen3(o.get("graphics_id"))]
    sem_script = [o for o in pessoas if str(o.get("script", "0")) in ("0", "0x0")]
    com_fala = [o for o in pessoas if fala_gen3(str(o.get("script", "0")), idx)]
    placas = [b for b in (d.get("bg_events") or []) if b.get("script")]
    # "Texto próprio" = o rótulo é DESTE mapa (o nome do mapa abre o rótulo) ou
    # não é dividido com nenhum outro mapa. As duas condições porque nenhuma
    # sozinha basta:
    #  - só "não dividido" reprovaria a estante do laboratório do Birch, que é
    #    texto escrito para Hoenn e que o `NewBarkTown_Lab` de Johto passou a
    #    reusar. O empréstimo é dívida de Johto, não de Hoenn, e sem esta regra
    #    o inventário cobrava do mapa errado (conferido à mão em 12/08/2026).
    #  - só "abre com o nome do mapa" deixaria passar rótulo compartilhado de
    #    câmara de Ruins of Alph e a placa importada de Sinnoh.
    placas_txt = [b for b in placas
                  if (rotulo_do_mapa(str(b["script"]), mapa)
                      or compartilhadas.get(str(b["script"]), 9) == 1)
                  and fala_gen3(str(b["script"]), idx)]
    return {
        "id": d.get("id"),
        "arquivo": f"data/maps/{mapa}/map.json",
        "objetos": len(d.get("object_events") or []),
        "pessoas": len(pessoas),
        "sem_script": len(sem_script),
        "com_fala": len(com_fala),
        "placas": len(placas),
        "placas_txt": len(placas_txt),
        "treinadores": treinadores_do_scripts_inc(f"{raiz}/data/maps/{mapa}/scripts.inc"),
    }


# ---------------------------------------------------------------- gen 4

def headers_plat():
    """MAP_HEADER_* -> campos que este inventário usa, lidos de uma vez só.

    `importa_npcs_sinnoh.headers_do_platinum()` já devolve eventos e matriz, mas
    não o arquivo de scripts nem o de encontros, e este inventário precisa dos
    quatro. Ler o mesmo arquivo uma vez é mais barato que quatro regex separadas.
    """
    txt = open(os.path.join(I.PLAT, "include/data/map_headers.h")).read()
    fora = {}
    for bloco in re.finditer(r"\[(MAP_HEADER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},",
                             txt, re.S):
        corpo = bloco.group(2)

        def campo(n):
            m = re.search(rf"\.{n}\s*=\s*(\w+)", corpo)
            return m.group(1) if m else None
        ev = campo("eventsArchiveID")
        if ev and ev.startswith("events_"):
            fora[bloco.group(1)] = {"eventos": ev, "scripts": campo("scriptsArchiveID"),
                                    "encontros": campo("wildEncountersArchiveID")}
    return fora


GOTO_GEN4 = re.compile(r"^GoTo\w*\s+(?:\w+,\s*)*(\w+)\s*$")


def fala_gen4(rot, corpos, visto=None, prof=0):
    """O rótulo do Platinum chega a pôr texto na tela?

    `texto_sinnoh.texto_do_rotulo` existe e faz quase isto, mas de propósito só
    segue o caminho de fall-through: lá o alvo é a fala PADRÃO, a que vai virar
    `.string`. Aqui a pergunta é outra e mais larga: "esta pessoa fala alguma
    coisa?". Seguir também o desvio condicional é o que deixa esta coluna
    comparável com a de gen 3, que varre o corpo inteiro do rótulo. Sem isso o
    denominador de Sinnoh sai baixo e o inventário diz que temos MAIS fala que o
    Platinum, o que seria o mesmo tipo de mentira que este arquivo existe para
    matar.
    """
    if not rot or prof > 4:
        return False
    visto = visto if visto is not None else set()
    if rot in visto:
        return False
    visto.add(rot)
    corpo = corpos.get(rot)
    if corpo is None:
        return False
    alvos = []
    for linha in corpo:
        if TS.MOSTRA.match(linha) or TS.CRY.match(linha):
            return True
        m = GOTO_GEN4.match(linha)
        if m:
            alvos.append(m.group(1))
    return any(fala_gen4(a, corpos, visto, prof + 1) for a in alvos)


def le_gen4(hdr):
    pe = os.path.join(I.PLAT, "res/field/events", hdr["eventos"] + ".json")
    if not os.path.exists(pe):
        return None
    d = json.load(open(pe))
    objs = d.get("object_events") or []
    pessoas = [o for o in objs if eh_pessoa_gen4(o.get("graphics_id"))]
    treinadores = {o["script"] for o in objs
                   if isinstance(o.get("script"), str) and o["script"].startswith("TRAINER_")}
    placas = [o for o in objs
              if any(t in (o.get("graphics_id") or "").replace("OBJ_EVENT_GFX_", "")
                     for t in I.GRAFICOS_PLACA)]
    # Placa e item escondido moram no MESMO array `bg_events` no Platinum e só
    # se distinguem pela faixa do `script`: 8000 a 8799 é item escondido
    # (`SCRIPT_ID_OFFSET_HIDDEN_ITEMS`). Contar item escondido como placa é o
    # defeito que `texto_sinnoh.py` documenta e que já inflou a coluna uma vez.
    placas += [b for b in (d.get("bg_events") or [])
               if not isinstance(b.get("script"), int)
               or b["script"] not in TS.ITEM_ESCONDIDO]

    ordem, corpos = ([], {})
    if hdr["scripts"]:
        ordem, corpos = TP.entradas_de_script(hdr["scripts"])

    def tem_fala(e):
        i = e.get("script")
        # Treinador de gen 4 fala, e a fala dele NÃO mora no banco de texto do
        # mapa: mora junto com o time, em `res/trainers/data/<slug>.json`, campo
        # `messages` (achado de `treinadores_rota_sinnoh.py`). Contar o objeto de
        # treinador como mudo faria o Platinum parecer ter menos fala que nós,
        # que é exatamente o tipo de resultado bom demais que este arquivo
        # existe para desconfiar.
        if isinstance(i, str) and i.startswith("TRAINER_"):
            return True
        if not isinstance(i, int) or not (1 <= i <= len(ordem)):
            return False
        return fala_gen4(ordem[i - 1], corpos)

    enc = hdr["encontros"]
    pe_enc = os.path.join(I.PLAT, "res/field/encounters", f"{enc}.json") if enc else None
    tem_enc = False
    if pe_enc and os.path.exists(pe_enc):
        e = json.load(open(pe_enc))
        tem_enc = any(e.get(k) for k in ("land_rate", "surf_rate", "old_rod_rate",
                                         "good_rod_rate", "super_rod_rate"))
    return {
        "arquivo": f"res/field/events/{hdr['eventos']}.json",
        "objetos": len(objs),
        "pessoas": len(pessoas),
        "sem_script": 0,
        "com_fala": sum(1 for o in pessoas if tem_fala(o)),
        "placas": len(placas),
        "placas_txt": sum(1 for o in placas if tem_fala(o)),
        "treinadores": treinadores,
        "encontro": tem_enc,
    }


# ---------------------------------------------------------------- gen 2

RE_OBJ = re.compile(
    r"^\s*object_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+),\s*(-?\d+),"
    r"\s*(-?\d+),\s*(-?\w+),\s*(-?\w+),\s*(\w+),\s*OBJECTTYPE_(\w*),"
    r"\s*(-?\w+),\s*(\w+)", re.M)
RE_BG = re.compile(r"^\s*bg_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+)", re.M)
# Cenário que o gen 2 declara como `OBJECTTYPE_SCRIPT` e que não é gente. Os 12
# `SPRITE_CABLE` da ponte de Driftveil são o cabo da ponte, e o importador já os
# trouxe como `TRICK_HOUSE_STATUE` (mobília) aqui: sem esta lista o inventário
# cobrava 12 pessoas que nunca existiram. Conferido à mão em
# `bw3g/maps/DriftveilDrawbridge.asm` em 12/08/2026.
CENARIO_GEN2 = frozenset("""
SPRITE_POKE_BALL SPRITE_BOULDER SPRITE_CABLE SPRITE_FRUIT_TREE SPRITE_FOSSIL
SPRITE_DOLL_1 SPRITE_DOLL_2 SPRITE_BIG_DOLL
""".split())
# Comando de gen 2 que põe texto na tela.
TEM_TEXTO_GEN2 = re.compile(r"^\s*(jumptext|jumptextfaceplayer|writetext"
                            r"|farwritetext|farjumptext|special\s+MapRadio)", re.M)
SEGUE_GEN2 = re.compile(r"^\s*(?:sjump|jump|callasm|scall|farsjump)\s+(\w+)", re.M)
# `jumpstd difficultbookshelf` cai em `DifficultBookshelfScript`, que mora em
# engine/events/std_scripts.asm e não no .asm do mapa. Sem seguir isso, as 13
# estantes, os 18 balcões de Centro Pokémon e as 26 prateleiras de revista de
# Unova saíam como "placa sem texto", e a coluna mentia para baixo.
JUMPSTD = re.compile(r"^\s*jumpstd\s+(\w+)", re.M)


def corpos_gen2(asm):
    """rótulo -> corpo, num .asm de mapa de pokecrystal."""
    corte = re.compile(r"^(\w+):+\s*$", re.M)
    marcas = list(corte.finditer(asm))
    fora = {}
    for n, m in enumerate(marcas):
        fim = marcas[n + 1].start() if n + 1 < len(marcas) else len(asm)
        fora[m.group(1)] = asm[m.end():fim]
    return fora


def corpos_std_gen2(fonte):
    """Os rótulos de `jumpstd`, já com a chave em minúsculas do jeito que o
    mapa os cita (`difficultbookshelf` -> `DifficultBookshelfScript`)."""
    p = f"{fonte}/engine/events/std_scripts.asm"
    if not os.path.exists(p):
        return {}
    todos = corpos_gen2(open(p, encoding="utf-8", errors="replace").read())
    return {k[:-len("Script")].lower(): v for k, v in todos.items()
            if k.endswith("Script")}


def fala_gen2(rot, corpos, std=None, visto=None, prof=0):
    if not rot or rot == "-1" or prof > 3:
        return False
    std = std or {}
    visto = visto if visto is not None else set()
    if rot in visto:
        return False
    visto.add(rot)
    corpo = corpos.get(rot)
    if corpo is None:
        return False
    if TEM_TEXTO_GEN2.search(corpo):
        return True
    for nome in JUMPSTD.findall(corpo):
        if TEM_TEXTO_GEN2.search(std.get(nome.lower(), "")):
            return True
    return any(fala_gen2(d, corpos, std, visto, prof + 1)
               for d in SEGUE_GEN2.findall(corpo))


def le_gen2(fonte, mapa, com_encontro, std):
    p = f"{fonte}/maps/{mapa}.asm"
    if not os.path.exists(p):
        return None
    asm = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(rf"^{re.escape(mapa)}_MapEvents:", asm, re.M)
    trecho = asm[m.end():] if m else ""
    corpos = corpos_gen2(asm)
    objs = RE_OBJ.findall(trecho)
    pessoas = [o for o in objs
               if o[9] in ("SCRIPT", "TRAINER") and o[2] not in CENARIO_GEN2]
    treinadores = {f"{mapa}:{o[11]}" for o in objs if o[9] == "TRAINER"}
    # BGEVENT_ITEM é item escondido, não placa.
    placas = [b for b in RE_BG.findall(trecho) if b[2] != "BGEVENT_ITEM"]
    return {
        "arquivo": f"maps/{mapa}.asm",
        "objetos": len(objs),
        "pessoas": len(pessoas),
        "sem_script": sum(1 for o in pessoas if o[11] in ("-1", "0")),
        "com_fala": sum(1 for o in pessoas if fala_gen2(o[11], corpos, std)),
        "placas": len(placas),
        # `std` de propósito FORA daqui: placa que só fala por `jumpstd` é a
        # estante padrão do motor, texto compartilhado por dezenas de mapas, e
        # entra como genérica pelo mesmo critério que separa genérica de própria
        # no gen 3. Para o NPC acima ela conta, porque lá a pergunta é "fala?".
        "placas_txt": sum(1 for b in placas if fala_gen2(b[3], corpos)),
        "treinadores": treinadores,
        "encontro": chave_simples(mapa) in com_encontro,
    }


def chave_simples(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def encontros_gen2(fonte):
    """Nomes de mapa (normalizados) que aparecem em `map_id` nos data/wild/*.asm.

    `map_id R_22` cita a constante, e a constante mora em
    `constants/map_constants.asm` como `map_const R_22, w, h`. O arquivo do mapa
    é `maps/R22.asm`. As três grafias colapsam na mesma chave sem letra nem
    número perdido.
    """
    fora = set()
    for p in glob.glob(f"{fonte}/data/wild/*.asm"):
        with open(p, encoding="utf-8", errors="replace") as f:
            fora |= {chave_simples(x) for x in re.findall(r"^\s*map_id\s+(\w+)", f.read(), re.M)}
    return fora


# ---------------------------------------------------------------- regiões

def lista_sinnoh():
    return I.nossos_mapas_sinnoh()


def monta():
    """[(região, [linha, ...], avulsos)] com tudo já medido."""
    idx_nosso = indice_rotulos(RAIZ)
    comp_nosso = placas_por_rotulo(RAIZ)
    times = times_declarados()
    enc_nosso = mapas_com_encontro(os.path.join(RAIZ, "src/data/wild_encounters.json"))
    mg = C.todos_os_mapas(RAIZ)
    sinnoh = set(lista_sinnoh())

    regioes = []

    # --- Kanto, Johto, Hoenn: fonte decomp de gen 3 ----------------------
    for nome, chave_grupo, fonte in (
            ("Kanto", "Frlg", f"{FONTES}/pokefirered"),
            ("Johto", "Johto", f"{FONTES}/hns"),
            ("Hoenn", "TownsAndRoutes", f"{FONTES}/pokeemerald")):
        nossos = [m for m in C.nossos_da_regiao(mg, chave_grupo) if m not in sinnoh]
        idx_fonte = indice_rotulos(fonte)
        comp_fonte = placas_por_rotulo(fonte)
        enc_fonte = mapas_com_encontro(f"{fonte}/src/data/wild_encounters.json")
        deles = {C.normaliza(m): m for m in C.todos_os_mapas(fonte)}
        linhas = []
        for meu in sorted(nossos):
            seu = deles.get(C.normaliza(meu))
            a = le_gen3(RAIZ, meu, idx_nosso, comp_nosso)
            if a is None:
                continue
            b = le_gen3(fonte, seu, idx_fonte, comp_fonte) if seu else None
            linhas.append(linha(nome, meu, a, b, seu,
                                os.path.basename(fonte), times,
                                a["id"] in enc_nosso,
                                bool(b) and b["id"] in enc_fonte))
        ausentes = C.mapas_so_na_fonte(deles, mg, fonte)
        regioes.append((nome, os.path.basename(fonte), linhas, sorted(ausentes)))

    # --- Sinnoh: pokeplatinum (gen 4) ------------------------------------
    heads = headers_plat()
    por_chave = {}
    for h in heads:
        por_chave.setdefault(I.chave(h), h)
    linhas, casadas = [], set()
    for meu in sorted(sinnoh):
        h = I.APELIDOS.get(meu) or por_chave.get(I.chave(meu))
        h = h if h in heads else None
        a = le_gen3(RAIZ, meu, idx_nosso, comp_nosso)
        if a is None:
            continue
        b = le_gen4(heads[h]) if h else None
        if h:
            casadas.add(I.chave(h))
        linhas.append(linha("Sinnoh", meu, a, b, h, "pokeplatinum", times,
                            a["id"] in enc_nosso, bool(b) and b["encontro"]))
    ausentes = sorted(h for h in heads if I.chave(h) not in casadas)
    regioes.append(("Sinnoh", "pokeplatinum", linhas, ausentes))

    # --- Unova: bw3g (gen 2) ---------------------------------------------
    fonte = f"{FONTES}/bw3g"
    enc_fonte = encontros_gen2(fonte)
    std = corpos_std_gen2(fonte)
    deles = {C.normaliza(os.path.basename(p)[:-4]): os.path.basename(p)[:-4]
             for p in glob.glob(f"{fonte}/maps/*.asm")}
    nossos = [m for m in C.nossos_da_regiao(mg, "Unova") if m not in sinnoh]
    linhas, casadas = [], set()
    for meu in sorted(nossos):
        k = C.normaliza(meu)
        seu = deles.get(k)
        a = le_gen3(RAIZ, meu, idx_nosso, comp_nosso)
        if a is None:
            continue
        b = le_gen2(fonte, seu, enc_fonte, std) if seu else None
        if seu:
            casadas.add(k)
        linhas.append(linha("Unova", meu, a, b, seu, "bw3g", times,
                            a["id"] in enc_nosso, bool(b) and b["encontro"]))
    ausentes = sorted(m for k, m in deles.items()
                      if k not in casadas and not C.LIXO.search(m))
    regioes.append(("Unova", "bw3g", linhas, ausentes))
    return regioes


def linha(regiao, meu, a, b, seu, fonte, times, enc_n, enc_f):
    """Uma linha do inventário: o que existe aqui, o que a fonte tem, e a prova."""
    batalhaveis = {t for t in a["treinadores"] if t in times}
    return {
        "regiao": regiao, "mapa": meu, "par": seu,
        "prova": f"{fonte}/{b['arquivo']}" if b else None,
        "obj_n": a["objetos"], "obj_f": b["objetos"] if b else None,
        "pessoas_n": a["pessoas"], "pessoas_f": b["pessoas"] if b else None,
        "fala_n": a["com_fala"], "fala_f": b["com_fala"] if b else None,
        "sem_script_n": a["sem_script"],
        "mudo_n": a["pessoas"] - a["com_fala"],
        # ARMADILHA da lição 4.10 do ESTADO.md: régua tirada da cabeça reprova o
        # jogo original. O pokeemerald vanilla tem 779 pessoas mudas em Hoenn
        # (guarda de museu que só empurra, gente de cena de história), então
        # "795 mudos em Hoenn" não é dívida nenhuma. O que é dívida é o mudo que
        # a FONTE não tem, e é só isso que entra na fila de trabalho.
        "mudo_f": (b["pessoas"] - b["com_fala"]) if b else None,
        "trein_n": len(batalhaveis), "trein_cit_n": len(a["treinadores"]),
        "trein_f": len(b["treinadores"]) if b else None,
        "placas_n": a["placas"], "placas_f": b["placas"] if b else None,
        "placas_txt_n": a["placas_txt"], "placas_txt_f": b["placas_txt"] if b else None,
        "placa_gen_n": a["placas"] - a["placas_txt"],
        "placa_gen_f": (b["placas"] - b["placas_txt"]) if b else None,
        "enc_n": enc_n, "enc_f": enc_f,
    }


# ---------------------------------------------------------------- relatório

def soma(linhas, campo):
    return sum(l[campo] or 0 for l in linhas if l[campo] is not None)


def com_par(linhas):
    return [l for l in linhas if l["prova"]]


def falta(l, cn, cf):
    return max(0, (l[cf] or 0) - (l[cn] or 0)) if l[cf] is not None else 0


def excesso(l, cn, cf):
    return max(0, (l[cn] or 0) - (l[cf] or 0)) if l[cf] is not None else 0


def tabela_resumo(regioes):
    fora = ["| região | fonte | mapas aqui / fonte | objetos | pessoas | com fala | "
            "treinadores | placas | com texto | encontros |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for nome, fonte, linhas, ausentes in regioes:
        p = com_par(linhas)
        fora.append(
            f"| {nome} | {fonte} | {len(linhas)} / {len(p) + len(ausentes)} | "
            f"{soma(p, 'obj_n')} / {soma(p, 'obj_f')} | "
            f"{soma(p, 'pessoas_n')} / {soma(p, 'pessoas_f')} | "
            f"{soma(p, 'fala_n')} / {soma(p, 'fala_f')} | "
            f"{soma(p, 'trein_n')} / {soma(p, 'trein_f')} | "
            f"{soma(p, 'placas_n')} / {soma(p, 'placas_f')} | "
            f"{soma(p, 'placas_txt_n')} / {soma(p, 'placas_txt_f')} | "
            f"{sum(1 for l in p if l['enc_n'])} / {sum(1 for l in p if l['enc_f'])} |")
    return fora


def lacunas(regioes):
    """(tamanho, região, o quê, como conferir), da maior para a menor."""
    fora = []
    for nome, fonte, linhas, ausentes in regioes:
        p = com_par(linhas)
        pares = [
            ("pessoas que a fonte tem e aqui não",
             sum(falta(l, "pessoas_n", "pessoas_f") for l in p),
             "completar object_events dos mapas com falta"),
            ("pessoas a mais que a fonte (conteúdo inventado)",
             sum(excesso(l, "pessoas_n", "pessoas_f") for l in p),
             "bloco B3: esconder atrás de flag depois das quatro provas"),
            ("NPC mudo a mais que a fonte (existe e não fala)",
             sum(excesso(l, "mudo_n", "mudo_f") for l in p),
             "bloco B2: trazer a fala da fonte"),
            ("treinador da fonte sem par batalhável aqui",
             sum(falta(l, "trein_n", "trein_f") for l in p),
             "bloco B4: ligar trainerbattle e declarar time"),
            ("placa genérica a mais que a fonte",
             sum(excesso(l, "placa_gen_n", "placa_gen_f") for l in p),
             "trazer o texto da placa da fonte"),
            ("mapa da fonte ausente aqui", len(ausentes),
             "bloco B1 (Sinnoh) ou conversão nova"),
            ("mapa com encontro selvagem na fonte e sem tabela aqui",
             sum(1 for l in p if l["enc_f"] and not l["enc_n"]),
             "importar a tabela de encontro da fonte"),
        ]
        for o_que, n, como in pares:
            if n:
                fora.append((n, nome, o_que, como, fonte))
    return sorted(fora, reverse=True)


def escreve(regioes):
    L = []
    L.append("# Inventário por região, medido contra a fonte")
    L.append("")
    L.append("Gerado por `python3 dev_scripts/inventario.py`. **Não edite à mão**:")
    L.append("todo número aqui sai de um arquivo da fonte, e o caminho do arquivo")
    L.append("está na própria linha, para poder ser conferido abrindo ele.")
    L.append("")
    L.append("Toda coluna aparece como `aqui / fonte`. Onde a fonte não tem par para o")
    L.append("mapa, a linha sai com `--` e nunca com zero: não saber é um resultado.")
    L.append("")
    L.append("**Existe não é ter conteúdo.** É a lição que fez `completude.py` dar 98%")
    L.append("para Unova sendo maquete de colisão. Por isso `pessoas` e `com fala` são")
    L.append("colunas diferentes, e `placas` e `com texto` também. Um NPC pode existir,")
    L.append("ocupar índice de save e não dizer uma palavra.")
    L.append("")
    L.append("Pokémon de overworld do hns (1390 objetos) fora da régua por decisão de "
             "12/08: dívida de feature inexistente não é fila de trabalho.")
    L.append("")
    L.append("## Resumo por região")
    L.append("")
    L += tabela_resumo(regioes)
    L.append("")
    L.append("Leitura das colunas:")
    L.append("")
    L.append("- **mapas aqui / fonte**: quantos mapas nossos casaram com a fonte, contra")
    L.append("  o total que a fonte tem daquela região (casados mais ausentes).")
    L.append("- **pessoas**: `object_event` que é gente. Item ball, árvore de Cut, pedra")
    L.append("  de Strength, caminhão e boneco de quarto secreto não entram, dos dois")
    L.append("  lados, senão a conta compara mobília com gente.")
    L.append("- **com fala**: dessas pessoas, quantas têm script que chega a pôr texto na")
    L.append("  tela. É a coluna de CONTEÚDO; a anterior é só de presença.")
    L.append("- **treinadores**: aqui é constante citada por `trainerbattle` E com bloco")
    L.append("  `=== TRAINER_X ===` num `.party` compilado (`trainers.party` e")
    L.append("  `trainers_frlg.party`; os `.party` de Johto e Sinnoh são acervo e não")
    L.append("  entram na ROM). Na fonte é o treinador que a fonte declara no mapa.")
    L.append("- **placas / com texto**: `bg_event` com script, e quantas dessas têm texto")
    L.append("  próprio em vez de rótulo genérico compartilhado.")
    L.append("- **encontros**: mapas com tabela de Pokémon selvagem.")
    L.append("")

    for nome, fonte, linhas, ausentes in regioes:
        p = com_par(linhas)
        L.append(f"## {nome} (fonte: `fontes-mapas/{fonte}`)")
        L.append("")
        L.append(f"{len(linhas)} mapas nossos, {len(p)} com par na fonte, "
                 f"{len(linhas) - len(p)} sem par, {len(ausentes)} mapas da fonte ausentes aqui.")
        L.append("")
        L.append("### Os dois totais, lado a lado")
        L.append("")
        L.append("| medida | existe | tem conteúdo | fonte |")
        L.append("|---|---:|---:|---:|")
        L.append(f"| pessoas | {soma(p, 'pessoas_n')} | {soma(p, 'fala_n')} com fala | "
                 f"{soma(p, 'pessoas_f')} ({soma(p, 'fala_f')} com fala) |")
        L.append(f"| placas | {soma(p, 'placas_n')} | {soma(p, 'placas_txt_n')} com texto | "
                 f"{soma(p, 'placas_f')} ({soma(p, 'placas_txt_f')} com texto) |")
        L.append(f"| treinadores | {soma(p, 'trein_cit_n')} citados por trainerbattle | "
                 f"{soma(p, 'trein_n')} com time | {soma(p, 'trein_f')} |")
        L.append(f"| mapas | {len(linhas)} | {sum(1 for l in p if l['fala_n'])} "
                 f"com pelo menos um NPC que fala | {len(p) + len(ausentes)} |")
        L.append(f"| encontros | {sum(1 for l in p if l['enc_n'])} | "
                 f"-- | {sum(1 for l in p if l['enc_f'])} |")
        L.append("")
        mudos = soma(p, "mudo_n")
        sem = soma(p, "sem_script_n")
        mudo_f = soma(p, "mudo_f")
        L.append(f"Dos {soma(p, 'pessoas_n')} que existem, **{mudos} não falam**: "
                 f"{sem} sem script nenhum (`script: \"0\"`) e {mudos - sem} com rótulo "
                 "que não tem comando de texto (parte é balconista e enfermeira, que "
                 "chamam loja e cura direto, e parte é NPC pela metade). "
                 f"A fonte tem {mudo_f} mudos nos mesmos mapas, então a dívida real é "
                 f"**{sum(excesso(l, 'mudo_n', 'mudo_f') for l in p)}**, somada mapa a "
                 "mapa (o excesso de um mapa não paga a falta de outro).")
        L.append("")

        nao_gente_n = soma(p, "obj_n") - soma(p, "pessoas_n")
        nao_gente_f = soma(p, "obj_f") - soma(p, "pessoas_f")
        L.append(f"Objetos que NÃO são gente (item ball, árvore, pedra, mobília): "
                 f"**{nao_gente_n} aqui contra {nao_gente_f} na fonte**. Esta linha "
                 "importa porque `completude.py` conta objeto e não gente: quando o "
                 "total de objetos bate com a fonte e o de pessoas não, o que aconteceu "
                 "foi troca de sprite, não falta de objeto. É o caso de Johto, onde o "
                 "importador pôs `OBJ_EVENT_GFX_ITEM_BALL` com `script: \"0\"` na "
                 "coordenada exata de cada NPC da fonte (conferido à mão em "
                 "`EcruteakCity`, 49 objetos dos dois lados e 49 item balls aqui).")
        L.append("")

        L.append("### Mapa a mapa (só os que divergem da fonte)")
        L.append("")
        L.append("Toda coluna de lacuna é medida CONTRA A FONTE, nunca contra o ideal. "
                 "Mapa igual à fonte não aparece aqui, mesmo cheio de NPC mudo: o "
                 "pokeemerald vanilla também tem, e reprovar o jogo original é a lição "
                 "4.10 do `ESTADO.md`.")
        L.append("")
        L.append("| mapa | objetos | pessoas | falta | excesso | mudo a mais | treinador "
                 "| placa genérica a mais | encontro | arquivo da fonte |")
        L.append("|---|---:|---:|---:|---:|---:|---:|---:|:-:|---|")

        def peso(l):
            return (falta(l, "pessoas_n", "pessoas_f")
                    + excesso(l, "pessoas_n", "pessoas_f")
                    + excesso(l, "mudo_n", "mudo_f")
                    + falta(l, "trein_n", "trein_f")
                    + excesso(l, "placa_gen_n", "placa_gen_f")
                    + (1 if l["enc_f"] and not l["enc_n"] else 0))
        divergentes = sorted((l for l in p if peso(l)), key=lambda l: -peso(l))
        for l in divergentes:
            enc = "ok" if l["enc_n"] == l["enc_f"] else ("falta" if l["enc_f"] else "extra")
            L.append(
                f"| `{l['mapa']}` | {l['obj_n']} / {l['obj_f']} | "
                f"{l['pessoas_n']} / {l['pessoas_f']} | "
                f"{falta(l, 'pessoas_n', 'pessoas_f') or ''} | "
                f"{excesso(l, 'pessoas_n', 'pessoas_f') or ''} | "
                f"{excesso(l, 'mudo_n', 'mudo_f') or ''} | "
                f"{l['trein_n']} / {l['trein_f']} | "
                f"{excesso(l, 'placa_gen_n', 'placa_gen_f') or ''} | {enc} | "
                f"`fontes-mapas/{l['prova']}` |")
        if not divergentes:
            L.append("| (nenhum) | | | | | | | | | |")
        L.append("")

        sem_par = [l for l in linhas if not l["prova"]]
        if sem_par:
            L.append(f"<details><summary>{len(sem_par)} mapas nossos sem par na fonte "
                     "(nativo, renomeado ou de outra fonte)</summary>")
            L.append("")
            for l in sem_par:
                L.append(f"- `{l['mapa']}` ({l['pessoas_n']} pessoas, "
                         f"{l['fala_n']} com fala)")
            L.append("")
            L.append("</details>")
            L.append("")
        if ausentes:
            L.append(f"<details><summary>{len(ausentes)} mapas que a fonte tem e nós "
                     "não</summary>")
            L.append("")
            for m in ausentes:
                L.append(f"- `{m}`")
            L.append("")
            L.append("</details>")
            L.append("")

    L.append("## Fila de trabalho")
    L.append("")
    L.append("**Isto substitui a seção 8 do `ESTADO.md` como fila.** A ordem é o tamanho")
    L.append("medido da lacuna, não a opinião de ninguém. Item que some do inventário na")
    L.append("próxima rodada é item resolvido; item que cresce é regressão.")
    L.append("")
    L.append("| # | tamanho | região | lacuna | por onde se fecha |")
    L.append("|---:|---:|---|---|---|")
    for n, (tam, reg, o_que, como, _f) in enumerate(lacunas(regioes), 1):
        L.append(f"| {n} | {tam} | {reg} | {o_que} | {como} |")
    L.append("")
    L.append("### Por região, a maior lacuna de cada uma")
    L.append("")
    vistas, L2 = set(), []
    for tam, reg, o_que, como, _f in lacunas(regioes):
        if reg in vistas:
            continue
        vistas.add(reg)
        L2.append(f"- **{reg}**: {o_que}, {tam}. {como}.")
    L += L2
    L.append("")
    return "\n".join(L) + "\n"


def main():
    regioes = monta()
    if "--resumo" not in sys.argv:
        with open(SAIDA, "w", encoding="utf-8") as f:
            f.write(escreve(regioes))
        print(f"escrito: {SAIDA}")
    print("\n".join(tabela_resumo(regioes)))
    print("\nas 5 maiores lacunas:")
    for tam, reg, o_que, _c, _f in lacunas(regioes)[:5]:
        print(f"  {tam:6}  {reg:7} {o_que}")
    return 0


def demo():
    """As regras que uma medida errada quebraria, cada uma com um caso real."""
    # 1. A armadilha do substring: "VENT" está dentro de "OBJ_EVENT_GFX_".
    #    Comparar contra o nome inteiro jogaria todo NPC fora, calado.
    assert eh_pessoa_gen3("OBJ_EVENT_GFX_ACE_TRAINER_F")
    assert eh_pessoa_gen4("OBJ_EVENT_GFX_ACE_TRAINER_F")
    # 2. Mobília não é gente, dos dois lados.
    assert not eh_pessoa_gen3("OBJ_EVENT_GFX_ITEM_BALL")
    assert not eh_pessoa_gen3("OBJ_EVENT_GFX_PUSHABLE_BOULDER")
    assert not eh_pessoa_gen3("OBJ_EVENT_GFX_SKITTY_DOLL")
    assert not eh_pessoa_gen4("OBJ_EVENT_GFX_BERRY_SOIL")
    # 3. Existir não é falar: o rótulo tem que chegar a um comando de texto.
    idx = {"A": "\tlock\n\tfaceplayer\n\tmsgbox X, MSGBOX_NPC\n\tend\n",
           "B": "\tlock\n\tapplymovement 1, Mov\n\tend\n",
           "C": "\tgoto A\n", "D": "\tgoto D\n",
           "T": "\ttrainerbattle_single TRAINER_X, Text_Visto, Text_Derrotado\n"}
    assert fala_gen3("A", idx)
    assert not fala_gen3("B", idx)
    # Treinador de gen 3 fala pelos ARGUMENTOS do trainerbattle, sem msgbox.
    assert fala_gen3("T", idx), "trainerbattle é fala; sem isso 360 NPC viram mudos"
    assert fala_gen3("C", idx), "goto tem que ser seguido, senão a placa some"
    assert not fala_gen3("D", idx), "ciclo de goto não pode travar o inventário"
    assert not fala_gen3("0", idx) and not fala_gen3("0x0", idx)
    # 4. O mesmo, em gen 2, onde o comando tem outro nome.
    c2 = {"S": "\tjumptextfaceplayer T\n", "M": "\tspecial Nada\n"}
    assert fala_gen2("S", c2) and not fala_gen2("M", c2)
    assert not fala_gen2("-1", c2), "-1 é 'sem script' no gen 2, não um rótulo"
    # 5. Falta e excesso são medidas SEPARADAS, e uma nunca vira a outra.
    l = {"pessoas_n": 12, "pessoas_f": 5}
    assert excesso(l, "pessoas_n", "pessoas_f") == 7
    assert falta(l, "pessoas_n", "pessoas_f") == 0
    # 6. Fonte sem par não vira zero: some da conta em vez de mentir.
    assert falta({"pessoas_n": 3, "pessoas_f": None}, "pessoas_n", "pessoas_f") == 0
    # 7. O mapa de Unova é `R22` na fonte e `Unova_R22` aqui: se a chave não
    #    colapsar as duas grafias, 45 mapas somem do denominador.
    assert C.normaliza("Unova_R22") == C.normaliza("R22")
    assert chave_simples("R_22") == chave_simples("R22")
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
