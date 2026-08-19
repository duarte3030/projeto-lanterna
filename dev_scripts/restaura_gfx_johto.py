#!/usr/bin/env python3
"""Devolve a Johto o `graphics_id` que a FONTE diz, em quem NÃO é gente.

O estrago tem autor conhecido, o mesmo do `restaura_npcs_johto.py`:
`dev_scripts/sanitize_johto_map_json.py` varre todo `map.json` de Johto e grava
`graphics_id = OBJ_EVENT_GFX_ITEM_BALL` em TODO `object_event`. O
`restaura_npcs_johto.py` devolveu quem era GENTE; sobrou o resto, e o resto é o
maior defeito visível do repo: o jogador anda por Johto e vê bola de item onde
a fonte tem efeito de luz, pedra de Rock Smash, canteiro de berry, árvore de
Cut, pedra empurrável e Pokémon de overworld.

MEDIDO em 19/08/2026, contra `fontes-mapas/hns`, nos 236 mapas de Johto: 1211
object events ainda são item ball MUDA (`flag: "0"`, `script: "0"`,
`trainer_sight_or_berry_tree_id: "0"`), e 1103 deles têm na fonte, na
COORDENADA EXATA, um objeto que não é bola e não é gente.

Divisão de trabalho, e ela é a lei desta ferramenta:

- **Gente é do outro gerador.** Objeto cuja fonte é pessoa (`eh_pessoa` do
  `restaura_npcs_johto`) sai no censo como recusado e NÃO é tocado aqui.
  Devolver o sprite de um NPC sem devolver a `FLAG_HIDE_*` que o esconde põe o
  personagem em campo para sempre, no estado errado da história, que é
  exatamente o erro que o outro gerador existe para não cometer.
- **Casamento por coordenada EXATA, nunca por raio.** É o critério de aceite
  escrito na fila (`johto:sprite_de_bola_em_quem_nao_e_bola`): casar
  `(mapa, x, y)` contra o objeto da fonte, nunca por escala nem por vizinhança.
- **Um objeto da fonte vale por UM objeto nosso.** Objeto nosso que já deixou
  de ser item ball (restaurado por qualquer rodada anterior) reserva o par
  dele antes do laço (`semeia`), senão a segunda rodada casaria de novo com o
  mesmo objeto da fonte e o N:1 voltaria sozinho.
- **Sem equivalente, sem invenção.** Gráfico da fonte que esta build não
  desenha vira o equivalente DOCUMENTADO (tabela `SPRITE` do
  `restaura_npcs_johto`, a mesma dos outros importadores) ou é recusado com
  motivo no censo. Objeto que a fonte não tem em lugar nenhum vira linha de
  censo e NÃO some: apagar objeto é conteúdo, e conteúdo não é decisão de
  ferramenta.

Traduções medidas nesta build, com a prova de cada uma:

- `OBJ_EVENT_GFX_MON_BASE+SPECIES_X` -> `OBJ_EVENT_GFX_SPECIES(X)`, que é a
  forma que ESTE repo já usa (`data/maps/LakeOfRage/map.json` e mais 5). Custo
  de ROM ZERO: `OW_POKEMON_OBJECT_EVENTS` é TRUE, então `gSpeciesInfo[].
  overworldData` já está ligado na ROM com ou sem estes mapas. Só entra espécie
  que tem `OVERWORLD(...)` de verdade no `species_info`; sem isso o objeto é
  recusado em vez de cair no boneco de substituição do motor.
- `OBJ_EVENT_GFX_LIGHT_SPRITE` existe aqui e é tratado pelo motor ANTES de
  virar object event (`TrySpawnObjectEvents`, `event_object_movement.c`): ele
  vira sprite de luz, não bloqueia tile nenhum e só aparece de noite
  (`gTimeOfDay != TIME_NIGHT` esconde). O campo `trainer_sight_or_berry_tree_id`
  é o TIPO de luz; a fonte usa 0, 3 e 4 e aqui só existem 0..2
  (`gFieldEffectLightTemplates`), então o campo fica em 0 = `LIGHT_TYPE_BALL`,
  a luz genérica. Não é invenção: é o único tipo que a fonte pede e que existe.
- Redemoinho: a fonte desenha a âncora INVISÍVEL
  (`movement_type: MOVEMENT_TYPE_INVISIBLE`) e usa `OBJ_EVENT_GFX_WHIRLPOOL`,
  que esta build não tem. Mesmo remédio já aprovado no `restaura_npcs_johto`:
  esconder no lugar, um campo só, gráfico e índice intactos.

Colisão, medido e não presumido: object event bloqueia o tile em que está
independentemente do `graphics_id` (`CheckForObjectEventCollision` olha
posição, nunca sprite). Trocar gráfico não fecha passagem nenhuma. A ÚNICA
mudança de passagem desta ferramenta é na direção permissiva: os 219 que viram
`LIGHT_SPRITE` deixam de virar object event, então o tile deles ABRE.

Uso:
    python3 dev_scripts/restaura_gfx_johto.py            # só censo
    python3 dev_scripts/restaura_gfx_johto.py --aplica   # escreve
    python3 dev_scripts/restaura_gfx_johto.py --demo     # autoteste
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import restaura_npcs_johto as RN  # noqa: E402  eh_pessoa, SPRITE, mapas_de_johto
import valida_mapas_sinnoh as VM  # noqa: E402  sprites_utilizaveis

HNS = RN.HNS
APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv

CENSO = os.path.join(REPO, "dev_scripts", "gfx_johto.json")

BOLAS = ("OBJ_EVENT_GFX_ITEM_BALL", "OBJ_EVENT_GFX_POKE_BALL")
MUDO = "OBJ_EVENT_GFX_ITEM_BALL"
MON_PREFIXO = "OBJ_EVENT_GFX_MON_BASE+"
LUZ = "OBJ_EVENT_GFX_LIGHT_SPRITE"
MOV_ESCONDIDO = RN.MOV_ESCONDIDO


def eh_mudo(obj):
    """Item ball que o sanitize deixou: sem flag, sem script, sem índice.

    Já ESCONDIDO não conta: a âncora de redemoinho guarda o gráfico de bola de
    propósito e o que muda nela é o movimento, então sem esta linha a segunda
    rodada acharia as 42 de novo e o relatório mentiria (o `--aplica` seria
    inócuo, mas o número não).
    """
    return (obj.get("graphics_id") == MUDO
            and obj.get("movement_type") != MOV_ESCONDIDO
            and str(obj.get("flag", "0")) == "0"
            and str(obj.get("script", "0")) == "0"
            and str(obj.get("trainer_sight_or_berry_tree_id", "0")) == "0")


def eh_redemoinho(gfx, script):
    """Âncora de redemoinho: decoração de campo, não gente e não bola."""
    return (gfx == "OBJ_EVENT_GFX_WHIRLPOOL"
            or script in RN.SCRIPTS_NAO_PESSOA)


def especies_com_overworld():
    """Espécies que têm sprite de overworld DE VERDADE no `species_info`.

    Lido do bloco `[SPECIES_X] = {...}` de cada arquivo: só conta quem chama a
    macro `OVERWORLD(...)`. O motor tem rede (`OW_SUBSTITUTE_PLACEHOLDER`), mas
    cair nela é trocar bola por boneco de substituição, e isso é invenção.
    """
    tem = set()
    base = os.path.join(REPO, "src/data/pokemon/species_info")
    for nome in sorted(os.listdir(base)):
        if not nome.endswith(".h"):
            continue
        with open(os.path.join(base, nome), encoding="utf-8",
                  errors="replace") as f:
            txt = f.read()
        partes = re.split(r"\n\s*\[(SPECIES_[A-Z0-9_]+)\]\s*=", txt)
        for i in range(1, len(partes), 2):
            if re.search(r"\bOVERWORLD\(", partes[i + 1]):
                tem.add(partes[i])
    return tem


def traduz(gfx, utilizaveis, especies):
    """(gfx_novo, motivo_da_recusa). Exatamente um dos dois é None."""
    if gfx.startswith(MON_PREFIXO):
        sp = gfx[len(MON_PREFIXO):]
        if sp not in especies:
            return None, f"espécie sem sprite de overworld nesta build ({sp})"
        return f"OBJ_EVENT_GFX_SPECIES({sp[len('SPECIES_'):]})", None
    if gfx in utilizaveis:
        return gfx, None
    equivalente = RN.SPRITE.get(gfx)
    if equivalente and equivalente in utilizaveis:
        return equivalente, None
    return None, f"sem equivalente desenhado nesta build ({gfx})"


def semeia(nossos, na_coord, utilizaveis, especies):
    """Objetos da fonte que rodadas ANTERIORES já gastaram, por coordenada.

    Idempotência: objeto nosso que já não é item ball muda casa com o objeto da
    fonte cuja tradução dá o gráfico dele. Sem isto, a segunda rodada acharia o
    mesmo candidato livre e restauraria em dobro.
    """
    gastos = set()
    for o in nossos:
        if eh_mudo(o):
            continue
        meu = o.get("graphics_id")
        for c in na_coord.get((o["x"], o["y"]), []):
            if id(c) in gastos:
                continue
            g = c.get("graphics_id", "")
            novo, _ = traduz(g, utilizaveis, especies)
            # o escondido guarda o gráfico de bola, então casa pelo movimento
            escondido = (o.get("movement_type") == MOV_ESCONDIDO
                         and meu == MUDO
                         and eh_redemoinho(g, c.get("script")))
            if novo == meu or escondido:
                gastos.add(id(c))
                break
    return gastos


def monta():
    utilizaveis = VM.sprites_utilizaveis()
    especies = especies_com_overworld()
    plano = {}          # mapa -> dados do map.json já alterados
    censo = []          # linha a linha, entrou ou não
    contagem = Counter()
    for mapa in sorted(RN.mapas_de_johto()):
        p = os.path.join(REPO, "data/maps", mapa, "map.json")
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            dados = json.load(f)
        fp = os.path.join(HNS, "data/maps", mapa, "map.json")
        na_coord = defaultdict(list)
        if os.path.exists(fp):
            with open(fp, encoding="utf-8") as f:
                for o in json.load(f).get("object_events", []):
                    na_coord[(o["x"], o["y"])].append(o)

        nossos = dados.get("object_events", [])
        gastos = semeia(nossos, na_coord, utilizaveis, especies)
        mudou = False
        for obj in nossos:
            if not eh_mudo(obj):
                continue
            linha = {"mapa": mapa, "x": obj["x"], "y": obj["y"],
                     "gfx_velho": MUDO}
            cands = [c for c in na_coord.get((obj["x"], obj["y"]), [])
                     if id(c) not in gastos]
            if not cands:
                linha["motivo"] = ("sem objeto livre da fonte nesta "
                                   "coordenada exata")
                censo.append(linha)
                contagem[linha["motivo"]] += 1
                continue
            fonte = cands[0]
            gfx = fonte.get("graphics_id", "")
            script = fonte.get("script")
            linha["gfx_fonte"] = gfx
            if gfx in BOLAS:
                linha["motivo"] = "a fonte diz BOLA aqui, já está certo"
            elif eh_redemoinho(gfx, script):
                gastos.add(id(fonte))
                obj["movement_type"] = MOV_ESCONDIDO
                linha["gfx_novo"] = MUDO
                linha["escondido"] = True
                mudou = True
            elif RN.eh_pessoa(gfx, script):
                linha["motivo"] = ("é GENTE na fonte; sprite de NPC é do "
                                   "restaura_npcs_johto.py, que precisa da "
                                   "flag junto")
            else:
                novo, recusa = traduz(gfx, utilizaveis, especies)
                if recusa:
                    linha["motivo"] = recusa
                else:
                    gastos.add(id(fonte))
                    obj["graphics_id"] = novo
                    linha["gfx_novo"] = novo
                    mudou = True
            censo.append(linha)
            contagem[linha.get("motivo") or linha["gfx_novo"]] += 1
        if mudou:
            plano[mapa] = dados
    return plano, censo, contagem


def grava_como_estava(p, dados):
    """Reescreve o `map.json` no MESMO formato que ele já tinha.

    Medido em 19/08/2026: dos 236 mapas de Johto, 201 usam indentação 2 e 35
    usam 4, e todos terminam em newline. `json.dump(..., indent=2)` cru
    reformataria 236 arquivos para trocar 1171 campos, e diff de reformatação
    esconde o conserto de verdade na hora de revisar.
    """
    with open(p, encoding="utf-8") as f:
        original = f.read()
    corpo = original.split("\n", 1)[1] if "\n" in original else ""
    recuo = len(corpo) - len(corpo.lstrip(" ")) if corpo.startswith(" ") else 2
    texto = json.dumps(dados, indent=recuo)
    if original.endswith("\n"):
        texto += "\n"
    with open(p, "w", encoding="utf-8") as f:
        f.write(texto)


def escreve(plano, censo):
    for mapa, dados in plano.items():
        grava_como_estava(os.path.join(REPO, "data/maps", mapa, "map.json"),
                          dados)
    entrou = [l for l in censo if "gfx_novo" in l]
    fora = [l for l in censo if "gfx_novo" not in l]
    with open(CENSO, "w", encoding="utf-8") as f:
        json.dump({"dentro": entrou, "fora": fora}, f,
                  ensure_ascii=False, indent=1)


def demo():
    """Autoteste: as regras que decidem, e uma mutação plantada de verdade."""
    utilizaveis = VM.sprites_utilizaveis()
    especies = especies_com_overworld()

    # o filtro do mudo: só pega o que o sanitize deixou, nunca bola ligada
    assert eh_mudo({"graphics_id": MUDO, "flag": "0", "script": "0",
                    "trainer_sight_or_berry_tree_id": "0"})
    assert not eh_mudo({"graphics_id": MUDO, "flag": "FLAG_ITEM_X",
                        "script": "Common_EventScript_FindItem",
                        "trainer_sight_or_berry_tree_id": "0"})
    assert not eh_mudo({"graphics_id": "OBJ_EVENT_GFX_BERRY_TREE",
                        "flag": "0", "script": "0",
                        "trainer_sight_or_berry_tree_id": "0"})

    # tradução: Pokémon de overworld pela forma que este repo já usa
    assert traduz("OBJ_EVENT_GFX_MON_BASE+SPECIES_GOLBAT",
                  utilizaveis, especies)[0] == "OBJ_EVENT_GFX_SPECIES(GOLBAT)"
    # espécie sem sprite de overworld é RECUSA, não boneco de substituição
    assert "SPECIES_UNOWN" not in especies
    novo, motivo = traduz("OBJ_EVENT_GFX_MON_BASE+SPECIES_UNOWN",
                          utilizaveis, especies)
    assert novo is None and "overworld" in motivo
    # gráfico que existe aqui passa direto
    assert traduz(LUZ, utilizaveis, especies)[0] == LUZ
    assert traduz("OBJ_EVENT_GFX_BREAKABLE_ROCK",
                  utilizaveis, especies)[0] == "OBJ_EVENT_GFX_BREAKABLE_ROCK"
    # equivalente DOCUMENTADO, o mesmo dos outros importadores
    assert traduz("OBJ_EVENT_GFX_SUPER_NERD",
                  utilizaveis, especies)[0] == "OBJ_EVENT_GFX_SCIENTIST_1"
    # sem equivalente: recusa com motivo, nunca chute
    assert traduz("OBJ_EVENT_GFX_WHIRLPOOL", utilizaveis, especies)[0] is None

    # redemoinho: gráfico da fonte OU script da fonte
    assert eh_redemoinho("OBJ_EVENT_GFX_WHIRLPOOL", None)
    assert eh_redemoinho("OBJ_EVENT_GFX_ARCHER", "EventScript_Whirlpool")
    assert not eh_redemoinho("OBJ_EVENT_GFX_ARCHER", "EventScript_Archer")

    # gente continua sendo do outro gerador
    assert RN.eh_pessoa("OBJ_EVENT_GFX_CLAIR")
    assert not RN.eh_pessoa("OBJ_EVENT_GFX_BREAKABLE_ROCK")

    # ---- mutação plantada: um mapa de verdade, restaurado e depois relido
    plano, censo, _ = monta()
    entrou = [l for l in censo if "gfx_novo" in l]
    # nenhuma linha que entrou pode ter virado item ball muda de novo
    for l in entrou:
        assert l["gfx_novo"] != MUDO or l.get("escondido")
    # Alvo da mutação: uma linha que ESTA rodada restauraria ou, com a árvore
    # já aplicada (o estado normal depois do --aplica), uma linha do censo
    # gravado. Sem isto o autoteste deixaria de provar qualquer coisa
    # exatamente depois de o conserto entrar, que é quando ele mais importa.
    if entrou:
        alvo_linha = entrou[0]
    else:
        with open(CENSO, encoding="utf-8") as f:
            alvo_linha = json.load(f)["dentro"][0]
    alvo = alvo_linha["mapa"]
    esperado = alvo_linha["gfx_novo"]
    p = os.path.join(REPO, "data/maps", alvo, "map.json")
    with open(p, encoding="utf-8") as f:
        original = f.read()
    try:
        if entrou:
            grava_como_estava(p, plano[alvo])
        _, censo2, _ = monta()
        restou = [l for l in censo2 if l["mapa"] == alvo and "gfx_novo" in l]
        assert not restou, (f"não é idempotente: {alvo} ainda tem "
                            f"{len(restou)} para restaurar na segunda rodada")
        # a mutação plantada: desfaz UM objeto para item ball muda e a rodada
        # seguinte tem que achar exatamente ele, com o mesmo gráfico de antes
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        for o in d["object_events"]:
            if (o["x"], o["y"]) == (alvo_linha["x"], alvo_linha["y"]):
                o["graphics_id"] = MUDO
                o["movement_type"] = "MOVEMENT_TYPE_LOOK_AROUND"
                break
        else:
            raise AssertionError("mutação não encontrou a coordenada")
        grava_como_estava(p, d)
        _, censo3, _ = monta()
        achou = [l for l in censo3 if l["mapa"] == alvo
                 and (l["x"], l["y"]) == (alvo_linha["x"], alvo_linha["y"])
                 and "gfx_novo" in l]
        assert len(achou) == 1, f"a mutação plantada não voltou: {achou}"
        assert achou[0]["gfx_novo"] == esperado, (achou[0]["gfx_novo"],
                                                  esperado)
    finally:
        with open(p, "w", encoding="utf-8") as f:
            f.write(original)
    print(f"demo OK ({len(entrou)} restauráveis agora, mutação plantada em "
          f"{alvo} ({alvo_linha['x']},{alvo_linha['y']}) voltou como "
          f"{esperado})")


def main():
    plano, censo, contagem = monta()
    entrou = [l for l in censo if "gfx_novo" in l]
    fora = [l for l in censo if "gfx_novo" not in l]
    print(f"item ball muda em Johto: {len(censo)}   "
          f"restaurável: {len(entrou)}   recusado: {len(fora)}   "
          f"mapas tocados: {len(plano)}")
    print("\ncontagem:")
    for k, v in contagem.most_common():
        print(f"  {v:5}  {k}")
    print("\namostra do censo (10 primeiras que entram):")
    for l in entrou[:10]:
        print(f"  {l['mapa']} ({l['x']},{l['y']}) {l['gfx_velho']} -> "
              f"{l['gfx_novo']}  [fonte: {l.get('gfx_fonte')}]")
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0
    escreve(plano, censo)
    print(f"\nescrito: {len(entrou)} objetos em {len(plano)} mapas; "
          f"censo em {os.path.relpath(CENSO, REPO)}")
    return 0


if __name__ == "__main__":
    if DEMO:
        demo()
    else:
        sys.exit(main())
