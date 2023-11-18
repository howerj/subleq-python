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
import signal

# See:
# <https://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c>
#
# I should probably change this to a "try...catch" around my code...
#
# I like programming in Python, I really do, but by god you can tell 
# when a program is made in Python (trace garbage when hitting CTRL+C 
# or worse catching and ignoring it, trouble getting the program 
# running at all because of the horrendous packaging situation or 
# because of the wrong version of the interpreter, performance problems,
# exceptions being thrown for things that could be caught at compile time
# in a language with strict static typing) much in the same way you can 
# tell when a program is made in Java (splash screens, slow loading times 
# ("the JIT is fast once its up and running", yeah right), huge memory 
# usage, performance problems, null pointer exceptions). 
#
# A rule of thumb I have is, if you can tell what language a program is 
# programmed in then you are going to have a suboptimal experience.
#
# Python is good for the programmer but I find it terrible for
# the user.
#
# This rant partially explains the next line, it overrides the
# default signal handler for CTRL+C, which exits after printing
# a stack trace (which I find it never useful, and just ugly).
#
# Should we exit with '0' or with '1' though? I think '1' is
# the best option (obviously, that's why I chose it) as we are
# not exiting "normally".
#
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))

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
