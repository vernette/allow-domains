#!/usr/bin/python3.10

import re
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


def dnsmasq(src, out):
    domains = set()
    domains_single = set()
    with open(src) as infile:
        for line in infile:
            if tldextract.extract(line).suffix:
                if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                    domains.add(
                        tldextract.extract(line.rstrip()).registered_domain
                    )
                    if (
                        not tldextract.extract(line).domain
                        and tldextract.extract(line).suffix
                    ):
                        domains.add(
                            '.' + tldextract.extract(line.rstrip()).suffix
                        )
    domains = domains.union(domains_single)
    domains = sorted(domains)
    with open(f'{out}-dnsmasq-nfset.lst', 'w') as file:
        for name in domains:
            file.write(f'nftset=/{name}/4#inet#fw4#vpn_domains\n')
    with open(f'{out}-dnsmasq-ipset.lst', 'w') as file:
        for name in domains:
            file.write(f'ipset=/{name}/vpn_domains\n')


if __name__ == '__main__':
    Path('Russia').mkdir(parents=True, exist_ok=True)
    raw(RAW_DOMAIN_LIST_FILE_PATH, OUTPUT_FOLDER)
    dnsmasq(RAW_DOMAIN_LIST_FILE_PATH, OUTPUT_FOLDER)
