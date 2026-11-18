#!/usr/bin/env python3
"""Verify the published task snapshot without installing task dependencies."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    expected = manifest['files']
    actual = {
        p.relative_to(ROOT).as_posix()
        for model in (ROOT / 'tasks').iterdir() if model.is_dir()
        for p in model.rglob('*') if p.is_file()
    }
    if actual != set(expected):
        raise SystemExit(f'File inventory mismatch: missing={set(expected)-actual}, extra={actual-set(expected)}')
    for name, entry in expected.items():
        path = ROOT / name
        if path.is_symlink() or sha256(path) != entry['sha256']:
            raise SystemExit(f'Content mismatch: {name}')
        if bool(path.stat().st_mode & 0o111) != (entry['mode'] == '100755'):
            raise SystemExit(f'Executable mode mismatch: {name}')
        if path.suffix == '.py':
            ast.parse(path.read_text(), filename=name)
        elif path.suffix == '.json':
            json.loads(path.read_text())
        elif path.suffix == '.toml':
            tomllib.loads(path.read_text())
        elif path.suffix == '.sh':
            subprocess.run(['bash', '-n', str(path)], check=True)
    tasks = list((ROOT / 'tasks').glob('*/task.toml'))
    if len(tasks) != 12:
        raise SystemExit(f'Expected 12 tasks, found {len(tasks)}')
    print(f'PASS: {len(tasks)} task packages; {len(expected)} files match the source snapshot.')
    print('Checked hashes, executable modes, and Python/JSON/TOML/shell syntax. No GPU evaluation performed.')


if __name__ == '__main__':
    main()
