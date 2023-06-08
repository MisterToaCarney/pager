import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nogui", action="store_true", help="Run without QT user interface")
parser.add_argument("--service-account", default="/tmp/test.json")
args = parser.parse_args()
