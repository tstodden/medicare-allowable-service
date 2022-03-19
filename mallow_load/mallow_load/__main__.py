from tempfile import SpooledTemporaryFile

from google.cloud import storage

from mallow_load.mallow_load.constant import MALLOW_BUCKET, BucketPrefix
from mallow_load.mallow_load.repository.mac_locality import MacLocalityRepository


def main():
    client = storage.Client()
    bucket = client.get_bucket(MALLOW_BUCKET)
    print(bucket)
    print(list(bucket.list_blobs(prefix=BucketPrefix.GPCI_DATA.value)))
    blob = bucket.get_blob(f"{BucketPrefix.GPCI_DATA.value}/gpci-2021.csv")
    with SpooledTemporaryFile(mode="w") as tmp_file:
        tmp_file.write(blob.download_as_text())
        tmp_file.seek(0)
        repo = MacLocalityRepository()
        repo.add_csv_file(tmp_file)
        print(repo.repository)


if __name__ == "__main__":
    main()
