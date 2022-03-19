import argparse

from mallow_load.mallow_load.app import ApplicationService


# configure CLI
parser = argparse.ArgumentParser(
    description="Load data for the Medicare allowable service."
)
parser.add_argument("-i", "--index", required=True, help="index to load data into")
parser.add_argument(
    "-y", "--year", required=True, type=int, help="year of data to load"
)


def main():
    args = parser.parse_args()
    app = ApplicationService()
    app.load_index_for_year(args.index, args.year)


if __name__ == "__main__":
    main()
