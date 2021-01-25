#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import collections
from numpy import *
import time

calcUrl = 'http://mfb.bplaced.net/dropcalc/dropcalc.php?lang=en&patch=113&mode=lod&interface=default&window=true'
MagicFind = '650'
hork = 0.52

display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Chrome()
browser.get(calcUrl)

mobs = collections.OrderedDict()
#mobs['85e'] = ['Bossmonster', 'Akt 2', 'Hell', 'Embalmed', 'Akt2 Ancient Tunnels', 0]
#mobs['Pin'] = ['Special Monster', '', 'Hell', 'Pindleskin', '', 0, 0, 0]
mobs['Thr'] = ['Special Monster', '', 'Hell', 'Thresh Socket', '', 0, 0, 0]

colors = {'u': '#A09868', 'g': '#00E000'}

nmob = 0
for mobKey,mob in mobs.items():
  #print('Checking chances for ', mobKey, ' ...')
  browser.switch_to_window(browser.window_handles[0])
  inputMonsterType = browser.find_element_by_name('monstertype')
  inputMonsterType.send_keys(mob[0])
  inputMF = browser.find_element_by_name('mf')
  inputMF.clear()
  inputMF.send_keys(int(MagicFind))
  inputAkt = browser.find_element_by_name('act')
  inputAkt.send_keys(mob[1])
  inputDifficulty = browser.find_element_by_name('difficulty')
  inputDifficulty.send_keys(mob[2])
  inputMonster = browser.find_element_by_name('monster')
  for option in inputMonster.find_elements_by_tag_name('option'):
      if option.text == mob[3]:
          option.click() # select() in earlier versions of webdriver
          break        
  inputLevel = browser.find_element_by_name('level')
  inputLevel.send_keys(mob[4])
  browser.execute_script("W('CalculateMonsterDropsbyForm(0,1)')")
  nmob = nmob + 1
  browser.switch_to_window(browser.window_handles[nmob])
  soup = BeautifulSoup(browser.page_source,features="lxml")
  alltext = soup.find_all('td')
  sum_chance = 0.0
  sum_chance_potion = 0.0
  for tag in (alltext[i:i + 3] for i in range(0, len(alltext), 3)):
    #print(tag.text)
    #print('--------')
    #continue
    item, chance, ratio = tag[0].text, tag[1].text, tag[2].text
    if item == 'Itemname': continue
    #print(tag)
    #print(dir(tag[0]))
    #for attr in dir(tag[0]):
    #  print("tag[0].%s = %r" % (attr, getattr(tag[0], attr)))
    item = item.replace('\n', '')
    chance = float(chance.replace('\n', '').replace('%', ''))*(1+hork)
    ratio = float(ratio.replace('\n', '').replace('1:', ''))
    #print(tag[0])
    if 'font color' in str(tag[0]):
      color = str(tag[0]).split('font color')[1].split('"')[1]
      #print('color = {}'.format(color))
      continue
    if 'Potion' in item and ('Rejuvenation' in item or 'Healing' in item or 'Mana' in item):
      sum_chance_potion += chance
    else:
      print('{} {} {}'.format(item, ratio, chance))
      sum_chance += chance
  #print('sum_chance = {}'.format(sum_chance/100.))
  #print('sum_chance_potion = {}'.format(sum_chance_potion/100.))
