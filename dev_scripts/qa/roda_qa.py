#!/usr/bin/env python3
"""Roda as QUATRO varreduras de QA e imprime a contagem por classe e por regiao.

Uso:
    python3 dev_scripts/qa/roda_qa.py            # as quatro, contagem consolidada
    python3 dev_scripts/qa/roda_qa.py --demo     # so os autotestes, exit 1 se um cair
    python3 dev_scripts/qa/roda_qa.py --json X   # despeja os achados crus em X

Por que existe
--------------
As primeiras quatro nasceram fora do repo, na auditoria de 23/08/2026, e cada
uma imprimia o resumo dela do seu jeito. Fora do repo, ferramenta de QA envelhece
sem ninguem ver: ninguem roda o que nao esta ao lado do codigo. Aqui elas ficam
juntas, com UMA contagem, e com um `--demo` unico que e o portao: cada varredura
tem mutacao plantada e cai se parar de morder.

O que cada uma mede, e o que ela NAO mede
-----------------------------------------
    checa_scripts.py   fluxo de script de mapa (C01..C27): `lock` sem `release`,
                       warp com `release` antes do `waitstate`, id de objeto que
                       o mapa nao tem, `special` fora da tabela.
    checa_texto.py     texto (T01..T09): largura em PIXEL contra a caixa, linha
                       a mais, `$` faltando, caractere fora do charmap, acento.
    mapas_qa.py        mapa, evento e alcancabilidade (A*, B*, C*, D*), com a
                       MESMA regua rodada no vanilla (`--vanilla`) para separar
                       defeito nosso de idioma do motor.
    estado_jogo.py     flag, var, item, treinador e save.
    lente_warps.py     ida e volta de warp (P1..P4): destino que nao existe,
                       porta de predio que devolve para outra rua, volta que
                       pousa fora da porta usada, e escada interna que nao
                       devolve. Nasceu do playtest de 06/09/2026, em que sair
                       da loja de Veilstone levava a Lilycove.

NENHUMA delas roda o jogo. Prova de comportamento e da suite do emulador
(`dev_scripts/testa_critico.py`); estas quatro so leem a arvore, e a divisao e
de proposito: elas acham o candidato, a suite prova o fato.

Regra de leitura, herdada da licao 4.10 do ESTADO: contagem alta numa regra NAO
e fila de conserto. Regra cuja taxa por 100 mapas empata com a do vanilla e
FALSO POSITIVO calibrado, e os vereditos ja medidos estao escritos em
VEREDITOS_DE_CALIBRACAO abaixo, para ninguem reabrir a mesma discussao.
"""
import argparse
import collections
import importlib
import json
import os
import sys
import traceback

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# Regras cujo veredito JA foi medido contra o pret/pokeemerald intocado em
# 23/08/2026: a taxa por 100 mapas empata com a do vanilla ou e MENOR que ela,
# entao mandar consertar tiraria desenho bom. Ficam escritas aqui, e nao numa
# conversa, porque falso positivo que volta todo mes custa mais que o bug.
#   A3 pouso em cima de objeto      3,96 nosso  x  5,41 vanilla
#   B1 objeto em tile solido        1,79       x  2,12
#   B2 objeto sobre warp            2,08       x  6,18
#   B3 objeto sobre coord_event     0,58       x  1,93
#   B4 dois objetos no mesmo tile   4,13       x  7,34
#   B9 objeto tapa o tile de fala   4,33       x 18,70
#   D2 tabela de encontro sem grama 11,9       x 11,8
VEREDITOS_DE_CALIBRACAO = {
    "A3": "falso positivo (taxa MENOR que a do vanilla)",
    "B1": "falso positivo (regra do balcao MB_COUNTER ja aplicada)",
    "B2": "falso positivo",
    "B3": "falso positivo",
    "B4": "falso positivo",
    "B9": "falso positivo (18,7 por 100 no vanilla contra 4,33 aqui)",
    "D2": "falso positivo",
    "C2": "so vale o recorte de fracao alcancada ridicula; em bloco, empata",
    "D1": "em Galar nao e defeito: a regiao tem grama e Dex 0 por escopo",
    "C15": "idioma normal do motor (flag de esconder acesa e nunca apagada)",
    "C24": "idioma normal do motor (flag de esconder que ninguem toca)",
}

# Achados NOMINAIS ja abertos no arquivo e medidos em 23/08/2026, um a um. Cada
# um parecia trava de Kanto e nenhum e. Ficam escritos porque a regra que os
# levanta continua certa: quem os reabrir gasta a manha de novo.
VEREDITOS_DE_CASO = {
    "Sevii (162 mapas de Kanto fora do grafo de warp)":
        "PORTAO DE ENREDO INTACTO, nao conteudo morto. A balsa e `special "
        "DoSeagallopFerryScene` (tabela sSeag em src/seagallop.c), nao warp, e a "
        "corrente esta inteira: Blaine grava VAR_MAP_SCENE_CINNABAR_ISLAND=1 "
        "(CinnabarIsland_Gym_Frlg/scripts.inc:61), a cena do Bill leva a One "
        "Island, e la nasce o TRI PASS. valida_conectividade ja le a tabela.",
    "ThreeIsland_DunsparceTunnel_Frlg (25,5) em tile solido":
        "FALSO POSITIVO: o mapa TROCA DE LAYOUT. O ON_TRANSITION chama "
        "`setmaplayoutindex LAYOUT_THREE_ISLAND_DUNSPARCE_TUNNEL_DUG_OUT` quando "
        "a Dex nacional esta ligada, e nesse layout (25,5) e corredor. Nao e "
        "`setmetatile`, que foi o que a auditoria procurou e nao achou.",
    "SSAnne_1F_Corridor_Frlg (20,0) em tile solido":
        "FALSO POSITIVO HERDADO: blockdata e warps IDENTICOS ao pokefirered. O "
        "gatilho do outro lado, SSAnne_Exterior warp 3 em (33,15), e "
        "MB_OCEAN_WATER com colisao 1 nas duas arvores: e o par de warp nao usado "
        "do navio. Consertar seria divergir do FRLG por zero ganho.",
    "E4 de Kanto: Lorelei, Bruno e Agatha, warp 0 em (6,12)":
        "FALSO POSITIVO HERDADO, e o mecanismo NAO e setmetatile. Blockdata "
        "identico ao pokefirered (colisao 1 nas linhas 11 e 12, entrada fechada). "
        "Quem tira o jogador de la e `PokemonLeague_EventScript_EnterRoom` "
        "(data/scripts/pokemon_league.inc:10) com `Common_Movement_WalkUp5`, e "
        "applymovement de script NAO consulta colisao.",
}

FERRAMENTAS = ("checa_scripts", "checa_texto", "mapas_qa", "estado_jogo",
               "lente_warps", "lente_portas")


def roda_demos():
    """Os quatro autotestes. Devolve 0 se os quatro morderem."""
    ruim = 0
    for nome in FERRAMENTAS:
        mod = importlib.import_module(nome)
        try:
            # As quatro `demo()` DEVOLVEM 1 quando a mutação plantada não é
            # mordida, e só algumas levantam. Até 06/09/2026 este laço olhava
            # só a exceção, então um `return 1` imprimia DEMO VERDE e o portão
            # passava com a lente cega. Agora o código de saída conta.
            codigo = mod.demo()
            if codigo:
                ruim = 1
                print(f"  {nome:16} DEMO REPROVOU (codigo {codigo})")
            else:
                print(f"  {nome:16} DEMO VERDE")
        except Exception:
            ruim = 1
            print(f"  {nome:16} DEMO REPROVOU")
            traceback.print_exc()
    return ruim


def achados_de_scripts():
    import checa_scripts
    v = checa_scripts.Varredura(checa_scripts.leitor.RAIZ_PADRAO)
    v.roda()
    return [dict(ferramenta="scripts", regra=x.sigla, classe=x.classe,
                 regiao=nome_de_regiao(x.regiao)) for x in v.achados]


def achados_de_texto():
    import checa_texto
    v = checa_texto.Varredura(checa_texto.leitor.RAIZ_PADRAO)
    v.roda()
    return [dict(ferramenta="texto", regra=x.sigla, classe=x.classe,
                 regiao=nome_de_regiao(x.regiao)) for x in v.achados]


def achados_de_mapas():
    import mapas_qa
    ach, _nao_medido, _censo, _ = mapas_qa.varre(mapas_qa.REPO)
    return [dict(ferramenta="mapas", regra=a["regra"], classe=a["classe"],
                 regiao=nome_de_regiao(a["regiao"])) for a in ach.itens]


def achados_de_estado():
    import estado_jogo
    _ctx, ach = estado_jogo.roda(sorted(estado_jogo.SECOES))
    saida = []
    for a in ach:
        # `estado_jogo` escreve a regiao em minuscula e JUNTA as regioes de um
        # achado que toca mais de uma ("galar+kanto": o Ho-Oh que divide flag de
        # esconder entre tres mapas de tres regioes). Aqui ele conta em CADA
        # uma, que e como o relatorio da auditoria conta, senao aparece uma
        # coluna nova por combinacao e a tabela deixa de ser lida.
        for r in str(a.get("regiao") or "comum").split("+"):
            saida.append(dict(ferramenta="estado", regra=a.get("id", "?"),
                              classe=a["classe"], regiao=nome_de_regiao(r)))
    return saida


def achados_de_warps():
    import lente_warps
    ach, _censo = lente_warps.varre()
    return [dict(ferramenta="warps", regra=a["regra"], classe=a["classe"],
                 regiao=nome_de_regiao(a["regiao"])) for a in ach]


def nome_de_regiao(r):
    r = (r or "").strip()
    if r in ("", "global", "comum"):
        return "comum"
    return r.capitalize() if r.islower() else r


def achados_de_portas():
    import lente_portas
    ach, _censo = lente_portas.varre()
    return [dict(ferramenta="portas", regra=a["regra"], classe=a["classe"],
                 regiao=nome_de_regiao(a["regiao"])) for a in ach]


COLETORES = (("scripts", achados_de_scripts), ("texto", achados_de_texto),
             ("mapas", achados_de_mapas), ("estado", achados_de_estado),
             ("warps", achados_de_warps), ("portas", achados_de_portas))

REGIOES = ("Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Galar", "comum")


def normaliza(c):
    return {"provavel": "provável", "cosmetico": "cosmético"}.get(c, c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.demo:
        return roda_demos()

    todos, falhou = [], 0
    for nome, fn in COLETORES:
        try:
            itens = fn()
        except Exception:
            falhou = 1
            print(f"{nome}: VARREDURA QUEBROU")
            traceback.print_exc()
            continue
        for x in itens:
            x["classe"] = normaliza(x["classe"])
        todos.extend(itens)
        print(f"{nome}: {len(itens)} achados")

    por = collections.Counter((x["classe"], x["regiao"]) for x in todos)
    # "sem interior" é classe da `lente_portas`: porta que o jogador vê, não
    # abre, e cujo interior NÃO EXISTE na árvore. Não é trava porque consertar
    # exigiria inventar mapa, e não é falso positivo porque o defeito é real.
    classes = [c for c in ("trava", "provável", "sem interior", "cosmético",
                           "falso positivo")
               if any(k[0] == c for k in por)]
    regioes = [r for r in REGIOES if any(k[1] == r for k in por)]
    extras = sorted({k[1] for k in por} - set(regioes))
    regioes += extras

    larg = max(len(c) for c in classes) if classes else 6
    print("\n" + " " * (larg + 2) + "".join(f"{r:>9}" for r in regioes) + f"{'total':>9}")
    for c in classes:
        linha = "".join(f"{por[(c, r)]:>9}" for r in regioes)
        print(f"{c:<{larg}}  " + linha + f"{sum(por[(c, r)] for r in regioes):>9}")
    print(f"\ntotal de achados: {len(todos)}")

    print("\nvereditos de calibracao ja medidos (nao reabrir):")
    for regra, veredito in sorted(VEREDITOS_DE_CALIBRACAO.items()):
        print(f"  {regra:5} {veredito}")
    print("\nachados nominais ja abertos e medidos (nao reabrir):")
    for caso, veredito in sorted(VEREDITOS_DE_CASO.items()):
        print(f"  {caso}\n      {veredito}")

    if a.json:
        json.dump(todos, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"\ngravado em {a.json}")
    return falhou


if __name__ == "__main__":
    sys.exit(main() or 0)
