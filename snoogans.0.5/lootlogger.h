#pragma once
#include "d2pointers.h"
#include "stdbool.h"

#define LOOTLOGGER_MAXITEMS 100000
bool lootlogger_id[LOOTLOGGER_MAXITEMS];
//int lootlogger_nloot;
//char lootlogger_loot[LOOTLOGGER_MAXITEMS][512];

void lootlogger_item(unit_any* item, char* name);
void lootlogger_print();
long int lootlogger_get_mtime();
