#!/usr/bin/env python3
# Necati Selcuk, 5001240039, G2 - data cache simulator for trace.csv (step 4e)
# LRU replacement, write-allocate; write-through: every store is a memory write.
# Usage: python cache_sim.py [trace.csv]

import sys, csv


def simulate(trace, size, line, ways):
    """Return (hits, misses, memory_writes) for one cache configuration."""
    lines = size // line
    ways = min(ways, lines)               # cannot have more ways than lines
    nsets = lines // ways
    sets = [[] for _ in range(nsets)]     # each set: list of tags, LRU first
    hits = misses = writes = 0
    for rw, addr in trace:
        block = addr // line
        s, tag = block % nsets, block // nsets
        lru = sets[s]
        if tag in lru:
            hits += 1
            lru.remove(tag)
        else:
            misses += 1
            if len(lru) == ways:
                lru.pop(0)                # evict least recently used block
        lru.append(tag)
        if rw == 'W':
            writes += 1                   # write-through
    return hits, misses, writes


def load(path):
    with open(path, newline='') as f:
        return [(r['RW'], int(r['adres_hex'], 16)) for r in csv.DictReader(f)]


def show(name, trace, size, line, ways):
    h, m, w = simulate(trace, size, line, ways)
    print('%-30s hit %5d  miss %4d  H %.4f  writes %d' % (name, h, m, h / (h + m), w))


def main():
    trace = load(sys.argv[1] if len(sys.argv) > 1 else 'trace.csv')
    size = 128
    print('Personal cache: 128 B, 16 B line, 4-way, LRU')
    show('4-way, 16 B line', trace, size, 16, 4)
    print('\nSeries 1: mapping (line = 16 B)')
    for name, ways in (('Direct', 1), ('2-way', 2), ('4-way', 4), ('Fully associative', 8)):
        show(name, trace, size, 16, ways)
    print('\nSeries 2: line size (4-way; 64 B line has only 2 lines -> 2-way)')
    for line in (8, 16, 32, 64):
        show('%d B line' % line, trace, size, line, 4)


if __name__ == '__main__':
    main()
