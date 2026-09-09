#include "global.h"
#include "time_events.h"
#include "event_data.h"
#include "field_weather.h"
#include "pokemon.h"
#include "random.h"
#include "overworld.h"
#include "rtc.h"
#include "script.h"
#include "task.h"

static u32 GetMirageRnd(void)
{
    u32 hi = VarGet(VAR_MIRAGE_RND_H);
    u32 lo = VarGet(VAR_MIRAGE_RND_L);
    return (hi << 16) | lo;
}

static void SetMirageRnd(u32 rnd)
{
    VarSet(VAR_MIRAGE_RND_H, rnd >> 16);
    VarSet(VAR_MIRAGE_RND_L, rnd);
}

// unused
void InitMirageRnd(void)
{
    SetMirageRnd(Random32());
}

void UpdateMirageRnd(u16 days)
{
    s32 rnd = GetMirageRnd();
    while (days)
    {
        rnd = ISO_RANDOMIZE2(rnd);
        days--;
    }
    SetMirageRnd(rnd);
}

bool8 IsMirageIslandPresent(void)
{
    u16 rnd = GetMirageRnd() >> 16;
    int i;

    for (i = 0; i < PARTY_SIZE; i++)
        if (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES) && (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_PERSONALITY) & 0xFFFF) == rnd)
            return TRUE;

    return FALSE;
}

// A tabela de mare, hora a hora: 1 quer dizer mare ALTA. Ela saiu de dentro de
// `UpdateShoalTideFlag` em 08/09/2026 porque passou a ter DOIS leitores, a
// Shoal Cave e o Lago da Furia, e duplicar a tabela seria duas verdades sobre a
// mesma mare.
static const u8 sMareDaHora[] =
{
        1, // 00
        1, // 01
        1, // 02
        0, // 03
        0, // 04
        0, // 05
        0, // 06
        0, // 07
        0, // 08
        1, // 09
        1, // 10
        1, // 11
        1, // 12
        1, // 13
        1, // 14
        0, // 15
        0, // 16
        0, // 17
        0, // 18
        0, // 19
        0, // 20
        1, // 21
        1, // 22
        1, // 23
};

void UpdateShoalTideFlag(void)
{
    if (IsMapTypeOutdoors(GetLastUsedWarpMapType()))
    {
        RtcCalcLocalTime();
        if (sMareDaHora[gLocalTime.hours])
            FlagSet(FLAG_SYS_SHOAL_TIDE);
        else
            FlagClear(FLAG_SYS_SHOAL_TIDE);
    }
}

// A mare do Lago da Furia, com a MESMA tabela e a MESMA flag da Shoal Cave, e
// sem o portao `IsMapTypeOutdoors(GetLastUsedWarpMapType())`.
//
// O portao nao foi esquecido, foi MEDIDO e descartado em 08/09/2026. Ele olha o
// tipo do ULTIMO WARP USADO, nao o do mapa em que o jogador esta. Na Shoal Cave
// isso funciona porque la se entra por WARP, vindo da rota, e o ultimo warp e a
// propria boca da caverna, ao ar livre. No Lago da Furia o jogador entra
// ANDANDO, por conexao com a Route 43, e o ultimo warp continua sendo a porta
// que ele usou antes, em outro canto do mundo: se foi um Pokecenter, o portao
// reprova e a flag nunca era escrita, ou seja a mare congelava no valor velho.
// Medido no emulador: com `special UpdateShoalTideFlag` no ON_TRANSITION do
// lago, o relogio nas 0h (mare ALTA na tabela) ainda entregava o layout de mare
// BAIXA, porque a flag ficou como estava.
//
// Aqui o portao e desnecessario por construcao: este special so e chamado do
// ON_TRANSITION do proprio lago, que e mapa ao ar livre.
void AtualizaMareDoLagoDaFuria(void)
{
    RtcCalcLocalTime();
    if (sMareDaHora[gLocalTime.hours])
        FlagSet(FLAG_SYS_SHOAL_TIDE);
    else
        FlagClear(FLAG_SYS_SHOAL_TIDE);
}

static void Task_WaitWeather(u8 taskId)
{
    if (IsWeatherChangeComplete())
    {
        ScriptContext_Enable();
        DestroyTask(taskId);
    }
}

void WaitWeather(void)
{
    CreateTask(Task_WaitWeather, 80);
}

void InitBirchState(void)
{
    *GetVarPointer(VAR_BIRCH_STATE) = 0;
}

void UpdateBirchState(u16 days)
{
    u16 *state = GetVarPointer(VAR_BIRCH_STATE);
    *state += days;
    *state %= 7;
}
