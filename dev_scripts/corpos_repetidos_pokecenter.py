#!/usr/bin/env python3
"""Apaga o corpo REPETIDO dos interiores de Sinnoh, com seis provas por objeto.

    python3 dev_scripts/corpos_repetidos_pokecenter.py            # só relata
    python3 dev_scripts/corpos_repetidos_pokecenter.py --aplica
    python3 dev_scripts/corpos_repetidos_pokecenter.py --demo     # autoteste

O defeito, achado pelo Gui no playtest de 06/09/2026
----------------------------------------------------
Foto do `SunyshoreCityPokecenter1F`: além da enfermeira do balcão havia OUTRA
enfermeira parada na frente do balcão, uma terceira ao lado da máquina, e um
segundo menino de cabelo rosa encostado na parede leste. Medido antes de tocar
em nada, contra a fonte:

    fontes-mapas/pokeplatinum/res/field/events/events_*_pokecenter_1f.json

Os DEZOITO Pokécenters 1F do Platinum têm **exatamente UMA** enfermeira cada
(`OBJ_EVENT_GFX_POKECENTER_NURSE`, sempre em (8,4) da grade de lá, com o script
de cura). Ou seja: nenhuma daquelas figuras a mais existe no jogo original. Não
são atendentes de Wi-Fi, de Union Room nem de GTS (que o Gui cortou); são cópias
da MESMA pessoa, e entraram por duas portas diferentes:

1. **`fecha_portas_sinnoh.py`, na criação do mapa.** O arquétipo `pc1` copia o
   NPC funcional do índice 0 de `OreburghCity_PokemonCenter_1F` (a enfermeira do
   balcão, com o `Common_EventScript_PkmnCenterNurse`) e o INSERE na posição 0
   do mapa novo, enquanto `conteudo_do_mapa` já tinha importado a enfermeira DA
   FONTE como um objeto qualquer. As duas são a mesma mulher; a importada ficou
   muda, em pé na frente do balcão.

2. **`importa_npcs_sinnoh.py`, nas rodadas de completude.** A guarda de
   idempotência dele (`reclama`) reconhece "já importado" por VIZINHANÇA de até
   um tile. Nestes mapas a planta é REAPROVEITADA do repo, então a coordenada da
   fonte não quer dizer nada: a régua de escala mudou entre rodadas, a mesma
   pessoa caiu em (8,4) numa e em (10,2) na outra, e nenhuma reclamou a outra.
   Foi assim que nasceram o segundo menino de Sunyshore, a segunda LASS de
   Canalave, a segunda WOMAN_3 de Eterna e as demais.

As duas portas foram fechadas nos dois geradores, no mesmo commit desta
ferramenta. Esta aqui é o conserto do que JÁ está escrito, e é idempotente:
rodar de novo depois de aplicar não acha nada.

As seis provas, uma por objeto, todas obrigatórias
-------------------------------------------------
1. **O mapa é Pokécenter 1F de Sinnoh e a fonte dele existe.** Sem o
   `events_<cidade>_pokecenter_1f.json` do Platinum não há teto contra o que
   comparar, e o mapa fica inteiro de fora.
2. **O objeto é MUDO e anônimo**: `script` "0", `flag` "0",
   `TRAINER_TYPE_NONE` e sem `local_id`. Corpo que fala pode ser a única boca de
   alguém; corpo com flag é peça de cena; corpo com `local_id` é citado por nome.
3. **A marca dele é `pokeplatinum`**, ou seja, ele foi IMPORTADO. Objeto
   autoral deste repo não é duplicata de ninguém e não sai por aqui.
4. **A pessoa continua no mapa, e com a fala dela**: existe outro objeto do
   MESMO `graphics_id`, no mesmo mapa, que TEM script. É esta prova que separa
   "cópia" de "a única aparição". Sem ela, apagar seria apagar conteúdo.
5. **A fonte tem MENOS corpos daquele gráfico do que nós** (contando a fonte
   pelo de-para de `valida_mapas_sinnoh.TROCA_SPRITE`, que é o mesmo que o
   importador usou). Enquanto o excesso não zerar, o próximo mudo sai.

A armadilha do apagar, e como ela é desarmada aqui
--------------------------------------------------
Apagar um `object_event` desloca o id de todos os seguintes DO MESMO MAPA,
porque `tools/mapjson` gera `#define <local_id> <posição + 1>`. Duas frentes:

- **Constante nomeada se conserta sozinha.** Os `LOCALID_*_PC_NURSE` destes 15
  mapas apontam todos para a posição 0 (a enfermeira do balcão), que nunca sai,
  e os `#define` escritos à mão em `include/constants/sinnoh/*.h` para estes
  mapas valem todos 1. Conferido linha a linha antes de escrever.
- **Id numérico CRU não se conserta.** `PokemonLeagueNorthPokecenter1F` chama o
  rival por `addobject 7` / `applymovement 7` / `removeobject 7`. Objeto citado
  por número é BATIZADO antes de qualquer remoção (tabela `BATIZA` abaixo): ele
  ganha `local_id` no `map.json` e o número vira a constante no `scripts.inc`.
  Depois disso o deslocamento é problema do `mapjson`, e não de quem lê. Mapa
  que ainda tiver número cru sem batismo é RECUSADO inteiro, com o motivo.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import valida_mapas_sinnoh as V  # noqa: E402

PLAT = os.path.join(os.path.dirname(REPO),
                    "fontes-mapas/pokeplatinum/res/field/events")

# Mapa nosso -> nome da cidade no arquivo de eventos do Platinum.
# Escrito à mão porque o nome da pasta daqui e o do arquivo de lá não se derivam
# um do outro (`FloaromaTown_PokemonCenter_1F` contra `floaroma_town`,
# `PokemonLeagueNorthPokecenter1F` contra `pokemon_league_north`), e derivar por
# regex já pôs agente casando mapa errado neste repo.
PARES = [
    ("CanalaveCityPokecenter1F", "canalave_city"),
    ("CelesticTownPokecenter1F", "celestic_town"),
    ("EternaCityPokecenter1F", "eterna_city"),
    ("FightAreaPokecenter1F", "fight_area"),
    ("FloaromaTown_PokemonCenter_1F", "floaroma_town"),
    ("HearthomeCityPokecenter1F", "hearthome_city"),
    ("JubilifeCity_PokemonCenter_1F", "jubilife_city"),
    ("OreburghCity_PokemonCenter_1F", "oreburgh_city"),
    ("PastoriaCityPokecenter1F", "pastoria_city"),
    ("PokemonLeagueNorthPokecenter1F", "pokemon_league_north"),
    ("PokemonLeagueSouthPokecenter1F", "pokemon_league_south"),
    ("ResortAreaPokecenter1F", "resort_area"),
    ("SandgemTown_PokemonCenter_1F", "sandgem_town"),
    ("SnowpointCityPokecenter1F", "snowpoint_city"),
    ("SolaceonTownPokecenter1F", "solaceon_town"),
    ("SunyshoreCityPokecenter1F", "sunyshore_city"),
    ("SurvivalAreaPokecenter1F", "survival_area"),
    ("VeilstoneCityPokecenter1F", "veilstone_city"),
]

# Objeto citado por NÚMERO no scripts.inc do próprio mapa, que precisa de nome
# antes de qualquer índice andar. Chave: (pasta, id numérico de hoje).
# Valor: a constante que ele passa a ter.
BATIZA = {
    ("PokemonLeagueNorthPokecenter1F", 7): "LOCALID_LEAGUE_NORTH_PC_RIVAL",
}

# Comentário que fica MENTINDO depois do batismo. Trocado junto, porque
# comentário velho é a próxima armadilha: ele diz em voz alta que o objeto não
# tem nome, e quem ler amanhã acredita nele.
COMENTARIO = {
    "PokemonLeagueNorthPokecenter1F": (
        "@ Objeto sem local_id (id 7 por posicao no map.json, sem tocar\n"
        "@ map_event_ids.h). A fonte so faz AddObject dentro desta cena: o objeto\n",
        "@ O rival e citado pela constante LOCALID_LEAGUE_NORTH_PC_RIVAL, que o\n"
        "@ mapjson gera a partir do local_id do map.json. Ate 06/09/2026 ele era\n"
        "@ o id 7 CRU, e id cru anda sozinho quando um objeto anterior sai da\n"
        "@ lista: foi o que aconteceria ao apagar as duas enfermeiras repetidas\n"
        "@ deste mapa (dev_scripts/corpos_repetidos_pokecenter.py).\n"
        "@ A fonte so faz AddObject dentro desta cena: o objeto\n",
    ),
}

# Macros de script que endereçam objeto pelo ID. A lista sai de
# `asm/macros/event.inc`; número cru em qualquer uma delas é a armadilha.
MACROS_DE_OBJETO = ("addobject", "removeobject", "applymovement", "setobjectxy",
                    "turnobject", "showobjectat", "hideobjectat", "showobject",
                    "hideobject", "setobjectmovementtype", "copyobjectxytoperm",
                    "setobjectxyperm", "setobjectsubpriority")
RX_NUMERO = re.compile(r"^\s*(" + "|".join(MACROS_DE_OBJETO) + r")\s+(\d+)\b")
RX_LAST_TALKED = re.compile(r"^\s*setvar\s+VAR_LAST_TALKED\s*,\s*(\d+)\b")


def escreve_json(caminho, dados):
    """Grava o map.json com a MESMA formatacao e o MESMO fim de arquivo.

    Metade dos `map.json` deste repo termina com quebra de linha e a outra
    metade nao, porque cada gerador gravou do seu jeito. `json.dump` cru tira a
    quebra de quem tinha, e o diff da rodada vira "No newline at end of file"
    em arquivo que ninguem pediu para mexer. Aqui o fim do arquivo e lido antes
    e reposto depois.
    """
    fim = "\n" if open(caminho, encoding="utf-8").read().endswith("\n") else ""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
        f.write(fim)


def caminho_mapa(pasta):
    return os.path.join(REPO, "data/maps", pasta, "map.json")


def caminho_inc(pasta):
    return os.path.join(REPO, "data/maps", pasta, "scripts.inc")


def fonte_de(arquivo):
    """O JSON de eventos do Platinum, pelo NOME do arquivo de eventos.

    Ate 08/09/2026 esta funcao montava o nome (`events_<cidade>_pokecenter_1f`)
    e por isso a ferramenta so sabia olhar Pokecenter. Agora o nome vem pronto:
    para Pokecenter ele sai da tabela PARES escrita a mao, e para o resto dos
    interiores de Sinnoh sai do `eventsArchiveID` do proprio header do Platinum,
    lido por `importa_npcs_sinnoh.headers_do_platinum()`, que e o mesmo
    casamento que o IMPORTADOR usou. Casar por regex no nome da pasta ja pos
    agente casando mapa errado neste repo.
    """
    p = os.path.join(PLAT, f"{arquivo}.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def pares_de_interior():
    """[(pasta, arquivo de eventos)] dos interiores de Sinnoh FORA de Pokecenter.

    O casamento sai de `importa_npcs_sinnoh`: apelido escrito a mao primeiro
    (`APELIDOS`), chave normalizada depois (`chave()`), exatamente na ordem que
    o importador usa. Mapa sem par no Platinum simplesmente nao entra: sem
    fonte nao ha teto contra o que comparar, que e a prova 1.
    """
    import importa_npcs_sinnoh as I
    heads = I.headers_do_platinum()
    por_chave = {}
    for h, (ev, _mx) in heads.items():
        por_chave.setdefault(I.chave(h), (h, ev))
    ja = {pasta for pasta, _ in PARES}
    fora = []
    for m in sorted(I.mapas_editaveis_sinnoh()):
        if m in ja:
            continue
        h = I.APELIDOS.get(m)
        alvo = (h, heads[h][0]) if h in heads else por_chave.get(I.chave(m))
        if not alvo:
            continue
        pm = caminho_mapa(m)
        if not os.path.exists(pm):
            continue
        d = json.load(open(pm, encoding="utf-8"))
        if "INDOOR" not in d.get("map_type", ""):
            continue
        fora.append((m, alvo[1]))
    return fora


def de_para(g, pokecenter=True):
    """Grafico da FONTE -> grafico NOSSO, pelo mesmo tradutor do importador.

    `valida_mapas_sinnoh.troca_de_sprite(g, pokecenter)` existe desde 06/09/2026,
    quando parte do de-para passou a depender do MAPA (a mesma
    `OBJ_EVENT_GFX_POKECENTER_NURSE` e enfermeira no Pokecenter e recepcionista
    no lobby do Contest Hall). Aqui o contexto e sempre Pokecenter, entao a
    chamada e com `True`; o `TROCA_SPRITE` cru fica de reserva para arvore que
    ainda nao tenha a funcao.
    """
    troca = getattr(V, "troca_de_sprite", None)
    if troca:
        return troca(g, pokecenter) or g
    return V.TROCA_SPRITE.get(g, g)


def conta_fonte(fonte, pokecenter=True):
    """{graphics_id NOSSO: quantos corpos a fonte tem}, pelo mesmo de-para."""
    c = {}
    for o in fonte.get("object_events", []):
        g = de_para(o.get("graphics_id", ""), pokecenter)
        c[g] = c.get(g, 0) + 1
    return c


def mudo(o):
    return (str(o.get("script", "0")) == "0"
            and str(o.get("flag", "0")) == "0"
            and o.get("trainer_type", "TRAINER_TYPE_NONE") == "TRAINER_TYPE_NONE"
            and "local_id" not in o)


def numeros_crus(pasta):
    """{id numérico citado no scripts.inc do mapa: quantas vezes}."""
    p = caminho_inc(pasta)
    if not os.path.exists(p):
        return {}
    achados = {}
    for linha in open(p, encoding="utf-8"):
        for rx in (RX_NUMERO, RX_LAST_TALKED):
            m = rx.search(linha)
            if m:
                n = int(m.groups()[-1])
                achados[n] = achados.get(n, 0) + 1
    return achados


def plano():
    """[(pasta, [índices a apagar], [motivo]), ...] e a lista de recusas."""
    saida, recusas = [], []
    alvo_de = [(pasta, f"events_{cidade}_pokecenter_1f", True)
               for pasta, cidade in PARES]
    alvo_de += [(pasta, arq, False) for pasta, arq in pares_de_interior()]
    for pasta, arquivo, pokecenter in alvo_de:
        pm = caminho_mapa(pasta)
        if not os.path.exists(pm):
            continue
        fonte = fonte_de(arquivo)
        if fonte is None:                                   # prova 1
            recusas.append((pasta, "sem fonte no pokeplatinum"))
            continue
        d = json.load(open(pm, encoding="utf-8"))
        objs = d.get("object_events") or []
        cf = conta_fonte(fonte, pokecenter)
        # Quantos corpos de cada gráfico nós temos hoje.
        cn = {}
        for o in objs:
            cn[o["graphics_id"]] = cn.get(o["graphics_id"], 0) + 1
        # Quem FALA, por gráfico: é a prova 4.
        fala = {o["graphics_id"] for o in objs if str(o.get("script", "0")) != "0"}

        alvos = []
        excesso = {g: cn[g] - cf.get(g, 0) for g in cn}
        # De trás para a frente: o corpo repetido é sempre o que entrou por
        # último, e apagar do fim para o começo mantém os índices de quem fica.
        for i in range(len(objs) - 1, -1, -1):
            o = objs[i]
            g = o["graphics_id"]
            if excesso.get(g, 0) <= 0:                      # prova 5
                continue
            if not mudo(o):                                 # prova 2
                continue
            if o.get("origem") != "pokeplatinum":           # prova 3
                continue
            if g not in fala:                               # prova 4
                continue
            alvos.append(i)
            excesso[g] -= 1
        if not alvos:
            continue

        # PROVA 6, e ela nasceu em 08/09/2026 com a extensao para interiores:
        # o conjunto a apagar tem que ser um SUFIXO da lista de objetos do mapa.
        # `SaveBlock1` guarda uma copia dos `objectEventTemplates` do mapa em que
        # o jogador esta, e apagar do MEIO desloca todo mundo depois do buraco:
        # quem salvou naquela sala volta com as pessoas trocadas de lugar. No fim
        # da lista nada anda. Alvo que nao e sufixo NAO e apagado, e o mapa vai
        # para as recusas com o motivo, em vez de sair calado do relatorio.
        n = len(objs)
        sufixo = set(range(n - len(alvos), n))
        if set(alvos) != sufixo:
            recusas.append((pasta, "corpo repetido no MEIO da lista "
                            f"(indices {sorted(alvos)} de {n} objetos): apagar "
                            "ali desloca o indice de objeto, que a save guarda"))
            continue

        # Armadilha do id cru: número que aponta para índice DEPOIS do primeiro
        # apagado anda; número que aponta para um dos apagados some. Os dois
        # casos param o mapa, a menos que o objeto tenha sido batizado.
        crus = numeros_crus(pasta)
        pendentes = sorted(n for n in crus
                           if (pasta, n) not in BATIZA
                           and (n - 1) >= min(alvos))
        if pendentes:
            recusas.append((pasta, f"id numérico cru sem batismo: {pendentes}"))
            continue
        aponta_para_apagado = sorted(n for n in crus if (n - 1) in set(alvos))
        if aponta_para_apagado:
            recusas.append((pasta, f"script cita objeto que sairia: {aponta_para_apagado}"))
            continue
        motivos = [f"[{i}] {objs[i]['graphics_id']} "
                   f"({objs[i]['x']},{objs[i]['y']}) mudo, cópia de quem fala"
                   for i in sorted(alvos)]
        saida.append((pasta, sorted(alvos, reverse=True), motivos))
    return saida, recusas


def batiza(pasta, escrever):
    """Dá nome ao objeto que o scripts.inc chama por número. Idempotente."""
    mudou = []
    for (p, n), const in BATIZA.items():
        if p != pasta:
            continue
        pm, pi = caminho_mapa(pasta), caminho_inc(pasta)
        d = json.load(open(pm, encoding="utf-8"))
        objs = d.get("object_events") or []
        if not (1 <= n <= len(objs)):
            raise SystemExit(f"{pasta}: id {n} fora da lista de objetos")
        alvo = objs[n - 1]
        txt = open(pi, encoding="utf-8").read()
        if alvo.get("local_id") == const and re.search(rf"\b{const}\b", txt):
            continue                                        # já batizado
        if "local_id" in alvo and alvo["local_id"] != const:
            raise SystemExit(f"{pasta}: objeto {n} já se chama {alvo['local_id']}")
        # `local_id` entra como PRIMEIRA chave, que é como o mapjson e os outros
        # map.json deste repo o trazem.
        novo = {"local_id": const}
        novo.update(alvo)
        objs[n - 1] = novo
        linhas = []
        for linha in txt.split("\n"):
            m = RX_NUMERO.search(linha)
            if m and int(m.group(2)) == n:
                linha = re.sub(rf"(\b{m.group(1)}\s+){n}\b", rf"\g<1>{const}", linha)
            m = RX_LAST_TALKED.search(linha)
            if m and int(m.group(1)) == n:
                linha = re.sub(rf"(VAR_LAST_TALKED,\s*){n}\b", rf"\g<1>{const}", linha)
            linhas.append(linha)
        saida_inc = "\n".join(linhas)
        de, para = COMENTARIO.get(pasta, (None, None))
        if de and de in saida_inc:
            saida_inc = saida_inc.replace(de, para)
        if escrever:
            escreve_json(pm, d)
            open(pi, "w", encoding="utf-8").write(saida_inc)
        mudou.append((pasta, n, const))
    return mudou


def aplica(escrever):
    passos, recusas = plano()
    total = 0
    for pasta, alvos, motivos in passos:
        batiza(pasta, escrever)
        pm = caminho_mapa(pasta)
        d = json.load(open(pm, encoding="utf-8"))
        objs = d["object_events"]
        antes = [(o["graphics_id"], o["x"], o["y"]) for o in objs]
        for i in alvos:
            objs.pop(i)
        # Verificação: quem ficou é exatamente quem não estava na lista, na
        # mesma ordem. Contar não basta; a identidade é que importa.
        esperado = [t for k, t in enumerate(antes) if k not in set(alvos)]
        agora = [(o["graphics_id"], o["x"], o["y"]) for o in objs]
        if agora != esperado:
            raise SystemExit(f"{pasta}: a remoção mexeu em quem devia ficar")
        if escrever:
            escreve_json(pm, d)
        total += len(alvos)
        print(f"{pasta}: {len(alvos)} corpo(s) repetido(s)")
        for m in motivos:
            print("   " + m)
    for pasta, motivo in recusas:
        print(f"RECUSADO {pasta}: {motivo}")
    print(f"\n{total} objetos em {len(passos)} mapas"
          + ("" if escrever else "  (nada escrito: use --aplica)"))
    return 0


def demo():
    """Autoteste: as cinco provas, cada uma no seu caso, sem tocar no repo."""
    ok = True

    def cobra(cond, nome):
        nonlocal ok
        print(("OK   " if cond else "FALHA") + "  " + nome)
        ok = ok and cond

    # 1. Toda fonte de Pokécenter 1F do Platinum tem UMA enfermeira. É o fato em
    #    que a prova 5 se apoia; se um dia deixar de valer, o demo cai antes.
    n = []
    for _, cidade in PARES:
        f = fonte_de(f"events_{cidade}_pokecenter_1f")
        if f is None:
            continue
        n.append(sum(1 for o in f["object_events"]
                     if o.get("graphics_id") == "OBJ_EVENT_GFX_POKECENTER_NURSE"))
    cobra(bool(n) and set(n) == {1},
          f"as {len(n)} fontes têm exatamente uma enfermeira cada")

    # 2. `mudo` recusa quem fala, quem tem flag, quem batalha e quem tem nome.
    base = {"script": "0", "flag": "0", "trainer_type": "TRAINER_TYPE_NONE"}
    cobra(mudo(dict(base)), "mudo() aceita corpo mudo e anônimo")
    cobra(not mudo(dict(base, script="X_EventScript_Npc1")), "mudo() recusa quem fala")
    cobra(not mudo(dict(base, flag="FLAG_X")), "mudo() recusa quem tem flag")
    cobra(not mudo(dict(base, local_id="LOCALID_X")), "mudo() recusa quem tem nome")
    cobra(not mudo(dict(base, trainer_type="TRAINER_TYPE_NORMAL")),
          "mudo() recusa treinador")

    # 3. O de-para da contagem da fonte é o MESMO do importador.
    cobra(de_para("OBJ_EVENT_GFX_POKECENTER_NURSE") == "OBJ_EVENT_GFX_NURSE",
          "de-para: POKECENTER_NURSE -> NURSE")

    # 4. O leitor de id cru acha o número que a armadilha usa.
    crus = numeros_crus("PokemonLeagueNorthPokecenter1F")
    cobra(7 in crus or "LOCALID_LEAGUE_NORTH_PC_RIVAL" in
          open(caminho_inc("PokemonLeagueNorthPokecenter1F"), encoding="utf-8").read(),
          "id cru 7 do League North achado, ou já batizado")

    # 5. O casamento dos interiores existe, sai do importador e nao inventa par.
    #    Se ele voltar VAZIO, a extensao de 08/09/2026 morreu calada e a
    #    ferramenta volta a ser so de Pokecenter sem ninguem perceber.
    inter = pares_de_interior()
    cobra(len(inter) > 100,
          f"casamento de interior nao vazio ({len(inter)} mapas)")
    pastas = {p for p, _ in inter}
    cobra(not (pastas & {p for p, _ in PARES}),
          "interior e Pokecenter nao se sobrepoem")
    cobra(all(fonte_de(a) is not None for _, a in inter),
          "todo par de interior aponta para um arquivo de eventos que existe")

    # 6. MUTACAO PLANTADA da prova 6, a do sufixo. Um alvo no MEIO da lista tem
    #    que ser RECUSADO, e o mesmo alvo no FIM tem que passar. Sem isso a
    #    regra que protege o indice de objeto da save poderia sumir num refactor
    #    e o `--demo` continuaria verde.
    def sufixo_ok(alvos, total):
        return set(alvos) == set(range(total - len(alvos), total))
    cobra(sufixo_ok([4], 5) and sufixo_ok([3, 4], 5),
          "regra do sufixo aceita o fim da lista")
    cobra(not sufixo_ok([1], 5) and not sufixo_ok([0, 4], 5),
          "regra do sufixo recusa o meio da lista")

    # 7. Idempotência: depois de aplicado, o plano fica vazio; antes, não.
    passos, recusas = plano()
    sobra = sum(len(a) for _, a, _ in passos)
    so_sufixo = [r for r in recusas if "MEIO da lista" not in r[1]]
    cobra(not so_sufixo, f"nenhuma recusa fora a do sufixo ({so_sufixo})")
    print(f"     plano de agora: {sobra} objetos em {len(passos)} mapas "
          f"(0 quer dizer que já foi aplicado); "
          f"{len(recusas)} recusa(s) pela regra do sufixo")
    return 0 if ok else 1


def main():
    if "--demo" in sys.argv:
        return demo()
    return aplica("--aplica" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
