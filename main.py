#!/usr/bin/env python3
"""Entry program for news-image-20261124, account 2 (Orochim25).

The image is drawn by build.py (PIL flat-vector newspaper) and shipped as
entry.png beside this file. This program copies it to /output/entry.png,
deterministically: the same bytes on every run.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
