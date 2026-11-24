[![news](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Orochim25/news-image-20261124-acct2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Orochim25/news-image-20261124-acct2/reward.svg)](https://make.fun/bounty/news-image-20261124)

# The World in One Day — Tuesday, 24 November 2026

A broadsheet newspaper image summing up 24 November 2026 in 31 verified
stories, drawn entirely with PIL flat-vector art (no AI photos).

Layout: 9 hero scenes — 3 large heroes on top (Hormuz tankers, Ulleung
air-raid alert, Sanofi's $41bn Insmed deal) and 6 smaller heroes below
(US chip blacklist, EU budget rejection, Estonia warning, Iran courts'
$290bn demand, Gaza strikes, Nepal quake) — each with its own bold,
high-contrast illustration. Plus the UTC strip, the day in numbers, the
world map with all 31 stories plotted at their true coordinates, the
"also on" list, and a date-check bar.

- `build.py` — draws `entry.png` (1024×1024, PNG) with PIL.
- `main.py` — copies `entry.png` to `/output/entry.png`, deterministically.
- `entry.png` — the submitted image.
