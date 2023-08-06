from __future__ import print_function

import argparse
import functools
import pathlib
import os
import shutil
import subprocess
import sys

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--outdir", default="build")
PARSER.add_argument("--input", default="talk.ipynb")

TALK_HEADER = r"""
\documentclass[ignorenonframetext]{beamer}
"""

HANDOUT_HEADER = r"""
\documentclass{article}
\usepackage{beamerarticle}
"""

def make_talk(*, args, workdir, runner):
    build = workdir / args.outdir
    run = functools.partial(runner, check=True, cwd=build)
    build.mkdir(exist_ok=True)
    shutil.copy(args.input, build / "base_talk.ipynb")
    jupyter = pathlib.Path(sys.executable).parent / "jupyter"
    run(["jupyter", "nbconvert", "base_talk.ipynb", "--to", "markdown",
         '--TagRemovePreprocessor.remove_cell_tags={"no_markdown"}',
         '--TagRemovePreprocessor.remove_all_outputs_tags={"no_output"}',
         '--output', "base_talk.md"])
    run(["pandoc", "--listings", "-o", "base_talk.tex", "base_talk.md"])
    source_tex = (build / "base_talk.tex").read_text()
    for line in source_tex.splitlines():
        line = line.strip()
        if not line.startswith(r'\lstinputlisting'):
            continue
        fname = line.split('{')[1].split('}')[0]
        shutil.copy(workdir / fname, build / fname)
    (build / "talk.tex").write_text(
        TALK_HEADER + source_tex
    )
    (build / "handout.tex").write_text(
        HANDOUT_HEADER + source_tex
    )
    run(["pdflatex", "talk.tex"])
    run(["pdflatex", "handout.tex"])
