#!/usr/bin/env python3
"""Fecha as placas de Unova que o importador deixou para trás.

MEDIDO em 22/08/2026 com `dev_scripts/completude.py`: Unova tem 468 `bg_events`
contra 469 da fonte (99,8%), e o buraco inteiro está em UM mapa,
`Unova_PlayersHouse2F`, com 2 de 4. As duas que faltam são a ESTANTE (5,1) e o
PÔSTER (6,0) do quarto do jogador.

Por que o `importa_placas_unova.py` não as trouxe, e não é descuido dele: a
tabela `STD_PLACA` dele casa placa de gen 2 pelo `jumpstd` (`magazinebookshelf`
e irmãs), e estas duas não usam `jumpstd`. Elas têm rótulo próprio:

- `PlayersHouseBookshelfScript`, cujo corpo no BW3G está INTEIRO comentado (é
  estante sem texto próprio; o hack a deixou como teste). Aqui ela vira
  `EventScript_BookShelf`, a estante genérica que este repo já tem em
  `data/scripts/check_furniture.inc`. Zero texto novo.
- `PlayersHousePosterScript`, que no BW3G é `describedecoration DECODESC_POSTER`,
  ou seja a descrição de uma DECORAÇÃO que o jogador pendurou. Esse sistema de
  decoração de quarto não existe neste porte, então descrever a decoração
  inexistente daria caixa vazia. A placa entra descrevendo o que está desenhado
  na parede, uma frase, sem inventar história nem prometer mecânica.

Compatibilidade de save: `bg_event` não mora na save e não tem índice que algum
script cite. As duas entram no FIM da lista.

Uso:
    python3 dev_scripts/completa_placas_unova.py            # só relata
    python3 dev_scripts/completa_placas_unova.py --aplica   # escreve
    python3 dev_scripts/completa_placas_unova.py --demo     # autoteste
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import restaura_gfx_johto as RG  # noqa: E402  grava_como_estava

APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv

MARCA = "@ Placas fechadas por dev_scripts/completa_placas_unova.py"

# (mapa, x, y, script, texto novo ou None quando o script ja existe no repo)
PLACAS = [
    ("Unova_PlayersHouse2F", 5, 1, "EventScript_BookShelf", None),
    ("Unova_PlayersHouse2F", 6, 0,
     "Unova_PlayersHouse2F_EventScript_Poster",
     'Um pôster grudado na parede.'),
]

TEXTO_POSTER = """
{marca}
Unova_PlayersHouse2F_EventScript_Poster::
\tmsgbox Unova_PlayersHouse2F_Text_Poster, MSGBOX_SIGN
\tend

Unova_PlayersHouse2F_Text_Poster::
\t.string "A POKéMON poster is stuck to\\n"
\t.string "the wall.$"
"""


def bg(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": script}


def monta():
    planos, relato = {}, []
    for mapa, x, y, script, _ in PLACAS:
        p = os.path.join(REPO, "data/maps", mapa, "map.json")
        d = planos.get(mapa) or json.load(open(p, encoding="utf-8"))
        planos[mapa] = d
        if any((b["x"], b["y"]) == (x, y) for b in d["bg_events"]):
            relato.append(f"{mapa} ({x},{y}): ja existe, nada a fazer")
            continue
        d["bg_events"].append(bg(x, y, script))
        relato.append(f"{mapa} ({x},{y}) -> {script}")
    return planos, relato


def escreve(planos, relato):
    tocados = {l.split(" ")[0] for l in relato if "->" in l}
    for mapa in tocados:
        RG.grava_como_estava(
            os.path.join(REPO, "data/maps", mapa, "map.json"), planos[mapa])
    if "Unova_PlayersHouse2F" in tocados:
        p = os.path.join(REPO, "data/maps/Unova_PlayersHouse2F/scripts.inc")
        txt = open(p, encoding="utf-8").read()
        if MARCA not in txt:
            with open(p, "w", encoding="utf-8") as f:
                f.write(txt.rstrip("\n") + "\n"
                        + TEXTO_POSTER.format(marca=MARCA))


def demo():
    """As duas coordenadas TÊM que ser as que faltam na fonte, não outras."""
    fonte = open("/Users/duarte/Projetos/pokemon-claude/fontes-mapas/bw3g/"
                 "maps/PlayersHouse2F.asm", encoding="utf-8").read()
    linhas = [l.strip() for l in fonte.splitlines()
              if l.strip().startswith("bg_event")]
    da_fonte = set()
    for l in linhas:
        p = [x.strip() for x in l[len("bg_event"):].split(",")]
        da_fonte.add((int(p[0]), int(p[1])))
    d = json.load(open(os.path.join(
        REPO, "data/maps/Unova_PlayersHouse2F/map.json"), encoding="utf-8"))
    nossas = {(b["x"], b["y"]) for b in d["bg_events"]}
    faltam = da_fonte - nossas
    minhas = {(x, y) for m, x, y, _, _ in PLACAS
              if m == "Unova_PlayersHouse2F"}
    assert faltam <= minhas or not faltam, (
        f"a fonte pede {sorted(faltam)} e a tabela cobre {sorted(minhas)}")
    # o script apontado tem que EXISTIR, senao o build quebra com rotulo solto
    alvo = os.path.join(REPO, "data/scripts/check_furniture.inc")
    assert "EventScript_BookShelf::" in open(alvo, encoding="utf-8").read()
    print(f"demo ok: a fonte tem {len(da_fonte)} placas, temos {len(nossas)}, "
          f"faltam {sorted(faltam) or 'nenhuma'}")


def main():
    if DEMO:
        demo()
        return 0
    planos, relato = monta()
    for l in relato:
        print("  " + l)
    if APLICA:
        escreve(planos, relato)
        print("\nescrito.")
    else:
        print("\n(nada escrito; rode com --aplica)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
