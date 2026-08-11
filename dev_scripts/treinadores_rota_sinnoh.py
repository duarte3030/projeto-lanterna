#!/usr/bin/env python3
"""Liga os treinadores de ROTA de Sinnoh: time, raio de visão e fala do Platinum.

Uso:
    python3 dev_scripts/treinadores_rota_sinnoh.py            # só relata
    python3 dev_scripts/treinadores_rota_sinnoh.py --aplica
    python3 dev_scripts/treinadores_rota_sinnoh.py --demo

## O buraco que este arquivo fecha

No Platinum o campo `script` de um objeto pode ser DUAS coisas: um índice
numérico dentro do arquivo de scripts do mapa, ou a constante `TRAINER_*` do
treinador que aquele boneco é. `importa_npcs_sinnoh.py` só sabia ler a primeira,
então todo treinador de rota entrou aqui com `script: "0"` e
`TRAINER_TYPE_NONE`: boneco mudo por quem se passa andando.

## O que a tarefa mandava fazer e a medida mostrou não ser preciso

O enunciado mandava copiar o bloco `=== TRAINER_... ===` do acervo
`src/data/trainers_sinnoh.party` para `src/data/trainers.party` e declarar a
constante em `include/constants/opponents.h` na faixa 2418-2549. **Medido antes
de escrever uma linha: os 45 treinadores de rota que faltam JÁ estão declarados
(ids 911 a 1256) e JÁ têm bloco em `trainers.party`, com o nível já remapeado
para a faixa 145-200 de Sinnoh.** Sessão anterior fez essa metade. Id novo para
eles duplicaria time e texto na ROM e daria DUAS flags de "já venci" para a
mesma pessoa.

Por isso este script **não toca em `src/data/trainers.party` nem em
`include/constants/opponents.h`**, e a faixa 2418-2549 continua como estava. Ela
também não serviria: `MAX_TRAINERS_COUNT_EMERALD` é **2500**, não 3000, e
2418-2440 já é de Johto (`TRAINER_JOHTO_CAROL` a `TRAINER_JOHTO_JONAH`).

## De onde sai cada campo (medido na fonte, não lembrado)

- **quem é treinador**: `res/field/events/events_<mapa>.json`, objeto cujo
  `script` é `str` e começa com `TRAINER_`.
- **raio de visão**: `data[0]` do MESMO objeto. Confirmado em
  `src/trainer_encounter.c:187` do pokeplatinum
  (`trainerSightRange = MapObject_GetDataAt(trainerMapObj, 0)`). Sem `data`, o
  raio é 0 e o treinador só luta quando falam com ele.
- **fala**: `res/trainers/data/<slug>.json`, campo `messages`. Em gen 4 o motor
  cuida do treinador sozinho e a fala mora junto com o time, não no banco de
  texto do mapa. **Nada de texto escrito aqui.**
- **qual metade de uma dupla**: campo `double_battle_id` do objeto (1 ou 2), que
  é o que `tools/jsoncnv/convert.py:79` usa para somar
  `SCRIPT_ID_OFFSET_DOUBLE_BATTLES`, e `Script_GetTrainerBattlerIndex`
  (`src/script_manager.c:509`) lê de volta para escolher `TRMSG_*_1` ou
  `TRMSG_*_2`. **A ORDEM no arquivo não serve**: em Route209 o objeto da Sue
  (metade 2) vem ANTES do do Ty (metade 1).

## Direção: fica como o importador deixou, de propósito

Coordenada de rua no Platinum é global da matriz de Sinnoh e o importador
reposicionou todo mundo por proporção (decisão 1 de `importa_npcs_sinnoh.py`).
"Virado para oeste" na fonte aponta para outra coisa aqui. `LOOK_AROUND`
enxerga girando, então o treinador funciona sem que ninguém invente direção.

## Por que reusar o objeto importado em vez de criar objeto novo

A save guarda ÍNDICE de objeto (`objectEvents[]`). Objeto novo só entraria no
fim da lista e o mudo continuaria lá do lado, em dobro. Reusar custa zero
índice, zero byte de `object_event` e zero flag: a flag de "já venci" o motor
deriva sozinho de `TRAINER_FLAGS_START`.

## Alinhamento: a mesma política conservadora de texto_sinnoh.py

Ligar o NOSSO objeto ao DELES é por ORDEM, porque o importador não gravou o
índice de origem. A ordem só vale se nada tiver sido descartado no meio, então o
mapa só entra se a contagem bater E o `graphics_id` bater um a um. Mapa que não
passa fica inteiro de fora: batalha trocada é pior que boneco mudo.

## O clone que fala fica escondido

Cinco vezes o mesmo nome aparece duas vezes na rota: um NPC nativo, escrito à
mão por sessão anterior, com fala inventada, e o importado que agora luta com o
time e a fala do Platinum. É o par que `PENDENCIAS-NPC-SINNOH.md` seção 0
descreve, e o critério de lá é CONTEÚDO, não origem: quem carrega o dado da
fonte fica. O nativo leva `FLAG_SINNOH_NPC_DUPLICADO` no campo `flag` e não
nasce. Zero flag nova, zero objeto apagado, reversível.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import texto_sinnoh as T  # noqa: E402
import valida_mapas_sinnoh as V  # noqa: E402

PLAT = T.PLAT
DADOS_TREINADOR = os.path.join(PLAT, "res/trainers/data")
APLICA = "--aplica" in sys.argv

MUDO = ("0", "0x0", "NULL", "")
SEM_FLAG = ("0", "0x0", "")
FLAG_CLONE = "FLAG_SINNOH_NPC_DUPLICADO"

# Corpo de NPC que só fala. Nada de goto, call, warp, setflag, applymovement ou
# special: esconder um desses poderia tirar um passo do enredo do caminho.
SO_FALA = re.compile(
    r"^\s*lock\s*\n\s*faceplayer\s*\n\s*msgbox\s+\w+,\s*MSGBOX_\w+\s*\n"
    r"\s*release\s*\n\s*end\s*$", re.M)


def camel(bruto, constante):
    """Nome legível do rótulo. Vem do LOCALID do objeto, não da constante.

    Numa dupla os dois objetos compartilham a MESMA constante, e o rótulo tem que
    ser diferente para cada um: `LOCALID_TWIN_EMMA` e `LOCALID_TWIN_LIL`.
    """
    fonte = bruto.get("id") or constante
    fonte = re.sub(r"^(LOCALID_|TRAINER_)", "", fonte)
    return "".join(p.capitalize() for p in fonte.split("_") if p)


def le(caminho):
    with open(caminho, encoding="utf-8", errors="replace") as f:
        return f.read()


def constantes_de_treinador():
    return {m.group(1): int(m.group(2)) for m in re.finditer(
        r"#define\s+(TRAINER_\w+)\s+(\d+)",
        le(os.path.join(REPO, "include/constants/opponents.h")))}


def blocos_com_time():
    """Constante existir NÃO é o jogo ter o time (lição 4.5 do ESTADO.md)."""
    return set(re.findall(r"^=== (\w+) ===", le(
        os.path.join(REPO, "src/data/trainers.party")), re.M))


def usados_em_scripts():
    """Toda constante `TRAINER_SINNOH_*` que algum script de `data/` já cita.

    Reusar uma delas em outro lugar daria duas pessoas com a mesma flag de
    derrotado, e a segunda nasceria já vencida.
    """
    achados = set()
    for raiz, _dirs, arqs in os.walk(os.path.join(REPO, "data")):
        for a in arqs:
            if a.endswith((".inc", ".s")):
                achados |= set(re.findall(r"TRAINER_SINNOH_\w+",
                                          le(os.path.join(raiz, a))))
    return achados


def dados_do_treinador(constante):
    p = os.path.join(DADOS_TREINADOR, constante[len("TRAINER_"):].lower() + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def falas(dados, metade):
    """(intro, derrota, depois, faltou_pokemon, duplo) prontas para `.string`.

    None em qualquer uma que o charmap desta build não desenhe: o chamador recusa
    o treinador inteiro em vez de escrever fala pela metade.
    """
    msg = {m["type"]: m.get("en_US") for m in dados.get("messages", [])}
    duplo = bool(dados.get("double_battle"))
    if duplo:
        s = str(metade if metade in (1, 2) else 1)
        chaves = (f"TRMSG_PRE_DOUBLE_BATTLE_{s}", f"TRMSG_DOUBLE_BATTLE_DEFEAT_{s}",
                  f"TRMSG_POST_DOUBLE_BATTLE_{s}",
                  f"TRMSG_DOUBLE_BATTLE_NOT_ENOUGH_POKEMON_{s}")
    else:
        chaves = ("TRMSG_PRE_BATTLE", "TRMSG_DEFEAT", "TRMSG_POST_BATTLE", None)
    saida = []
    for k in chaves:
        if k is None:
            saida.append(None)
            continue
        if k not in msg:
            return None
        pronto = T.resolve(msg[k], {})
        if pronto is None:
            return None
        saida.append(pronto)
    return tuple(saida) + (duplo,)


def rotulo_livre(usados, mapa, quem):
    """`<Mapa>_EventScript_<Quem>`, com sufixo se o nome já existir.

    `usados` TEM que vir semeado com os rótulos que o `scripts.inc` já tem, e a
    checagem certa é na unidade de montagem inteira, não por arquivo: os 2018
    `scripts.inc` viram um `data/event_scripts.s` só (lição 4.12).
    """
    base = f"{mapa}_EventScript_{quem}"
    cand, n = base, 1
    while any(c in usados for c in (cand, cand.replace("_EventScript_", "_Text_"))):
        n += 1
        cand = f"{base}{n}"
    usados.add(cand)
    return cand


def clone_que_fala(mapa, nativos, nome_proprio, grafico, inc):
    """Índice do NPC nativo que é a MESMA pessoa do treinador, ou None.

    Três condições, todas necessárias: o `local_id` termina no primeiro nome do
    treinador, o gráfico é o mesmo, e o script do nativo é só `lock/faceplayer/
    msgbox/release/end`. Qualquer coisa fora disso e o nativo fica de pé
    (lição 4.10: na dúvida, os dois ficam).
    """
    alvo = nome_proprio.upper()
    for i, o in enumerate(nativos):
        if o.get("origem") == "pokeplatinum" or str(o.get("flag", "0")) not in SEM_FLAG:
            continue
        li = (o.get("local_id") or "").upper()
        if not li.endswith("_" + alvo) or o.get("graphics_id") != grafico:
            continue
        lab = o.get("script") or ""
        corpo = re.search(rf"^{re.escape(lab)}::\n(.*?)(?=\n\S)", inc, re.S | re.M)
        if not corpo or not SO_FALA.match("\n" + corpo.group(1).rstrip()):
            continue
        # Ninguém mais pode citar este local_id: esconder objeto que outro script
        # move ou espera trava a cena dele.
        if len(re.findall(rf"\b{re.escape(o['local_id'])}\b", inc)) > 0:
            continue
        return i
    return None


def plano():
    """[(mapa, [peça]), ...] mais estatística e recusas."""
    sprites = V.sprites_utilizaveis()
    consts, com_time = constantes_de_treinador(), blocos_com_time()
    ja = usados_em_scripts()
    st = dict(fora_do_escopo=0, desalinhado=0, filtrado=0, ja_ligado=0,
              sem_constante=0, sem_time=0, sem_dados=0, sem_texto=0,
              ocupado=0, escondido=0, clones=0, metade_repetida=0)
    saida, recusas = [], []
    # O que ESTA rodada já colocou. Separado de `ja` de propósito: `ja` é o
    # passado e não pode crescer, senão a segunda metade de uma dupla é lida
    # como reuso indevido da constante.
    feitos, feitos_const = set(), set()

    for meu, _header, arq in T.casados():
        # Espelho exato do filtro de `treinadores_masmorra_sinnoh.py`, que pula
        # todo mapa `Route*`: junto, os dois cobrem Sinnoh sem sobreposição.
        if not meu.startswith("Route"):
            st["fora_do_escopo"] += 1
            continue
        pe = os.path.join(PLAT, "res/field/events", arq + ".json")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not (os.path.exists(pe) and os.path.exists(pm)):
            continue
        fonte = json.load(open(pe, encoding="utf-8"))
        brutos = [o for o in fonte.get("object_events", [])
                  if isinstance(o.get("script"), str)
                  and o["script"].startswith("TRAINER_")]
        if not brutos:
            continue
        d = json.load(open(pm, encoding="utf-8"))
        f_npcs, _ = T.separa_fonte(fonte)
        n_npcs = [(i, o) for i, o in enumerate(d.get("object_events", []))
                  if o.get("origem") == "pokeplatinum"]
        if not (len(n_npcs) == len(f_npcs) and
                all(T.sprite_esperado(a, sprites) == b.get("graphics_id")
                    for a, (_, b) in zip(f_npcs, n_npcs))):
            st["desalinhado"] += len(brutos)
            recusas.append((meu, "alinhamento",
                            f"{len(f_npcs)} na fonte contra {len(n_npcs)} aqui"))
            continue

        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        inc = le(ps) if os.path.exists(ps) else ""
        usados = set(re.findall(r"^(\w+)::?", inc, re.M))
        # Identidade por POSIÇÃO dentro de f_npcs, nunca por `in`: os dois
        # objetos de uma dupla podem ser dicionários iguais.
        onde = {id(o): k for k, o in enumerate(f_npcs)}
        pecas, esconder = [], []
        for bruto in brutos:
            nossa = "TRAINER_SINNOH_" + bruto["script"][len("TRAINER_"):]
            metade = bruto.get("double_battle_id", 1)
            # `ja` é o que os scripts de `data/` JÁ citavam antes desta rodada, e
            # nunca cresce: reusar uma dessas daria duas pessoas com a mesma flag
            # de derrotado, e a segunda nasceria vencida. Vem ANTES do filtro do
            # importador para o relatório não acusar de "descartado" quem já luta.
            if nossa in ja:
                st["ja_ligado"] += 1
                continue
            k = onde.get(id(bruto))
            if k is None:
                # `hidden_flag` do Platinum (NPC que a cena faz aparecer),
                # mobília ou nome próprio sem sprite: o objeto nem existe aqui.
                st["filtrado"] += 1
                recusas.append((meu, "descartado pelo importador ("
                                + str(bruto.get("hidden_flag", "0")) + ")",
                                bruto["script"]))
                continue
            pos, obj = n_npcs[k]
            if nossa not in consts:
                st["sem_constante"] += 1
                recusas.append((meu, "sem constante", nossa))
                continue
            if nossa not in com_time:
                st["sem_time"] += 1
                recusas.append((meu, "sem bloco em trainers.party", nossa))
                continue
            if str(obj.get("script", "0")) not in MUDO:
                st["ocupado"] += 1
                continue
            if str(obj.get("flag", "0")) not in SEM_FLAG:
                st["escondido"] += 1
                recusas.append((meu, "objeto importado escondido por flag", nossa))
                continue
            dados = dados_do_treinador(bruto["script"])
            if dados is None:
                st["sem_dados"] += 1
                recusas.append((meu, "sem res/trainers/data", bruto["script"]))
                continue
            # A MESMA constante volta uma segunda vez, e só uma: numa dupla os
            # DOIS bonecos carregam `trainerbattle_double` com o mesmo id (Anna e
            # Meg em Route117 são o precedente vanilla). O que separa os dois é
            # `double_battle_id`; se ele repetir, ou se o treinador não for de
            # batalha dupla, o segundo objeto seria uma batalha simples idêntica
            # à do primeiro, que é bug, e fica de fora.
            if (nossa, metade) in feitos or (nossa in feitos_const
                                             and not dados.get("double_battle")):
                st["metade_repetida"] += 1
                recusas.append((meu, "segunda copia da mesma batalha", nossa))
                continue
            texto = falas(dados, metade)
            if texto is None:
                st["sem_texto"] += 1
                recusas.append((meu, "fala nao traduz", nossa))
                continue
            intro, derrota, depois, faltou, duplo = texto
            lab = rotulo_livre(usados, meu, camel(bruto, bruto["script"]))
            txt = lab.replace("_EventScript_", "_Text_")
            batalha = (f"\ttrainerbattle_double {nossa}, {txt}Intro, {txt}Defeat, "
                       f"{txt}NoPartner\n") if duplo else \
                      f"\ttrainerbattle_single {nossa}, {txt}Intro, {txt}Defeat\n"
            trecho = (f"\n{lab}::\n{batalha}"
                      f"\tmsgbox {txt}Post, MSGBOX_AUTOCLOSE\n\tend\n\n"
                      f'{txt}Intro:\n\t.string "{intro}"\n\n'
                      f'{txt}Defeat:\n\t.string "{derrota}"\n\n'
                      f'{txt}Post:\n\t.string "{depois}"\n')
            bytes_txt = len(intro) + len(derrota) + len(depois)
            if duplo:
                trecho += f'\n{txt}NoPartner:\n\t.string "{faltou}"\n'
                bytes_txt += len(faltou)
            raio = str((bruto.get("data") or [0])[0])
            pecas.append((pos, lab, raio, trecho, bytes_txt, nossa))
            feitos.add((nossa, metade))
            feitos_const.add(nossa)
            primeiro = re.split(r"[ &]", dados.get("name", ""))[0]
            i = clone_que_fala(meu, d.get("object_events") or [], primeiro,
                               obj.get("graphics_id"), inc) if primeiro else None
            if i is not None:
                esconder.append((i, primeiro))
                st["clones"] += 1
        if pecas:
            saida.append((meu, pecas, esconder))
    return saida, st, recusas


def main():
    tudo, st, recusas = plano()
    total = sum(len(p) for _m, p, _e in tudo)
    bytes_txt = sum(x[4] for _m, p, _e in tudo for x in p)
    duplos = len({x[5] for _m, p, _e in tudo for x in p})
    print(f"treinadores de rota a ligar: {total} em {len(tudo)} mapas "
          f"({duplos} constantes distintas; a diferenca sao as metades de dupla)")
    print(f"clones nativos a esconder com {FLAG_CLONE}: "
          f"{sum(len(e) for _m, _p, e in tudo)}")
    print(f"custo de texto: {bytes_txt} B de .string ({bytes_txt / 1024:.1f} KB)")
    print("zero id novo, zero flag nova, zero objeto novo")
    print("nao entram: " + "  ".join(f"{k}={v}" for k, v in st.items() if v))
    for meu, pecas, esconder in tudo:
        print(f"  {meu:24s} {len(pecas):2d} treinador(es)"
              + (f"   esconde {[e[1] for e in esconder]}" if esconder else ""))
    if recusas:
        print("\nrecusados:")
        for r in recusas:
            print("   ", *r)

    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    feitos = escondidos = recusados = 0
    for meu, pecas, esconder in tudo:
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        # Releitura tardia: outro agente pode ter mexido no mesmo map.json entre
        # o planejamento e agora. Só o objeto que CONTINUA importado, mudo e sem
        # flag é trocado; qualquer outra coisa é recusada em vez de sobrescrita.
        atual = json.load(open(pm, encoding="utf-8"))
        lista = atual.get("object_events") or []
        corpo, n = "", 0
        for pos, lab, raio, trecho, _b, _c in pecas:
            if pos >= len(lista):
                recusados += 1
                continue
            ev = lista[pos]
            if ev.get("origem") != "pokeplatinum" \
                    or str(ev.get("script", "0")) not in MUDO \
                    or str(ev.get("flag", "0")) not in SEM_FLAG:
                recusados += 1
                continue
            ev["script"] = lab
            ev["trainer_type"] = "TRAINER_TYPE_NORMAL"
            ev["trainer_sight_or_berry_tree_id"] = raio
            corpo += trecho
            n += 1
        if not n:
            continue
        for i, _nome in esconder:
            if i < len(lista) and str(lista[i].get("flag", "0")) in SEM_FLAG \
                    and lista[i].get("origem") != "pokeplatinum":
                lista[i]["flag"] = FLAG_CLONE
                escondidos += 1
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(atual, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(os.path.join(REPO, "data/maps", meu, "scripts.inc"), "a",
                  encoding="utf-8") as f:
            f.write("\n@ Treinador de rota do pokeplatinum: time, raio de visao e "
                    "fala\n@ (dev_scripts/treinadores_rota_sinnoh.py)\n" + corpo)
        feitos += n
    print(f"\nligados: {feitos}   clones escondidos: {escondidos}   "
          f"recusados na releitura: {recusados}")
    return 0


def demo():
    """Uma armadilha por caso, todas medidas na fonte."""
    # 1. o rótulo sai do LOCALID do objeto, não da constante: numa dupla os dois
    #    objetos compartilham a constante e precisam de rótulos diferentes.
    a = {"id": "LOCALID_TWIN_EMMA"}
    b = {"id": "LOCALID_TWIN_LIL"}
    assert camel(a, "TRAINER_TWINS_EMMA_AND_LIL") == "TwinEmma"
    assert camel(b, "TRAINER_TWINS_EMMA_AND_LIL") == "TwinLil"
    assert camel({}, "TRAINER_LASS_SARAH") == "LassSarah"

    # 2. rótulo tem que pular nome já ocupado, e o par _Text_ conta tanto quanto
    #    o _EventScript_ (lição 4.12: existir não é ser único)
    ja = {"Foo_EventScript_HikerLouis", "Foo_Text_HikerLouis2"}
    assert rotulo_livre(ja, "Foo", "HikerLouis") == "Foo_EventScript_HikerLouis3"

    # 3. constante existir NÃO é ter time (lição 4.5): os dois conjuntos saem de
    #    arquivos diferentes de propósito.
    consts, times = constantes_de_treinador(), blocos_com_time()
    orfas = [c for c in consts if c.startswith("TRAINER_SINNOH_") and c not in times]
    assert not orfas, f"{len(orfas)} constante(s) de Sinnoh sem bloco: {orfas[:5]}"

    # 4. id de treinador tem que caber embaixo do teto, senão `gTrainers` é lido
    #    fora do array. O teto desta build é 2500, não 3000.
    teto = int(re.search(r"#define\s+MAX_TRAINERS_COUNT_EMERALD\s+(\d+)", le(
        os.path.join(REPO, "include/constants/opponents.h"))).group(1))
    acima = [c for c, n in consts.items() if n >= teto]
    assert not acima, f"id acima de MAX_TRAINERS_COUNT ({teto}): {acima[:5]}"

    # 5. a metade da dupla vem de `double_battle_id`, NUNCA da ordem no arquivo.
    #    Em Route209 o objeto da Sue (metade 2) vem antes do do Ty (metade 1).
    ev = json.load(open(os.path.join(
        PLAT, "res/field/events/events_route_209.json"), encoding="utf-8"))
    par = [o for o in ev["object_events"]
           if o.get("script") == "TRAINER_YOUNG_COUPLE_TY_AND_SUE"]
    assert [o["double_battle_id"] for o in par] == [2, 1], \
        "a ordem no arquivo deixou de contradizer o double_battle_id"
    d = dados_do_treinador("TRAINER_YOUNG_COUPLE_TY_AND_SUE")
    assert falas(d, 1)[0].startswith("Ty:") and falas(d, 2)[0].startswith("Sue:")

    # 6. batalha dupla exige o texto de "faltou Pokémon", senão o macro
    #    `trainerbattle_double` não monta; batalha simples não tem esse texto.
    assert falas(d, 1)[3] and falas(d, 1)[4]
    s = falas(dados_do_treinador("TRAINER_LASS_SARAH"), 1)
    assert s[3] is None and not s[4] and s[0].endswith("$")

    # 7. a fala sai da fonte, nunca daqui.
    cru = [m for m in dados_do_treinador("TRAINER_LASS_SARAH")["messages"]
           if m["type"] == "TRMSG_PRE_BATTLE"][0]
    assert cru["en_US"][0].split()[1] in s[0], "a intro nao e a da fonte"

    # 8. raio de visão é `data[0]`, e `data` vazio é raio 0 (legítimo: o
    #    Fisherman Juan de Route212 só luta quando falam com ele).
    ev = json.load(open(os.path.join(
        PLAT, "res/field/events/events_route_212_south.json"), encoding="utf-8"))
    juan = [o for o in ev["object_events"]
            if o.get("script") == "TRAINER_FISHERMAN_JUAN"][0]
    assert (juan.get("data") or [0])[0] == 0

    # 9. a checagem na camada da afirmação: nenhum rótulo pode estar definido
    #    duas vezes na unidade de montagem inteira de `data/event_scripts.s`.
    repetidos = T.rotulos_repetidos()
    assert not repetidos, (f"{len(repetidos)} rotulo(s) duplicado(s), o build "
                           f"reprova: {repetidos[:5]}")

    # 10. todo `script` citado num map.json de rota de Sinnoh existe no
    #     scripts.inc do MESMO mapa, e todo texto novo fecha com `$`.
    faltando = []
    for meu, _h, _a in T.casados():
        if not meu.startswith("Route"):
            continue
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        if not os.path.exists(pm):
            continue
        inc = le(ps) if os.path.exists(ps) else ""
        rot = set(re.findall(r"^(\w+)::?", inc, re.M))
        d = json.load(open(pm, encoding="utf-8"))
        for o in (d.get("object_events") or []) + (d.get("bg_events") or []):
            s = str(o.get("script", "0"))
            if s in MUDO or "_EventScript_" not in s or s.startswith("Sinnoh_"):
                continue
            if s not in rot:
                faltando.append((meu, s))
        # `$` fecha o BLOCO, não cada linha: `.string` seguidas são um texto só,
        # e exigir `$` em todas reprovaria o repo inteiro pelo motivo errado.
        for bloco in re.findall(r'^(\w+:\n(?:\t\.string ".*"\n)+)', inc, re.M):
            assert bloco.rstrip().endswith('$"'), f"{meu}: texto sem $ final"
    assert not faltando, f"script citado e inexistente: {faltando[:5]}"

    print("demo ok (10 casos; unidade de montagem conferida, zero rotulo "
          "duplicado, zero script fantasma nas rotas de Sinnoh)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
