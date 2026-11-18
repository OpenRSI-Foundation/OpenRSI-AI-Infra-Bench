#!/usr/bin/env python3
"""Materialize an ASR execution copy matching its original package manifest.

The public release appended provenance to README.md and added publication
metadata. The original launcher's strict inventory predates those additions.
Restore only those publication changes in a separate directory; retain every
evaluator, source, data, and configuration hash from the original manifest.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(source, destination):
    source, destination = source.resolve(), destination.resolve()
    if destination.exists():
        raise ValueError('Destination already exists; choose a new directory.')
    if destination == source or source in destination.parents:
        raise ValueError('Destination must be outside the published task package.')
    manifest = json.loads((source / 'tools/package-manifest.json').read_text())
    required = set(manifest) | {
        'tools/package-manifest.json', 'tests/build-inventory.json',
        'tests/comparison-state.json',
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.prepare-asr-', dir=destination.parent) as scratch:
        staged = Path(scratch) / source.name
        staged.mkdir()
        for name in sorted(required):
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError(f'Unsafe manifest path: {name}')
            path = source / name
            if path.is_symlink() or source not in path.resolve().parents:
                raise ValueError(f'Unsafe source path: {name}')
            data = path.read_bytes()
            expected = manifest.get(name)
            if name == 'README.md' and digest(data) != expected:
                prefix = data.split(b'## Public task copy', 1)[0].rstrip()
                variants = [prefix + b'\n' * n for n in range(5)]
                matches = [candidate for candidate in variants if digest(candidate) == expected]
                if len(matches) != 1:
                    raise ValueError('Cannot restore the original README hash.')
                data = matches[0]
            if expected and digest(data) != expected:
                raise ValueError(f'Original package hash mismatch: {name}')
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            shutil.copymode(path, target)
        staged.rename(destination)
    print(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        prepare(args.task, args.destination)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
