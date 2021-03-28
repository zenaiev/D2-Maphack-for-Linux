#include "lootlogger.h"
#include "patch.h"
#include <sys/stat.h>
#include <stdio.h>
#include <time.h>
#include <utime.h>
#include "string.h"

bool lootlogger_id[LOOTLOGGER_MAXITEMS] = { false };
int lootlogger_nloot = 0;
int lootlogger_mtime = 0;
const char* lootlogger_fout = "/home/zenaiev/games/Diablo2/502/lootfilter/D2-Maphack-for-Linux/loot.txt";

void lootlogger_item(unit_any* item, char* name)
{
  // ned to check flags: my items have flags             8388624
  if(lootlogger_mtime == 0)
    lootlogger_mtime = lootlogger_get_mtime();
  int mtime = lootlogger_get_mtime();
  if(lootlogger_mtime != mtime)
  {
    lootlogger_mtime = mtime;
    for(int i = 0; i < LOOTLOGGER_MAXITEMS; i++)
      lootlogger_id[i] = false;
  }
  if(lootlogger_id[item->id]) return;
  lootlogger_id[item->id] = true;
  if(item->item_data->owner_inventory || item->item_data->item_location != 0) return;
  //strcpy(lootlogger_loot[lootlogger_nloot]+4, name);
  char rarity = 'w';
  if(item->item_data->quality == 4) 
    rarity = 'b';
  else if(item->item_data->quality == 5) 
    rarity = 'g';
  else if(item->item_data->quality == 6) 
    rarity = 'y';
  else if(item->item_data->quality == 7) 
    rarity = 'u';
  else if(strstr(name, " Rune") != NULL)
    rarity = 'o';
  //sprintf(lootlogger_loot[lootlogger_nloot], "[%c] %s\n", rarity, name);
  //lootlogger_nloot++;
  //printf(" >>> NEW LOOT[%u]: %s\n", item->id, lootlogger_loot[lootlogger_nloot]);
  printf(" >>> NEW LOOT[%u]: [%c] %s\n", item->id, rarity, name);
  print_item(item);
  FILE* fout = fopen(lootlogger_fout, "a+");
  //fprintf(fout, "%s\n", lootlogger_loot[lootlogger_nloot]);
  fprintf(fout, "[%c] %s\n", rarity, name);
  fclose(fout);
}

void lootlogger_print()
{
  printf("_____________\n");
  printf("ALL LOOT [%u]:\n", lootlogger_nloot);
  for(int i = 0; i < lootlogger_nloot; i++)
  {
    ;//printf(" *** %s\n", lootlogger_loot[i]);
  }
  printf("_____________\n");
}

long int lootlogger_get_mtime()
{
  const char *filename = "/home/zenaiev/games/Diablo2/502/lootfilter/D2-Maphack-for-Linux/ln-loot-character";
  struct stat foo;
  time_t mtime;
  //struct utimbuf new_times;
  if (stat(filename, &foo) < 0) {
    perror(filename);
    return 1;
  }
  mtime = foo.st_mtime; /* seconds since the epoch */
  //printf("mtime: %ld\n", mtime);
  return mtime;
}