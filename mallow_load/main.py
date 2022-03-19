import argparse
import subprocess

# configure CLI
parser = argparse.ArgumentParser(
    description="Load data for the Medicare allowable service."
)
parser.add_argument("-i", "--index", required=True, help="index to load data into")
parser.add_argument("-y", "--year", required=True, help="year of data to load")

args = parser.parse_args()
subprocess.run(
    ["python", "-m", "mallow_load.mallow_load", "-i", args.index, "-y", args.year]
)
