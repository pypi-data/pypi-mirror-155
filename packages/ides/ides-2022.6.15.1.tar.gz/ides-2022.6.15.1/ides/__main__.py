import pathlib
import subprocess
import sys
from . import api

args = api.PARSER.parse_args(sys.argv[1:])
api.make_talk(
    args=args,
    workdir=pathlib.Path("."),
    runner=subprocess.run,
)