#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Varredura estática dos scripts de evento das seis regiões.

Procura o que o assembler NÃO pega: rótulo inexistente o assembler pega,
`lock` sem `release` ele não pega. Cada checagem tem sigla, e o `--demo`
planta uma mutação em cópia temporária para provar que a checagem morde.

    python3 checa_scripts.py                 # varre tudo, imprime resumo
    python3 checa_scripts.py --detalhe C01   # lista os achados de uma checagem
    python3 checa_scripts.py --json saida.json
    python3 checa_scripts.py --demo          # autoteste com mutação plantada
"""

from __future__ import print_function

import argparse
import collections
import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leitor  # noqa: E402


# --------------------------------------------------------------- vocabulário
TERMINADORES = {"end", "return", "endram", "returnram", "gotonative",
                "step_end", "pokemartlistend", "closebraillemessage"}
DIRETIVA_DADO = {".string", ".asciz", ".ascii", ".byte", ".2byte", ".4byte",
                 ".align", ".incbin", ".space", ".word", ".short"}
SALTO_INCOND = {"goto": 0, "vgoto": 0}
SALTO_COND = {
    "goto_if": 1, "vgoto_if": 1,
    "goto_if_set": 1, "goto_if_unset": 1,
    "vgoto_if_set": 1, "vgoto_if_unset": 1,
    "goto_if_defeated": 1, "goto_if_not_defeated": 1,
    "case": 1,
}
SALTO_CMP = {"goto_if_eq", "goto_if_ne", "goto_if_lt", "goto_if_gt",
             "goto_if_le", "goto_if_ge", "vgoto_if_eq", "vgoto_if_ne"}
CHAMADA = {"call": 0, "vcall": 0, "call_if": 1, "vcall_if": 1,
           "call_if_set": 1, "call_if_unset": 1,
           "call_if_defeated": 1, "call_if_not_defeated": 1}
CHAMADA_CMP = {"call_if_eq", "call_if_ne", "call_if_lt", "call_if_gt",
               "call_if_le", "call_if_ge"}

WARPS = {"warp", "warpsilent", "warpdoor", "warphole", "warpteleport",
         "warpspinenter", "warpwhitefade", "warpmossdeepgym", "setescapewarp",
         "setwarp", "setdynamicwarp", "setdivewarp", "setholewarp"}
WARP_QUE_TROCA = {"warp", "warpsilent", "warpdoor", "warphole", "warpteleport",
                  "warpspinenter", "warpwhitefade", "warpmossdeepgym"}

# comandos que recebem local id no argumento 0
CMD_LOCALID = {
    "applymovement": 0, "removeobject": 0, "addobject": 0, "setobjectxy": 0,
    "turnobject": 0, "showobjectat": 0, "hideobjectat": 0,
    "setobjectxyperm": 0, "copyobjectxytoperm": 0,
    "setobjectmovementtype": 0, "setobjectsubpriority": 0,
    "resetobjectsubpriority": 0, "waitmovement": 0,
}
LOCALID_LIVRE = {"LOCALID_PLAYER", "OBJ_EVENT_ID_PLAYER", "LOCALID_CAMERA",
                 "OBJ_EVENT_ID_CAMERA", "LOCALID_NONE", "LOCALID_FOLLOWING_POKEMON",
                 "VAR_LAST_TALKED", "OBJ_EVENT_ID_FOLLOWER"}

VAR_MIN, VAR_MAX = 0x4000, 0x41FF

MSGBOX_OK = {"MSGBOX_NPC", "MSGBOX_SIGN", "MSGBOX_DEFAULT", "MSGBOX_YESNO",
             "MSGBOX_AUTOCLOSE", "MSGBOX_GETPOINTS", "MSGBOX_POKENAV"}


class Achado(object):
    __slots__ = ("sigla", "classe", "regiao", "mapa", "rotulo", "arquivo",
                 "linha", "texto")

    def __init__(self, sigla, classe, regiao, mapa, rotulo, arquivo, linha, texto):
        self.sigla, self.classe, self.regiao = sigla, classe, regiao
        self.mapa, self.rotulo = mapa, rotulo
        self.arquivo, self.linha, self.texto = arquivo, linha, texto

    def como_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}

    def linha_curta(self, raiz):
        rel = self.arquivo[len(raiz):].lstrip("/") if self.arquivo.startswith(raiz) else self.arquivo
        return "[%s][%s][%s] %s:%d %s -- %s" % (
            self.sigla, self.classe, self.regiao, rel, self.linha,
            self.rotulo, self.texto)


class Varredura(object):
    def __init__(self, raiz):
        self.raiz = raiz
        self.arv = leitor.Arvore(raiz)
        self.achados = []
        self._indexa()

    # ------------------------------------------------------------- indexação
    def _indexa(self):
        arv = self.arv
        self.destino_de_bloco = {}
        self.chamados = set()
        self.saltados = set()
        self.flags_acesas = collections.Counter()
        self.flags_apagadas = collections.Counter()
        self.flags_lidas = collections.Counter()
        self.trainer_usos = collections.defaultdict(list)
        self.especiais_usados = collections.Counter()

        for caminho, blocos in arv.arquivos.items():
            for i, b in enumerate(blocos):
                prox = blocos[i + 1].rotulo if i + 1 < len(blocos) else None
                self.destino_de_bloco[id(b)] = prox
                for (n, nome, args) in b.cmds:
                    d = self.destino(nome, args)
                    if d:
                        if nome in CHAMADA or nome in CHAMADA_CMP:
                            self.chamados.add(d)
                        else:
                            self.saltados.add(d)
                    if nome in ("setflag", "setworldmapflag") and args:
                        self.flags_acesas[args[0].strip()] += 1
                    elif nome == "clearflag" and args:
                        self.flags_apagadas[args[0].strip()] += 1
                    elif nome in ("checkflag", "goto_if_set", "goto_if_unset",
                                  "call_if_set", "call_if_unset",
                                  "vgoto_if_set", "vgoto_if_unset") and args:
                        self.flags_lidas[args[0].strip()] += 1
                    elif nome.startswith("trainerbattle") and args:
                        self._registra_treinador(nome, args, caminho, n, b)
                    elif nome == "special" and args:
                        self.especiais_usados[args[0].strip()] += 1

        # flags mexidas em C
        self.flags_c = set()
        srcdir = os.path.join(self.raiz, "src")
        rx = re.compile(r"(?:FlagSet|FlagClear|FlagToggle)\s*\(\s*(FLAG_[A-Z0-9_]+)")
        for dirp, _, arqs in os.walk(srcdir):
            for a in arqs:
                if not a.endswith((".c", ".h")):
                    continue
                try:
                    txt = open(os.path.join(dirp, a), encoding="utf-8",
                               errors="replace").read()
                except Exception:
                    continue
                for m in rx.finditer(txt):
                    self.flags_c.add(m.group(1))


    @staticmethod
    def roteiro_pos_batalha(nome, args):
        """O `event_script` de trainerbattle_*: para onde o jogo vai DEPOIS.

        Com ele, `gotobeatenscript` desvia e a linha seguinte ao comando
        nunca roda; sem ele, `gotopostbattlescript` volta para a linha
        seguinte, e é ali que o `release` tem de estar.
        """
        idx = {"trainerbattle_single": 3, "trainerbattle_double": 4}.get(nome)
        if idx is None or len(args) <= idx:
            return None
        v = args[idx].strip()
        if v in ("FALSE", "0", "NULL", ""):
            return None
        return v

    @staticmethod
    def _solta_por_msgbox(cmds):
        for (n, nome, args) in cmds:
            if nome == "msgbox" and len(args) >= 2 and \
                    args[1].strip() in ("MSGBOX_SIGN", "MSGBOX_NPC",
                                        "MSGBOX_AUTOCLOSE"):
                return True
            if nome in ("callstd", "gotostd") and args and \
                    args[0].strip() in ("STD_MSGBOX_SIGN", "STD_MSGBOX_NPC"):
                return True
        return False

    def _registra_treinador(self, nome, args, caminho, n, b):
        idx = {"trainerbattle_single": 0, "trainerbattle_double": 0,
               "trainerbattle_rematch": 0, "trainerbattle_rematch_double": 0,
               "trainerbattle_no_intro": 0, "trainerbattle_earlyrival": 0,
               "trainerbattle_two_trainers": 0}.get(nome)
        if idx is None:
            return
        alvo = args[idx].strip()
        self.trainer_usos[alvo].append((caminho, n, b.rotulo, nome))
        if nome == "trainerbattle_two_trainers" and len(args) > 2:
            self.trainer_usos[args[2].strip()].append((caminho, n, b.rotulo, nome))

    @staticmethod
    def destino(nome, args):
        if not args:
            return None
        if nome in SALTO_INCOND:
            return args[SALTO_INCOND[nome]].strip() if len(args) > SALTO_INCOND[nome] else None
        if nome in SALTO_COND:
            i = SALTO_COND[nome]
            return args[i].strip() if len(args) > i else None
        if nome in CHAMADA:
            i = CHAMADA[nome]
            return args[i].strip() if len(args) > i else None
        if nome in SALTO_CMP or nome in CHAMADA_CMP:
            return args[-1].strip()
        return None

    # -------------------------------------------------------------- ajudantes
    def add(self, sigla, classe, arquivo, linha, rotulo, texto, mapa=None):
        mapa = mapa or self.arv.mapa_do_arquivo.get(arquivo)
        reg = self.arv.regiao.get(mapa) if mapa else None
        reg = reg or self.arv.regiao_do_arquivo(arquivo)
        self.achados.append(Achado(sigla, classe, reg, mapa or "", rotulo,
                                   arquivo, linha, texto))

    def bloco(self, rotulo):
        return self.arv.blocos.get(rotulo)

    def entradas_do_mapa(self, mapa):
        """Rótulos que o motor pode entrar sozinho neste mapa."""
        j = self.arv.mapas.get(mapa) or {}
        alvos = set()
        for chave in ("object_events", "bg_events", "coord_events"):
            for ev in j.get(chave) or []:
                s = (ev.get("script") or "0").strip()
                if s not in ("", "0", "0x0", "NULL"):
                    alvos.add(s)
        alvos.add("%s_MapScripts" % mapa)
        return alvos

    # ------------------------------------------------- caminhada de fluxo
    def caminha(self, rotulo, visitados=None, prof=0):
        """Todos os comandos alcançáveis a partir de um rótulo (goto+call)."""
        if visitados is None:
            visitados = set()
        if rotulo in visitados or prof > 200:
            return []
        visitados.add(rotulo)
        b = self.bloco(rotulo)
        if b is None:
            return []
        saida = list(b.cmds)
        for (n, nome, args) in b.cmds:
            d = self.destino(nome, args)
            if d and d in self.arv.blocos:
                saida += self.caminha(d, visitados, prof + 1)
        prox = self.destino_de_bloco.get(id(b))
        if prox and not self._termina(b) and prox in self.arv.blocos:
            saida += self.caminha(prox, visitados, prof + 1)
        return saida

    @staticmethod
    def _e_dado(bloco):
        """Bloco de dado (texto, tabela de mart, lista de movimento)."""
        if any(c[1] in DIRETIVA_DADO for c in bloco.cmds):
            return True
        if bloco.cmds and bloco.cmds[-1][1] in ("step_end", "pokemartlistend"):
            return True
        return False

    @classmethod
    def _termina(cls, bloco):
        if cls._e_dado(bloco):
            return True
        for (n, nome, args) in reversed(bloco.cmds):
            if nome.startswith("."):
                continue
            return nome in TERMINADORES or nome in SALTO_INCOND
        return False

    # ================================================================ checagens
    def c01_lock_sem_release(self):
        """C01: `lock`/`lockall` sem `release`/`releaseall` em ramo nenhum."""
        for mapa in sorted(self.arv.mapas):
            for entrada in sorted(self.entradas_do_mapa(mapa)):
                b = self.bloco(entrada)
                if b is None:
                    continue
                cmds = self.caminha(entrada)
                for (n0, nm0, ar0) in list(cmds):
                    alvo0 = self.roteiro_pos_batalha(nm0, ar0)
                    if alvo0:
                        cmds += self.caminha(alvo0)
                nomes = [c[1] for c in cmds]
                if not any(x in ("lock", "lockall", "lockfortrainer") for x in nomes):
                    continue
                if any(x in ("release", "releaseall") for x in nomes):
                    continue
                if self._solta_por_msgbox(cmds):
                    continue
                if "waitstate" in nomes and any(
                        x in ("special", "specialvar", "callnative")
                        for x in nomes):
                    continue
                if any(x in WARP_QUE_TROCA for x in nomes):
                    continue
                if any(x in ("startcontest", "contestlinktransfer",
                             "choosecontestmon", "playslotmachine",
                             "endram", "returnram") for x in nomes):
                    continue
                self.add("C01", "trava", b.arquivo, b.linha, entrada,
                         "lock/lockall e NENHUM release em todo o alcance "
                         "(%d comandos varridos)" % len(cmds))

    def c02_release_faltando_num_ramo(self):
        """C02: caminho concreto que chega a `end` ainda travado."""
        for mapa in sorted(self.arv.mapas):
            for entrada in sorted(self.entradas_do_mapa(mapa)):
                if self.bloco(entrada) is None:
                    continue
                self._anda_travado(entrada)

    def _anda_travado(self, entrada):
        vistos = set()
        pilha = [(entrada, False, 0)]
        while pilha:
            rot, trancado, prof = pilha.pop()
            if (rot, trancado) in vistos or prof > 120:
                continue
            vistos.add((rot, trancado))
            b = self.bloco(rot)
            if b is None:
                continue
            estado = trancado
            for (n, nome, args) in b.cmds:
                if nome in ("lock", "lockall", "lockfortrainer"):
                    estado = True
                elif nome in ("release", "releaseall"):
                    estado = False
                elif nome == "msgbox" and len(args) >= 2 and \
                        args[1].strip() in ("MSGBOX_SIGN", "MSGBOX_NPC",
                                            "MSGBOX_AUTOCLOSE"):
                    estado = False
                elif nome in ("callstd", "gotostd") and args and \
                        args[0].strip() in ("STD_MSGBOX_SIGN", "STD_MSGBOX_NPC"):
                    estado = False
                elif nome in WARP_QUE_TROCA or \
                        nome in ("startcontest", "contestlinktransfer",
                                 "playslotmachine", "choosecontestmon"):
                    estado = False
                elif nome == "waitstate" and any(
                        c[1] in ("special", "specialvar", "callnative",
                                 "dofieldeffect", "fadescreenswapbuffers")
                        for c in b.cmds):
                    estado = False
                elif nome.startswith("trainerbattle"):
                    alvo = self.roteiro_pos_batalha(nome, args)
                    if alvo:
                        pilha.append((alvo, estado, prof + 1))
                        break
                elif nome in TERMINADORES:
                    if estado and nome == "end":
                        self.add("C02", "provável", b.arquivo, n, rot,
                                 "`end` com o jogador travado (entrada %s)" % entrada)
                    estado = False
                    break
                d = self.destino(nome, args)
                if d and d in self.arv.blocos:
                    if nome in CHAMADA or nome in CHAMADA_CMP:
                        sub = [c[1] for c in self.caminha(d)]
                        if any(x in ("release", "releaseall") for x in sub):
                            estado = False
                        if any(x in ("lock", "lockall") for x in sub):
                            pass
                    else:
                        pilha.append((d, estado, prof + 1))
                        if nome in SALTO_INCOND:
                            break
            else:
                prox = self.destino_de_bloco.get(id(b))
                if prox and prox in self.arv.blocos:
                    pilha.append((prox, estado, prof + 1))

    def c03_waitmovement_sem_applymovement(self):
        """C03: `waitmovement` sem `applymovement` antes no mesmo alcance."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                visto_apply = False
                for (n, nome, args) in b.cmds:
                    if nome == "applymovement":
                        visto_apply = True
                    elif nome in ("waitmovement", "waitmovementall") and not visto_apply:
                        # pode ter vindo de bloco anterior por queda ou de um call
                        if self._apply_antes(b, caminho):
                            continue
                        self.add("C03", "cosmético", caminho, n, b.rotulo,
                                 "`%s` sem `applymovement` antes em nenhum "
                                 "caminho de entrada" % nome)

    def _apply_antes(self, bloco, caminho):
        """Algum bloco que cai/salta para este tem applymovement?"""
        for b2 in self.arv.arquivos[caminho]:
            if b2 is bloco:
                continue
            tem_apply = any(c[1] == "applymovement" for c in b2.cmds)
            if not tem_apply:
                continue
            if self.destino_de_bloco.get(id(b2)) == bloco.rotulo and not self._termina(b2):
                return True
            for (n, nome, args) in b2.cmds:
                if self.destino(nome, args) == bloco.rotulo:
                    return True
        # entradas de outros arquivos
        for rot in (self.chamados | self.saltados):
            pass
        return False

    def c04_localid_inexistente(self):
        """C04: comando de objeto com local id que o mapa não tem."""
        for caminho, blocos in self.arv.arquivos.items():
            mapa = self.arv.mapa_do_arquivo.get(caminho)
            if not mapa:
                continue
            n_obj = len(self.arv.objetos_do_mapa(mapa))
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    if nome not in CMD_LOCALID or not args:
                        continue
                    # com argumento de mapa explícito, o alvo é outro mapa
                    if nome in ("applymovement", "waitmovement", "removeobject",
                                "addobject") and len(args) >= 3:
                        continue
                    if nome in ("showobjectat", "hideobjectat",
                                "setobjectsubpriority", "resetobjectsubpriority"):
                        continue
                    alvo = args[0].strip()
                    if alvo in LOCALID_LIVRE or alvo.startswith("VAR_"):
                        continue
                    v = leitor.resolve_num(alvo, self.arv.defines)
                    if v is None:
                        continue
                    if v == 0 and nome == "waitmovement":
                        continue
                    if v >= 240 or v == 127:
                        continue
                    if v > n_obj:
                        self.add("C04", "trava" if nome == "applymovement"
                                 else "provável", caminho, n, b.rotulo,
                                 "%s id %s (=%d) e o mapa %s tem %d objetos"
                                 % (nome, alvo, v, mapa, n_obj))

    def c05_goto_para_outro_mapa(self):
        """C05: `goto`/`call` para rótulo definido no scripts.inc de outro mapa."""
        for caminho, blocos in self.arv.arquivos.items():
            mapa = self.arv.mapa_do_arquivo.get(caminho)
            if not mapa:
                continue
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    d = self.destino(nome, args)
                    if not d:
                        continue
                    alvo = self.arv.blocos.get(d)
                    if alvo is None or alvo.arquivo == caminho:
                        continue
                    outro = self.arv.mapa_do_arquivo.get(alvo.arquivo)
                    if outro is None:
                        continue  # data/scripts compartilhado: legítimo
                    self.add("C05", "provável", caminho, n, b.rotulo,
                             "%s para %s, que mora em %s" % (nome, d, outro))

    def c06_return_sem_call(self):
        """C06: bloco com `return` que ninguém `call`."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                tem_return = any(c[1] == "return" for c in b.cmds)
                if not tem_return:
                    continue
                if b.rotulo in self.chamados:
                    continue
                # pode ser continuação por queda de um bloco chamado
                if self._alcancavel_por_call(b, caminho):
                    continue
                self.add("C06", "provável", caminho,
                         [c[0] for c in b.cmds if c[1] == "return"][0], b.rotulo,
                         "`return` num rótulo que nenhum `call` alcança")

    def _alcancavel_por_call(self, bloco, caminho, prof=0):
        if prof > 6:
            return True
        for b2 in self.arv.arquivos[caminho]:
            if b2 is bloco:
                continue
            cai = (self.destino_de_bloco.get(id(b2)) == bloco.rotulo
                   and not self._termina(b2))
            salta = any(self.destino(c[1], c[2]) == bloco.rotulo for c in b2.cmds)
            if cai or salta:
                if b2.rotulo in self.chamados:
                    return True
                if self._alcancavel_por_call(b2, caminho, prof + 1):
                    return True
        return False

    def c07_queda_em_texto(self):
        """C07: bloco de código sem terminador que cai num rótulo de texto."""
        for caminho, blocos in self.arv.arquivos.items():
            for i, b in enumerate(blocos):
                if i + 1 >= len(blocos):
                    continue
                if not b.cmds or self._termina(b) or self._e_dado(b):
                    continue
                if not any(not c[1].startswith(".") for c in b.cmds):
                    continue
                prox = blocos[i + 1]
                if prox.textos:
                    self.add("C07", "trava", caminho, b.cmds[-1][0], b.rotulo,
                             "cai em %s, que é texto: o motor executa letra "
                             "como bytecode" % prox.rotulo)

    def c08_queda_no_fim_do_arquivo(self):
        """C08: último bloco do arquivo sem terminador."""
        for caminho, blocos in self.arv.arquivos.items():
            if not blocos:
                continue
            b = blocos[-1]
            if not b.cmds or self._termina(b) or self._e_dado(b):
                continue
            if not any(not c[1].startswith(".") for c in b.cmds):
                continue
            self.add("C08", "trava", caminho, b.cmds[-1][0], b.rotulo,
                     "último bloco do arquivo sem end/return/goto")

    def c09_msgbox_tipo_invalido(self):
        """C09: `msgbox` com segundo argumento que não é MSGBOX_*."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    if nome != "msgbox" or len(args) < 2:
                        continue
                    t = args[1].strip()
                    if t in MSGBOX_OK:
                        continue
                    if leitor.resolve_num(t, self.arv.defines) is not None:
                        self.add("C09", "cosmético", caminho, n, b.rotulo,
                                 "msgbox com tipo numérico %s" % t)
                    else:
                        self.add("C09", "provável", caminho, n, b.rotulo,
                                 "msgbox com tipo desconhecido %s" % t)

    def c10_warp_sem_waitstate(self):
        """C10: `warp` sem `waitstate` logo depois (troca de mapa não acontece)."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                cmds = [c for c in b.cmds if not c[1].startswith(".")]
                for i, (n, nome, args) in enumerate(cmds):
                    if nome not in WARP_QUE_TROCA:
                        continue
                    depois = [c[1] for c in cmds[i + 1:i + 4]]
                    if "waitstate" in depois:
                        continue
                    if depois and depois[0] in ("release", "releaseall"):
                        self.add("C10", "trava", caminho, n, b.rotulo,
                                 "%s seguido de %s antes de waitstate"
                                 % (nome, depois[0]))
                    else:
                        self.add("C10", "provável", caminho, n, b.rotulo,
                                 "%s sem waitstate nas 3 linhas seguintes (%s)"
                                 % (nome, ",".join(depois) or "fim do bloco"))

    def c11_special_por_indice(self):
        """C11: `special` com número em vez de nome, ou nome fora de specials.inc."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    if nome not in ("special", "specialvar") or not args:
                        continue
                    alvo = args[-1].strip() if nome == "specialvar" else args[0].strip()
                    if alvo in self.arv.specials:
                        continue
                    if re.match(r"^[-+0-9]", alvo):
                        self.add("C11", "trava", caminho, n, b.rotulo,
                                 "%s por índice numérico (%s)" % (nome, alvo))
                    else:
                        self.add("C11", "provável", caminho, n, b.rotulo,
                                 "%s %s fora de data/specials.inc" % (nome, alvo))

    def c12_flag_e_var_fora_da_faixa(self):
        """C12: setflag/clearflag/setvar com número acima do teto."""
        teto_flag = leitor.resolve_num("FLAGS_COUNT", self.arv.defines) or 0x1000
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    if nome in ("setflag", "clearflag", "checkflag") and args:
                        v = leitor.resolve_num(args[0], self.arv.defines)
                        esp = 0x4000 <= v <= 0x407F if v is not None else False
                        if v is not None and v >= teto_flag and not esp:
                            self.add("C12", "trava", caminho, n, b.rotulo,
                                     "%s %s (=%d) acima de FLAGS_COUNT (%d)"
                                     % (nome, args[0], v, teto_flag))
                    if nome in ("setvar", "addvar", "subvar", "compare") and args:
                        v = leitor.resolve_num(args[0], self.arv.defines)
                        if v is not None and not (VAR_MIN <= v <= VAR_MAX
                                                  or 0x8000 <= v <= 0x8020):
                            self.add("C12", "provável", caminho, n, b.rotulo,
                                     "%s em %s (=0x%X), fora da faixa de var"
                                     % (nome, args[0], v))

    def c13_nivel_impossivel(self):
        """C13: givemon/setwildbattle/createmon com nível 0 ou acima de 100."""
        for caminho, blocos in self.arv.arquivos.items():
            reg = self.arv.regiao_do_arquivo(caminho)
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    if nome == "givemon" and len(args) >= 2:
                        idx = 1
                    elif nome == "setwildbattle" and len(args) >= 2:
                        idx = 1
                    elif nome == "createmon" and len(args) >= 4:
                        idx = 3
                    elif nome == "seteventmon" and len(args) >= 2:
                        idx = 1
                    else:
                        continue
                    v = leitor.resolve_num(args[idx], self.arv.defines)
                    if v is None:
                        continue
                    if v == 255:
                        continue
                    if v <= 0 or v > 100:
                        self.add("C13", "provável", caminho, n, b.rotulo,
                                 "%s com nível %s (=%s)" % (nome, args[idx], v))

    def c14_flag_lida_que_ninguem_acende(self):
        """C14: checkflag/goto_if_set de flag que nenhum script nem C acende."""
        for flag, _ in sorted(self.flags_lidas.items()):
            if not flag.startswith("FLAG_"):
                continue
            if self.flags_acesas.get(flag) or flag in self.flags_c:
                continue
            if any(p in flag for p in ("_SYS_", "_BADGE", "_RECEIVED",
                                       "_TEMP_", "_HIDDEN_ITEM", "_ITEM_",
                                       "_LANDMARK", "_UNUSED", "_DEFEATED")):
                classe = "cosmético"
            else:
                classe = "provável"
            ondes = self._onde_flag(flag)
            for (caminho, n, rot) in ondes[:3]:
                self.add("C14", classe, caminho, n, rot,
                         "lê %s, que nenhum setflag nem FlagSet acende" % flag)

    def _onde_flag(self, flag):
        out = []
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    if args and args[0].strip() == flag and nome in (
                            "checkflag", "goto_if_set", "goto_if_unset",
                            "call_if_set", "call_if_unset"):
                        out.append((caminho, n, b.rotulo))
        return out

    def c15_objeto_com_flag_orfa(self):
        """C15: objeto de mapa escondido por flag que ninguém apaga (nunca aparece)."""
        for mapa, j in sorted(self.arv.mapas.items()):
            for i, ev in enumerate(j.get("object_events") or [], 1):
                f = (ev.get("flag") or "0").strip()
                if f in ("", "0", "0x0"):
                    continue
                if not f.startswith("FLAG_"):
                    continue
                acende = self.flags_acesas.get(f, 0)
                apaga = self.flags_apagadas.get(f, 0)
                if apaga == 0 and f not in self.flags_c:
                    if acende == 0:
                        continue  # nasce apagada: objeto visível, normal
                    self.add("C15", "cosmético",
                             os.path.join(self.raiz, "data", "maps", mapa, "map.json"),
                             i, "objeto %d" % i,
                             "escondido por %s, que %d setflag acende e "
                             "NENHUM clearflag apaga: some para sempre"
                             % (f, acende), mapa=mapa)

    def c16_flag_de_esconder_sem_ninguem(self):
        """C16: flag de esconder objeto que nenhum objeto usa (setflag inócuo)."""
        usadas = set()
        for mapa, j in self.arv.mapas.items():
            for ev in j.get("object_events") or []:
                f = (ev.get("flag") or "0").strip()
                if f not in ("", "0", "0x0"):
                    usadas.add(f)
        for flag, cont in sorted(self.flags_acesas.items()):
            if "ESCONDE" not in flag and "HIDE" not in flag:
                continue
            if flag in usadas:
                continue
            if self.flags_lidas.get(flag):
                continue
            achou = False
            for caminho, blocos in self.arv.arquivos.items():
                for b in blocos:
                    for (n, nome, args) in b.cmds:
                        if nome in ("setflag", "clearflag") and args and \
                                args[0].strip() == flag:
                            self.add("C16", "provável", caminho, n, b.rotulo,
                                     "%s %s, mas nenhum objeto de mapa usa "
                                     "essa flag" % (nome, flag))
                            achou = True
                            break
                    if achou:
                        break
                if achou:
                    break

    def c17_trainer_repetido(self):
        """C17: mesmo id de treinador em dois objetos diferentes."""
        for t, usos in sorted(self.trainer_usos.items()):
            locais = {(u[0], u[2]) for u in usos}
            mapas = {self.arv.mapa_do_arquivo.get(u[0]) for u in usos}
            mapas.discard(None)
            if len(mapas) > 1:
                c, n, rot, _ = usos[0]
                self.add("C17", "provável", c, n, rot,
                         "%s aparece em %d mapas: %s" %
                         (t, len(mapas), ", ".join(sorted(mapas))[:120]))

    def c18_mapscript_tabela(self):
        """C18: MAP_SCRIPT_ON_FRAME_TABLE/ON_TRANSITION com var ou alvo suspeito."""
        for caminho, blocos in self.arv.arquivos.items():
            mapa = self.arv.mapa_do_arquivo.get(caminho)
            if not mapa:
                continue
            for b in blocos:
                for (n, nome, args) in b.cmds:
                    if nome == "map_script" and len(args) >= 2:
                        alvo = args[1].strip()
                        if alvo not in self.arv.blocos:
                            self.add("C18", "trava", caminho, n, b.rotulo,
                                     "map_script aponta para %s, que não existe"
                                     % alvo)
                    if nome == "map_script_2" and len(args) >= 3:
                        var = args[0].strip()
                        alvo = args[2].strip()
                        v = leitor.resolve_num(var, self.arv.defines)
                        if v is None:
                            self.add("C18", "provável", caminho, n, b.rotulo,
                                     "ON_FRAME_TABLE com var %s que não resolve"
                                     % var)
                        elif not (VAR_MIN <= v <= VAR_MAX):
                            self.add("C18", "trava", caminho, n, b.rotulo,
                                     "ON_FRAME_TABLE com var %s (=0x%X) fora "
                                     "da faixa" % (var, v))
                        if alvo not in self.arv.blocos:
                            self.add("C18", "trava", caminho, n, b.rotulo,
                                     "ON_FRAME_TABLE aponta para %s, que não "
                                     "existe" % alvo)

    def c19_objeto_sem_script_nem_movimento(self):
        """C19: objeto com script que aponta para rótulo inexistente."""
        for mapa, j in sorted(self.arv.mapas.items()):
            for i, ev in enumerate(j.get("object_events") or [], 1):
                s = (ev.get("script") or "0").strip()
                if s in ("", "0", "0x0", "NULL"):
                    continue
                if s not in self.arv.blocos:
                    self.add("C19", "trava",
                             os.path.join(self.raiz, "data", "maps", mapa, "map.json"),
                             i, "objeto %d" % i,
                             "script %s não existe em .inc nenhum" % s, mapa=mapa)
            for chave in ("bg_events", "coord_events"):
                for i, ev in enumerate(j.get(chave) or [], 1):
                    s = (ev.get("script") or "0").strip()
                    if s in ("", "0", "0x0", "NULL"):
                        continue
                    if s not in self.arv.blocos:
                        self.add("C19", "trava",
                                 os.path.join(self.raiz, "data", "maps", mapa,
                                              "map.json"),
                                 i, "%s %d" % (chave, i),
                                 "script %s não existe em .inc nenhum" % s,
                                 mapa=mapa)

    def c20_rotulo_orfao(self):
        """C20: rótulo de script que nada alcança (código morto)."""
        alcancados = self.chamados | self.saltados
        for mapa, j in self.arv.mapas.items():
            alcancados |= self.entradas_do_mapa(mapa)
        for caminho, blocos in self.arv.arquivos.items():
            mapa = self.arv.mapa_do_arquivo.get(caminho)
            if not mapa:
                continue
            for i, b in enumerate(blocos):
                if b.textos or not b.cmds:
                    continue
                if b.rotulo in alcancados:
                    continue
                if i > 0 and not self._termina(blocos[i - 1]):
                    continue
                if b.rotulo.endswith("_MapScripts"):
                    continue
                if "EventScript" not in b.rotulo:
                    continue
                if self._e_dado(b):
                    continue
                reais = [c for c in b.cmds if not c[1].startswith(".")]
                if len(reais) < 4:
                    continue
                self.add("C20", "cosmético", caminho, b.linha, b.rotulo,
                         "cena de %d comandos que nenhum goto/call/mapa "
                         "alcança" % len(reais))

    def c21_lock_duplo(self):
        """C21: `lock` depois de `lock` sem release no meio (fila de trava)."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                travado = False
                for (n, nome, args) in b.cmds:
                    if nome in ("lock", "lockall"):
                        if travado:
                            self.add("C21", "cosmético", caminho, n, b.rotulo,
                                     "%s repetido sem release no meio" % nome)
                        travado = True
                    elif nome in ("release", "releaseall"):
                        travado = False

    def c22_removeobject_depois_de_batalha(self):
        """C22: `removeobject VAR_LAST_TALKED` depois de trainerbattle (corrida)."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                viu_batalha = False
                for (n, nome, args) in b.cmds:
                    if nome.startswith("trainerbattle") or nome == "dotrainerbattle":
                        viu_batalha = True
                    elif nome in ("removeobject", "hideobjectat") and args and \
                            args[0].strip() == "VAR_LAST_TALKED" and viu_batalha:
                        self.add("C22", "provável", caminho, n, b.rotulo,
                                 "%s VAR_LAST_TALKED depois de batalha: "
                                 "VAR_LAST_TALKED pode ter mudado" % nome)


    def c23_no_intro_sem_guarda(self):
        """C23: `trainerbattle_no_intro` sem guarda de flag antes (rebatalha eterna).

        `trainerbattle_no_intro` NAO consulta a flag do treinador: sem um
        `goto_if_defeated`/`goto_if_set` antes, o NPC briga toda vez que o
        jogador fala com ele.
        """
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                for i, (n, nome, args) in enumerate(b.cmds):
                    if nome != "trainerbattle_no_intro":
                        continue
                    antes = [c[1] for c in b.cmds[:i]]
                    guarda = any(x in ("goto_if_defeated", "goto_if_set",
                                       "goto_if_unset", "checktrainerflag",
                                       "checkflag", "goto_if_not_defeated",
                                       "goto_if_eq", "goto_if_ne", "switch")
                                 for x in antes)
                    if guarda:
                        continue
                    if self._guarda_a_montante(b.rotulo):
                        continue
                    if not self._so_por_fala(b.rotulo):
                        continue
                    self.add("C23", "provável", caminho, n, b.rotulo,
                             "trainerbattle_no_intro %s sem guarda de flag: "
                             "rebriga a cada fala" % args[0].strip())

    def _guarda_a_montante(self, rotulo, prof=0):
        if prof > 4:
            return True
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                for i, (n, nome, args) in enumerate(b.cmds):
                    if self.destino(nome, args) == rotulo:
                        antes = [c[1] for c in b.cmds[:i + 1]]
                        if any(x in ("goto_if_defeated", "goto_if_set",
                                     "goto_if_unset", "goto_if_not_defeated",
                                     "checktrainerflag", "checkflag")
                               for x in antes):
                            return True
        return False

    def _entradas_que_alcancam(self):
        """rotulo alcancavel -> conjunto de tipos de entrada (objeto/coord/bg)."""
        if getattr(self, "_cache_entradas", None) is not None:
            return self._cache_entradas
        tipos = collections.defaultdict(set)
        for mapa, j in self.arv.mapas.items():
            for chave, tipo in (("object_events", "objeto"),
                                ("coord_events", "coord"),
                                ("bg_events", "placa")):
                for ev in j.get(chave) or []:
                    s2 = (ev.get("script") or "0").strip()
                    if s2 in ("", "0", "0x0"):
                        continue
                    marca = tipo
                    if tipo == "coord" and (ev.get("var") or "0") not in ("0", ""):
                        marca = "coord_com_var"
                    for (n, nome, args) in self.caminha(s2):
                        pass
                    for rot in self._alcance_rotulos(s2):
                        tipos[rot].add(marca)
        self._cache_entradas = tipos
        return tipos

    def _alcance_rotulos(self, rotulo, vis=None, prof=0):
        if vis is None:
            vis = set()
        if rotulo in vis or prof > 120 or rotulo not in self.arv.blocos:
            return vis
        vis.add(rotulo)
        b = self.bloco(rotulo)
        for (n, nome, args) in b.cmds:
            d = self.destino(nome, args)
            if d:
                self._alcance_rotulos(d, vis, prof + 1)
        prox = self.destino_de_bloco.get(id(b))
        if prox and not self._termina(b):
            self._alcance_rotulos(prox, vis, prof + 1)
        return vis

    def _so_por_fala(self, rotulo):
        tipos = self._entradas_que_alcancam().get(rotulo, set())
        if not tipos:
            return False
        return tipos <= {"objeto", "placa"}

    def c24_objeto_com_flag_intocada(self):
        """C24: objeto escondido por flag que NENHUM script acende nem apaga."""
        for mapa, j in sorted(self.arv.mapas.items()):
            for i, ev in enumerate(j.get("object_events") or [], 1):
                f = (ev.get("flag") or "0").strip()
                if f in ("", "0", "0x0") or not f.startswith("FLAG_"):
                    continue
                if self.flags_acesas.get(f) or self.flags_apagadas.get(f) \
                        or f in self.flags_c:
                    continue
                self.add("C24", "cosmético",
                         os.path.join(self.raiz, "data", "maps", mapa, "map.json"),
                         i, "objeto %d" % i,
                         "flag %s nunca é acesa nem apagada: o objeto está "
                         "sempre visível e a flag é enfeite" % f, mapa=mapa)

    def c25_transicao_esconde_obrigatorio(self):
        """C25: ON_TRANSITION/ON_LOAD do mapa acende flag de esconder de objeto DELE."""
        for caminho, blocos in self.arv.arquivos.items():
            mapa = self.arv.mapa_do_arquivo.get(caminho)
            if not mapa:
                continue
            flags_do_mapa = {}
            for i, ev in enumerate(self.arv.objetos_do_mapa(mapa), 1):
                f = (ev.get("flag") or "0").strip()
                if f.startswith("FLAG_"):
                    flags_do_mapa.setdefault(f, []).append((i, ev))
            if not flags_do_mapa:
                continue
            tabela = self.bloco("%s_MapScripts" % mapa)
            if tabela is None:
                continue
            alvos = [a[2][1].strip() for a in
                     [(x[0], x[1], x[2]) for x in tabela.cmds]
                     if a[1] == "map_script" and len(a[2]) >= 2 and
                     a[2][0].strip() in ("MAP_SCRIPT_ON_TRANSITION",
                                         "MAP_SCRIPT_ON_LOAD",
                                         "MAP_SCRIPT_ON_RESUME")]
            for alvo in alvos:
                for (n, nome, args) in self._trecho_incondicional(alvo):
                    if nome != "setflag" or not args:
                        continue
                    f = args[0].strip()
                    if f in flags_do_mapa and not self.flags_apagadas.get(f):
                        ids = [str(x[0]) for x in flags_do_mapa[f]]
                        self.add("C25", "provável", caminho, n, alvo,
                                 "a tabela do mapa acende %s ao entrar e "
                                 "nenhum clearflag apaga: objeto(s) %s de %s "
                                 "somem sempre" % (f, ",".join(ids), mapa))

    def _trecho_incondicional(self, rotulo, prof=0):
        """Comandos que rodam SEM depender de nenhuma condicional."""
        if prof > 30:
            return []
        b = self.bloco(rotulo)
        if b is None:
            return []
        saida = []
        for (n, nome, args) in b.cmds:
            if nome in SALTO_COND or nome in SALTO_CMP or nome in CHAMADA_CMP \
                    or nome in ("call_if", "call_if_set", "call_if_unset",
                                "call_if_defeated", "call_if_not_defeated",
                                "gotostd_if", "callstd_if"):
                return saida
            saida.append((n, nome, args))
            if nome in ("call", "vcall") and args:
                saida += self._trecho_incondicional(args[0].strip(), prof + 1)
            if nome in SALTO_INCOND and args:
                return saida + self._trecho_incondicional(args[0].strip(), prof + 1)
            if nome in TERMINADORES:
                return saida
        prox = self.destino_de_bloco.get(id(b))
        if prox and not self._termina(b):
            saida += self._trecho_incondicional(prox, prof + 1)
        return saida

    def c26_mexe_em_objeto_removido(self):
        """C26: `applymovement`/`turnobject` num id que o mesmo bloco já removeu."""
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                removidos = set()
                for (n, nome, args) in b.cmds:
                    if not args:
                        continue
                    alvo = args[0].strip()
                    if nome in ("removeobject", "hideobjectat"):
                        removidos.add(alvo)
                    elif nome in ("addobject", "showobjectat"):
                        removidos.discard(alvo)
                    elif nome in ("applymovement", "turnobject", "setobjectxy") \
                            and alvo in removidos:
                        self.add("C26", "provável", caminho, n, b.rotulo,
                                 "%s no id %s depois de removeobject no mesmo "
                                 "bloco" % (nome, alvo))

    def c27_checkflag_sem_consumidor(self):
        """C27: `checkflag`/`compare` cujo resultado ninguém lê na sequência."""
        consumidores = {"goto_if", "call_if", "vgoto_if", "vcall_if",
                        "goto_if_eq", "goto_if_ne", "goto_if_lt", "goto_if_gt",
                        "goto_if_le", "goto_if_ge", "call_if_eq", "call_if_ne",
                        "call_if_lt", "call_if_gt", "call_if_le", "call_if_ge",
                        "gotostd_if", "callstd_if", "case", "trycompare"}
        for caminho, blocos in self.arv.arquivos.items():
            for b in blocos:
                reais = [c for c in b.cmds if not c[1].startswith(".")]
                for i, (n, nome, args) in enumerate(reais):
                    if nome not in ("checkflag", "checktrainerflag"):
                        continue
                    seg = reais[i + 1][1] if i + 1 < len(reais) else None
                    if seg in consumidores:
                        continue
                    self.add("C27", "cosmético", caminho, n, b.rotulo,
                             "%s sem goto_if/call_if depois (o resultado "
                             "morre; o seguinte é %s)" % (nome, seg))

    # ---------------------------------------------------------------- execução
    # ------------------------------------------------------------------ C28
    # Modos de `trainerbattle` que passam por `special SetTrainerFacingDirection`
    # (data/scripts/trainer_battle.inc, linhas 19, 34, 61 e 78). Esse special
    # (src/battle_setup.c:1258) tem `assertf(gSelectedObjectEvent !=
    # gPlayerAvatar.objectEventId)`, ou seja EXIGE um objeto de evento
    # selecionado. Os demais modos caem em `EventScript_DoNoIntroTrainerBattle`
    # e não o chamam.
    MODO_PEDE_OBJETO = {
        "TRAINER_BATTLE_SINGLE",
        "TRAINER_BATTLE_DOUBLE",
        "TRAINER_BATTLE_CONTINUE_SCRIPT",
        "TRAINER_BATTLE_CONTINUE_SCRIPT_NO_MUSIC",
        "TRAINER_BATTLE_CONTINUE_SCRIPT_DOUBLE",
        "TRAINER_BATTLE_CONTINUE_SCRIPT_DOUBLE_NO_MUSIC",
        "TRAINER_BATTLE_REMATCH",
        "TRAINER_BATTLE_REMATCH_DOUBLE",
    }
    MACRO_PEDE_OBJETO = {
        "trainerbattle_single": "TRAINER_BATTLE_SINGLE/CONTINUE_SCRIPT",
        "trainerbattle_double": "TRAINER_BATTLE_DOUBLE/CONTINUE_SCRIPT_DOUBLE",
        "trainerbattle_rematch": "TRAINER_BATTLE_REMATCH",
        "trainerbattle_rematch_double": "TRAINER_BATTLE_REMATCH_DOUBLE",
    }
    # Entradas do motor em que NÃO há objeto selecionado quando o script começa.
    # `ProcessPlayerFieldInput` zera `gSelectedObjectEvent`
    # (src/field_control_avatar.c:169) e só `GetInteractedObjectEventScript`
    # (linha 420) e o avistamento de treinador (src/trainer_see.c:484) o
    # reatribuem. Gatilho de chão, placa e script de mapa não passam por
    # nenhum dos dois.
    # Moldes que caem em `EventScript_DoNoIntroTrainerBattle`: não chamam o
    # special, mas fazem `applymovement VAR_LAST_TALKED` do mesmo jeito.
    MACRO_SEM_INTRO = {"trainerbattle_no_intro", "trainerbattle_earlyrival",
                       "trainerbattle_two_trainers"}
    ENTRADA_SEM_OBJETO = {
        "coord_events": "gatilho de chão",
        "bg_events": "placa",
    }

    def _entradas_sem_objeto(self, mapa):
        """[(rótulo, de_onde)] das entradas do mapa que NÃO têm objeto."""
        j = self.arv.mapas.get(mapa) or {}
        out = []
        for chave, comofala in self.ENTRADA_SEM_OBJETO.items():
            for ev in j.get(chave) or []:
                alvo = (ev.get("script") or "0").strip()
                if alvo in ("", "0", "0x0", "NULL"):
                    continue
                out.append((alvo, "%s (%s,%s)" % (comofala, ev.get("x"),
                                                  ev.get("y"))))
        ms = self.bloco("%s_MapScripts" % mapa)
        if ms is not None:
            out += self._alvos_de_mapscripts(ms)
        return out

    def _alvos_de_mapscripts(self, bloco):
        """[(rótulo, tipo)] de um `<Mapa>_MapScripts`, tabela por dentro."""
        out = []
        for (n, nome, args) in bloco.cmds:
            if nome != "map_script" or len(args) < 2:
                continue
            tipo, alvo = args[0].strip(), args[1].strip()
            tabela = self.bloco(alvo)
            if tipo.endswith("_TABLE") and tabela is not None:
                for (n2, nm2, ar2) in tabela.cmds:
                    if nm2 == "map_script_2" and len(ar2) >= 3:
                        out.append((ar2[2].strip(), "%s/%s" % (tipo, alvo)))
            else:
                out.append((alvo, tipo))
        return out

    def c28_batalha_sem_objeto(self):
        """C28: batalha COM intro chamada de gatilho, placa ou script de mapa.

        Achado em 06/09/2026 pelo playtest do Gui: pisar na emboscada do
        `Unova_LentimasGym` dava TELA AZUL com
        `SRC/BATTLE_SETUP.C:1258: TRAINER SCRIPT THAT NEEDS TO BE USED FROM AN
        OBJECT EVENT WAS CALLED FROM PLAYER`. O motivo é de desenho, não de
        dado: `trainerbattle_single` e irmãos vão a
        `EventScript_TryDoNormalTrainerBattle`, que chama `special
        SetTrainerFacingDirection`, e esse special assere que
        `gSelectedObjectEvent` NÃO é o jogador. Num gatilho de chão, numa
        placa ou num script de mapa não há objeto selecionado, e
        `SetMapVarsToTrainerA` só reatribui quando o comando traz local id
        (os macros passam `LOCALID_NONE`). Vale em qualquer região.

        O conserto é o caminho SEM intro: `msgbox <intro>` +
        `trainerbattle_no_intro`, que cai em
        `EventScript_DoNoIntroTrainerBattle` e não toca no special. Como esse
        molde não confere a flag de vitória por dentro, o `goto_if_defeated`
        deixa de ser conforto e vira obrigação (e o C23 cobra isso).

        O que NÃO virou checagem, e o motivo está medido:
        `EventScript_DoNoIntroTrainerBattle` faz `applymovement
        VAR_LAST_TALKED, Movement_RevealTrainer` sem perguntar, e numa entrada
        sem objeto `gSpecialVar_LastTalked` vale `LOCALID_NONE`, que não é
        local id de objeto nenhum (`GetObjectEventIdByLocalId` devolve
        `OBJECT_EVENTS_COUNT`, src/event_object_movement.c:1490). São 196
        lugares na árvore e a maioria é VANILLA intocado
        (`EverGrandeCity_ChampionsRoom`, `FiveIsland_LostCave_Room10`,
        `EcruteakCity_Theater`): as três linhas de `applymovement` são acréscimo
        da pokeemerald-expansion para o seguidor, e o jogo roda com elas há
        anos. Cobrar isso seria 196 travas de falso positivo calibrado, pela
        regra da lição 4.10. O conserto de 06/09/2026 mesmo assim escreve
        `setvar VAR_LAST_TALKED, LOCALID_X` antes do `trainerbattle_no_intro`,
        porque é o idioma do FireRed vanilla
        (`Route24_EventScript_BattleRocket`) e custa uma linha.
        """
        vistos = set()
        for mapa in sorted(self.arv.mapas):
            for (entrada, de_onde) in self._entradas_sem_objeto(mapa):
                if self.bloco(entrada) is None:
                    continue
                for (n, nome, args) in self.caminha(entrada):
                    motivo = self.MACRO_PEDE_OBJETO.get(nome)
                    if motivo is None and nome == "trainerbattle" and args \
                            and args[0].strip() in self.MODO_PEDE_OBJETO:
                        motivo = args[0].strip()
                    if motivo is None:
                        continue
                    b = self.bloco(entrada)
                    dono = self.arv.blocos.get(entrada)
                    chave = (mapa, entrada, n, nome)
                    if chave in vistos:
                        continue
                    vistos.add(chave)
                    self.add("C28", "trava", b.arquivo, b.linha, entrada,
                             "%s (%s) alcançável de %s: sem objeto "
                             "selecionado, SetTrainerFacingDirection assere "
                             "em battle_setup.c:1258 (tela azul)"
                             % (nome, motivo, de_onde), mapa=mapa)

    CHECAGENS = ["c01_lock_sem_release", "c02_release_faltando_num_ramo",
                 "c03_waitmovement_sem_applymovement", "c04_localid_inexistente",
                 "c05_goto_para_outro_mapa", "c06_return_sem_call",
                 "c07_queda_em_texto", "c08_queda_no_fim_do_arquivo",
                 "c09_msgbox_tipo_invalido", "c10_warp_sem_waitstate",
                 "c11_special_por_indice", "c12_flag_e_var_fora_da_faixa",
                 "c13_nivel_impossivel", "c14_flag_lida_que_ninguem_acende",
                 "c15_objeto_com_flag_orfa", "c16_flag_de_esconder_sem_ninguem",
                 "c17_trainer_repetido", "c18_mapscript_tabela",
                 "c19_objeto_sem_script_nem_movimento", "c20_rotulo_orfao",
                 "c21_lock_duplo", "c22_removeobject_depois_de_batalha",
                 "c23_no_intro_sem_guarda", "c24_objeto_com_flag_intocada",
                 "c25_transicao_esconde_obrigatorio",
                 "c26_mexe_em_objeto_removido",
                 "c27_checkflag_sem_consumidor",
                 "c28_batalha_sem_objeto"]

    def roda(self, so=None):
        for nome in self.CHECAGENS:
            if so and not nome.upper().startswith(so.lower().replace("c", "c")):
                if not nome.startswith(so.lower()):
                    continue
            getattr(self, nome)()
        return self.achados


def resumo(achados, raiz):
    por_sigla = collections.Counter(a.sigla for a in achados)
    por_classe = collections.Counter(a.classe for a in achados)
    por_regiao = collections.Counter(a.regiao for a in achados)
    print("=== por checagem ===")
    for s in sorted(set(a.sigla for a in achados) | set()):
        cl = collections.Counter(a.classe for a in achados if a.sigla == s)
        rg = collections.Counter(a.regiao for a in achados if a.sigla == s)
        print("%-4s %5d  %s  %s" % (s, por_sigla[s], dict(cl), dict(rg)))
    print("=== por classe ===", dict(por_classe))
    print("=== por regiao ===", dict(por_regiao))
    print("total:", len(achados))


def demo():
    """Copia a árvore para /tmp, planta um defeito de cada família e cobra."""
    origem = leitor.RAIZ_PADRAO
    tmp = tempfile.mkdtemp(prefix="qa_scripts_demo_")
    for sub in ("data", "include", "asm", "charmap.txt"):
        s = os.path.join(origem, sub)
        d = os.path.join(tmp, sub)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=True)
        else:
            shutil.copy2(s, d)
    os.makedirs(os.path.join(tmp, "src"), exist_ok=True)

    alvo = os.path.join(tmp, "data", "maps", "LittlerootTown", "scripts.inc")
    with open(alvo, "a", encoding="utf-8") as fh:
        fh.write("""
QA_Demo_Trava::
\tlock
\tfaceplayer
\tapplymovement 99, QA_Demo_Movimento
\twaitmovement 0
\tspecial 0x42
\tmsgbox QA_Demo_Texto, MSGBOX_DEFAULT
\tend

QA_Demo_Warp::
\tlock
\twarp MAP_LITTLEROOT_TOWN, 0, 0
\trelease
\tend

QA_Demo_Gatilho::
\tlock
\tgoto_if_defeated TRAINER_QA_DEMO, QA_Demo_Gatilho_Fim
\ttrainerbattle_single TRAINER_QA_DEMO, QA_Demo_Texto, QA_Demo_Texto
QA_Demo_Gatilho_Fim:
\trelease
\tend

QA_Demo_Tabela::
\tmap_script_2 VAR_TEMP_1, 0, QA_Demo_Quadro
\t.2byte 0

QA_Demo_Quadro::
\tcall QA_Demo_Indireto
\tend

QA_Demo_Indireto::
\ttrainerbattle_rematch TRAINER_QA_DEMO, QA_Demo_Texto, QA_Demo_Texto
\treturn

QA_Demo_Texto:
\t.string "oi$"

QA_Demo_Movimento:
\tstep_end
""")
    # a checagem C01 so olha script que o MAPA alcanca: pendura o defeito
    # num objeto de verdade, senao a mutacao fica invisivel de proposito.
    # O C28 tem DOIS braços, e o de script de mapa não aparece no coord_event:
    # planta também um MAP_SCRIPT_ON_FRAME_TABLE com a batalha atrás de um
    # `call`, para a caminhada indireta ficar coberta.
    with open(alvo, encoding="utf-8") as fh:
        corpo = fh.read()
    corpo = corpo.replace(
        "LittlerootTown_MapScripts::\n",
        "LittlerootTown_MapScripts::\n"
        "\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, QA_Demo_Tabela\n", 1)
    with open(alvo, "w", encoding="utf-8") as fh:
        fh.write(corpo)

    mj = os.path.join(tmp, "data", "maps", "LittlerootTown", "map.json")
    j = json.load(open(mj))
    j["object_events"][0] = dict(j["object_events"][0])
    j["object_events"][0]["script"] = "QA_Demo_Trava"
    j["object_events"][1] = dict(j["object_events"][1])
    j["object_events"][1]["script"] = "QA_Demo_Warp"
    # C28 só morde o que o motor alcança SEM objeto: o gatilho de chão é a
    # única forma de plantar a mutação dele.
    j.setdefault("coord_events", []).append(
        {"type": "trigger", "x": 9, "y": 9, "elevation": 0,
         "var": "VAR_TEMP_0", "var_value": "0", "script": "QA_Demo_Gatilho"})
    json.dump(j, open(mj, "w"))
    v = Varredura(tmp)
    v.roda()
    por = collections.Counter(a.sigla for a in v.achados
                              if "QA_Demo" in a.rotulo or "QA_Demo" in a.texto)
    esperado = {"C01", "C04", "C10", "C11", "C28"}
    achou = set(por)
    print("demo: plantado em %s" % alvo)
    print("demo: siglas que morderam:", sorted(achou))
    # O C28 tem que morder pelos DOIS braços, e não só pelo gatilho: sem esta
    # cobrança, perder o braço de script de mapa passaria calado.
    c28 = [a.texto for a in v.achados
           if a.sigla == "C28" and "QA_Demo" in a.rotulo]
    bracos = {("gatilho" if "gatilho" in t else
               "mapscript" if "MAP_SCRIPT" in t else "?") for t in c28}
    if bracos != {"gatilho", "mapscript"}:
        print("DEMO VERMELHO: C28 mordeu só", sorted(bracos))
        shutil.rmtree(tmp, ignore_errors=True)
        return 1
    faltou = esperado - achou
    if faltou:
        print("DEMO VERMELHO: não mordeu", sorted(faltou))
        shutil.rmtree(tmp, ignore_errors=True)
        return 1
    print("DEMO VERDE: as cinco famílias plantadas foram pegas")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", default=leitor.RAIZ_PADRAO)
    ap.add_argument("--detalhe", help="sigla (C01...) para listar tudo")
    ap.add_argument("--limite", type=int, default=40)
    ap.add_argument("--json")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    v = Varredura(a.raiz)
    v.roda()
    if a.detalhe:
        sel = [x for x in v.achados if x.sigla == a.detalhe.upper()]
        for x in sel[:a.limite]:
            print(x.linha_curta(a.raiz))
        print("(%d de %d)" % (min(len(sel), a.limite), len(sel)))
    else:
        resumo(v.achados, a.raiz)
    if a.json:
        json.dump([x.como_dict() for x in v.achados], open(a.json, "w"),
                  ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
