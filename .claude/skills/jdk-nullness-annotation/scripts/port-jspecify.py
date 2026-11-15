#!/usr/bin/env python3
"""Copies JSpecify jdk's @Nullable annotations into the matching lines of eisop/jdk.

usage: port-jspecify.py <jspecify classes dir> <eisop classes dir> <package dir>...

A JSpecify line with @Nullable is matched to the eisop line whose text is the same once nullness
annotations are removed from both.  JSpecify's @Nullable has the same simple name as the Checker
Framework's, so the line is copied as is and the Checker Framework import is added.  Lines that match
zero or several eisop lines are reported, not guessed.
"""
import re, sys, pathlib
ANNOS = re.compile(r'@(?:Nullable|NonNull|NullMarked|NullUnmarked|PolyNull)\b\s*')
IMP = 'import org.checkerframework.checker.nullness.qual.Nullable;'
def key(line): return re.sub(r'\s+', ' ', ANNOS.sub('', line)).strip()
src_root, dst_root, pkgs = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3:]
copied = skipped = 0
for pkg in pkgs:
    for s in sorted((src_root / pkg).glob('*.java')):
        d = dst_root / pkg / s.name
        if not d.exists(): print('no eisop file', d); continue
        sl, dl = s.read_text().split('\n'), d.read_text().split('\n')
        dkeys = {}
        for i, l in enumerate(dl): dkeys.setdefault(key(l), []).append(i)
        changed = False
        for l in sl:
            if '@Nullable' not in l or l.lstrip().startswith(('import', '*', '//', '/*')): continue
            hits = dkeys.get(key(l), [])
            if len(hits) != 1:
                print(f'{pkg}/{s.name}: {len(hits)} matches for: {l.strip()}'); skipped += 1; continue
            i = hits[0]
            if dl[i] == l or '@Nullable' in dl[i] and key(dl[i]) == key(l) and dl[i].count('@Nullable') >= l.count('@Nullable'):
                continue
            dl[i] = l; changed = True; copied += 1
        if changed:
            if IMP not in dl:
                imps = [i for i, x in enumerate(dl) if x.startswith('import ')]
                at = imps[0] if imps else next(i for i, x in enumerate(dl) if x.startswith('package ')) + 2
                dl.insert(at, IMP)
            d.write_text('\n'.join(dl))
print(f'copied {copied} lines, skipped {skipped}')
