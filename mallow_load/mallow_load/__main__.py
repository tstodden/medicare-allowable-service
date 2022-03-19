from mallow_load.mallow_load.app import ApplicationService


def main():
    app = ApplicationService()
    app.load_index_for_year("gpci_by_year", 2021)


if __name__ == "__main__":
    main()
