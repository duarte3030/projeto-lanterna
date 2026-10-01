#ifndef GUARD_KIT_PLAYTEST_H
#define GUARD_KIT_PLAYTEST_H

// Kit de playtest da mochila (pedido do Gui, 30/09/2026). Interruptor em
// include/config/debug.h, PLAYTEST_KIT_MOCHILA. Explicação inteira em
// src/kit_playtest.c.

extern const u8 KitPlaytest_EventScript_Entregue[];
extern const u8 KitPlaytest_EventScript_EntregueSemEspaco[];

// Entrega o kit e acende FLAG_KIT_PLAYTEST_ENTREGUE. Devolve quantos tipos de
// item ficaram de fora por falta de vaga (0 = tudo coube).
u32 KitPlaytest_Entrega(void);

// Chamada a cada quadro em que o jogador tem o controle do campo
// (ProcessPlayerFieldInput). Devolve TRUE se abriu o aviso.
bool32 KitPlaytest_TentaEntregarNaSaveAntiga(void);

#endif // GUARD_KIT_PLAYTEST_H
