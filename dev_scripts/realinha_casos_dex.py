#!/usr/bin/env python3
"""Realinha os casos de estático da Dex com `dex_distribuicao.json`.

Por que este arquivo existe
---------------------------
Os casos T131 a T134 (e o T136.1/T136.2, que reaproveita a rota do T132.38)
provam uma coisa só: o tile T de um mapa tem um objeto SÓLIDO, e a flag de HIDE
daquele objeto faz o tile ficar vazio. O par positivo anda até encostar no bicho
e para em `para`; o par negativo anda a MESMA rota com UMA flag a mais e
escorrega até `vazio`. É a diferença entre os dois que prova alguma coisa: sem o
negativo, "o jogador parou" tem parede, elevação e mapa que não carregou como
explicações concorrentes.

A onda 2 (`eec7d7a401`) reescreveu a régua 3 e redistribuiu 256 espécies. Ela
NÃO mexeu na geometria: em 24 dos 25 mapas tocados o CONJUNTO de tiles de
estático ficou igual (só ganhou tiles novos). O que mudou foi QUAL espécie senta
em QUAL tile, porque `decide_estaticos` distribui na ordem da lista de espécies
e a lista ganhou 171 entradas de geração 5 que antes moravam em Unova.

Efeito medido na suíte: o par POSITIVO continuava verde (o tile segue ocupado,
só que por outro bicho) e o par NEGATIVO reprovava sempre (a flag citada no caso
esconde uma espécie que não mora mais ali, então o tile continuava sólido). Ou
seja, o positivo tinha virado um teste que passa pelo motivo errado, e só o
negativo denunciava. Foi exatamente isso que os 41 vermelhos de 07/09/2026
diziam, com a assinatura "esperado (vazio), obtido (para)".

O conserto é no CASO, não no mapa: o tile passou pelos mesmos portões de sempre
(colisão, elevação, não-ilhar, teto de sprite), a rota até ele continua válida,
e só o NOME da espécie e a FLAG de HIDE que o caso cita é que envelheceram. Este
script relê a tabela e reescreve nome e flag pelo OCUPANTE ATUAL do tile.

Como ele decide, caso a caso
----------------------------
1. Acha na tabela a linha cujo (mapa, `para`) é o mesmo do `prova.pos` do par
   positivo. `para` é o tile em que o jogador encosta, então ele identifica o
   ALVO da rota sem depender do texto do caso.
2. Achou, e a geometria do caso bate com a da tabela: troca só espécie e flag.
3. Achou, mas o caso está em `GEOMETRIA_A_MAO`: troca só espécie e flag, e a
   rota do caso fica INTOCADA. São as rotas que já foram corrigidas no
   emulador contra coisa que a tabela não enxerga (linha de visão de treinador,
   porta animada).
4. Achou, e o caso está em `REGEOMETRIA`: a rota do caso ficou obsoleta porque
   um estático NOVO caiu em cima dela. A rota nova sai da própria tabela, que a
   recalculou com todos os irmãos do mapa como parede (`rota_entre_vizinhos`).
5. NÃO achou linha nenhuma naquele tile: o estático saiu do tile de vez. Aí o
   caso segue a ESPÉCIE para a casa nova dela e pega a geometria inteira da
   tabela.

Uso:
    python3 dev_scripts/realinha_casos_dex.py            # aplica
    python3 dev_scripts/realinha_casos_dex.py --confere  # só diz o que faria

É idempotente: rodar duas vezes seguidas não muda nada na segunda, porque a
segunda já encontra o caso citando o ocupante atual.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABELA = os.path.join(RAIZ, "dev_scripts", "dex_distribuicao.json")
CASOS = os.path.join(RAIZ, "dev_scripts", "testes_criticos")

ARQUIVOS = ("131_dex_kanto.json", "132_dex_johto.json",
            "133_dex_hoenn.json", "134_dex_sinnoh.json")

# Rota medida no emulador contra coisa que a busca em largura da tabela não
# enxerga. Trocar espécie e flag aqui é seguro; trocar a rota desfaz a medição.
GEOMETRIA_A_MAO = {
    # A tabela manda o par negativo escorregar 22 tiles até (24,13), mas em
    # (12,12) mora o LOCALID_MT_CORONET_B1F_GALACTIC_GRUNT, virado para baixo
    # com sight 2, e ele aborda o jogador em (12,13). Medido em 21/08/2026, e a
    # perna final do caso é exata de 9 tiles por causa disso.
    "T134.5": "linha de visao do Galactic Grunt de (12,12)",
    "T134.6": "linha de visao do Galactic Grunt de (12,12)",
}

# Rota que ficou obsoleta porque um estático NOVO caiu em cima dela. A rota nova
# vem da tabela, que já a recalculou com o intruso como parede.
REGEOMETRIA = {
    # O FEZANDIPITI entrou em IlexForest no tile (31,16), que é bem no meio da
    # linha 16 que a rota antiga percorria para chegar ao (36,16). O jogador
    # parava em (30,16). A rota da tabela desce para a linha 15, atravessa e
    # volta para a 16 depois do intruso.
    "T132.13": "FEZANDIPITI novo em (31,16), no meio da linha 16",
    "T132.14": "FEZANDIPITI novo em (31,16), no meio da linha 16",
}

MARCA = ("REALINHADO EM 07/09/2026: a onda 2 da Dex (eec7d7a401) redistribuiu "
         "as 256 especies que perderam fonte com a saida de Unova e Galar, e a "
         "ordem da lista de especies mudou quem senta em cada tile. O TILE, a "
         "rota e a prova continuam os mesmos; mudou a especie que mora nele, "
         "e com ela a flag de HIDE. Sem esta troca o par negativo reprovava "
         "sempre (a flag citada escondia um bicho que nao mora mais ali, entao "
         "o tile seguia solido) e o par positivo passava pelo motivo errado.")


def curto(especie):
    return especie.replace("SPECIES_", "")


def tabela():
    d = json.load(open(TABELA, encoding="utf-8"))
    por_para, por_especie = {}, {}
    for e in d["estaticos"]:
        por_para[(e["mapa"], tuple(e["para"]))] = e
        por_especie[curto(e["especie"])] = e
    return por_para, por_especie


def pasta_por_const():
    import glob
    fora = {}
    for p in glob.glob(os.path.join(RAIZ, "data", "maps", "*", "map.json")):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if d.get("id"):
            fora[d["id"]] = os.path.basename(os.path.dirname(p))
    return fora


def toques(rota):
    """A rota da tabela virada em pernas de roteiro, com a MESMA regra dos casos
    originais: perna que zera leva DOIS toques (aperto contra parede, fixa a
    direcao sem andar), perna que satura leva n+2 (toque a mais contra parede
    nao custa nada) e perna exata leva n+1 (a primeira tecla de uma direcao nova
    so VIRA o boneco, T121.1)."""
    fora = []
    for D, n, sat in rota:
        fora.append((D, 2 if n == 0 else (n + 2 if sat else n + 1)))
    return fora


def roteiro(rota, positivo):
    """O campo `roteiro` do caso. Cada toque dura 17 quadros e nao 16: 16 empata
    com o passo do jogador e come um toque por perna exata."""
    partes = ["60:NADA"]
    pernas = toques(rota)
    for i, (D, n) in enumerate(pernas):
        partes.append(f"17:{D}*{n}")
        partes.append("90:NADA" if i == len(pernas) - 1 else "40:NADA")
    if positivo:
        # O A abre o msgbox de abertura, que comeca com lockall: a perna de
        # volta NAO move o jogador, e e por isso que ela e a prova de que a
        # caixa de texto abriu.
        volta = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        partes += ["17:A", "180:NADA", f"17:{volta[pernas[-1][0]]}*8", "150:NADA"]
    return ",".join(partes)


def troca_nome(texto, velho, novo):
    texto = re.sub(rf"\bFLAG_HIDE_DEX_{velho}\b", f"FLAG_HIDE_DEX_{novo}", texto)
    return re.sub(rf"\b{velho}\b", novo, texto)


def troca_flags(flags, velho, novo):
    return ["FLAG_HIDE_DEX_" + novo if f == f"FLAG_HIDE_DEX_{velho}" else f
            for f in flags]


def descreve_rota(rota):
    fora = []
    for D, n, sat in rota:
        fora.append(f"{D}(zera)" if n == 0 else f"{D}*{n}")
    return " ".join(fora)


# O texto do caso, quando a geometria inteira e refeita. Ele nao pode ficar o
# antigo: o antigo cita o tile velho, a rota velha e a parada velha, e caso que
# descreve outra coisa do que faz e pior do que caso nenhum. E a MESMA forma dos
# casos originais (T134.1 e T134.2), com os numeros novos.
def monta_nome(e, const, positivo, par, motivo):
    novo = curto(e["especie"])
    T, para, vazio = tuple(e["tile"]), tuple(e["para"]), tuple(e["vazio"])
    comum = (
        f"O tile {T} saiu da busca em largura do T123 (colisao E elevacao, "
        f"portao de que por o bicho ali nao ilha nenhum tile do mapa, 3 tiles "
        f"de folga de NPC que anda) e passou pelo teto de sprite: nenhuma "
        f"janela de 20x17 tiles do mapa fica com mais de 15 objetos, senao o "
        f"motor deixaria de acordar o Pokemon sem dizer nada. ROTA: "
        f"{descreve_rota(e['rota'])}, a partir do warp {e['warp']} "
        f"{tuple(e['porta'])}, pousando em {tuple(e['pouso'])}. A perna que "
        f"ZERA e um aperto contra parede: fixa a direcao do boneco sem andar; "
        f"as outras levam UM aperto a mais porque a primeira tecla de uma "
        f"direcao nova so VIRA o boneco (T121.1), e a que satura leva DOIS, "
        f"porque toque a mais contra parede nao custa nada. Cada toque dura 17 "
        f"quadros e nao 16: 16 empata com o passo do jogador e come um toque "
        f"por perna exata.")
    refeita = (
        f" ROTA REFEITA PELA TABELA (07/09/2026), motivo: {motivo}. Ela saiu do "
        f"`rota_entre_vizinhos` do `distribui_dex.py`, que refaz a busca em "
        f"largura com TODOS os irmaos do mapa como parede, e e a mesma fonte "
        f"que gerou os casos originais. Quem regera este texto: "
        f"`dev_scripts/realinha_casos_dex.py`.")
    if positivo:
        return (
            f"{novo} EXISTE EM {const} ({e['regiao']}) E A INTERACAO TRAVA O "
            f"JOGADOR. {comum} "
            f"A ultima perna satura CONTRA o Pokemon e para em {para}. O A abre "
            f"o msgbox de abertura, que comeca com lockall, e por isso a perna "
            f"de volta NAO move o jogador; o msgbox vem ANTES do playmoncry "
            f"justamente para a prova parar na caixa de texto, sem entrar na "
            f"batalha, que o harness nao le. Par negativo: {par}." + refeita)
    return (
        f"PAR NEGATIVO DO {par}: com {e['flag']} ACESA o tile {T} esta VAZIO. "
        f"MESMA rota (o positivo so acrescenta o A e a perna de volta), e a "
        f"perna final escorrega ate {vazio} em vez de parar em {para}. Sem ele "
        f"o positivo nao prova nada: parada de jogador tem muitas causas "
        f"(parede, elevacao, mapa que nao carregou), e a diferenca entre os "
        f"dois casos e exatamente UMA flag. E tambem a prova de que a flag de "
        f"HIDE escrita no campo `flag` do object_event e a mesma que o script "
        f"acende ao vencer ou capturar. O `andou` prova que o jogo continua "
        f"respondendo." + refeita)


def realinha(confere=False):
    por_para, por_especie = tabela()
    pasta = pasta_por_const()
    mudou_algo, relato = False, []
    for arq in ARQUIVOS:
        caminho = os.path.join(CASOS, arq)
        casos = json.load(open(caminho, encoding="utf-8"))
        mudou = False
        for i in range(0, len(casos), 2):
            pos, neg = casos[i], casos[i + 1]
            m = re.match(r"([A-Z0-9_]+) EXISTE EM", pos["nome"])
            if not m:
                raise SystemExit(f"{pos['id']}: o nome nao comeca com "
                                 "'<ESPECIE> EXISTE EM'. Pare e olhe.")
            velho = m.group(1)
            mapa = pasta.get(pos["warp"])
            e = por_para.get((mapa, tuple(pos["prova"]["pos"])))
            regeo = pos["id"] in REGEOMETRIA
            if e is None:
                # O tile sumiu: a especie mudou de casa dentro do mapa (ou de
                # mapa). Segue a especie e pega a geometria inteira da tabela.
                e = por_especie.get(velho)
                if e is None:
                    raise SystemExit(f"{pos['id']}: nem o tile {pos['prova']['pos']} "
                                     f"tem ocupante nem {velho} esta na tabela. "
                                     "Pare e meca.")
                regeo = True
            novo = curto(e["especie"])
            precisa = (novo != velho) or regeo
            if not precisa:
                continue
            relato.append(f"{pos['id']}/{neg['id']} {e['mapa']} tile "
                          f"{e['tile']}: {velho} -> {novo}"
                          + (" (+ rota da tabela)" if regeo else ""))
            if confere:
                continue
            if regeo and pos["id"] not in GEOMETRIA_A_MAO:
                motivo = REGEOMETRIA.get(
                    pos["id"], f"o tile antigo {tuple(pos['prova']['pos'])} "
                               f"ficou sem ocupante e a especie mudou de casa")
                pos["warp_id"] = e["warp"]
                neg["warp_id"] = e["warp"]
                pos["roteiro"] = roteiro(e["rota"], True)
                neg["roteiro"] = roteiro(e["rota"], False)
                pos["prova"]["pos"] = list(e["para"])
                neg["prova"]["pos"] = list(e["vazio"])
                pos["nome"] = monta_nome(e, pos["warp"], True, neg["id"], motivo)
                neg["nome"] = monta_nome(e, neg["warp"], False, pos["id"], motivo)
                pos["flags"] = troca_flags(pos["flags"], velho, novo)
                neg["flags"] = troca_flags(neg["flags"], velho, novo)
            else:
                for c in (pos, neg):
                    c["nome"] = troca_nome(c["nome"], velho, novo)
                    c["flags"] = troca_flags(c["flags"], velho, novo)
                    if MARCA not in c["nome"]:
                        c["nome"] = c["nome"].rstrip() + " " + MARCA
            mudou = mudou_algo = True
        if mudou and not confere:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(casos, f, ensure_ascii=False, indent=2)
                f.write("\n")
    for l in relato:
        print(l)
    print(f"{len(relato)} pares realinhados" + (" (conferencia)" if confere else ""))
    return mudou_algo


if __name__ == "__main__":
    realinha(confere="--confere" in sys.argv)
