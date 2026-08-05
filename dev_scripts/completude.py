#!/usr/bin/env python3
"""Quanto de cada regiao ja esta pronto, medido CONTRA A FONTE dela, MAPA A MAPA.

Uso:
    python3 dev_scripts/completude.py
    python3 dev_scripts/completude.py --detalhe Johto

Existe porque numero cru nao significa nada. "82% dos warps disparam" nao diz se
isso e bom: o proprio jogo original nunca chega a 100%, porque muita porta e
trocada por script em tempo de execucao e muito warp so e usado por barco ou
cutscene, sem ninguem pisar nele.

A regua certa e a FONTE. 100% quer dizer "tao completo quanto o jogo de onde a
regiao veio", nao "perfeito".

    Hoenn  -> pret/pokeemerald   (nossa Hoenn e o vanilla; deve dar ~100%)
    Kanto  -> pret/pokefirered
    Johto  -> fontes-mapas/hns
    Sinnoh -> fontes-mapas/sinnoh
    Unova  -> BW3G (gen 2, formato incomparavel: sai como "sem fonte")

PRIMEIRA VERSAO ESTAVA ERRADA e vale registrar: ela casava por NOME DE GRUPO de
mapa. As fontes usam outros nomes de grupo, entao o denominador pegava um punhado
de mapas e Johto saiu com "833% dos mapas" e Hoenn com 270%. Numero acima de 100
era o unico motivo de eu ter olhado de novo; se tivesse dado 91% eu teria
acreditado. **Comparacao so vale se os dois lados falarem do mesmo conjunto**, e
o unico jeito de garantir isso e casar MAPA A MAPA pelo nome.

Regiao sem fonte em disco aparece como "sem fonte", nunca como 100%. Nao saber e
um resultado; fingir que sabe foi o erro que esta sessao cometeu a noite toda.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.dirname(RAIZ) + "/fontes-mapas"

REGIOES = {
    "Kanto":  {"grupo": "Frlg",           "fonte": f"{FONTES}/pokefirered"},
    "Johto":  {"grupo": "Johto",          "fonte": f"{FONTES}/hns"},
    "Hoenn":  {"grupo": "TownsAndRoutes", "fonte": f"{FONTES}/pokeemerald"},
    "Sinnoh": {"grupo": "Sinnoh",         "fonte": f"{FONTES}/sinnoh"},
    "Unova":  {"grupo": "Unova",          "fonte": None},
}

CAMPOS = [("object_events", "objetos (NPC, item)"),
          ("warp_events", "warps"),
          ("bg_events", "placas e sinais")]


def todos_os_mapas(raiz):
    p = f"{raiz}/data/maps/map_groups.json"
    if not os.path.exists(p):
        return {}
    g = json.load(open(p))
    return {m: grp for grp in g.get("group_order", []) for m in g.get(grp, [])}


def nossos_da_regiao(mapa_grupo, chave):
    if chave == "TownsAndRoutes":
        # Hoenn e "tudo que nao e das outras quatro"
        outras = ("frlg", "johto", "sinnoh", "unova")
        return [m for m, g in mapa_grupo.items()
                if not any(o in g.lower() or o in m.lower() for o in outras)]
    return [m for m, g in mapa_grupo.items()
            if chave.lower() in g.lower() or chave.lower() in m.lower()]


def normaliza(nome):
    """Nosso 'PalletTown_Frlg' e o 'PalletTown' da fonte sao o mesmo mapa."""
    n = re.sub(r"_Frlg$", "", nome)
    n = re.sub(r"_johto$", "", n, flags=re.I)
    return n.lower().replace("_", "")


def eventos(raiz, mapa):
    p = f"{raiz}/data/maps/{mapa}/map.json"
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {c: len(d.get(c) or []) for c, _ in CAMPOS}


def main():
    alvo = None
    if "--detalhe" in sys.argv:
        alvo = sys.argv[sys.argv.index("--detalhe") + 1]

    nosso_mg = todos_os_mapas(RAIZ)
    print("Completude por regiao, normalizada pela FONTE, mapa a mapa.")
    print("100% = tao completo quanto o jogo de onde a regiao veio.\n")
    print(f"{'regiao':8} {'mapas':>14} {'objetos':>14} {'warps':>14} {'placas':>14}")

    faltando_total = {}
    for nome, cfg in REGIOES.items():
        if alvo and alvo.lower() != nome.lower():
            continue
        fonte = cfg["fonte"]
        if not (fonte and os.path.isdir(fonte)):
            nossos = nossos_da_regiao(nosso_mg, cfg["grupo"])
            print(f"{nome:8} {len(nossos):>8} sem fonte" + " " * 30)
            continue

        deles = {normaliza(m): m for m in todos_os_mapas(fonte)}
        nossos = nossos_da_regiao(nosso_mg, cfg["grupo"])
        casados = [(m, deles[normaliza(m)]) for m in nossos if normaliza(m) in deles]
        # Mapas que a FONTE tem e nos nao.
        #
        # ARMADILHA: o denominador tem que descontar o que ja veio por OUTRA
        # fonte. O hns e um hack de Johto E Kanto, entao ele tem PalletTown,
        # ViridianCity e mais 730. Comparando so contra os nossos mapas de
        # Johto, esses 732 apareciam como "faltando" e Johto saia com 23,3% dos
        # mapas, quando o que falta de verdade e outra coisa. Nos importamos
        # Kanto do pokefirered, entao eles JA ESTAO no jogo.
        # Por isso o desconto e contra TODOS os nossos mapas, nao so os da regiao.
        todos_nossos_norm = {normaliza(m) for m in nosso_mg}
        so_na_fonte = [m for k, m in deles.items() if k not in todos_nossos_norm]

        soma_n = {c: 0 for c, _ in CAMPOS}
        soma_f = {c: 0 for c, _ in CAMPOS}
        piores = []
        for meu, seu in casados:
            a, b = eventos(RAIZ, meu), eventos(fonte, seu)
            if not a or not b:
                continue
            for c, _ in CAMPOS:
                soma_n[c] += a[c]
                soma_f[c] += b[c]
            if b["object_events"] >= 5:
                r = a["object_events"] / b["object_events"]
                if r < 0.75:
                    piores.append((r, meu, a["object_events"], b["object_events"]))

        def p(c):
            return (f"{100*soma_n[c]/soma_f[c]:5.1f}%"
                    if soma_f[c] else "  n/a ")
        # mapas: o denominador e o que a fonte tem daquela regiao, e para as
        # fontes que sao o jogo inteiro isso e o total delas
        pm = 100.0 * len(casados) / max(1, len(casados) + len(so_na_fonte))
        print(f"{nome:8} {pm:13.1f}% {p('object_events'):>14} "
              f"{p('warp_events'):>14} {p('bg_events'):>14}")
        faltando_total[nome] = (so_na_fonte, sorted(piores)[:6])

    if alvo:
        for nome, (falta, piores) in faltando_total.items():
            print(f"\n=== {nome}: {len(falta)} mapas que a fonte tem e nos nao ===")
            for m in falta[:15]:
                print(f"   {m}")
            if piores:
                print(f"\n=== {nome}: mapas mais vazios que o original ===")
                for r, m, a, b in piores:
                    print(f"   {100*r:5.1f}%  {m:42} {a} de {b} objetos")
    else:
        print("\nuse --detalhe <regiao> para ver o que falta em cada uma")
    return 0


def demo():
    """Duas regras que a primeira versao quebrou."""
    # 1. mapa da fonte com sufixo nosso e o MESMO mapa
    assert normaliza("PalletTown_Frlg") == normaliza("PalletTown")
    assert normaliza("Route3_Frlg") == normaliza("Route3")
    # 2. nomes diferentes continuam diferentes
    assert normaliza("Route3_Frlg") != normaliza("Route4")
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
