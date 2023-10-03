#!/usr/bin/env python
# Author: Richard James Howe
# License: The Unlicense
# Project: N-bit SUBLEQ OISC
# Repo: <https:github.com/howerj/subleq-python>
# Email: <mailto:howe.r.j.89@gmail.com>
#
# See <https://github.com/howerj/subleq> for more information
# and images.

import sys


def die(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


if len(sys.argv) < 2:
    die("Usage: " + sys.argv[0] + " bits image.dec...")

bits = int(sys.argv[1])

if bits < 8 or bits > 32:
    die("Invalid bit range (8-32)")

mask = (1 << bits) - 1
high = 1 << (bits - 1)
mlen = 65536
m = [0] * mlen

i = 0
for image in sys.argv[2:]:
    with open(image) as f:
        for line in f.readlines():
            for v in line.split():
                m[i] = int(v)
                if m[i] < 0:
                    m[i] = mask + m[i] + 1
                i = i + 1

pc = 0
while pc < mlen and pc != mask:
    a = m[pc + 0]
    b = m[pc + 1]
    c = m[pc + 2]
    pc = pc + 3
    if a == mask:
        try:
            m[b] = ord(sys.stdin.read(1))
        except TypeError:
            m[b] = mask
    elif b == mask:
        print(chr(m[a]), end="")
        sys.stdout.flush()
    else:
        r = m[b] - m[a]
        r = r & mask
        m[b] = r
        if r == 0 or r & high:
            pc = c
