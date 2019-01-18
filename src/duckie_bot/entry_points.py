#external
import argparse
import glob
import importlib.util
import sys

from functools import reduce
from inspect import isclass
from pathlib import Path

#inhouse
from duckie_bot.cameras import RPiCamera, WebCamera
from duckie_bot.cars import RPiCar, DebugCar
from duckie_bot.servers import duckie_server
from duckie_bot.mode import Mode

def import_module(file):
    file = file.resolve()
    if len(file.name) > 0 and file.name[0] in ["_", "."]: #private
        return None
    spec = importlib.util.spec_from_file_location(".", str(file))
    if spec is None: #likely a package import
        #need to add path to package to sys.path
        sys.path.append(str(file/".."))
        return __import__(file.name)
    m = importlib.util.module_from_spec(spec)
################################################################################
#IF YOU'RE READING THIS, THIS IS YOUR FAULT NOT MINE                           #
################################################################################
    spec.loader.exec_module(m)
    return m
def get_modes(filename):
    m = import_module(filename)
    if m is None: #failed to import or private
        return []
    attributes = [getattr(m, attr_name) for attr_name in dir(m)]
    return [
        a
        for a in attributes
        if isclass(a) and issubclass(a, Mode) and a is not Mode
    ]

def get_files():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        type=str,
        nargs="+",
        help='''mode files to be run; regular expressions and packages can be
                used; ex: *.py''')
    return parser.parse_args().files

def parse_arguments():
    #grabs all file names (no repeats)
    files = reduce(lambda s,l: s|l, [set(glob.glob(f)) for f in get_files()], set())
    return reduce(lambda acc,l: acc+l, [get_modes(Path(fn)) for fn in files], [])

def debug_modes():
    modes = parse_arguments()
    classes = []
    debug_car = DebugCar()
    web_camera = WebCamera()
    duckie_server.run(
        host="0.0.0.0",
        port=9694,
        car=debug_car,
        camera=web_camera,
        mode_modules=modes
    )

def run_modes():
    modes = parse_arguments()
    classes = []
    car = RPiCar()
    cam = RPiCamera()
    duckie_server.run(
        host="0.0.0.0",
        port=9694,
        car=car,
        camera=cam,
        mode_modules=modes
    )

