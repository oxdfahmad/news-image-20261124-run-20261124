# The World — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/oxdfahmad/news-image-20261124-run-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/oxdfahmad/news-image-20261124-run-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper front page summing up Tuesday 24 November 2026 in six verified
stories, drawn as one 1024×1024 image. Every story below happened, or was
first reported, on 24 November 2026, checked against live reporting from
CNN, AP, Reuters, Le Monde, WSJ and BBC on the day itself. Nothing here is
speculation.

## The six stories

1. **Climate (lead)** — COP31 collapses in Antalya: after two weeks, the
   longest COP in history ends Sunday with no deal — the first major
   breakdown since Copenhagen 2009. The EU refused a text that never
   mentioned fossil fuels; the US stayed out.
2. **War at sea** — Ukraine sinks the Russian corvette Merkury off Libya:
   seven sea drones struck in Benghazi on Sunday, 2,400 km from the front
   line; a Ka-27 helicopter was destroyed and the cargo ship Angara hit.
3. **Indonesia** — A fire at the Milkita candy factory in Serang, Banten,
   kills 24 people; about 30 workers remain missing.
4. **Markets** — Jensen Huang returns to Nvidia; the company adds nearly
   $1tn in value as tech stocks rally, and Donald Trump urges his comeback
   as chief executive.
5. **Justice** — The International Court of Justice rules Myanmar committed
   genocide against the Rohingya minority.
6. **Sport** — Carlos Alcaraz wins his first ATP Finals crown; Max
   Verstappen takes the Las Vegas Grand Prix.

Also in the ticker: thousands march in Lisbon over living costs; the
India–Nepal Saryu–Kamala Express rail link opens; Waymo pulls its driverless
taxis from US freeways; Denmark's top court backs the 'ghetto law'.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3, standard library only) places the bundled
`entry.png` at `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`),
checking the PNG magic bytes and the 1 MiB size cap first. The image was
drawn with a small Python/PIL script kept in this repository as
`render.py`; the entry itself is the program plus the image.
