#include "global.h"
#include "chapter_jump.h"
#include "event_data.h"
#include "field_screen_effect.h"
#include "list_menu.h"
#include "malloc.h"
#include "overworld.h"
#include "script.h"
#include "script_menu.h"
#include "script_pokemon_util.h"
#include "string_util.h"
#include "constants/flags.h"
#include "constants/heal_locations.h"
#include "constants/maps.h"
#include "constants/opponents.h"
#include "constants/opponents_frlg.h"

// ============================================================================
// CHAPTER JUMP, o seletor de capítulo (ITEM_CHAPTER_JUMP, id 879)
// ============================================================================
//
// PARA QUE SERVE
//
// Retestar qualquer trecho das cinco regiões sem recomeçar save. O jogador
// escolhe região e depois capítulo, e o jogo o coloca na cidade daquele
// capítulo com o estado mínimo de quem acabou de chegar lá: as insígnias e os
// líderes ANTERIORES resolvidos, nada mais.
//
// Dois caminhos entram aqui, e os dois usam esta mesma tabela e o mesmo roteiro
// (data/scripts/chapter_jump.inc):
//
//   1. o seletor automático do jogo novo, que roda uma vez, no primeiro quadro
//      em que o jogador ganha o controle (gChapterJumpModo, lido em
//      src/field_control_avatar.c);
//   2. o item CHAPTER JUMP, para pular no meio de uma save que já existe.
//
// POR QUE UMA TABELA E NÃO UM ROTEIRO POR CAPÍTULO
//
// São 50 capítulos (5 regiões x (1 início + 8 ginásios + 1 Liga)). Escritos à
// mão em .inc seriam 50 blocos quase iguais, e capítulo novo custaria um bloco
// novo. Aqui cada ginásio é UMA LINHA, e a lista dos menus é gerada dela: o
// nome do capítulo, o destino e as flags saem todos do mesmo lugar, então não
// existe o erro clássico de acrescentar o capítulo na lista e esquecer da flag.
//
// O QUE O SELETOR NÃO FAZ, DE PROPÓSITO
//
// Não simula flag de história fina (cena vista, NPC movido, item pego). O
// objetivo é testar as CENAS DALI EM DIANTE no estado natural de quem chegou
// ali pela porta da frente, e uma máquina de estados de história inteira seria
// conteúdo novo com toda a chance de mentir sobre o jogo de verdade.

// ----------------------------------------------------------------------------
// Formas
// ----------------------------------------------------------------------------

struct DestinoDeCapitulo
{
    // Quando existe, o ponto de cura manda: ele já é a coordenada certa do
    // Centro Pokémon e ainda arruma o ponto de respawn de quem desmaiar.
    u16 healLocation;
    // Só valem quando healLocation é HEAL_LOCATION_NONE. Sinnoh tem ponto de
    // cura para Oreburgh e mais nada, então as outras sete cidades de ginásio
    // dela chegam por mapa e coordenada.
    u16 mapa;
    u8 x;
    u8 y;
};

struct GinasioDoHack
{
    // Nome do líder, em inglês. Vira "Before <líder>" na lista.
    const u8 *lider;
    // A cidade DESTE ginásio: quem escolhe "Before ROXANNE" quer estar em
    // Rustboro com a insígnia de Rustboro ainda por ganhar.
    struct DestinoDeCapitulo onde;
    // 0 quando a região não tem esse tipo de flag. Ver o comentário de cada
    // região abaixo para saber quais existem e quais não.
    u16 flagInsignia;
    u16 flagDerrotado;
    // TRAINER_*, ou 0. Acender a flag do treinador é o que faz o líder parar de
    // desafiar de novo nas regiões cujo ginásio pergunta `goto_if_defeated` em
    // vez de ler uma FLAG_DEFEATED_* própria (Johto, Sinnoh e Unova).
    u16 treinador;
};

struct RegiaoDoHack
{
    const u8 *nome;
    // Onde a região começa NESTE hack. Ver a nota de cada região.
    struct DestinoDeCapitulo inicio;
    // A Liga daquela região.
    struct DestinoDeCapitulo liga;
    const struct GinasioDoHack *ginasios;
    u8 numGinasios;
};

// Atalhos de leitura. `CURA` é o caso normal; `MAPA` é a exceção de Sinnoh.
#define CURA(hl)        { hl, 0, 0, 0 }
#define MAPA(m, mx, my) { HEAL_LOCATION_NONE, m, mx, my }
// Todos os Centros Pokémon de Sinnoh compartilham LAYOUT_OREBURGH_CITY_POKEMON_
// CENTER_1F, e o ponto de cura de Oreburgh (src/data/heal_locations.json) fica
// em (7,4) dentro dele: o mesmo par serve para as sete cidades sem ponto de cura.
#define CENTRO_SINNOH(m) MAPA(m, 7, 4)

// ----------------------------------------------------------------------------
// KANTO
// ----------------------------------------------------------------------------
// Insígnias: FLAG_BADGE01_GET..08, as OITO DO MOTOR (decisão de 12/08/2026, ver
// include/constants/flags.h). Kanto é a única região cujas insígnias destravam
// obediência e limite de nível, então acendê-las tem efeito de verdade.
// Cada ginásio também tem a sua FLAG_DEFEATED_* própria, que é quem os scripts
// de Kanto leem para trocar a fala do ajudante e da estátua.
static const struct GinasioDoHack sGinasiosKanto[] =
{
    { COMPOUND_STRING("BROCK"),    CURA(HEAL_LOCATION_PEWTER_CITY),    FLAG_BADGE01_GET, FLAG_DEFEATED_BROCK,           TRAINER_LEADER_BROCK },
    { COMPOUND_STRING("MISTY"),    CURA(HEAL_LOCATION_CERULEAN_CITY),  FLAG_BADGE02_GET, FLAG_DEFEATED_MISTY,           TRAINER_LEADER_MISTY },
    { COMPOUND_STRING("LT SURGE"), CURA(HEAL_LOCATION_VERMILION_CITY), FLAG_BADGE03_GET, FLAG_DEFEATED_LT_SURGE,        TRAINER_LEADER_LT_SURGE },
    { COMPOUND_STRING("ERIKA"),    CURA(HEAL_LOCATION_CELADON_CITY),   FLAG_BADGE04_GET, FLAG_DEFEATED_ERIKA,           TRAINER_LEADER_ERIKA },
    { COMPOUND_STRING("KOGA"),     CURA(HEAL_LOCATION_FUCHSIA_CITY),   FLAG_BADGE05_GET, FLAG_DEFEATED_KOGA,            TRAINER_LEADER_KOGA },
    { COMPOUND_STRING("SABRINA"),  CURA(HEAL_LOCATION_SAFFRON_CITY),   FLAG_BADGE06_GET, FLAG_DEFEATED_SABRINA,         TRAINER_LEADER_SABRINA },
    { COMPOUND_STRING("BLAINE"),   CURA(HEAL_LOCATION_CINNABAR_ISLAND), FLAG_BADGE07_GET, FLAG_DEFEATED_BLAINE,         TRAINER_LEADER_BLAINE },
    { COMPOUND_STRING("GIOVANNI"), CURA(HEAL_LOCATION_VIRIDIAN_CITY),  FLAG_BADGE08_GET, FLAG_DEFEATED_LEADER_GIOVANNI, TRAINER_LEADER_GIOVANNI },
};

// ----------------------------------------------------------------------------
// JOHTO
// ----------------------------------------------------------------------------
// Insígnias: FLAG_INSIGNIA_JOHTO_1..8, só de conteúdo (não mexem em obediência).
// NÃO existe FLAG_DEFEATED_* por líder em Johto: os ginásios perguntam
// `goto_if_defeated TRAINER_JOHTO_LEADER_*`, então quem lembra da vitória é a
// flag do próprio treinador, e é ela que este seletor acende.
static const struct GinasioDoHack sGinasiosJohto[] =
{
    { COMPOUND_STRING("FALKNER"), CURA(HEAL_LOCATION_VIOLET_CITY),     FLAG_INSIGNIA_JOHTO_1, 0, TRAINER_JOHTO_LEADER_FALKNER },
    { COMPOUND_STRING("BUGSY"),   CURA(HEAL_LOCATION_AZALEA_TOWN),     FLAG_INSIGNIA_JOHTO_2, 0, TRAINER_JOHTO_LEADER_BUGSY },
    { COMPOUND_STRING("WHITNEY"), CURA(HEAL_LOCATION_GOLDENROD_CITY),  FLAG_INSIGNIA_JOHTO_3, 0, TRAINER_JOHTO_LEADER_WHITNEY },
    { COMPOUND_STRING("MORTY"),   CURA(HEAL_LOCATION_ECRUTEAK_CITY),   FLAG_INSIGNIA_JOHTO_4, 0, TRAINER_JOHTO_LEADER_MORTY },
    { COMPOUND_STRING("JASMINE"), CURA(HEAL_LOCATION_OLIVINE_CITY),    FLAG_INSIGNIA_JOHTO_5, 0, TRAINER_JOHTO_LEADER_JASMINE },
    { COMPOUND_STRING("CHUCK"),   CURA(HEAL_LOCATION_CIANWOOD_CITY),   FLAG_INSIGNIA_JOHTO_6, 0, TRAINER_JOHTO_LEADER_CHUCK },
    { COMPOUND_STRING("PRYCE"),   CURA(HEAL_LOCATION_MAHOGANY_TOWN),   FLAG_INSIGNIA_JOHTO_7, 0, TRAINER_JOHTO_LEADER_PRYCE },
    { COMPOUND_STRING("CLAIR"),   CURA(HEAL_LOCATION_BLACKTHORN_CITY), FLAG_INSIGNIA_JOHTO_8, 0, TRAINER_JOHTO_LEADER_CLAIR },
};

// ----------------------------------------------------------------------------
// HOENN
// ----------------------------------------------------------------------------
// Insígnias: FLAG_INSIGNIA_HOENN_1..8, também só de conteúdo desde 12/08/2026.
// Aqui existem AS DUAS: a insígnia de conteúdo e a FLAG_DEFEATED_*_GYM do
// vanilla, que é o que a estátua e o guarda da Liga leem.
static const struct GinasioDoHack sGinasiosHoenn[] =
{
    { COMPOUND_STRING("ROXANNE"),      CURA(HEAL_LOCATION_RUSTBORO_CITY),   FLAG_INSIGNIA_HOENN_1, FLAG_DEFEATED_RUSTBORO_GYM,   TRAINER_ROXANNE_1 },
    { COMPOUND_STRING("BRAWLY"),       CURA(HEAL_LOCATION_DEWFORD_TOWN),    FLAG_INSIGNIA_HOENN_2, FLAG_DEFEATED_DEWFORD_GYM,    TRAINER_BRAWLY_1 },
    { COMPOUND_STRING("WATTSON"),      CURA(HEAL_LOCATION_MAUVILLE_CITY),   FLAG_INSIGNIA_HOENN_3, FLAG_DEFEATED_MAUVILLE_GYM,   TRAINER_WATTSON_1 },
    { COMPOUND_STRING("FLANNERY"),     CURA(HEAL_LOCATION_LAVARIDGE_TOWN),  FLAG_INSIGNIA_HOENN_4, FLAG_DEFEATED_LAVARIDGE_GYM,  TRAINER_FLANNERY_1 },
    { COMPOUND_STRING("NORMAN"),       CURA(HEAL_LOCATION_PETALBURG_CITY),  FLAG_INSIGNIA_HOENN_5, FLAG_DEFEATED_PETALBURG_GYM,  TRAINER_NORMAN_1 },
    { COMPOUND_STRING("WINONA"),       CURA(HEAL_LOCATION_FORTREE_CITY),    FLAG_INSIGNIA_HOENN_6, FLAG_DEFEATED_FORTREE_GYM,    TRAINER_WINONA_1 },
    { COMPOUND_STRING("TATE & LIZA"),  CURA(HEAL_LOCATION_MOSSDEEP_CITY),   FLAG_INSIGNIA_HOENN_7, FLAG_DEFEATED_MOSSDEEP_GYM,   TRAINER_TATE_AND_LIZA_1 },
    { COMPOUND_STRING("JUAN"),         CURA(HEAL_LOCATION_SOOTOPOLIS_CITY), FLAG_INSIGNIA_HOENN_8, FLAG_DEFEATED_SOOTOPOLIS_GYM, TRAINER_JUAN_1 },
};

// ----------------------------------------------------------------------------
// SINNOH
// ----------------------------------------------------------------------------
// Insígnias: FLAG_INSIGNIA_SINNOH_1..8. A ORDEM é a que os próprios nomes das
// flags declaram em include/constants/flags.h (Roark, Gardenia, Maylene, Wake,
// Fantina, Byron, Candice, Volkner), que é a do Diamond/Pearl.
// Sem FLAG_DEFEATED_* por líder: os ginásios usam `goto_if_defeated`.
// Sete das oito cidades não têm ponto de cura, daí o CENTRO_SINNOH.
static const struct GinasioDoHack sGinasiosSinnoh[] =
{
    { COMPOUND_STRING("ROARK"),    CURA(HEAL_LOCATION_OREBURGH_CITY),                     FLAG_INSIGNIA_SINNOH_1, 0, TRAINER_SINNOH_LEADER_ROARK },
    { COMPOUND_STRING("GARDENIA"), CENTRO_SINNOH(MAP_ETERNA_CITY_POKECENTER_1F),          FLAG_INSIGNIA_SINNOH_2, 0, TRAINER_SINNOH_LEADER_GARDENIA },
    { COMPOUND_STRING("MAYLENE"),  CENTRO_SINNOH(MAP_VEILSTONE_CITY_POKECENTER_1F),       FLAG_INSIGNIA_SINNOH_3, 0, TRAINER_SINNOH_LEADER_MAYLENE },
    { COMPOUND_STRING("CRASHER WAKE"), CENTRO_SINNOH(MAP_PASTORIA_CITY_POKECENTER_1F),  FLAG_INSIGNIA_SINNOH_4, 0, TRAINER_SINNOH_LEADER_WAKE },
    { COMPOUND_STRING("FANTINA"),  CENTRO_SINNOH(MAP_HEARTHOME_CITY_POKECENTER_1F),       FLAG_INSIGNIA_SINNOH_5, 0, TRAINER_SINNOH_LEADER_FANTINA },
    { COMPOUND_STRING("BYRON"),    CENTRO_SINNOH(MAP_CANALAVE_CITY_POKECENTER_1F),        FLAG_INSIGNIA_SINNOH_6, 0, TRAINER_SINNOH_LEADER_BYRON },
    { COMPOUND_STRING("CANDICE"),  CENTRO_SINNOH(MAP_SNOWPOINT_CITY_POKECENTER_1F),       FLAG_INSIGNIA_SINNOH_7, 0, TRAINER_SINNOH_LEADER_CANDICE },
    { COMPOUND_STRING("VOLKNER"),  CENTRO_SINNOH(MAP_SUNYSHORE_CITY_POKECENTER_1F),       FLAG_INSIGNIA_SINNOH_8, 0, TRAINER_SINNOH_LEADER_VOLKNER },
};

// ----------------------------------------------------------------------------
// UNOVA
// ----------------------------------------------------------------------------
// Insígnias: FLAG_BADGE_UNOVA_*, uma por cidade, sem numeração no nome. A ORDEM
// abaixo é a que a própria ROM declara na Rota 23, onde oito guardas conferem
// uma insígnia cada, em fila: Rt23East pergunta LENTIMAS, CASTELIA, VIRBANK,
// ASPERTIA, STRIATON e MISTRALTON (rótulos R23Badge1..6), Rt23West pergunta
// OPELUCID (R23Badge7) e o portão pergunta HUMILAU (a oitava, que também é a
// que o bloqueio de Undella Town cobra).
// Sem FLAG_DEFEATED_* por líder: os ginásios usam `goto_if_defeated`.
static const struct GinasioDoHack sGinasiosUnova[] =
{
    { COMPOUND_STRING("SHAUNTAL"), CURA(HEAL_LOCATION_UNOVA_LENTIMAS),   FLAG_BADGE_UNOVA_LENTIMAS,   0, TRAINER_UNOVA_LEADER_SHAUNTAL },
    { COMPOUND_STRING("BURGH"),    CURA(HEAL_LOCATION_UNOVA_CASTELIA),   FLAG_BADGE_UNOVA_CASTELIA,   0, TRAINER_UNOVA_LEADER_BURGH },
    { COMPOUND_STRING("ROXIE"),    CURA(HEAL_LOCATION_UNOVA_VIRBANK),    FLAG_BADGE_UNOVA_VIRBANK,    0, TRAINER_UNOVA_LEADER_ROXIE },
    { COMPOUND_STRING("CHEREN"),   CURA(HEAL_LOCATION_UNOVA_ASPERTIA),   FLAG_BADGE_UNOVA_ASPERTIA,   0, TRAINER_UNOVA_LEADER_CHEREN },
    { COMPOUND_STRING("CILAN"),    CURA(HEAL_LOCATION_UNOVA_STRIATON),   FLAG_BADGE_UNOVA_STRIATON,   0, TRAINER_UNOVA_LEADER_CILAN },
    { COMPOUND_STRING("SKYLA"),    CURA(HEAL_LOCATION_UNOVA_MISTRALTON), FLAG_BADGE_UNOVA_MISTRALTON, 0, TRAINER_UNOVA_LEADER_SKYLA },
    { COMPOUND_STRING("DRAYDEN"),  CURA(HEAL_LOCATION_UNOVA_OPELUCID),   FLAG_BADGE_UNOVA_OPELUCID,   0, TRAINER_UNOVA_LEADER_DRAYDEN },
    { COMPOUND_STRING("MARLON"),   CURA(HEAL_LOCATION_UNOVA_HUMILAU),    FLAG_BADGE_UNOVA_HUMILAU,    0, TRAINER_UNOVA_LEADER_MARLON },
};

// ----------------------------------------------------------------------------
// As cinco regiões, na ordem em que aparecem no menu
// ----------------------------------------------------------------------------
//
// "Start of region" é o ponto por onde o jogador ENTRA na região NESTE hack, e
// não a cidade natal do jogo original. Kanto é onde o jogo começa (Pallet Town,
// src/new_game.c); as outras quatro se alcançam de barco, e os portos estão
// escritos em data/scripts/travessia_regioes.inc: OLIVINE (Johto), SLATEPORT
// (Hoenn), CANALAVE (Sinnoh) e VIRBANK (Unova).
//
// A Liga de JOHTO é o mesmo Planalto Índigo de Kanto, e isso não é descuido:
// data/scripts/travessia_regioes.inc registra que esta ROM não tem uma Elite
// dos Quatro de Johto, e que o fim de Johto é a oitava insígnia.
static const struct RegiaoDoHack sRegioes[] =
{
    {
        COMPOUND_STRING("HOENN"),
        CURA(HEAL_LOCATION_SLATEPORT_CITY),
        CURA(HEAL_LOCATION_EVER_GRANDE_CITY_POKEMON_LEAGUE),
        sGinasiosHoenn, ARRAY_COUNT(sGinasiosHoenn),
    },
    {
        COMPOUND_STRING("KANTO"),
        CURA(HEAL_LOCATION_PALLET_TOWN),
        CURA(HEAL_LOCATION_INDIGO_PLATEAU),
        sGinasiosKanto, ARRAY_COUNT(sGinasiosKanto),
    },
    {
        COMPOUND_STRING("JOHTO"),
        CURA(HEAL_LOCATION_OLIVINE_CITY),
        CURA(HEAL_LOCATION_INDIGO_PLATEAU),
        sGinasiosJohto, ARRAY_COUNT(sGinasiosJohto),
    },
    {
        COMPOUND_STRING("SINNOH"),
        CENTRO_SINNOH(MAP_CANALAVE_CITY_POKECENTER_1F),
        CENTRO_SINNOH(MAP_POKEMON_LEAGUE_SOUTH_POKECENTER_1F),
        sGinasiosSinnoh, ARRAY_COUNT(sGinasiosSinnoh),
    },
    {
        COMPOUND_STRING("UNOVA"),
        CURA(HEAL_LOCATION_UNOVA_VIRBANK),
        CURA(HEAL_LOCATION_UNOVA_PKMN_LEAGUE),
        sGinasiosUnova, ARRAY_COUNT(sGinasiosUnova),
    },
};

#define NUM_REGIOES ARRAY_COUNT(sRegioes)

// Capítulos de uma região: o início, um por ginásio, e a Liga.
#define NUM_CAPITULOS(r) ((r)->numGinasios + 2)

static const u8 sTexto_Inicio[]  = _("Start of region");
static const u8 sTexto_Antes[]   = _("Before ");
static const u8 sTexto_Liga[]    = _("Before Pokémon League");
static const u8 sTexto_Sair[]    = _("EXIT");
static const u8 sTexto_Comeco[]  = _("START FROM BEGINNING");

// A ordem da fila do jogo novo. `RunScriptImmediately` usa um contexto de script
// só dele (sImmediateScriptContext, src/script.c:310), então chamá-lo de dentro
// de um special não atropela o roteiro que está rodando.
extern const u8 EventScript_ResetAllMapFlags[];
extern const u8 EventScript_ResetAllMapFlagsFrlg[];

COMMON_DATA u8 gChapterJumpModo = CHAPTER_JUMP_NADA;

// ----------------------------------------------------------------------------
// Montagem dos dois menus
// ----------------------------------------------------------------------------
//
// O mecanismo é o `dynmultistack` que a ROM já usa no menu do barco
// (data/scripts/travessia_regioes.inc): a lista é empilhada item a item e o
// `dynmultistack` a consome, rolando sozinho quando passa de maxBeforeScroll.
// Foi escolhido por ser o único dos três (multichoice fixo, dynmultichoice com
// argv, dynmultistack) que aceita lista MONTADA EM C e ROLA: os dez capítulos
// de uma região não cabem na tela de uma vez.
//
// O `id` empilhado é o que volta em VAR_RESULT, e não a linha escolhida. Aqui id
// e linha coincidem de propósito, para o roteiro poder comparar direto.

// A lista libera cada `name` sozinha quando o menu fecha (FreeListMenuItems em
// src/script_menu.c), então o texto precisa vir do heap, nunca da ROM.
static void EmpilhaOpcao(const u8 *texto, u32 id)
{
    struct ListMenuItem item;
    u8 *copia = Alloc(32);

    if (copia == NULL)
        return;

    StringCopy(copia, texto);
    item.name = copia;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

static void EmpilhaCapitulo(const struct RegiaoDoHack *regiao, u32 capitulo)
{
    struct ListMenuItem item;
    u8 *nome = Alloc(32);

    if (nome == NULL)
        return;

    if (capitulo == 0)
        StringCopy(nome, sTexto_Inicio);
    else if (capitulo > regiao->numGinasios)
        StringCopy(nome, sTexto_Liga);
    else
        StringCopy(StringCopy(nome, sTexto_Antes), regiao->ginasios[capitulo - 1].lider);

    item.name = nome;
    item.id = capitulo;
    MultichoiceDynamic_PushElement(item);
}

// Nível 1: as cinco regiões e a saída. A última entrada muda de nome conforme a
// porta de entrada: pelo item ela é "EXIT", e no jogo novo ela é
// "START FROM BEGINNING", que é o que aquele menu significa ali.
void ChapterJump_MontaListaDeRegioes(void)
{
    u32 i;

    for (i = 0; i < NUM_REGIOES; i++)
        EmpilhaOpcao(sRegioes[i].nome, i);

    EmpilhaOpcao(gChapterJumpModo == CHAPTER_JUMP_JOGO_NOVO ? sTexto_Comeco : sTexto_Sair, NUM_REGIOES);
}

// Nível 2: os capítulos da região escolhida, que chegou em VAR_0x8004.
// Devolve FALSE quando VAR_0x8004 não é região: é assim que o roteiro descobre
// que o jogador escolheu a última entrada da lista (EXIT / START FROM BEGINNING)
// sem precisar saber quantas regiões existem.
u16 ChapterJump_MontaListaDeCapitulos(void)
{
    const struct RegiaoDoHack *regiao;
    u32 i;

    if (gSpecialVar_0x8004 >= NUM_REGIOES)
        return FALSE;

    regiao = &sRegioes[gSpecialVar_0x8004];
    for (i = 0; i < NUM_CAPITULOS(regiao); i++)
        EmpilhaCapitulo(regiao, i);

    return TRUE;
}

// ----------------------------------------------------------------------------
// O pulo
// ----------------------------------------------------------------------------

static void MarcaGinasioVencido(const struct GinasioDoHack *ginasio)
{
    if (ginasio->flagInsignia != 0)
        FlagSet(ginasio->flagInsignia);
    if (ginasio->flagDerrotado != 0)
        FlagSet(ginasio->flagDerrotado);
    if (ginasio->treinador != 0)
        FlagSet(TRAINER_FLAGS_START + ginasio->treinador);
}

static void VaiPara(const struct DestinoDeCapitulo *destino)
{
    if (destino->healLocation != HEAL_LOCATION_NONE)
    {
        // Arruma também o ponto de respawn: desmaiar logo depois do pulo tem que
        // devolver o jogador à cidade do capítulo, não à última em que ele
        // dormiu do outro lado do mundo.
        SetLastHealLocationWarp(destino->healLocation);
        SetWarpDestinationToHealLocation(destino->healLocation);
    }
    else
    {
        // Sinnoh sem ponto de cura: o respawn fica como estava, de propósito.
        // Inventar um aqui exigiria entrada nova em heal_locations.json, e a
        // janela de save está fechada.
        SetWarpDestination(MAP_GROUP(destino->mapa), MAP_NUM(destino->mapa), WARP_ID_NONE, destino->x, destino->y);
    }

    // Mesma trinca do comando `warp` de script (ScrCmd_warp, src/scrcmd.c:968).
    // Quem chama precisa de um `waitstate` logo depois.
    DoWarp();
    ResetInitialPlayerAvatarState();
}

// Roda o capítulo escolhido: região em VAR_0x8004, capítulo em VAR_0x8005.
// A ordem das quatro etapas não é livre: os resets de mapa vêm ANTES das flags
// de insígnia (eles acendem flags de esconder de jogo novo e apagariam o
// progresso que acabamos de montar se viessem depois), e o warp vem por último
// porque ele encerra o roteiro.
void ChapterJump_AplicaCapitulo(void)
{
    const struct RegiaoDoHack *regiao;
    u32 capitulo, i;

    if (gSpecialVar_0x8004 >= NUM_REGIOES)
        gSpecialVar_0x8004 = 0;

    regiao = &sRegioes[gSpecialVar_0x8004];
    capitulo = gSpecialVar_0x8005;
    // Grampeia em vez de recusar. O roteiro só chega aqui com escolha válida,
    // mas este special carrega um `waitstate` implícito (data/specials.inc):
    // voltar sem dar warp travaria o jogo de vez, e travar é pior que pular
    // para o capítulo errado.
    if (capitulo >= NUM_CAPITULOS(regiao))
        capitulo = NUM_CAPITULOS(regiao) - 1;

    // (a) A fiação de jogo novo, os mesmos dois roteiros que src/new_game.c
    // roda. São só `setflag`/`setberrytree`/`setvar`, logo idempotentes, e é o
    // que faz uma save velha ganhar os consertos de fiação que entraram depois
    // dela. Efeito colateral declarado: cena já vista volta a poder acontecer,
    // porque as flags de "esconder NPC de cena" voltam ao estado de jogo novo.
    RunScriptImmediately(EventScript_ResetAllMapFlags);
    RunScriptImmediately(EventScript_ResetAllMapFlagsFrlg);

    // (b) Os ginásios ANTERIORES ao capítulo. Antes do primeiro líder não acende
    // nenhum; "Before Pokémon League" acende os oito.
    for (i = 0; i + 1 < capitulo && i < regiao->numGinasios; i++)
        MarcaGinasioVencido(&regiao->ginasios[i]);

    // (c) Time curado: chegar num capítulo novo com o time desmaiado da luta
    // anterior não testa nada.
    HealPlayerParty();

    // (d) O pulo.
    VaiPara(capitulo == 0 ? &regiao->inicio
          : capitulo > regiao->numGinasios ? &regiao->liga
          : &regiao->ginasios[capitulo - 1].onde);
}
