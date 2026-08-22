#!/usr/bin/env python3
"""As 3 cenas do PWT de Unova, que saíram da fila de bloqueio residual.

As três eram as únicas da fila `portavel_bloqueio` de Unova que NÃO são enredo:
o corpo delas na fonte é `applymovement PLAYER` mais `warpcheck`, sem uma linha
de história. O que as segurava era outra coisa, e a medição de 22/08/2026 diz
qual: o `coord_event` de `PWTHallway (4,1)` fica EXATAMENTE embaixo da porta da
sala de qualificação, em (4,0). Sem var de cena, ele dispara toda vez que o
jogador sobe para entrar naquela porta e o arrasta embora, ou seja **tranca a
sala para sempre**. Não é parede permanente por falta de enredo: é armadilha de
geometria.

O condutor autorizou em 22/08/2026 acrescentar `PWT_HALLWAY` e `PWT_INSIDE` à
tabela mapa → var → valores do `PLANO-OBRAS-UNOVA.md` (0x417E e 0x417F, apelidos
de `VAR_UNUSED`, `VARS_COUNT` intacto). Com a var, o
`gatilhos_setscene_unova.py` escreveu os 3 gatilhos com `var_value 0` e os 3
stubs; este gerador troca o corpo do stub pela cena de verdade.

A ÚNICA ADAPTAÇÃO, e ela é o critério de aceite

A fonte não fecha a cena: quem devolve `PWT_HALLWAY` para `SCENE_FINISHED` é o
`PwtBlockerScript`, que depende do enredo do torneio (`EVENT_FINISHED_PWT`), e
esse enredo não existe aqui. Então **cada cena fecha a si mesma**: grava a
própria var em 1 na PRIMEIRA linha, antes de mexer no jogador. Consequência
escrita: a cena roda UMA vez e para. Em qualquer ordem de visita a sala de
qualificação fica acessível, que era o defeito a evitar.

Segunda adaptação, medida e não presumida: o `warpcheck` do gen 2 **não existe
neste motor** (`grep -n "macro warpcheck" asm/macros/event.inc` volta vazio; há
`warp`, `warpsilent`, `warpdoor`, `warphole` e `warpteleport`, nenhum deles é
"agora confira se o tile embaixo do jogador é warp"). As duas cenas do corredor
terminam o passeio EM CIMA do warp de destino, e quem entra na porta é o
jogador, num passo. Chamar `warp` no lugar seria trocar um passeio por um
teleporte e mudar o que a fonte faz.

Movimentos e coordenadas são os da fonte, sem reescrever nada:

- `PWTHallway (4,1)`: DOWN DOWN, RIGHT x10, UP x3, e o UP final cai em (14,0),
  o tile do warp da sala dos fundos. É a passagem qualificação -> fundos.
- `PWTHallway (14,1)`: DOWN DOWN, LEFT x4, DOWN DOWN, caindo em (10,5), o warp
  o tile do warp para o saguão. É o caminho de volta.
- `PWTInside (7,1)`: o recepcionista de (7,3) (nosso `object_event` 1) sai da
  frente, o jogador desce 3 e o recepcionista volta. Sem `warpcheck`: esta
  cena não leva o jogador para fora do mapa.

Uso:
    python3 dev_scripts/cenas_pwt_unova.py            # só relata
    python3 dev_scripts/cenas_pwt_unova.py --aplica   # escreve
    python3 dev_scripts/cenas_pwt_unova.py --demo     # autoteste
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BW3G = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/bw3g"
APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv

# O recepcionista que sai da frente é o object_event de (7,3) do Unova_PWTInside.
# O índice é LIDO do map.json (ver `localid`), nunca cravado: `applymovement`
# com id errado não dá erro de compilação, mexe no boneco errado em jogo.
BLOQUEADOR = (7, 3)

CENAS = {
    "Unova_PWTHallway": {
        "PwtEnterFromLeftScript": """\tlockall
\tsetvar VAR_UNOVA_PWT_CORREDOR_CENA, 1
\tapplymovement OBJ_EVENT_ID_PLAYER, Unova_PWTHallway_Movement_EsquerdaParaDireita
\twaitmovement 0
\treleaseall
\tend""",
        "PwtEnterFromRightScript": """\tlockall
\tsetvar VAR_UNOVA_PWT_CORREDOR_CENA, 1
\tapplymovement OBJ_EVENT_ID_PLAYER, Unova_PWTHallway_Movement_SaidaPelaDireita
\twaitmovement 0
\treleaseall
\tend""",
    },
    "Unova_PWTInside": {
        "PwtEnterFromBackScript": """\tlockall
\tsetvar VAR_UNOVA_PWT_DENTRO_CENA, 1
\tapplymovement {localid}, Unova_PWTInside_Movement_BloqueadorSai
\twaitmovement 0
\tapplymovement OBJ_EVENT_ID_PLAYER, Unova_PWTInside_Movement_JogadorEntra
\twaitmovement 0
\tapplymovement {localid}, Unova_PWTInside_Movement_BloqueadorVolta
\twaitmovement 0
\treleaseall
\tend""",
    },
}

MOVIMENTOS = {
    "Unova_PWTHallway": """
\t.align 2
Unova_PWTHallway_Movement_EsquerdaParaDireita:
\twalk_down
\twalk_down
\twalk_right
\twalk_right
\twalk_right
\twalk_right
\twalk_right
\twalk_right
\twalk_right
\twalk_right
\twalk_right
\twalk_right
\twalk_up
\twalk_up
\twalk_up
\tstep_end

\t.align 2
Unova_PWTHallway_Movement_SaidaPelaDireita:
\twalk_down
\twalk_down
\twalk_left
\twalk_left
\twalk_left
\twalk_left
\twalk_down
\twalk_down
\tstep_end
""",
    "Unova_PWTInside": """
\t.align 2
Unova_PWTInside_Movement_BloqueadorSai:
\twalk_up
\twalk_right
\twalk_in_place_faster_left
\tstep_end

\t.align 2
Unova_PWTInside_Movement_JogadorEntra:
\twalk_down
\twalk_down
\twalk_down
\tstep_end

\t.align 2
Unova_PWTInside_Movement_BloqueadorVolta:
\twalk_left
\twalk_down
\tstep_end
""",
}

MARCA = "@ Cenas do PWT (dev_scripts/cenas_pwt_unova.py), autorizadas em 22/08/2026"
STUB = re.compile(r"(@ STUB A2: cena do bloco A4/A5/A6, rotulo (\w+)\n(\w+)::\n)\tend\n")


def localid(mapa, alvo):
    """Índice 1-based do object_event daquela coordenada, LIDO do map.json."""
    d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                       encoding="utf-8"))
    for i, o in enumerate(d["object_events"], 1):
        if (o["x"], o["y"]) == alvo:
            return i
    raise SystemExit(f"{mapa}: nenhum object_event em {alvo}")


def monta():
    plano, relato = {}, []
    for mapa, corpos in CENAS.items():
        p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        txt = open(p, encoding="utf-8").read()
        if MARCA in txt:
            relato.append(f"{mapa}: ja tem as cenas, nada a fazer")
            continue
        lid = localid(mapa, BLOQUEADOR) if mapa == "Unova_PWTInside" else 0
        novo, trocados = txt, []

        def troca(m):
            rot = m.group(2)
            if rot not in corpos:
                return m.group(0)
            trocados.append(rot)
            return m.group(1) + corpos[rot].format(localid=lid) + "\n"

        novo = STUB.sub(troca, novo)
        if not trocados:
            relato.append(f"{mapa}: nenhum stub casou (o gatilho ja foi "
                          f"escrito?)")
            continue
        novo = novo.rstrip("\n") + "\n\n" + MARCA + "\n" + MOVIMENTOS[mapa]
        plano[mapa] = novo
        relato.append(f"{mapa}: {len(trocados)} cena(s) -> "
                      + ", ".join(trocados)
                      + (f" (bloqueador = object_event {lid})" if lid else ""))
    return plano, relato


def demo():
    """As três coisas que o build não pega e que quebram em jogo."""
    # 1. o gatilho TEM que estar preso a uma var, senao a cena repete e a sala
    #    de qualificacao fica trancada (o defeito que esta obra existe para
    #    evitar)
    for mapa in CENAS:
        d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))
        gat = [c for c in d["coord_events"]
               if c["script"].endswith(tuple(CENAS[mapa]))]
        assert gat, f"{mapa}: gatilho da cena sumiu do map.json"
        for c in gat:
            assert c["var"].startswith("VAR_UNOVA_PWT_"), c
            assert str(c["var_value"]) == "0", c

    # 2. a cena TEM que gravar a propria var, senao ela repete
    for mapa, corpos in CENAS.items():
        var = {c["var"] for c in json.load(open(
            os.path.join(REPO, "data/maps", mapa, "map.json"),
            encoding="utf-8"))["coord_events"]
            if c["script"].endswith(tuple(corpos))}
        for corpo in corpos.values():
            assert any(f"setvar {v}, 1" in corpo for v in var), corpo
        # e antes do warpcheck, se houver
        for corpo in corpos.values():
            if "warpcheck" in corpo:
                assert corpo.index("setvar") < corpo.index("warpcheck")

    # 3. o localid do bloqueador e LIDO, e o objeto tem que existir
    lid = localid("Unova_PWTInside", BLOQUEADOR)
    assert lid >= 1

    plano, relato = monta()
    print(f"demo ok: bloqueador do PWTInside e o object_event {lid}, "
          f"{len(plano)} mapa(s) a escrever, gatilhos presos a var com "
          "var_value 0")


def main():
    if DEMO:
        demo()
        return 0
    plano, relato = monta()
    for l in relato:
        print("  " + l)
    if APLICA:
        for mapa, txt in plano.items():
            open(os.path.join(REPO, "data/maps", mapa, "scripts.inc"),
                 "w", encoding="utf-8").write(txt)
        print("\nescrito.")
    else:
        print("\n(nada escrito; rode com --aplica)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
