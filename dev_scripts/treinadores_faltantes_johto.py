#!/usr/bin/env python3
"""Fecha o que da para fechar do bloco B4 de Johto: os 8 treinadores do hns que
tem mapa aqui, time la, e nenhuma cena no caminho.

Uso:
    python3 dev_scripts/treinadores_faltantes_johto.py            # so relata
    python3 dev_scripts/treinadores_faltantes_johto.py --aplica
    python3 dev_scripts/treinadores_faltantes_johto.py --demo

## A lacuna, medida e nao lembrada

`dev_scripts/treinadores_faltantes_b4.py` mede Johto contra o hns: **273
treinadores na fonte, 254 batalhaveis aqui**. Das 36 ausencias, 28 nao sao
trabalho deste script e estao classificadas no relatorio dele (12 sao variante
de time do rival por inicial escolhido e escala de lider, feature que esta ROM
nao tem; 13 sao batalha DENTRO de cena, que e do bloco B6; 3 estao num mapa que
nao existe aqui, que e do bloco B1).

Sobram **8**, e as 8 sao mecanicas:

- **BETH**, na `Route26North`. O boneco DELA ja esta aqui, na coordenada exata
  da fonte (26,24), com o sprite certo e `script: "0"`: e o caso classico de
  NPC importado mudo. So faltava declarar o time, a constante e a batalha.
- **7 Rockets e cientistas da Torre de Radio de Goldenrod** (2F, 3F e 4F). O
  proprio comentario no topo dos tres `scripts.inc` diz por que eles nao
  entraram: *"sairam por falta de vaga de treinador"*, quando
  `MAX_TRAINERS_COUNT_EMERALD` era 2500 e restavam 14 vagas. **O teto subiu para
  4000 em 12/08/2026 e o motivo daquele corte deixou de existir.** Os tres
  comentarios sao corrigidos junto, senao viram a licao 4.11 (teste, ou nota,
  que guarda copia de um fato e envelhece calado).

## Coordenada: a da FONTE, e mesmo assim conferida

Ao contrario de Sinnoh, Johto veio do hns inteira e nossa planta e a mesma da
fonte, entao a coordenada nao precisa ser inventada: e a do `map.json` do hns.
Isso NAO dispensa as guardas, e elas sao as mesmas quatro de
`treinadores_faltantes_sinnoh.py` (dentro do mapa, tile andavel e livre, chao
comum e nao porta, conectividade preservada), importadas de la em vez de
copiadas.

## Nivel: a curva que o proprio importador de Johto declara

`importa_treinadores_johto.autoteste` afirma
`curva.transforma(nivel, (2, 50), ALVO["Johto"])`, e a medida bate: dos 209
treinadores de Johto que casam com o hns, essa formula reproduz o nivel gravado
na esmagadora maioria (2->45, 26->72, 36->84, 45->94, 50->100). Os grunts da
Torre de Radio que ja estavam aqui foram portados A MAO por outra sessao e
ficaram 2 a 3 niveis acima dessa curva; os novos entram pela curva declarada,
nao pela excecao, porque nivel e assunto do bloco B8 e a curva e a regra escrita.

## Sprite: o do VIZINHO, nao o da fonte, e de proposito

Na fonte o Rocket e `OBJ_EVENT_GFX_ROCKET_M`, e esse sprite EXISTE nesta build.
Mesmo assim os novos entram como `OBJ_EVENT_GFX_AQUA_MEMBER_M/F`, que e o que os
grunts JA PORTADOS do mesmo andar usam: dois desenhos diferentes de Rocket na
mesma sala e defeito visivel, e a escolha de sprite para o Rocket de Johto ja
foi feita pela sessao que portou os primeiros. Trocar todos para ROCKET_* seria
mudanca de arte, nao de treinador, e nao e deste bloco.

## Objeto novo entra no FIM da lista

A save guarda ÍNDICE de objeto (`objectEvents[]`). Acrescentar no fim nao mexe
em indice de ninguem; inserir no meio quebraria a save do Gui.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HNS = os.path.abspath(os.path.join(REPO, "..", "fontes-mapas/hns"))
HEADER = os.path.join(REPO, "include/constants/opponents.h")
PARTY = os.path.join(REPO, "src/data/trainers.party")
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importlib.util  # noqa: E402


def _mod(nome, arquivo):
    e = importlib.util.spec_from_file_location(
        nome, os.path.join(REPO, "dev_scripts", arquivo))
    m = importlib.util.module_from_spec(e)
    e.loader.exec_module(m)
    return m


IT = _mod("it_johto", "importa_treinadores_johto.py")
CURVA = _mod("curva", "curva_de_nivel.py")
S = _mod("b4_sinnoh", "treinadores_faltantes_sinnoh.py")
W = _mod("warp", "valida_warp_tile.py")

APLICA = "--aplica" in sys.argv
MARCA = "hns_b4"
ORIGEM_NIVEL = (2, 50)      # faixa de nivel do hns, declarada pelo importador
MUDO = ("0", "0x0", "NULL", "")

# (nosso mapa, [entradas]). Cada entrada:
#   hns_mapa   arquivo de scripts.inc da fonte onde o bloco mora
#   hns_rot    rotulo do bloco la
#   tr         constante do hns
#   nossa      constante nossa (nova)
#   rot        rotulo nosso
#   txt        prefixo dos nossos textos
#   onde       ("reuso", indice) ou ("novo", x, y, sprite, movimento, raio)
LIGAR = [
    # Beth: o boneco esta aqui, na coordenada da fonte, mudo desde a importacao.
    ("Route26North", [dict(
        hns_mapa="Route26", hns_rot="Route26_EventScript_Beth",
        tr="TRAINER_BETH", nossa="TRAINER_JOHTO_BETH",
        rot="Route26North_EventScript_Beth", txt="Route26North_Text_Beth",
        onde=("reuso", 0, "OBJ_EVENT_GFX_COOLTRAINER_F", "7"))]),
    ("GoldenrodCity_RadioTower_2F", [
        dict(hns_mapa="GoldenrodCity_RadioTower_2F",
             hns_rot="GoldenrodRaidoTower2_EventScript_Grunt4",
             tr="TRAINER_GRUNT_4", nossa="TRAINER_JOHTO_GRUNT_4",
             rot="RadioTower2F_EventScript_Grunt3", txt="RadioTower2F_Text_Grunt3",
             onde=("novo", 13, 7, "OBJ_EVENT_GFX_AQUA_MEMBER_M",
                   "MOVEMENT_TYPE_FACE_LEFT", "4")),
        dict(hns_mapa="GoldenrodCity_RadioTower_2F",
             hns_rot="GoldenrodRaidoTower2_EventScript_GruntF2",
             tr="TRAINER_GRUNT_26", nossa="TRAINER_JOHTO_GRUNT_26",
             rot="RadioTower2F_EventScript_Grunt4", txt="RadioTower2F_Text_Grunt4",
             onde=("novo", 7, 7, "OBJ_EVENT_GFX_AQUA_MEMBER_F",
                   "MOVEMENT_TYPE_FACE_RIGHT", "4")),
    ]),
    ("GoldenrodCity_RadioTower_3F", [
        dict(hns_mapa="GoldenrodCity_RadioTower_3F",
             hns_rot="GoldenrodRaidoTower3_EventScript_Grunt8",
             tr="TRAINER_GRUNT_8", nossa="TRAINER_JOHTO_GRUNT_8",
             rot="RadioTower3F_EventScript_Grunt3", txt="RadioTower3F_Text_Grunt3",
             onde=("novo", 25, 5, "OBJ_EVENT_GFX_AQUA_MEMBER_M",
                   "MOVEMENT_TYPE_FACE_DOWN_AND_RIGHT", "4")),
        dict(hns_mapa="GoldenrodCity_RadioTower_3F",
             hns_rot="GoldenrodRaidoTower3_EventScript_Scientist",
             tr="TRAINER_MARC", nossa="TRAINER_JOHTO_MARC",
             rot="RadioTower3F_EventScript_Marc", txt="RadioTower3F_Text_Marc",
             onde=("novo", 17, 10, "OBJ_EVENT_GFX_SCIENTIST_1",
                   "MOVEMENT_TYPE_LOOK_AROUND", "4")),
    ]),
    ("GoldenrodCity_RadioTower_4F", [
        dict(hns_mapa="GoldenrodCity_RadioTower_4F",
             hns_rot="GoldenrodRaidoTower4_EventScript_Grunt9",
             tr="TRAINER_GRUNT_9", nossa="TRAINER_JOHTO_GRUNT_9",
             rot="RadioTower4F_EventScript_Grunt1", txt="RadioTower4F_Text_Grunt1",
             # raio 67 no hns e lixo de conversao (o campo e um byte e o mapa tem
             # 30 de largura): entra com 4, o mesmo dos irmaos do andar.
             onde=("novo", 15, 11, "OBJ_EVENT_GFX_AQUA_MEMBER_M",
                   "MOVEMENT_TYPE_FACE_UP", "4")),
        dict(hns_mapa="GoldenrodCity_RadioTower_4F",
             hns_rot="GoldenrodRaidoTower4_EventScript_Grunt28",
             tr="TRAINER_GRUNT_28", nossa="TRAINER_JOHTO_GRUNT_28",
             rot="RadioTower4F_EventScript_Grunt2", txt="RadioTower4F_Text_Grunt2",
             onde=("novo", 15, 5, "OBJ_EVENT_GFX_AQUA_MEMBER_F",
                   "MOVEMENT_TYPE_FACE_DOWN", "7")),
        dict(hns_mapa="GoldenrodCity_RadioTower_4F",
             hns_rot="GoldenrodCity_RadioTower_4F4_EventScript_Scientist",
             tr="TRAINER_RICH", nossa="TRAINER_JOHTO_RICH",
             rot="RadioTower4F_EventScript_Rich", txt="RadioTower4F_Text_Rich",
             onde=("novo", 12, 13, "OBJ_EVENT_GFX_SCIENTIST_1",
                   "MOVEMENT_TYPE_FACE_UP", "4")),
    ]),
]

# Comentario de topo que virou mentira quando o teto de treinador subiu.
CORRIGE_NOTA = {
    "GoldenrodCity_RadioTower_2F": (
        "@ ponytail: dos quatro grunts do hns ficaram dois, porque so restam 14 vagas de\n"
        "@ treinador no jogo inteiro (MAX_TRAINERS_COUNT). Buena e o policial sairam:\n"
        "@ dependiam de VAR_GOLDENROD_CITY_STATE e de sprite que esta build nao desenha.\n",
        "@ Os QUATRO grunts do hns estao aqui: os dois primeiros vieram na leva de\n"
        "@ portes e os outros dois em 12/08/2026, quando MAX_TRAINERS_COUNT_EMERALD\n"
        "@ subiu de 2500 para 4000 e as 14 vagas que travavam o porte viraram 1559.\n"
        "@ Buena e o policial continuam de fora: dependiam de VAR_GOLDENROD_CITY_STATE\n"
        "@ e de sprite que esta build nao desenha.\n"),
    "GoldenrodCity_RadioTower_3F": (
        "@ ponytail: o cientista MARC e o terceiro grunt sairam por falta de vaga de\n"
        "@ treinador. ",
        "@ O cientista MARC e o terceiro grunt entraram em 12/08/2026, quando o teto de\n"
        "@ treinador subiu de 2500 para 4000 e a falta de vaga que os cortava acabou.\n"
        "@ "),
    "GoldenrodCity_RadioTower_4F": (
        "@ ponytail: o 4F ficou com o PROTON, que e o reencontro do arco do Slowpoke\n"
        "@ Well, e com a DJ MARY. Os dois cientistas e os dois grunts do hns sairam por\n"
        "@ falta de vaga de treinador.\n",
        "@ O 4F tem o PROTON, que e o reencontro do arco do Slowpoke Well, a DJ MARY, os\n"
        "@ dois grunts e o cientista RICH. Os tres ultimos entraram em 12/08/2026, com o\n"
        "@ teto de treinador em 4000; antes eram cortados por falta de vaga. O segundo\n"
        "@ cientista do hns nao existe: o 4F da fonte tem RICH e mais nenhum.\n"),
}


def le(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def ids_e_teto():
    txt = le(HEADER)
    pares = re.findall(r"^#define\s+(TRAINER_\w+)\s+(\d+)\s*$", txt, re.M)
    teto = int(re.search(r"MAX_TRAINERS_COUNT_EMERALD\s+(\d+)", txt).group(1))
    return {n: int(v) for n, v in pares}, teto


def ocupados(d):
    fora = set()
    for chave in ("object_events", "warp_events", "bg_events", "coord_events"):
        for e in d.get(chave) or []:
            if e.get("x") is not None:
                fora.add((e["x"], e["y"]))
    return fora


def recusa_coordenada(mapa, pontos):
    """As quatro guardas de `treinadores_faltantes_sinnoh`, sem copiar codigo."""
    d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                       encoding="utf-8"))
    w, h, pal, ts1, ts2 = S.layout_do_mapa(mapa)
    prim, _ = W.tabela_de_atributos(ts1)
    sec, _ = W.tabela_de_atributos(ts2)
    tomados = {p for p in ocupados(d)}
    # Ja aplicado? Entao o proprio tile do nosso boneco nao conta como ocupado,
    # senao o --demo fica vermelho DEPOIS de um --aplica bom (licao 4.11).
    meus = {(o["x"], o["y"]) for o in (d.get("object_events") or [])
            if o.get("origem") == MARCA}
    tomados -= meus
    males, novos = [], set()
    for x, y in pontos:
        if not (0 <= x < w and 0 <= y < h):
            males.append((x, y, "fora do mapa"))
            continue
        pal_i = pal[y * w + x]
        if (pal_i >> 10) & 3:
            males.append((x, y, "tile de colisao"))
            continue
        if (x, y) in tomados or (x, y) in novos:
            males.append((x, y, "tile ja ocupado"))
            continue
        if S.comportamento(prim or [], sec or [], pal_i & 0x3FF) in W.COMPORTA_WARP:
            males.append((x, y, "tile de porta/escada: esconderia a passagem"))
            continue
        novos.add((x, y))
    if males or not novos:
        return males
    solidos = {(o["x"], o["y"]) for o in (d.get("object_events") or [])
               if o.get("x") is not None and o.get("origem") != MARCA}
    depois = S.componentes(w, h, pal, solidos | novos)
    for ilha in S.componentes(w, h, pal, solidos):
        resto = ilha - novos
        if resto and not any(resto <= nova for nova in depois):
            males.append((None, None, f"a ilha de {len(ilha)} tile(s) em "
                                      f"{sorted(ilha)[0]} parte em duas"))
    for x, y in novos:
        if not any(any((x + dx, y + dy) in nova for nova in depois)
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            males.append((x, y, "ninguem chega perto: batalha inalcancavel"))
    return males


def bloco_party(tr, nossa, times, ctx):
    """Bloco `=== TRAINER_X ===` com o time do hns e o nivel na curva de Johto."""
    t = times[tr]
    classe = _resolve(t["class"], IT.CLASSE, ctx["classes"])
    pic = _resolve(t["pic"], IT.PIC, ctx["pics"])
    if not pic:
        return None, f"{tr}: sem pic utilizavel nesta build"
    L = [f"=== {nossa} ===", f"Name: {t['name'].title()}"]
    if classe:
        L.append(f"Class: {classe}")
    L.append(f"Pic: {pic}")
    itens = [i for i in t["items"] if i != "ITEM_NONE" and i in ctx["itens"]]
    if itens:
        L.append("Items: " + " / ".join(itens))
    L.append("Double Battle: " + ("Yes" if t["double"] else "No"))
    macro = t["macro"] or "NO_ITEM_DEFAULT_MOVES"
    alvo = CURVA.ALVO["Johto"]
    for mon in t["mons"]:
        if mon["species"] not in ctx["species"]:
            return None, f"{tr}: especie {mon['species']} nao existe aqui"
        cabeca = mon["species"]
        if macro.startswith("ITEM_") and mon["item"] and mon["item"] != "ITEM_NONE" \
                and mon["item"] in ctx["itens"]:
            cabeca += f" @ {mon['item']}"
        nivel = CURVA.transforma(int(mon["lvl"] or 5), ORIGEM_NIVEL, alvo)
        v = min(31, int(mon["iv"] or 0) * 31 // 255)
        L += ["", cabeca, f"Level: {nivel}",
              f"IVs: {v} HP / {v} Atk / {v} Def / {v} SpA / {v} SpD / {v} Spe"]
        if macro.endswith("CUSTOM_MOVES"):
            for mv in mon["moves"]:
                mv = IT.RENOMEIA_MOVE.get(mv, mv)
                if mv in ("MOVE_NONE", None):
                    continue
                if mv not in ctx["moves"]:
                    return None, f"{tr}: golpe {mv} nao existe aqui"
                L.append(f"- {mv}")
    return "\n".join(L) + "\n", None


def _resolve(valor, tabela, existentes):
    for t in (tabela.get(valor), valor, (valor or "") + "_FRLG"):
        if t and t in existentes:
            return t
    return None


def contexto():
    return {
        "species": IT.constantes("include/constants/species.h", "SPECIES_"),
        "moves": IT.constantes("include/constants/moves.h", "MOVE_"),
        "itens": IT.constantes("include/constants/items.h", "ITEM_"),
        "classes": IT.constantes("include/constants/trainers.h", "TRAINER_CLASS_"),
        "pics": IT.constantes("include/constants/trainers.h", "TRAINER_PIC_"),
    }


def elevacao_da_fonte(e):
    """(elevacao, erro). Acha o objeto da fonte pelo rotulo e confere a coordenada.

    Para o caso de reuso nao ha objeto novo, e a elevacao do boneco que ja esta
    aqui nao se toca: devolve None.
    """
    if e["onde"][0] != "novo":
        return None, None
    _t, x, y, _gfx, _mov, _raio = e["onde"]
    for m in (e["hns_mapa"], e["nossa_fonte_mapa"] if "nossa_fonte_mapa" in e else None):
        if not m:
            continue
        p = os.path.join(HNS, "data/maps", m, "map.json")
        if not os.path.exists(p):
            continue
        for o in json.load(open(p, encoding="utf-8")).get("object_events") or []:
            if o.get("script") == e["hns_rot"]:
                if (o["x"], o["y"]) != (x, y):
                    return None, f"{e['hns_rot']}: fonte em ({o['x']},{o['y']}), " \
                                 f"tabela em ({x},{y})"
                return o.get("elevation", 0), None
    return None, f"{e['hns_rot']}: sem objeto na fonte"


def plano():
    """[(mapa, [entradas prontas])], recusas."""
    times = IT.times_do_hns(HNS)
    ctx = contexto()
    ids, teto = ids_e_teto()
    ja_party = set(re.findall(r"^=== (TRAINER_\w+) ===", le(PARTY), re.M))
    proximo = max(ids.values()) + 1
    saida, recusas = [], []
    for mapa, entradas in LIGAR:
        pm = os.path.join(REPO, "data/maps", mapa, "map.json")
        ps = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        if not os.path.exists(pm) or not os.path.exists(ps):
            recusas.append((mapa, "mapa nao existe aqui", ""))
            continue
        inc = le(ps)
        rotulos = set(re.findall(r"^(\w+):{1,2}", inc, re.M))
        pontos = [(e["onde"][1], e["onde"][2]) for e in entradas
                  if e["onde"][0] == "novo"]
        males = recusa_coordenada(mapa, pontos) if pontos else []
        if males:
            for m in males:
                recusas.append((mapa, "coordenada recusada", m))
            continue
        prontas = []
        for e in entradas:
            fonte = le(os.path.join(HNS, "data/maps", e["hns_mapa"], "scripts.inc"))
            blocos = IT.blocos_de_script(fonte)
            corpo = blocos.get(e["hns_rot"])
            if corpo is None:
                recusas.append((mapa, "rotulo nao esta na fonte", e["hns_rot"]))
                continue
            b = IT.batalha_simples(corpo)
            if b is None or b[1] != e["tr"]:
                recusas.append((mapa, "bloco da fonte nao e batalha simples",
                                e["hns_rot"]))
                continue
            _tipo, tr, args = b
            depois = IT.depois_da_batalha(corpo)
            txts = IT.textos_do_hns(fonte)
            if len(args) < 2 or any(a not in txts for a in args[:2]) \
                    or (depois and depois not in txts):
                recusas.append((mapa, "texto da fonte nao encontrado", e["hns_rot"]))
                continue
            if tr not in times or not times[tr]["mons"]:
                recusas.append((mapa, "sem time no hns, nao inventado", tr))
                continue
            if e["nossa"] in ids or e["nossa"] in ja_party:
                recusas.append((mapa, "constante ja existe", e["nossa"]))
                continue
            if e["rot"] in rotulos:
                recusas.append((mapa, "rotulo ja usado neste mapa", e["rot"]))
                continue
            corpo_party, erro = bloco_party(tr, e["nossa"], times, ctx)
            if erro:
                recusas.append((mapa, "time nao traduz", erro))
                continue
            if proximo >= teto:
                recusas.append((mapa, "id acima do teto", e["nossa"]))
                continue
            # Elevacao e coordenada saem do OBJETO DA FONTE, nao da tabela: a
            # primeira versao cravou `elevation: 3`, que e o padrao de Sinnoh, e
            # nos tres andares da Torre de Radio TUDO esta em 0, aqui e la.
            # Elevacao trocada num interior e boneco em outro plano de colisao.
            elev, erro_obj = elevacao_da_fonte(e)
            if erro_obj:
                recusas.append((mapa, "objeto da fonte nao confere", erro_obj))
                continue
            prontas.append(dict(
                e, id=proximo, party=corpo_party, elevation=elev,
                visto=txts[args[0]], batido=txts[args[1]],
                depois=txts[depois] if depois else None))
            proximo += 1
            ids[e["nossa"]] = prontas[-1]["id"]
            rotulos.add(e["rot"])
        if prontas:
            saida.append((mapa, prontas))
    return saida, recusas


def tabula(bloco):
    """Recuo do hns e as vezes espaco; aqui tudo e tabulacao, como no resto do repo."""
    return "\n".join("\t" + l.strip() for l in bloco.split("\n") if l.strip())


def trecho_script(e):
    t = e["txt"]
    fora = (f"\n{e['rot']}::\n"
            f"\ttrainerbattle_single {e['nossa']}, {t}Seen, {t}Beaten\n")
    if e["depois"]:
        fora += f"\tmsgbox {t}After, MSGBOX_AUTOCLOSE\n"
    fora += "\tend\n"
    fora += f"\n{t}Seen:\n{tabula(e['visto'])}\n"
    fora += f"\n{t}Beaten:\n{tabula(e['batido'])}\n"
    if e["depois"]:
        fora += f"\n{t}After:\n{tabula(e['depois'])}\n"
    return fora


def aplica(tudo):
    ids, _teto = ids_e_teto()
    feitos = recusados = 0
    novas_consts = []
    novos_blocos = []
    for mapa, entradas in tudo:
        pm = os.path.join(REPO, "data/maps", mapa, "map.json")
        ps = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        # Releitura tardia: outro agente pode ter mexido entre o plano e agora.
        atual = json.load(open(pm, encoding="utf-8"))
        lista = atual.get("object_events")
        if lista is None:
            lista = atual["object_events"] = []
        tomados = ocupados(atual)
        corpo, n = "", 0
        for e in entradas:
            if e["onde"][0] == "reuso":
                _t, i, gfx, raio = e["onde"]
                if i >= len(lista):
                    recusados += 1
                    continue
                ev = lista[i]
                if ev.get("graphics_id") != gfx \
                        or str(ev.get("script", "0")) not in MUDO \
                        or str(ev.get("flag", "0")) not in ("0", "0x0", ""):
                    recusados += 1
                    continue
                ev["script"] = e["rot"]
                ev["trainer_type"] = "TRAINER_TYPE_NORMAL"
                ev["trainer_sight_or_berry_tree_id"] = raio
            else:
                _t, x, y, gfx, mov, raio = e["onde"]
                if (x, y) in tomados:
                    recusados += 1
                    continue
                lista.append({
                    "graphics_id": gfx, "x": x, "y": y,
                    "elevation": e["elevation"],
                    "movement_type": mov,
                    "movement_range_x": 0, "movement_range_y": 0,
                    "trainer_type": "TRAINER_TYPE_NORMAL",
                    "trainer_sight_or_berry_tree_id": raio,
                    "script": e["rot"], "flag": "FLAG_HIDE_GOLDENROD_ROCKETS",
                    "origem": MARCA,
                })
                tomados.add((x, y))
            corpo += trecho_script(e)
            novas_consts.append((e["nossa"], e["id"]))
            novos_blocos.append(e["party"])
            n += 1
        if not n:
            continue
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(atual, f, indent=2, ensure_ascii=False)
            f.write("\n")
        inc = le(ps)
        velho, novo = CORRIGE_NOTA.get(mapa, (None, None))
        if velho and velho in inc:
            inc = inc.replace(velho, novo, 1)
        inc += ("\n@ Treinador do hns que faltava, ligado em 12/08/2026 por\n"
                "@ dev_scripts/treinadores_faltantes_johto.py\n" + corpo)
        with open(ps, "w", encoding="utf-8") as f:
            f.write(inc)
        feitos += n
    if novas_consts:
        larg = max(len(n) for n, _ in novas_consts) + 4
        linhas = "".join(f"#define {n:<{larg}}{i}\n" for n, i in novas_consts)
        txt = le(HEADER)
        alvo = "\n#define TRAINERS_COUNT_EMERALD"
        assert alvo in txt, "opponents.h mudou de forma"
        txt = txt.replace(
            alvo,
            "\n// Treinadores do hns que faltavam em Johto, ligados em 12/08/2026 por\n"
            "// dev_scripts/treinadores_faltantes_johto.py. Acrescentados NO FIM: a flag\n"
            "// de \"ja venci\" deriva do id, entao renumerar aqui apagaria vitoria na save.\n"
            + linhas + alvo, 1)
        with open(HEADER, "w", encoding="utf-8") as f:
            f.write(txt)
        with open(PARTY, "a", encoding="utf-8") as f:
            f.write("\n/*=== TREINADORES DE JOHTO QUE FALTAVAM "
                    "(treinadores_faltantes_johto.py) ===*/\n\n")
            f.write("\n".join(novos_blocos))
    return feitos, recusados


def main():
    tudo, recusas = plano()
    n = sum(len(e) for _m, e in tudo)
    print(f"treinadores a ligar: {n} em {len(tudo)} mapas")
    for mapa, entradas in tudo:
        for e in entradas:
            print(f"  {mapa:32s} {e['nossa']:26s} id={e['id']} "
                  f"{e['onde'][0]} {e['tr']}")
    if recusas:
        print("\nrecusados:")
        for x in recusas:
            print("   ", *x)
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0
    feitos, rec = aplica(tudo)
    print(f"\nligados: {feitos}   recusados na releitura: {rec}")
    return 0


def demo():
    # 1. a lacuna e real: cada constante da tabela esta na fonte com time, e
    #    nenhuma tem par batalhavel aqui.
    times = IT.times_do_hns(HNS)
    # NAO se testa "ainda falta", que e o que este script existe para desfazer:
    # depois do --aplica esse teste ficaria vermelho por ter dado certo, que e a
    # licao 4.11. O que se testa e a FORMA: a fonte declara o treinador, com
    # time, e o nosso lado ou ainda nao existe, ou existe exatamente como esta
    # tabela escreve (mesma constante, mesmo rotulo, mesmo boneco).
    ids, _teto = ids_e_teto()
    for mapa, entradas in LIGAR:
        nj = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                            encoding="utf-8"))
        inc = le(os.path.join(REPO, "data/maps", mapa, "scripts.inc"))
        for e in entradas:
            assert e["tr"] in times and times[e["tr"]]["mons"], e["tr"]
            if e["nossa"] not in ids:
                continue
            assert f"{e['rot']}::" in inc, f"{e['nossa']} tem id e nao tem script"
            assert f"trainerbattle_single {e['nossa']}," in inc, e["nossa"]
            dono = [o for o in nj["object_events"] if o.get("script") == e["rot"]]
            assert len(dono) == 1, f"{e['rot']}: {len(dono)} bonecos"
            o = dono[0]
            alvo = e["onde"]
            if alvo[0] == "novo":
                assert (o["x"], o["y"]) == (alvo[1], alvo[2]), e["rot"]
                assert o["graphics_id"] == alvo[3]
            assert o["trainer_type"] == "TRAINER_TYPE_NORMAL", e["rot"]

    # 2. id e rotulo UNICOS em opponents.h, e o maior id abaixo do teto.
    ids, teto = ids_e_teto()
    txt = le(HEADER)
    pares = re.findall(r"#define\s+(TRAINER_\w+)\s+(\d+)", txt)
    nomes = [a for a, _ in pares]
    assert len(set(nomes)) == len(nomes), "rotulo repetido em opponents.h"
    assert len(set(int(b) for _a, b in pares)) == len(pares), "id repetido"
    assert max(ids.values()) < teto

    # 3. as coordenadas escolhidas passam nas quatro guardas.
    for mapa, entradas in LIGAR:
        p = [(e["onde"][1], e["onde"][2]) for e in entradas if e["onde"][0] == "novo"]
        if p:
            assert not recusa_coordenada(mapa, p), (mapa, recusa_coordenada(mapa, p))

    # 4. MUTACAO PLANTADA: a guarda de tile ocupado tem que reprovar a
    #    coordenada de um boneco que JA esta no 2F (o grunt de (19,11)). Se este
    #    assert ficar verde, a guarda parou de guardar e dois NPC nascem no mesmo
    #    tile.
    ruim = recusa_coordenada("GoldenrodCity_RadioTower_2F", [(19, 11)])
    assert any("ocupado" in m[2] for m in ruim), "a guarda de tile ocupado morreu"
    # 4b. e a de parede. O tile de parede e PROCURADO no map.bin em vez de
    #     cravado: (0,0) do 2F e chao andavel, e cravar o canto deixava este
    #     caso verde sem testar nada.
    w, h, pal, _t1, _t2 = S.layout_do_mapa("GoldenrodCity_RadioTower_2F")
    parede = next((x, y) for y in range(h) for x in range(w)
                  if (pal[y * w + x] >> 10) & 3)
    assert any("colisao" in m[2] for m in
               recusa_coordenada("GoldenrodCity_RadioTower_2F", [parede]))
    # 4c. e a de fora do mapa.
    assert any("fora do mapa" in m[2] for m in
               recusa_coordenada("GoldenrodCity_RadioTower_2F", [(w, h)]))

    # 5. o nivel sai da curva DECLARADA, nao de chute: o proprio autoteste do
    #    importador de Johto usa (2,50) -> ALVO["Johto"], e o topo tem que cair
    #    dentro da faixa.
    lo, hi = CURVA.ALVO["Johto"]
    for l in range(ORIGEM_NIVEL[0], ORIGEM_NIVEL[1] + 1):
        v = CURVA.transforma(l, ORIGEM_NIVEL, (lo, hi))
        assert lo <= v <= hi, (l, v)

    # 6. o boneco da Beth continua sendo o boneco da Beth: mesmo sprite e mesma
    #    coordenada da fonte, no indice que a tabela usa.
    nj = json.load(open(os.path.join(REPO, "data/maps/Route26North/map.json"),
                        encoding="utf-8"))
    o = nj["object_events"][0]
    fj = json.load(open(os.path.join(HNS, "data/maps/Route26North/map.json"),
                        encoding="utf-8"))
    f = [x for x in fj["object_events"]
         if x.get("script") == "Route26_EventScript_Beth"][0]
    assert (o["x"], o["y"]) == (f["x"], f["y"]) == (26, 24)
    assert o["graphics_id"] == f["graphics_id"] == "OBJ_EVENT_GFX_COOLTRAINER_F"

    # 7. a fala sai da fonte, nunca daqui, e fecha em `$`.
    for _mapa, entradas in LIGAR:
        for e in entradas:
            fonte = le(os.path.join(HNS, "data/maps", e["hns_mapa"], "scripts.inc"))
            b = IT.batalha_simples(IT.blocos_de_script(fonte)[e["hns_rot"]])
            t = IT.textos_do_hns(fonte)
            assert b and b[1] == e["tr"]
            assert t[b[2][0]].rstrip().endswith('$"'), e["tr"]

    # 8. nenhum rotulo duplicado na unidade de montagem inteira.
    T = _mod("txt_sinnoh", "texto_sinnoh.py")
    rep = T.rotulos_repetidos()
    assert not rep, f"{len(rep)} rotulo(s) duplicado(s): {rep[:5]}"

    print("demo ok (8 casos; mutacao de tile ocupado reprovada como devia)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
