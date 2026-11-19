#!/usr/bin/env python3
"""Split a TwinMind transcript into readable chunks.

Usage: chunk.py TRANSCRIPT.txt OUTDIR [--minutes 25] [--overlap 2] [--max-bytes 14000] [--after HH:MM]

--after HH:MM keeps only turns at or after that local clock time, so a later
run can pick up where an earlier one stopped (the watermark).

Reads the `text` of a TwinMind fetch (lines like
"[2026-11-13T09:40:02-05:00] Speaker 1: words"), compacts it, and writes
OUTDIR/chunk-NN.txt. Compacting: timestamps cut to HH:MM, consecutive turns
by the same speaker merged,
(a chunk also closes early at MAX-BYTES, so each one fits in a single read) pure backchannel turns ("Mm-hmm.", "Yeah.")
dropped. Chunks break at a speaker change once the time window is full;
each chunk repeats the last OVERLAP minutes of the one before it, so
nothing said across a cut is lost. Prints one line per chunk.
"""
import re, sys, os
from datetime import datetime, timedelta

LINE = re.compile(r'^\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[^\]]*)\]\s*(Speaker \d+|[^:]{1,40}):\s*(.*)$')
BACK = re.compile(r"^(mm+-?hmm+|m+-?hm+|yeah|yep|yes|no|okay|ok|right|uh-huh|sure|wow|oh|huh|um+|uh+|exactly|totally|true|cool|nice|great|for sure)[.,!?]*$", re.I)

def parse(path):
    turns = []
    for raw in open(path, encoding='utf-8'):
        m = LINE.match(raw.strip())
        if not m:
            if turns and raw.strip():
                turns[-1][2] += ' ' + raw.strip()
            continue
        ts = datetime.fromisoformat(m.group(1))
        turns.append([ts, m.group(2), m.group(3).strip()])
    return turns

def compact(turns):
    out = []
    for ts, sp, tx in turns:
        if BACK.match(tx.strip()):
            continue
        if out and out[-1][1] == sp:
            out[-1][2] += ' ' + tx
        else:
            out.append([ts, sp, tx])
    return out

def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    src, outdir = a[0], a[1]
    minutes = int(a[a.index('--minutes') + 1]) if '--minutes' in a else 25
    overlap = int(a[a.index('--overlap') + 1]) if '--overlap' in a else 2
    maxb = int(a[a.index('--max-bytes') + 1]) if '--max-bytes' in a else 14000
    turns = parse(src)
    if '--after' in a:
        hh, mm = map(int, a[a.index('--after') + 1].split(':'))
        turns = [t for t in turns if (t[0].hour, t[0].minute) >= (hh, mm)]
    turns = compact(turns)
    if not turns:
        sys.exit('no timestamped turns found')
    os.makedirs(outdir, exist_ok=True)
    chunks, start = [], 0
    while start < len(turns):
        t0 = turns[start][0]
        end, size = start, 0
        while end < len(turns) and turns[end][0] - t0 < timedelta(minutes=minutes):
            size += len(turns[end][2]) + 20
            if size > maxb and end > start:
                break
            end += 1
        end = max(end, start + 1)
        chunks.append((start, end))
        if end >= len(turns):
            break
        nxt = end
        while nxt > start + 1 and turns[end][0] - turns[nxt - 1][0] < timedelta(minutes=overlap):
            nxt -= 1
        start = nxt
    for i, (s, e) in enumerate(chunks, 1):
        p = os.path.join(outdir, f'chunk-{i:02d}.txt')
        with open(p, 'w', encoding='utf-8') as f:
            for ts, sp, tx in turns[s:e]:
                f.write(f'{ts:%H:%M} {sp}: {tx}\n')
        print(f'{p}\t{turns[s][0]:%H:%M}-{turns[e-1][0]:%H:%M}\t{os.path.getsize(p)} bytes')

if __name__ == '__main__':
    main()
