import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import boto3
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
)


class StorageBucket:
    """
    Class to interact with an AWS storage bucket, find the latest file, and
    upload this back to the bucket itself. This class assumes you have a .env
    file in your project with your AWS access credentials in them.

    Parameters
    ----------
    bucket_name: str
        The name of the S3 bucket

    """

    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            service_name="s3",
            region_name=os.getenv("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def list_objects(self) -> list:
        """Method to list of all the objects available in the storage bucket.

        Returns
        -------
        objects : list
            A list of all the objects in the S3 storage bucket
        """
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        objects = []
        for object in response["Contents"]:
            objects.append(object["Key"])

        return objects

    def get_latest_file(self) -> Optional[str]:
        """Method to get the latest file from the S3 bucket, assuming the
        files have a YYMMDD prefix.

        Returns
        -------
        latest_file : str
            The string of the latest file in the S3 bucket
        """
        latest_date = datetime(1970, 1, 1)  # intialize a date object
        latest_file = None

        for object in self.list_objects():
            file_date_str = object.split("_")[0]
            try:
                file_date = datetime.strptime(file_date_str, "%y%m%d")
                if file_date > latest_date:
                    latest_date = file_date
                    latest_file = object
            except ValueError:
                pass

        return latest_file

    def download_latest_data(self, filepath: Path) -> None:
        """Method to download the latest file from an S3 bucket to your local
        machine given a filepath.

        Parameters
        ----------
        filepath : Path
            The filepath where you'd like to store the object
        """
        latest_file = self.get_latest_file()
        logger.info("Downloading latest data")
        self.s3.download_file(self.bucket_name, latest_file, filepath)
        logger.info(f"Downloaded {latest_file} from {self.bucket_name}")

    def upload_file(self, filepath: Path, filename: str) -> None:
        logger.info("Preparing to upload file")
        self.s3.upload_file(filepath, self.bucket_name, filename)
        logger.info(f"{filepath} uploaded to {self.bucket_name} as {filename}")
