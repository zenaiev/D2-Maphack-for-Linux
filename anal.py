#!/usr/bin/python3
 
import sys
import math
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

def anal(infile, chancesfile, runs):
  print('anal: ', infile, chancesfile, runs)
  assert len(infile) == len(runs)
  loot = {}
  rarity = {}
  nruns = 0
  for f,r in zip(infile,runs):
    nruns += r
    with open(f) as fin:
      for line in fin.readlines():
        if len(line) < 2:
          continue
        rar = str(line[1])
        item = line[4:-1] # remove end of line
        #if 'Potion' in item and ('Rejuvenation' in item or 'Healing' in item or 'Mana' in item):
        if 'Potion' in item:
          continue
        rarity[rar] = rarity.get(rar, 0) + 1
        loot[item] = loot.get(item, 0) + 1

  report = {}
  sum_exp, sum_obs = 0.0, 0.0
  sum_sigma = 0.0
  with open(chancesfile) as f:
    for line in f.readlines():
      item, chance = ' '.join(line.split(' ')[:-2]), float(line.split(' ')[-1])/100.
      if 'Potion' in item:
        continue
      #print(item, chance)
      expect = chance * nruns
      unc = math.sqrt(expect)
      obs = loot.get(item, 0)
      prob = scipy.stats.poisson.cdf(obs, expect)
      sigma = (obs-expect)/unc
      sigma_prob = scipy.stats.norm.ppf(prob)
      if obs == 0 and prob > 0.5:
        #sigma_prob *= -1
        #sigma_prob = 0
        sigma_prob = sigma
      sum_sigma += sigma_prob
      #print('{} {}+-{} -> {} [{}] [{}] [{}]'.format(item, expect, unc, obs, prob, sigma, sigma_prob))
      #print('{:25s} {:10.3f}  +-{:7.3f}    -> {:5d} [{:.3f}] [{:+7.3f}] [{:+7.3f}]'.format(item, expect, unc, obs, prob, sigma, sigma_prob))
      print('{:25s} {:10.3f}  +-{:7.3f}    -> {:5d} [{:.3f}] [{:+7.3f}]'.format(item, expect, unc, obs, prob, sigma_prob))
      report[item] = (expect, unc, obs, prob, sigma_prob)
      sum_exp += expect
      sum_obs += obs
  #print('loot: {}'.format(loot))
  print('rarity: {}'.format(rarity))
  print('rariry per run: {}'.format({k: round(v/nruns,3) for k,v in rarity.items()}))
  allitems = rarity['b'] + rarity['y'] + rarity['u'] + rarity['g']
  print('fractions: b = {:.3f} y = {:.3f} u = {:.3f} g = {:.3f}'.format(rarity['b']/allitems, rarity['y']/allitems, rarity['u']/allitems, rarity['g']/allitems))
  print('len(report), len(loot): ', len(report), len(loot))
  print('strange: ', [x for x in loot.keys() if x not in report.keys()])
  print('sum_sigma = {:+.3f}'.format(sum_sigma/len(report)))
  sum_prob = scipy.stats.poisson.cdf(sum_obs, sum_exp)
  sum_sigma = scipy.stats.norm.ppf(sum_prob)
  print('all expected {:.0f}, observed {:.0f} [prob {:.3f} sigma {:+.3f}]'.format(sum_exp, sum_obs, sum_prob, sum_sigma))

  report_runes = {k:v for k,v in report.items() if ' Rune' in k}
  plot(report_runes, 'plots/runes.pdf')
  report = {k:v for k,v in report.items() if k not in report_runes.keys()}
  report_gems = {k:v for k,v in report.items() if 'Chipped ' in k or 'Flawed ' in k or 'Flawless ' in k or 'Diamond' == k or 'Ruby' == k or 'Sapphire' == k or 'Amethyst' == k or 'Topaz' == k or 'Emerald' == k or 'Skull' == k}
  plot(report_gems, 'plots/gems.pdf')
  report = {k:v for k,v in report.items() if k not in report_gems.keys()}
  print('len(report) = {}'.format(len(report)))
  n = 100
  iplot = 0
  rep = {}
  for idx, k in enumerate(report):
    if idx % n == 0:
      print('printing {}'.format(idx))
      if iplot > 0:
        plot(rep, 'plots/plot{}.pdf'.format(iplot))
      rep = {}
      iplot += 1
    rep.update({k:report[k]})
  plot(rep, 'plots/plot{}.pdf'.format(iplot))

def plot(report, fout):
  plt.rcParams.update({'font.size': 14})
  nplot = len(report)
  fig, ax = plt.subplots(2, 1, sharex=True, figsize=(19.9,8))
  #ax[0].grid(axis='x')
  ax[0].set_axisbelow(True)
  ax[1].grid()
  ax[1].set_axisbelow(True)
  ax[0].bar(range(nplot), [v[0] for v in report.values()])
  ax[0].plot(range(nplot), [v[2] for v in report.values()], 'o', color='darkviolet')
  ax[1].bar(range(nplot), [v[4] for v in report.values()])
  ax[1].set_ylim([-5, 5])
  ax[1].set_xlim([-1, len(report)])
  plt.xticks(range(nplot), list(report.keys())[:nplot], rotation='vertical')
  fig.tight_layout()
  fig.subplots_adjust(hspace=0.01)
  fig.savefig(fout)

if __name__ == '__main__':
  chancesfile = 'thr.txt'
  runs = []
  infile = []
  if len(sys.argv) >= 2:
    for arg in sys.argv[1:]:
      infile.append(arg)
      if len(infile[-1].split('-')) > 1:
        runs.append(int(infile[-1].split('-')[2].split('.')[0]))
      else:
        runs.append(1)
  if len(sys.argv) == 3:
    try:
      runs = [int(sys.argv[2])]
      infile = infile[:-1]
    except:
      ...
  if len(infile) == 0:
    infile = ['loot.txt']
    runs = [1]
  anal(infile, chancesfile, runs)