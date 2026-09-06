#!/usr/bin/env python3
"""Reaplica o de-para de sprite de Sinnoh nos map.json que já foram escritos.

    python3 dev_scripts/de_para_sprites_sinnoh.py            # só relata
    python3 dev_scripts/de_para_sprites_sinnoh.py --aplicar  # escreve os map.json
    python3 dev_scripts/de_para_sprites_sinnoh.py --demo     # autoteste, não grava

POR QUE ESTE ARQUIVO EXISTE, 06/09/2026
---------------------------------------
O Gui jogou a ROM `23d`, entrou na casona do Contest Hall de Hearthome e trouxe
a pergunta: "que tanto de enfermeira é essa?". Medido no `map.json` antes de
tocar em qualquer coisa: `ContestHallLobby` tinha **7 objetos
`OBJ_EVENT_GFX_NURSE` num salão de 11 objetos**, e a fonte (`pokeplatinum`,
`res/field/events/events_contest_hall_lobby.json`) tem **3**, que lá são as
recepcionistas do concurso.

São duas causas somadas, e as duas são de raiz:

1. **O de-para não olhava o mapa.** `OBJ_EVENT_GFX_POKECENTER_NURSE` não quer
   dizer "enfermeira" no Platinum: quer dizer ATENDENTE DE BALCÃO com aquele
   uniforme. Em Pokécenter ela é a enfermeira mesmo; no lobby do Contest Hall
   ela é a RECEPCIONISTA do concurso. Medido nos 499 mapas de Sinnoh casados
   com a fonte: dos **21 objetos** com esse gráfico, **18 estão num
   `events_*_pokecenter_1f`** e **3 estão em `events_contest_hall_lobby`**. O
   conserto de raiz mora em `valida_mapas_sinnoh.TROCA_SPRITE_POR_BALCAO`, e
   este arquivo só reaplica a decisão em quem já foi escrito.

2. **Planta emprestada plantou a mesma pessoa duas vezes.** 197 mapas de Sinnoh
   nasceram com a planta REAPROVEITADA de outro mapa do repo
   (`fecha_portas_sinnoh.py` grava isso no próprio `map.json`), e nesses mapas a
   coordenada da fonte não é testemunha: a mesma pessoa cai em (8,4) numa
   passada do importador e em (2,2) na seguinte, então a guarda por vizinhança
   de 1 tile não reconhece as duas como a mesma e o corpo entra de novo, mudo.
   Medido nesta ferramenta, contra a árvore de `7b9a11ce64`: **38 corpos mudos
   importados acima do que a fonte pede, em 27 interiores fora de Pokécenter**,
   e 5 deles são justamente o salão que o Gui viu. Os Pokécenters não aparecem
   na conta porque a frente deles já limpou os 25 que tinham.

O QUE ESTE ARQUIVO NÃO FAZ, E POR QUÊ
-------------------------------------
- **Não escreve `map.json` de Pokécenter.** As enfermeiras repetidas dos
  Pokécenters de Sinnoh são de outro executor nesta mesma rodada, e a lista
  `POKECENTERS` abaixo é trava de escrita, não régua de medição.
- **Não apaga objeto com script, com flag ou com `local_id`.** A save guarda
  ÍNDICE de objeto, e `local_id` sem nome é a posição mais um. Por isso o corte
  sai sempre do FIM da lista: todo objeto que sobrevive fica com o índice que já
  tinha, e nenhum `addobject N` de cena passa a mirar outra pessoa.
- **Não devolve fala a NPC mudo.** As 94 falas órfãs de Sinnoh
  (`*_EventScript_NpcN` sem objeto que aponte para elas, em 45 mapas) são a
  outra metade do mesmo estrago e precisam do índice de script da fonte, que é
  assunto de `texto_sinnoh.py`, não deste de-para.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import valida_mapas_sinnoh as V  # noqa: E402
import importa_npcs_sinnoh as I  # noqa: E402

APLICAR = "--aplicar" in sys.argv

# Trava de ESCRITA: Pokécenter de Sinnoh é de outro executor nesta rodada.
# Continua entrando na medição, e é por isso que a lista não vive dentro da
# função que lista os mapas.
POKECENTERS = tuple(sorted(
    m for m in I.nossos_mapas_sinnoh()
    if re.search(r"poke(mon)?_?center", m, re.I)))


def e_balcao_de_enfermeira(mapa, arq_ev, obj=None):
    """O balcão deste mapa é o de um Pokécenter? Três testemunhas, nesta ordem.

    Nenhuma delas é o nome da nossa pasta, que é justamente o que envelhece
    calado: `CelesticTownPokecenter1F` e `FightAreaPokecenter1F` não são heal
    location nenhuma, e mesmo assim têm enfermeira.
    """
    # 1. A FONTE. O arquivo de eventos do Platinum diz o que a sala é.
    if arq_ev and "pokecenter" in arq_ev:
        return True
    # 2. O MOTOR. Mapa para onde uma heal location manda o jogador renascer tem
    #    enfermeira por definição, senão ninguém o cura.
    if mapa in respawns():
        return True
    # 3. O SCRIPT. Objeto cujo rótulo se apresenta como enfermeira é enfermeira,
    #    e essa é a régua da rodada 10 ("o de-para por nome olha o script").
    if obj is not None and re.search(r"nurse|enfermeir", str(obj.get("script", "")), re.I):
        return True
    return False


_RESP = None


def respawns():
    """Mapas de Sinnoh que são `respawn_map` de alguma heal location."""
    global _RESP
    if _RESP is None:
        heal = json.load(open(os.path.join(REPO, "src/data/heal_locations.json")))
        alvo = {h.get("respawn_map") for h in heal["heal_locations"]}
        _RESP = set()
        for m in I.nossos_mapas_sinnoh():
            d = json.load(open(os.path.join(REPO, "data/maps", m, "map.json")))
            if d.get("id") in alvo:
                _RESP.add(m)
    return _RESP


def casamento():
    """{nosso mapa: arquivo de eventos do Platinum}, a mesma régua do importador."""
    heads = I.headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(I.chave(h), (h, ev, mx))
    par = {}
    for m in I.nossos_mapas_sinnoh():
        h = I.APELIDOS.get(m)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(I.chave(m))
        if alvo:
            par[m] = alvo[1]
    return par


def esperado(gfx, pokecenter, sprites, especies):
    """O que ESTE gráfico da fonte vira aqui, ou None quando não vira gente."""
    classe = gfx.replace("OBJ_EVENT_GFX_", "")
    if classe in especies:
        return f"OBJ_EVENT_GFX_SPECIES({classe})"
    if gfx in I.DE_PARA_SINNOH:
        return I.DE_PARA_SINNOH[gfx]
    if any(t in classe for t in I.GRAFICOS_PROIBIDOS):
        return None
    if any(t in classe for t in I.GRAFICOS_PLACA):
        return None
    if any(t in classe for t in I.NOMES_PROPRIOS):
        return None
    if gfx in sprites:
        return gfx
    return V.troca_de_sprite(gfx, pokecenter) or V.SPRITE_PADRAO


def podavel(o):
    """Corpo que o corte pode tirar: importado, mudo, sem flag e sem nome."""
    return (o.get("origem") == "pokeplatinum"
            and str(o.get("script", "0")) in ("0", "")
            and str(o.get("flag", "0")) in ("0", "")
            and not o.get("local_id"))


def planeja(mapa, d, arq_ev, sprites, especies):
    """(repinturas, cortes) para um mapa, sem gravar nada.

    `repinturas` é [(indice, de, para)]; `cortes` é a lista de índices, sempre
    os MAIORES de cada excesso, para que o índice de quem fica não ande.
    """
    objs = d.get("object_events") or []
    repinturas = []
    for i, o in enumerate(objs):
        g = o.get("graphics_id")
        certo = V.sprite_de_balcao(g, e_balcao_de_enfermeira(mapa, arq_ev, o))
        if certo and certo != g:
            repinturas.append((i, g, certo))

    cortes = []
    if "planta reaproveitada" in str(d.get("origem", "")) and arq_ev:
        pe = os.path.join(I.PLAT, "res/field/events", arq_ev + ".json")
        if os.path.exists(pe):
            pc = e_balcao_de_enfermeira(mapa, arq_ev)
            quer = {}
            for e in json.load(open(pe)).get("object_events", []):
                alvo = esperado(e.get("graphics_id", ""), pc, sprites, especies)
                if alvo:
                    quer[alvo] = quer.get(alvo, 0) + 1
            # a contagem é feita JÁ com a repintura aplicada, senão o corte
            # mediria a enfermeira contra a vaga da recepcionista
            depois = [dict(o) for o in objs]
            for i, _de, para in repinturas:
                depois[i]["graphics_id"] = para
            tem = {}
            for o in depois:
                tem[o.get("graphics_id")] = tem.get(o.get("graphics_id"), 0) + 1
            for g, n in sorted(tem.items()):
                sobra = n - quer.get(g, 0)
                if sobra <= 0:
                    continue
                candidatos = [i for i, o in enumerate(depois)
                              if o.get("graphics_id") == g and podavel(o)]
                cortes += candidatos[-min(sobra, len(candidatos)):]
    return repinturas, sorted(set(cortes))


def main():
    sprites = V.sprites_utilizaveis()
    V.confere_tabela_de_trocas(sprites)
    especies = I.especies()
    par = casamento()

    tot_rep = tot_cor = 0
    linhas = []
    for m in I.nossos_mapas_sinnoh():
        pm = os.path.join(REPO, "data/maps", m, "map.json")
        d = json.load(open(pm))
        rep, cor = planeja(m, d, par.get(m), sprites, especies)
        if m in POKECENTERS:
            if rep or cor:
                linhas.append((m, len(rep), len(cor),
                               "PULADO, nao gravado: Pokecenter e de outro executor"))
            continue
        if not rep and not cor:
            continue
        detalhe = []
        for _i, de, para in rep:
            detalhe.append(de.replace("OBJ_EVENT_GFX_", "")
                           + " -> " + para.replace("OBJ_EVENT_GFX_", ""))
        for i in cor:
            detalhe.append("corta "
                           + str(d["object_events"][i].get("graphics_id", ""))
                           .replace("OBJ_EVENT_GFX_", ""))
        linhas.append((m, len(rep), len(cor), "; ".join(sorted(set(detalhe)))))
        tot_rep += len(rep)
        tot_cor += len(cor)
        if APLICAR:
            for i, _de, para in rep:
                d["object_events"][i]["graphics_id"] = para
            d["object_events"] = [o for i, o in enumerate(d["object_events"])
                                  if i not in set(cor)]
            json.dump(d, open(pm, "w"), indent=2, ensure_ascii=False)

    print(f"{'mapa':36s} {'rep':>3s} {'cor':>3s}  o que muda")
    for m, r, c, det in linhas:
        print(f"{m:36s} {r:3d} {c:3d}  {det[:110]}")
    print(f"\nmapas tocados: {len(linhas)}   repinturas: {tot_rep}   "
          f"cortes: {tot_cor}   ({'GRAVADO' if APLICAR else 'so relato'})")
    return 0


def demo():
    """Autoteste. Nada grava, e cada asserção mede o mecanismo, não a contagem."""
    sprites = V.sprites_utilizaveis()
    especies = I.especies()

    # 1. A tabela de contexto aponta para sprite que esta build DESENHA. Sem
    #    isto, o conserto plantaria o crash de sprite fantasma da lição de 04/08.
    for balcao, outro in V.TROCA_SPRITE_POR_BALCAO.values():
        assert balcao in sprites, balcao
        assert outro in sprites, outro

    # 2. O mesmo gráfico da fonte dá pessoas DIFERENTES conforme o balcão.
    n = "OBJ_EVENT_GFX_POKECENTER_NURSE"
    assert V.troca_de_sprite(n, True) == "OBJ_EVENT_GFX_NURSE"
    assert V.troca_de_sprite(n, False) == "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST"
    # e o de-para SEM contexto continua respondendo o de sempre, porque
    # corpos_repetidos_pokecenter.py cobra esta chave.
    assert V.TROCA_SPRITE[n] == "OBJ_EVENT_GFX_NURSE"

    # 2b. O SENTIDO ÚNICO, e ele é medido contra a tabela, não afirmado: o lado
    #     de Pokécenter do par tem que ser destino de UM só gráfico da fonte
    #     (senão desfazê-lo seria chute), e o outro lado tem que ser destino de
    #     VÁRIOS (é por isso que ele nunca volta atrás).
    for balcao, outro in V.TROCA_SPRITE_POR_BALCAO.values():
        origens_b = [k for k, v in V.TROCA_SPRITE.items() if v == balcao]
        origens_o = [k for k, v in V.TROCA_SPRITE.items() if v == outro]
        assert origens_b == [n], origens_b
        assert len(origens_o) >= 2, origens_o
    assert V.sprite_de_balcao("OBJ_EVENT_GFX_NURSE", False) == \
        "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST"
    assert V.sprite_de_balcao("OBJ_EVENT_GFX_NURSE", True) is None
    assert V.sprite_de_balcao("OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST", True) is None
    assert V.sprite_de_balcao("OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST", False) is None

    # 3. As três testemunhas do balcão, cada uma num caso que só ela resolve.
    assert e_balcao_de_enfermeira("QualquerCoisa",
                                  "events_celestic_town_pokecenter_1f")
    assert "SandgemTown_PokemonCenter_1F" in respawns()
    assert e_balcao_de_enfermeira("SinnohLeague_Entrance", None,
                                  {"script": "SinnohLeague_Entrance_EventScript_Nurse"})
    assert not e_balcao_de_enfermeira("ContestHallLobby",
                                      "events_contest_hall_lobby")

    # 4. A FONTE, lida do disco: o Contest Hall tem TRÊS atendentes de balcão, e
    #    é contra este número que o corte mede.
    pe = os.path.join(I.PLAT, "res/field/events/events_contest_hall_lobby.json")
    fonte = json.load(open(pe)).get("object_events", [])
    assert sum(1 for e in fonte if e.get("graphics_id") == n) == 3, "a fonte mudou"

    # 5. MUTAÇÃO PLANTADA, em mapa de verdade e em memória: seis enfermeiras
    #    mudas num salão que a fonte quer com três atendentes têm que virar três
    #    recepcionistas, e as três que sobram têm que ser as ÚLTIMAS da lista.
    d = json.load(open(os.path.join(REPO, "data/maps/ContestHallLobby/map.json")))
    d["object_events"] = [
        {"graphics_id": "OBJ_EVENT_GFX_NURSE", "x": i, "y": 2, "script": "0",
         "flag": "0", "origem": "pokeplatinum"} for i in range(6)]
    rep, cor = planeja("ContestHallLobby", d, "events_contest_hall_lobby",
                       sprites, especies)
    assert len(rep) == 6, rep
    assert {p for _i, _g, p in rep} == {"OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST"}
    assert cor == [3, 4, 5], cor

    # 6. O par negativo: a MESMA lista num Pokécenter não é repintada nem
    #    cortada por gente demais, porque lá a enfermeira é a certa.
    d2 = json.load(open(os.path.join(
        REPO, "data/maps/SandgemTown_PokemonCenter_1F/map.json")))
    d2["object_events"] = [
        {"graphics_id": "OBJ_EVENT_GFX_NURSE", "x": 5, "y": 2, "script": "0",
         "flag": "0", "origem": "pokeplatinum"}]
    rep2, _cor2 = planeja("SandgemTown_PokemonCenter_1F", d2,
                          "events_sandgem_town_pokecenter_1f", sprites, especies)
    assert rep2 == [], rep2

    # 7. Corpo com script, com flag ou com nome NUNCA é podável, e é isso que
    #    segura o índice de objeto que a save guarda.
    assert podavel({"origem": "pokeplatinum", "script": "0", "flag": "0"})
    assert not podavel({"origem": "pokeplatinum", "script": "X_EventScript_Y",
                        "flag": "0"})
    assert not podavel({"origem": "pokeplatinum", "script": "0",
                        "flag": "FLAG_SINNOH_X"})
    assert not podavel({"origem": "pokeplatinum", "script": "0", "flag": "0",
                        "local_id": "LOCALID_X"})
    assert not podavel({"script": "0", "flag": "0"})

    # 8. IDEMPOTÊNCIA: o plano do mapa como ele está no disco, aplicado em
    #    memória, tem que dar plano VAZIO na segunda passada.
    d3 = json.load(open(os.path.join(REPO,
                                     "data/maps/ContestHallLobby/map.json")))
    r3, c3 = planeja("ContestHallLobby", d3, "events_contest_hall_lobby",
                     sprites, especies)
    for i, _g, p in r3:
        d3["object_events"][i]["graphics_id"] = p
    d3["object_events"] = [o for i, o in enumerate(d3["object_events"])
                           if i not in set(c3)]
    r4, c4 = planeja("ContestHallLobby", d3, "events_contest_hall_lobby",
                     sprites, especies)
    assert (r4, c4) == ([], []), (r4, c4)

    print("demo: 9 casos, todos verdes")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
