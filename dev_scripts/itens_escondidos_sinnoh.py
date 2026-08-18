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
import importa_npcs_sinnoh as I  # noqa: E402

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


def _layouts():
    global _LAYOUTS
    try:
        return _LAYOUTS
    except NameError:
        _LAYOUTS = {l["id"]: l for l in json.load(open(
            os.path.join(REPO, "data/layouts/layouts.json"),
            encoding="utf-8"))["layouts"]}
        return _LAYOUTS


def alinha_por_coordenada(meu, header, matriz, fonte, d):
    """{indice do nosso bg_event: evento da fonte}, ou None se o mapa reprova.

    POR QUE NAO E MAIS A ORDEM. A primeira versao alinhava por ORDEM, exigindo
    que a contagem batesse. A propria passada de 11/08/2026 quebrou essa regua:
    apagar 96 bg_events encurtou o nosso array e a contagem parou de bater em 40
    mapas ja resolvidos, alem dos 8 que ela ja reprovava desde o comeco. Ordem
    que so vale antes da primeira escrita nao e alinhamento, e ferramenta que
    so roda uma vez.

    A coordenada, sim, sobrevive: o importador gravou cada placa em
    `conversor_de_coordenada(fonte)` do evento de origem, e nada depois mexeu
    nesse x,y. Entao a identificacao e a conta do importador rodada de novo, nao
    um palpite. Duas guardas mantem isso honesto:

    - **orfao reprova o mapa inteiro.** Se algum bg_event nosso cair numa
      coordenada onde a fonte nao tem evento nenhum, aquele mapa nao foi escrito
      por esta conta e nada nele pode ser identificado. E o que separa, sozinho,
      os 96 mapas de `importa_npcs_sinnoh.py` dos 38 criados por
      `fecha_portas_sinnoh.py` e `converte_cavernas_sinnoh.py`, que usam a
      colocacao `poe()` deles e ja pulam item escondido na origem (por isso nao
      ha nada a consertar neles). Os dois sinais, orfao e o campo `origem` do
      map.json, concordam nos 134 mapas, medido em 11/08/2026.
    - **coordenada com mais de um candidato fica de fora.** Dois eventos da
      fonte que caem no mesmo tile depois da conversao nao se distinguem, e
      escolher um seria exatamente o chute que esta ferramenta existe para
      evitar.
    """
    L = _layouts().get(d.get("layout"))
    if not L:
        return None
    conv = I.conversor_de_coordenada(fonte, L["width"], L["height"], header,
                                     matriz, d)
    if conv is None:
        return None
    _, f_placas = T.separa_fonte(fonte)
    porxy = {}
    for e in f_placas:
        porxy.setdefault(conv(e), []).append(e)
    pares = {}
    for i, b in enumerate(d.get("bg_events") or []):
        if b.get("origem") != "pokeplatinum":
            continue
        cands = porxy.get((b.get("x"), b.get("y")))
        if not cands:
            return None                      # orfao: o mapa inteiro reprova
        if len(cands) == 1:
            pares[i] = cands[0]
    return pares


def itens_da_fonte(relata=False):
    """[(mapa, pos, x, y, item, quantidade, flag do Platinum)] a resolver.

    `pos` e o indice dentro do NOSSO array `bg_events`, e o alinhamento e o de
    `alinha_por_coordenada`. So entra o que ainda e a placa generica importada:
    o que ja virou `hidden_item` numa passada anterior fica quieto.
    """
    heads = I.headers_do_platinum()
    saida, reprovados = [], []
    for meu, header, arq_ev in T.casados():
        pe = os.path.join(T.PLAT, "res/field/events", arq_ev + ".json")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not (os.path.exists(pe) and os.path.exists(pm)):
            continue
        fonte = json.load(open(pe, encoding="utf-8"))
        d = json.load(open(pm, encoding="utf-8"))
        if not any(b.get("origem") == "pokeplatinum"
                   for b in (d.get("bg_events") or [])):
            continue
        pares = alinha_por_coordenada(meu, header, heads[header][1], fonte, d)
        if pares is None:
            reprovados.append(meu)
            continue
        tab = T.tabela_de_itens()
        for pos, dela in sorted(pares.items()):
            nossa = d["bg_events"][pos]
            if nossa.get("script") != T.GENERICO:
                continue
            idx = dela.get("script")
            if not (isinstance(idx, int) and idx in T.ITEM_ESCONDIDO):
                continue
            item, qtd, flag = (tab[idx - 8000] if idx - 8000 < len(tab)
                               else ("?", "?", "?"))
            saida.append((meu, pos, nossa.get("x"), nossa.get("y"),
                          item, qtd, flag))
    if relata and reprovados:
        print(f"mapas reprovados pelo alinhamento (bg_event nosso em coordenada "
              f"que a fonte nao tem): {len(reprovados)}")
        for m in reprovados:
            print("   ", m)
    return saida


def identificadores_de_item():
    """Todo nome de item que o enum desta ROM define."""
    corpo = open(ITENS_H, encoding="utf-8").read()
    return set(re.findall(r"^\s*(ITEM_[A-Z0-9_]+)\s*[=,]", corpo, re.M))


def numeros_no_flags_h():
    """{FLAG_ITEM_SINNOH_X: 'FLAG_UNUSED_0xNNN'} que o flags.h ja grava hoje.

    Numero de flag e promessa permanente: a save guarda o BIT, e nao o nome.
    A primeira versao desta ferramenta reatribuia a faixa inteira por ordem
    alfabetica a cada passada, o que estava certo enquanto ela rodava UMA vez e
    vira quebra de save na segunda: um nome novo no meio do alfabeto empurraria
    todos os seguintes uma casa e o item que o jogador ja pegou voltaria a
    existir (ou sumiria) na partida dele. Daqui em diante quem ja tem numero
    fica com ele, e o nome novo so ocupa vaga livre da faixa.
    """
    texto = open(FLAGS_H, encoding="utf-8").read()
    m = re.search(re.escape(ABRE) + r"(.*?)" + re.escape(FECHA), texto, re.S)
    if not m:
        return {}
    return dict(re.findall(r"#define\s+(" + PREFIXO + r"\w+)\s+"
                           r"(FLAG_UNUSED_0x[0-9A-Fa-f]+)", m.group(1)))


def vagas(faixa, ja):
    """Numeros da faixa que ninguem ainda apelidou, em ordem crescente."""
    tomados = set(ja.values())
    return [n for n in (f"FLAG_UNUSED_0x{v:03X}" for v in faixa)
            if n not in tomados]


def reparte(achados, conhecidos, faixa=FAIXA, ja=None):
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

    if ja is None:
        ja = numeros_no_flags_h()
    livres = iter(vagas(faixa, ja))

    flags = []
    for plat, nosso in sorted(ordem):
        nome = PREFIXO + plat.replace("FLAG_OBTAINED_HIDDEN_", "")
        numero = ja.get(nome) or next(livres, None)
        if numero is None:
            raise SystemExit(f"faltam flags: {len(ordem)} itens distintos e so "
                             f"{len(vagas(faixa, ja))} vagas livres na faixa.")
        por_plat[plat] = nome
        flags.append((nome, numero, nosso, plat))
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

    Quem ja tem numero no flags.h FICA com ele (ver `numeros_no_flags_h`); nome
    novo pega a primeira vaga livre da faixa. Reordenar por alfabeto, que era o
    que esta funcao fazia, renumeraria flag que ja esta na ROM do Gui.

    ARMADILHA QUE SOBRA: se alguem APAGAR o bloco inteiro do flags.h, nao ha de
    onde ler os numeros antigos e a faixa e reatribuida do zero, o que muda o
    significado dos bits na save do Gui. Recuperar o bloco e `git checkout` do
    flags.h, nunca rodar esta ferramenta de novo em cima do buraco.
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
    ja = numeros_no_flags_h()
    livres = iter(vagas(FAIXA, ja))
    saida = []
    for nome in sorted(achado):
        numero = ja.get(nome) or next(livres, None)
        if numero is None:
            raise SystemExit(f"sem vaga livre na faixa para {nome}.")
        saida.append((nome, numero, achado[nome]))
    return sorted(saida, key=lambda t: t[1])


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
    achados = itens_da_fonte(relata=True)
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
    conv, apg, fl = reparte(achados, conhecidos, ja={})
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
        reparte(muitos, conhecidos, faixa=range(0x8F0, 0x8F2), ja={})
    except SystemExit:
        pass
    else:
        raise AssertionError("faixa estourada passou calada")

    # 5b. QUEM JA TEM NUMERO FICA COM ELE. Este e o caso que quebra a save do
    #     Gui se voltar: um nome novo no meio do alfabeto nao pode empurrar o
    #     numero de quem ja esta na ROM.
    velhos = {"FLAG_ITEM_SINNOH_B": "FLAG_UNUSED_0x8F0",
              "FLAG_ITEM_SINNOH_D": "FLAG_UNUSED_0x8F1"}
    dois = [("M", 0, 0, 0, "ITEM_RARE_CANDY", "1", "FLAG_OBTAINED_HIDDEN_B"),
            ("M", 1, 0, 0, "ITEM_RARE_CANDY", "1", "FLAG_OBTAINED_HIDDEN_C"),
            ("M", 2, 0, 0, "ITEM_RARE_CANDY", "1", "FLAG_OBTAINED_HIDDEN_D")]
    _, _, fl2 = reparte(dois, conhecidos, ja=dict(velhos))
    por_nome = {n: u for n, u, _, _ in fl2}
    assert por_nome["FLAG_ITEM_SINNOH_B"] == "FLAG_UNUSED_0x8F0", por_nome
    assert por_nome["FLAG_ITEM_SINNOH_D"] == "FLAG_UNUSED_0x8F1", por_nome
    assert por_nome["FLAG_ITEM_SINNOH_C"] == "FLAG_UNUSED_0x8F2", por_nome
    assert vagas(range(0x8F0, 0x8F3), velhos) == ["FLAG_UNUSED_0x8F2"]

    # 8. ALINHAMENTO POR COORDENADA. O mapa reprova inteiro se algum bg_event
    #    nosso cair onde a fonte nao tem evento: e o unico jeito de nao chutar
    #    qual placa e qual num mapa cujo array encolheu (ou que foi escrito por
    #    outra ferramenta, com outra colocacao).
    fonte = {"object_events": [],
             "bg_events": [{"x": 3, "z": 4, "script": 8000},
                           {"x": 7, "z": 4, "script": 12},
                           {"x": 7, "z": 8, "script": 13}]}
    d = {"layout": "L", "bg_events": [
        {"x": 3, "y": 4, "script": T.GENERICO, "origem": "pokeplatinum"},
        {"x": 7, "y": 8, "script": T.GENERICO, "origem": "pokeplatinum"},
        {"x": 1, "y": 1, "script": "Meu_EventScript_Placa"}]}
    global _LAYOUTS
    _LAYOUTS = {"L": {"width": 10, "height": 10}}
    pares = alinha_por_coordenada("M", "MAP_HEADER_X", None, fonte, d)
    assert set(pares) == {0, 1}, pares
    assert pares[0]["script"] == 8000 and pares[1]["script"] == 13
    # bg nosso numa coordenada que a fonte nao tem: reprova o mapa inteiro
    d["bg_events"][1]["y"] = 9
    assert alinha_por_coordenada("M", "MAP_HEADER_X", None, fonte, d) is None
    # dois eventos da fonte no mesmo tile: aquele indice fica de fora, sem chute
    d["bg_events"][1]["y"] = 8
    fonte["bg_events"].append({"x": 7, "z": 8, "script": 8001})
    pares = alinha_por_coordenada("M", "MAP_HEADER_X", None, fonte, d)
    assert set(pares) == {0}, pares
    del _LAYOUTS

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
