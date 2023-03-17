import boto3
import pytest
from moto import mock_s3

from rugby_stats_scraper.s3 import StorageBucket


@pytest.fixture(scope="module")
def s3_client():
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture(scope="module")
def test_bucket(s3_client):
    bucket_name = "test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    yield bucket_name


def test_list_objects(s3_client, test_bucket):
    s3_client.put_object(Bucket=test_bucket, Key="file1.txt", Body=b"test")
    s3_client.put_object(Bucket=test_bucket, Key="file2.txt", Body=b"test")

    storage_bucket = StorageBucket(test_bucket)
    objects = storage_bucket.list_objects()

    assert len(objects) == 2
    assert "file1.txt" in objects
    assert "file2.txt" in objects


def test_get_latest_file(s3_client, test_bucket):
    s3_client.put_object(
        Bucket=test_bucket, Key="210101_file1.txt", Body=b"test"
    )
    s3_client.put_object(
        Bucket=test_bucket, Key="210102_file2.txt", Body=b"test"
    )
    s3_client.put_object(
        Bucket=test_bucket, Key="210103_file3.txt", Body=b"test"
    )

    storage_bucket = StorageBucket(test_bucket)
    latest_file = storage_bucket.get_latest_file()

    assert latest_file == "210103_file3.txt"


def test_download_latest_data(s3_client, test_bucket, tmp_path):
    s3_client.put_object(
        Bucket=test_bucket, Key="210101_file1.txt", Body=b"test"
    )

    storage_bucket = StorageBucket(test_bucket)
    storage_bucket.download_latest_data(tmp_path / "test_file.txt")

    assert (tmp_path / "test_file.txt").exists()


def test_upload_file(s3_client, test_bucket, tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test")

    storage_bucket = StorageBucket(test_bucket)
    storage_bucket.upload_file(file_path, "test_upload.txt")

    s3_objects = s3_client.list_objects_v2(Bucket=test_bucket)["Contents"]
    assert len(s3_objects) == 6
    assert s3_objects[5]["Key"] == "test_upload.txt"
