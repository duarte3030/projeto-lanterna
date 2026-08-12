#!/usr/bin/env python3
"""Remede os NPC mudos de Sinnoh e diga, um a um, POR QUE cada um ainda e mudo.

A divisao de 11/08/2026 (559 mudos: 344 treinador, 108 Wi-Fi/Union, 68 de
sistema, 19 de charmap, 8 de alinhamento) foi medida a mao e nao sobreviveu ao
dia seguinte: o B3 escondeu duplicado, o B4 deu `trainerbattle` a treinador e o
B1.a esta criando mapa novo. Numero de ontem nao mede a arvore de hoje, entao
esta ferramenta refaz a conta inteira toda vez que roda.

MUDO, aqui, e objeto de mapa de Sinnoh com `"origem": "pokeplatinum"` e
`script` igual a `0`: da para esbarrar nele, nao para conversar. Quem esta
escondido atras de `FLAG_SINNOH_NPC_DUPLICADO` (o perdedor dos pares do B3)
sai contado em SEPARADO, porque o jogador nunca o encontra; somar os dois
inflaria a fila de trabalho com gente que nao esta no jogo.

O alinhamento, que e o elo fraco de tudo nesta frente, tem dois passos:

1. **ordem + grafico**, a regra de `texto_sinnoh.py`: a contagem bate e o
   `graphics_id` bate posicao a posicao. Vale para os mapas escritos de uma vez
   so pelo importador.
2. **subsequencia por coordenada**, quando a 1 falha. O importador percorre a
   fonte EM ORDEM e poe cada NPC no tile livre mais proximo de `conv(e)` dentro
   de raio 8 (`importa_npcs_sinnoh.livre`), pulando quem nao couber. Entao o
   casamento certo e uma SUBSEQUENCIA da fonte, com o grafico igual e a
   distancia de Chebyshev dentro do raio que o proprio importador usou. Se
   existir mais de uma subsequencia possivel, o mapa reprova: escolher uma
   seria o chute que a ferramenta existe para evitar.

Uso:
    python3 dev_scripts/mudos_sinnoh.py                # divisao por categoria
    python3 dev_scripts/mudos_sinnoh.py --lista CAT    # os mudos de uma categoria
    python3 dev_scripts/mudos_sinnoh.py --lista-wifi   # os de Wi-Fi, por mapa
    python3 dev_scripts/mudos_sinnoh.py --lojas        # estoque de cada loja
    python3 dev_scripts/mudos_sinnoh.py --esconde-wifi # ESCREVE: poe a flag neles
    python3 dev_scripts/mudos_sinnoh.py --demo
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importa_npcs_sinnoh as I  # noqa: E402
import texto_sinnoh as T  # noqa: E402
import valida_mapas_sinnoh as V  # noqa: E402
from texto_placas_sinnoh import (campos_do_header, entradas_de_script,  # noqa: E402
                                 banco_de_texto)

MUDO = ("0", "0x0", "NULL", "")
FLAG_DUP = "FLAG_SINNOH_NPC_DUPLICADO"

# Rotina de sistema do Platinum, reconhecida pelo comando que o corpo chama.
# Nao ha texto a portar nesses: o rotulo E a rotina.
SISTEMA = (
    (re.compile(r"^Common_CallPokecenterNurse"), "enfermeira"),
    (re.compile(r"^PokeMartCommonWithGreeting"), "loja_comum"),
    (re.compile(r"^PokeMartSpecialtiesWithGreeting\s+(\w+)"), "loja_especial"),
    (re.compile(r"^PokeMart(Common|Specialties)?\b"), "loja"),
)

# Wi-Fi, Union Room e Colosseum: sistema de comunicacao do DS que esta ROM nao
# tem. O sinal e o comando, nao o nome do rotulo: `Dummy9004` nao diz nada.
COMUNICACAO = re.compile(
    r"UnionRoom|WiFi|Wifi|WIFI|Colosseum|COLOSSEUM|VAR_COMMUNICATION"
    r"|CommunicationStandby|SelectMultiplayer|Gts|GTS|VideoPhone", re.I)

# `include/script_manager.h` da fonte: acima de 2000 o `script` de um evento nao
# indexa mais a lista do PROPRIO mapa, e sim um arquivo compartilhado. Sem esta
# tabela os 108 atendentes de Wi-Fi/Union caem como "indice fora da lista", que
# e verdade e nao e resposta. Faixa -> (nome do arquivo, categoria).
FAIXAS = [
    (2000, "COMMON_SCRIPTS", "compartilhado"),
    (2500, "BG_EVENTS", "compartilhado"),
    (2800, "BERRY_TREE", "compartilhado"),
    (3000, "SINGLE_BATTLES", "treinador"),
    (5000, "DOUBLE_BATTLES", "treinador"),
    (7000, "VISIBLE_ITEMS", "item"),
    (8000, "HIDDEN_ITEMS", "item"),
    (8800, "SAFARI_GAME", "compartilhado"),
    (8900, "RECORD_CHATOT_CRY", "compartilhado"),
    (8950, "VS_SEEKER", "compartilhado"),
    (8970, "POKE_RADAR", "compartilhado"),
    (9000, "POKEMON_CENTER_2F_COMMON", "wifi_union"),
    (9100, "COMMUNICATION_CLUB", "wifi_union"),
    (9200, "POKEMON_CENTER_B1F_COMMON", "wifi_union"),
    (9300, "GROUP_CONNECTION", "wifi_union"),
    (9400, "POFFIN_COMMON", "sistema_ausente"),
    (9500, "DAY_CARE_COMMON", "sistema_ausente"),
    (9600, "INIT_NEW_GAME", "compartilhado"),
    (9700, "FOLLOWER_PARTNERS", "compartilhado"),
    (9800, "CONTESTS", "sistema_ausente"),
    (9900, "UNUSED_0397", "compartilhado"),
    (9950, "POKEDEX_RATINGS", "compartilhado"),
    (10000, "FIELD_MOVES", "compartilhado"),
    (10100, "TV_BROADCAST", "compartilhado"),
    (10150, "TV_REPORTER_INTERVIEWS", "compartilhado"),
    (10200, "MYSTERY_GIFT_DELIVERYMAN", "compartilhado"),
    (10300, "COUNTERPART_TALK", "compartilhado"),
    (10400, "POKEMON_CENTER_DAILY_TRAINERS", "compartilhado"),
    (10450, "BATTLE_FRONTIER_RECORDS", "compartilhado"),
    (10490, "SCRATCH_OFF_CARDS", "compartilhado"),
]


def faixa(idx):
    """(nome do arquivo compartilhado, categoria) do `script` de um evento."""
    achado = None
    for base, nome, cat in FAIXAS:
        if idx >= base:
            achado = (nome, cat, idx - base)
    return achado


# O alinhamento (ordem, depois subsequencia por coordenada) mora em
# `texto_sinnoh.alinha_npcs`, que e quem ESCREVE a fala. Medir com uma copia da
# regra faria o relatorio prometer NPC que o escritor recusa, e vice-versa.
alinha = T.alinha_npcs
subsequencias = T.subsequencias


def corpo_do_rotulo(corpos, rot, visto=None):
    """As linhas do caminho de fall-through, seguindo `GoTo` cru e `Call`."""
    visto = visto or set()
    linhas = []
    while rot and rot not in visto:
        visto.add(rot)
        prox = None
        for l in corpos.get(rot, []):
            linhas.append(l)
            g = re.match(r"^GoTo\s+(\w+)\s*$", l)
            if g:
                prox = g.group(1)
                break
        rot = prox
    return linhas


def classifica(dela, ordem, corpos, banco):
    """(categoria, detalhe) de UM evento da fonte que aqui esta mudo."""
    idx = dela.get("script")
    if isinstance(idx, str) and idx.startswith("TRAINER_"):
        return "treinador", idx
    if not isinstance(idx, int):
        return "script_estranho", str(idx)
    if idx >= FAIXAS[0][0]:
        nome, cat, rel = faixa(idx)
        return cat, f"{nome}+{rel}"
    if idx == 0:
        return "sem_script_na_fonte", "0"
    if not (1 <= idx <= len(ordem)):
        return "script_fora_da_lista", str(idx)
    rot = ordem[idx - 1]
    linhas = corpo_do_rotulo(corpos, rot)
    corpo = "\n".join(linhas)
    if COMUNICACAO.search(corpo) or COMUNICACAO.search(rot):
        return "wifi_union", rot
    tid, buffers = T.texto_do_rotulo(corpos, rot)
    if tid is None:
        for l in linhas:
            for rx, nome in SISTEMA:
                m = rx.match(l)
                if m:
                    # o argumento e a IDENTIDADE da loja
                    # (`MART_SPECIALTIES_ID_CANALAVE`): sem ele, casar a
                    # especialidade por parecenca de nome fazia
                    # `..._ETERNA_MART` casar com toda loja, por causa do
                    # sufixo `MART`, e tres cidades saiam acusadas de vender o
                    # estoque de Eterna.
                    arg = m.group(1) if m.groups() and m.lastindex else ""
                    return "sistema", f"{nome}:{rot}:{arg or ''}"
        return "sem_comando_de_texto", rot
    if tid not in banco:
        return "texto_ausente", f"{rot}/{tid}"
    if T.resolve(banco[tid], buffers)[0] is None:
        return "charmap", f"{rot}/{tid}"
    return "portavel", f"{rot}/{tid}"


def escondido(o):
    """O jogador encontra este objeto? Flag NENHUMA no campo `flag` e que o faz
    nascer (`src/event_object_movement.c:2882` so cria quando `!FlagGet`).

    Ela e QUALQUER flag, nao so a do B3: desde 12/08 os atendentes de Wi-Fi
    estao atras de FLAG_SINNOH_WIFI_ESCONDIDO, e contar so a duplicado punha os
    102 na coluna de "visivel", ou seja, o relatorio prometia trabalho que ja
    tinha sido feito.
    """
    return str(o.get("flag", "0")) not in ("0", "0x0", "")


def varre():
    """[(mapa, indice, objeto, evento da fonte, categoria, detalhe, escondido)]"""
    sprites = V.sprites_utilizaveis()
    heads = I.headers_do_platinum()
    linhas, reprovados, hidden, coord = [], [], 0, 0
    for meu, header, arq_ev in T.casados():
        pe = os.path.join(T.PLAT, "res/field/events", arq_ev + ".json")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not (os.path.exists(pe) and os.path.exists(pm)):
            continue
        fonte = json.load(open(pe, encoding="utf-8"))
        d = json.load(open(pm, encoding="utf-8"))
        # A conta do `fora_hidden` do importador, na MESMA ordem de filtro: so e
        # "objeto que ficou de fora pela hidden_flag" quem passaria por todos os
        # filtros anteriores. Contar hidden_flag cru daria 1092, porque pedra de
        # Strength e Poke Ball do chao tambem nascem escondidas e nunca foram
        # candidatas a virar NPC.
        #
        # 12/08/2026: desconta quem JA entrou com a cena junto. `cena_galactica
        # _sinnoh.py` grava o LOCALID da fonte no campo `fonte_id` do objeto que
        # cria, entao da para responder "este continua fora?" sem chutar. Sem
        # este desconto o placar prometia trabalho ja feito, que e o mesmo
        # defeito de regua que a linha do Wi-Fi levou dois dias para largar.
        ja_com_cena = {o.get("fonte_id")
                       for o in (d.get("object_events") or [])
                       if o.get("fonte_id")}
        for e in fonte.get("object_events", []):
            classe = e.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
            if any(t in classe for t in I.GRAFICOS_PROIBIDOS):
                continue
            if any(t in classe for t in I.NOMES_PROPRIOS):
                continue
            if e.get("id") in ja_com_cena:
                continue
            if str(e.get("hidden_flag", "0")) not in ("0", "0x0"):
                hidden += 1
        coord += len(fonte.get("coord_events", []))
        mudos = [(i, o) for i, o in enumerate(d.get("object_events") or [])
                 if o.get("origem") == "pokeplatinum"
                 and str(o.get("script", "0")) in MUDO]
        if not mudos:
            continue
        pares, metodo = alinha(header, heads[header][1], fonte, d, sprites)
        if pares is None:
            reprovados.append((meu, metodo, len(mudos)))
            for i, o in mudos:
                linhas.append((meu, i, o, None, "alinhamento", metodo,
                               escondido(o)))
            continue
        campos = campos_do_header(header)
        arq_scr, arq_msg = (campos[0], campos[1]) if campos else (None, None)
        ordem, corpos = entradas_de_script(arq_scr) if arq_scr else ([], {})
        banco = banco_de_texto(arq_msg) if arq_msg else {}
        for i, o in mudos:
            dela = pares.get(i)
            if dela is None:
                cat, det = "alinhamento", "fora do casamento"
            else:
                cat, det = classifica(dela, ordem, corpos, banco)
            linhas.append((meu, i, o, dela, cat, det, escondido(o)))
    return linhas, reprovados, hidden, coord


def corpo_daqui(texto, rot, visto=None):
    """As linhas do rotulo `rot` de um scripts.inc NOSSO, seguindo `goto`/`call`."""
    corpos, atual = {}, None
    for l in texto.split("\n"):
        m = re.match(r"^(\w+):{1,2}\s*$", l)
        if m:
            atual = m.group(1)
            corpos[atual] = []
        elif atual is not None:
            corpos[atual].append(l.strip())
    visto = visto or set()
    fila, saida = [rot], []
    while fila:
        r = fila.pop(0)
        if r in visto:
            continue
        visto.add(r)
        for l in corpos.get(r, []):
            saida.append(l)
            g = re.match(r"^(?:goto|call)\s+(\w+)", l)
            if g:
                fila.append(g.group(1))
    return saida, corpos


def mercadoria(corpos, tabela):
    """[ITEM_*] de um rotulo `.2byte` de pokemart deste repo."""
    return [m.group(1) for l in corpos.get(tabela, [])
            for m in [re.match(r"^\.2byte\s+(ITEM_\w+)", l)] if m]


def especialidades_do_platinum():
    """MART_SPECIALTIES_ID_X -> [ITEM_* do Platinum]."""
    txt = open(os.path.join(T.PLAT, "include/data/mart_items.h"),
               encoding="utf-8").read()
    arrays = {m.group(1): re.findall(r"\b(ITEM_[A-Z0-9_]+)\b", m.group(2))
              for m in re.finditer(r"const u16 (\w+)\[\] = \{(.*?)\};", txt, re.S)}
    fora = {}
    # ponytail: a virgula no fim e OPCIONAL. Exigi-la perdia calada a ULTIMA
    # entrada da tabela, `MART_SPECIALTIES_ID_VEILSTONE_B1F`, e o vendedor de
    # frutas do subsolo de Veilstone ficava de fora sem uma linha de aviso.
    for m in re.finditer(r"\[(MART_SPECIALTIES_ID_\w+)\]\s*=\s*(\w+)\s*[,}]", txt):
        fora[m.group(1)] = arrays.get(m.group(2), [])
    return fora, re.findall(r"\{\s*(ITEM_[A-Z0-9_]+),", txt.split("PokeMartCommonItems")[1]
                            .split("};")[0])


def confere_sistema(linhas):
    """[(mapa, papel, veredito, detalhe)] para cada mudo de sistema.

    A pergunta e a da camada da afirmacao: nao "existe um balconista", e sim
    **a rotina que este mapa chama e a certa**. Enfermeira tem que chegar em
    `Common_EventScript_PkmnCenterNurse`; loja tem que ter `pokemart` apontando
    para uma tabela que existe no proprio arquivo, e a mercadoria dessa tabela e
    comparada com a do Platinum.
    """
    espec, comum = especialidades_do_platinum()
    fora, parciais = [], []
    for meu, i, o, dela, cat, det, esc in linhas:
        if cat != "sistema":
            continue
        papel, rot_fonte, arg = (det.split(":") + ["", ""])[:3]
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        texto = open(ps, encoding="utf-8", errors="replace").read() \
            if os.path.exists(ps) else ""
        d = json.load(open(pm, encoding="utf-8"))
        # Todo script que algum objeto DESTE mapa realmente chama. Rotulo solto
        # no arquivo nao conta: NPC nenhum encosta nele.
        chamados = [str(e.get("script", "")) for e in (d.get("object_events") or [])
                    if str(e.get("script", "0")) not in MUDO]
        achou, detalhe = False, ""
        for s in chamados:
            corpo, corpos = corpo_daqui(texto, s)
            junto = "\n".join(corpo)
            if papel == "enfermeira" and "Common_EventScript_PkmnCenterNurse" in junto:
                achou, detalhe = True, s
                break
            if papel.startswith("loja"):
                # Todos os `pokemart` do caminho, nao o primeiro: desde 12/08 um
                # mapa tem ate tres balconistas com tabelas diferentes, e parar
                # no primeiro media o vendedor errado.
                melhor = None
                for m in re.finditer(r"^pokemart\s+(\w+)", junto, re.M):
                    itens = mercadoria(corpos, m.group(1))
                    if not itens:
                        detalhe = f"{s}: tabela {m.group(1)} vazia ou ausente"
                        continue
                    nota = len(set(espec.get(arg, [])) & set(itens))
                    if melhor is None or nota > melhor[0]:
                        melhor = (nota, m.group(1), itens)
                if melhor:
                    _n, tab, itens = melhor
                    achou, detalhe = True, f"{s} -> {tab} ({len(itens)} itens)"
                    # A identidade da loja vem do ARGUMENTO da fonte
                    # (`MART_SPECIALTIES_ID_CANALAVE`), nunca de parecenca de
                    # nome: casar por nome fazia `..._ETERNA_MART` bater com
                    # toda loja pelo sufixo `MART` e acusar tres cidades de
                    # vender o estoque de Eterna.
                    if papel == "loja_especial" and arg in espec:
                        alvo = set(espec[arg])
                        tem = alvo & set(itens)
                        parciais.append((meu, arg, len(tem), len(alvo)))
                        if not tem:
                            fora.append((meu, papel, "tabela generica",
                                         f"{detalhe}; o Platinum vende "
                                         f"{', '.join(espec[arg][:4])} em {arg}"))
                            achou = None   # ja registrado
                    break
        if achou is None:
            continue
        if not achou:
            fora.append((meu, papel, "rotina ausente",
                         detalhe or f"nenhum script deste mapa chega na rotina "
                                    f"(fonte: {rot_fonte})"))
    del comum
    return fora, parciais


FLAG_WIFI = "FLAG_SINNOH_WIFI_ESCONDIDO"

# ---------------------------------------------------------------- lojas ----
#
# TM: o NUMERO nao atravessa. Esta ROM tem 50 TM, na lista gen 3
# (`include/constants/tms_hms.h`), e o Platinum tem 92, na lista gen 4. Os
# `ITEM_TM52`, `54`, `70` e `83` ate existem como constante aqui, mas em
# `src/data/items.h` eles sao vaga numerada com `sQuestionMarksDesc` e move
# nenhum: vender um deles seria vender TM que nao ensina nada.
#
# Para os que sobrevivem, o numero foi PROVADO contra a arvore, nao lembrado.
# O teste: o conjunto de especies que aprende TMnn no Platinum
# (`res/pokemon/*/data.json`, campo `learnset.by_tm`) contra o conjunto que
# aprende cada move por TM aqui (`src/data/pokemon/teachable_learnsets.h`), nas
# 491 especies que casam por nome. Contencao medida em 12/08/2026:
#
#     TM14 -> BLIZZARD      177/177     TM22 -> SOLAR_BEAM   163/163
#     TM15 -> HYPER_BEAM    252/252     TM25 -> THUNDER      136/136
#     TM16 -> LIGHT_SCREEN  117/117     TM33 -> REFLECT       87/87
#     TM17 -> PROTECT       472/474     TM38 -> FIRE_BLAST   117/117
#     TM20 -> SAFEGUARD     107/107
#
# Reflect e Light Screen so se separam por CONTENCAO, nunca por Jaccard: as duas
# distribuicoes sao quase a mesma (0,50 contra 0,50), e quem decide e o
# 87/87 contra 81/87. O nome escrito e o do MOVE (`ITEM_TM_BLIZZARD`), nao o
# numero, para a tabela sobreviver a uma renumeracao de TM.
TM_DAQUI = {
    "ITEM_TM14": "ITEM_TM_BLIZZARD", "ITEM_TM15": "ITEM_TM_HYPER_BEAM",
    "ITEM_TM16": "ITEM_TM_LIGHT_SCREEN", "ITEM_TM17": "ITEM_TM_PROTECT",
    "ITEM_TM20": "ITEM_TM_SAFEGUARD", "ITEM_TM22": "ITEM_TM_SOLAR_BEAM",
    "ITEM_TM25": "ITEM_TM_THUNDER", "ITEM_TM33": "ITEM_TM_REFLECT",
    "ITEM_TM38": "ITEM_TM_FIRE_BLAST",
}

# Tabela do balconista COMUM das duas lojas novas. E a tabela que os oito marts
# de Sinnoh deste repo ja usam, copiada em vez de inventada.
# ponytail: o Platinum trava a lista comum por numero de insignia
# (`PokeMartCommonItems`, 19 itens com `requiredBadges`), e aqui ela e plana.
# Reproduzir o degrau e outra frente: mexe nos oito marts que ja existem, nao
# so nestes dois.
COMUM_PADRAO = ["ITEM_POKE_BALL", "ITEM_POTION", "ITEM_SUPER_POTION",
                "ITEM_ANTIDOTE", "ITEM_PARALYZE_HEAL", "ITEM_AWAKENING"]

# Saudacao que os marts de Sinnoh deste repo ja usam, palavra por palavra. So
# entra em mapa que ainda nao tem uma.
SAUDACAO = ("Welcome! Take a look around, we've\\n"
            "got everything a TRAINER needs.")


def tms_desta_rom():
    """`ITEM_TM_<MOVE>` que existem: o enum nasce da macro FOREACH_TM, entao
    `include/constants/items.h` nao tem os nomes escritos e a busca por texto la
    reprovaria os nove TM bons."""
    global _TMS
    try:
        return _TMS
    except NameError:
        txt = open(os.path.join(REPO, "include/constants/tms_hms.h"),
                   encoding="utf-8").read()
        bloco = txt.split("FOREACH_TM")[1].split("FOREACH_HM")[0]
        _TMS = {f"ITEM_TM_{m}" for m in re.findall(r"F\((\w+)\)", bloco)}
        return _TMS


def traduz_item(nome):
    """(nome do item nesta ROM, motivo da recusa). Nunca inventa substituto."""
    if nome.startswith("ITEM_TM") or nome.startswith("ITEM_HM"):
        novo = TM_DAQUI.get(nome)
        if novo and novo in tms_desta_rom():
            return novo, ""
        return None, "TM/HM de gen 4 sem move nesta ROM"
    if nome in T.itens_desta_rom():
        return nome, ""
    return None, "constante nao existe nesta ROM"

# A cena da Good Rod da Route 209, o piloto do B6. Cada linha e uma coisa que
# tem que estar VERDADE no arquivo, e o `--demo` prova que a checagem morde
# plantando a mutacao que quebraria cada uma.
CENA_GOOD_ROD = (
    ("da o item de verdade", r"^\tgiveitem ITEM_GOOD_ROD$"),
    ("trata mochila cheia", r"goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull"),
    ("acende o 'ja recebi'", r"^\tsetflag FLAG_RECEBEU_GOOD_ROD_SINNOH$"),
    ("le o 'ja recebi' antes de oferecer", r"goto_if_set FLAG_RECEBEU_GOOD_ROD_SINNOH"),
    ("nao oferece a quem ja tem a vara", r"^\tcheckitem ITEM_GOOD_ROD$"),
    ("pergunta com menu sim/nao", r"Route209_Text_GoodRodIsReallyGood, MSGBOX_YESNO"),
    ("enche a STR_VAR do nome do item", r"^\tbufferitemname STR_VAR_1, ITEM_GOOD_ROD$"),
)


def confere_cena(texto, mapa="Route209", ponto="Route209_EventScript_FishermanGoodRod"):
    """[falha] da cena portada: regra que nao aparece, rotulo citado e ausente.

    Duas perguntas diferentes, e as duas na camada do assembler:
    1. cada regra de `CENA_GOOD_ROD` casa no arquivo;
    2. todo rotulo que a cena CITA existe (no proprio arquivo ou nos comuns).
       Rotulo citado e inexistente e `undefined reference` no build, e a versao
       anterior desta checagem so olhava se o script do objeto existia.
    """
    falhas = [nome for nome, rx in CENA_GOOD_ROD
              if not re.search(rx, texto, re.M)]
    daqui = set(re.findall(r"^(\w+):{1,2}\s*$", texto, re.M))
    for alvo in re.findall(r"^\t(?:goto|call)(?:_if_set|_if_eq)?\s+"
                           r"(?:VAR_\w+,\s*\w+,\s*|FLAG_\w+,\s*)?(\w+)", texto, re.M):
        if alvo.startswith(f"{mapa}_") and alvo not in daqui:
            falhas.append(f"rotulo citado e ausente: {alvo}")
    if ponto not in daqui:
        falhas.append(f"ponto de entrada ausente: {ponto}")
    return falhas


def esconde_wifi(linhas, aplica):
    """Poe FLAG_SINNOH_WIFI_ESCONDIDO no campo `flag` dos atendentes de Wi-Fi.

    Decisao do dono do projeto em 12/08/2026: esconder, nao dar fala substituta
    de sistema que nao existe. Tres guardas:

    - **so a categoria `wifi_union`.** A lista sai da mesma varredura do
      relatorio, entao o que e escondido e exatamente o que foi contado.
    - **so quem esta com `flag` zerada.** Os que ja estao atras de
      `FLAG_SINNOH_NPC_DUPLICADO` ficam como estao: eles ja nao nascem, e trocar
      a flag apagaria a marca do B3 sem esconder ninguem a mais.
    - **releitura tardia.** O map.json e lido de novo na hora de escrever, e a
      troca so vale se o objeto daquele indice ainda for o mesmo importado com
      `flag` zerada. Outro agente pode ter mexido no arquivo no meio.
    """
    por_mapa = {}
    for meu, i, o, _dela, cat, _det, esc in linhas:
        if cat != "wifi_union" or esc:
            continue
        if str(o.get("flag", "0")) not in ("0", "0x0", ""):
            continue
        por_mapa.setdefault(meu, []).append((i, o.get("graphics_id"),
                                             o.get("x"), o.get("y")))
    if not aplica:
        return por_mapa, 0, 0
    postos = recusados = 0
    for meu, itens in por_mapa.items():
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        d = json.load(open(pm, encoding="utf-8"))
        lista = d.get("object_events") or []
        mudou = False
        for i, g, x, y in itens:
            if i >= len(lista):
                recusados += 1
                continue
            e = lista[i]
            if e.get("origem") != "pokeplatinum" or e.get("graphics_id") != g \
                    or e.get("x") != x or e.get("y") != y \
                    or str(e.get("flag", "0")) not in ("0", "0x0", ""):
                recusados += 1
                continue
            e["flag"] = FLAG_WIFI
            postos += 1
            mudou = True
        if mudou:
            with open(pm, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
    return por_mapa, postos, recusados


def confere_wifi(linhas):
    """(quantos objetos de Sinnoh tem a flag, quantos deles nao sao Wi-Fi)."""
    esperado = {(meu, i) for meu, i, _o, _d, cat, _t, _e in linhas
                if cat == "wifi_union"}
    com_flag, intrusos = set(), []
    for m in I.nossos_mapas_sinnoh():
        p = os.path.join(REPO, "data/maps", m, "map.json")
        if not os.path.exists(p):
            continue
        for i, o in enumerate(json.load(open(p, encoding="utf-8"))
                              .get("object_events") or []):
            if str(o.get("flag", "0")) == FLAG_WIFI:
                com_flag.add((m, i))
                if (m, i) not in esperado:
                    intrusos.append((m, i, o.get("graphics_id")))
    return com_flag, intrusos


def saudacao_do_mapa(texto, meu, usados):
    """(rotulo da saudacao, trecho novo). Reusa a que o mapa ja tem, se tem.

    Todo mart deste repo ja abre com `msgbox <Mapa>_Text_Cashier`/`_Caixa`. Reusar
    o rotulo poupa a string e, principalmente, faz o vendedor de especialidade
    falar como o vendedor comum do lado, que e o que o Platinum faz.
    """
    m = re.search(r"^\tmsgbox\s+(\w+_Text_\w+), MSGBOX_DEFAULT\n\tpokemart",
                  texto, re.M)
    if m:
        return m.group(1), ""
    lab = f"{meu}_Text_LojaSaudacao"
    if lab in usados:
        return lab, ""
    usados.add(lab)
    return lab, f'\n{lab}:\n\t.string "{SAUDACAO}$"\n'


def planeja_lojas(linhas):
    """{mapa: (trocas, trecho)} e a lista de itens recusados, sem escrever nada.

    Um `pokemart` proprio por vendedor: o Platinum tem DOIS balconistas em cada
    mart (comum e especialidade) e eles vendem coisas diferentes. Hoje os dois
    caem no mesmo `pokemart` generico do caixa nativo, e o de especialidade esta
    mudo.
    """
    espec, _comum = especialidades_do_platinum()
    plano, recusados = {}, []
    porta = {}
    for meu, i, o, _dela, cat, det, _esc in linhas:
        if cat != "sistema" or "loja" not in det:
            continue
        papel, _rot, arg = (det.split(":") + ["", ""])[:3]
        porta.setdefault(meu, []).append((i, papel, arg))
    for meu, vendedores in sorted(porta.items()):
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not (os.path.exists(ps) and os.path.exists(pm)):
            continue
        texto = open(ps, encoding="utf-8", errors="replace").read()
        d = json.load(open(pm, encoding="utf-8"))
        usados = set(re.findall(r"^(\w+)::?", texto, re.M))
        # Balconista COMUM so entra em mapa que nao tem loja nenhuma. Nos oito
        # marts que ja existem, o caixa nativo ja vende a lista comum, e ligar o
        # importado ao lado dele poria duas lojas iguais no mesmo balcao: e o
        # caso de NPC duplicado do B3, nao de loja que falta.
        tem_loja = bool(re.search(r"^\tpokemart\s+\w+", texto, re.M))
        trecho, trocas, seq = "", [], [0]
        for i, papel, arg in sorted(vendedores):
            if i >= len(d.get("object_events") or []):
                continue
            if str(d["object_events"][i].get("script", "0")) not in MUDO:
                continue      # ja tem script: passada anterior, ou outro agente
            if papel != "loja_especial":
                if tem_loja:
                    continue
                fonte = COMUM_PADRAO
            elif arg in espec:
                fonte = espec[arg]
            else:
                continue
            itens = []
            for it in fonte:
                novo, motivo = traduz_item(it)
                (itens.append(novo) if novo
                 else recusados.append((meu, arg or "comum", it, motivo)))
            if not itens:
                recusados.append((meu, arg or "comum", "TABELA INTEIRA",
                                  "nada da fonte existe aqui: vendedor fica mudo"))
                continue
            lab = T.rotulo_livre(usados, meu, "Loja", seq)
            tab = lab.replace("_EventScript_", "_Pokemart_")
            usados.add(tab)
            ola, novo_texto = saudacao_do_mapa(texto + trecho, meu, usados)
            trecho += novo_texto
            trecho += (
                f"\n@ {papel} do Platinum ({arg or 'lista comum'}), "
                f"tabela de include/data/mart_items.h\n"
                f"{lab}::\n\tlock\n\tfaceplayer\n"
                f"\tmsgbox {ola}, MSGBOX_DEFAULT\n"
                f"\tpokemart {tab}\n"
                f"\tmsgbox gText_PleaseComeAgain, MSGBOX_DEFAULT\n"
                f"\trelease\n\tend\n\n"
                f"\t.align 2\n{tab}:\n"
                + "".join(f"\t.2byte {it}\n" for it in itens)
                + "\tpokemartlistend\n")
            trocas.append((i, lab))
        if trocas:
            plano[meu] = (trocas, trecho)
    return plano, recusados


def aplica_lojas(plano):
    """Escreve o plano, relendo cada arquivo na hora. (vendedores, recusados)."""
    postos = recusados = 0
    for meu, (trocas, trecho) in plano.items():
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        d = json.load(open(pm, encoding="utf-8"))
        lista = d.get("object_events") or []
        feito = False
        for i, lab in trocas:
            if i >= len(lista) or str(lista[i].get("script", "0")) not in MUDO \
                    or lista[i].get("origem") != "pokeplatinum":
                recusados += 1
                continue
            lista[i]["script"] = lab
            postos += 1
            feito = True
        if not feito:
            continue
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(os.path.join(REPO, "data/maps", meu, "scripts.inc"),
                  "a", encoding="utf-8") as f:
            f.write("\n@ Lojas de Sinnoh portadas do pokeplatinum "
                    "(dev_scripts/mudos_sinnoh.py --lojas-aplica)\n" + trecho)
    return postos, recusados


def confere_lojas_escritas():
    """Le de volta cada loja escrita e compara com a fonte. [(mapa, id, ...)].

    Ler o plano de novo nao prova nada: o plano e a mesma conta que escreveu.
    Quem responde e o ARQUIVO. Para cada `<Mapa>_Pokemart_Loja<N>` no disco:
    o `MART_SPECIALTIES_ID_*` sai do comentario que o escritor deixou, os itens
    saem do `.2byte`, e a lista tem que ser exatamente a da fonte menos o que
    `traduz_item` recusa, na mesma ordem.
    """
    espec, _c = especialidades_do_platinum()
    fora, ok = [], 0
    for meu in I.nossos_mapas_sinnoh():
        p = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        if not os.path.exists(p):
            continue
        texto = open(p, encoding="utf-8", errors="replace").read()
        _corpo, corpos = corpo_daqui(texto, "")
        for m in re.finditer(r"^@ (loja_\w+) do Platinum \(([^)]*)\).*?\n"
                             r"(\w+)::", texto, re.M | re.S):
            papel, arg, lab = m.groups()
            tab = lab.replace("_EventScript_", "_Pokemart_")
            itens = mercadoria(corpos, tab)
            if papel == "loja_especial":
                esperado = [t for t in (traduz_item(i)[0] for i in espec.get(arg, []))
                            if t]
            else:
                esperado = COMUM_PADRAO
            if itens != esperado:
                fora.append((meu, arg, itens, esperado))
            else:
                ok += 1
    return ok, fora


def main():
    linhas, reprovados, hidden, coord = varre()
    vis = [l for l in linhas if not l[6]]
    esc = [l for l in linhas if l[6]]
    print(f"mudos de Sinnoh: {len(linhas)}  "
          f"(que o jogador encontra: {len(vis)}, escondidos por flag: {len(esc)})\n")
    print(f"{'categoria':24} {'encontrave':>10} {'escondido':>10} {'total':>7}")
    cats = sorted({l[4] for l in linhas})
    for c in cats:
        v = sum(1 for l in vis if l[4] == c)
        e = sum(1 for l in esc if l[4] == c)
        print(f"{c:24} {v:>10} {e:>10} {v + e:>7}")
    print(f"{'TOTAL':24} {len(vis):>10} {len(esc):>10} {len(linhas):>7}")

    if reprovados:
        print(f"\nmapas reprovados pelo alinhamento: {len(reprovados)}")
        for m, motivo, n in reprovados:
            print(f"    {m:40} {motivo:15} {n} mudo(s)")

    print(f"\nnao importados, e que NAO entram sem a cena que os apaga (B6): "
          f"{hidden} objetos com hidden_flag, {coord} coord_events")

    por_mapa, postos, recusados = esconde_wifi(linhas, "--esconde-wifi" in sys.argv)
    alvos = sum(len(v) for v in por_mapa.values())
    com_flag, intrusos = confere_wifi(linhas)
    print(f"\nWi-Fi/Union a esconder com {FLAG_WIFI}: {alvos} em "
          f"{len(por_mapa)} mapas" +
          (f"   escritos: {postos}, recusados na releitura: {recusados}"
           if "--esconde-wifi" in sys.argv else "   (use --esconde-wifi)"))
    print(f"    objetos de Sinnoh hoje com a flag: {len(com_flag)}   "
          f"fora da lista de Wi-Fi: {len(intrusos)}")
    for m, i, g in intrusos:
        print(f"      INTRUSO {m} obj {i} {g}")
    if "--lista-wifi" in sys.argv:
        for m in sorted(por_mapa):
            print(f"    {m:38} {len(por_mapa[m])}  "
                  f"{', '.join(f'obj {i}' for i, _g, _x, _y in por_mapa[m])}")

    p209 = os.path.join(REPO, "data/maps/Route209/scripts.inc")
    falhas = confere_cena(open(p209, encoding="utf-8").read())
    print(f"\ncena piloto do B6 (Good Rod da Route 209): "
          f"{'ok' if not falhas else 'REPROVADA'}")
    for f in falhas:
        print(f"    falta: {f}")

    plano, rec = planeja_lojas(linhas)
    alvo = sum(len(t) for t, _ in plano.values())
    print(f"\nvendedores a ligar com tabela da fonte: {alvo} em {len(plano)} mapas"
          + ("" if "--lojas-aplica" not in sys.argv else ""))
    if "--lojas-aplica" in sys.argv:
        postos, recu = aplica_lojas(plano)
        print(f"    escritos: {postos}   recusados na releitura: {recu}")
        linhas, reprovados, hidden, coord = varre()
    if rec:
        print(f"    itens da fonte RECUSADOS (nao existem nesta ROM): {len(rec)}")
        vistos = set()
        for meu, arg, it, motivo in rec:
            if (it, motivo) in vistos:
                continue
            vistos.add((it, motivo))
            print(f"      {it:24} {motivo}")

    ok_loja, fora_loja = confere_lojas_escritas()
    print(f"    lojas relidas do disco e conferidas contra a fonte: {ok_loja} ok, "
          f"{len(fora_loja)} divergentes")
    for meu, arg, itens, esperado in fora_loja:
        print(f"      {meu} {arg}\n        disco: {itens}\n        fonte: {esperado}")

    n_sist = sum(1 for l in linhas if l[4] == "sistema")
    excecoes, parciais = confere_sistema(linhas)
    print(f"\nNPC de sistema conferidos: {n_sist}   excecoes: {len(excecoes)}")
    for meu, papel, veredito, detalhe in excecoes:
        print(f"    {meu:36} {papel:15} {veredito:18} {detalhe}")
    incompletas = [p for p in parciais if p[2] < p[3]]
    print(f"    lojas de especialidade medidas: {len(parciais)}   "
          f"com estoque INCOMPLETO contra o Platinum: {len(incompletas)}")
    if "--lojas" in sys.argv:
        for meu, arg, tem, total in sorted(parciais):
            print(f"      {meu:34} {arg:38} {tem}/{total} itens da fonte")

    alvo = None
    if "--lista" in sys.argv:
        i = sys.argv.index("--lista")
        alvo = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
    if alvo:
        print(f"\nmudos da categoria {alvo}:")
        for meu, i, o, dela, cat, det, e in linhas:
            if cat != alvo:
                continue
            print(f"  {meu:38} obj {i:<3} {o.get('graphics_id',''):32} "
                  f"({o.get('x')},{o.get('y')}) "
                  f"{'[escondido]' if e else '':12} {det}"
                  f"  {dela.get('id','') if dela else ''}")
    return 0


def demo():
    """As duas regras que uma medicao por ordem crua erraria."""
    # 1. subsequencia unica: a fonte tem 3 e nos temos 2, mas so um casamento
    #    respeita ordem, grafico e raio.
    fc = [({"id": "A"}, (10, 10), "G1"),
          ({"id": "B"}, (20, 20), "G1"),
          ({"id": "C"}, (99, 99), "G1")]
    nossos = [(0, {"graphics_id": "G1", "x": 11, "y": 12}),
              (1, {"graphics_id": "G1", "x": 22, "y": 20})]
    assert subsequencias(fc, nossos) == [(0, 1)]
    # 2. dois candidatos dentro do raio reprovam o mapa em vez de chutar
    fc2 = [({"id": "A"}, (10, 10), "G1"), ({"id": "B"}, (12, 12), "G1")]
    assert len(subsequencias(fc2, [(0, {"graphics_id": "G1", "x": 11, "y": 11})])) == 2
    # 3. grafico diferente nao casa nem colado
    assert subsequencias([({"id": "A"}, (10, 10), "G2")],
                         [(0, {"graphics_id": "G1", "x": 10, "y": 10})]) == []
    # 4. o classificador separa treinador de indice de texto sem abrir arquivo
    assert classifica({"script": "TRAINER_X"}, [], {}, {})[0] == "treinador"
    assert classifica({"script": 1}, ["R"], {"R": ["PokeMartCommonWithGreeting"]},
                      {})[0] == "sistema"
    assert classifica({"script": 1}, ["R"],
                      {"R": ["Common_CallPokecenterNurse LOCALID_X"]},
                      {})[0] == "sistema"
    assert classifica({"script": 1}, ["R"],
                      {"R": ["GoTo U"], "U": ["Message T"]}, {})[0] == "texto_ausente"
    assert classifica({"script": 1}, ["AttendantUnionRoom"],
                      {"AttendantUnionRoom": ["Message T"]}, {"T": ["oi"]})[0] == "wifi_union"
    # 5. o `script` acima de 2000 nao indexa mais o arquivo do mapa: os 108
    #    atendentes de Wi-Fi so aparecem como Wi-Fi por causa desta tabela
    assert classifica({"script": 9001}, [], {}, {}) == ("wifi_union",
                                                       "POKEMON_CENTER_2F_COMMON+1")
    assert classifica({"script": 9204}, [], {}, {})[0] == "wifi_union"
    assert classifica({"script": 9500}, [], {}, {})[0] == "sistema_ausente"

    # 6. a checagem da cena piloto tem que MORDER. Cada mutacao abaixo e um
    #    conserto mal feito de verdade, plantado no texto do arquivo de hoje,
    #    e a checagem tem que reprovar cada uma delas sozinha.
    p = os.path.join(REPO, "data/maps/Route209/scripts.inc")
    real = open(p, encoding="utf-8").read()
    assert not confere_cena(real), confere_cena(real)
    mutacoes = [
        # esqueceu de dar o item: o NPC fala e nao entrega nada
        ("\tgiveitem ITEM_GOOD_ROD\n", "\tnop\n"),
        # mochila cheia deixa de ser tratada: o item some no ar
        ("goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull",
         "goto_if_eq VAR_RESULT, FALSE, Route209_EventScript_GoodRodReel"),
        # nunca acende o "ja recebi": vara infinita
        ("\tsetflag FLAG_RECEBEU_GOOD_ROD_SINNOH\n", "\n"),
        # nunca le o "ja recebi": oferece de novo a quem ja pegou
        ("goto_if_set FLAG_RECEBEU_GOOD_ROD_SINNOH", "goto_if_unset FLAG_UNUSED_0x000"),
        # desvia para um rotulo que nao existe: `undefined reference` no build
        ("Route209_EventScript_GoodRodReel::", "Route209_EventScript_Datilografado::"),
    ]
    for antes, depois in mutacoes:
        assert antes in real, f"a mutacao nao encontrou o alvo: {antes!r}"
        assert confere_cena(real.replace(antes, depois, 1)), \
            f"a checagem da cena NAO mordeu a mutacao {antes!r} -> {depois!r}"
    # 7. as tabelas de loja, comparadas com a fonte INTEIRA, nao por amostra.
    espec, _c = especialidades_do_platinum()
    assert len(espec) == 20, len(espec)   # a ultima entrada nao tem virgula
    # 7a. tabela sem nada de exotico: sai igual a fonte, na ordem, item a item
    vit = espec["MART_SPECIALTIES_ID_VEILSTONE_2F_MID"]
    assert vit == ["ITEM_PROTEIN", "ITEM_IRON", "ITEM_CALCIUM", "ITEM_ZINC",
                   "ITEM_CARBOS", "ITEM_HP_UP"], vit
    assert [traduz_item(i)[0] for i in vit] == vit
    # 7b. tabela de TM: numero de gen 4 vira NOME DE MOVE, e o que esta ROM nao
    #     ensina e recusado em vez de virar TM muda
    tm = espec["MART_SPECIALTIES_ID_VEILSTONE_3F_UP"]
    assert tm == ["ITEM_TM83", "ITEM_TM17", "ITEM_TM54", "ITEM_TM20",
                  "ITEM_TM33", "ITEM_TM16", "ITEM_TM70"], tm
    assert [traduz_item(i)[0] for i in tm] == [
        None, "ITEM_TM_PROTECT", None, "ITEM_TM_SAFEGUARD",
        "ITEM_TM_REFLECT", "ITEM_TM_LIGHT_SCREEN", None]
    # 7c. correio de gen 4 nao existe aqui, e nao vira correio de Hoenn parecido
    assert traduz_item("ITEM_AIR_MAIL") == (None, "constante nao existe nesta ROM")
    # 7d. o TM que sobra tem que existir MESMO: o enum sai da macro FOREACH_TM,
    #     e procurar o nome em items.h (onde ele nao esta escrito) reprovava os
    #     nove bons de uma vez.
    assert "ITEM_TM_REFLECT" in tms_desta_rom()
    assert "ITEM_TM_FALSE_SWIPE" not in tms_desta_rom()
    print("demo ok (5 mutacoes plantadas na cena da Good Rod, 5 reprovadas; "
          "2 tabelas de loja conferidas inteiras contra a fonte)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
