import os
import boto3
import awswrangler as wr
from pandas import DataFrame
from defi_common_lib.storage.storage_service import StorageService
from typing import Any, List, Tuple

import logging
logger = logging.getLogger(__name__)


class S3Service(StorageService):
    """Service to handle S3 operations"""

    def __init__(self, session: boto3.Session) -> None:
        self.s3_session = session

    def save_file(self, file_content: Any, config) -> None:
        """
            Overrides abstract method. It saves a file in S3
            :param file_content: content of the file
            :param file_name: name of the file
            :param config: dictionary with additional configuration; 'bucket_name' and 'key'
            :return: None

        """
        key = config['key']
        bucket_name = config['bucket_name']

        s3 = self.s3_session.resource("s3")
        s3.Object(bucket_name, key).put(Body=file_content)
        
        url = "s3://{0}/{1}".format(
            bucket_name,
            key
        )

        logger.debug(
            f'Dataset saved in S3 repository at {url}'
        )

        return url

    def download_file(self, path: str, file_name: str, config) -> None:
        """
            Overrides abstract method. It downloads a file from S3
            :param path: local path to download the file
            :param file_name: name of the file  will be saved in local path
            :param config: dictionary with additional configuration; 'bucket_name' and 'key'. 'key' represents the whole path in s3
            :return: None

        """

        key = config['key']
        bucket_name = config['bucket_name']

        local_file = os.path.join(path, file_name)
        s3_client = self.s3_session.client('s3')

        s3_client.download_file(bucket_name, key, local_file)

    def getContent_file(self, **config):
        """
            Overrides abstract method. Get the content of a file from S3
            :param config: dictionary with additional configuration; 'bucket_name' and 'key'. 'key' represents the whole path in s3
            :return: Content of the object stored in S3

        """
        key = config['key']
        bucket_name = config['bucket_name']

        return self.s3_session.Object(bucket_name, key).get()

    def list_protocol_files(self, bucket: str, agent: str, year: str, month: str, protocols_to_filter: List[str]) -> List[Tuple[str, str, str, str]]:
        """
            Finds the files stored in S3 for that match the criteria of agent, year, month and protocol indicated by the parameters

            :param bucket: Name of the s3 bucket
            :param agent: Name of the agent (Loader agent)
            :param year: Year
            :param month: Month (represented as a number)
            :param protocols_to_filter: List of the name of the protocols to find ("ALL" to find all )
            :return: List of files found. The list contains tuples with the format [protocol, network, file_name, path]
        """
        objects = wr.s3.list_objects(
            f's3://{bucket}/{agent}/*/{year}{month}*/*/*.csv', boto3_session=self.s3_session
        )

        # returns protocol, network, file_name, path
        files = list(map(lambda obj: (f'{obj.split("/")[7].split("-")[0]}-{obj.split("/")[7].split("-")[1]}', obj.split(
            "/")[7].split("-")[3].split("_")[0], obj.split("/")[7], obj), objects)
        )

        if 'ALL' not in protocols_to_filter:
            files = list(
                filter(lambda file: file[0] in protocols_to_filter, files)
            )

        return files

    def get_protocol_file_at(self, bucket: str, agent: str, date: str, protocol: str) -> str:
        """
            Finds the file stored in S3 for that match the at the specified date for the protocol

            :param bucket: Name of the s3 bucket
            :param agent: Name of the agent (Loader agent)
            :param date: Date of the file in format yyyymmdd
            :param protocol: protocol name with version EX: Aave-v2
            :return: file path
        """
        objects = wr.s3.list_objects(
            f's3://{bucket}/{agent}/*/{date}/*/{protocol}*.csv',
            boto3_session=self.s3_session
        )

        return_value = objects[0] if len(objects) > 0 else None
        return return_value

    def download_file_at(self, bucket: str, agent: str, date: str, protocol: str, path: str) -> str:
        """
            Finds and donwload the file from s3 repository with the filters given in the parameters

            :param bucket: Name of the s3 bucket
            :param agent: Name of the agent (Loader agent)
            :param date: Date of the file in format yyyymmdd
            :param protocol: protocol name with version EX: Aave-v2
            :param path: path where download the file
            :return: file name of downloaded file
        """
        file_object = self.get_protocol_file_at(
            bucket=bucket,
            agent=agent,
            date=date,
            protocol=protocol
        )

        file_key = "/".join(file_object.split('/')[3:])
        file_name = file_object.split('/')[-1]

        self.download_file(
            path=path,
            file_name=file_name,
            config={
                'key': file_key,
                'bucket_name': bucket
            }
        )

        return file_name

    def delete_local_file(self, file_name: str, path: str) -> None:
        """
            Deletes local file

            :param file_name: file name to delete
            :param path: path of the file
        """
        file = os.path.join(path, file_name)
        os.remove(file)

    # paths: array of full s3 paths
    # it assumes the size of the files are quite small, as the current ones
    # in case we need to read some fair big files, the read_csv offers a chunk parameter

    def get_dataframe_from_files(self, paths: List[str]) -> DataFrame:
        """
            Returns a single DataFrame with the contents of the files of the paths
            it assumes the size of the files are quite small

            :param paths: List with the s3 paths to the files we want to merge in a single DataFrame
            :return: DataFrame with the content of the files
        """
        return wr.s3.read_csv(path=paths, boto3_session=self.s3_session, encoding = 'ISO-8859-1')

    def save_dataframe(self, df: DataFrame, path: str) -> None:
        """
            Saves in S3  the content of a DataFrame as csv

            :param df: DataFrame
            :path path: full s3 path to store the file
        """
        wr.s3.to_csv(
            df=df,
            path=path,
            boto3_session=self.s3_session,
            encoding = 'ISO-8859-1'
        )


class S3ServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, s3_access_key: str, s3_secret_key: str, **_ignored) -> S3Service:
        if not self._instance:
            session = self.getSession(s3_access_key, s3_secret_key)
            self._instance = S3Service(session)

        return self._instance

    def getSession(self, access_key: str, secret_key: str) -> boto3.Session:
        return boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
