#!/usr/bin/env python3
"""Win-rate sanity math for vendor claims.
usage: winrate_check.py <wins> <trades> [target_over_stop] [dials]
prints the breakeven rate for the target size, the 95% interval for the observed win rate,
and how often a coin-flip system shows that record on at least one of N optimizer dials."""
import math, sys
w, n = int(sys.argv[1]), int(sys.argv[2]); tpm = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; dials = int(sys.argv[4]) if len(sys.argv) > 4 else 144
p = w / n; z = 1.96; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
print('observed %d/%d = %.1f%% | 95%% interval %.0f%%..%.0f%%' % (w, n, p * 100, (c - h) * 100, (c + h) * 100))
be = 1 / (1 + tpm); print('target %.2fx stop -> breakeven %.0f%%; expectancy at observed rate %+.2fR/trade' % (tpm, be * 100, p * tpm - (1 - p)))
p1 = sum(math.comb(n, k) * 0.5 ** n for k in range(w, n + 1)); print('coin flip shows >= %d/%d on a given dial %.2f%%; on at least one of %d dials %.0f%%' % (w, n, p1 * 100, dials, (1 - (1 - p1) ** dials) * 100))
