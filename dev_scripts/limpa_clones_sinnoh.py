#!/usr/bin/env python3
"""Apaga o NPC inventado das rotas de Sinnoh, com as quatro provas antes de cada um.

Uso:
    python3 dev_scripts/limpa_clones_sinnoh.py            # só relata
    python3 dev_scripts/limpa_clones_sinnoh.py --aplica
    python3 dev_scripts/limpa_clones_sinnoh.py --demo

## Por que APAGAR e não esconder atrás de flag

`treinadores_rota_sinnoh.py` escondeu 8 clones atrás de `FLAG_SINNOH_NPC_DUPLICADO`
porque a save do Gui estava congelada e apagar objeto move índice. Em 12/08/2026 o
dono reabriu a janela de save, e dentro dela apagar é MELHOR que esconder: devolve
o índice de `objectEvents[]`, devolve os bytes de `object_event` e do texto, e não
gasta flag. Esta ferramenta é a versão "janela aberta" daquela.

## As quatro provas, uma por vez, e o que cada uma vale

1. **Cobertura fechada.** O mapa só entra se os objetos importados baterem um a um
   com as pessoas da fonte (contagem e `graphics_id`, a mesma checagem que libera a
   ligação de treinador) E se cada importado ESCONDIDO for uma pessoa que continua
   representada: como o que esconde importado é a leva de deduplicação, o importado
   escondido tem que ser um TREINADOR da fonte cuja constante `TRAINER_SINNOH_*`
   algum objeto VISÍVEL do mapa batalha. Prova nominal, não contagem de sprite.

   Importado escondido que era falante (não treinador) reprova o mapa inteiro: o
   texto dele do Platinum não está na boca de ninguém que dê para provar, e alguém
   nativo pode ser a única voz daquela pessoa. Eram dois mapas, Route204 e
   Route209, e os dois saíram da recusa por INVERSÃO de par (ver `INVERSOES`), não
   por afrouxar a prova: o importado voltou a nascer e a cobertura fechou.

2. **O excedente é nativo e sem par.** Com a prova 1 fechada, toda pessoa da fonte
   já tem corpo visível: quem é nativo e sobra não representa ninguém do Platinum.
   Um nativo que só fala também não pode ser o corpo de um treinador da fonte,
   porque treinador batalha.

3. **Só fala, e ninguém o cita.** O corpo do script tem que ser `msgbox` e nada
   mais (nada de `goto`, `call`, `warp`, `giveitem`, `setflag`, `applymovement`,
   `special`), e o `local_id` dele não pode aparecer em script nenhum de `data/`,
   `src/` ou `include/`. Medido em 12/08: nenhum `LOCALID_ROUTE2*` de Sinnoh é
   citado por script, e nenhum `scripts.inc` de rota de Sinnoh usa macro de objeto
   (`applymovement`, `removeobject`, `setobjectxy`...). A ferramenta confere de
   novo a cada rodada em vez de confiar nessa medição.

4. **Apaga**: o `object_event` sai do `map.json`, o bloco de script sai do
   `scripts.inc`, e o texto sai junto se mais ninguém o citar.

## A armadilha do apagar, e onde ela mora neste repo

Apagar um `object_event` desloca o `local_id` de todos os objetos seguintes DO
MESMO MAPA, porque `tools/mapjson/mapjson.cpp:443` gera
`#define <local_id> <posição + 1>`. Duas consequências:

- **`include/constants/map_event_ids.h` se conserta sozinho**: é gerado do
  `map.json` a cada build, e a constante nomeada continua apontando para o mesmo
  boneco. É por isso que constante nomeada é o modo seguro de citar objeto.
- **`include/constants/sinnoh/*.h` NÃO se conserta**: são os mesmos `#define`
  escritos à mão, com o número cravado, e o pré-processador aceita redefinição só
  quando o valor é idêntico. Deixar esses números velhos daria `#define` divergente
  e id errado calado. Esta ferramenta renumera esses arquivos e apaga a linha de
  quem morreu, e a verificação no fim confere OBJETO A OBJETO, por `graphics_id` e
  coordenada, que cada constante que sobrou aponta para a MESMA pessoa de antes.

## A segunda leva: quem já estava escondido atrás da flag

`escondidos_nativos()` varre o repo INTEIRO, não só as rotas, e apaga o nativo que
já está atrás de `FLAG_SINNOH_NPC_DUPLICADO`. Esses não repassam pelas quatro
provas, e é decisão do dono (12/08/2026): o julgamento "é inventado" já foi feito e
provado caso a caso quando cada um foi escondido, e apagar hoje é a MESMA decisão
executada mais barato. O que continua valendo é a parte mecânica, que é a que pode
quebrar o build: mapa com macro de objeto por número sai inteiro, e `local_id`
citado por script fica de pé.

Importado escondido pela mesma flag **não entra**: o corpo dele é gente da fonte, e
apagá-lo apagaria conteúdo do Platinum. São 212 objetos, e é por causa deles que a
flag continua em uso depois desta leva.

## Exceção deliberada

`EXCECOES` é escrita à mão: NPC de sistema fica mesmo sem par na fonte (seção 9 do
PRD). Hoje está vazia, e o motivo está medido: os candidatos que pareciam de
sistema (`LOCALID_ROUTE201_CASHIER`, os `_GUARD` dos portões, os `SAILOR` de rota)
só têm `msgbox` no corpo, ou seja, não vendem, não curam e não embarcam ninguém. O
marinheiro da travessia entre regiões mora em mapa de porto (`valida_barco.py`
lista os cinco), nunca em `Route*`, e nenhum deles entra aqui.
"""
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import texto_sinnoh as T  # noqa: E402
import valida_mapas_sinnoh as V  # noqa: E402
import importa_npcs_sinnoh as I  # noqa: E402

PLAT = T.PLAT
APLICA = "--aplica" in sys.argv
SEM_FLAG = ("0", "0x0", "")

# Corpo de NPC que só fala, nas duas formas que o repo usa. É a MESMA expressão de
# `treinadores_rota_sinnoh.py`, de propósito: as duas ferramentas têm que
# concordar sobre o que é "só fala", senão uma esconde o que a outra apagaria.
SO_FALA = re.compile(
    r"^\s*(?:lock\s*\n\s*faceplayer\s*\n\s*)?msgbox\s+\w+,\s*MSGBOX_\w+\s*\n"
    r"\s*(?:release\s*\n\s*)?end\s*$", re.M)

# Macro que recebe local_id NUMÉRICO. Constante nomeada (`LOCALID_*`,
# `OBJ_EVENT_ID_*`) não entra aqui de propósito: o mapjson regera o `#define` dela
# a partir da posição no `map.json`, então ela acompanha o boneco sozinha. Quem
# não acompanha é o número cravado, e mapa que tenha um sai inteiro do plano:
# renumerar argumento de macro é conserto que ninguém conferiu.
MACRO_DE_OBJETO = re.compile(
    r"^\s*(?:applymovement|removeobject|addobject|setobjectxy|setobjectxyperm|"
    r"turnobject|showobjectat|hideobjectat|moveobjectoffscreen|"
    r"setobjectmovementtype|copyobjectxytoperm|setobjectsubpriority|"
    r"resetobjectsubpriority|createvobject|removeobjectat|addobjectat)\s+"
    r"(?![A-Za-z_])", re.M)

# NPC de sistema: fica mesmo sem par na fonte. Uma linha por caso, com o motivo.
EXCECOES = {}

FLAG_CLONE = "FLAG_SINNOH_NPC_DUPLICADO"

# Inversão de par: o importado sai de trás da flag e volta a nascer, e com isso o
# mapa passa a fechar a cobertura e os nativos que só falam podem ser apagados.
#
# Escrita à MÃO, uma linha por par, porque inverter é decisão humana: a leva de
# deduplicação de 11/08 escondeu o importado por ele ser MUDO, e a régua da seção
# 2 do PRD é conteúdo contra a fonte, não quem fala mais alto. Autorizada pelo
# dono em 12/08/2026, dentro da janela de save aberta.
#
# Chave: (nosso mapa, índice da pessoa DENTRO da fonte). Índice da fonte, e não
# posição no nosso array, porque é a fonte que decide quem essa pessoa é; a
# ferramenta confere o `graphics_id` dos dois lados antes de mexer.
INVERSOES = {
    ("Route204", 4): (
        "OBJ_EVENT_GFX_YOUNGSTER",
        "o objeto 6 da fonte tem `script: 0`, ou seja, e MUDO no proprio Platinum "
        "(nao ha entrada de script para o indice 0). Revelar o importado devolve "
        "um boneco identico ao da fonte, e os tres nativos que so falam desta rota "
        "passam a nao ter ninguem para representar"),
    ("Route209", 9): (
        "OBJ_EVENT_GFX_FISHERMAN",
        "o objeto 28 da fonte (`script: 5`) e o pescador que DA a Good Rod: o corpo "
        "dele no Platinum faz `SetVar VAR_0x8004, ITEM_GOOD_ROD` mais menu de sim e "
        "nao e `FLAG_RECEIVED_GOOD_ROD`. O nativo `Route209_EventScript_Fisherman` "
        "nao e essa pessoa: ele so diz para pescar onde ha agua, texto inventado "
        "aqui. O importado volta a nascer na coordenada certa; a cena da Good Rod "
        "de Sinnoh continua por fazer e e de outro bloco"),
}


def le(caminho):
    with open(caminho, encoding="utf-8", errors="replace") as f:
        return f.read()


def pessoa(o):
    """True se o objeto é gente, e não mobília nem placa.

    Mesmo filtro que `separa_fonte` aplica do lado do Platinum: contar item ball
    como pessoa faria a conta de excedente mentir nos dois lados.
    """
    classe = o.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
    return not any(t in classe for t in I.GRAFICOS_PROIBIDOS + I.GRAFICOS_PLACA)


def corpo_do_script(inc, rotulo):
    """Corpo do bloco `rotulo::`, ou None se o rótulo não existe neste arquivo."""
    if not rotulo:
        return None
    m = re.search(rf"^{re.escape(rotulo)}::\n(.*?)(?=\n\S)", inc, re.S | re.M)
    return m.group(1) if m else None


def ignorados(aprovados):
    """Arquivos que NÃO valem como citação, porque são exatamente o que muda.

    O `map.json` do mapa (é dele que o objeto sai), os `include/constants/*/*.h`
    escritos à mão (esta ferramenta os renumera) e o `map_event_ids.h`, que o
    mapjson regera do `map.json` a cada build e por isso se conserta sozinho.
    """
    fora = {os.path.abspath(os.path.join(REPO, "data/maps", m, "map.json"))
            for m, _l, _s in aprovados}
    fora |= {os.path.abspath(f) for f in
             glob.glob(os.path.join(REPO, "include/constants/*/*.h"))}
    fora.add(os.path.abspath(os.path.join(
        REPO, "include/constants/map_event_ids.h")))
    return fora


def _arquivos_de_montagem():
    """Todo arquivo que o assembler ou o compilador enxerga, sem o lixo."""
    saida = []
    for raiz, sub, arqs in os.walk(REPO):
        if any(p in raiz for p in (os.sep + ".git", os.sep + ".claude",
                                   "build", "fontes-mapas")):
            sub[:] = []
            continue
        for a in arqs:
            if a.endswith((".inc", ".s", ".c", ".h")):
                saida.append(os.path.join(raiz, a))
    return saida


def textos_alheios(meu_arquivo):
    """Símbolo `*_Text_*` citado por QUALQUER arquivo que não seja este.

    A unidade de montagem é `data/event_scripts.s` inteira mais o código C, não um
    `scripts.inc` por vez (lição 4.12). Apagar aqui um texto que outro arquivo cita
    só aparece no LINK, quando ninguém mais lembra do que foi apagado.
    """
    global _TEXTOS
    try:
        por_arquivo = _TEXTOS
    except NameError:
        por_arquivo = _TEXTOS = {
            os.path.abspath(p): set(re.findall(r"\b\w+_Text_\w+\b", le(p)))
            for p in _arquivos_de_montagem()}
    meu = os.path.abspath(meu_arquivo)
    achados = set()
    for p, s in por_arquivo.items():
        if p != meu:
            achados |= s
    return achados


def citados_fora(caminhos_ignorados):
    """Todo LOCALID_* que aparece em script, código ou dado, fora dos ignorados.

    Vale para `.inc`, `.s`, `.c`, `.h` e o `heal_locations.json`, que cita NPC de
    respawn por nome. O `map.json` do próprio mapa e os `include/constants/sinnoh/*.h`
    ficam de fora porque são justamente o que esta ferramenta reescreve.
    """
    achados = set()
    alvos = []
    for raiz, sub, arqs in os.walk(REPO):
        # `.claude/worktrees` guarda a cópia de outro agente rodando em paralelo.
        # Contar a cópia dele como citação reprovaria tudo, e a cópia dele não é
        # este repo: quem manda aqui é o diretório de trabalho.
        if any(p in raiz for p in (os.sep + ".git", os.sep + ".claude",
                                   "build", "fontes-mapas")):
            sub[:] = []
            continue
        for a in arqs:
            if a.endswith((".inc", ".s", ".c", ".h", ".json")):
                alvos.append(os.path.join(raiz, a))
    for p in alvos:
        if os.path.abspath(p) in caminhos_ignorados:
            continue
        achados |= set(re.findall(r"LOCALID_\w+", le(p)))
    return achados


def defines_escritos_a_mao():
    """{LOCALID_X: (arquivo, valor)} dos `#define` que NÃO são gerados.

    `include/constants/map_event_ids.h` é gerado pelo mapjson a cada build e está
    no `.gitignore`: ele se conserta sozinho e não entra aqui. Quem precisa de
    conserto é o que foi escrito à mão.
    """
    saida = {}
    for f in sorted(glob.glob(os.path.join(REPO, "include/constants/*/*.h"))):
        if os.path.basename(os.path.dirname(f)) not in ("sinnoh", "johto"):
            continue
        for m in re.finditer(r"^#define\s+(LOCALID_\w+)\s+(\d+)", le(f), re.M):
            saida[m.group(1)] = (f, int(m.group(2)))
    return saida


def identidade(o):
    """Quem é este boneco, sem depender do índice.

    A verificação do fim compara ISTO antes e depois, nunca a posição: posição é
    exatamente o que a edição mexe, então usá-la para conferir a edição não prova
    nada.
    """
    return (o.get("graphics_id"), o.get("x"), o.get("y"), o.get("script"),
            o.get("local_id"))


def aplica_inversoes(escrever):
    """Tira `FLAG_SINNOH_NPC_DUPLICADO` dos importados de `INVERSOES`.

    Roda ANTES do plano, porque é ela que fecha a cobertura dos dois mapas: com o
    importado de volta, toda pessoa da fonte tem corpo visível e o nativo que só
    fala deixa de poder ser a única representação de alguém.

    Recusa em vez de adivinhar se o objeto não estiver exatamente no estado
    esperado: importado, escondido por essa flag, e com o `graphics_id` que a
    tabela escreveu à mão. Rodar de novo com a flag já removida não faz nada.
    """
    sprites = V.sprites_utilizaveis()
    arqs = {m: a for m, _h, a in T.casados()}
    feitos, recusas = [], []
    for (meu, k), (grafico, _motivo) in INVERSOES.items():
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        pe = os.path.join(PLAT, "res/field/events", arqs.get(meu, "") + ".json")
        if not (os.path.exists(pm) and os.path.exists(pe)):
            recusas.append((meu, k, "mapa ou fonte nao encontrados"))
            continue
        # Releitura tardia: o disco manda, sempre.
        d = json.load(open(pm, encoding="utf-8"))
        objs = d.get("object_events") or []
        f_npcs, _ = T.separa_fonte(json.load(open(pe, encoding="utf-8")))
        imp = [(i, o) for i, o in enumerate(objs)
               if o.get("origem") == "pokeplatinum"]
        if len(imp) != len(f_npcs) or k >= len(imp):
            recusas.append((meu, k, "a fonte e o mapa deixaram de bater um a um"))
            continue
        if T.sprite_esperado(f_npcs[k], sprites) != grafico:
            recusas.append((meu, k, "a pessoa da fonte nesse indice mudou de sprite"))
            continue
        i, o = imp[k]
        if o.get("graphics_id") != grafico:
            recusas.append((meu, k, "o objeto importado mudou de sprite"))
            continue
        if str(o.get("flag", "0")) in SEM_FLAG:
            continue                      # já revelado: rodar de novo não repete
        if str(o.get("flag")) != FLAG_CLONE:
            recusas.append((meu, k, "escondido por outra flag: " + str(o.get("flag"))))
            continue
        if escrever:
            objs[i]["flag"] = "0"
            with open(pm, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
        feitos.append((meu, k, i + 1))
    return feitos, recusas


def plano():
    """[(mapa, [(indice, objeto)], motivo_de_recusa)], mapa a mapa."""
    sprites = V.sprites_utilizaveis()
    aprovados, recusas = [], []
    for meu, _header, arq in T.casados():
        if not meu.startswith("Route"):
            continue
        pe = os.path.join(PLAT, "res/field/events", arq + ".json")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        if not (os.path.exists(pe) and os.path.exists(pm)):
            continue
        fonte = json.load(open(pe, encoding="utf-8"))
        d = json.load(open(pm, encoding="utf-8"))
        objs = d.get("object_events") or []
        f_npcs, _ = T.separa_fonte(fonte)
        imp = [(i, o) for i, o in enumerate(objs)
               if o.get("origem") == "pokeplatinum"]
        nativos = [(i, o) for i, o in enumerate(objs)
                   if o.get("origem") != "pokeplatinum" and pessoa(o)
                   and str(o.get("flag", "0")) in SEM_FLAG]
        if not nativos:
            continue

        # PROVA 1a: os importados batem um a um com a fonte.
        if not (len(imp) == len(f_npcs) and
                all(T.sprite_esperado(a, sprites) == b.get("graphics_id")
                    for a, (_i, b) in zip(f_npcs, imp))):
            recusas.append((meu, len(nativos), "prova 1: cobertura aberta, "
                            f"{len(f_npcs)} na fonte contra {len(imp)} importados"))
            continue

        inc = le(ps) if os.path.exists(ps) else ""
        if MACRO_DE_OBJETO.search(inc):
            recusas.append((meu, len(nativos),
                            "prova 3: o mapa usa macro que recebe local_id"))
            continue

        # Quem batalha, de verdade, entre os objetos VISÍVEIS deste mapa.
        batalhados = set()
        for i, o in enumerate(objs):
            if str(o.get("flag", "0")) not in SEM_FLAG:
                continue
            c = corpo_do_script(inc, o.get("script"))
            if c:
                batalhados |= set(re.findall(r"TRAINER_SINNOH_\w+", c))

        # PROVA 1b: todo importado ESCONDIDO continua representado por alguém
        # visível, e a prova é nominal (a constante do treinador), não de sprite.
        buracos = []
        for k, (_i, o) in enumerate(imp):
            # Quem está em `INVERSOES` conta como visível mesmo antes da escrita:
            # `aplica_inversoes` tira a flag dele, e sem isto o relatório seco
            # mostraria um plano diferente do que o `--aplica` executa.
            if str(o.get("flag", "0")) in SEM_FLAG or (meu, k) in INVERSOES:
                continue
            s = f_npcs[k].get("script")
            if not (isinstance(s, str) and s.startswith("TRAINER_")):
                buracos.append(f"falante #{k} da fonte escondido")
                continue
            nossa = "TRAINER_SINNOH_" + s[len("TRAINER_"):]
            if nossa not in batalhados:
                buracos.append(nossa + " escondido e nao batalhado")
        if buracos:
            recusas.append((meu, len(nativos), "prova 1: " + "; ".join(buracos[:2])))
            continue

        # PROVA 2 e 3: nativo visível que só fala.
        alvos, sobrou = [], 0
        for i, o in nativos:
            if o.get("local_id") in EXCECOES:
                sobrou += 1
                continue
            c = corpo_do_script(inc, o.get("script"))
            if c is None or not SO_FALA.match("\n" + c.rstrip()):
                sobrou += 1
                continue
            alvos.append((i, o))
        if alvos:
            aprovados.append((meu, alvos, sobrou))
    return aprovados, recusas


def escondidos_nativos():
    """[(mapa, [(indice, objeto)])] dos nativos que já estão atrás da flag.

    Estes NÃO passam pelas quatro provas de novo, e é decisão do dono
    (12/08/2026): o julgamento "é inventado" foi feito e provado caso a caso
    quando cada um foi escondido, e apagar hoje é a MESMA decisão executada mais
    barato, porque devolve o índice de `objectEvents[]` que esconder não devolve.
    O git guarda tudo se algum julgamento daqueles se revelar errado.

    O que continua valendo é a parte mecânica: mapa com macro de objeto por número
    sai inteiro, e `local_id` citado por script fica de pé.

    Importado escondido pela mesma flag NÃO entra: ele é gente da fonte, e apagar
    o corpo dele apaga conteúdo do Platinum. É o par "resolvido para o lado
    errado", e desfazer isso é inversão, não limpeza.
    """
    saida, recusas = [], []
    for pm in sorted(glob.glob(os.path.join(REPO, "data/maps/*/map.json"))):
        meu = os.path.basename(os.path.dirname(pm))
        objs = json.load(open(pm, encoding="utf-8")).get("object_events") or []
        alvos = [(i, o) for i, o in enumerate(objs)
                 if o.get("origem") != "pokeplatinum"
                 and str(o.get("flag")) == FLAG_CLONE]
        if not alvos:
            continue
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        if os.path.exists(ps) and MACRO_DE_OBJETO.search(le(ps)):
            recusas.append((meu, len(alvos),
                            "o mapa usa macro de objeto com id numerico"))
            continue
        saida.append((meu, alvos, 0))
    return saida, recusas


def tira_bloco(txt, rotulo):
    """(texto sem o bloco `rotulo`, corpo removido). (txt, None) se não existe.

    O bloco vai do rótulo até a próxima linha que começa na coluna zero, que é
    como o repo separa rótulo de rótulo. A linha em branco do fim vem junto, senão
    sobra um buraco de duas linhas a cada remoção.
    """
    m = re.search(rf"^{re.escape(rotulo)}::?\n", txt, re.M)
    if not m:
        return txt, None
    resto = txt[m.end():]
    prox = re.search(r"^\S", resto, re.M)
    fim = m.end() + (prox.start() if prox else len(resto))
    return txt[:m.start()] + txt[fim:], txt[m.start():fim]


def limpa_scripts(inc, rotulos, fora):
    """Tira os blocos de script e os textos que só eles citavam.

    `fora` é o conjunto de símbolos citados em QUALQUER outro arquivo da unidade de
    montagem. Texto citado lá fora fica, mesmo órfão aqui: apagar símbolo que outro
    arquivo referencia é `undefined reference` no link, e o build só reclama disso
    no fim, quando ninguém mais lembra do que foi apagado.
    """
    tirados = []
    for rot in rotulos:
        inc, corpo = tira_bloco(inc, rot)
        if corpo is None:
            continue
        tirados.append(rot)
        for txt in set(re.findall(r"\b\w+_Text_\w+\b", corpo)):
            if txt in fora or re.search(rf"\b{re.escape(txt)}\b",
                                        re.sub(rf"^{re.escape(txt)}:.*?(?=\n\S)",
                                               "", inc, flags=re.S | re.M)):
                continue
            inc, _ = tira_bloco(inc, txt)
            tirados.append(txt)
    return inc, tirados


def renumera_headers(mudancas, escrever):
    """Ajusta os `#define LOCALID_*` escritos à mão. {nome: novo_valor ou None}.

    None apaga a linha (o boneco morreu). O valor novo entra preservando a coluna
    do número SÓ onde o arquivo já era alinhado à mão (separador com mais de um
    espaço); onde o padrão é um espaço só, continua um espaço só, senão a
    renumeração inventaria alinhamento que ninguém pediu.
    """
    defs = defines_escritos_a_mao()
    por_arquivo = {}
    for nome, novo in mudancas.items():
        if nome in defs:
            por_arquivo.setdefault(defs[nome][0], []).append((nome, novo))
    tocados = []
    for arq, itens in por_arquivo.items():
        txt = le(arq)
        for nome, novo in itens:
            pad = re.search(rf"^#define\s+{re.escape(nome)}(\s+)(\d+)[ \t]*$",
                            txt, re.M)
            if not pad:
                continue
            if novo is None:
                txt = re.sub(rf"^#define\s+{re.escape(nome)}\s+\d+[ \t]*\n",
                             "", txt, flags=re.M)
                continue
            sep = pad.group(1)
            if len(sep) > 1:
                sep += " " * max(0, len(pad.group(2)) - len(str(novo)))
            txt = txt[:pad.start()] + f"#define {nome}{sep}{novo}" + txt[pad.end():]
        if escrever:
            with open(arq, "w", encoding="utf-8") as f:
                f.write(txt)
        tocados.append(arq)
    return tocados


def fora_de_sincronia():
    """[(mapa, LOCALID, valor no header, posição real)] do repo inteiro.

    É a pergunta na camada do pré-processador: o `#define` escrito à mão e o que o
    mapjson vai gerar do `map.json` têm que ser o MESMO número, senão a redefinição
    diverge. Serve de verificação depois de apagar e de guarda antes, e é o que
    torna a ferramenta idempotente: rodar de novo com tudo sincronizado não escreve
    nada.
    """
    defs = defines_escritos_a_mao()
    ruins = []
    for p in sorted(glob.glob(os.path.join(REPO, "data/maps/*/map.json"))):
        objs = json.load(open(p, encoding="utf-8")).get("object_events") or []
        for i, o in enumerate(objs):
            li = o.get("local_id")
            if li in defs and defs[li][1] != i + 1:
                ruins.append((os.path.basename(os.path.dirname(p)), li,
                              defs[li][1], i + 1))
    return ruins


def confere(antes, depois, apagados, defs_depois):
    """A verificação na camada da afirmação, mapa a mapa. Devolve lista de erros.

    A afirmação é "cada referência continua apontando para a MESMA pessoa", e ela
    não se confere por índice: índice é o que mudou. Confere-se por identidade
    (`graphics_id` + coordenada + script) e pelo número que o mapjson VAI gerar,
    que é a posição mais um.
    """
    erros = []
    ids_apagados = {identidade(o) for o in apagados}
    esperado = [identidade(o) for o in antes if identidade(o) not in ids_apagados]
    virou = [identidade(o) for o in depois]
    if esperado != virou:
        erros.append("a lista que sobrou nao e a de antes menos os apagados")
    for i, o in enumerate(depois):
        li = o.get("local_id")
        if not li:
            continue
        if li in defs_depois and defs_depois[li][1] != i + 1:
            erros.append(f"{li}: define diz {defs_depois[li][1]}, o mapjson vai "
                         f"gerar {i + 1}")
        antigo = [x for x in antes if x.get("local_id") == li]
        if len(antigo) != 1 or identidade(antigo[0]) != identidade(o):
            erros.append(f"{li} aponta para outra pessoa depois da edicao")
    for o in apagados:
        if o.get("local_id") in defs_depois:
            erros.append(f"{o.get('local_id')}: apagado mas o define ficou")
    return erros


def main():
    # A inversão vem PRIMEIRO e escreve de verdade: é ela que fecha a cobertura
    # dos mapas de `INVERSOES`, e o plano tem que ver o mapa já com o importado
    # visível, senão recusaria os dois de novo pela prova 1.
    invertidos, rec_inv = aplica_inversoes(APLICA)
    if invertidos:
        print("importados revelados (inversao de par, tabela escrita a mao):")
        for m, k, pos in invertidos:
            print(f"  {m:20s} pessoa #{k} da fonte, objeto {pos}"
                  + ("" if APLICA else "   (so simulado)"))
    for r in rec_inv:
        print("  INVERSAO RECUSADA:", *r)

    visiveis, recusas = plano()
    ja_ocultos, rec_ocultos = escondidos_nativos()
    print(f"NPC nativo visivel a apagar (as quatro provas): "
          f"{sum(len(l) for _m, l, _s in visiveis)} em {len(visiveis)} mapas")
    for m, lista, sobrou in visiveis:
        print(f"  {m:20s} apaga {len(lista):2d}   fica de pe {sobrou:2d}   "
              + ", ".join(o.get("local_id", "?").replace("LOCALID_", "")
                          for _i, o in lista))
    print(f"NPC nativo JA escondido pela flag, a apagar: "
          f"{sum(len(l) for _m, l, _s in ja_ocultos)} em {len(ja_ocultos)} mapas")

    # Um mapa pode estar nas duas listas. Juntar por mapa é obrigatório: duas
    # passadas de escrita no mesmo `map.json` fariam a segunda ler índices que a
    # primeira já deslocou, e a guarda de identidade recusaria tudo caladamente.
    por_mapa = {}
    for m, lista, _s in visiveis + ja_ocultos:
        por_mapa.setdefault(m, []).extend(lista)
    aprovados = [(m, sorted(l, key=lambda x: x[0]), 0)
                 for m, l in sorted(por_mapa.items())]
    alvos = [(m, o.get("local_id"), o.get("script"))
             for m, lista, _s in aprovados for _i, o in lista]

    if recusas or rec_ocultos:
        print("\nmapas recusados (o NPC fica de pe):")
        for m, n, por in recusas + rec_ocultos:
            print(f"  {m:20s} {n:2d} nativo(s)   {por}")

    # Prova 3, a parte que não é do mapa: ninguém pode citar o local_id.
    citados = citados_fora(ignorados(aprovados))
    presos = [(m, li) for m, li, _s in alvos if li in citados]
    if presos:
        print("\nRECUSADOS por citacao em script (ficam de pe):", presos)

    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    apagados = renomeados = rotulos_fora = 0
    tocados = []
    mudancas_header = {}
    for meu, lista, _sobrou in aprovados:
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        # Releitura tardia: o disco manda. Outro agente pode ter mexido no mesmo
        # map.json entre o planejamento e agora, e apagar por índice velho apagaria
        # a pessoa errada.
        d = json.load(open(pm, encoding="utf-8"))
        antes = list(d.get("object_events") or [])
        fora = []
        for i, o in lista:
            if i >= len(antes) or identidade(antes[i]) != identidade(o) \
                    or o.get("local_id") in citados:
                continue
            fora.append(i)
        if not fora:
            continue
        alvo_objs = [antes[i] for i in fora]
        depois = [o for i, o in enumerate(antes) if i not in set(fora)]
        d["object_events"] = depois

        for o in alvo_objs:
            if o.get("local_id"):
                mudancas_header[o["local_id"]] = None
        for i, o in enumerate(depois):
            if o.get("local_id"):
                mudancas_header[o["local_id"]] = i + 1

        inc = le(ps) if os.path.exists(ps) else ""
        # Rótulo que um objeto SOBREVIVENTE ainda usa não pode sair: dois bonecos
        # podem compartilhar o mesmo script, e apagar o bloco deixaria o que ficou
        # apontando para símbolo inexistente.
        vivos = {o.get("script") for o in depois}
        rotulos = [o.get("script") for o in alvo_objs
                   if o.get("script") not in vivos]
        inc, tirados = limpa_scripts(inc, rotulos, textos_alheios(ps))
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(ps, "w", encoding="utf-8") as f:
            f.write(inc)
        apagados += len(fora)
        rotulos_fora += len(tirados)
        tocados += [pm, ps]

    # Sincronia de header: pede pelo estado do DISCO, não pelo plano. Assim uma
    # segunda rodada não escreve nada, e um define que outro agente tenha mexido no
    # meio do caminho volta ao valor que o mapjson vai gerar.
    do_disco = {}
    for p in glob.glob(os.path.join(REPO, "data/maps/*/map.json")):
        for i, o in enumerate(json.load(open(p, encoding="utf-8"))
                              .get("object_events") or []):
            if o.get("local_id"):
                do_disco[o["local_id"]] = i + 1
    do_disco.update({k: None for k, v in mudancas_header.items() if v is None})
    renumera_headers(do_disco, True)
    renomeados = sum(1 for v in mudancas_header.values() if v is not None)

    # Verificação na camada da afirmação, com o disco já escrito: o número do
    # header e o que o mapjson vai gerar têm que ser o mesmo, no repo inteiro.
    defs = defines_escritos_a_mao()
    erros = [f"{m}: {li} define={a} posicao={b}"
             for m, li, a, b in fora_de_sincronia()]
    for _meu, lista, _s in aprovados:
        for _i, o in lista:
            if o.get("local_id") in defs:
                erros.append(f"{o.get('local_id')}: apagado mas o define ficou")
    print(f"\napagados: {apagados}   rotulos de script/texto removidos: "
          f"{rotulos_fora}   constantes renumeradas: {renomeados}   "
          f"arquivos tocados: {len(set(tocados))}")
    print("erros de verificacao:", erros if erros else "nenhum")
    return 1 if erros else 0


def demo():
    """Uma armadilha por caso. As de dado são medidas na fonte, não lembradas."""
    # 1. o bloco removido vai do rótulo até a próxima linha na coluna zero, e leva
    #    a linha em branco junto: sobrar linha em branco empilha a cada remoção.
    A, TA, B = "Rt_EventScript_A", "Rt_Text_A", "Rt_EventScript_B"
    inc = (f"{A}::\n\tmsgbox {TA}, MSGBOX_NPC\n\tend\n\n"
           f"{TA}:\n\t.string \"oi$\"\n\n"
           f"{B}::\n\tend\n")
    sem_a, corpo = tira_bloco(inc, A)
    assert corpo.startswith(A + "::") and "msgbox" in corpo
    assert sem_a.startswith(TA + ":") and sem_a.endswith(f"{B}::\n\tend\n")
    assert tira_bloco(inc, "NAO_EXISTE") == (inc, None)

    # 2. o texto sai junto SÓ se mais ninguém citar. Citado em outro arquivo, fica.
    limpo, tirados = limpa_scripts(inc, [A], set())
    assert tirados == [A, TA] and limpo == f"{B}::\n\tend\n", (tirados, limpo)
    limpo2, tirados2 = limpa_scripts(inc, [A], {TA})
    assert tirados2 == [A] and TA + ":" in limpo2

    # 2b. e fica também quando o próprio arquivo ainda cita o texto noutro bloco.
    dois = inc.replace(f"{B}::\n\tend\n",
                       f"{B}::\n\tmsgbox {TA}, MSGBOX_NPC\n\tend\n")
    _l3, t3 = limpa_scripts(dois, [A], set())
    assert t3 == [A], "o texto saiu mesmo com outro bloco do arquivo citando"

    # 3. "só fala" é só msgbox. Dar item, andar ou pular para outro script não é
    #    falar, e quem faz isso não pode sumir.
    assert SO_FALA.match("\n\tmsgbox X, MSGBOX_NPC\n\tend")
    assert SO_FALA.match("\n\tlock\n\tfaceplayer\n\tmsgbox X, MSGBOX_DEFAULT"
                         "\n\trelease\n\tend")
    for perigoso in ("\n\tgiveitem ITEM_POTION\n\tend",
                     "\n\tmsgbox X, MSGBOX_NPC\n\tgiveitem ITEM_POTION\n\tend",
                     "\n\tgoto Outro\n\tend",
                     "\n\ttrainerbattle_single TRAINER_X, A, B\n\tend"):
        assert not SO_FALA.match(perigoso), perigoso

    # 4. a conta que o mapjson faz é posição + 1, e é ela que a renumeração tem que
    #    reproduzir. Medido no próprio conversor, não lembrado.
    fonte = le(os.path.join(REPO, "tools/mapjson/mapjson.cpp"))
    assert 'json_to_string(obj_event, "local_id") << " " << i + 1' in fonte, \
        "o mapjson deixou de derivar o local_id da posicao; a renumeracao mudou"

    # 5. estado do repo ANTES de qualquer edição: todo define escrito à mão já bate
    #    com a posição do objeto. Se essa linha de base estivesse quebrada, a
    #    verificação do fim acusaria erro que não foi esta ferramenta que criou.
    defs = defines_escritos_a_mao()
    fora = []
    for p in glob.glob(os.path.join(REPO, "data/maps/*/map.json")):
        for i, o in enumerate(json.load(open(p, encoding="utf-8"))
                              .get("object_events") or []):
            li = o.get("local_id")
            if li in defs and defs[li][1] != i + 1:
                fora.append((os.path.basename(os.path.dirname(p)), li))
    assert not fora, f"define fora de sincronia ANTES de editar: {fora[:5]}"

    # 6. a verificação pega o deslocamento que é o risco inteiro deste bloco: se o
    #    define não acompanhar a remoção, `confere` tem que reprovar.
    antes = [{"graphics_id": "A", "x": 1, "y": 1, "local_id": "LOCALID_X"},
             {"graphics_id": "B", "x": 2, "y": 2, "local_id": "LOCALID_Y"}]
    depois = [antes[1]]
    assert confere(antes, depois, [antes[0]], {"LOCALID_Y": ("f", 1)}) == []
    ruim = confere(antes, depois, [antes[0]], {"LOCALID_Y": ("f", 2)})
    assert ruim and "define diz 2" in ruim[0], "o deslocamento passou batido"
    assert confere(antes, depois, [antes[0]],
                   {"LOCALID_Y": ("f", 1), "LOCALID_X": ("f", 9)}), \
        "define de quem morreu ficou e a verificacao nao viu"

    # 7. prova 1 na fonte: Route220 tem SETE pessoas no Platinum e as sete são
    #    treinador. Os três nativos `Swimmer<nome>` que só falam não têm oitava
    #    pessoa para ser, e os sete treinadores são batalhados por outros bonecos.
    ev = json.load(open(os.path.join(
        PLAT, "res/field/events/events_route_220.json"), encoding="utf-8"))
    gente, _ = T.separa_fonte(ev)
    assert len(gente) == 7 and all(
        str(o.get("script", "")).startswith("TRAINER_") for o in gente)
    inc220 = le(os.path.join(REPO, "data/maps/Route220/scripts.inc"))
    for o in gente:
        nossa = "TRAINER_SINNOH_" + o["script"][len("TRAINER_"):]
        assert re.search(rf"trainerbattle\w*\s+{nossa}\b", inc220), nossa

    # 8. a inversão só vale para par que a FONTE prova, e a prova de cada um mora
    #    lá, não na memória: o Youngster da Route 204 é mudo no Platinum
    #    (`script: 0`, que não é índice de script nenhum), e o Fisherman da
    #    Route 209 é o doador da Good Rod, não um NPC de conversa. Se qualquer um
    #    dos dois deixar de ser assim, a inversão perde o motivo escrito na tabela.
    arqs = {m: a for m, _h, a in T.casados()}
    gente204, _ = T.separa_fonte(json.load(open(os.path.join(
        PLAT, "res/field/events", arqs["Route204"] + ".json"), encoding="utf-8")))
    assert gente204[4].get("script") == 0, \
        "a pessoa #4 da Route204 deixou de ser muda na fonte"
    _ordem, corpos = T.entradas_de_script("scripts_route_209")
    corpo = " ".join(corpos["Route209_Fisherman"])
    assert "ITEM_GOOD_ROD" in corpo and "FLAG_RECEIVED_GOOD_ROD" in corpo, \
        "o pescador da Route209 deixou de ser o doador da Good Rod"

    # 8b. a inversão é idempotente e nunca adivinha: com a flag já removida não
    #     repete, e com o objeto fora do estado esperado recusa. Aqui só simula.
    _feitos, recusados_inv = aplica_inversoes(False)
    assert not recusados_inv, recusados_inv

    # 8c. o mapa que continua sem fechar fica de fora inteiro.
    aprovados, recusas = plano()
    recusados = {m for m, _n, _p in recusas}
    assert "Route205_North" in recusados, \
        "Route205_North tem 4 pessoas na fonte contra 3 importados e passou"
    assert not [m for m, _l, _s in aprovados if m in recusados]

    # 9. nenhum candidato pode ser citado por script, código ou heal_locations.
    citados = citados_fora(ignorados(aprovados))
    presos = [o.get("local_id") for _m, lista, _s in aprovados for _i, o in lista
              if o.get("local_id") in citados]
    assert not presos, f"local_id a apagar mas citado por script: {presos}"

    # 10. e nenhum é NPC de sistema disfarçado: o corpo é msgbox, então não vende,
    #     não cura e não embarca ninguém. Quem faz isso já reprovou na prova 3.
    for _m, lista, _s in aprovados:
        for _i, o in lista:
            assert o.get("local_id") not in EXCECOES

    # 11. nenhum candidato divide o rótulo de script com um boneco que fica: se
    #     dividisse, apagar o bloco deixaria o sobrevivente apontando para símbolo
    #     que não existe mais. Medido, e o `main` recusa o rótulo mesmo assim.
    for m, lista, _s in aprovados:
        objs = json.load(open(os.path.join(REPO, "data/maps", m, "map.json"),
                              encoding="utf-8"))["object_events"]
        # Identidade, não `id()`: o JSON foi lido de novo e os objetos são outros
        # dicionários com o mesmo conteúdo.
        ids_mortos = {identidade(o) for _i, o in lista}
        vivos = {o.get("script") for o in objs
                 if identidade(o) not in ids_mortos}
        compartilhados = [o.get("script") for _i, o in lista
                          if o.get("script") in vivos]
        assert not compartilhados, f"{m}: rotulo compartilhado {compartilhados}"

    # 12. a guarda de macro separa id NUMERICO de constante nomeada: a nomeada o
    #     mapjson regera da posicao e acompanha o boneco, o numero cravado nao.
    #     Confundir os dois recusaria mapa que nao tem risco (JubilifeCity usa
    #     `removeobject LOCALID_JUBILIFE_ROWAN`) ou, pior, aprovaria um que tem.
    assert MACRO_DE_OBJETO.search("\tapplymovement 3, Foo\n")
    assert MACRO_DE_OBJETO.search("\tremoveobject 12\n")
    assert not MACRO_DE_OBJETO.search("\tremoveobject LOCALID_X\n")
    assert not MACRO_DE_OBJETO.search("\tapplymovement LOCALID_PLAYER, Foo\n")

    # 13. a varredura dos ja escondidos NUNCA pega importado: o corpo dele e gente
    #     da fonte, e apagar apagaria conteudo do Platinum.
    ocultos, _rec = escondidos_nativos()
    assert not [o for _m, l, _s in ocultos for _i, o in l
                if o.get("origem") == "pokeplatinum"]
    citados_o = citados_fora(ignorados(ocultos))
    presos_o = [o.get("local_id") for _m, l, _s in ocultos for _i, o in l
                if o.get("local_id") in citados_o]
    assert not presos_o, f"escondido a apagar mas citado por script: {presos_o}"

    print(f"demo ok (14 casos; {sum(len(l) for _m, l, _s in aprovados)} NPC "
          f"aprovado em {len(aprovados)} mapas, {len(recusas)} mapa(s) recusado)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
