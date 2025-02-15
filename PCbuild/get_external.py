#!/usr/bin/env python3

import argparse
import os
import pathlib
import zipfile
from urllib.request import urlretrieve


def fetch_zip(commit_hash, zip_dir, *, org='Nuitka', binary=False, verbose):
    repo = f'Nuitka-Python-{"bin" if binary else "source"}-deps'
    url = f'https://github.com/{org}/{repo}/archive/{commit_hash}.zip'
#    print(f"Fetching: {url}")
    reporthook = None
    if verbose:
        reporthook = print
    zip_dir.mkdir(parents=True, exist_ok=True)
    filename, headers = urlretrieve(
        url,
        zip_dir / f'{commit_hash}.zip',
        reporthook=reporthook,
    )
    return filename


def extract_zip(externals_dir, zip_path):
    with zipfile.ZipFile(os.fspath(zip_path)) as zf:
        zf.extractall(os.fspath(externals_dir))
        return externals_dir / zf.namelist()[0].split('/')[0]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-b', '--binary', action='store_true',
                   help='Is the dependency in the binary repo?')
    p.add_argument('-O', '--organization',
                   help='Organization owning the deps repos', default='python')
    p.add_argument('-e', '--externals-dir', type=pathlib.Path,
                   help='Directory in which to store dependencies',
                   default=pathlib.Path(__file__).parent.parent / 'externals')
    p.add_argument('tag',
                   help='tag of the dependency')
    return p.parse_args()


def main():
    args = parse_args()
    zip_path = fetch_zip(
        args.tag,
        args.externals_dir / 'zips',
        org=args.organization,
        binary=args.binary,
        verbose=args.verbose,
    )
    final_name = args.externals_dir / args.tag
    extract_zip(args.externals_dir, zip_path).replace(final_name)


if __name__ == '__main__':
    main()
