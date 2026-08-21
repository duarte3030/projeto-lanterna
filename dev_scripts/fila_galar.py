#!/usr/bin/env python3
"""A FILA DE CONTEUDO DE GALAR: o que a obra de geometria deixou por escrever.

    python3 dev_scripts/fila_galar.py            # so o resumo por tipo e bloqueio
    python3 dev_scripts/fila_galar.py --gravar   # escreve dev_scripts/fila_galar.json
    python3 dev_scripts/fila_galar.py --demo     # autoteste, nao escreve nada

## Por que este arquivo existe

A obra G0..G5 trouxe 438 mapas, 1.473 warps, 1.204 NPCs e 33 itens escondidos de
Galar, e NENHUMA cena: por decisao 1 do PLANO-OBRAS-GALAR.md, cena, treinador e
encontro sao fase de conteudo. Sem uma fila GERADA, o tamanho dessa fase viraria
numero escrito a mao num documento, que e exatamente o que o `fila_b6.py`
existe para nao deixar acontecer (ver o cabecalho dele: 104 x 107 x 40 cenas de
changeblock, tres numeros para a mesma coisa, em tres arquivos).

Entao esta fila e SAIDA DE VARREDURA dos dois censos que a obra ja gera
(`galar_gente.json` e `galar_mundo.json`), nunca texto digitado. Rodar de novo
depois de qualquer leva reconta a verdade daquele dia. `fila_galar.json` e
artefato gerado: nao editar a mao.

## Fila e COBRANCA, nao certeza

Cada linha diz "aqui a fonte tem alguma coisa e nos nao temos". Ela NAO promete
que a coisa vale a pena: o demake tem placa que so diz o nome da cidade e NPC
que repete a fala do vizinho. Quem executar a fase de conteudo decide item a
item, e a decisao volta para ca como `status`, com o motivo escrito na linha,
igual ao que o `fila_b6.py` aprendeu em 18/08/2026 (`feita`, `descartada`,
`adiada`).

## VOCABULARIO ESTAVEL, que e a licao que quase custou caro em Sinnoh

A chave de cada linha e da FONTE (`gNNmMM` + tipo + indice na lista da fonte), e
nunca o nosso nome de mapa. Dois motivos MEDIDOS:

1. o G3 RENOMEIA 140 dos 438 mapas pelo grafo de warps (`Galar_Postwick14` virou
   `Galar_Motostoke23`), entao chave por nome nosso se desfaz sozinha na proxima
   rodada de renomeacao;
2. e a licao do `--gravar` da maquina de Sinnoh (ESTADO 0.e): quando a lista de
   entrada muda de tamanho, tudo que foi numerado por posicao anda de lugar
   embaixo de quem ja citou o numero. Aqui isso apareceria como status de uma
   linha migrando para outra pendencia, calado.

Por isso o nome nosso entra na linha como INFORMACAO (`mapa`), e a identidade e
`chave`. Quem consumir esta fila casa por `chave`.

## Os quatro tipos, e de onde cada um sai

    script_objeto   NPC que na fonte tem ponteiro de script e aqui entrou MUDO
                    (`script "0"`), ou nem entrou. Sai do censo do G4.
    placa           bg_event que na fonte aponta para texto e aqui nao tem
                    script. Sai do censo do G4.
    map_script      mapa cujo header da fonte tem ponteiro de map script
                    (ON_TRANSITION, ON_FRAME e irmaos). Sai do censo do G3
                    (`map_script_ptr` no de-para).
    porta_morta     warp da fonte que nao tem destino representavel na ROM e por
                    isso aponta para si mesmo. Sai do censo do G3
                    (`pendencias_warp`). E o unico tipo que e pendencia de MAPA
                    e nao de cena.

O que NAO entra, de proposito, com o motivo medido em cada caso:

    - NPC que virou mudo E cuja fonte tambem nao tem script (`script_fonte` 0):
      nao ha o que portar, so desenho, e ele ja esta na tela.
    - objeto cujo grafico e Pokemon ou cenario: o G4 ja decidiu que nao vira NPC
      (1.549 + 438 linhas de censo), e "portar" seria inventar personagem.
    - warp em tile que nao dispara: tem censo proprio no G3
      (`warps_sem_gatilho`), e 464 dos 466 sao fieis a fonte, ou seja nao ha
      trabalho pendente ali. Ver o docstring de `mundo_galar.warps_sem_gatilho`.
"""
import argparse
import collections
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSO_GENTE = f"{RAIZ}/dev_scripts/galar_gente.json"
CENSO_MUNDO = f"{RAIZ}/dev_scripts/galar_mundo.json"
FILA = f"{RAIZ}/dev_scripts/fila_galar.json"

# Status que uma linha pode ter. Os quatro sao os mesmos do fila_b6.py, para
# quem le uma fila ler a outra sem aprender vocabulario novo.
STATUS = ("pendente", "feita", "descartada", "adiada")

# Ponteiro nulo da fonte, nas duas grafias que os censos usam.
NULOS = ("0x0", "0x00000000", "0", None, 0)


INC_FALA = f"{RAIZ}/data/scripts/galar_fala.inc"
ROTEIROS = f"{RAIZ}/dev_scripts/galar_roteiros.json"

# DECISAO DA CONDUTORA, 21/08/2026 (duvida 1 da fase de conteudo). Os NPCs que a
# FONTE manda falar e que o G4 NAO pos no mapa (grafico de Pokemon ou de
# cenario, tile nao andavel, tile de warp) NAO voltam para o mapa so porque a
# fala existe: por o sprite substituto de volta mentiria a especie, que e a
# mesma lei que valeu em Sinnoh, e realocar despeja fantasma dentro de sala
# pequena (medido no G4, ver o filtro 2 de gente_galar.py). Ficam DESCARTADAS
# com motivo, para ninguem reabrir sem querer.
DESCARTE_FORA_DO_MAPA = ("fonte manda falar, G4 nao pos no mapa: sprite "
                         "mentiria especie (decisao da condutora, 21/08/2026)")


def baldes():
    """{chave: balde} de dev_scripts/galar_roteiros.json, se ele existir."""
    if not os.path.exists(ROTEIROS):
        return {}
    return {l["chave"]: l.get("balde")
            for l in json.load(open(ROTEIROS)).get("linhas", [])}


def map_scripts_vazios(de_para):
    """Chaves cujo `map_script_ptr` aponta para uma TABELA VAZIA na fonte.

    MEDIDO em 21/08/2026: `map_script_ptr` nao aponta para bytecode, aponta para
    a tabela `.byte tipo / .4byte script` terminada por tipo 0 (asm/macros/map.inc
    do FireRed). Sessenta e dois dos 256 mapas com ponteiro tem a tabela VAZIA no
    primeiro byte: nao ha cena nenhuma para portar ali, e cobra-las era a fila
    mentindo para cima. Le-se a fonte, nao um campo escrito.

    Sem o datamine em disco a leitura nao acontece e a fila fica como estava,
    dizendo isso em voz alta: silencio aqui viraria 62 linhas ressuscitando
    calado na proxima rodada.
    """
    try:
        import fala_galar
        rom = open(fala_galar.ROM_FONTE, "rb").read()
    except Exception as e:                                          # noqa: BLE001
        print("AVISO: nao consegui abrir a fonte para medir map script (%s);"
              " as 62 linhas de tabela vazia continuam na fila" % e)
        return set()
    vazios = set()
    for chave, d in de_para.items():
        ptr = d.get("map_script_ptr")
        if ptr in NULOS:
            continue
        if not fala_galar.tabela_de_map_script(rom, int(ptr, 16)):
            vazios.add(chave)
    return vazios


def feitas():
    """{chave: motivo} MEDIDO na arvore, lendo os rotulos gravados no .inc.

    A fase de conteudo (baldes a e b, `dev_scripts/fala_galar.py`) grava
    `GalarFala_<CHAVE DA FONTE>_o<N>` / `_bg<N>`. Ler o rotulo e ler o que EXISTE
    no jogo; escrever "feita" a mao no JSON seria acreditar num campo, que e
    exatamente o que a rodada de 19/08 tirou desta fila (ESTADO 0.h, "a fila
    passou a CALCULAR bloqueio").
    """
    if not os.path.exists(INC_FALA):
        return {}
    achados = {}
    for k, tipo, i in re.findall(r"^GalarFala_([Gg]\d+[Mm]\d+)_(o|bg)(\d+)::",
                                 open(INC_FALA).read(), re.M):
        chave = "%s/%s/%d" % (k.lower(), "objeto" if tipo == "o" else "bg", int(i))
        achados[chave] = "escrita por dev_scripts/fala_galar.py (balde a ou b)"
    return achados


def carrega():
    return json.load(open(CENSO_GENTE)), json.load(open(CENSO_MUNDO))


def decisoes_anteriores():
    """{chave: (status, motivo)} do que ja foi decidido em rodada anterior.

    HISTORIA, no mesmo sentido do `alias_ja_gravados` da maquina de Sinnoh:
    status que alguem escreveu nao pode ser apagado por uma regeneracao. Linha
    que sumiu da varredura tambem nao volta como pendente; ela some, e isso e
    visivel no placar.
    """
    if not os.path.exists(FILA):
        return {}
    doc = json.load(open(FILA))
    return {l["chave"]: (l.get("status", "pendente"), l.get("motivo_do_status", ""))
            for l in doc.get("linhas", [])}


def varre():
    gente, mundo = carrega()
    de_para = mundo["de_para"]
    linhas = []

    def nome_de(chave):
        return de_para.get(chave, {}).get("nome", chave)

    for l in gente["linhas"]:
        ptr = l.get("script_fonte")
        if l["tipo"] == "objeto":
            # So cobra quem a fonte mandou falar. Sem ponteiro nao ha cena.
            if ptr in NULOS:
                continue
            entrou = l.get("motivo", "").startswith("entrou mudo")
            linhas.append({
                "chave": "%s/objeto/%d" % (l["mapa"], l["i"]),
                "tipo": "script_objeto",
                "mapa": nome_de(l["mapa"]), "mapa_fonte": l["mapa"],
                "x": l.get("x"), "y": l.get("y"),
                "ponteiro_fonte": ptr,
                "no_mapa": entrou,
                "trainer_type_fonte": l.get("trainer_type_fonte", 0),
                "flag_fonte": l.get("flag_fonte", 0),
                "bloqueio": "" if entrou else
                            "o NPC nao esta no mapa: %s" % l.get("motivo", ""),
            })
        elif l["tipo"] == "bg" and l.get("motivo", "").startswith("placa/script"):
            if ptr in NULOS:
                continue
            linhas.append({
                "chave": "%s/bg/%d" % (l["mapa"], l["i"]),
                "tipo": "placa",
                "mapa": nome_de(l["mapa"]), "mapa_fonte": l["mapa"],
                "x": l.get("x"), "y": l.get("y"),
                "ponteiro_fonte": ptr,
                "no_mapa": False,
                "bloqueio": "",
            })

    vazios = map_scripts_vazios(de_para)
    for chave, d in de_para.items():
        ptr = d.get("map_script_ptr")
        if ptr in NULOS or chave in vazios:
            continue
        linhas.append({
            "chave": "%s/map_script" % chave,
            "tipo": "map_script",
            "mapa": d["nome"], "mapa_fonte": chave,
            "x": None, "y": None,
            "ponteiro_fonte": ptr,
            "no_mapa": True,
            "bloqueio": "",
        })

    for p in mundo.get("pendencias_warp", []):
        linhas.append({
            "chave": "%s/warp/%d" % (p["mapa_fonte"], p["warp"]),
            "tipo": "porta_morta",
            "mapa": nome_de(p["mapa_fonte"]), "mapa_fonte": p["mapa_fonte"],
            "x": p.get("x"), "y": p.get("y"),
            "ponteiro_fonte": None,
            "no_mapa": True,
            "bloqueio": p.get("motivo", ""),
        })

    linhas.sort(key=lambda l: l["chave"])
    velhas = decisoes_anteriores()
    prontas = feitas()
    balde = baldes()
    for l in linhas:
        st, motivo = velhas.get(l["chave"], ("pendente", ""))
        if (l["tipo"] == "script_objeto" and not l["no_mapa"]
                and balde.get(l["chave"]) in ("a_fala", "b_flag")):
            st, motivo = "descartada", DESCARTE_FORA_DO_MAPA
        if l["chave"] in prontas:
            st, motivo = "feita", prontas[l["chave"]]
        l["status"] = st
        l["motivo_do_status"] = motivo
    return linhas, velhas


def placar(linhas):
    por_tipo = collections.defaultdict(collections.Counter)
    for l in linhas:
        por_tipo[l["tipo"]][l["status"]] += 1
        if l["status"] == "pendente" and l["bloqueio"]:
            por_tipo[l["tipo"]]["_bloqueadas"] += 1
    return por_tipo


def imprime(linhas, velhas):
    p = placar(linhas)
    print("%-16s %9s %7s %11s %8s   %s" %
          ("tipo", "pendente", "feita", "descartada", "adiada", "das pendentes, bloqueadas"))
    for tipo in sorted(p):
        c = p[tipo]
        print("%-16s %9d %7d %11d %8d   %d"
              % (tipo, c["pendente"], c["feita"], c["descartada"], c["adiada"],
                 c["_bloqueadas"]))
    print("%-16s %9d de %d linhas"
          % ("TOTAL", sum(1 for l in linhas if l["status"] == "pendente"), len(linhas)))
    sumiram = set(velhas) - {l["chave"] for l in linhas}
    if sumiram:
        print("\n%d chaves com decisao anterior sumiram da varredura (base mudou): %s"
              % (len(sumiram), sorted(sumiram)[:5]))


def demo():
    linhas, velhas = varre()
    falhas = []

    # 1. chave unica: fila com chave repetida perde decisao ao regenerar
    dup = [k for k, n in collections.Counter(l["chave"] for l in linhas).items() if n > 1]
    if dup:
        falhas.append("chaves repetidas: %s" % dup[:5])

    # 2. a chave e da FONTE, nunca do nome nosso (o G3 renomeia 140 mapas)
    nomes = {l["mapa"] for l in linhas}
    if any(n in k for l in linhas for k in [l["chave"]] for n in [l["mapa"]] if n.startswith("Galar_")):
        falhas.append("chave carrega nome nosso; renomeacao do G3 a quebraria")

    # 3. status so do vocabulario
    fora = {l["status"] for l in linhas} - set(STATUS)
    if fora:
        falhas.append("status fora do vocabulario: %s" % sorted(fora))

    # 4. nada de ponteiro nulo virando cobranca (menos porta_morta, que nao tem)
    nulos = [l["chave"] for l in linhas
             if l["tipo"] != "porta_morta" and l["ponteiro_fonte"] in NULOS]
    if nulos:
        falhas.append("%d linhas cobram cena de ponteiro nulo" % len(nulos))

    # 5. idempotencia: varrer duas vezes da a mesma fila
    outra, _ = varre()
    if [l["chave"] for l in outra] != [l["chave"] for l in linhas]:
        falhas.append("varredura nao e idempotente")

    # 6. a fila cobre os quatro tipos e nao esta vazia
    tipos = {l["tipo"] for l in linhas}
    if tipos != {"script_objeto", "placa", "map_script", "porta_morta"}:
        falhas.append("tipos fora do esperado: %s" % sorted(tipos))

    # 7. contraprova de que a fila LE o censo e nao um numero cravado: o total de
    # map_script tem que bater com os ponteiros nao nulos do de-para do G3.
    _gente, mundo = carrega()
    vazios = map_scripts_vazios(mundo["de_para"])
    esperado = sum(1 for chave, d in mundo["de_para"].items()
                   if d.get("map_script_ptr") not in NULOS and chave not in vazios)
    achado = sum(1 for l in linhas if l["tipo"] == "map_script")
    if esperado != achado:
        falhas.append("map_script: fila diz %d, censo do G3 menos tabela vazia "
                      "diz %d" % (achado, esperado))
    # 8. a tabela vazia nao pode voltar sozinha: nenhuma linha de map_script
    # sobrevivente pode ter tabela vazia na fonte.
    vivas = {l["mapa_fonte"] for l in linhas if l["tipo"] == "map_script"}
    if vivas & vazios:
        falhas.append("%d map_script de tabela vazia voltaram para a fila"
                      % len(vivas & vazios))

    print("\n".join("  FALHA " + f for f in falhas) if falhas else "demo: OK")
    imprime(linhas, velhas)
    return 1 if falhas else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gravar", action="store_true")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo:
        raise SystemExit(demo())
    linhas, velhas = varre()
    imprime(linhas, velhas)
    if a.gravar:
        json.dump({"gerado_por": "dev_scripts/fila_galar.py",
                   "fonte_dos_censos": ["dev_scripts/galar_gente.json",
                                        "dev_scripts/galar_mundo.json"],
                   "status_possiveis": list(STATUS),
                   "linhas": linhas},
                  open(FILA, "w"), indent=1, ensure_ascii=False)
        print("\ngravado em %s (%d linhas)" % (FILA, len(linhas)))
    else:
        print("\n(nada gravado; use --gravar)")


if __name__ == "__main__":
    main()
