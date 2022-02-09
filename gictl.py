#! /usr/bin/env python3
"""
game-industry cli control app.
"""

import os
import sys

# Make the project root an import path directory:
sys.path.append(os.getcwd())

from lib import scraping


def main(argv) -> int:
    print(f'gictl called with {argv!r} ;)')
    if argv[0] == 'two':
        from lib import two_records
        two_records.execute()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
