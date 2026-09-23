#include "global.h"
#include "chapter_jump.h"
#include "event_data.h"
#include "field_screen_effect.h"
#include "pokemon.h"
#include "constants/moves.h"
#include "constants/species.h"
#include "list_menu.h"
#include "malloc.h"
#include "overworld.h"
#include "script.h"
#include "script_menu.h"
#include "script_pokemon_util.h"
#include "string_util.h"
#include "constants/flags.h"
#include "constants/heal_locations.h"
#include "constants/opponents.h"
#include "constants/opponents_frlg.h"
#include "constants/items.h"
#include "constants/pokemon.h"
#include "config/battle.h"
#include "item.h"

// Nível do time que o seletor entrega a quem salta com a party vazia.
// Era 20 até 07/09/2026, quando o time virou cinco: nível 50 é o que
// aguenta chefe de qualquer capítulo, inclusive a Liga.
#define NIVEL_DO_TIME_DE_TESTE 50

// ============================================================================
// CHAPTER JUMP, o seletor de capítulo (ITEM_CHAPTER_JUMP, id 879)
// ============================================================================
//
// PARA QUE SERVE
//
// Retestar qualquer trecho das quatro regiões sem recomeçar save. O jogador
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
// São 40 capítulos (4 regiões x (1 início + 8 ginásios + 1 Liga)). Escritos à
// mão em .inc seriam 40 blocos quase iguais, e capítulo novo custaria um bloco
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
    // O ponto de cura já é a coordenada certa do Centro Pokémon e ainda
    // arruma o ponto de respawn de quem desmaiar (dev_scripts/
    // heal_locations_sinnoh_ginasios.py, Fase C, 18/08/2026: as sete
    // cidades de ginásio de Sinnoh e a Liga sul ganharam HEAL_LOCATION_*
    // próprio, então o caminho por mapa e coordenada não é mais preciso
    // aqui).
    u16 healLocation;
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
    // vez de ler uma FLAG_DEFEATED_* própria (Johto e Sinnoh).
    u16 treinador;
    // 0 quando o ginásio não tem trava de enredo FORA dele. Quando tem, é a
    // flag do acontecimento que precisa ter acontecido para o jogador CHEGAR
    // neste ginásio, e o salto a acende (e a apaga nos capítulos anteriores,
    // para o par negativo continuar valendo). Entrou em 06/09/2026 com o
    // ginásio de ECRUTEAK: quem pula para "Before MORTY" tem que achar a porta
    // do ginásio aberta, e quem abre é a cena dos três cães da BURNED TOWER,
    // que o seletor não roda. Campo no fim da struct de propósito: as outras
    // 39 linhas não mudam uma vírgula e ficam com 0 por omissão.
    u16 flagEnredo;
};

struct RegiaoDoHack
{
    const u8 *nome;
    // Onde a região começa NESTE hack. Ver a nota de cada região.
    struct DestinoDeCapitulo inicio;
    // A Liga daquela região, ou healLocation 0 quando a região NÃO TEM Liga
    // nesta ROM. No cartucho 1 as quatro regiões têm Liga, e o campo continua
    // porque oferecer "Before Pokémon League" numa região sem Liga seria
    // capítulo mentiroso.
    struct DestinoDeCapitulo liga;
    const struct GinasioDoHack *ginasios;
    u8 numGinasios;
};

// Atalho de leitura: todo destino é um ponto de cura.
#define CURA(hl) { hl }

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
    { COMPOUND_STRING("MORTY"),   CURA(HEAL_LOCATION_ECRUTEAK_CITY),   FLAG_INSIGNIA_JOHTO_4, 0, TRAINER_JOHTO_LEADER_MORTY, FLAG_JOHTO_CAES_LIBERTOS },
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
// As sete cidades que não tinham ponto de cura ganharam o delas em
// dev_scripts/heal_locations_sinnoh_ginasios.py (Fase C, 18/08/2026).
static const struct GinasioDoHack sGinasiosSinnoh[] =
{
    { COMPOUND_STRING("ROARK"),        CURA(HEAL_LOCATION_OREBURGH_CITY),   FLAG_INSIGNIA_SINNOH_1, 0, TRAINER_SINNOH_LEADER_ROARK },
    { COMPOUND_STRING("GARDENIA"),     CURA(HEAL_LOCATION_ETERNA_CITY),     FLAG_INSIGNIA_SINNOH_2, 0, TRAINER_SINNOH_LEADER_GARDENIA },
    { COMPOUND_STRING("MAYLENE"),      CURA(HEAL_LOCATION_VEILSTONE_CITY),  FLAG_INSIGNIA_SINNOH_3, 0, TRAINER_SINNOH_LEADER_MAYLENE },
    { COMPOUND_STRING("CRASHER WAKE"), CURA(HEAL_LOCATION_PASTORIA_CITY),   FLAG_INSIGNIA_SINNOH_4, 0, TRAINER_SINNOH_LEADER_WAKE },
    { COMPOUND_STRING("FANTINA"),      CURA(HEAL_LOCATION_HEARTHOME_CITY),  FLAG_INSIGNIA_SINNOH_5, 0, TRAINER_SINNOH_LEADER_FANTINA },
    { COMPOUND_STRING("BYRON"),        CURA(HEAL_LOCATION_CANALAVE_CITY),   FLAG_INSIGNIA_SINNOH_6, 0, TRAINER_SINNOH_LEADER_BYRON },
    { COMPOUND_STRING("CANDICE"),      CURA(HEAL_LOCATION_SNOWPOINT_CITY),  FLAG_INSIGNIA_SINNOH_7, 0, TRAINER_SINNOH_LEADER_CANDICE },
    { COMPOUND_STRING("VOLKNER"),      CURA(HEAL_LOCATION_SUNYSHORE_CITY),  FLAG_INSIGNIA_SINNOH_8, 0, TRAINER_SINNOH_LEADER_VOLKNER },
};

// ----------------------------------------------------------------------------
// As quatro regiões, na ordem em que aparecem no menu
// ----------------------------------------------------------------------------
//
// "Start of region" é o ponto por onde o jogador ENTRA na região NESTE hack, e
// não a cidade natal do jogo original. Kanto é onde o jogo começa (Pallet Town,
// src/new_game.c); as outras três se alcançam de barco, e os portos estão
// escritos em data/scripts/travessia_regioes.inc: OLIVINE (Johto), SLATEPORT
// (Hoenn) e CANALAVE (Sinnoh).
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
        CURA(HEAL_LOCATION_CANALAVE_CITY),
        CURA(HEAL_LOCATION_POKEMON_LEAGUE_SOUTH),
        sGinasiosSinnoh, ARRAY_COUNT(sGinasiosSinnoh),
    },
};

#define NUM_REGIOES ARRAY_COUNT(sRegioes)

// Capítulos de uma região: o início, um por ginásio, e a Liga QUANDO EXISTE.
// Região sem Liga teria um capítulo a menos, em vez de uma linha que levaria a
// lugar nenhum. No cartucho 1 as quatro têm Liga.
#define TEM_LIGA(r) ((r)->liga.healLocation != 0)
#define NUM_CAPITULOS(r) ((r)->numGinasios + 1 + (TEM_LIGA(r) ? 1 : 0))

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
    else if (capitulo > regiao->numGinasios && TEM_LIGA(regiao))
        StringCopy(nome, sTexto_Liga);
    else
        StringCopy(StringCopy(nome, sTexto_Antes), regiao->ginasios[capitulo - 1].lider);

    item.name = nome;
    item.id = capitulo;
    MultichoiceDynamic_PushElement(item);
}

// Nível 1: as quatro regiões e a saída. A última entrada muda de nome conforme a
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
    // Arruma também o ponto de respawn: desmaiar logo depois do pulo tem que
    // devolver o jogador à cidade do capítulo, não à última em que ele
    // dormiu do outro lado do mundo. Todo destino tem HEAL_LOCATION_* próprio
    // desde a Fase C (18/08/2026): as sete cidades de ginásio de Sinnoh e a
    // Liga sul ganharam o delas em dev_scripts/heal_locations_sinnoh_ginasios.py.
    SetLastHealLocationWarp(destino->healLocation);
    SetWarpDestinationToHealLocation(destino->healLocation);

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
    //
    // A INSÍGNIA DO MOTOR entra JUNTO, por ÍNDICE, e isso entrou em 23/08/2026.
    // Medido, não suposto: os oito golpes de campo perguntam FLAG_BADGE01..08_GET
    // e mais nada (src/field_move.c:11-64). Nesta ROM os ramos `IS_FRLG` daquele
    // arquivo estão MORTOS, e isso foi medido e não suposto: `IS_FRLG` é
    // constante de compilação e vale 0 aqui (include/constants/global.h:76, o
    // ramo Emerald), então Rock Smash pede a 03 em Kanto também, Strength pede a
    // 04 e Surf a 05, no mapa que for. `flagInsignia` só É a insígnia do
    // motor em KANTO; Hoenn, Johto e Sinnoh acendem FLAG_INSIGNIA_*, e nenhuma
    // dessas destrava golpe de campo.
    // Consequência que o playtest batia de frente: pular para "Before CANDICE"
    // entregava um Pikachu com Surf, Rock Smash e Strength que o motor RECUSA, e
    // o jogador de teste não atravessava lago nem quebrava pedra em cinco das
    // seis regiões. Uma linha, custo ZERO de save (as oito já existem).
    //
    // Por ÍNDICE, e não incondicional, porque o par negativo T99.2 mede o
    // contrário e está certo: "Start of region" de Kanto tem que sair em Pallet
    // Town com as OITO APAGADAS. Capítulo 0 é "não ganhei nada ainda" em toda
    // região; quem quer andar com HM escolhe o capítulo do ginásio.
    for (i = 0; i + 1 < capitulo && i < regiao->numGinasios; i++)
    {
        MarcaGinasioVencido(&regiao->ginasios[i]);
        if (i < 8)
            FlagSet(FLAG_BADGE01_GET + i);
    }

    // (b2) As travas de ENREDO que ficam FORA do ginásio, 06/09/2026. Aqui a
    // conta é `i < capitulo` e não `i + 1 < capitulo`: a cena que abre a porta
    // do ginásio i é pré-requisito DELE, não do seguinte, então "Before MORTY"
    // (capítulo 4 de Johto) já precisa dela acesa. E apaga nos capítulos
    // anteriores, senão pular de uma save adiantada para "Before FALKNER"
    // deixaria Ecruteak sem o sábio que ainda deveria estar lá.
    for (i = 0; i < regiao->numGinasios; i++)
    {
        if (regiao->ginasios[i].flagEnredo == 0)
            continue;
        if (i < capitulo)
            FlagSet(regiao->ginasios[i].flagEnredo);
        else
            FlagClear(regiao->ginasios[i].flagEnredo);
    }

    // (c) O ARSENAL DAS MECÂNICAS MODERNAS, e ele é da MOCHILA, não do time.
    // Quem salta ganha os quatro aparelhos, porque sem eles as mecânicas nem
    // aparecem no menu de batalha, e isso foi MEDIDO, não suposto:
    // `CanMegaEvolve` recusa sem ITEM_MEGA_RING (src/battle_util.c:8426),
    // `CanUseZMove` sem ITEM_Z_POWER_RING (src/battle_z_move.c:121),
    // `CanDynamax` sem ITEM_DYNAMAX_BAND E sem B_FLAG_DYNAMAX_BATTLE acesa
    // (src/battle_dynamax.c:86 e :88) e `CanTerastallize` sem ITEM_TERA_ORB e
    // sem B_FLAG_TERA_ORB_CHARGED (src/battle_terastal.c:77 e :86).
    //
    // O jogo novo (src/new_game.c) já dava a Dynamax Band e o Mega Ring, mas
    // NUNCA deu o Z-Power Ring nem a Tera Orb: até 07/09/2026 o Z-move e o
    // Terastal eram inalcançáveis para o jogador em qualquer save desta ROM,
    // e nenhum teste pegava porque nenhum teste chegava a abrir o menu.
    // Aqui os quatro entram no salto, que é a ferramenta de teste, e por isso
    // vale para save velha também. Custo de save ZERO: são itens na mochila,
    // que já existe, e duas flags que já existem; nenhum índice de save muda.
    //
    // Condicional para não empilhar cópias a cada salto (item-chave repetido
    // não dá poder nenhum e só suja a mochila do jogador).
    if (!CheckBagHasItem(ITEM_MEGA_RING, 1))
        AddBagItem(ITEM_MEGA_RING, 1);
    if (!CheckBagHasItem(ITEM_Z_POWER_RING, 1))
        AddBagItem(ITEM_Z_POWER_RING, 1);
    if (!CheckBagHasItem(ITEM_DYNAMAX_BAND, 1))
        AddBagItem(ITEM_DYNAMAX_BAND, 1);
    if (!CheckBagHasItem(ITEM_TERA_ORB, 1))
        AddBagItem(ITEM_TERA_ORB, 1);
#if B_FLAG_DYNAMAX_BATTLE != 0
    FlagSet(B_FLAG_DYNAMAX_BATTLE);
#endif
#if B_FLAG_TERA_ORB_CHARGED != 0
    // A Terastalização GASTA a carga (B_FLAG_TERA_ORB_NO_COST é 0 aqui), e
    // quem devolve é `HealPlayerParty`, o item (d) logo abaixo, que só recarrega
    // se a Tera Orb estiver na mochila. Por isso a orbe entra ANTES dele.
    FlagSet(B_FLAG_TERA_ORB_CHARGED);
#endif

    // (c2) Ninguém teleporta sem Pokémon (pedido do Gui, 18/08/2026): quem
    // salta com a party VAZIA (jogo novo que pulou a escolha do inicial)
    // ganha um TIME DE CINCO, nível 50, montado para exercitar as quatro
    // mecânicas modernas de uma vez (pedido do Gui, 07/09/2026; antes disto
    // era um Pikachu nível 20 sozinho).
    //
    // POR QUE NÍVEL 50 E NÃO 20. O time de teste tem que aguentar qualquer
    // chefe de qualquer capítulo, inclusive a Liga, senão a batalha acaba
    // antes de dar tempo de abrir o menu da mecânica. O modo de teste LV.5
    // TRAINERS não rebaixa isto: ele mexe SÓ na party do TREINADOR
    // (src/battle_main.c:2003, dentro do laço que monta `party` a partir de
    // `partyData` do oponente), e o time do jogador não passa por ali.
    //
    // POR QUE O RAICHU CARREGA A SUÍTE DE HM INTEIRA. Surf, Rock Smash e
    // Strength são golpes de MOVIMENTAÇÃO, e a suíte de testes críticos
    // inteira depende deles (T112.4, T166.2, T166.3, T166.4 e os blocos de
    // pedra de Sinnoh). `ScrCmd_checkfieldmove` (src/scrcmd.c:2307) varre a
    // party do índice 0 para cima e PARA no primeiro que conhece o golpe:
    // pondo os três no slot 0, a rota de cada caso continua valendo letra por
    // letra, porque quem responde ao `checkfieldmove` continua sendo o
    // primeiro Pokémon do time. A insígnia que o motor exige junto
    // (FLAG_BADGE03_GET para Rock Smash, 04 para Strength, 05 para Surf,
    // src/field_move.c:11-64) vem do item (b) acima, por índice.
    //
    // O QUE CADA UM PROVA:
    //   Raichu   + Raichunite Y  -> Mega Raichu Y  (SPECIES_RAICHU_MEGA_Y,
    //                               form_change_tables.h:97) + a suíte de HM.
    //   Charizard, fator Gmax    -> Gigantamax (FORM_CHANGE_BATTLE_GIGANTAMAX
    //                               só dispara com `gmaxFactor`,
    //                               src/pokemon.c:6277) + Fly de campo.
    //   Mew      + Mewnium Z     -> Genesis Supernova, que é Z-move de
    //                               ASSINATURA e exige MOVE_PSYCHIC no time
    //                               (src/battle_z_move.c:91): por isso o
    //                               Psychic é o slot 0 dele e não decoração.
    //   Incineroar, tera Dark    -> Terastal (MON_DATA_TERA_TYPE gravado; sem
    //                               gravar, o tipo tera sairia da PERSONALITY,
    //                               src/pokemon.c:2445).
    //   Lucario  + Lucarionite Z -> Mega Lucario Z (SPECIES_LUCARIO_MEGA_Z,
    //                               form_change_tables.h:880).
    //
    // UMA MECÂNICA DE CADA TIPO POR BATALHA, e isso é do motor, não do time:
    // `HasTrainerUsedGimmick` marca por TREINADOR, então o Mega Raichu Y e o
    // Mega Lucario Z NÃO cabem na mesma batalha (os dois são Mega). Dynamax,
    // Z-move e Terastal, sendo de tipos diferentes, cabem os três junto com UM
    // dos dois Megas.
    //
    // Personality fixa e DIFERENTE por bicho, de propósito: ferramenta de
    // teste, determinismo vale mais que variedade, e personality repetida
    // deixaria os cinco com a mesma natureza e a mesma metade de IV.
    //
    // MOVE_NONE na tabela quer dizer SLOT VAZIO, e isso foi medido no menu de
    // golpes do emulador, não suposto: o `CreateMon` deste fork
    // (src/pokemon.c) NÃO chama `GiveMonInitialMoveset`, então o que o bicho
    // sabe é exatamente o que esta tabela escreve, e mais nada.
    if (CalculatePlayerPartyCount() == 0)
    {
        static const struct
        {
            u16 especie;
            u16 item;
            u16 golpes[MAX_MON_MOVES];
            u32 personality;
            u8 tipoTera;
            bool8 fatorGmax;
        } sTimeDeTeste[] =
        {
            {
                SPECIES_RAICHU, ITEM_RAICHUNITE_Y,
                {MOVE_THUNDERBOLT, MOVE_SURF, MOVE_ROCK_SMASH, MOVE_STRENGTH},
                0x00C0FFEE, TYPE_NONE, FALSE,
            },
            {
                SPECIES_CHARIZARD, ITEM_NONE,
                // Flamethrower junto com o Fly porque o golpe G-Max do
                // Charizard é o G-Max Wildfire, de tipo FOGO
                // (sGMaxMoveTable, src/battle_dynamax.c): sem golpe de fogo o
                // Gigantamax dispararia e mostraria só Max Airstream, e a
                // prova ficaria muda sobre a forma.
                // Sunny Day é de STATUS de propósito, pela mesma razão do
                // Bulk Up do Incineroar: sob Dynamax golpe de status vira
                // MAX GUARD, que não machuca, e é o único jeito de gastar o
                // Dynamax sem encerrar a batalha (ver o comentário do
                // Incineroar sobre a fila das mecânicas).
                {MOVE_FLAMETHROWER, MOVE_FLY, MOVE_SUNNY_DAY, MOVE_NONE},
                0x0BADF00D, TYPE_NONE, TRUE,
            },
            {
                SPECIES_MEW, ITEM_MEWNIUM_Z,
                // O DIVE do slot 3 é o que deixa a suíte provar o mergulho da
                // Route 41 para a Undersea Cavern (T272.8, 11/09/2026). Ele
                // entrou NO SLOT VAZIO de propósito: o Psychic do slot 0 é o
                // que `CanUseZMove` exige para o Genesis Supernova, e trocar
                // qualquer um dos outros três apagaria prova que já existe.
                // Mew aprende todo HM, então o golpe não é enxerto: é o bicho
                // que o Gui escolheu fazendo o que ele sabe fazer.
                {MOVE_PSYCHIC, MOVE_CUT, MOVE_FLASH, MOVE_DIVE},
                0x0DEFACED, TYPE_NONE, FALSE,
            },
            {
                // MÃOS VAZIAS, E ISSO CUSTA UMA ORDEM NA DEMONSTRAÇÃO.
                // MEDIDO em 07/09/2026, com a mecânica lida da EWRAM em duas
                // execuções do gba_runner, e não deduzido: `AssignUsableGimmicks`
                // (src/battle_gimmick.c:20) dá a cada lutador UMA mecânica só, a
                // PRIMEIRA da fila MEGA, ULTRA BURST, Z-MOVE, DYNAMAX, TERA
                // (a ordem do enum em include/battle_gimmick.h). Um Pokémon do
                // jogador de mãos vazias sempre cai no DYNAMAX, que vem ANTES do
                // TERA, então o START do menu de golpes oferece Dynamax.
                //
                // Segurar uma Mega Stone inerte foi TENTADO e NÃO resolve: ela
                // derruba o Dynamax (src/battle_dynamax.c:111), mas `CanTerastallize`
                // recusa Mega Stone e Z-Crystal pela MESMA linha
                // (src/battle_terastal.c:102), e o Incineroar ficava sem mecânica
                // NENHUMA. Medido com ITEM_DARKRANITE na mão: nenhum gatilho no
                // menu, `FLAG_B8_TERA_ORB_CARREGADO` intacta no fim da luta.
                //
                // Sobra a ordem, e ela é do MOTOR, não deste time: cada mecânica
                // é uma vez por batalha, então DEPOIS de o Charizard Dynamaxar,
                // `CanDynamax` recusa o time inteiro e o Incineroar cai no TERA.
                // Dynamaxar primeiro, Terastalizar depois, na MESMA batalha.
                //
                // O BULK UP NO SLOT 3 É DE STATUS, e é ele que dá o caminho
                // curto: golpe de status vira MAX GUARD sob Dynamax, que não
                // machuca ninguém. Com ele, o próprio Incineroar gasta o
                // Dynamax num turno sem derrubar o adversário e Terastaliza no
                // turno seguinte, na mesma batalha e sem depender do Charizard.
                SPECIES_INCINEROAR, ITEM_NONE,
                {MOVE_DARKEST_LARIAT, MOVE_FLARE_BLITZ, MOVE_BULK_UP, MOVE_NONE},
                0x0FEEDBEE, TYPE_DARK, FALSE,
            },
            {
                SPECIES_LUCARIO, ITEM_LUCARIONITE_Z,
                {MOVE_AURA_SPHERE, MOVE_CLOSE_COMBAT, MOVE_NONE, MOVE_NONE},
                0x0C0DEBED, TYPE_NONE, FALSE,
            },
        };
        u32 mao, golpe;

        for (mao = 0; mao < ARRAY_COUNT(sTimeDeTeste); mao++)
        {
            struct Pokemon mon;
            u32 dado;

            CreateMon(&mon, sTimeDeTeste[mao].especie, NIVEL_DO_TIME_DE_TESTE,
                      sTimeDeTeste[mao].personality, OTID_STRUCT_PLAYER_ID);

            for (golpe = 0; golpe < MAX_MON_MOVES; golpe++)
            {
                if (sTimeDeTeste[mao].golpes[golpe] != MOVE_NONE)
                    SetMonMoveSlot(&mon, sTimeDeTeste[mao].golpes[golpe], golpe);
            }

            if (sTimeDeTeste[mao].item != ITEM_NONE)
            {
                dado = sTimeDeTeste[mao].item;
                SetMonData(&mon, MON_DATA_HELD_ITEM, &dado);
            }

            if (sTimeDeTeste[mao].tipoTera != TYPE_NONE)
            {
                dado = sTimeDeTeste[mao].tipoTera;
                SetMonData(&mon, MON_DATA_TERA_TYPE, &dado);
            }

            if (sTimeDeTeste[mao].fatorGmax)
            {
                dado = TRUE;
                SetMonData(&mon, MON_DATA_GIGANTAMAX_FACTOR, &dado);
            }

            // Sem isto o mon nasce com maxHP 0 e chega DESMAIADO (o CreateMon
            // deste fork deixa o cálculo de stats para o chamador, como o clamp
            // de nível do LV.5 já fazia; bug pego pelo fechador do D3 em 18/08).
            CalculateMonStats(&mon);
            CopyMon(&gPlayerParty[mao], &mon, sizeof(mon));
        }

        CalculatePlayerPartyCount();
        FlagSet(FLAG_SYS_POKEMON_GET);
    }

    // (d) Time curado: chegar num capítulo novo com o time desmaiado da luta
    // anterior não testa nada.
    HealPlayerParty();

    // (e) O pulo. `capitulo > numGinasios` só é Liga quando ela existe, e o
    // grampo acima garante que região sem Liga nunca chega aqui com capítulo
    // fora do início.
    VaiPara(capitulo == 0 ? &regiao->inicio
          : (capitulo > regiao->numGinasios && TEM_LIGA(regiao)) ? &regiao->liga
          : &regiao->ginasios[capitulo - 1].onde);
}
