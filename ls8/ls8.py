#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    print(f"Specify a file name as command line argument.")
    sys.exit(1)
else:
    filename = sys.argv[1]

cpu = CPU()

cpu.load(filename)
cpu.run()