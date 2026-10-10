#!/usr/bin/env python3
from cogc.cli import main

raise SystemExit(main(["validate", *__import__("sys").argv[1:]]))
