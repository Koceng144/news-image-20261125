# The World in One Day — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Koceng144/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Koceng144/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the [news-image-20261125 bounty](https://make.fun/bounties/news-image-20261125):
**"Sum up 25 November's world news in one image."**

A night-sky broadsheet front page — a dark-navy masthead with gold
stars, a full-width cinematic hero lead (Shenzhou-24 lifts off with the
first foreign astronaut to Tiangong, big rocket over a starfield), a UTC
timeline strip, twelve illustrated flat-vector tiles in three rows of
four, a "BY THE NUMBERS" band of five hard numbers (4.9% Australia CPI,
−2.55% Nikkei, $7.4bn Boeing order, 78,000 women killed last year,
3,000 ha Flinders Island fire), a pin world map, 22 more numbered
stories, a markets ticker, and a DATE CHECK box holding over the big
stories that were *not* Wednesday's news. 35 stories total.

Date rule: every story was reported on 25 Nov 2026. Scheduled items
(US data pile 13:30 UTC, Trump–Rutte, EU–Balkans summit, Gukesh Game 2)
are labelled DUE — forecasts, never results. Two facts were refreshed
at build time (~02:00 UTC, 25 Nov): the Xiamen/Boeing agreement was
signed and filed 24 Nov and is worded as a 25 Nov report; the Cartagena
"all hostages out" claim is contested (El Tiempo vs Sky News), so it was
demoted from illustrated slot 13 to the tail with neutral wording and
the FBI crime-database breach promoted in its place. Brent was dropped
entirely (two conflicting prices). No war-death tallies anywhere.
See `facts-2026-11-25.md` for per-story verification and exclusions.

`main.py` (stdlib only) copies the pre-composed `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). `build.py`
composes the image offline with PIL; run `python3 -P -s build.py` to
regenerate it — two runs produce byte-identical output (verified).
