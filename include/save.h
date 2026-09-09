#ifndef GUARD_SAVE_H
#define GUARD_SAVE_H

#include "main.h"

// Each 4 KiB flash sector contains 3968 bytes of actual data followed by 116 bytes of SaveBlock3 and then 12 bytes of footer.
#define SECTOR_DATA_SIZE 3968
#define SAVE_BLOCK_3_CHUNK_SIZE 116
#define SECTOR_FOOTER_SIZE 12
#define SECTOR_SIZE (SECTOR_DATA_SIZE + SAVE_BLOCK_3_CHUNK_SIZE + SECTOR_FOOTER_SIZE)

#define NUM_SAVE_SLOTS 2

// If the sector's signature field is not this value then the sector is either invalid or empty.
//
// SAVE_LAYOUT_REVISION é a revisão do LAYOUT da save deste hack, e existe porque
// pokeemerald não tem versionamento de save nem migração. Medido em 18/08/2026,
// na onda de janela aberta: quando o `flags[]` do SaveBlock1 cresceu 576 B, uma
// save do layout anterior NÃO era recusada. `HandleWriteSector` zera os 3968 B
// do setor antes de gravar e `CalculateChecksum` soma palavras de 32 bits, então
// os bytes a mais lidos são zeros, o checksum bate, e `GetSaveValidStatus`
// devolvia SAVE_STATUS_OK para uma save que o jogo passava a ler DESLOCADA (as
// 512 vars saíam 288 posições fora do lugar, Pokédex e creche embaralhadas).
// Carregar lixo em silêncio é pior do que perder a save: o jogador joga horas em
// cima de estado corrompido e só descobre num travamento.
//
// Somar a revisão à assinatura do setor faz o motor não reconhecer setor nenhum
// da save velha, tratar os dois slots como VAZIOS e abrir o menu principal em
// NEW GAME, que é um caminho digno (o Chapter Jump repõe o progresso).
//
// REGRA: SUBIR SAVE_LAYOUT_REVISION em toda mudança que desloque campo dentro de
// SaveBlock1/2/3 (FLAGS_COUNT, VARS_COUNT, campo novo no meio, reordenação de
// SPECIES/ITEM/MOVE). Quem diz o que desloca é `dev_scripts/guarda_save.py`.
// Revisão 1 = onda de janela aberta de 18/08/2026 (FLAGS_COUNT 8248 -> 12856).
//
// Revisão 2 = QUEBRA ÚNICA DE SAVE do cartucho 1, 08/09/2026. Ela junta todas as
// quebras que o projeto tinha pendentes numa só, de propósito, para matar a save
// do Gui UMA vez em vez de três, e a promessa que vem junto é que **nenhuma onda
// posterior tem licença para quebrar de novo**. O que andou, medido por
// `guarda_save.py` e colado na seção 0.z do ESTADO.md:
//
//   - os 812 mapas túmulo saíram do disco: 1.330 mapas mudaram de
//     `location.mapGroup`/`mapNum` e 565 layouts mudaram de `mapLayoutId`;
//   - `group_order` virou bloco contíguo por região (Hoenn, Kanto, Johto,
//     Sinnoh, comum), de 129 grupos para 103;
//   - os ids de treinador foram compactados e `MAX_TRAINERS_COUNT` caiu de 4.000
//     para 2.200, o que encolhe `flags[]`;
//   - a reserva de 467 flags dos itens de Unova saiu, e `FLAGS_COUNT` foi de
//     12.856 para 10.584;
//   - os 9 `MAPSEC_RESERVADO_*` saíram, então `regionMapSectionId` (o local de
//     captura gravado dentro do Pokémon) deslizou;
//   - `BERRY_TREES_COUNT` subiu de 128 para 178 pelos canteiros de Sinnoh, e
//     `berryTrees[]` cresceu 400 B, empurrando tudo que vem depois dele.
//
// A última ROM que ainda abre a save antiga é
// `roms/pokemon-claude-2026-09-08-c1-consolidada.gba`
// (md5 bc5f411d54ba26ade79fd7653a1f082f). Da revisão 2 em diante ela abre em
// NEW GAME, e o Chapter Jump repõe o progresso.
//
// Revisão 3 = 08/09/2026, BERRY_TREES_COUNT sobe para as 36 berries de Johto,
// autorizada pelo Gui na resposta 58 ("pode subir o teto das IDs, não tem
// problema quebrar save"). É a SEGUNDA e ÚLTIMA quebra do cartucho 1, e depois
// dela a regra "nunca mais" volta a valer.
//
// A promessa da revisão 2 era que a quebra tinha sido ÚNICA, e ela foi
// desfeita por decisão explícita do Gui no mesmo dia, não por descuido de
// ninguém: o item 12 da fila de bugs mediu 36 árvores de berry de Johto e do
// WorldHub com `trainer_sight_or_berry_tree_id` igual a 0, ou seja lendo a vaga
// `berryTrees[0]`, que jogo nenhum planta. Elas eram desenho de árvore, sem
// resposta ao aperto de A, e consertar isso exige vaga própria para cada uma.
//
// O que andou, e é UMA coisa só: `BERRY_TREES_COUNT` foi de 178 para 222 (as 36
// árvores nos ids 178 a 213, mais 8 vagas de folga), então `berryTrees[]`
// cresceu 352 B e empurrou tudo que vem depois dele dentro do SaveBlock1, que
// foi de 15.080 para 15.432 B dos 15.872 do teto. `guarda_save.py` acusou as
// duas linhas, "SAVEBLOCK1 MUDOU DE TAMANHO" e "SAVE_LAYOUT_REVISION NÃO
// SUBIU", e o relatório inteiro está colado na seção 0.ab do ESTADO.md.
//
// A última ROM que ainda abre a save da revisão 2 é
// `roms/pokemon-claude-2026-09-08-c1-bugs.gba`
// (md5 9954be734a93fefcb0cd4180cea64cd7). Da revisão 3 em diante ela abre em
// NEW GAME, pelo mesmo caminho digno da revisão 2.
#define SAVE_LAYOUT_REVISION 3
#define SECTOR_SIGNATURE (0x8012025 + SAVE_LAYOUT_REVISION)

#define SPECIAL_SECTOR_SENTINEL 0xB39D

#define SECTOR_ID_SAVEBLOCK2          0
#define SECTOR_ID_SAVEBLOCK1_START    1
#define SECTOR_ID_SAVEBLOCK1_END      4
#define SECTOR_ID_PKMN_STORAGE_START  5
#define SECTOR_ID_PKMN_STORAGE_END   13
#define NUM_SECTORS_PER_SLOT         14
// Save Slot 1: 0-13;  Save Slot 2: 14-27
#define SECTOR_ID_HOF_1              28
#define SECTOR_ID_HOF_2              29
#define SECTOR_ID_TRAINER_HILL       30
#define SECTOR_ID_RECORDED_BATTLE    31
#define SECTORS_COUNT                32

#define NUM_HOF_SECTORS 2

#define SAVE_STATUS_EMPTY    0
#define SAVE_STATUS_OK       1
#define SAVE_STATUS_CORRUPT  2
#define SAVE_STATUS_NO_FLASH 4
#define SAVE_STATUS_ERROR    0xFF

// Special sector id value for certain save functions to
// indicate that no specific sector should be used.
#define FULL_SAVE_SLOT 0xFFFF

// SetDamagedSectorBits states
enum
{
    ENABLE,
    DISABLE,
    CHECK // unused
};

// Do save types
enum
{
    SAVE_NORMAL,
    SAVE_LINK, // Link / Battle Frontier
    SAVE_EREADER, // deprecated in Emerald
    SAVE_HALL_OF_FAME,
    SAVE_OVERWRITE_DIFFERENT_FILE,
    SAVE_HALL_OF_FAME_ERASE_BEFORE // unused
};

// A save sector location holds a pointer to the data for a particular sector
// and the size of that data. Size cannot be greater than SECTOR_DATA_SIZE.
struct SaveSectorLocation
{
    void *data;
    u16 size;
};

struct SaveSector
{
    u8 data[SECTOR_DATA_SIZE];
    u8 saveBlock3Chunk[SAVE_BLOCK_3_CHUNK_SIZE];
    u16 id;
    u16 checksum;
    u32 signature;
    u32 counter;
}; // size is SECTOR_SIZE (0x1000)

#define SECTOR_SIGNATURE_OFFSET offsetof(struct SaveSector, signature)
#define SECTOR_COUNTER_OFFSET   offsetof(struct SaveSector, counter)

extern u16 gLastWrittenSector;
extern u32 gLastSaveCounter;
extern u16 gLastKnownGoodSector;
extern u32 gDamagedSaveSectors;
extern u32 gSaveCounter;
extern struct SaveSector *gFastSaveSector;
extern u16 gIncrementalSectorId;
extern u16 gSaveFileStatus;
extern MainCallback gGameContinueCallback;
extern struct SaveSectorLocation gRamSaveSectorLocations[];

extern struct SaveSector gSaveDataBuffer;

void ClearSaveData(void);
void Save_ResetSaveCounters(void);
u8 HandleSavingData(u8 saveType);
u8 TrySavingData(u8 saveType);
bool8 LinkFullSave_Init(void);
bool8 LinkFullSave_WriteSector(void);
bool8 LinkFullSave_ReplaceLastSector(void);
bool8 LinkFullSave_SetLastSectorSignature(void);
bool8 WriteSaveBlock2(void);
bool8 WriteSaveBlock1Sector(void);
u8 LoadGameSave(u8 saveType);
u16 GetSaveBlocksPointersBaseOffset(void);
u32 TryReadSpecialSaveSector(u8 sector, u8 *dst);
u32 TryWriteSpecialSaveSector(u8 sector, u8 *src);
void Task_LinkFullSave(u8 taskId);

// save_failed_screen.c
void DoSaveFailedScreen(u8 saveType);

#endif // GUARD_SAVE_H
