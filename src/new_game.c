#include "global.h"
#include "clock.h"
#include "chapter_jump.h"
#include "new_game.h"
#include "random.h"
#include "pokemon.h"
#include "roamer.h"
#include "pokemon_size_record.h"
#include "script.h"
#include "lottery_corner.h"
#include "play_time.h"
#include "mauville_old_man.h"
#include "match_call.h"
#include "lilycove_lady.h"
#include "load_save.h"
#include "pokeblock.h"
#include "dewford_trend.h"
#include "berry.h"
#include "rtc.h"
#include "easy_chat.h"
#include "event_data.h"
#include "money.h"
#include "trainer_hill.h"
#include "trainer_tower.h"
#include "tv.h"
#include "coins.h"
#include "text.h"
#include "overworld.h"
#include "mail.h"
#include "battle_records.h"
#include "item.h"
#include "pokedex.h"
#include "apprentice.h"
#include "frontier_util.h"
#include "pokedex.h"
#include "save.h"
#include "link_rfu.h"
#include "main.h"
#include "contest.h"
#include "item_menu.h"
#include "pokemon_storage_system.h"
#include "pokemon_jump.h"
#include "decoration_inventory.h"
#include "secret_base.h"
#include "string_util.h"
#include "player_pc.h"
#include "field_specials.h"
#include "berry_powder.h"
#include "mystery_gift.h"
#include "union_room_chat.h"
#include "constants/map_groups.h"
#include "constants/heal_locations.h"
#include "constants/species.h"
#include "constants/items.h"
#include "difficulty.h"
#include "follower_npc.h"
#include "script_pokemon_util.h"

extern const u8 EventScript_ResetAllMapFlags[];
extern const u8 EventScript_ResetAllMapFlagsFrlg[];

static void ClearFrontierRecord(void);
static void WarpToTruck(void);
static void ResetMiniGamesRecords(void);
static void ResetItemFlags(void);
static void ResetDexNav(void);

EWRAM_DATA bool8 gDifferentSaveFile = FALSE;
EWRAM_DATA bool8 gEnableContestDebugging = FALSE;

static const struct ContestWinner sContestWinnerPicDummy =
{
    .monName = _(""),
    .trainerName = _("")
};

void SetTrainerId(u32 trainerId, u8 *dst)
{
    dst[0] = trainerId;
    dst[1] = trainerId >> 8;
    dst[2] = trainerId >> 16;
    dst[3] = trainerId >> 24;
}

u32 GetTrainerId(u8 *trainerId)
{
    return (trainerId[3] << 24) | (trainerId[2] << 16) | (trainerId[1] << 8) | (trainerId[0]);
}

void CopyTrainerId(u8 *dst, u8 *src)
{
    s32 i;
    for (i = 0; i < TRAINER_ID_LENGTH; i++)
        dst[i] = src[i];
}

static void InitPlayerTrainerId(void)
{
    u32 trainerId = (Random() << 16) | GetGeneratedTrainerIdLower();
    SetTrainerId(trainerId, gSaveBlock2Ptr->playerTrainerId);
}

// L=A isnt set here for some reason.
static void SetDefaultOptions(void)
{
    gSaveBlock2Ptr->optionsTextSpeed = OPTIONS_TEXT_SPEED_MID;
    gSaveBlock2Ptr->optionsWindowFrameType = 0;
    gSaveBlock2Ptr->optionsSound = OPTIONS_SOUND_MONO;
    gSaveBlock2Ptr->optionsBattleStyle = OPTIONS_BATTLE_STYLE_SHIFT;
    gSaveBlock2Ptr->optionsBattleSceneOff = FALSE;
    gSaveBlock2Ptr->regionMapZoom = FALSE;
}

static void ClearPokedexFlags(void)
{
    gUnusedPokedexU8 = 0;
    memset(&gSaveBlock1Ptr->dexCaught, 0, sizeof(gSaveBlock1Ptr->dexCaught));
    memset(&gSaveBlock1Ptr->dexSeen, 0, sizeof(gSaveBlock1Ptr->dexSeen));
}

void ClearAllContestWinnerPics(void)
{
    s32 i;

    ClearContestWinnerPicsInContestHall();

    // Clear Museum paintings
    for (i = MUSEUM_CONTEST_WINNERS_START; i < NUM_CONTEST_WINNERS; i++)
        gSaveBlock1Ptr->contestWinners[i] = sContestWinnerPicDummy;
}

static void ClearFrontierRecord(void)
{
    CpuFill32(0, &gSaveBlock2Ptr->frontier, sizeof(gSaveBlock2Ptr->frontier));

    gSaveBlock2Ptr->frontier.opponentNames[0][0] = EOS;
    gSaveBlock2Ptr->frontier.opponentNames[1][0] = EOS;
}

static void WarpToTruck(void)
{
    // O jogo novo comeca em Pallet Town, no quarto do jogador. Decisao do dono
    // do projeto em 05/08/2026: a ordem das cinco regioes e cronologica, Kanto,
    // Johto, Hoenn, Sinnoh, Unova. Antes comecava em Twinleaf porque Sinnoh era
    // a unica regiao montada.
    //
    // A abertura de Kanto nao precisou ser escrita: o roteiro do laboratorio do
    // Oak ja existe inteiro em data/maps/PalletTown_ProfessorOaksLab_Frlg, com
    // escolha de inicial e rival, e e autocontido (usa
    // VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB e VAR_STARTER_MON, que
    // existem nesta build). O que o prendia era so IS_FRLG, que aqui e 0.
    //
    // Nao ha caminhao: ele so serve a cutscene de abertura do Emerald.
#if DEV_SKIP_INTRO
    // ponytail: sem introducao, o jogo comeca direto no mapa de desenvolvimento.
    SetWarpDestination(MAP_GROUP(DEV_START_MAP), MAP_NUM(DEV_START_MAP), WARP_ID_NONE, DEV_START_X, DEV_START_Y);
#else
    // (6, 6) e a mesma casa do FRLG original: o jogador nasce de pe ao lado da
    // cama, e PalletTown_PlayersHouse_2F_OnWarp vira ele para o norte.
    SetWarpDestination(MAP_GROUP(MAP_PALLET_TOWN_PLAYERS_HOUSE_2F), MAP_NUM(MAP_PALLET_TOWN_PLAYERS_HOUSE_2F), WARP_ID_NONE, 6, 6);
#endif
    WarpIntoMap();
}

void Sav2_ClearSetDefault(void)
{
    ClearSav2();
    SetDefaultOptions();
}

void ResetMenuAndMonGlobals(void)
{
    gDifferentSaveFile = FALSE;
    ResetPokedexScrollPositions();
    ZeroPlayerPartyMons();
    ZeroEnemyPartyMons();
    ResetBagScrollPositions();
    ResetPokeblockScrollPositions();
}

void NewGameInitData(void)
{
    // O nome do rival e digitado na abertura do Carvalho, ANTES de ClearSav1(),
    // entao ele tem que ser guardado e devolvido, ou a limpeza o apaga.
    u8 rivalName[PLAYER_NAME_LENGTH + 1];
    if (gSaveFileStatus == SAVE_STATUS_EMPTY || gSaveFileStatus == SAVE_STATUS_CORRUPT)
        RtcReset();

    StringCopy(rivalName, gSaveBlock1Ptr->rivalName);
    gDifferentSaveFile = TRUE;
    gSaveBlock2Ptr->encryptionKey = 0;
    ZeroPlayerPartyMons();
    ZeroEnemyPartyMons();
    ResetPokedex();
    ClearFrontierRecord();
    ClearSav1();
    ClearSav3();
    ClearAllMail();
    gSaveBlock2Ptr->specialSaveWarpFlags = 0;
    gSaveBlock2Ptr->gcnLinkFlags = 0;
    InitPlayerTrainerId();
    PlayTimeCounter_Reset();
    ClearPokedexFlags();
    InitEventData();
    ClearTVShowData();
    ResetGabbyAndTy();
    ClearSecretBases();
    ClearBerryTrees();
    SetMoney(&gSaveBlock1Ptr->money, 3000);
    SetCoins(0);
    ResetLinkContestBoolean();
    ResetGameStats();
    ClearAllContestWinnerPics();
    ClearPlayerLinkBattleRecords();
    InitSeedotSizeRecord();
    InitLotadSizeRecord();
    gPartiesCount[B_TRAINER_PLAYER] = 0;
    ZeroPlayerPartyMons();
    ResetPokemonStorageSystem();
    DeactivateAllRoamers();
    gSaveBlock1Ptr->registeredItem = ITEM_NONE;
    ClearBag();
    NewGameInitPCItems();
    ClearPokeblocks();
    ClearDecorationInventories();
    InitEasyChatPhrases();
    SetMauvilleOldMan();
    InitDewfordTrend();
    ResetFanClub();
    ResetLotteryCorner();
    UpdateDailySeed();
    WarpToTruck();
    // Os DOIS, sempre: a ROM tem Hoenn e Kanto no mesmo save, entao as duas
    // listas de "nasce escondido" precisam valer. Nao e um ou outro.
    //
    // Ate 16/08/2026 so o de Hoenn rodava, com a justificativa (correta em
    // 05/08) de que toda FLAG_HIDE_* de Kanto era o literal 0 e o script FRLG
    // seria ~50 setflag em cima do nada. Isso deixou de ser verdade quando o
    // liga_flags_kanto.py deu numero de verdade a essas flags: as 49 do script
    // FRLG existem, e nao acender nenhuma delas custou a casa do Bill em
    // Route 25. FLAG_HIDE_BILL_HUMAN_SEA_COTTAGE nunca era acesa, entao o Bill
    // humano nascia visivel DENTRO do pod do teletransporte ao lado do
    // Bill-Clefairy andando pela sala, e a cena do separador de celulas rodava
    // em cima de dois Bills.
    //
    // Efeito colateral conhecido e aceito: a ultima linha do script FRLG grava
    // 500 em VAR_MASSAGE_COOLDOWN_STEP_COUNTER (0x4025), que nesta build e
    // VAR_MIRAGE_RND_L, de Hoenn. E inofensivo: UpdateMirageRnd sobrescreve
    // esse var na proxima virada de dia do RTC.
    RunScriptImmediately(EventScript_ResetAllMapFlags);
    RunScriptImmediately(EventScript_ResetAllMapFlagsFrlg);
    StringCopy(gSaveBlock1Ptr->rivalName, rivalName);
    ResetMiniGamesRecords();
    InitUnionRoomChatRegisteredTexts();
    InitLilycoveLady();
    ResetAllApprenticeData();
    ClearRankingHallRecords();
    InitMatchCallCounters();
    ClearMysteryGift();
    WipeTrainerNameRecords();
    ResetTrainerHillResults();
    ResetTrainerTowerResults();
    ResetContestLinkResults();
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    ResetItemFlags();
    ResetDexNav();
    ClearFollowerNPCData();
    // ponytail: Dynamax e Terastal ligados desde o começo do jogo. Se um dia
    // virarem recompensa de história, tire estas duas linhas e dê FlagSet no
    // script do evento que libera cada um.
    FlagSet(B_FLAG_DYNAMAX_BATTLE);
    FlagSet(B_FLAG_TERA_ORB_CHARGED);
    // A flag sozinha nao basta do lado do JOGADOR: CanDynamax exige
    // ITEM_DYNAMAX_BAND na mochila e CanMegaEvolve exige ITEM_MEGA_RING
    // (src/battle_dynamax.c e src/battle_util.c, checagem so nas posicoes do
    // jogador). Sem os dois itens, os lideres e a Elite Four Dynamaxariam e o
    // jogador nao teria resposta. O Mega Ring sozinho nao da poder nenhum:
    // ainda e preciso achar a Mega Stone certa e o Pokemon precisa segura-la.
    // Vem depois de ClearBag() de proposito.
    AddBagItem(ITEM_DYNAMAX_BAND, 1);
    AddBagItem(ITEM_MEGA_RING, 1);
    // Conveniencias do jogador, so no JOGO NOVO. Esta funcao roda em um unico
    // lugar, CB2_NewGame (src/overworld.c), e carregar save existente passa por
    // CB2_ContinueSavedGame, que nao a chama: save antiga nao ganha nada disso,
    // que e exatamente o combinado da janela de save fechada.
    //
    // Tenis de corrida desde o primeiro passo (sem isso, correr so depois da
    // mae entregar o item) e EXP ALL ligado (I_EXP_SHARE_FLAG aponta para
    // FLAG_EXP_ALL em include/config/item.h).
    FlagSet(FLAG_SYS_B_DASH);
    FlagSet(FLAG_EXP_ALL);
    // FLAG_SEM_ENCONTRO_SELVAGEM nao aparece aqui de proposito: ela tem que
    // nascer APAGADA (encontros normais) ate o jogador usar o Infinite Repel, e
    // o ClearSav1() + InitEventData() la em cima ja zeram o vetor de flags.
    //
    // Vem depois de ClearBag(), pelo mesmo motivo dos dois itens acima.
    AddBagItem(ITEM_MACH_BIKE, 1);
    AddBagItem(ITEM_INFINITE_CANDY, 1);
    AddBagItem(ITEM_INFINITE_REPEL, 1);
    // CHAPTER JUMP, o seletor de capitulo (src/chapter_jump.c). Ele cobre o
    // meio do jogo; o comeco e coberto pelo seletor automatico logo abaixo.
    AddBagItem(ITEM_CHAPTER_JUMP, 1);
    // TURBO A/B nasce LIGADO. E a unica opcao do modo de teste cujo default nao
    // e o valor 0 do byte; o bit vive em gSaveBlock2Ptr->filler_90[0], que o
    // Sav2_ClearSetDefault do intro (src/intro.c) ja zerou antes desta funcao.
    // Ele e inofensivo para a suite: o disparo so comeca depois de 20 quadros
    // de botao segurado, e o gba_runner segura 6.
    TestOptionSet(TEST_OPT_TURBO_AB, TRUE);
    // AUTO RUN nasce DESLIGADO, e isto foi DECIDIDO PELA SUITE em 17/08/2026,
    // nao por gosto. Correr muda a gramatica de andar: com o jogador correndo,
    // mudar de direcao LOGO DEPOIS de um passo gasta um aperto so para virar, e
    // mudar de direcao parado nao gasta. Medido nas duas ROMs com o mesmo
    // roteiro (T80.1, biblioteca de Canalave): na build de 15/08 o `16:RIGHT`
    // depois de dois `16:UP` ANDA, e com AUTO RUN ligado ele so VIRA. Isso
    // reprovou 15 casos de percurso de uma vez, e o custo de acerto nao e
    // remedir 15 roteiros: e que o custo de virar passa a depender de o aperto
    // anterior ter andado ou nao, ou seja, todo roteiro futuro fica fragil.
    // A opcao continua no menu de opcoes (modo de teste), a um toque de
    // distancia de quem quiser jogar correndo.
    TestOptionSet(TEST_OPT_AUTO_RUN, FALSE);
    // Arma o seletor de capitulo do jogo novo. Quem o dispara e
    // ProcessPlayerFieldInput (src/field_control_avatar.c), no primeiro quadro
    // em que o jogador ganha o controle. Nao e bit de save: esta funcao e a
    // primeira entrada no overworld acontecem no mesmo boot.
    gChapterJumpModo = CHAPTER_JUMP_PENDENTE;
    // Ponto de cura inicial de Kanto. Sem isto, desmaiar manda o jogador para a
    // casa da mae em Hoenn, que e o padrao do Emerald.
    // PalletTown_PlayersHouse_2F_OnTransition tambem faz este setrespawn, mas so
    // depois que o mapa carrega; aqui garante o valor antes de qualquer coisa.
    SetLastHealLocationWarp(HEAL_LOCATION_PALLET_TOWN);
#if DEV_SKIP_INTRO
    // ponytail: sem introducao ninguem recebe inicial. Sem time nao da para
    // testar batalha.
    SetLastHealLocationWarp(HEAL_LOCATION_OREBURGH_CITY);
    {
        static const enum Species timeDeTeste[] = {
            SPECIES_INFERNAPE, SPECIES_EMPOLEON, SPECIES_TORTERRA,
            SPECIES_STARAPTOR, SPECIES_LUXRAY,   SPECIES_GARCHOMP,
        };
        u32 i;
        for (i = 0; i < ARRAY_COUNT(timeDeTeste); i++)
            ScriptGiveMon(timeDeTeste[i], 25, ITEM_NONE);
    }
#endif
}

static void ResetMiniGamesRecords(void)
{
    CpuFill16(0, &gSaveBlock2Ptr->berryCrush, sizeof(struct BerryCrush));
    SetBerryPowder(&gSaveBlock2Ptr->berryCrush.berryPowderAmount, 0);
    ResetPokemonJumpRecords();
    CpuFill16(0, &gSaveBlock2Ptr->berryPick, sizeof(struct BerryPickingResults));
}

static void ResetItemFlags(void)
{
#if OW_SHOW_ITEM_DESCRIPTIONS == OW_ITEM_DESCRIPTIONS_FIRST_TIME
    memset(&gSaveBlock3Ptr->itemFlags, 0, sizeof(gSaveBlock3Ptr->itemFlags));
#endif
}

static void ResetDexNav(void)
{
#if USE_DEXNAV_SEARCH_LEVELS == TRUE
    memset(gSaveBlock3Ptr->dexNavSearchLevels, 0, sizeof(gSaveBlock3Ptr->dexNavSearchLevels));
#endif
    gSaveBlock3Ptr->dexNavChain = 0;
}
