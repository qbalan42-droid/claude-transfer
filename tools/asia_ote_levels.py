#!/usr/bin/env python3
"""Asia OTE levels from the prior New York cash session (Yahoo chart API, no key).
usage: asia_ote_levels.py [SYMBOL=NQ=F] [YYYY-MM-DD=today ET]
prints the 0.705 limit, the 0.79 stop, equilibrium and the draw for both directions."""
import json, sys, urllib.request, datetime, zoneinfo
sym = sys.argv[1] if len(sys.argv) > 1 else 'NQ=F'; et = zoneinfo.ZoneInfo('America/New_York')
day = datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else datetime.datetime.now(et).date()
u = 'https://query1.finance.yahoo.com/v8/finance/chart/' + sym.replace('=', '%3D') + '?range=5d&interval=1m'
d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))
r = d['chart']['result'][0]; q = r['indicators']['quote'][0]; hi = lo = None; last = None
for t, h, l, c in zip(r['timestamp'], q['high'], q['low'], q['close']):
    if None in (h, l, c): continue
    dt = datetime.datetime.fromtimestamp(t, et); last = c
    if dt.date() == day and datetime.time(9, 30) <= dt.time() < datetime.time(16, 0): hi = h if hi is None else max(hi, h); lo = l if lo is None else min(lo, l)
if hi is None: sys.exit('no cash-session bars for %s' % day)
R = hi - lo; print('%s cash range %s: %.2f - %.2f (%.0f pts), last %.2f' % (sym, day, lo, hi, R, last))
for bias, name in ((-1, 'SELL (1H down)'), (1, 'BUY (1H up)')):
    ote = hi - 0.705 * R if bias == 1 else lo + 0.705 * R; f79 = hi - 0.79 * R if bias == 1 else lo + 0.79 * R
    stp = f79 - 2 if bias == 1 else f79 + 2; eq = hi - 0.5 * R; draw = hi if bias == 1 else lo
    print('%-14s limit %.2f | stop %.2f (%.0f pts) | bank %.2f | runner %.2f | %.1fR | %.0f pts %s price' % (name, ote, stp, abs(ote - stp), eq, draw, abs(draw - ote) / abs(ote - stp), abs(ote - last), 'above' if ote > last else 'below'))
