#!/usr/bin/env python3
# vim: expandtab:ts=4:sw=4:noai

import getopt
import sys

opts = args = None
try:
    opts, args = getopt.getopt(sys.argv[1:],'a:a',['bc','de'])
except getopt.GetoptError as exc:
    print(exc.msg)
print(opts)
print(args)

    

