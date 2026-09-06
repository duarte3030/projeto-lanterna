#!/usr/bin/env python3
"""Prova, NO EMULADOR, que quem entra por uma porta sai por ela.

Por que existe
--------------
Em 06/09/2026 o Gui trouxe do playtest: em Veilstone (Sinnoh) ele entrou no
predio da esquerda, saiu, e apareceu em Lilycove City. A loja de Veilstone e a
loja de Lilycove REAPROVEITADA, e a saida dela era fixa para Hoenn.

O conserto e de dado mais motor (`MAP_DYNAMIC` na porta de saida, mais o
`special DefinirRetornoPredioCompartilhado` no ON_TRANSITION do terreo), e
"compilou" nao prova nada sobre porta. Esta ferramenta anda de verdade: warpa
pela porta pelo menu de debug, ENTRA andando, SAI andando, e le da EWRAM o
`(grupo, num)` e o `(x, y)` em que o jogador parou.

Cada caso vem em PAR: o lado NOVO (a cidade que reaproveita o interior) e o lado
ORIGINAL (a cidade dona dele). Sem o par, um conserto que quebra o original
passa verde.

Uso
---
    python3 dev_scripts/prova_portas_compartilhadas.py
    python3 dev_scripts/prova_portas_compartilhadas.py --rom outra.gba
    python3 dev_scripts/prova_portas_compartilhadas.py --caso veilstone
    python3 dev_scripts/prova_portas_compartilhadas.py --demo
"""
import argparse
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import testa_critico as tc  # noqa: E402

SAIDA = "/tmp/claude-501/portas-compartilhadas"

# Um caso e: warpar para o warp `warp` do mapa `de`, andar `entrar` para dentro,
# conferir que chegou em `dentro`, andar `sair` de volta e conferir que voltou
# para `de`. `dentro` e `de` sao nomes de constante, resolvidos pela tabela de
# map_groups.h, nunca digitados como numero.
CASOS = [
    # ---- Sinnoh: a loja e o museu de Lilycove reaproveitados ---------------
    dict(id="veilstone", regiao="Sinnoh",
         de="MAP_VEILSTONE_CITY", warp=3,
         dentro="MAP_LILYCOVE_CITY_DEPARTMENT_STORE_1F",
         entrar="UP", sair="DOWN",
         o_que="o defeito do Gui: sair da loja de Veilstone levava a Lilycove"),
    dict(id="lilycove_loja", regiao="Hoenn",
         de="MAP_LILYCOVE_CITY", warp=0,
         dentro="MAP_LILYCOVE_CITY_DEPARTMENT_STORE_1F",
         entrar="UP", sair="DOWN",
         o_que="REGRESSAO: o lado original da mesma loja tem que continuar igual"),
    dict(id="oreburgh", regiao="Sinnoh",
         de="MAP_OREBURGH_CITY", warp=4,
         dentro="MAP_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F",
         entrar="UP", sair="DOWN",
         o_que="o museu de Oreburgh e o museu de Lilycove"),
    dict(id="lilycove_museu", regiao="Hoenn",
         de="MAP_LILYCOVE_CITY", warp=3,
         dentro="MAP_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F",
         entrar="UP", sair="DOWN",
         o_que="REGRESSAO: o lado original do mesmo museu"),
    # ---- Johto: o Safari que e o de Hoenn ----------------------------------
    dict(id="safari_johto", regiao="Johto",
         de="MAP_SAFARI_ZONE_GATE_SAFARI_ZONE_ENTRANCE", warp=0,
         dentro="MAP_SAFARI_ZONE_SOUTH",
         entrar="UP", sair="UP",
         o_que="o Safari de Johto e o Safari de Hoenn, e a saida ia para a Rota 121"),
    dict(id="safari_hoenn", regiao="Hoenn",
         de="MAP_ROUTE121_SAFARI_ZONE_ENTRANCE", warp=0,
         dentro="MAP_SAFARI_ZONE_SOUTH",
         entrar="DOWN", sair="UP",
         o_que="REGRESSAO: o portao original do Safari de Hoenn"),
    # ---- Johto e Kanto: o portao da Victory Road ---------------------------
    dict(id="portao_victory", regiao="Johto",
         de="MAP_RECEPTION_GATE", warp=1,
         dentro="MAP_VICTORY_ROAD_1F_FRLG",
         entrar="UP", sair="DOWN",
         o_que="o portao de Johto caia na escada do 2F da Victory Road"),
    # ---- Sinnoh: a seta da Rota 218 mandava para o outro lado do mapa -----
    dict(id="route218", regiao="Sinnoh",
         de="MAP_ROUTE218", warp=0,
         dentro="MAP_ROUTE218_EAST",
         entrar="RIGHT", sair="LEFT", passos=2, passos_sair=4,
         o_que="a seta leste da Rota 218 caia na Rota 211 Leste, perto do Mt. Coronet"),
    dict(id="portao_rota22", regiao="Johto",
         de="MAP_RECEPTION_GATE", warp=4,
         dentro="MAP_ROUTE22_NORTH_ENTRANCE",
         entrar="DOWN", sair="UP",
         o_que="a porta leste do portao de Johto cuspia o jogador em cima da "
               "porta do portao de Kanto, na Rota 22"),
    # ---- ADVERSARIAL: o elevador suja o retorno, e o special tem que repor --
    # Sem este caso os outros nove passariam com o special QUEBRADO, porque o
    # caminho curto (entra, sai) nunca chega a sujar o `dynamicWarp`. Entrar no
    # ELEVADOR faz o proprio motor gravar `dynamicWarp = (loja 1F, warp 3)`, que
    # e um mapa FECHADO; sem a reposicao, a porta da rua mandaria o jogador para
    # dentro da propria loja, na porta do elevador.
    dict(id="elevador", regiao="Sinnoh",
         de="MAP_VEILSTONE_CITY", warp=3,
         dentro="MAP_LILYCOVE_CITY_DEPARTMENT_STORE_ELEVATOR",
         # Rota lida da grade de colisao da loja (18x8), e o roteiro so anda de
         # ANCORA em ANCORA. A loja tem DUAS NPCs que andam,
         # MOVEMENT_TYPE_WANDER_AROUND de alcance 1, em (4,4) e em (14,5), e
         # elas guardam justamente os corredores: (4,4) pisa em (3,4), (5,4),
         # (4,3) e (4,5), que e o unico caminho para o lado oeste do salao, onde
         # fica a porta do elevador. CONTAR TILES ao lado delas e decorar
         # sorteio, e um roteiro que contava a linha 5 abriu VERMELHO com o jogo
         # certo, uma vez em cada tres rodadas: a NPC barrava a ida e o jogador
         # subia a coluna 5 ate (5,2), sem chegar ao elevador.
         #
         # O conserto e andar SEMPRE ate esbarrar em coisa que NAO SE MEXE, com
         # apertos de sobra, e nunca contar tile em corredor que uma NPC de
         # andar alcanca:
         #   LEFT,20  linha 5   -> PAREDE do oeste, (2,5) ((1,5) e solido)
         #   UP,6     coluna 2  -> a porta do ELEVADOR em (2,1)
         #   DOWN,4             -> sai do elevador e cai no terreo, em (2,2)
         #   DOWN,8   coluna 2  -> a LOOK_AROUND PARADA de (2,6): ancora (2,5)
         #   RIGHT,24 linha 5   -> PAREDE do leste, (17,5)
         #   DOWN,4   coluna 17 -> PAREDE do sul, (17,6)
         #   LEFT,24  linha 6   -> a LOOK_AROUND PARADA de (3,6): ancora (4,6)
         #   DOWN,3   coluna 4  -> a BORDA do mapa, (4,7)
         #   RIGHT,24 linha 7   -> PAREDE de (14,7): ancora (13,7)
         #   LEFT,6   linha 7   -> a PORTA, que e LARGA: (8,7) e (9,7) sao os
         #                         dois tiles dela, entao esta perna acerta com
         #                         5 OU com 6 apertos, e e a unica contada
         #   DOWN,3   em cima   -> a porta e MB_SOUTH_ARROW_WARP: nao basta
         #                         pisar, tem que estar VIRADO para baixo e
         #                         apertar DOWN de novo em cima dela. O POUSO
         #                         medido e Veilstone (25,31), o tile em frente
         #                         a porta (25,30); o terceiro aperto sobra e
         #                         desce mais um, e por isso o fim e (25,32)
         #
         # SEGUNDA MEDIDA, e ela vale para qualquer roteiro futuro: TROCAR DE
         # DIRECAO custa UM APERTO. Medido aqui, quadro a quadro: o jogador
         # parado em (0,2) virado para cima recebeu RIGHT duas vezes e andou UM
         # tile so; andar na direcao que ja se encara nao cobra nada (UP,3 na
         # coluna 8 andou os tres).
         #
         # TERCEIRA MEDIDA: ESBARRAR DESREGULA A CADENCIA. Cada aperto do
         # roteiro sao 20 quadros segurando mais 60 de folga, e isso basta para
         # UM PASSO, mas a animacao de esbarrao e mais longa, entao a perna
         # seguinte comeca no meio dela e perde apertos. Foi assim que um
         # roteiro de ancoras deu 10 de 11 numa rodada e 11 de 11 na outra, com
         # a mesma ROM. Por isso TODA perna que termina esbarrando e seguida de
         # `espera`, que e de graca: ela devolve o jogador parado e virado, que
         # e o unico estado de onde a contagem de tile vale.
         roteiro=["UP,2", "espera",
                  "UP,2", "LEFT,20", "espera", "UP,6", "espera",
                  "DOWN,4", "espera",
                  "DOWN,8", "espera", "RIGHT,24", "espera", "DOWN,4", "espera",
                  "LEFT,24", "espera", "DOWN,3", "espera", "RIGHT,24", "espera",
                  "LEFT,6", "espera", "DOWN,3", "espera"],
         o_que="ADVERSARIAL: entra na loja por Veilstone, ENTRA NO ELEVADOR, "
               "volta ao terreo e sai pela porta da rua"),
    dict(id="victory_kanto", regiao="Kanto",
         de="MAP_ROUTE23", warp=0,
         dentro="MAP_VICTORY_ROAD_1F_FRLG",
         entrar="UP", sair="DOWN",
         o_que="REGRESSAO: a entrada original da Victory Road, pela Rota 23"),
]

# ESPERA E DE GRACA, APERTO NAO E. Depois que o warp dispara o motor trava o
# input por volta de 60 quadros (medido na secao 0. do ESTADO, `sLockFieldControls`),
# e aperto dado dentro da trava e ENGOLIDO. Por isso cada passo carrega 60
# quadros de espera e o fim de cada fase carrega mais 240: com folga o roteiro
# nao depende de o warp caber num numero exato de quadros.
DEMORA = "240:NADA"


def passos(direcao, quantos=2):
    """Andar `quantos` tiles na direcao, com espera propria por passo."""
    return ",".join(f"20:{direcao},60:NADA" for _ in range(quantos))


def roda(rom, simbolos, roteiro, prefixo):
    os.makedirs(SAIDA, exist_ok=True)
    cmd = [tc.RUNNER, rom, "900", roteiro, f"{SAIDA}/{prefixo}.png",
           "--dump-estado",
           "--sb1ptr", simbolos["gSaveBlock1Ptr"],
           "--partycount", simbolos["gPartiesCount"],
           "--oponente", simbolos["gTrainerBattleParameter"]]
    saida = subprocess.run(cmd, capture_output=True, text=True)
    estados = []
    for linha in saida.stdout.splitlines():
        m = tc.LINHA_ESTADO.match(linha)
        if m:
            estados.append(dict(p.split("=", 1) for p in m.group(2).split()))
    if not estados:
        raise SystemExit(f"gba_runner nao imprimiu estado. stderr:\n{saida.stderr}")
    return estados


def onde(est):
    return (int(est["grupo"]), int(est["num"]), int(est["x"]), int(est["y"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=os.path.join(RAIZ, "pokeemerald.gba"))
    ap.add_argument("--map", dest="mapfile",
                    default=os.path.join(RAIZ, "pokeemerald.map"))
    ap.add_argument("--caso")
    ap.add_argument("--passos", type=int, default=2)
    ap.add_argument("--verboso", action="store_true",
                    help="imprime o (grupo,num,x,y) de CADA passo do roteiro")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    por_nome, _ = tc.carrega_mapas()
    if args.demo:
        faltam = sorted({c[k] for c in CASOS for k in ("de", "dentro")}
                        - set(por_nome))
        if faltam:
            print("demo REPROVOU, mapa desconhecido:", faltam)
            return 1
        print(f"demo OK: {len(CASOS)} casos, todos os mapas resolvidos na tabela")
        return 0

    simbolos = tc.carrega_simbolos(args.mapfile)
    casos = [c for c in CASOS if not args.caso or c["id"] == args.caso]
    ruins = 0
    for c in casos:
        g_de, n_de = por_nome[c["de"]]
        g_in, n_in = por_nome[c["dentro"]]
        if c.get("roteiro"):
            pernas = []
            for perna in c["roteiro"]:
                if perna == "espera":
                    pernas.append(DEMORA)
                else:
                    d, k = perna.split(",")
                    pernas.append(passos(d, int(k)))
            roteiro = ",".join([tc.ABERTURA, tc.rota_warp(g_de, n_de, c["warp"])] + pernas)
        else:
            roteiro = ",".join([
                tc.ABERTURA,
                tc.rota_warp(g_de, n_de, c["warp"]),
            # ARMADILHA MEDIDA em 06/09/2026: seta de rota (`MB_*_ARROW_WARP`)
            # so dispara com a direcao SEGURADA e o jogador ja VIRADO para ela
            # (`input->heldDirection && input->dpadDirection == playerDirection`,
            # src/field_control_avatar.c), entao o primeiro aperto depois de dar
            # meia-volta e gasto virando. Andar N tiles para dentro e N de volta
            # gasta todos os apertos chegando na seta e nenhum a acionando: a
            # volta precisa de aperto A MAIS que a ida, e e para isso que serve
            # `passos_sair`. Porta nao tem esse problema, porque dispara ao ser
            # PISADA.
                passos(c["entrar"], c.get("passos", args.passos)), DEMORA,
                passos(c["sair"], c.get("passos_sair", c.get("passos", args.passos))), DEMORA,
            ])
        est = roda(args.rom, simbolos, roteiro, c["id"])
        # O estado da CHEGADA e o ultimo antes de o roteiro comecar a sair; como
        # o runner despeja um por passo, procuro o primeiro passo em que o
        # (grupo,num) e o do interior, e o ultimo estado de todos e a volta.
        dentro = [e for e in est if (int(e["grupo"]), int(e["num"])) == (g_in, n_in)]
        fim = est[-1]
        chegou = bool(dentro)
        voltou = (int(fim["grupo"]), int(fim["num"])) == (g_de, n_de)
        ok = chegou and voltou
        ruins += not ok
        veredito = ("OK" if ok else
                    ("NAO ENTROU" if not chegou else "SAIU NO LUGAR ERRADO"))
        print(f"[{veredito:20s}] {c['regiao']:6} {c['id']:16} "
              f"{c['de']} warp {c['warp']} -> {c['dentro']}")
        print(f"      dentro: {'sim' if chegou else 'NAO'}    "
              f"parou em grupo={fim['grupo']} num={fim['num']} "
              f"({fim['x']},{fim['y']})   PNGs em {SAIDA}/{c['id']}-*.png")
        print(f"      {c['o_que']}")
        if args.verboso:
            visto = None
            for i, e in enumerate(est):
                agora = onde(e)
                if agora != visto:
                    print(f"        passo {i:3d}: grupo={agora[0]} num={agora[1]} "
                          f"({agora[2]},{agora[3]})")
                    visto = agora
    print(f"\n{len(casos) - ruins} de {len(casos)} portas devolvem para onde o "
          f"jogador entrou.")
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main() or 0)
