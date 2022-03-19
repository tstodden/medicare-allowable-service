from google.cloud import storage

from mallow_load.mallow_load.constant import MALLOW_BUCKET, BucketPrefix


def main():
    client = storage.Client()
    bucket = client.get_bucket(MALLOW_BUCKET)
    print(bucket)
    print(list(bucket.list_blobs(prefix=BucketPrefix.ZIP_DATA.value)))


if __name__ == "__main__":
    main()
