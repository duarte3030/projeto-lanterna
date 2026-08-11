#!/usr/bin/env python3
"""Liga os treinadores de MASMORRA, PRÉDIO e GINÁSIO de Sinnoh.

Uso:
    python3 dev_scripts/treinadores_masmorra_sinnoh.py            # só relata
    python3 dev_scripts/treinadores_masmorra_sinnoh.py --aplica
    python3 dev_scripts/treinadores_masmorra_sinnoh.py --demo

## O buraco que este arquivo fecha

No Platinum o campo `script` de um objeto pode ser DUAS coisas diferentes: um
índice numérico dentro do arquivo de scripts do mapa, ou a constante `TRAINER_*`
do treinador que aquele boneco é. `importa_npcs_sinnoh.py` só sabia ler a
primeira, então todo treinador entrou aqui com `script: "0"` e
`TRAINER_TYPE_NONE`: boneco mudo em cima do qual dá para passar andando.

## O que este script NÃO precisou fazer, e a medida que provou

O enunciado da tarefa mandava copiar o bloco `=== TRAINER_... ===` do acervo
`src/data/trainers_sinnoh.party` para `src/data/trainers.party` e declarar a
constante em `include/constants/opponents.h` numa faixa nova de id. **Medido
antes de escrever uma linha: os 425 `TRAINER_SINNOH_*` já estão declarados
(855 a 1315) e os 425 já têm bloco em `trainers.party`.** Sessão anterior já
tinha feito essa metade. Criar id novo para eles duplicaria time e texto na ROM
e daria duas flags de "já venci" para a mesma pessoa. Então este script **não
toca em `trainers.party` nem em `opponents.h`**, e a faixa 2550-2749 continua
livre. O que falta é só a ligação: objeto do mapa -> script -> constante.

## De onde sai cada campo (medido, não lembrado)

- **quem é treinador**: `res/field/events/events_<mapa>.json`, objeto cujo
  `script` é `str` e começa com `TRAINER_`.
- **raio de visão**: primeiro elemento de `data` do MESMO objeto (`data: [3]` no
  Youngster Jonathon do ginásio de Oreburgh). Sem `data`, o raio é 0 e o
  treinador só luta quando falam com ele; o Platinum tem 7 assim.
- **direção**: `movement_type` da fonte. `LOOK_SOUTH/NORTH/WEST/EAST` viram
  `MOVEMENT_TYPE_FACE_DOWN/UP/LEFT/RIGHT`. Raio de visão só enxerga para onde o
  boneco ESTÁ virado, e o importador achatou todo mundo em `LOOK_AROUND`; quem
  não tem tradução direta fica como está (roda no lugar, e enxerga girando).
- **fala de antes, de derrota e de depois**: `res/trainers/data/<slug>.json`,
  campo `messages`, tipos `TRMSG_PRE_BATTLE`, `TRMSG_DEFEAT` e
  `TRMSG_POST_BATTLE`. Não é o banco de texto do mapa: em gen 4 o motor cuida do
  treinador sozinho e a fala mora junto com o time dele. **Nada de texto novo.**

## Por que reusa o objeto importado em vez de criar objeto novo

A save guarda ÍNDICE de objeto (`objectEvents[]`). Objeto novo só pode entrar no
fim da lista, e o mudo continuaria lá do lado do treinador, em dobro. Reusar o
mudo custa zero índice, zero byte de `object_event` e zero flag: a flag de
"já venci" é derivada de `TRAINER_FLAGS_START` pelo próprio motor.

## Alinhamento: a mesma política conservadora de texto_sinnoh.py

Ligar o NOSSO objeto ao DELES é por ORDEM, porque o importador não gravou o
índice de origem. A ordem só vale se nada tiver sido descartado no meio, então o
mapa só entra se a contagem bater E o `graphics_id` bater um a um. Mapa que não
passa fica inteiro de fora: batalha trocada é pior que boneco mudo.
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

# `data[0]` do objeto e a direcao inicial. So estes quatro tem equivalente
# honesto aqui; o resto (WANDER_*, WALK_*, LOOK_NORTH_AND_EAST) fica como o
# importador deixou, porque inventar direcao muda quem o treinador enxerga.
DIRECAO = {
    "MOVEMENT_TYPE_LOOK_SOUTH": "MOVEMENT_TYPE_FACE_DOWN",
    "MOVEMENT_TYPE_LOOK_NORTH": "MOVEMENT_TYPE_FACE_UP",
    "MOVEMENT_TYPE_LOOK_WEST": "MOVEMENT_TYPE_FACE_LEFT",
    "MOVEMENT_TYPE_LOOK_EAST": "MOVEMENT_TYPE_FACE_RIGHT",
}

MUDO = ("0", "0x0", "NULL", "")
SEM_FLAG = ("0", "0x0", "")


def camel(nome):
    """TRAINER_YOUNGSTER_JONATHON -> YoungsterJonathon."""
    return "".join(p.capitalize() for p in nome[len("TRAINER_"):].split("_") if p)


def constantes_de_treinador():
    txt = open(os.path.join(REPO, "include/constants/opponents.h"),
               encoding="utf-8", errors="replace").read()
    return {m.group(1): int(m.group(2))
            for m in re.finditer(r"#define\s+(TRAINER_\w+)\s+(\d+)", txt)}


def blocos_com_time():
    """Nome de todo treinador que TEM bloco no arquivo que compila.

    Constante existir não é o jogo ter o time (lição 4.5 do ESTADO.md):
    treinador sem bloco cai em cima de quem já ocupa o id.
    """
    txt = open(os.path.join(REPO, "src/data/trainers.party"),
               encoding="utf-8", errors="replace").read()
    return set(re.findall(r"^=== (\w+) ===", txt, re.M))


def usados_em_scripts():
    """Toda constante TRAINER_SINNOH_* que algum script JÁ cita.

    Reusar uma delas noutro lugar daria duas pessoas com a mesma flag de
    derrotado. Varre `data/` inteiro porque a frente da Galáctica pôs vários
    grunts do interior no mapa de fora (o grunt do LakeValorDrained mora hoje em
    `data/maps/LakeValor/scripts.inc`).
    """
    achados = set()
    for raiz, _dirs, arqs in os.walk(os.path.join(REPO, "data")):
        for a in arqs:
            if a.endswith((".inc", ".s")):
                with open(os.path.join(raiz, a), errors="replace") as f:
                    achados |= set(re.findall(r"TRAINER_SINNOH_\w+", f.read()))
    return achados


def falas(constante_platinum):
    """(intro, derrota, depois, faltou_pokemon) já prontas para `.string`.

    Devolve None em qualquer uma que o charmap desta build não desenhe; o
    chamador recusa o treinador inteiro em vez de escrever fala pela metade.
    """
    p = os.path.join(DADOS_TREINADOR,
                     constante_platinum[len("TRAINER_"):].lower() + ".json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    msg = {m["type"]: m.get("en_US") for m in d.get("messages", [])}
    duplo = bool(d.get("double_battle"))
    if duplo:
        chaves = ("TRMSG_PRE_DOUBLE_BATTLE_1", "TRMSG_DOUBLE_BATTLE_DEFEAT_1",
                  "TRMSG_POST_DOUBLE_BATTLE_1",
                  "TRMSG_DOUBLE_BATTLE_NOT_ENOUGH_POKEMON_1")
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
    checagem é na unidade de montagem inteira, não por arquivo: os 2018
    `scripts.inc` viram um `data/event_scripts.s` só (lição 4.12).
    """
    base = f"{mapa}_EventScript_{quem}"
    n, cand = 1, base
    while any(c in usados for c in (cand, cand.replace("_EventScript_", "_Text_"))):
        n += 1
        cand = f"{base}{n}"
    usados.add(cand)
    return cand


def alvos():
    """(mapa, [(indice do nosso objeto, objeto da fonte, constante nossa)])."""
    sprites = V.sprites_utilizaveis()
    consts = constantes_de_treinador()
    com_time = blocos_com_time()
    ja = usados_em_scripts()
    st = dict(fora_do_escopo=0, sem_par=0, desalinhado=0, filtrado=0,
              ja_ligado=0, sem_constante=0, sem_time=0, sem_texto=0,
              ocupado=0, escondido=0)
    plano, recusas = [], []

    for meu, _header, arq in T.casados():
        if meu.startswith("Route"):
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

        # Identidade por posicao dentro de f_npcs, nao por `in`: dois objetos da
        # fonte podem ser dicionarios iguais (o par de batalha dupla e).
        onde = {id(o): k for k, o in enumerate(f_npcs)}
        do_mapa = []
        for bruto in brutos:
            k = onde.get(id(bruto))
            if k is None:
                st["filtrado"] += 1  # hidden_flag, sprite proibido ou nome proprio
                continue
            nossa = "TRAINER_SINNOH_" + bruto["script"][len("TRAINER_"):]
            pos, obj = n_npcs[k]
            if str(obj.get("script", "0")) not in MUDO:
                st["ocupado"] += 1
                continue
            if str(obj.get("flag", "0")) not in SEM_FLAG:
                st["escondido"] += 1
                recusas.append((meu, "objeto escondido por flag", nossa))
                continue
            if any(nossa == c for _p, _b, c, _t in do_mapa):
                # Batalha dupla: os dois bonecos do par carregam a MESMA
                # constante na fonte. Aqui os dois apontam para o MESMO
                # EventScript, que e um `trainerbattle_double`; o segundo nao
                # gera texto nem id novo. Deixar o parceiro mudo do lado do
                # treinador era o defeito que este ramo evita.
                do_mapa.append((pos, bruto, nossa, None))
                continue
            if nossa in ja:
                st["ja_ligado"] += 1
                continue
            if nossa not in consts:
                st["sem_constante"] += 1
                recusas.append((meu, "sem constante", nossa))
                continue
            if nossa not in com_time:
                st["sem_time"] += 1
                recusas.append((meu, "sem bloco em trainers.party", nossa))
                continue
            texto = falas(bruto["script"])
            if texto is None:
                st["sem_texto"] += 1
                recusas.append((meu, "fala nao traduz", nossa))
                continue
            do_mapa.append((pos, bruto, nossa, texto))
            ja.add(nossa)   # o par de batalha dupla so entra uma vez
        if do_mapa:
            plano.append((meu, do_mapa))
    return plano, st, recusas


def monta(meu, do_mapa, nossos):
    """[(indice, rotulo, raio, direcao ou None, trecho, bytes de texto)].

    Uma peça por treinador, para que a escrita possa recusar um sem descartar os
    vizinhos: só o trecho de quem realmente entrou no `map.json` vai para o
    `scripts.inc`.
    """
    ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
    usados = set(re.findall(r"^(\w+)::?", open(ps, errors="replace").read(), re.M)) \
        if os.path.exists(ps) else set()
    pecas, ja_escrito = [], {}
    for pos, bruto, nossa, texto in do_mapa:
        # Parceiro de batalha dupla: mesmo rotulo, nenhum texto novo.
        if texto is None:
            lab = ja_escrito[nossa]
            raio = str((bruto.get("data") or [0])[0])
            no_lugar = (nossos[pos].get("x"), nossos[pos].get("y")) == \
                (bruto.get("x"), bruto.get("z"))
            pecas.append((pos, lab, raio,
                          DIRECAO.get(bruto.get("movement_type")) if no_lugar
                          else None, "", 0))
            continue
        intro, derrota, depois, faltou, duplo = texto
        lab = rotulo_livre(usados, meu, camel(bruto["script"]))
        ja_escrito[nossa] = lab
        txt = lab.replace("_EventScript_", "_Text_")
        if duplo:
            batalha = (f"\ttrainerbattle_double {nossa}, {txt}Intro, "
                       f"{txt}Defeat, {txt}NoPartner\n")
        else:
            batalha = f"\ttrainerbattle_single {nossa}, {txt}Intro, {txt}Defeat\n"
        trecho = (f"\n{lab}::\n{batalha}"
                  f"\tmsgbox {txt}Post, MSGBOX_AUTOCLOSE\n\tend\n\n"
                  f'{txt}Intro:\n\t.string "{intro}"\n\n'
                  f'{txt}Defeat:\n\t.string "{derrota}"\n\n'
                  f'{txt}Post:\n\t.string "{depois}"\n')
        b = len(intro) + len(derrota) + len(depois)
        if duplo:
            trecho += f'\n{txt}NoPartner:\n\t.string "{faltou}"\n'
            b += len(faltou)
        raio = str((bruto.get("data") or [0])[0])
        # A direção da fonte só vale se o boneco estiver na coordenada da fonte.
        # Nos interiores de planta REAPROVEITADA (ginásio de Hearthome, salas de
        # Sunyshore, Oreburgh Gate, Café) o importador teve que reposicionar, e
        # ali "virado para oeste" aponta para outra parede: nesses fica o
        # `LOOK_AROUND` que o importador deixou, que enxerga girando.
        no_lugar = (nossos[pos].get("x"), nossos[pos].get("y")) == \
            (bruto.get("x"), bruto.get("z"))
        direcao = DIRECAO.get(bruto.get("movement_type")) if no_lugar else None
        pecas.append((pos, lab, raio, direcao, trecho, b))
    return pecas


def main():
    plano, st, recusas = alvos()
    total = sum(len(v) for _m, v in plano)
    escrita, bytes_txt, girando = {}, 0, 0
    for meu, do_mapa in plano:
        nossos = json.load(open(os.path.join(REPO, "data/maps", meu, "map.json"),
                                encoding="utf-8"))["object_events"]
        pecas = monta(meu, do_mapa, nossos)
        escrita[meu] = pecas
        bytes_txt += sum(p[5] for p in pecas)
        girando += sum(1 for p in pecas if p[3] is None)

    espelhos = sum(1 for _m, v in plano for p in v if p[3] is None)
    print(f"objetos a ligar: {total} em {len(plano)} mapas "
          f"({total - espelhos} treinadores; {espelhos} parceiro(s) de "
          f"batalha dupla apontando para o mesmo script)")
    print(f"direcao portada da fonte: {total - girando}; "
          f"sem direcao portada (fica LOOK_AROUND): {girando}")
    print(f"custo de texto: {bytes_txt} B de .string "
          f"(~{bytes_txt / 1024:.1f} KB antes da compressao de rotulo)")
    print("nao entram: " + "  ".join(f"{k}={v}" for k, v in st.items() if v))
    for meu, do_mapa in plano:
        print(f"  {meu:34s} {len(do_mapa):2d}")
    if recusas:
        print("\nrecusados:")
        for r in recusas:
            print("   ", *r)

    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    feitos = recusados = 0
    for meu, pecas in escrita.items():
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        # Releitura tardia: outro agente pode ter mexido no mesmo map.json entre
        # o planejamento e agora. Só o objeto que CONTINUA importado e mudo é
        # trocado; qualquer outra coisa é recusada em vez de sobrescrita.
        atual = json.load(open(pm, encoding="utf-8"))
        lista = atual.get("object_events") or []
        corpo, n = "", 0
        for pos, lab, raio, direcao, trecho, _b in pecas:
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
            if direcao:
                ev["movement_type"] = direcao
            corpo += trecho
            n += 1
        if not n:
            continue
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(atual, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(os.path.join(REPO, "data/maps", meu, "scripts.inc"), "a",
                  encoding="utf-8") as f:
            f.write("\n@ Treinador do pokeplatinum: time, raio de visao e fala\n"
                    "@ (dev_scripts/treinadores_masmorra_sinnoh.py)\n" + corpo)
        feitos += n
    print(f"\nligados: {feitos}   recusados na releitura: {recusados}")
    return 0


def demo():
    """As armadilhas que este script tinha que evitar, cada uma com um caso."""
    # 1. camel() tem que virar nome de rotulo legivel, sem o prefixo
    assert camel("TRAINER_YOUNGSTER_JONATHON") == "YoungsterJonathon"

    # 2. rotulo tem que pular nome ja ocupado, e o par _Text_ conta tanto quanto
    #    o _EventScript_ (licao 4.12: existir nao e ser unico)
    ja = {"Foo_EventScript_HikerMike", "Foo_Text_HikerMike2"}
    assert rotulo_livre(ja, "Foo", "HikerMike") == "Foo_EventScript_HikerMike3"

    # 3. constante existir NAO e ter time (licao 4.5). Os dois conjuntos vem de
    #    arquivos diferentes de proposito.
    consts, times = constantes_de_treinador(), blocos_com_time()
    orfas = [c for c in consts if c.startswith("TRAINER_SINNOH_") and c not in times]
    assert not orfas, f"{len(orfas)} constante(s) de Sinnoh sem bloco: {orfas[:5]}"

    # 4. a faixa 2550-2749 desta frente tem que continuar VAZIA: os treinadores
    #    de Sinnoh ja tinham id, e criar id novo duplicaria time e flag.
    faixa = [c for c, n in consts.items() if 2550 <= n <= 2749]
    assert not faixa, f"faixa 2550-2749 deixou de ser livre: {faixa[:5]}"

    # 5. a fala sai da fonte, nunca daqui. Um treinador conhecido, conferido
    #    contra o arquivo de dados do Platinum.
    f = falas("TRAINER_YOUNGSTER_JONATHON")
    assert f is not None and f[0].endswith("$") and not f[4]
    bruto = json.load(open(os.path.join(DADOS_TREINADOR, "youngster_jonathon.json"),
                           encoding="utf-8"))
    cru = [m for m in bruto["messages"] if m["type"] == "TRMSG_PRE_BATTLE"][0]
    assert cru["en_US"][0].split()[0] in f[0], "a intro nao e a da fonte"

    # 6. batalha dupla usa o outro conjunto de mensagens e exige o texto de
    #    "faltou Pokemon", senao o macro trainerbattle_double nao monta
    dup = falas("TRAINER_DOUBLE_TEAM_AL_AND_KAY")
    assert dup is not None and dup[4] and dup[3] and dup[3].endswith("$")

    # 7. raio de visao 0 e legitimo: 7 treinadores do Platinum nao tem `data`,
    #    e eles lutam quando falam com eles
    assert str(({}.get("data") or [0])[0]) == "0"

    # 8. e a checagem na camada do assembler: nenhum rotulo duplicado na unidade
    #    de montagem inteira depois do que este script escreveu
    repetidos = T.rotulos_repetidos()
    assert not repetidos, (f"{len(repetidos)} rotulo(s) duplicado(s), o build "
                           f"reprova: {repetidos[:5]}")
    print("demo ok (faixa 2550-2749 livre, zero constante sem time, "
          "zero rotulo duplicado)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
