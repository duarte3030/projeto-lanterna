#!/usr/bin/env python3
"""Devolve a Johto os objetos que a importação NÃO TROUXE, no estado do sanitize.

Irmão mais novo do `restaura_npcs_johto.py` e do `restaura_gfx_johto.py`, e a
divisão de trabalho é a razão de ele existir:

- `restaura_npcs_johto.py` devolve IDENTIDADE (sprite, fala, flag) a objeto que
  ESTÁ no `map.json` e virou item ball muda.
- `restaura_gfx_johto.py` devolve GRÁFICO a quem não é gente, no mesmo caso.
- **este** devolve o OBJETO em si, quando ele nunca chegou a existir aqui.

MEDIDO em 22/08/2026, contra `fontes-mapas/hns`, com a mesma régua do
`dev_scripts/completude.py`: os 236 mapas de Johto têm 2.282 object events e a
fonte tem 2.374 nos mesmos mapas (96,1%). O buraco não é de identidade, é de
CONTAGEM: 111 objetos da fonte não têm nenhum objeto nosso na coordenada deles.
Por família, medido e não estimado: 73 Pokémon de overworld
(`OBJ_EVENT_GFX_MON_BASE+SPECIES_X` e `SLOWPOKE_NO_TAIL`), 36 de gente, 5 bolas
e 4 efeitos de luz.

O QUE ESTE GERADOR ESCREVE, E POR QUE É TÃO POUCO

Ele grava o objeto no ESTADO EXATO em que o `sanitize_johto_map_json.py` deixou
todos os outros: `OBJ_EVENT_GFX_ITEM_BALL`, `script: "0"`, `flag: "0"`,
`trainer_sight_or_berry_tree_id: "0"`, `MOVEMENT_TYPE_LOOK_AROUND`, na
coordenada e na elevação da fonte. Nada de sprite, nada de fala, nada de flag.

Isso é de propósito, e é a decisão de desenho desta ferramenta: as duas
ferramentas que já existem sabem fazer o resto, com regras já auditadas
(equivalente de sprite documentado, recusa de flag que não existe, fecho
transitivo de fala, espécie só com `OVERWORLD(...)` de verdade). Reimplementar
isso aqui seria um terceiro conjunto de regras para divergir do primeiro no meio
de um mapa. A ordem de uso é, portanto:

    python3 dev_scripts/completa_objetos_johto.py --aplica
    python3 dev_scripts/restaura_gfx_johto.py --aplica
    python3 dev_scripts/restaura_npcs_johto.py --aplica
    python3 dev_scripts/completa_objetos_johto.py --limpa --aplica

O `--limpa` é a limpeza obrigatória do fim: objeto que os dois geradores
recusaram continua bola muda, e bola muda que o jogador vê e não pega é mentira
visível. `--limpa` TIRA do mapa só os que ESTE gerador criou (marcados em
`dev_scripts/objetos_johto.json`), nunca os herdados, e grava o motivo no censo
para que a rodada seguinte não os reponha. Esconder não serve: ver `limpa()`.

AS DUAS RECUSAS, AMBAS MEDIDAS

1. **Tile de warp** (2 casos): o objeto trancaria o warp para sempre. Ver
   `julga()`, que traz o caso real do policial da Torre Rádio.
2. **Sem identidade possível** (18 casos, e a lista está no censo): o
   `--limpa` já provou que nem o gerador de gráfico nem o de NPC conseguem
   dizer quem o objeto é, quase sempre porque a `FLAG_HIDE_*` de cena que a
   fonte usa não existe nesta build.

Colisão e coordenada fora do retângulo NÃO são recusa, e as duas custaram uma
medição cada: ver `julga()`. Dois objetos da fonte na MESMA coordenada entram os
dois, porque é o que a fonte tem (par dia/noite de Pokémon de overworld).
Empilhar dois objetos num tile é legal no motor; o que não é legal é inventar
um terceiro.

Compatibilidade de save: object event não mora na save. Os objetos entram no FIM
da lista de cada mapa, então nenhum índice existente se move e nenhum
`applymovement` de script antigo passa a apontar para outro boneco.

Uso:
    python3 dev_scripts/completa_objetos_johto.py            # só censo
    python3 dev_scripts/completa_objetos_johto.py --aplica   # escreve
    python3 dev_scripts/completa_objetos_johto.py --limpa --aplica  # tira a sobra
    python3 dev_scripts/completa_objetos_johto.py --demo     # autoteste
"""
import json
import os
import struct
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import restaura_npcs_johto as RN   # noqa: E402  mapas_de_johto, HNS
import restaura_gfx_johto as RG    # noqa: E402  grava_como_estava, eh_mudo

HNS = RN.HNS
APLICA = "--aplica" in sys.argv
LIMPA = "--limpa" in sys.argv
DEMO = "--demo" in sys.argv

CENSO = os.path.join(REPO, "dev_scripts", "objetos_johto.json")
MUDO = "OBJ_EVENT_GFX_ITEM_BALL"
MOV_PADRAO = "MOVEMENT_TYPE_LOOK_AROUND"
MOV_ESCONDIDO = RN.MOV_ESCONDIDO


def layouts(_cache={}):
    """`layouts.json` indexado por id, com o caminho do `map.bin`."""
    if not _cache:
        with open(os.path.join(REPO, "data/layouts/layouts.json"),
                  encoding="utf-8") as f:
            for L in json.load(f)["layouts"]:
                if L:
                    _cache[L["id"]] = L
    return _cache


def colisao(layout_id, x, y):
    """0 = andável, None = fora do retângulo ou layout ilegível."""
    L = layouts().get(layout_id)
    if not L:
        return None
    if not (0 <= x < L["width"] and 0 <= y < L["height"]):
        return None
    caminho = os.path.join(REPO, L["blockdata_filepath"])
    try:
        with open(caminho, "rb") as f:
            f.seek((y * L["width"] + x) * 2)
            dados = f.read(2)
    except OSError:
        return None
    if len(dados) < 2:
        return None
    return (struct.unpack("<H", dados)[0] >> 10) & 0x3


def julga(dados, fonte_obj):
    """(True, nota) se o objeto pode entrar; (False, motivo) se não.

    UMA recusa só, e ela é a única MEDIDA como estrago: objeto em cima de warp.
    O caso real é o policial de `GoldenrodCity_RadioTower_2F (10,5)`, que na
    fonte está em cima da escada para o 3F de propósito (é o bloqueio do arco
    da Rocket) e que aqui trancaria os andares 3F a 5F para sempre, porque a
    flag que o tira de lá não existe nesta build. Warp trancado não aparece
    como erro de compilação: aparece como andar inalcançável.

    O que NÃO é recusa, e cada uma custou uma medição:

    - **Tile não andável.** A fonte é um hack de gen 3 JOGÁVEL e os 236
      `map.bin` de Johto são byte a byte os dela (conferido por md5 em
      22/08/2026 em 6 layouts, entre eles AzaleaTown e SproutTower_3F).
      Objeto em tile de colisão 1 APARECE: é o Pokémon em cima da árvore, do
      rochedo, da água. Recusar por colisão jogava fora 25 objetos que a fonte
      desenha na tela.
    - **Coordenada fora do retângulo.** São 37, e a maior parte é objeto
      ESTACIONADO em coordenada negativa (os 14 do `NationalPark_BugContest`,
      o Jake e a Joyce da `Route26`), truque que a fonte usa para guardar
      objeto que só uma cena traz para dentro. O motor aceita: dez `map.json`
      deste repo já têm `x` negativo desde antes desta rodada e a ROM compila
      e roda. Recusar aqui seria apagar conteúdo da fonte por preciosismo.
    """
    x, y = fonte_obj["x"], fonte_obj["y"]
    for w in dados.get("warp_events", []):
        if (w["x"], w["y"]) == (x, y):
            return False, "tile de warp (trancaria o warp para sempre)"
    c = colisao(dados.get("layout", ""), x, y)
    if c is None:
        return True, "fora do retângulo do layout (objeto estacionado)"
    if c != 0:
        return True, f"tile de colisão {c} (decoração em cima de cenário)"
    return True, None


def novo_objeto(fonte_obj):
    """O objeto no estado do sanitize: existe, e não diz nada ainda."""
    return {
        "graphics_id": MUDO,
        "x": fonte_obj["x"],
        "y": fonte_obj["y"],
        "elevation": fonte_obj.get("elevation", 0),
        "movement_type": MOV_PADRAO,
        "movement_range_x": 0,
        "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": "0",
        "flag": "0",
    }


def sobrando(nossos, fonte):
    """Objetos da FONTE sem par nosso, casando 1:1 pela coordenada exata."""
    livres = Counter((o["x"], o["y"]) for o in nossos)
    fora = []
    for o in fonte:
        p = (o["x"], o["y"])
        if livres[p] > 0:
            livres[p] -= 1
        else:
            fora.append(o)
    return fora


def monta():
    plano, censo, contagem = {}, [], Counter()
    for mapa in sorted(RN.mapas_de_johto()):
        p = os.path.join(REPO, "data/maps", mapa, "map.json")
        fp = os.path.join(HNS, "data/maps", mapa, "map.json")
        if not (os.path.exists(p) and os.path.exists(fp)):
            continue
        with open(p, encoding="utf-8") as f:
            dados = json.load(f)
        with open(fp, encoding="utf-8") as f:
            fonte = json.load(f).get("object_events", [])
        nossos = dados.get("object_events", [])
        novos = []
        veto = vetados()
        for o in sobrando(nossos, fonte):
            linha = {"mapa": mapa, "x": o["x"], "y": o["y"],
                     "gfx_fonte": o.get("graphics_id", "")}
            if (mapa, o["x"], o["y"]) in veto:
                linha["motivo"] = SEM_IDENTIDADE
                contagem["RECUSADO: " + SEM_IDENTIDADE] += 1
                censo.append(linha)
                continue
            ok, nota = julga(dados, o)
            if not ok:
                linha["motivo"] = nota
                contagem["RECUSADO: " + nota] += 1
            else:
                novos.append(novo_objeto(o))
                linha["entrou"] = True
                if nota:
                    linha["nota"] = nota
                contagem[nota or "entrou, tile normal"] += 1
            censo.append(linha)
        if novos:
            dados["object_events"] = nossos + novos
            plano[mapa] = dados
    return plano, censo, contagem


SEM_IDENTIDADE = ("nenhum dos dois geradores deu identidade: continuaria bola "
                  "muda na tela")


def le_censo():
    if not os.path.exists(CENSO):
        return {"dentro": [], "fora": []}
    with open(CENSO, encoding="utf-8") as f:
        return json.load(f)


def vetados():
    """(mapa,x,y) que uma rodada de `--limpa` já provou não ter identidade.

    É o que torna o encadeamento IDEMPOTENTE: sem esta lista, o `--aplica`
    seguinte reporia exatamente os objetos que o `--limpa` acabou de tirar, e
    os dois ficariam se desfazendo em loop.
    """
    return {(l["mapa"], l["x"], l["y"]) for l in le_censo().get("fora", [])
            if l.get("motivo") == SEM_IDENTIDADE}


def limpa():
    """Tira do mapa o que ESTE gerador criou e que continuou bola muda.

    ESCONDER NÃO SERVE, e isto foi MEDIDO em 22/08/2026 em vez de suposto:
    `MOVEMENT_TYPE_INVISIBLE` só faz `objectEvent->invisible = TRUE`
    (`src/event_object_movement.c:1869`); o objeto continua existindo e
    CONTINUA BLOQUEANDO O TILE. Esconder as quatro bolas do `SlowpokeWell_B1F`
    seria trocar quatro pokébolas falsas por quatro paredes invisíveis, que é
    pior. Então sai do mapa, e a linha vai para o censo com o motivo.

    Contar objeto invisível como completude também seria régua feita da própria
    resposta: o número subiria sem que existisse conteúdo.
    """
    censo = le_censo()
    alvos = {(l["mapa"], l["x"], l["y"]): l for l in censo.get("dentro", [])}
    plano, contagem, tirados = {}, Counter(), []
    for mapa in sorted({m for m, _, _ in alvos}):
        p = os.path.join(REPO, "data/maps", mapa, "map.json")
        with open(p, encoding="utf-8") as f:
            dados = json.load(f)
        fica = []
        for o in dados.get("object_events", []):
            k = (mapa, o["x"], o["y"])
            if k in alvos and RG.eh_mudo(o):
                linha = dict(alvos[k])
                linha.pop("entrou", None)
                linha["motivo"] = SEM_IDENTIDADE
                tirados.append(linha)
                contagem[f"tirado ({linha['gfx_fonte']})"] += 1
                continue
            fica.append(o)
        if len(fica) != len(dados.get("object_events", [])):
            dados["object_events"] = fica
            plano[mapa] = dados
    if tirados:
        saiu = {(l["mapa"], l["x"], l["y"]) for l in tirados}
        censo["dentro"] = [l for l in censo["dentro"]
                           if (l["mapa"], l["x"], l["y"]) not in saiu]
        censo["fora"] = [l for l in censo.get("fora", [])
                         if (l["mapa"], l["x"], l["y"]) not in saiu] + tirados
    return plano, contagem, censo


def escreve(plano, censo=None, ja_partido=False):
    for mapa, dados in plano.items():
        RG.grava_como_estava(
            os.path.join(REPO, "data/maps", mapa, "map.json"), dados)
    if censo is None:
        return
    if not ja_partido:
        censo = {"dentro": [l for l in censo if l.get("entrou")],
                 "fora": [l for l in censo if not l.get("entrou")]}
    with open(CENSO, "w", encoding="utf-8") as f:
        json.dump(censo, f, ensure_ascii=False, indent=1)


def demo():
    """Autoteste. Cada asserção existe porque o erro dela já é conhecido."""
    # 1. o casamento é 1:1 por coordenada, e DOIS na mesma coordenada valem dois
    nossos = [{"x": 1, "y": 1}, {"x": 2, "y": 2}]
    fonte = [{"x": 1, "y": 1}, {"x": 1, "y": 1}, {"x": 2, "y": 2},
             {"x": 3, "y": 3}]
    fora = sobrando(nossos, fonte)
    assert [(o["x"], o["y"]) for o in fora] == [(1, 1), (3, 3)], fora

    # 2. o objeto emitido é exatamente o que o restaura_gfx_johto chama de MUDO,
    #    senão o passo seguinte do encadeamento não o enxerga
    assert RG.eh_mudo(novo_objeto({"x": 4, "y": 5, "elevation": 3}))
    assert novo_objeto({"x": 4, "y": 5, "elevation": 3})["elevation"] == 3

    # 3. a régua de geometria: SÓ o warp recusa; parede e fora do retângulo
    #    entram com nota, porque a fonte é jogável e desenha os dois
    real = json.load(open(os.path.join(REPO, "data/maps/AzaleaTown/map.json"),
                          encoding="utf-8"))
    ok, nota = julga(real, {"x": -3, "y": -3})
    assert ok is True and "retângulo" in nota, (ok, nota)
    assert real["warp_events"], "AzaleaTown sem warp: o teste abaixo perdeu o pé"
    w = real["warp_events"][0]
    ok, motivo = julga(real, {"x": w["x"], "y": w["y"]})
    assert ok is False and "warp" in motivo, (ok, motivo)
    # tile de parede real deste mapa: entra, e a nota diz que é decoração
    parede = next(((x, y) for y in range(20) for x in range(20)
                   if colisao(real["layout"], x, y) == 1), None)
    assert parede, "AzaleaTown sem nenhum tile de colisão 1 nos 20x20 iniciais"
    ok, nota = julga(real, {"x": parede[0], "y": parede[1]})
    assert ok is True and "colisão" in nota, (ok, nota)

    # 4. IDEMPOTÊNCIA, que é o portão caro: rodar duas vezes não pode duplicar.
    #    Simula o depois-de-aplicar somando o que entraria e remedindo.
    plano, censo, _ = monta()
    entram = sum(1 for l in censo if l.get("entrou"))
    depois = 0
    for mapa, dados in plano.items():
        with open(os.path.join(HNS, "data/maps", mapa, "map.json"),
                  encoding="utf-8") as f:
            fonte = json.load(f).get("object_events", [])
        depois += len(sobrando(dados["object_events"], fonte))
    assert depois == sum(1 for l in censo
                         if not l.get("entrou") and l["mapa"] in plano), (
        f"segunda rodada acharia {depois} candidatos onde só as recusas podem "
        "sobrar")
    print(f"demo ok: {entram} objetos entrariam, e a segunda rodada acharia "
          f"só as {depois} recusas dos mesmos mapas")


def main():
    if DEMO:
        demo()
        return 0
    if LIMPA:
        plano, contagem, censo = limpa()
        print(f"mapas tocados: {len(plano)}   objetos tirados: "
              f"{sum(contagem.values())}")
        for k, v in contagem.most_common():
            print(f"   {v:4}  {k}")
        if APLICA:
            escreve(plano, censo, ja_partido=True)
            print("\nescrito.")
        else:
            print("\n(nada escrito; rode com --limpa --aplica)")
        return 0

    plano, censo, contagem = monta()
    entrou = sum(1 for l in censo if l.get("entrou"))
    print(f"mapas tocados: {len(plano)}   objetos criados: {entrou}   "
          f"recusados: {len(censo) - entrou}")
    print("\ncontagem:")
    for k, v in contagem.most_common():
        print(f"   {v:4}  {k}")
    if APLICA:
        escreve(plano, censo)
        print("\nescrito.")
    else:
        print("\n(nada escrito; rode com --aplica)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
