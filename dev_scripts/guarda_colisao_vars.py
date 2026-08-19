#!/usr/bin/env python3
"""Portão de colisão de vars: dois donos diferentes no mesmo endereço.

O caso que mordeu (J4 da onda de janela aberta, 18/08/2026): as vars de cena
de Kanto em `include/constants/vars_frlg.h` não têm guarda nenhuma e caíam em
cima de vars de Hoenn de `include/constants/vars.h`. Três foram realiasadas
para 0x40F7-0x40F9 no commit a5dc22e600; o que faltava era o portão que
impede colisão NOVA de entrar calada.

Como ele prova (lição 4.6 do ESTADO): quem resolve o valor é o
PRÉ-PROCESSADOR, não o texto do define. `VAR_SINNOH_X` definida como
`VAR_UNUSED_0x4130` devolve a si mesma no texto e só o cpp entrega 0x4130.

Como ele evita falso positivo (lição 4.3): a regra larga "dois nomes, mesmo
valor" acusa 307 grupos nesta árvore, quase todos legítimos, porque
`vars_frlg.h` inteiro é uma releitura do MESMO espaço de 0x40xx. A regra usada
aqui exige as três coisas juntas:

  1. o nome é DONO do endereço. Dono é quase todo mundo: corpo numérico, corpo
     de base mais deslocamento (`(FLAG_ITEM_BALLS_JSU_START + 0x00A)`) e
     também APELIDO, porque neste projeto apelidar é como se ALOCA
     (`#define VAR_MINHA VAR_UNUSED_0x41C3`, o jeito de Johto, Sinnoh, Unova e
     Galar). O único nome que deixa de ser dono é o RÓTULO DO POOL
     (`VAR_UNUSED_0x41C3`, `FLAG_UNUSED_0x1CFF`) depois que um apelido o tomou
     para si: a vaga passou a ter dono com nome, e contar os dois seria
     acusar toda alocação legítima do repo;
  2. os dois nomes são REFERENCIADOS na árvore (data/, src/, include/,
     test/). Nome que ninguém usa não briga com ninguém;
  3. o par não está na lista de autorizados (`colisoes_vars_autorizadas.json`,
     gerada por `--gravar`, com dono e data).

**BURACO H, medido pelo adversarial da onda em 18/08/2026 e tapado no J9**: até
ali, corpo que citava outro nome era descartado como "apelido declarado", e
apelidar `*_UNUSED_*` é EXATAMENTE como este projeto aloca. Ou seja, a forma
mais comum de alocar era a única que o portão não enxergava, e duas frentes
apelidando o mesmo `VAR_UNUSED_*` devolviam a colisão calada que ele existe
para impedir. Junto vieram os irmãos (também plantados no `--demo`): apelido
para nome VIVO, apelido de apelido, e `#define` em ramo morto de `#ifndef`,
em que o cpp entrega um número e o leitor guardava o corpo do outro ramo.

O MESMO portão vale para FLAGS desde o J7 (18/08/2026), com `--flags`. O nome
do arquivo ficou (renomear quebraria ESTADO.md e o caso da suíte); o que mudou
é que os endereços vêm de um PERFIL, não de constantes cravadas. Uma coisa teve
que ser diferente no perfil de flags, e ela foi medida:

- **ordem dos headers = ordem do include.** `flags.h` inclui `flags_frlg.h` na
  linha 50 e depois REDEFINE nomes dele (`FLAG_HIDE_ARTICUNO` é 0x082 no frlg e
  `FLAG_UNUSED_0x020` no flags.h). Quem lê os dois headers tem que terminar pelo
  que o cpp deixa valer, senão grava o corpo de um e o valor do outro, e inventa
  colisão que não existe. Foi exatamente o falso positivo de 0x20.

A regra de apelido, essa, passou a ser a MESMA nos dois perfis no J9: não existe
mais corpo que dê passe livre.

Uso:
  python3 dev_scripts/guarda_colisao_vars.py           # portão (vars)
  python3 dev_scripts/guarda_colisao_vars.py --flags   # portão (flags)
  python3 dev_scripts/guarda_colisao_vars.py --lista   # mostra as herdadas
  python3 dev_scripts/guarda_colisao_vars.py --gravar  # regrava a autorizada
  python3 dev_scripts/guarda_colisao_vars.py --demo    # autoteste de mutação

Qualquer um dos três aceita `--flags` junto, e cada perfil tem a sua lista de
autorizadas.
"""

import collections
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZES_DE_USO = ["data", "src", "include", "test"]
EXTENSOES = (".c", ".h", ".inc", ".json", ".s", ".pory")

# Perfis. `headers` vai na ORDEM DO INCLUDE (o último é o que o cpp deixa
# valer), `ponta` é o header que puxa o outro, `plante` é um endereço com
# exatamente UM dono próprio e usado, onde o autoteste finge o segundo dono.
#
# `include/config/*.h` entra na leva de encerramento (19/08/2026). Ele estava
# FORA do alcance e escondia dois nomes que o motor trata como endereço:
# `FLAG_TEXT_SPEED_INSTANT` (include/config/text.h) e `VAR_LAST_REPEL_LURE_USED`
# (include/config/item.h). Nenhum dos dois é alcançável a partir da ponta
# antiga: medido com o próprio cpp, `#include "constants/flags.h"` deixa
# `FLAG_TEXT_SPEED_INSTANT` sem expandir, e `constants/vars.h` faz o mesmo com
# `VAR_LAST_REPEL_LURE_USED`. Por isso `ponta` virou LISTA: o segundo include é
# quem puxa o header de config (`text.h` puxa `config/text.h`,
# `constants/global.h` puxa `config/item.h`), e a ordem continua sendo a do
# include de verdade, que é a regra que já custou o falso positivo de 0x20.
PERFIS = {
    "vars": dict(
        prefixo="VAR",
        headers=["include/constants/vars.h", "include/constants/vars_frlg.h",
                 "include/config/item.h"],
        ponta=["constants/vars.h", "constants/global.h"],
        autorizadas="colisoes_vars_autorizadas.json",
        plante=0x4060,
    ),
    "flags": dict(
        prefixo="FLAG",
        headers=["include/constants/flags_frlg.h", "include/constants/flags.h",
                 "include/config/text.h"],
        ponta=["constants/flags.h", "text.h"],
        autorizadas="colisoes_flags_autorizadas.json",
        # 0x0001 é FLAG_TEMP_1, dono próprio citado em 13 arquivos em
        # 18/08/2026. Quem fabrica o SEGUNDO dono é o plante.
        plante=0x0001,
    ),
}
PERFIL = "vars"


def usa(perfil):
    """Troca o perfil ativo. Tudo que varia entre vars e flags mora aqui."""
    global PERFIL, HEADERS, PONTA, AUTORIZADAS, PLANTE
    global DEF, APELIDO, POOL, TOKEN, SONDA, PREFIXO
    PERFIL = perfil
    p = PERFIS[perfil]
    PREFIXO = p["prefixo"]
    HEADERS = p["headers"]
    PONTA = p["ponta"]
    AUTORIZADAS = os.path.join(RAIZ, "dev_scripts", p["autorizadas"])
    PLANTE = p["plante"]
    DEF = re.compile(r"^\s*#define\s+(%s_[A-Za-z0-9_]+)[ \t]+(.*)$" % PREFIXO, re.M)
    APELIDO = re.compile(r"^\(*\s*(%s_[A-Za-z0-9_]+)\s*\)*$" % PREFIXO)
    POOL = re.compile(r"^%s_UNUSED" % PREFIXO)
    TOKEN = re.compile((r"%s_[A-Za-z0-9_]+" % PREFIXO).encode())
    SONDA = re.compile(r'^@@ "(%s_\w+)" @@ (.*)$' % PREFIXO)


usa("vars")


def le_defines(caminhos):
    """nome -> (header do último define, LISTA de todos os corpos).

    A lista, e não o último corpo, porque o mesmo nome pode ser definido duas
    vezes com corpos diferentes, e só o cpp sabe qual vale. Guardar um corpo só
    era o buraco E2 do adversarial de 18/08/2026:

        #ifndef FLAG_X
        #define FLAG_X 0x4400      <- é este que o cpp entrega
        #else
        #define FLAG_X FLAG_UNUSED_0x1D01
        #endif

    O leitor ficava com o corpo do ramo MORTO e concluía "apelido", enquanto o
    valor de verdade vinha do ramo vivo.
    """
    fora = {}
    for c in caminhos:
        texto = open(c, encoding="utf-8", errors="replace").read()
        for m in DEF.finditer(texto):
            corpo = m.group(2).split("//")[0].split("/*")[0].strip()
            corpos = fora.get(m.group(1), (None, []))[1]
            fora[m.group(1)] = (os.path.basename(c), corpos + [corpo])
    return fora


def pool_reclamado(defs, valores):
    """Rótulos `PREFIXO_UNUSED_*` que um apelido tomou para si.

    Apelidar uma vaga do pool é como este repo ALOCA endereço, e depois disso a
    vaga tem dono com nome: contar o rótulo do pool junto acusaria toda
    alocação legítima (foi o falso positivo medido em 0x20, 0x30, 0x1CFF e
    0x2030 quando o J9 desmanchou a regra de apelido).

    A exigência é uma só, e é MEDIÇÃO e não confiança no texto: o VALOR que o
    cpp entrega para o apelido tem que ser o mesmo do alvo. Com isso:

      - `FLAG_HIDE_ARTICUNO` (0x082 em flags_frlg.h, redefinida como
        `FLAG_UNUSED_0x020` em flags.h) reclama a vaga, porque o cpp entrega
        0x20 para ela e para o rótulo. Sem a conferência de valor essa linha
        virava o falso positivo de 0x20 que o J7 já tinha medido;
      - o `#define X PREFIXO_UNUSED_0xNNN` escondido no ramo MORTO de um
        `#ifndef` (buraco E2) NÃO reclama nada, porque o cpp entregou para X o
        número do ramo vivo, que é outro. O ramo morto deixa de ser disfarce.
    """
    fora = set()
    for nome, (_, corpos) in defs.items():
        valor = valores.get(nome)
        if valor is None:
            continue
        for corpo in corpos:
            m = APELIDO.match(corpo)
            if m and POOL.match(m.group(1)) and valores.get(m.group(1)) == valor:
                fora.add(m.group(1))
    return fora


def compilador():
    for cc in ("cc", "gcc", "clang"):
        if shutil.which(cc):
            return cc
    raise SystemExit("nenhum pré-processador C no PATH (cc, gcc, clang)")


def resolve(nomes, inc_dir):
    """Valor que o PRÉ-PROCESSADOR entrega para cada nome.

    O nome vai entre aspas na sonda de propósito: string não é expandida,
    então a etiqueta sobrevive e só o lado direito vira número.
    """
    fonte = "".join('#include "%s"\n' % h for h in PONTA)
    fonte += "".join('@@ "%s" @@ %s\n' % (n, n) for n in nomes)
    # O include real entra DEPOIS do inc_dir de propósito: na árvore de mentira
    # do autoteste só os headers do perfil são copiados, e `flags.h` puxa
    # `constants/trainers.h` e companhia, que não estão lá. Primeiro ganha o
    # header mutado; o resto vem do repo.
    saida = subprocess.run(
        [compilador(), "-E", "-P", "-I", inc_dir,
         "-I", os.path.join(RAIZ, "include"), "-x", "c", "-"],
        input=fonte, capture_output=True, text=True,
    )
    if saida.returncode != 0:
        raise SystemExit("pré-processador reprovou:\n" + saida.stderr[:2000])
    valores = {}
    for linha in saida.stdout.splitlines():
        m = SONDA.match(linha.strip())
        if not m:
            continue
        try:
            valores[m.group(1)] = eval(m.group(2).strip(), {"__builtins__": {}}, {})
        except Exception:
            pass  # define sem valor inteiro não entra na conta de endereço
    return valores


def indice_de_uso(base, raizes, ignorar):
    """nome -> número de arquivos que citam o nome (fora dos headers de define)."""
    uso = collections.Counter()
    ignorar = {os.path.normpath(os.path.join(base, p)) for p in ignorar}
    for r in raizes:
        for dp, _, fn in os.walk(os.path.join(base, r)):
            for f in fn:
                p = os.path.join(dp, f)
                if os.path.normpath(p) in ignorar or not f.endswith(EXTENSOES):
                    continue
                try:
                    b = open(p, "rb").read()
                except OSError:
                    continue
                for m in set(TOKEN.findall(b)):
                    uso[m.decode()] += 1
    return uso


def colisoes(base, headers, raizes):
    """Grupos de 2+ nomes DONOS e USADOS no mesmo endereço."""
    caminhos = [os.path.join(base, h) for h in headers]
    defs = le_defines(caminhos)
    valores = resolve(sorted(defs), os.path.join(base, "include"))
    uso = indice_de_uso(base, raizes, headers)
    tomados = pool_reclamado(defs, valores)
    por_valor = collections.defaultdict(list)
    for nome, valor in valores.items():
        if nome in tomados:
            continue  # rótulo do pool que um apelido tomou: não é dono
        if not uso.get(nome):
            continue  # ninguém usa: não briga com ninguém
        por_valor[valor].append(nome)
    fora = []
    for valor, nomes in sorted(por_valor.items()):
        if len(nomes) > 1:
            fora.append({
                "endereco": hex(valor),
                "nomes": sorted(nomes),
                "onde": {n: defs[n][0] for n in sorted(nomes)},
                "arquivos_que_usam": {n: uso[n] for n in sorted(nomes)},
            })
    return fora


# O portão de colisão só enxerga endereço com DOIS donos usados. Um stub que
# inventa endereço AINDA LIVRE passa calado por ele, e foi assim que o import de
# Johto deixou `#ifndef FLAG_NIGHT_POKEMON / #define FLAG_NIGHT_POKEMON 0x4000`
# vivo (J8, 18/08/2026): quem escreve `#ifndef` está dizendo "se o de verdade
# não existir, invente um", que é exatamente a receita de endereço fantasma. A
# única forma legítima de `#ifndef` nestes headers é a guarda do próprio
# arquivo, e ela nunca começa com o prefixo do perfil.
#
# Duas fugas medidas pelo adversarial em 18/08/2026, e as duas eram do REGEX,
# não do desenho: comentário na mesma linha (`#ifndef FLAG_STUB // por quê`) e a
# forma equivalente `#if !defined(FLAG_STUB)`. As duas passavam batidas e vêm
# plantadas no `--demo` desde o J9.
IFNDEF = (r"^\s*#\s*(?:ifndef\s+(?P<a>%(p)s_[A-Za-z0-9_]+)"
          r"|if\s+!\s*defined\s*\(?\s*(?P<b>%(p)s_[A-Za-z0-9_]+)\s*\)?)"
          r"\s*(?://.*|/\*.*)?$")


def stubs(base=RAIZ, headers=None, verboso=True):
    """Linhas `#ifndef PREFIXO_X` nos headers do perfil. Devia ser zero."""
    padrao = re.compile(IFNDEF % {"p": PREFIXO})
    fora = []
    for h in headers or HEADERS:
        caminho = os.path.join(base, h)
        if not os.path.exists(caminho):
            continue
        for n, linha in enumerate(open(caminho, encoding="utf-8",
                                       errors="replace"), 1):
            m = padrao.match(linha)
            if m:
                fora.append((h, n, m.group("a") or m.group("b")))
    if verboso:
        print("stubs `#ifndef %s_` medidos: %d (o certo é 0)"
              % (PREFIXO, len(fora)))
        for h, n, nome in fora:
            print("  REPROVA %s:%d  #ifndef %s" % (h, n, nome))
            print("    `#ifndef` inventa endereço quando o símbolo de verdade "
                  "não existe. Declare o nome com endereço próprio no header.")
    return fora


def chave(grupo):
    return grupo["endereco"] + " " + " ".join(grupo["nomes"])


def le_autorizadas(caminho):
    if not os.path.exists(caminho):
        return {}
    dados = json.load(open(caminho, encoding="utf-8"))
    return {chave(g): g for g in dados.get("herdadas", []) + dados.get("realias", [])}


def portao(base=RAIZ, headers=None, raizes=None, caminho_autorizadas=None,
           verboso=True):
    achadas = colisoes(base, headers or HEADERS, raizes or RAIZES_DE_USO)
    autorizadas = le_autorizadas(caminho_autorizadas or AUTORIZADAS)
    novas = [g for g in achadas if chave(g) not in autorizadas]
    herdadas = len(achadas) - len(novas)
    if verboso:
        print("colisões medidas: %d (herdadas e declaradas: %d, novas: %d)"
              % (len(achadas), herdadas, len(novas)))
        for g in novas:
            print("  REPROVA %s" % g["endereco"])
            for n in g["nomes"]:
                print("    %-70s %s, em %d arquivo(s)"
                      % (n, g["onde"][n], g["arquivos_que_usam"][n]))
    return novas


# Dono e motivo POR LINHA, escritos por quem mediu. O que não estiver aqui cai
# no texto genérico, que é o sinal de que ninguém olhou aquela linha ainda.

# Os apelidos de rascunho do pokeemerald de fábrica. Eles apareceram no J9,
# quando a regra de apelido caiu (buraco H): `#define FLAG_TEMP_REGICE_PUZZLE_
# STARTED FLAG_TEMP_2` é upstream dando NOME a uma vaga de rascunho, e a vaga é
# reusada de propósito por cena que nunca roda junto. É desenho, e desenho
# declarado é o certo: o dia em que uma cena NOVA apelidar um TEMP já apelidado,
# o portão acusa, porque o grupo autorizado é o par exato de endereço + nomes.
# Vale o aviso do ESTADO 0.f: `P_FLAG_FORCE_SHINY` aponta para `FLAG_TEMP_7`, e
# essa mora em `include/config/`, fora do alcance deste portão (ver a fila).
_RASCUNHO = ("pokeemerald de fábrica (apelido de vaga de rascunho)",
             "DESENHO, não defeito: upstream dá um nome legível a uma vaga "
             "TEMP e reusa a mesma vaga em cenas que não rodam juntas. "
             "Declarado para o portão não repetir a linha, e para que apelido "
             "NOVO em cima da mesma vaga volte a reprovar")

MOTIVOS = {
    "vars": {k: _RASCUNHO for k in ("0x4000", "0x4001", "0x400d", "0x400e")},
    "flags": {
        **{k: _RASCUNHO for k in ("0x1", "0x2", "0x3", "0x11")},
        "0x1f4": (
            "pokeemerald de fábrica (include/constants/flags.h:569)",
            "DESENHO, não defeito: FLAG_HIDDEN_ITEMS_START é o MARCADOR da "
            "faixa e vale o mesmo que o primeiro item dela "
            "(FLAG_HIDDEN_ITEM_LAVARIDGE_TOWN_ICE_HEAL = START + 0x00). "
            "Marcador de faixa não é dono de flag, e o par nasce assim no "
            "upstream. Só entra na lista para o portão não repetir a linha"),
        # 0x4000 e 0x4001 SAIRAM em 18/08/2026 (J8): eram o stub do import de
        # Johto em cima de FLAG_HIDE_MAP_NAME_POPUP e
        # FLAG_DONT_TRANSITION_MUSIC. FLAG_NIGHT_POKEMON e FLAG_DAY_POKEMON
        # ganharam endereço próprio (0x1D01 e 0x1D02, transbordo de Johto) e o
        # `#ifndef` morreu. Colisão que deixou de existir não fica declarada.
    },
}


def grava(base=RAIZ, caminho=None):
    caminho = caminho or AUTORIZADAS
    achadas = colisoes(base, HEADERS, RAIZES_DE_USO)
    for g in achadas:
        dono, motivo = MOTIVOS[PERFIL].get(g["endereco"], (
            "herança do merge de FRLG, medida em 18/08/2026",
            "colisão que já existia antes do portão; não consertada "
            "nesta onda, esperando decisão do condutor"))
        g["dono"] = dono
        g["motivo"] = motivo
    # Chave que este gerador não conhece é texto escrito à mão por quem mediu
    # ("historia", "ressalva_das_utilitarias"): ela SOBREVIVE ao --gravar. Sem
    # isto, regravar a lista apagava calada a história do J6, que é a única
    # explicação de por que 19 endereços saíram dela.
    antigo = {}
    if os.path.exists(caminho):
        antigo = {k: v for k, v in json.load(open(caminho, encoding="utf-8")).items()
                  if k not in ("medido_em", "perfil", "regra", "realias", "herdadas")}
    json.dump({"medido_em": "2026-08-18",
               "perfil": PERFIL,
               "regra": "grupo autorizado é par exato de endereço + nomes",
               **antigo,
               "realias": [],
               "herdadas": achadas},
              open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("gravadas %d colisões herdadas em %s" % (len(achadas), caminho))


def demo():
    """Autoteste com mutação plantada, em árvore de mentira e descartável.

    Roda no perfil ATIVO: `--demo` sozinho testa vars, `--demo --flags` testa
    flags. Os nomes plantados e o endereço do passo 6 vêm do perfil, porque um
    endereço cravado seria mentira no outro dialeto.
    """
    P = PREFIXO
    # Onde a mutação é plantada: o header PRINCIPAL do perfil, que é o primeiro
    # include da ponta.
    ponta = os.path.basename(PONTA[0])

    def copia_headers(tmp):
        """Headers do perfil E os da ponta, com o CAMINHO preservado.

        Duas coisas que a versão achatada em `constants/` não fazia, e as duas
        nasceram em 19/08/2026 com `include/config/*.h` entrando no perfil:

        1. caminho preservado, senão o header de config nem existe na árvore de
           mentira e o passo 7 não prova alcance nenhum;
        2. os headers da PONTA junto. `#include "config/text.h"` dentro de
           `include/text.h` é ASPAS, e aspas resolvem primeiro no diretório do
           arquivo que inclui: sem uma cópia de `text.h` aqui dentro, o cpp
           pegava `config/text.h` do repo de VERDADE e a mutação plantada na
           cópia ficava invisível (medido: o plante em config/text.h passava
           calado enquanto o de config/item.h reprovava, porque
           `constants/global.h` mora um diretório abaixo e cai no -I).
        """
        for h in list(HEADERS) + [os.path.join("include", p) for p in PONTA]:
            destino = os.path.join(tmp, h)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            if not os.path.exists(destino):
                shutil.copy(os.path.join(RAIZ, h), destino)

    with tempfile.TemporaryDirectory() as tmp:
        inc = os.path.join(tmp, "include", "constants")
        os.makedirs(inc)
        os.makedirs(os.path.join(tmp, "data"))
        copia_headers(tmp)
        aut = os.path.join(tmp, "autorizadas.json")
        json.dump({"realias": [], "herdadas": []}, open(aut, "w"))

        def planta(*linhas):
            with open(os.path.join(inc, ponta), "r+", encoding="utf-8") as f:
                texto = f.read()
                corte = texto.rindex("#endif")
                f.seek(0)
                f.write(texto[:corte] + "".join(linhas) + texto[corte:])
                f.truncate()

        def roda():
            return portao(base=tmp, raizes=["data"], caminho_autorizadas=aut,
                          verboso=False)

        # 1. sem plante: verde (nenhum arquivo de uso na árvore de mentira)
        assert roda() == [], "árvore limpa devia estar verde"

        # 2. mutação plantada: dois nomes PRÓPRIOS no mesmo 0x4210, ambos usados,
        #    mais um APELIDO de um deles. O apelido de nome VIVO entra no grupo
        #    (buraco A do adversarial de 18/08/2026): até o J9 o regex aceitava
        #    apelido de QUALQUER nome e descartava os dois, contradizendo o
        #    próprio docstring, e com isso `#define X FLAG_BADGE01_GET` escondia
        #    que a insígnia passara a ter dois usuários vivos.
        planta("#define %s_PLANTADA_A 0x4210\n" % P,
               "#define %s_PLANTADA_B 0x4210\n" % P,
               "#define %s_PLANTADA_APELIDO %s_PLANTADA_A\n" % (P, P))
        usos = os.path.join(tmp, "data", "plante.inc")
        open(usos, "w").write("%s_PLANTADA_A %s_PLANTADA_B %s_PLANTADA_APELIDO\n"
                              % (P, P, P))
        vermelho = roda()
        assert len(vermelho) == 1, "o plante devia acusar 1 grupo, deu %r" % vermelho
        assert vermelho[0]["endereco"] == "0x4210"
        assert vermelho[0]["nomes"] == ["%s_PLANTADA_A" % P, "%s_PLANTADA_APELIDO" % P,
                                        "%s_PLANTADA_B" % P], \
            "apelido de nome VIVO tinha que entrar: %r" % vermelho[0]["nomes"]

        # 3. o mesmo plante, agora declarado como autorizado: volta ao verde
        json.dump({"realias": [vermelho[0]], "herdadas": []}, open(aut, "w"))
        assert roda() == [], "colisão declarada não podia reprovar"

        # 4. nome novo no MESMO endereço já declarado: reprova de novo
        open(usos, "a").write("%s_PLANTADA_C\n" % P)
        planta("#define %s_PLANTADA_C 0x4210\n" % P)
        assert len(roda()) == 1, "terceiro nome no endereço declarado devia reprovar"

        # 5. tirando o plante inteiro: verde de novo
        os.remove(usos)
        assert roda() == [], "sem o plante devia voltar ao verde"

        # 5a. o stub de `#ifndef`, que é a segunda doença e a que o portão de
        #     colisão NÃO pega sozinho: endereço inventado ainda livre não tem
        #     segundo dono para brigar. Sem este passo, o conserto do J8 seria
        #     só do caso, não da classe.
        def stubs_aqui():
            return stubs(base=tmp, headers=[os.path.join("include", "constants",
                                                         ponta)], verboso=False)

        assert stubs_aqui() == [], "árvore limpa não podia ter stub"
        planta("#ifndef %s_STUB_PLANTADA\n" % P,
               "#define %s_STUB_PLANTADA 0x4400\n" % P,
               "#endif\n")
        pego = stubs_aqui()
        assert len(pego) == 1 and pego[0][2] == "%s_STUB_PLANTADA" % P, \
            "o `#ifndef` plantado tinha que reprovar: %r" % pego

        # 5a-C e 5a-D: as duas fugas de REGEX que o adversarial fabricou em
        #     18/08/2026. Comentário na mesma linha e a forma equivalente
        #     `#if !defined(...)` passavam batidas, e a doença é a mesma:
        #     "se o de verdade não existir, invente um".
        planta("#ifndef %s_STUB_COMENTADA // vem do import, some depois\n" % P,
               "#define %s_STUB_COMENTADA 0x4401\n" % P,
               "#endif\n",
               "#if !defined(%s_STUB_DEFINED)\n" % P,
               "#define %s_STUB_DEFINED 0x4402\n" % P,
               "#endif\n")
        pego = {n for _, _, n in stubs_aqui()}
        assert pego == {"%s_STUB_PLANTADA" % P, "%s_STUB_COMENTADA" % P,
                        "%s_STUB_DEFINED" % P}, \
            "as três formas de stub tinham que reprovar: %r" % pego

        # 5b. Expressão de base mais deslocamento é dono PRÓPRIO, não apelido.
        #     Sem isto, a faixa gerada das item balls ficaria invisível para o
        #     portão, que é o defeito que ele existe para pegar.
        planta("#define %s_BASE_PLANTADA 0x4300\n" % P,
               "#define %s_PLANTADA_E (%s_BASE_PLANTADA + 0x1)\n" % (P, P),
               "#define %s_PLANTADA_F (%s_BASE_PLANTADA + 0x1)\n" % (P, P))
        open(usos, "w").write("%s_PLANTADA_E %s_PLANTADA_F\n" % (P, P))
        base = roda()
        assert len(base) == 1 and base[0]["endereco"] == "0x4301", \
            "duas faixas geradas no mesmo endereço tinham que reprovar: %r" % base
        os.remove(usos)
        assert roda() == [], "sem o plante devia voltar ao verde"

        # 5c. BURACO H, o grave, e o motivo do J9. Apelidar uma vaga do pool é
        #     COMO ESTE REPO ALOCA (Johto, Sinnoh, Unova e Galar fazem assim),
        #     e até aqui era a única forma de alocar que o portão não enxergava:
        #     duas frentes apelidando a MESMA vaga voltavam a ser colisão calada.
        planta("#define %s_UNUSED_0x4500 0x4500\n" % P,
               "#define %s_FRENTE_UM %s_UNUSED_0x4500\n" % (P, P),
               "#define %s_FRENTE_DOIS %s_UNUSED_0x4500\n" % (P, P))
        open(usos, "w").write("%s_FRENTE_UM %s_FRENTE_DOIS\n" % (P, P))
        h = roda()
        assert len(h) == 1 and h[0]["endereco"] == "0x4500" \
            and h[0]["nomes"] == ["%s_FRENTE_DOIS" % P, "%s_FRENTE_UM" % P], \
            "duas alocações na mesma vaga do pool tinham que reprovar: %r" % h

        # 5c-negativo: UMA alocação, com o rótulo do pool citado na árvore. O
        #     rótulo tomado NÃO é segundo dono, senão o portão acusaria toda
        #     alocação legítima. Foi este passo que fixou os falsos positivos
        #     medidos em 0x20, 0x30, 0x1CFF e 0x2030.
        open(usos, "w").write("%s_FRENTE_UM %s_UNUSED_0x4500\n" % (P, P))
        assert roda() == [], "alocação sozinha não podia brigar com o rótulo do pool"

        # 5d. Apelido de apelido (buraco B): a cadeia não pode virar disfarce.
        planta("#define %s_UNUSED_0x4501 0x4501\n" % P,
               "#define %s_FRENTE_TRES %s_UNUSED_0x4501\n" % (P, P),
               "#define %s_FRENTE_QUATRO %s_FRENTE_TRES\n" % (P, P))
        open(usos, "w").write("%s_FRENTE_TRES %s_FRENTE_QUATRO\n" % (P, P))
        b = roda()
        assert len(b) == 1 and b[0]["endereco"] == "0x4501" \
            and b[0]["nomes"] == ["%s_FRENTE_QUATRO" % P, "%s_FRENTE_TRES" % P], \
            "apelido de apelido tinha que reprovar: %r" % b

        # 5e. Buraco E2: dois `#define` para o mesmo nome, o cpp entrega o
        #     NÚMERO do ramo vivo e o leitor guardava o corpo do ramo MORTO.
        #     Com um corpo só, o nome era descartado como apelido E ainda
        #     desalojava o rótulo do pool que o ramo morto citava.
        planta("#ifndef %s_DOIS_CORPOS\n" % P,
               "#define %s_DOIS_CORPOS 0x4502\n" % P,
               "#else\n",
               "#define %s_DOIS_CORPOS %s_UNUSED_0x4501\n" % (P, P),
               "#endif\n",
               "#define %s_VIZINHA_0x4502 0x4502\n" % P)
        open(usos, "w").write("%s_DOIS_CORPOS %s_VIZINHA_0x4502\n" % (P, P))
        e2 = roda()
        assert len(e2) == 1 and e2[0]["endereco"] == "0x4502" \
            and e2[0]["nomes"] == ["%s_DOIS_CORPOS" % P, "%s_VIZINHA_0x4502" % P], \
            "o corpo do ramo morto não podia esconder o dono: %r" % e2
        assert "%s_DOIS_CORPOS" % P in {n for _, _, n in stubs_aqui()}, \
            "o `#ifndef` do ramo morto também tinha que reprovar"
        os.remove(usos)

    # 6. o mesmo plante contra a ÁRVORE DE VERDADE e a lista autorizada de
    #    verdade: headers copiados e mutados, data/src/test por link para o
    #    repo, e um nome novo em cima do endereço do perfil. Verde antes,
    #    vermelho com o plante.
    #    vars: 0x4060 tinha DOIS donos declarados quando o J4 escreveu isto; o
    #    realias do J6, no mesmo 18/08/2026, tirou de lá
    #    VAR_MAP_SCENE_SILPH_CO_11F e hoje o endereço é só de VAR_ROUTE101_STATE.
    #    flags: 0x0001 é FLAG_TEMP_1. Nos dois casos o plante fabrica o SEGUNDO
    #    dono, que é o que o portão tem que acusar.
    assert portao(verboso=False) == [], \
        "a árvore de hoje devia estar verde antes do plante (perfil %s)" % PERFIL
    def arvore_de_verdade(tmp):
        """Cópia mutável dos headers do perfil, com o resto do repo por link."""
        copia_headers(tmp)
        for r in ("data", "src", "test"):
            os.symlink(os.path.join(RAIZ, r), os.path.join(tmp, r))
        os.makedirs(os.path.join(tmp, "plante"))

    def planta_em(caminho, linha):
        with open(caminho, "r+", encoding="utf-8") as f:
            texto = f.read()
            corte = texto.rindex("#endif")
            f.seek(0)
            f.write(texto[:corte] + linha + texto[corte:])
            f.truncate()

    with tempfile.TemporaryDirectory() as tmp:
        arvore_de_verdade(tmp)
        open(os.path.join(tmp, "plante", "usa.inc"), "w").write("%s_PLANTADA_D\n" % P)
        planta_em(os.path.join(tmp, "include", "constants", ponta),
                  "#define %s_PLANTADA_D 0x%X\n" % (P, PLANTE))
        novas = portao(base=tmp, raizes=["data", "src", "include", "test", "plante"],
                       verboso=False)
        assert len(novas) == 1 and int(novas[0]["endereco"], 16) == PLANTE \
            and "%s_PLANTADA_D" % P in novas[0]["nomes"], \
            "o plante na árvore de verdade devia reprovar, deu %r" % novas

    # 7. ALCANCE NOVO (19/08/2026): a mesma mutação, agora plantada dentro do
    #    `include/config/*.h` do perfil. Antes desta leva o portão nem lia esse
    #    arquivo, e um segundo dono declarado ali passava calado. É o passo que
    #    prova o alcance: se alguém tirar o header de config do perfil, ele cai.
    config = [h for h in HEADERS if h.startswith("include/config/")]
    assert config, "o perfil %s perdeu o header de config" % PERFIL
    with tempfile.TemporaryDirectory() as tmp:
        arvore_de_verdade(tmp)
        open(os.path.join(tmp, "plante", "usa.inc"), "w").write("%s_PLANTADA_G\n" % P)
        planta_em(os.path.join(tmp, config[0]),
                  "#define %s_PLANTADA_G 0x%X\n" % (P, PLANTE))
        novas = portao(base=tmp, raizes=["data", "src", "include", "test", "plante"],
                       verboso=False)
        assert len(novas) == 1 and int(novas[0]["endereco"], 16) == PLANTE \
            and "%s_PLANTADA_G" % P in novas[0]["nomes"], \
            ("o plante em %s devia reprovar, deu %r" % (config[0], novas))

    assert stubs(verboso=False) == [], \
        "a árvore de hoje tem stub `#ifndef %s_` (perfil %s)" % (PREFIXO, PERFIL)

    print("demo (%s): 14 checagens passaram (verde; vermelho com mutação, "
          "APELIDO DE NOME VIVO junto; verde com autorização; vermelho com nome "
          "novo; verde sem mutação; vermelho com as TRÊS formas de stub "
          "(`#ifndef`, `#ifndef` com comentário e `#if !defined`); vermelho com "
          "duas faixas de base+deslocamento; vermelho com DUAS ALOCAÇÕES na "
          "mesma vaga do pool; verde com alocação sozinha; vermelho com apelido "
          "de apelido; vermelho com `#define` em dois ramos; vermelho com "
          "mutação plantada na árvore de verdade; e vermelho com mutação "
          "plantada dentro do include/config/ do perfil)" % PERFIL)


if __name__ == "__main__":
    if "--flags" in sys.argv:
        usa("flags")
    if "--demo" in sys.argv:
        demo()
    elif "--gravar" in sys.argv:
        grava()
    elif "--lista" in sys.argv:
        for g in colisoes(RAIZ, HEADERS, RAIZES_DE_USO):
            print(g["endereco"], g["nomes"], g["onde"])
    else:
        # os dois têm que passar: colisão de endereço E stub de `#ifndef`.
        ruim = portao()
        ruim = stubs() or ruim
        sys.exit(1 if ruim else 0)
