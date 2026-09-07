#ifndef GUARD_REGIONS_H
#define GUARD_REGIONS_H

#include "global.h"
#include "constants/regions.h"
#include "constants/map_groups.h"
#include "constants/maps.h"

enum KantoSubRegion GetKantoSubregion(u32 mapSecId);

static inline enum Region GetRegionForSectionId(u32 sectionId)
{
    if (sectionId >= KANTO_MAPSEC_START && sectionId < MAPSEC_SPECIAL_AREA)
        return REGION_KANTO;
    // >>> Dex completa: as outras regioes (dev_scripts/distribui_dex.py) >>>
    // MEDIDO em 21/08/2026, e nao lembrado: a faixa abaixo e a unica do enum de
    // MAPSEC que pertence a UMA regiao so. `MAPSEC_SS_AQUA` fica de fora de
    // proposito: e o barco, e ele liga Johto a Kanto. As faixas de Unova e de
    // Galar sairam com as duas regioes no cartucho 1 (07/09/2026); os slots do
    // enum ficaram como MAPSEC_RESERVADO_*, sem mover indice, porque
    // `regionMapSectionId` e gravado na save como local de captura.
    if (sectionId >= MAPSEC_SINNOH_WEST && sectionId <= MAPSEC_SINNOH_NORTH)
        return REGION_SINNOH;
    // <<< Dex completa <<<
    return REGION_HOENN;
}

// Johto NAO tem faixa de mapsec propria, e essa e a armadilha desta funcao.
// Os 65 apelidos de MAPSEC de Johto (MAPSEC_NEW_BARK_TOWN, MAPSEC_ILEX_FOREST,
// MAPSEC_GOLDENROD_CITY, ...) sao todos `#define ... MAPSEC_SINNOH_WEST` em
// include/constants/region_map_sections.h, porque MAPSEC e u8 e nao cabe uma
// por cidade. Numericamente Johto E Sinnoh Oeste: nenhuma comparacao de
// sectionId pode separar as duas. Quem separa e o GRUPO do mapa, que e exato:
// os grupos 84 a 98 (`gMapGroup_TownsAndRoutes_Johto` ate
// `gMapGroup_SpecialArea_Johto`) sao Johto e nada mais, e sao contiguos.
//
// Custo de save ZERO: `location.mapGroup` ja e gravado pelo motor desde sempre
// e nenhum campo, tamanho ou ordem de SaveBlock muda aqui. E leitura.
static inline enum Region GetCurrentRegion(void)
{
    u32 grupo = gSaveBlock1Ptr->location.mapGroup;

    if (grupo >= MAP_GROUP(MAP_NEW_BARK_TOWN) && grupo <= MAP_GROUP(MAP_WORLD_HUB2))
        return REGION_JOHTO;
    return GetRegionForSectionId(gMapHeader.regionMapSectionId);
}

#endif // GUARD_REGIONS_H
