#include "global.h"
#include "battle_pyramid.h"
#include "event_data.h"
#include "item.h"
#include "kit_playtest.h"
#include "script.h"
#include "constants/items.h"
#include "constants/tms_hms.h"

// ============================================================================
// KIT DE PLAYTEST DA MOCHILA (pedido do Gui, 30/09/2026)
// ============================================================================
//
// PARA QUE SERVE
//
// O Gui joga para testar. Comprar bola, cura e TM a cada trecho é pedágio, então
// a mochila dele chega cheia: todos os TM e HM, Poké Balls variadas, berries de
// batalha, cura, PP, vitaminas e X-itens.
//
// QUANDO ENTRA, E SÓ UMA VEZ
//
//   1. Jogo novo: NewGameInitData (src/new_game.c) chama KitPlaytest_Entrega
//      depois do ClearBag. Sem aviso na tela, de propósito: um aviso ali
//      apareceria logo depois do seletor de capítulo, comeria os apertos da
//      abertura de todos os casos da suíte e o warp de debug não abriria.
//   2. Save que já existe (a do Gui, feita na ROM bugs2b): no primeiro quadro em
//      que o jogador tem o controle do campo, ProcessPlayerFieldInput
//      (src/field_control_avatar.c) vê FLAG_KIT_PLAYTEST_ENTREGUE apagada,
//      entrega e mostra um aviso curto.
//
// Nos dois casos a flag acende junto, e ela mora no SaveBlock1: recarregar a
// save não entrega de novo. O interruptor é PLAYTEST_KIT_MOCHILA, em
// include/config/debug.h. Desligado, este arquivo não entrega nada.
//
// REGRAS DA ENTREGA
//
// - SOMA ao que já está na mochila, nunca apaga nada, e nunca passa de 999 por
//   item (MAX_BAG_ITEM_CAPACITY). Item que já está na mochila só ganha
//   quantidade, sem gastar vaga.
// - Item NOVO só entra se o bolso ainda tiver mais vagas livres que a reserva
//   do bolso (sReservaDoBolso). A reserva existe para o jogo continuar
//   entregando item novo ao Gui (NPC, item no chão, loja): bolso lotado pelo
//   kit faria o jogo responder "mochila cheia" a cada achado. Quando um item
//   não cabe, ele fica de fora, a lista segue (os seguintes ainda podem só
//   somar a uma pilha que já existe), e o aviso diz que nem tudo coube.
// - A lista está em ordem de prioridade dentro de cada bolso: se faltar vaga,
//   sai o fim da lista.
// - Bolso de itens-chave não é tocado: nada de progresso, nada de flag de
//   história. O Gui já tem Infinite Candy e Infinite Repel do jogo novo, por
//   isso Rare Candy e Max Repel não entram.
// - ORAN BERRY, LEVEL BALL e as seis berries antes da ORAN ficam de fora
//   por causa da suíte (ver o bolso de berries abaixo): T193.1 a T193.4
//   contam ORAN BERRY colhida da árvore de Route30, e T231.4 e T231.5 contam
//   LEVEL BALL comprada em Azalea. Com o kit, a mochila nasceria com elas e os
//   seis casos perderiam a prova.
//
// LIMITES DOS BOLSOS (include/constants/global.h, não aumentar: muda a save)
//
//   ITEMS 30, POKEBALLS 16, TMHM 64, BERRIES 46. Os 50 TM e 8 HM de
//   include/constants/tms_hms.h cabem nos 64 sem reserva, porque só TM e HM
//   vão para aquele bolso e eles só somam à própria pilha.

struct ItemDoKit
{
    u16 item;
    u16 quantidade;
};

static const u8 sReservaDoBolso[POCKETS_COUNT] =
{
    [POCKET_ITEMS] = 4,
    [POCKET_POKE_BALLS] = 2,
    [POCKET_BERRIES] = 4,
};

// TM com I_REUSABLE_TMS FALSE (include/config/item.h) gasta ao ensinar, então
// 99 de cada é o "infinito" do playtest. HM não gasta: 1 basta.
#define KIT_TM(id) { CAT(ITEM_TM_, id), 99 },
#define KIT_HM(id) { CAT(ITEM_HM_, id), 1 },

static const struct ItemDoKit sKit[] =
{
    // Bolso de TM e HM: todos.
    FOREACH_TM(KIT_TM)
    FOREACH_HM(KIT_HM)

    // Bolso de Poké Balls (16 vagas, reserva 2): 14 tipos.
    { ITEM_MASTER_BALL,  10 },
    { ITEM_ULTRA_BALL,   99 },
    { ITEM_POKE_BALL,    99 },
    { ITEM_GREAT_BALL,   99 },
    { ITEM_QUICK_BALL,   99 },
    { ITEM_DUSK_BALL,    99 },
    { ITEM_TIMER_BALL,   99 },
    { ITEM_REPEAT_BALL,  99 },
    { ITEM_NET_BALL,     99 },
    { ITEM_DIVE_BALL,    99 },
    { ITEM_NEST_BALL,    99 },
    { ITEM_HEAL_BALL,    99 },
    { ITEM_LUXURY_BALL,  99 },
    { ITEM_PREMIER_BALL, 99 },

    // Bolso de itens (30 vagas, reserva 4): cura, PP, vitaminas, X-itens.
    { ITEM_FULL_RESTORE,    99 },
    { ITEM_MAX_POTION,      99 },
    { ITEM_HYPER_POTION,    99 },
    { ITEM_MAX_REVIVE,      99 },
    { ITEM_REVIVE,          99 },
    { ITEM_FULL_HEAL,       99 },
    { ITEM_MAX_ELIXIR,      50 },
    { ITEM_MAX_ETHER,       50 },
    { ITEM_PP_MAX,          50 },
    { ITEM_HP_UP,           50 },
    { ITEM_PROTEIN,         50 },
    { ITEM_IRON,            50 },
    { ITEM_CALCIUM,         50 },
    { ITEM_ZINC,            50 },
    { ITEM_CARBOS,          50 },
    { ITEM_ABILITY_CAPSULE, 20 },
    { ITEM_ABILITY_PATCH,   10 },
    { ITEM_X_ATTACK,        20 },
    { ITEM_X_SP_ATK,        20 },
    { ITEM_X_SPEED,         20 },
    { ITEM_X_DEFENSE,       20 },
    { ITEM_X_SP_DEF,        20 },
    { ITEM_X_ACCURACY,      20 },
    { ITEM_DIRE_HIT,        20 },
    { ITEM_GUARD_SPEC,      20 },

    // Bolso de berries (46 vagas, reserva 4): 35 tipos. Cura e status primeiro,
    // depois as de atributo em perigo, depois as de resistência de tipo, e as
    // de confusão por último. As seis de número menor que a ORAN (CHERI,
    // CHESTO, PECHA, RAWST, ASPEAR e LEPPA) ficam de fora: o bolso se ordena
    // pelo número da berry, e o T193.4 planta a PRIMEIRA da lista esperando a
    // ORAN. A LUM cobre os cinco status dessas berries; PP fica com MAX ELIXIR
    // e MAX ETHER.
    { ITEM_SITRUS_BERRY, 99 },
    { ITEM_LUM_BERRY,    99 },
    { ITEM_PERSIM_BERRY, 99 },
    { ITEM_LIECHI_BERRY, 20 },
    { ITEM_SALAC_BERRY,  20 },
    { ITEM_PETAYA_BERRY, 20 },
    { ITEM_GANLON_BERRY, 20 },
    { ITEM_APICOT_BERRY, 20 },
    { ITEM_LANSAT_BERRY, 20 },
    { ITEM_STARF_BERRY,  20 },
    { ITEM_MICLE_BERRY,  20 },
    { ITEM_CUSTAP_BERRY, 20 },
    { ITEM_OCCA_BERRY,   20 },
    { ITEM_PASSHO_BERRY, 20 },
    { ITEM_WACAN_BERRY,  20 },
    { ITEM_RINDO_BERRY,  20 },
    { ITEM_YACHE_BERRY,  20 },
    { ITEM_CHOPLE_BERRY, 20 },
    { ITEM_KEBIA_BERRY,  20 },
    { ITEM_SHUCA_BERRY,  20 },
    { ITEM_COBA_BERRY,   20 },
    { ITEM_PAYAPA_BERRY, 20 },
    { ITEM_TANGA_BERRY,  20 },
    { ITEM_CHARTI_BERRY, 20 },
    { ITEM_KASIB_BERRY,  20 },
    { ITEM_HABAN_BERRY,  20 },
    { ITEM_COLBUR_BERRY, 20 },
    { ITEM_BABIRI_BERRY, 20 },
    { ITEM_CHILAN_BERRY, 20 },
    { ITEM_ROSELI_BERRY, 20 },
    { ITEM_FIGY_BERRY,   20 },
    { ITEM_WIKI_BERRY,   20 },
    { ITEM_MAGO_BERRY,   20 },
    { ITEM_AGUAV_BERRY,  20 },
    { ITEM_IAPAPA_BERRY, 20 },
};

#undef KIT_TM
#undef KIT_HM

static u32 VagasLivres(enum Pocket bolso)
{
    u32 i, livres = 0;

    for (i = 0; i < gBagPockets[bolso].capacity; i++)
    {
        if (GetBagItemId(bolso, i) == ITEM_NONE)
            livres++;
    }
    return livres;
}

// TRUE se o item entrou (ou já estava no teto de 999), FALSE se ficou de fora.
static bool32 EntregaUm(u16 item, u16 quantidade)
{
    enum Pocket bolso = GetItemPocket(item);
    u32 atual = CountTotalItemQuantityInBag(item);

    if (atual >= MAX_BAG_ITEM_CAPACITY)
        return TRUE;
    if (atual == 0 && VagasLivres(bolso) <= sReservaDoBolso[bolso])
        return FALSE;
    if (quantidade > MAX_BAG_ITEM_CAPACITY - atual)
        quantidade = MAX_BAG_ITEM_CAPACITY - atual;
    return AddBagItem(item, quantidade);
}

u32 KitPlaytest_Entrega(void)
{
    u32 i, deFora = 0;

    if (!PLAYTEST_KIT_MOCHILA)
        return 0;
    for (i = 0; i < ARRAY_COUNT(sKit); i++)
    {
        if (!EntregaUm(sKit[i].item, sKit[i].quantidade))
            deFora++;
    }
    FlagSet(FLAG_KIT_PLAYTEST_ENTREGUE);
    return deFora;
}

bool32 KitPlaytest_TentaEntregarNaSaveAntiga(void)
{
    if (!PLAYTEST_KIT_MOCHILA || FlagGet(FLAG_KIT_PLAYTEST_ENTREGUE))
        return FALSE;
    // Dentro da Battle Pyramid o AddBagItem cai na bolsa da pirâmide
    // (src/item.c). Espera o jogador sair.
    if (CurrentBattlePyramidLocation() != PYRAMID_LOCATION_NONE
     || FlagGet(FLAG_STORING_ITEMS_IN_PYRAMID_BAG))
        return FALSE;
    if (KitPlaytest_Entrega() == 0)
        ScriptContext_SetupScript(KitPlaytest_EventScript_Entregue);
    else
        ScriptContext_SetupScript(KitPlaytest_EventScript_EntregueSemEspaco);
    return TRUE;
}
