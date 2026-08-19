#!/usr/bin/env python3
"""Devolve a Johto as item balls que a importação achatou, uma flag por bola.

Bloco J2 da onda de JANELA ABERTA (18/08/2026). O plano falava em "as 1362 item
balls de Johto, Sinnoh e Unova entram 1:1". A MEDIÇÃO derrubou o número e a
geografia, e quem mede manda (lição 1 do ESTADO 0.f):

- 1431 `object_events` com `OBJ_EVENT_GFX_ITEM_BALL` e `flag: 0` existem, sim.
  Mas 1372 deles têm `script: "0"` e `trainer_sight_or_berry_tree_id: "0"`: não
  dão item nenhum, porque `Std_FindItem` nem é chamado. Não duplicam nada, e dar
  flag a eles gastaria 1372 endereços para não mudar UM bit de comportamento.
  Eles são o estrago conhecido do `dev_scripts/sanitize_johto_map_json.py`, que
  achatou TODO objeto de Johto em item ball muda (ver
  `dev_scripts/restaura_npcs_johto.py`, que devolve os que eram GENTE).
- Dos 1372 achatados, 1364 casam por coordenada exata com um objeto da fonte
  `hns`, e só 161 são BOLA na fonte (98 `OBJ_EVENT_GFX_POKE_BALL` mais 63
  `OBJ_EVENT_GFX_ITEM_BALL`). O resto é efeito de luz, pedra de Rock Smash,
  canteiro de berry, Pokémon de overworld e NPC: outra frente.
- Os 48 restantes com `flag: 0` são o Battle Pyramid de Hoenn
  (`gMapGroup_IndoorDynamic`), dinâmico de propósito, e os 11 últimos são NPCs
  de Unova que ganharam sprite de bola por falta de mapeamento. Nenhum dos dois
  é item ball.
- Sinnoh e Unova NÃO têm nada a consertar: as 764 bolas COM script deste repo
  foram resolvidas numericamente uma a uma (apelido e expressão
  `FLAG_ITEMS_UNOVA_START + 0xNNN`) e CINCO números se repetem: o 0 dos 48
  do Battle Pyramid, os três `FLAG_INICIAL_*` das trincas de inicial (pegar um
  inicial some com os três), e o **0x3C, `FLAG_GALACTICA_QG_CHAVE`**, dividido
  entre a única item ball do QG da Galáctica e DOIS NPCs guardas, um no 2F e
  outro no 3F. Também é desenho, e está escrito em
  `data/maps/GalacticHQ_2F/scripts.inc:5`: a Poke Ball do dormitório é a chave,
  o `finditem` acende a flag do objeto de onde o item saiu, e é essa mesma flag
  que apaga os dois guardas. Zero var, nenhum `coord_event`.

  **O 0x3C foi achado pelo adversarial da onda, não por este censo, e o que
  importa é o MÉTODO.** A conta original era bola contra bola, e bola contra
  bola é CEGA para bola contra NPC: `Std_FindItem` termina em `removeobject`,
  que chama `FlagSet(flagId)`, e qualquer objeto do jogo com aquele mesmo
  número de flag some junto, seja ele bola, guarda, pedra ou canteiro. O
  censo certo agrupa por número de flag TODO `object_event` de `data/maps/`
  com `flag` diferente de 0, resolvendo o nome pelo pré-processador (apelido e
  expressão `base + deslocamento` não se comparam por texto), e olha os grupos
  MISTOS: bola com script de um lado, qualquer outra coisa do outro. Medido
  assim em 18/08/2026 pelo J9: grupo misto existe UM, o 0x3C acima.

Então o defeito real, e o único, é este: 161 item balls de Johto perderam o
script, o item e a flag na importação. Esta ferramenta devolve os três, com uma
flag própria por bola, na faixa que o J1 reservou (`FLAG_ITEM_BALLS_JSU_START`).

Por que a flag é obrigatória junto com o script: `Std_FindItem` termina em
`removeobject VAR_LAST_TALKED` -> `RemoveObjectEventByLocalIdAndMap` ->
`FlagSet(flagId)` (src/event_object_movement.c:1700). Com `flag: 0`,
`GetFlagPointer(0)` devolve NULL (src/event_data.c:229) e o `FlagSet` vira
no-op: a bola renasce a cada entrada no mapa e o item duplica sem limite. Foi
exatamente o que aconteceu com Kanto antes do `liga_flags_kanto.py`.

ENDEREÇO GRAVADO É HISTÓRIA. `alias_ja_gravados()` relê o bloco desta
ferramenta em `flags.h` e devolve a cada bola já apelidada o MESMO apelido e o
MESMO endereço, aconteça o que acontecer com a fonte. Bola nova entra em append
depois do maior offset já usado. Rodar duas vezes não renumera nada.

Uso:
    python3 dev_scripts/liga_bolas_johto.py            # só relata
    python3 dev_scripts/liga_bolas_johto.py --aplica
    python3 dev_scripts/liga_bolas_johto.py --demo
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HNS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"
FLAGS_H = f"{REPO}/include/constants/flags.h"
CENSO = f"{REPO}/dev_scripts/bolas_johto.json"

APLICA = "--aplica" in sys.argv

ABRE = ("// >>> Onda de JANELA ABERTA, bloco J2 (18/08/2026): uma flag por item "
        "ball de\n// Johto, gerado por dev_scripts/liga_bolas_johto.py >>>")
FECHA = "// <<< Onda de JANELA ABERTA, bloco J2 <<<"

BOLA = ("OBJ_EVENT_GFX_ITEM_BALL", "OBJ_EVENT_GFX_POKE_BALL")
GFX = "OBJ_EVENT_GFX_ITEM_BALL"
SCRIPT = "Common_EventScript_FindItem"

# Item da fonte que existe aqui com outro nome. Uma linha por tradução, e cada
# uma é uma AFIRMAÇÃO sobre o que o item é, não um apelido de conveniência.
SUBST_ITEM = {
    # Gen 2 tinha duas Exp. Share; a "SMALL" é a que se segura em um Pokémon,
    # que é justamente o ITEM_EXP_SHARE do expansion (ITEM_EXP_ALL é o apelido
    # Gen 1 da versão que divide com o time inteiro).
    "ITEM_EXP_SHARE_SMALL": "ITEM_EXP_SHARE",
}

# Item da fonte que NÃO existe aqui e não tem tradução honesta. A bola fica como
# está (achatada), e a dívida fica escrita no censo em vez de virar item errado.
FORA = {
    "ITEM_GS_BALL": ("o expansion não tem GS Ball; escolher outra bola mudaria "
                     "conteúdo, e inventar item é outra obra"),
}


def texto(p):
    return open(p, encoding="utf-8").read()


def corpos_da_fonte():
    """`rótulo -> corpo` de todo script da fonte, para achar o `finditem`."""
    import glob
    out = {}
    for p in (glob.glob(f"{HNS}/data/maps/*/scripts.inc")
              + glob.glob(f"{HNS}/data/scripts/*.inc")):
        for m in re.finditer(r"^(\w+)::[ \t]*\n((?:(?!^\w+::).*\n)*)",
                             open(p, errors="replace").read(), re.M):
            out.setdefault(m.group(1), m.group(2))
    return out


ITEM_DO_FINDITEM = re.compile(r"\bfinditem\s+(ITEM_\w+)(?:\s*,\s*(\d+))?")


def achatada(obj):
    """Bola muda: sprite de bola, sem script, sem item e sem flag.

    As três pernas juntas, e não uma só. Objeto com script é NPC ou bola que já
    funciona; objeto com flag já tem endereço e não é assunto desta ferramenta.
    """
    return (obj.get("graphics_id") == GFX
            and str(obj.get("script", "0")) in ("0", "")
            and str(obj.get("flag", "0")) == "0")


def nossa(obj, mapa, ja):
    """Bola que esta ferramenta já escreveu: mesma chave E mesmo apelido.

    Comparar o apelido junto, e não só a coordenada, para que uma bola que outra
    frente reaproveitou (script próprio, flag de cena) não seja recapturada.
    """
    reg = ja.get((mapa, obj.get("x"), obj.get("y")))
    return bool(reg) and obj.get("graphics_id") == GFX \
        and str(obj.get("flag")) == reg[0]


def eh_bola_na_fonte(obj, corpos):
    """Par da fonte que é bola DE VERDADE: sprite de bola e `finditem` no script.

    Sprite sozinho não basta: a fonte usa sprite de bola para o Pokémon parado
    do Dragon's Den e para o efeito de luz. Quem decide é o `finditem`.
    """
    if obj.get("graphics_id") not in BOLA:
        return None
    m = ITEM_DO_FINDITEM.search(corpos.get(str(obj.get("script", "")), ""))
    return m if m else None


def fonte_bolas(ja=None):
    """Uma entrada por bola achatada aqui que é bola com `finditem` na fonte.

    Bola que ESTA ferramenta já escreveu deixa de ser achatada (ganhou script,
    item e flag), e por isso `ja` entra aqui: sem ele, a segunda rodada acharia
    zero bolas e o `--aplica` apagaria o bloco inteiro de flags.h, que é
    exatamente o desastre que `alias_ja_gravados()` existe para impedir.
    """
    import glob
    ja = alias_ja_gravados() if ja is None else ja
    corpos = corpos_da_fonte()
    achado = []
    for p in sorted(glob.glob(f"{REPO}/data/maps/*/map.json")):
        mapa = os.path.basename(os.path.dirname(p))
        fp = f"{HNS}/data/maps/{mapa}/map.json"
        if not os.path.exists(fp):
            continue
        nossos = [o for o in json.load(open(p)).get("object_events", [])
                  if achatada(o) or nossa(o, mapa, ja)]
        if not nossos:
            continue
        na_coord = defaultdict(list)
        for o in json.load(open(fp)).get("object_events", []):
            na_coord[(o.get("x"), o.get("y"))].append(o)
        for o in nossos:
            for c in na_coord[(o["x"], o["y"])][:1]:
                m = eh_bola_na_fonte(c, corpos)
                if not m:
                    continue
                achado.append(dict(mapa=mapa, x=o["x"], y=o["y"],
                                   item=m.group(1), qtd=int(m.group(2) or 1),
                                   flag_fonte=str(c.get("flag", "")),
                                   script_fonte=str(c.get("script", ""))))
    return achado


ALIAS_GRAVADO = re.compile(
    r"#define\s+(FLAG_ITEM_JOHTO_\w+)\s+\(FLAG_ITEM_BALLS_JSU_START \+ "
    r"(0x[0-9A-Fa-f]{3})\)\s*//\s*(\S+)\s+(-?\d+),(-?\d+)\s")


def alias_ja_gravados(t=None):
    """`(mapa, x, y) -> (apelido, offset)` do que já saiu gravado em flags.h.

    Existe porque ENDEREÇO DE FLAG GRAVADA É HISTÓRIA. A alocação sai da fonte
    e da varredura de `data/maps`; as duas mexem (mapa renomeado, bola movida,
    NPC restaurado por outra ferramenta). Sem esta trava, um `--aplica` inocente
    reescreveria o bloco com endereços diferentes embaixo de saves que já têm
    aquelas bolas pegas, e o jogador veria bola voltando do nada.
    """
    t = texto(FLAGS_H) if t is None else t
    if ABRE not in t:
        return {}
    bloco = t[t.index(ABRE):t.index(FECHA)]
    return {(mapa, int(x), int(y)): (alias, int(off, 16))
            for alias, off, mapa, x, y in ALIAS_GRAVADO.findall(bloco)}


def sumidas(ja, dentro):
    """Bola já gravada que a varredura de hoje não achou mais.

    Isso NUNCA pode virar escrita: reescrever o bloco sem ela liberaria o
    endereço dela para a próxima bola nova, e duas coisas passariam a dividir o
    mesmo bit, que é o defeito que este bloco existe para matar. A ferramenta
    para e chama gente, em vez de decidir sozinha.
    """
    return sorted(set(ja) - {(d["mapa"], d["x"], d["y"]) for d in dentro})


def apelido(mapa, item, usados):
    """`FLAG_ITEM_JOHTO_<MAPA>_<ITEM>`, no molde das faixas de Kanto e Sinnoh."""
    base = f"FLAG_ITEM_JOHTO_{mapa.upper().replace('_', '')}_{item[5:]}"
    nome, n = base, 1
    while nome in usados:
        n += 1
        nome = f"{base}_{n}"
    usados.add(nome)
    return nome


def censo():
    """Lista final, com dentro e fora, e cada offset decidido uma única vez."""
    ja = alias_ja_gravados()
    usados = {a for a, _ in ja.values()}
    proximo = max((o for _, o in ja.values()), default=-1) + 1
    dentro, fora = [], []
    for b in sorted(fonte_bolas(ja), key=lambda b: (b["mapa"], b["x"], b["y"])):
        if b["item"] in FORA:
            fora.append(dict(b, motivo=FORA[b["item"]]))
            continue
        item = SUBST_ITEM.get(b["item"], b["item"])
        chave = (b["mapa"], b["x"], b["y"])
        if chave in ja:
            alias, off = ja[chave]
        else:
            alias, off = apelido(b["mapa"], item, usados), proximo
            proximo += 1
        dentro.append(dict(b, item=item, item_fonte=b["item"], flag=alias,
                           offset=off, endereco=f"0x{0x2031 + off:04X}"))
    # TETO, posto pelo J7 em 18/08/2026: a segunda metade da faixa deixou de ser
    # de item ball. `proximo` avançando até lá escreveria bola nova em cima de
    # FLAG_UNUSED que o pool já está distribuindo, e o dono dobrado só
    # apareceria depois, quando alguém apelidasse a mesma flag. Lido do
    # flags.h, não cravado: cravar o número aqui é a classe de erro que o
    # `alias_ja_gravados()` inteiro existe para evitar.
    if proximo > teto_da_faixa():
        raise SystemExit(
            f"a faixa das item balls acabou: o próximo offset seria "
            f"0x{proximo:03X} e o teto é 0x{teto_da_faixa():03X} "
            f"(FLAG_SOBRA_ITEM_BALLS_START). Pedir faixa nova ao condutor.")
    return dentro, fora


def teto_da_faixa(t=None):
    """Primeiro offset que NÃO é mais de item ball, lido de flags.h."""
    t = open(FLAGS_H, encoding="utf-8").read() if t is None else t
    m = re.search(r"^#define\s+FLAG_SOBRA_ITEM_BALLS_START\s+"
                  r"\(FLAG_ITEM_BALLS_JSU_START \+ 0x([0-9A-Fa-f]+)\)", t, re.M)
    if not m:
        raise SystemExit("FLAG_SOBRA_ITEM_BALLS_START sumiu do flags.h")
    return int(m.group(1), 16)


def bloco_de_flags(dentro):
    L = [ABRE,
         "//",
         "// CORREÇÃO DE MEDIÇÃO, e ela vale mais que o comentário do J1 acima:",
         "// a demanda desta faixa NÃO é 1383. Das 1431 item balls com `flag: 0`",
         "// que o J1 contou, 1372 têm `script: \"0\"` e item 0, ou seja não são",
         "// item ball nenhuma: são objetos de Johto achatados pelo",
         "// `sanitize_johto_map_json.py` (efeito de luz, pedra, berry, Pokémon de",
         "// overworld, NPC), e quem os devolve é o `restaura_npcs_johto.py`. As 48",
         "// que sobram são o Battle Pyramid de Hoenn e 11 NPCs de Unova com sprite",
         "// de bola. A demanda medida em 18/08/2026 é 161, todas de JOHTO: Sinnoh e",
         "// Unova não tinham nada a consertar, porque as bolas delas já têm uma",
         "// flag cada. Prova, CORRIGIDA em 18/08/2026 pelo J9: das 764 bolas COM",
         "// script do repo, os números de flag repetidos são CINCO, não quatro. O",
         "// 0 dos 48 do Battle Pyramid, os três FLAG_INICIAL_* das trincas de",
         "// inicial, e o 0x3C (FLAG_GALACTICA_QG_CHAVE), que a bola do QG da",
         "// Galáctica divide com dois NPCs guardas de propósito (está escrito em",
         "// data/maps/GalacticHQ_2F/scripts.inc:5). O quinto escapou porque a",
         "// conta era bola contra bola, e essa conta é CEGA para bola contra NPC:",
         "// o removeobject do Std_FindItem apaga TODO objeto com aquele número de",
         "// flag. O censo certo agrupa todo object_event de data/maps por número",
         "// de flag resolvido no pré-processador e olha os grupos MISTOS.",
         "//",
         "// Uma flag por bola, endereço decidido UMA vez e nunca recalculado.",
         "// O comentário de cada linha é a chave da alocação (mapa e coordenada),",
         "// e é ele que `alias_ja_gravados()` relê: não edite à mão.",
         f"// Consumo: {len(dentro)} das {0x600} vagas da faixa.",
         ""]
    larg = max(len(d["flag"]) for d in dentro) + 1
    for d in dentro:
        L.append(f"#define {d['flag'].ljust(larg)}"
                 f"(FLAG_ITEM_BALLS_JSU_START + 0x{d['offset']:03X})"
                 f"  // {d['mapa']} {d['x']},{d['y']} {d['item']}")
    L += ["", FECHA, ""]
    return "\n".join(L)


def escreve_flags(dentro):
    t = texto(FLAGS_H)
    novo = bloco_de_flags(dentro)
    if ABRE in t:
        t = t[:t.index(ABRE)] + novo + t[t.index(FECHA) + len(FECHA) + 1:]
    else:
        t = t.rstrip("\n") + "\n\n" + novo
    open(FLAGS_H, "w", encoding="utf-8").write(t)


def escreve_mapas(dentro):
    """Escreve script, item e flag no `map.json`, e não toca em mais nada."""
    por_mapa = defaultdict(list)
    for d in dentro:
        por_mapa[d["mapa"]].append(d)
    mudados = 0
    for mapa, bolas in por_mapa.items():
        p = f"{REPO}/data/maps/{mapa}/map.json"
        d = json.load(open(p))
        alvo = {(b["x"], b["y"]): b for b in bolas}
        mexeu = False
        for o in d.get("object_events", []):
            b = alvo.get((o.get("x"), o.get("y")))
            if not b or o.get("graphics_id") != GFX:
                continue
            # Só a bola achatada, ou a que ESTA ferramenta já escreveu. Objeto
            # com outro script é de outra frente e fica intocado.
            if not (achatada(o) or str(o.get("flag")) == b["flag"]):
                continue
            if (o.get("script") == SCRIPT
                    and o.get("trainer_sight_or_berry_tree_id") == b["item"]
                    and o.get("flag") == b["flag"]):
                continue
            o["script"] = SCRIPT
            o["trainer_sight_or_berry_tree_id"] = b["item"]
            o["flag"] = b["flag"]
            mexeu = True
        if mexeu:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
            mudados += 1
    return mudados


def main():
    dentro, fora = censo()
    ja = alias_ja_gravados()
    novas = [d for d in dentro if (d["mapa"], d["x"], d["y"]) not in ja]
    print(f"bolas achatadas de Johto que a fonte prova serem bola: "
          f"{len(dentro) + len(fora)}")
    print(f"  entram, uma flag cada: {len(dentro)} "
          f"({len(ja)} já gravadas, {len(novas)} novas)")
    print(f"  ficam de fora: {len(fora)}")
    for f in fora:
        print(f"    {f['mapa']} {f['x']},{f['y']} {f['item']}: {f['motivo']}")
    print(f"  mapas tocados: {len(set(d['mapa'] for d in dentro))}")
    print(f"  itens distintos: {len(set(d['item'] for d in dentro))}")
    teto = teto_da_faixa()
    print(f"  faixa: 0x2031 a 0x{0x2031 + max(d['offset'] for d in dentro):04X}, "
          f"teto em 0x{0x2031 + teto:04X}, "
          f"{teto - len(dentro)} vaga(s) de item ball ainda livre(s)")
    print(f"  a sobra 0x{0x2031 + teto:04X}-0x2630 ({0x600 - teto}) deixou de "
          f"ser de item ball: virou reserva de conteúdo no J7 (18/08/2026)")
    perdidas = sumidas(ja, dentro)
    if perdidas:
        print(f"\nRECUSADO: {len(perdidas)} bolas já gravadas sumiram da "
              f"varredura, e reescrever o bloco sem elas liberaria o endereço "
              f"delas para outra coisa: {perdidas[:5]}")
        return 1
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0
    escreve_flags(dentro)
    n = escreve_mapas(dentro)
    with open(CENSO, "w", encoding="utf-8") as f:
        json.dump(dict(dentro=dentro, fora=fora), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"\nescrito: flags.h, {n} map.json, censo em "
          f"{os.path.relpath(CENSO, REPO)}")
    return 0


def demo():
    """As regras que decidem o resultado, e a trava contra renumerar."""
    # 1. Quem é bola achatada: as TRÊS pernas juntas.
    assert achatada({"graphics_id": GFX, "script": "0", "flag": "0"})
    assert not achatada({"graphics_id": GFX, "script": "Foo", "flag": "0"})
    assert not achatada({"graphics_id": GFX, "script": "0", "flag": "FLAG_X"})
    assert not achatada({"graphics_id": "OBJ_EVENT_GFX_BOY_1", "script": "0",
                         "flag": "0"})

    # 2. Quem é bola na FONTE: sprite de bola E `finditem`. Sprite sozinho não,
    # senão o efeito de luz e o Pokémon parado da fonte virariam item ball.
    corpos = {"S_Item": "\tfinditem ITEM_POTION\n\tend\n",
              "S_Fala": "\tmsgbox gText_Oi\n\tend\n"}
    assert eh_bola_na_fonte({"graphics_id": "OBJ_EVENT_GFX_POKE_BALL",
                             "script": "S_Item"}, corpos)
    assert not eh_bola_na_fonte({"graphics_id": "OBJ_EVENT_GFX_POKE_BALL",
                                 "script": "S_Fala"}, corpos)
    assert not eh_bola_na_fonte({"graphics_id": "OBJ_EVENT_GFX_LIGHT_SPRITE",
                                 "script": "S_Item"}, corpos)
    m = ITEM_DO_FINDITEM.search("\tfinditem ITEM_RARE_CANDY, 3\n")
    assert m.group(1) == "ITEM_RARE_CANDY" and m.group(2) == "3"

    # 3. Apelido único mesmo com duas bolas do mesmo item no mesmo mapa.
    u = set()
    assert apelido("Route32", "ITEM_GREAT_BALL", u) == \
        "FLAG_ITEM_JOHTO_ROUTE32_GREAT_BALL"
    assert apelido("Route32", "ITEM_GREAT_BALL", u) == \
        "FLAG_ITEM_JOHTO_ROUTE32_GREAT_BALL_2"

    # 4. A TRAVA: o bloco gravado é relido pela chave (mapa, x, y), e mutação
    # plantada nele tem que ser REPROVADA, não absorvida.
    linha = ("#define FLAG_ITEM_JOHTO_DARKCAVESOUTHSIDE_POTION  "
             "(FLAG_ITEM_BALLS_JSU_START + 0x00C)  // DarkCave_SouthSide "
             "10,7 ITEM_POTION\n")
    achados = ALIAS_GRAVADO.findall(linha)
    assert achados == [("FLAG_ITEM_JOHTO_DARKCAVESOUTHSIDE_POTION", "0x00C",
                        "DarkCave_SouthSide", "10", "7")], achados
    # Mutação 1: o offset trocado. A releitura tem que devolver o offset NOVO
    # do arquivo, nunca o que a conta daria, senão a história não manda.
    mut = linha.replace("0x00C", "0x0FF")
    assert ALIAS_GRAVADO.findall(mut)[0][1] == "0x0FF"
    # Mutação 2: coordenada trocada. A chave muda, então a bola de verdade
    # aparece como NOVA e ganha endereço em append, e a linha plantada NÃO é
    # confundida com ela.
    mut = linha.replace("10,7", "11,7")
    assert ALIAS_GRAVADO.findall(mut)[0][2:] == ("DarkCave_SouthSide", "11", "7")
    # Mutação 3: a linha quebrada (sem o comentário-chave) some da releitura,
    # o que faz a bola entrar como nova em vez de herdar endereço errado.
    mut = linha.split("  //")[0] + "\n"
    assert ALIAS_GRAVADO.findall(mut) == []

    # 5. Idempotência da alocação: com o gravado batendo com a fonte, o
    # `proximo` não avança e nenhum offset muda.
    ja = {("A", 1, 2): ("FLAG_ITEM_JOHTO_A_POTION", 0),
          ("B", 3, 4): ("FLAG_ITEM_JOHTO_B_ETHER", 1)}
    assert max(o for _, o in ja.values()) + 1 == 2
    # E a bola gravada continua sendo reconhecida no map.json DEPOIS de escrita,
    # senão a segunda rodada acharia zero e apagaria o bloco inteiro.
    escrita = {"graphics_id": GFX, "x": 1, "y": 2, "script": SCRIPT,
               "flag": "FLAG_ITEM_JOHTO_A_POTION"}
    assert not achatada(escrita) and nossa(escrita, "A", ja)
    assert not nossa(dict(escrita, flag="FLAG_HIDE_OUTRA_COISA"), "A", ja)

    # 6. MUTAÇÃO PLANTADA, de ponta a ponta contra o flags.h de verdade. O bloco
    # real é lido, mutado em memória e relido: o que a ferramenta enxerga tem
    # que ser o arquivo, nunca a conta.
    real = texto(FLAGS_H)
    if ABRE in real:
        base = alias_ja_gravados(real)
        assert base, "bloco gravado existe mas nao foi lido"
        chave, (alias, off) = sorted(base.items())[0]
        linha = [l for l in real.splitlines() if l.startswith(f"#define {alias} ")][0]
        # 6a. offset trocado no arquivo: a releitura devolve o do ARQUIVO.
        plantado = real.replace(linha, linha.replace(f"0x{off:03X})", "0x5AA)"))
        assert alias_ja_gravados(plantado)[chave][1] == 0x5AA
        # 6b. linha apagada: a chave some, e `sumidas` REPROVA a escrita, em vez
        # de deixar o endereço livre para a próxima bola nova.
        podado = real.replace(linha + "\n", "")
        depois = alias_ja_gravados(podado)
        assert chave not in depois
        fingindo = [dict(mapa=m, x=x, y=y) for (m, x, y) in base]
        assert sumidas(base, [d for d in fingindo
                              if (d["mapa"], d["x"], d["y"]) != chave]) == [chave]
        assert sumidas(base, fingindo) == []

    # 7. Tradução e exclusão de item são declaradas, nunca adivinhadas.
    assert SUBST_ITEM["ITEM_EXP_SHARE_SMALL"] == "ITEM_EXP_SHARE"
    assert "ITEM_GS_BALL" in FORA

    # 8. O teto posto pelo J7 é LIDO do flags.h e sobra do que já foi gravado.
    teto = teto_da_faixa()
    assert teto == 0x0A0, hex(teto)
    if ABRE in real:
        assert max(o for _, o in alias_ja_gravados(real).values()) < teto
    # e some junto com a declaração, em vez de virar número de fantasia
    try:
        teto_da_faixa(real.replace("FLAG_SOBRA_ITEM_BALLS_START ", "FLAG_X "))
        raise AssertionError("teto sem declaração tinha que reprovar")
    except SystemExit:
        pass
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
