#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Varredura do TEXTO das seis regiões: largura, quebra, charmap, idioma.

A largura é medida em PIXEL, não em caractere: cada letra vira byte pelo
`charmap.txt` e o byte vira largura por `gFontNormalLatinGlyphWidths`
(`src/fonts.c`). A caixa de fala padrão tem 26 tiles de 8 px, 208 px úteis.

    python3 checa_texto.py                  # resumo
    python3 checa_texto.py --detalhe T01
    python3 checa_texto.py --json saida.json
    python3 checa_texto.py --demo           # autoteste com mutação plantada
"""

from __future__ import print_function

import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leitor  # noqa: E402

LARGURA_CAIXA = 208          # 26 tiles de 8 px
LINHAS_POR_PAGINA = 2        # a caixa padrão mostra duas linhas por vez
# largura suposta do que só existe em tempo de execução
NOMINAL = {"PLAYER": 7, "RIVAL": 7, "STR_VAR_1": 0, "STR_VAR_2": 0,
           "STR_VAR_3": 0, "KUN": 0}


def le_charmap(caminho):
    """nome/letra -> lista de bytes."""
    mapa = {}
    rx1 = re.compile(r"^'(.+?)'\s*=\s*((?:[0-9A-Fa-f]{2}\s*)+)")
    rx2 = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*((?:[0-9A-Fa-f]{2}\s*)+)")
    for linha in open(caminho, encoding="utf-8", errors="replace"):
        linha = linha.rstrip("\n")
        if linha.startswith("@"):
            continue
        m = rx1.match(linha) or rx2.match(linha)
        if not m:
            continue
        chave = m.group(1)
        if len(chave) == 2 and chave[0] == "\\":
            chave = {"n": "\n", "l": "\l", "p": "\p"}.get(chave[1], chave[1])
        bs = [int(x, 16) for x in m.group(2).split()]
        mapa.setdefault(chave, bs)
    return mapa


def le_larguras(caminho):
    txt = open(caminho, encoding="utf-8", errors="replace").read()
    m = re.search(r"gFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};", txt, re.S)
    if not m:
        return [6] * 256
    nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
    return nums + [6] * (256 - len(nums))


RE_CHAVE = re.compile(r"\{([A-Z0-9_]+)(?:\s+[^}]*)?\}")


class Medidor(object):
    def __init__(self, raiz):
        self.charmap = le_charmap(os.path.join(raiz, "charmap.txt"))
        self.larguras = le_larguras(os.path.join(raiz, "src", "fonts.c"))

    def largura(self, trecho):
        """Largura em px de um pedaço sem quebra de linha. (px, [fora do charmap])"""
        px = 0
        fora = []
        i = 0
        while i < len(trecho):
            c = trecho[i]
            if c == "{":
                m = RE_CHAVE.match(trecho, i)
                if m:
                    nome = m.group(1)
                    n = NOMINAL.get(nome)
                    if n is None:
                        n = 6 if nome not in self.charmap else 1
                        px += n * 6
                    else:
                        px += n * 6
                    i = m.end()
                    continue
            if c == "\\":
                i += 2
                continue
            bs = self.charmap.get(c)
            if bs is None:
                fora.append(c)
                px += 6
            else:
                for b in bs:
                    px += self.larguras[b]
            i += 1
        return px, fora


class Achado(object):
    __slots__ = ("sigla", "classe", "regiao", "rotulo", "arquivo", "linha", "texto")

    def __init__(self, *a):
        for k, v in zip(self.__slots__, a):
            setattr(self, k, v)

    def como_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}

    def linha_curta(self, raiz):
        rel = self.arquivo[len(raiz):].lstrip("/") if self.arquivo.startswith(raiz) \
            else self.arquivo
        return "[%s][%s][%s] %s:%d %s -- %s" % (self.sigla, self.classe,
                                                self.regiao, rel, self.linha,
                                                self.rotulo, self.texto)


PT_SEM_ACENTO = re.compile(
    r"\b(nao|voce|voces|entao|estao|sao|tambem|ja|esta|aqui e|ate|so|"
    r"tres|apos|proximo|ultimo|dificil|facil|possivel|numero|codigo|"
    r"mae|pai e|irma|licao|missao|caverna e|traves|atras e)\b", re.I)
EN_MARCADORES = re.compile(
    r"\b(the|you|your|there|here|this|that|with|have|will|would|about|"
    r"they|what|when|where|because|Pokemon are|isn't|don't|it's)\b")
PT_MARCADORES = re.compile(
    r"\b(que|para|com|uma|você|voce|não|nao|está|esta|meu|minha|seu|sua|"
    r"aqui|então|entao|também|tambem|muito|todos|quando|porque)\b", re.I)

# Idioma que cada região DEVE falar. Região fora deste mapa não tem alvo e o
# T07 não opina sobre ela. A justificativa de cada linha, e por que Galar virou
# `en` em 06/09/2026, está no docstring de `Varredura._idioma`.
IDIOMA_ALVO = {"Sinnoh": "pt", "Unova": "pt", "Galar": "en"}


class Varredura(object):
    def __init__(self, raiz):
        self.raiz = raiz
        self.arv = leitor.Arvore(raiz)
        self.med = Medidor(raiz)
        self.achados = []
        self.contagem = collections.Counter()
        self._indexa_buffers()

    def _indexa_buffers(self):
        """rótulo de texto -> conjunto de STR_VAR carregados antes de exibi-lo."""
        self.buffers = collections.defaultdict(set)
        self.texto_usado = collections.defaultdict(list)
        buf = {"bufferspeciesname": 0, "bufferleadmonspeciesname": 0,
               "bufferpartymonnick": 0, "bufferitemname": 0,
               "bufferdecorationname": 0, "buffermovename": 0,
               "buffernumberstring": 0, "bufferstdstring": 0,
               "bufferstring": 0, "buffertrainerclassname": 0,
               "buffertrainername": 0, "buffercontestname": 0,
               "bufferboxname": 0, "bufferitemnameplural": 0}
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                vivos = set()
                for (n, nome, args) in b.cmds:
                    if nome in buf and args:
                        vivos.add(args[0].strip())
                    elif nome in ("msgbox", "message", "messageinstant",
                                  "braillemsgbox", "pokenavcall",
                                  "messageautoscroll", "vmessage") and args:
                        alvo = args[0].strip()
                        self.buffers[alvo] |= vivos
                        self.texto_usado[alvo].append((caminho, n, b.rotulo))
                    elif nome in ("special", "specialvar", "callstd",
                                  "gotostd", "call"):
                        pass

    def add(self, sigla, classe, arquivo, linha, rotulo, texto):
        reg = self.arv.regiao_do_arquivo(arquivo)
        self.achados.append(Achado(sigla, classe, reg, rotulo, arquivo,
                                   linha, texto))

    # --------------------------------------------------------------- checagens
    def roda(self):
        for caminho, blocos in self.arv.arquivos.items():
            reg = self.arv.regiao_do_arquivo(caminho)
            for b in blocos:
                if not b.textos:
                    continue
                self._um_texto(caminho, reg, b)
        return self.achados

    def _um_texto(self, caminho, reg, b):
        # junta o corpo inteiro do rótulo, guardando a linha de cada pedaço
        pedacos = []
        for (n, diretiva, bruto) in b.textos:
            m = re.match(r'^"(.*)"\s*$', bruto.strip())
            if not m:
                m = re.match(r'^"(.*)"', bruto.strip())
            if not m:
                continue
            pedacos.append((n, m.group(1)))
        if not pedacos:
            return
        inteiro = "".join(p[1] for p in pedacos)
        self.contagem["textos[%s]" % reg] += 1

        if not inteiro.endswith("$"):
            self.add("T05", "trava", caminho, pedacos[0][0], b.rotulo,
                     "bloco de texto sem `$` no fim")
        corpo = inteiro[:-1] if inteiro.endswith("$") else inteiro
        if corpo.strip() == "":
            self.add("T06", "provável", caminho, pedacos[0][0], b.rotulo,
                     "texto vazio")

        # T01/T02: largura e quebra, por linha lógica
        linhas = re.split(r"\\[nlp]", corpo)
        marcas = re.findall(r"\\([nlp])", corpo)
        pagina = 1
        for i, ln in enumerate(linhas):
            px, fora = self.med.largura(ln)
            if px > LARGURA_CAIXA:
                self.add("T01", "cosmético", caminho, self._linha_de(pedacos, corpo, ln),
                         b.rotulo, "linha de %d px (teto %d): %r"
                         % (px, LARGURA_CAIXA, ln[:60]))
            if fora:
                self.add("T03", "provável", caminho,
                         self._linha_de(pedacos, corpo, ln), b.rotulo,
                         "caractere fora do charmap: %s" % " ".join(sorted(set(fora))))
            if i < len(marcas):
                if marcas[i] == "n":
                    pagina += 1
                    if pagina > LINHAS_POR_PAGINA:
                        self.add("T02", "cosmético", caminho,
                                 self._linha_de(pedacos, corpo, ln), b.rotulo,
                                 "terceira linha sem \\l nem \\p (a caixa "
                                 "mostra %d)" % LINHAS_POR_PAGINA)
                        pagina = 1
                else:
                    pagina = 1

        # T04: STR_VAR sem buffer
        usados = set(RE_CHAVE.findall(corpo))
        precisa = {u for u in usados if u.startswith("STR_VAR")}
        if precisa:
            carregados = self.buffers.get(b.rotulo, set())
            faltando = {u for u in precisa if u not in carregados}
            if faltando and self.texto_usado.get(b.rotulo):
                self.add("T04", "provável", caminho, pedacos[0][0], b.rotulo,
                         "usa %s e o script que exibe não carrega buffer"
                         % ",".join(sorted(faltando)))

        self._idioma(caminho, reg, b, corpo, pedacos)

        if "ä" in corpo or "ö" in corpo:
            self.add("T09", "provável", caminho, pedacos[0][0], b.rotulo,
                     "trema sobrando (era para ser til)")

    def _idioma(self, caminho, reg, b, corpo, pedacos):
        """T07 (idioma errado) e T08 (português sem acento).

        DECISÃO DE DESENHO, 06/09/2026, tomada pela condutora da Frente A
        (Galar) do cartucho 2 e registrada aqui porque ela INVERTE a régua e
        quem ler o relatório de QA sem este comentário vai achar que a
        ferramenta enlouqueceu.

        Até hoje a régua era uma só: Sinnoh, Unova e Galar deveriam falar
        PORTUGUÊS, e T07 reprovava inglês nas três. A decisão 32 do Gui
        (PRD-CARTUCHO-2.md) tirou Galar dessa lista: o cartucho 2 traduz o
        português do demake para o INGLÊS, fielmente, com glossário fixo. Com a
        régua velha a frente entregaria vermelho por acertar, porque traduzir os
        310 blocos de português de Galar levaria o T07 de 28 para 338 achados.

        Régua de hoje, por região (`IDIOMA_ALVO`):

        - Sinnoh e Unova: alvo `pt`. T07 reprova INGLÊS. Não mudou nada.
          Unova hoje fala inglês por herança do importador e o cartucho 2 ainda
          não decidiu o idioma dela; mexer aqui seria decidir por tabela, então
          ela fica como estava.
        - Galar: alvo `en`. T07 reprova PORTUGUÊS, com ou sem acento, e aceita
          inglês.
        - As outras (Hoenn, Kanto, Johto, `comum`): sem alvo, T07 não opina.

        T08 (português sem acento) IGNORA Galar de propósito, e SÓ Galar. Ele só
        dispara dentro do ramo "este bloco é português", e em Galar esse ramo
        agora já emite T07 no mesmo bloco: manter os dois faria o mesmo defeito
        ser contado duas vezes, com o T08 dizendo "conserte o acento" de um
        texto que a decisão 32 manda apagar e reescrever em inglês. Em toda
        região que NÃO tem alvo `en` ele continua valendo inteiro, inclusive
        Hoenn, Kanto, Johto e `comum`, que nunca tiveram alvo de idioma.

        O CENSO (`self.contagem`) continua contando os dois idiomas em TODAS as
        regiões, porque ele é medição, não julgamento: é por ele que a próxima
        rodada mede quanto da tradução de Galar já andou.
        """
        limpo = re.sub(r"\{[^}]*\}", " ", corpo).replace("\\n", " ") \
                  .replace("\\l", " ").replace("\\p", " ")
        en = len(EN_MARCADORES.findall(limpo))
        pt = len(PT_MARCADORES.findall(limpo))
        alvo = IDIOMA_ALVO.get(reg)
        if en >= 2 and en > pt:
            self.contagem["ingles[%s]" % reg] += 1
            if alvo == "pt":
                self.add("T07", "cosmético", caminho, pedacos[0][0], b.rotulo,
                         "texto em inglês numa região que deveria estar em "
                         "português: %r" % limpo[:60])
        elif pt >= 2 and pt > en:
            self.contagem["portugues[%s]" % reg] += 1
            sem_acento = PT_SEM_ACENTO.search(limpo)
            if sem_acento:
                self.contagem["pt_sem_acento[%s]" % reg] += 1
            if alvo == "en":
                self.add("T07", "cosmético", caminho, pedacos[0][0], b.rotulo,
                         "texto em português numa região que deveria estar em "
                         "inglês: %r" % limpo[:60])
            elif sem_acento:
                self.add("T08", "cosmético", caminho, pedacos[0][0], b.rotulo,
                         "português sem acento: %r" % sem_acento.group(0))

    @staticmethod
    def _linha_de(pedacos, corpo, trecho):
        alvo = trecho[:20]
        for (n, p) in pedacos:
            if alvo and alvo in p:
                return n
        return pedacos[0][0]


def resumo(v, raiz):
    print("=== por checagem ===")
    for s in sorted(set(a.sigla for a in v.achados)):
        cl = collections.Counter(a.classe for a in v.achados if a.sigla == s)
        rg = collections.Counter(a.regiao for a in v.achados if a.sigla == s)
        print("%-4s %6d  %s  %s" % (s, sum(cl.values()), dict(cl), dict(rg)))
    print("=== censo de idioma ===")
    for k in sorted(v.contagem):
        print("  %-26s %d" % (k, v.contagem[k]))
    print("total de achados:", len(v.achados))


def demo():
    import shutil
    import tempfile
    origem = leitor.RAIZ_PADRAO
    tmp = tempfile.mkdtemp(prefix="qa_texto_demo_")
    for sub in ("data", "include", "charmap.txt"):
        s = os.path.join(origem, sub)
        d = os.path.join(tmp, sub)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=True)
        else:
            shutil.copy2(s, d)
    os.makedirs(os.path.join(tmp, "src"), exist_ok=True)
    shutil.copy2(os.path.join(origem, "src", "fonts.c"),
                 os.path.join(tmp, "src", "fonts.c"))
    alvo = os.path.join(tmp, "data", "maps", "LittlerootTown", "scripts.inc")
    with open(alvo, "a", encoding="utf-8") as fh:
        fh.write('''
QA_Demo_Texto::
\t.string "Esta linha foi escrita de proposito muito mais larga do que a caixa aguenta\\n"
\t.string "segunda linha\\n"
\t.string "terceira linha sem l nem p\\n"
\t.string "quarta linha com trema irmä$"

QA_Demo_TextoSemCifrao::
\t.string "sem fim"
''')
    v = Varredura(tmp)
    v.roda()
    siglas = {a.sigla for a in v.achados if a.rotulo.startswith("QA_Demo")}
    esperado = {"T01", "T02", "T05", "T09"}
    print("demo: siglas que morderam:", sorted(siglas))
    faltou = esperado - siglas
    shutil.rmtree(tmp, ignore_errors=True)
    if faltou:
        print("DEMO VERMELHO: não mordeu", sorted(faltou))
        return 1
    print("DEMO VERDE")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", default=leitor.RAIZ_PADRAO)
    ap.add_argument("--detalhe")
    ap.add_argument("--limite", type=int, default=40)
    ap.add_argument("--regiao")
    ap.add_argument("--json")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    v = Varredura(a.raiz)
    v.roda()
    if a.detalhe:
        sel = [x for x in v.achados if x.sigla == a.detalhe.upper()
               and (not a.regiao or x.regiao == a.regiao)]
        for x in sel[:a.limite]:
            print(x.linha_curta(a.raiz))
        print("(%d de %d)" % (min(len(sel), a.limite), len(sel)))
    else:
        resumo(v, a.raiz)
    if a.json:
        json.dump([x.como_dict() for x in v.achados], open(a.json, "w"),
                  ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
