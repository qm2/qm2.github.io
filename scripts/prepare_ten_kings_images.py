"""Reproduce only the explicitly selected images from a private handoff directory.

Usage: python3 scripts/prepare_ten_kings_images.py /path/to/extracted/package
The package and original photographs stay outside the repository. No network IO.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'museum-notes/ten-kings'


def prepare(package, supplement_directory=None):
    rows = list(csv.DictReader((package/'data/photo_manifest.csv').open(encoding='utf-8-sig')))
    assert len(rows) == 458
    for row in rows:
        source = (package/row['package_file']).resolve()
        assert source.is_relative_to(package.resolve())
        assert hashlib.sha256(source.read_bytes()).hexdigest() == row['sha256'], source
    records = json.loads((BASE/'data/photos.json').read_text())
    for key, record in records.items():
        selected = record.get('selected_asset')
        if record.get('source_group') == 'supplement':
            if supplement_directory is None:
                assert all((BASE/v['path']).exists() for v in record['variants']), 'Supplement photographs require --supplement-directory'
                continue
            source = supplement_directory/record['source_filename']
            assert hashlib.sha256(source.read_bytes()).hexdigest() == record['source_sha256']
        else:
            source = package/(selected or f'assets/original_photos/{record["source_index"]:03}.jpg')
        im = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
        if record.get('rotation'): im = im.rotate(record['rotation'], expand=True)
        assert im.size == (record['width'],record['height']), key
        for v in record['variants']:
            target = BASE/v['path']
            target.parent.mkdir(parents=True,exist_ok=True)
            if (v['width'],v['height']) == im.size and selected and not record.get('rotation') and key!='hero':
                target.write_bytes(source.read_bytes())
            else:
                quality = 90 if record.get('source_group') == 'supplement' else (87 if key=='hero' else 88)
                im.resize((v['width'],v['height']),Image.Resampling.LANCZOS).save(target,'WEBP',quality=quality,method=6)
    print(f'Verified 458 original hashes; prepared selected derivatives ({len(records)-1} source photographs plus hero crop).')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package',type=Path)
    parser.add_argument('--supplement-directory',type=Path)
    args = parser.parse_args()
    prepare(args.package, args.supplement_directory)
