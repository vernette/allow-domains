#!/usr/bin/python3.10

from pathlib import Path

import tldextract

RAW_DOMAIN_LIST_FILE_PATH = 'src/Russia-domains-inside.lst'
OUTPUT_FOLDER = 'Russia/inside'


def raw(src, out):
    domains_raw = set()
    with open(src) as infile:
        for line in infile:
            if tldextract.extract(line).suffix:
                domains_raw.add(line.rstrip())
    domains_raw = sorted(domains_raw)

    with open(f'{out}-raw.lst', 'w') as file:
        for name in domains_raw:
            file.write(f'{name}\n')


if __name__ == '__main__':
    Path('Russia').mkdir(parents=True, exist_ok=True)
    raw(RAW_DOMAIN_LIST_FILE_PATH, OUTPUT_FOLDER)
