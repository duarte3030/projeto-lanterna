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
import glob
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
    # Sinnoh saiu de fontes-mapas/sinnoh para o pokeplatinum em 05/08/2026. O
    # motivo esta na ARMADILHA da funcao p(): a fonte antiga tem ZERO NPC nos
    # mapas de Sinnoh, entao ela media "objetos" contra um denominador vazio e
    # imprimia "fonte 0". O pokeplatinum tem os 2278 objetos de verdade, so que
    # em outro formato (events_*.json ligados por MAP_HEADER). Ver le_plat().
    "Sinnoh": {"grupo": "Sinnoh",         "fonte": f"{FONTES}/pokeplatinum",
               "plat": True},
    # BW3G e pokecrystal (gen 2). O formato e outro, mas e legivel: cada mapa
    # tem um .asm com warp_event, bg_event e object_event em macro. Eu tinha
    # marcado "sem fonte" por nao ter escrito o leitor, o que e diferente de nao
    # dar para medir. Ver le_gen2().
    "Unova":  {"grupo": "Unova",          "fonte": "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/bw3g",
               "gen2": True},
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
    n = re.sub(r"^Unova_", "", n)          # Unova_AccumulaTown == AccumulaTown
    # No BW3G a rota e "R5NimbasaGate"; aqui ela virou "Rt5NimbasaGate". Sem
    # esta linha o painel dava 45 mapas de Unova como ausentes, sendo que a
    # maioria estava dentro da ROM com outro nome.
    n = re.sub(r"^R(?=\d)", "Rt", n)
    return n.lower().replace("_", "")


def le_gen2(caminho):
    """Conta eventos num mapa de pokecrystal (.asm com macros).

    O gen 2 guarda os eventos como linhas de macro no proprio .asm do mapa:
        warp_event  4, 6, R_2_ACCUMULA_GATE, 3
        bg_event   24, 14, BGEVENT_READ, AccumulaTownSign
        object_event 19, 9, SPRITE_POKEFAN_M, ...
    Contar linha de macro e a leitura certa aqui, e da o mesmo numero que o
    map.json de gen 3 daria depois de convertido.
    """
    if not os.path.exists(caminho):
        return None
    txt = open(caminho, errors="ignore").read()
    return {
        "warp_events": len(re.findall(r"^\s*warp_event\b", txt, re.M)),
        "bg_events": len(re.findall(r"^\s*bg_event\b", txt, re.M)),
        "object_events": len(re.findall(r"^\s*object_event\b", txt, re.M)),
    }


def cidades_de_outra_fonte(fonte_atual=""):
    """Prefixo de nome (a parte antes do primeiro '_') das cidades que vieram
    de OUTRA fonte. `CeladonCity_PokemonCenter` do hns e o
    `CeladonCity_PokemonCenter_1F` do pokefirered sao o mesmo lugar, mas o nome
    difere no sufixo, entao o desconto por nome inteiro nao pega. O que nao
    varia e a cidade. Sem isto, Johto saia com 63,6% dos mapas por causa de 92
    mapas de Kanto que ja estao no jogo, vindos do FireRed com outro nome."""
    cidades = set()
    for f in ("pokefirered", "pokeemerald"):
        # ARMADILHA que eu cai: sem esta linha, medir Kanto contra o
        # pokefirered descontava o pokefirered inteiro e Kanto dava 100,0% com
        # qualquer buraco. A fonte da propria regiao nunca entra no desconto.
        if f in fonte_atual:
            continue
        raiz = f"{FONTES}/{f}/data/maps"
        if os.path.isdir(raiz):
            cidades |= {m.split("_")[0].lower() for m in os.listdir(raiz)
                        if os.path.isdir(f"{raiz}/{m}")}
    return cidades


# Mapa que a fonte tem e que nao e conteudo: rascunho do autor do hack e
# variante de horario, que aqui nao existe como mapa separado.
LIXO = re.compile(r"^(NewMap|Trees|.*_Temp|Gate_)|(Day|Night)$", re.I)


def mapas_so_na_fonte(deles, nosso_mg, fonte=""):
    nossos = {normaliza(x) for x in nosso_mg}
    cidades = cidades_de_outra_fonte(fonte)
    return [m for k, m in deles.items()
            if k not in nossos
            and m.split("_")[0].lower() not in cidades
            and not LIXO.search(m)]


def le_plat(fonte, header):
    """Conta eventos num mapa do pokeplatinum (formato de DS).

    O mapa la nao guarda os eventos: guarda o NOME do arquivo de eventos, em
    include/data/map_headers.h. Placa de rua no Platinum e object_event com
    grafico de SIGNBOARD, nao bg_event, entao ela e contada como placa aqui,
    senao o denominador de "placas" fica quase zero e a coluna mente para cima.
    """
    import importa_npcs_sinnoh as I
    arq = I.headers_do_platinum().get(header)
    if not arq:
        return None
    p = f"{fonte}/res/field/events/{arq[0]}.json"
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    objs = d.get("object_events") or []
    placas = [o for o in objs
              if any(t in o.get("graphics_id", "") for t in I.GRAFICOS_PLACA)]
    return {"object_events": len(objs) - len(placas),
            "warp_events": len(d.get("warp_events") or []),
            "bg_events": len(d.get("bg_events") or []) + len(placas)}


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

        gen2, plat = cfg.get("gen2"), cfg.get("plat")
        if plat:
            sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
            import importa_npcs_sinnoh as I
            heads = I.headers_do_platinum()
            deles = {}
            for h in heads:
                deles.setdefault(I.chave(h), h)
            nossos = I.nossos_mapas_sinnoh()
            casados = [(m, I.APELIDOS.get(m) or deles.get(I.chave(m)))
                       for m in nossos]
            casados = [(m, h) for m, h in casados if h in heads]
            casadas_norm = {I.chave(h) for _, h in casados}
            so_na_fonte = [h for k, h in deles.items() if k not in casadas_norm]
        else:
            if gen2:
                deles = {normaliza(os.path.basename(f)[:-4]): os.path.basename(f)[:-4]
                         for f in glob.glob(f"{fonte}/maps/*.asm")}
            else:
                deles = {normaliza(m): m for m in todos_os_mapas(fonte)}
            nossos = nossos_da_regiao(nosso_mg, cfg["grupo"])
            casados = [(m, deles[normaliza(m)]) for m in nossos if normaliza(m) in deles]
            so_na_fonte = mapas_so_na_fonte(deles, nosso_mg, fonte)
        # Mapas que a FONTE tem e nos nao.
        #
        # ARMADILHA: o denominador tem que descontar o que ja veio por OUTRA
        # fonte. O hns e um hack de Johto E Kanto, entao ele tem PalletTown,
        # ViridianCity e mais 730. Comparando so contra os nossos mapas de
        # Johto, esses 732 apareciam como "faltando" e Johto saia com 23,3% dos
        # mapas, quando o que falta de verdade e outra coisa. Nos importamos
        # Kanto do pokefirered, entao eles JA ESTAO no jogo.
        # Por isso o desconto e contra TODOS os nossos mapas, nao so os da regiao.

        soma_n = {c: 0 for c, _ in CAMPOS}
        soma_f = {c: 0 for c, _ in CAMPOS}
        piores = []
        for meu, seu in casados:
            a = eventos(RAIZ, meu)
            b = (le_plat(fonte, seu) if plat else
                 le_gen2(f"{fonte}/maps/{seu}.asm") if gen2 else
                 eventos(fonte, seu))
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
            # ARMADILHA: denominador zero nao e "nao da para medir", e um FATO
            # sobre a fonte. A fonte de Sinnoh tem 2778 objetos no total e ZERO
            # nos 69 mapas de cidade de Sinnoh: os objetos dela sao todos de
            # Hoenn. Ou seja, nao ha NPC de Sinnoh para importar dali, e quem
            # quiser fechar essa lacuna tem que ir no pokeplatinum.
            # Imprimir "n/a" escondia isso; agora diz que a fonte esta vazia.
            if not soma_f[c]:
                return "fonte 0" if soma_n[c] else "  --  "
            return f"{100*soma_n[c]/soma_f[c]:5.1f}%"
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
