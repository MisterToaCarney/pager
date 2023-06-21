import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nogui", action="store_true", help="Run without QT user interface")
parser.add_argument("--service-account", default="/tmp/test.json")
parser.add_argument("--iio-context", default="ip:pluto.local")
args = parser.parse_args()
