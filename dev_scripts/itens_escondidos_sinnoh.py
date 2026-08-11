#!/usr/bin/env python3
"""As 146 "placas" de Sinnoh que nunca foram placa.

No Platinum, placa e item escondido moram no MESMO array `bg_events` e so se
distinguem pela faixa do campo `script` (`include/script_manager.h:90-98` da
fonte): abaixo de 2500 e placa, 8000 a 8799 e item ESCONDIDO, 8800 pra cima e
Safari/Chatot. O importador (`importa_npcs_sinnoh.py:385`) leu o array cru e
copiou os tres como placa. Resultado medido em 11/08/2026: **146 bg_events de
Sinnoh que sao item escondido disfarcado**, e o jogador para em cima de um item
invisivel para ler "The lettering has faded with age."

Esta ferramenta faz as duas metades do conserto:

1. **Apaga** a bg_event falsa. Ela nunca foi placa; mentir para o jogador e pior
   do que nao ter nada ali. Apagar bg_event NAO quebra save: a save guarda
   indice de mapa, indice de `object_event` e numero de flag, e nada em
   SaveBlock1/2/3 aponta para uma posicao dentro de `bg_events`. Todo acesso do
   motor (`src/field_control_avatar.c:1203`, `src/item_use.c:453` e `:483`,
   `src/secret_base.c`) varre o array por COORDENADA dentro do mapa carregado.
   A unica identidade que atravessa o save de um item escondido e a FLAG, que
   viaja dentro do proprio dado (`hiddenItemId + FLAG_HIDDEN_ITEMS_START`).

2. **Converte** os que valem a pena catar em item escondido de verdade, com a
   mecanica que o pokeemerald ja tem: `bg_events` do tipo `hidden_item`, do
   mesmo jeito que Hoenn faz. Nao existe tabela para manter; o `mapjson` emite
   `bg_hidden_item_event` e o motor le item, quantidade e flag do proprio
   evento.

Converter custa **uma flag por item** e o pool livre do jogo inteiro e pequeno,
entao a lista do que vale (`VALIOSOS`) foi aprovada pelo dono do projeto em
11/08/2026 e o lixo de rota (Stardust, Tinymushroom, Pearl, Shard, Poke Ball,
pocao comum) fica de fora, ou seja, e apagado junto com o resto.

Armadilha ja paga, e que continua valendo aqui: `script - 8000` **nao** e a
posicao na tabela `gHiddenItems` do Platinum, e a posicao da FLAG dentro do
bloco `HIDDEN_ITEM_FLAGS_START` (`src/script_manager.c:534` da fonte). Ler pela
tabela resolve so 139 dos 146. Quem faz essa conta certo e
`texto_sinnoh.tabela_de_itens()`, reusada aqui em vez de reescrita.

Flag compartilhada, de proposito: quatro itens aparecem em DOIS mapas vizinhos
com a MESMA flag do Platinum (Moon Stone em EternaCity e Route211_West, por
exemplo). Isso e costura de mapa da fonte, e o Platinum se comporta assim: pegar
de um lado apaga o do outro. Reproduzimos dando UMA flag nossa aos dois, o que
tambem economiza quatro flags.

Uso:
    python3 dev_scripts/itens_escondidos_sinnoh.py            # so relata
    python3 dev_scripts/itens_escondidos_sinnoh.py --aplica
    python3 dev_scripts/itens_escondidos_sinnoh.py --demo
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import texto_sinnoh as T  # noqa: E402

FLAGS_H = os.path.join(REPO, "include/constants/flags.h")
ITENS_H = os.path.join(REPO, "include/constants/items.h")
APLICA = "--aplica" in sys.argv

# Faixa exclusiva desta frente, tirada de `flags_livres.py` em 11/08/2026.
FAIXA = range(0x8F0, 0x920)          # 0x8F0 a 0x91F, 48 flags
PREFIXO = "FLAG_ITEM_SINNOH_"
ABRE = "// >>> Itens escondidos de Sinnoh (dev_scripts/itens_escondidos_sinnoh.py) >>>"
FECHA = "// <<< Itens escondidos de Sinnoh (dev_scripts/itens_escondidos_sinnoh.py) <<<"

# O que vale gastar flag. Nomes como o Platinum escreve; a traducao para o nome
# desta ROM sai de TRADUZ_ITEM logo abaixo. Lista aprovada pelo dono do projeto.
VALIOSOS = {
    "ITEM_RARE_CANDY",
    # pedras de evolucao
    "ITEM_MOON_STONE", "ITEM_DAWN_STONE", "ITEM_SHINY_STONE", "ITEM_LEAF_STONE",
    "ITEM_WATER_STONE", "ITEM_THUNDERSTONE",
    "ITEM_PP_UP", "ITEM_PP_MAX",
    # placas do Arceus
    "ITEM_DRACO_PLATE", "ITEM_INSECT_PLATE", "ITEM_SKY_PLATE",
    "ITEM_MEADOW_PLATE", "ITEM_ZAP_PLATE",
    "ITEM_ODD_KEYSTONE", "ITEM_SUITE_KEY", "ITEM_RAZOR_FANG",
    "ITEM_REVIVAL_HERB", "ITEM_MAX_REVIVE",
    # vitaminas
    "ITEM_CALCIUM", "ITEM_CARBOS", "ITEM_ZINC", "ITEM_IRON", "ITEM_PROTEIN",
    "ITEM_HP_UP",
}

# Nome que o Platinum usa e esta ROM nao. `ITEM_THUNDERSTONE` ate existe aqui,
# mas so como apelido dentro do enum (`ITEM_THUNDERSTONE = ITEM_THUNDER_STONE`);
# escrever o nome canonico dispensa depender de como o preproc resolve apelido.
TRADUZ_ITEM = {"ITEM_THUNDERSTONE": "ITEM_THUNDER_STONE"}


def itens_da_fonte():
    """[(mapa, pos, x, y, item, quantidade, flag do Platinum)] das 146.

    `pos` e o indice dentro do NOSSO array `bg_events`. O alinhamento e o mesmo
    de `texto_sinnoh`, e pela mesma razao: o importador nao gravou o indice de
    origem, sobra a ORDEM, e a ordem so vale onde a contagem bate. Mapa que nao
    bate fica inteiro de fora, sem exececao.
    """
    saida = []
    for meu, header, arq_ev in T.casados():
        pe = os.path.join(T.PLAT, "res/field/events", arq_ev + ".json")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not (os.path.exists(pe) and os.path.exists(pm)):
            continue
        fonte = json.load(open(pe, encoding="utf-8"))
        d = json.load(open(pm, encoding="utf-8"))
        _, f_placas = T.separa_fonte(fonte)
        n_placas = [(i, b) for i, b in enumerate(d.get("bg_events", []))
                    if b.get("origem") == "pokeplatinum"]
        if not n_placas or len(n_placas) != len(f_placas):
            continue
        tab = T.tabela_de_itens()
        for dela, (pos, nossa) in zip(f_placas, n_placas):
            if nossa.get("script") != T.GENERICO:
                continue
            idx = dela.get("script")
            if not (isinstance(idx, int) and idx in T.ITEM_ESCONDIDO):
                continue
            item, qtd, flag = (tab[idx - 8000] if idx - 8000 < len(tab)
                               else ("?", "?", "?"))
            saida.append((meu, pos, nossa.get("x"), nossa.get("y"),
                          item, qtd, flag))
    return saida


def identificadores_de_item():
    """Todo nome de item que o enum desta ROM define."""
    corpo = open(ITENS_H, encoding="utf-8").read()
    return set(re.findall(r"^\s*(ITEM_[A-Z0-9_]+)\s*[=,]", corpo, re.M))


def reparte(achados, conhecidos, faixa=FAIXA):
    """(converter, apagar, flags) a partir da lista crua.

    `converter` = [(mapa, pos, x, y, item desta ROM, quantidade, flag nossa)]
    `apagar`    = [(mapa, pos, motivo)]
    `flags`     = [(flag nossa, FLAG_UNUSED_0xNNN, item, flag do Platinum)]

    Item aprovado cujo nome nao existe nesta ROM cai em `apagar` com o motivo
    escrito: constante que nao existe nao vira item, vira erro de montagem.
    """
    converter, apagar = [], []
    ordem, por_plat = [], {}
    for mapa, pos, x, y, item, qtd, plat in achados:
        nosso = TRADUZ_ITEM.get(item, item)
        if item not in VALIOSOS:
            apagar.append((mapa, pos, "lixo de rota"))
            continue
        if nosso not in conhecidos:
            apagar.append((mapa, pos, f"{item} nao existe nesta ROM"))
            continue
        if plat not in por_plat:
            por_plat[plat] = None
            ordem.append((plat, nosso))
        converter.append([mapa, pos, x, y, nosso, int(qtd), plat])

    if len(ordem) > len(faixa):
        raise SystemExit(f"faltam flags: {len(ordem)} itens distintos para "
                         f"{len(faixa)} flags da faixa reservada.")

    flags = []
    for (plat, nosso), n in zip(sorted(ordem), faixa):
        nome = PREFIXO + plat.replace("FLAG_OBTAINED_HIDDEN_", "")
        por_plat[plat] = nome
        flags.append((nome, f"FLAG_UNUSED_0x{n:03X}", nosso, plat))
    for linha in converter:
        linha[6] = por_plat[linha[6]]
    return [tuple(l) for l in converter], apagar, flags


def novo_bg(velho, item, flag, qtd):
    """A bg_event virando item escondido. So o que o mapjson le fica."""
    return {"type": "hidden_item", "x": velho["x"], "y": velho["y"],
            "elevation": velho.get("elevation", 0), "item": item,
            "flag": flag, "quantity": qtd, "underfoot": False,
            "origem": "pokeplatinum"}


def aplica_em_lista(bg, plano):
    """Nova lista de bg_events, e quantas posicoes foram recusadas.

    `plano` = {pos: dict novo ou None para apagar}. Uma posicao so e mexida se
    o evento que esta la AINDA e a placa generica importada; qualquer outra
    coisa e recusada em vez de sobrescrita, porque outro agente pode ter mexido
    no mesmo arquivo. E o que torna a ferramenta idempotente: numa segunda
    passada nada mais casa e nada acontece.
    """
    saida, recusados = [], 0
    for i, ev in enumerate(bg):
        if i not in plano:
            saida.append(ev)
            continue
        if ev.get("origem") != "pokeplatinum" or ev.get("script") != T.GENERICO:
            recusados += 1
            saida.append(ev)
            continue
        if plano[i] is not None:
            saida.append(plano[i])
    return saida, recusados


def flags_em_uso():
    """[(flag nossa, FLAG_UNUSED_0xNNN, item)] lido dos map.json de verdade.

    O bloco do flags.h e REGENERADO daqui, nunca do que a passada atual acabou
    de decidir. Foi assim que a primeira versao se estragou sozinha: na segunda
    passada ela nao achava mais nada para converter (correto, ja estava feito) e
    reescrevia o bloco VAZIO, apagando os 46 apelidos e deixando o build sem os
    nomes que os map.json citam. Regenerar do estado em disco torna a ferramenta
    idempotente de verdade e conserta o bloco se alguem o truncar.

    A ordem e a mesma da atribuicao original (nome ordenado -> faixa), porque
    nosso nome e o nome da flag do Platinum com prefixo trocado: prefixo
    constante nao muda ordem alfabetica.
    """
    achado = {}
    base = os.path.join(REPO, "data/maps")
    for mapa in os.listdir(base):
        pm = os.path.join(base, mapa, "map.json")
        if not os.path.exists(pm):
            continue
        for ev in json.load(open(pm, encoding="utf-8")).get("bg_events") or []:
            f = ev.get("flag", "")
            if ev.get("type") == "hidden_item" and f.startswith(PREFIXO):
                achado[f] = ev.get("item")
    if len(achado) > len(FAIXA):
        raise SystemExit(f"{len(achado)} flags em uso para {len(FAIXA)} da faixa.")
    return [(n, f"FLAG_UNUSED_0x{v:03X}", achado[n])
            for n, v in zip(sorted(achado), FAIXA)]


def escreve_flags(flags):
    """Poe (ou troca) o bloco de apelidos dentro do guard do flags.h."""
    if not flags:
        return
    texto = open(FLAGS_H, encoding="utf-8").read()
    largura = max(len(n) for n, _, _ in flags) + 2
    linhas = [ABRE,
              "// Uma flag por item. Item que aparece em dois mapas vizinhos com a mesma",
              "// flag do Platinum divide a flag aqui tambem: e costura de mapa da fonte,",
              "// e pegar de um lado apaga o do outro, como no jogo original."]
    for nome, unused, item in flags:
        linhas.append(f"#define {nome:<{largura}}{unused}  // {item}")
    linhas.append(FECHA)
    bloco = "\n".join(linhas) + "\n"

    velho = re.search(re.escape(ABRE) + r".*?" + re.escape(FECHA) + r"\n",
                      texto, re.S)
    if velho:
        texto = texto[:velho.start()] + bloco + texto[velho.end():]
    else:
        marca = "#endif // GUARD_CONSTANTS_FLAGS_H"
        i = texto.rindex(marca)
        texto = texto[:i] + bloco + "\n" + texto[i:]
    open(FLAGS_H, "w", encoding="utf-8").write(texto)


def main():
    achados = itens_da_fonte()
    conhecidos = identificadores_de_item()
    converter, apagar, flags = reparte(achados, conhecidos)

    print(f"bg_events de Sinnoh que nunca foram placa: {len(achados)}")
    print(f"  viram item escondido de verdade: {len(converter)}"
          f"   (custo: {len(flags)} flags, faixa 0x{FAIXA[0]:03X} a 0x{FAIXA[-1]:03X})")
    print(f"  apagadas: {len(apagar)}")
    motivos = {}
    for _, _, m in apagar:
        motivos[m] = motivos.get(m, 0) + 1
    for m, n in sorted(motivos.items(), key=lambda x: -x[1]):
        print(f"    {n:3d}  {m}")

    if not APLICA:
        print("\nitem, quantas vezes, flag nossa:")
        for nome, unused, item, plat in flags:
            print(f"    {item:<22} {nome} = {unused}")
        print("\n(nada escrito; rode com --aplica)")
        return 0

    por_mapa = {}
    for mapa, pos, x, y, item, qtd, flag in converter:
        por_mapa.setdefault(mapa, {})[pos] = (item, flag, qtd)
    for mapa, pos, _ in apagar:
        por_mapa.setdefault(mapa, {})[pos] = None

    escritos = convertidas = apagadas = recusadas = 0
    for mapa, alvos in sorted(por_mapa.items()):
        pm = os.path.join(REPO, "data/maps", mapa, "map.json")
        # Releitura tardia, colada na escrita: outro agente mexe nos
        # `object_events` dos mesmos arquivos. So a chave `bg_events` e trocada,
        # e o resto do arquivo volta do disco como estava.
        atual = json.load(open(pm, encoding="utf-8"))
        bg = atual.get("bg_events") or []
        plano = {}
        for pos, alvo in alvos.items():
            if pos >= len(bg):
                recusadas += 1
                continue
            plano[pos] = None if alvo is None else novo_bg(bg[pos], *alvo)
        nova, rec = aplica_em_lista(bg, plano)
        recusadas += rec
        if nova == bg:
            continue
        atual["bg_events"] = nova
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(atual, f, indent=2, ensure_ascii=False)
            f.write("\n")
        escritos += 1
        convertidas += sum(1 for p, a in plano.items()
                           if a is not None and bg[p].get("script") == T.GENERICO)
        apagadas += sum(1 for p, a in plano.items()
                        if a is None and bg[p].get("script") == T.GENERICO)

    em_uso = flags_em_uso()
    escreve_flags(em_uso)
    print(f"\nescrito: {convertidas} itens escondidos e {apagadas} placas falsas "
          f"apagadas, em {escritos} mapas")
    print(f"recusados na releitura: {recusadas}")
    print(f"flags.h: {len(em_uso)} apelidos no bloco de Sinnoh")
    return 0


def demo():
    """As regras que quebram calado se alguem mexer nisto."""
    placa = {"type": "sign", "x": 5, "y": 7, "elevation": 0,
             "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
             "script": T.GENERICO, "origem": "pokeplatinum"}
    minha = {"type": "sign", "x": 1, "y": 1, "elevation": 0,
             "script": "Route213_EventScript_HotelSign"}
    bg = [minha, dict(placa), dict(placa, x=9)]

    # 1. converter preserva coordenada e elevacao, e nao deixa `script` para tras
    nova, rec = aplica_em_lista(
        bg, {1: novo_bg(bg[1], "ITEM_RARE_CANDY", "FLAG_ITEM_SINNOH_X", 1), 2: None})
    assert rec == 0
    assert len(nova) == 2, nova
    assert nova[0] == minha, "placa que nao e nossa nao pode ser tocada"
    assert nova[1]["type"] == "hidden_item"
    assert (nova[1]["x"], nova[1]["y"]) == (5, 7)
    assert "script" not in nova[1] and "player_facing_dir" not in nova[1]

    # 2. idempotente: segunda passada no resultado nao acha mais nada
    outra, rec2 = aplica_em_lista(nova, {1: None})
    assert outra == nova and rec2 == 1, (outra, rec2)

    # 3. evento que outro agente mudou e RECUSADO, nunca sobrescrito
    mexido = [dict(placa, script="Outro_EventScript_Coisa")]
    saida, rec3 = aplica_em_lista(mexido, {0: None})
    assert saida == mexido and rec3 == 1

    # 4. o item aprovado cujo nome nao existe nesta ROM nao vira item: e apagado.
    #    (E o caso real do ITEM_SUITE_KEY, que o pokeemerald nao tem.)
    achados = [("M", 0, 1, 1, "ITEM_RARE_CANDY", "1", "FLAG_OBTAINED_HIDDEN_A"),
               ("M", 1, 2, 2, "ITEM_SUITE_KEY", "1", "FLAG_OBTAINED_HIDDEN_B"),
               ("M", 2, 3, 3, "ITEM_STARDUST", "1", "FLAG_OBTAINED_HIDDEN_C"),
               ("N", 0, 4, 4, "ITEM_THUNDERSTONE", "1", "FLAG_OBTAINED_HIDDEN_D"),
               # mesmo item, mesma flag do Platinum, dois mapas vizinhos:
               # uma flag nossa so, como no jogo original
               ("O", 0, 5, 5, "ITEM_THUNDERSTONE", "1", "FLAG_OBTAINED_HIDDEN_D")]
    conhecidos = {"ITEM_RARE_CANDY", "ITEM_STARDUST", "ITEM_THUNDER_STONE"}
    conv, apg, fl = reparte(achados, conhecidos)
    assert len(conv) == 3, conv
    assert len(fl) == 2, fl
    assert conv[1][4] == "ITEM_THUNDER_STONE", "apelido do Platinum tem que traduzir"
    assert conv[1][6] == conv[2][6], "flag compartilhada na costura de mapa"
    assert sorted(m for _, _, m in apg) == ["ITEM_SUITE_KEY nao existe nesta ROM",
                                            "lixo de rota"]
    assert fl[0][1] == "FLAG_UNUSED_0x8F0", fl

    # 5. estourar a faixa reservada tem que PARAR, nunca invadir flag alheia
    muitos = [("M", i, 0, 0, "ITEM_RARE_CANDY", "1", f"FLAG_OBTAINED_HIDDEN_{i}")
              for i in range(3)]
    try:
        reparte(muitos, conhecidos, faixa=range(0x8F0, 0x8F2))
    except SystemExit:
        pass
    else:
        raise AssertionError("faixa estourada passou calada")

    # 6. a flag tem que caber no que o motor sabe ler: o macro
    #    `bg_hidden_item_event` recusa flag abaixo de FLAG_HIDDEN_ITEMS_START, e
    #    `hiddenItemId` e um campo de 13 bits (include/global.fieldmap.h)
    inicio = int(re.search(r"#define FLAG_HIDDEN_ITEMS_START\s+(0x[0-9A-Fa-f]+)",
                           open(FLAGS_H, encoding="utf-8").read()).group(1), 16)
    assert FAIXA[0] > inicio, "flag abaixo de FLAG_HIDDEN_ITEMS_START nao monta"
    assert FAIXA[-1] - inicio < (1 << 13), "hiddenItemId nao cabe em 13 bits"

    # 7. lista vazia NAO apaga o bloco que ja esta no flags.h. E o bug que esta
    #    ferramenta cometeu contra si mesma: a segunda passada nao acha nada
    #    para converter (certo, ja foi feito) e reescrevia o bloco vazio,
    #    levando junto os 46 apelidos que os map.json citam.
    antes = open(FLAGS_H, encoding="utf-8").read()
    escreve_flags([])
    assert open(FLAGS_H, encoding="utf-8").read() == antes, "bloco vazio apagou o bloco"
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
