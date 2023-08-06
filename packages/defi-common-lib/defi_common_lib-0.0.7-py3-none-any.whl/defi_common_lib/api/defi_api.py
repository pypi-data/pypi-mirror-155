from defi_common_lib.nvm.protocol_assets_service import ProtocolAssetsPublishService
from defi_common_lib.storage.filecoin_service import FilecoinService
from defi_common_lib.storage.s3_service import S3Service 
from defi_common_lib.storage.storage_service_factory import factory
from defi_common_lib.api.protocol_files_api import ProtocolFilesApi
from defi_common_lib.api.publish_api import PublishApi
from typing import List, Set, Dict, Tuple, Optional

import logging
logger = logging.getLogger(__name__) 

class DefiApi:
    """Entry Point for the Defi API"""
    def __init__(self, s3_service: S3Service = None, 
                    filecoin_service: FilecoinService = None, 
                    publish_service: ProtocolAssetsPublishService = None):

        self._protocol_files_api =  None
        self._publishApi = None

        self._s3_service = s3_service
        self._filecoin_service = filecoin_service
        self._publish_service = publish_service

    @property
    def protocol_files_api(self):
        """
            It gets an instance of ProtocolFilesAPI, which provides the API methods to handle files with Defi Protocols Data
            :return: instance of ProtocolFilesAPI
        """
        if not self._protocol_files_api:
            self._protocol_files_api = ProtocolFilesApi(self._s3_service, self._filecoin_service, self._publish_service)
        return self._protocol_files_api

    @property
    def publish_api(self):
        """
            It gets an instance of PublishApi, which provides the API methods to publish assets in NVM
            :return: instance of ProtocolFilesAPI
        """
        if not self._publishApi:
            self._publishApi = PublishApi(self._filecoin_service, self._publish_service)
        return self._publishApi

    def init_s3_service(self, s3_access_key: str, s3_secret_key: str)-> S3Service:
        """
            Initializes an S3Service which holds a connection to AWS with the credentials provided
            It works as a fluent API, so it returns the very same instance of the object

            :param s3_access_key: AWS Access Key
            :param s3_secret_key: AWS Secret Key
            :return: self instance
        """
       
        config = {
            's3_access_key': s3_access_key,
            's3_secret_key': s3_secret_key
        }

        if not self._s3_service:
            self._s3_service = factory.create('S3', **config)

        return self

    def init_filecoin_service(self, gateway_url:str, crypto_key_file:str = None, crypto_password:str = None) -> FilecoinService:
        """
            Initializes a Filecoin service which handles a connection to Filecoin (through NVM Gateway) to upload and download files
            It works as a fluent API, so it returns the very same instance of the object

            :param gateway_url: url of a NVM Gateway to post the request to upload to filecoin
            :param crypto_key_file: Path to Key file. Optional. Not needed to upload
            :param crypto_password: Password.  Optional. Not needed to upload
            :return: self instance
        """
       
        config = {
            'gateway_url': gateway_url,
            'crypto_key_file': crypto_key_file,
            'crypto_password': crypto_password     
        }

        self._filecoin_service = factory.create('FILECOIN', **config)

        return self

    def init_nvm_publisher(self, 
                    nvm_config_file: str, 
                    gateway_address: str, 
                    provider_address: str, 
                    provider_password: str, 
                    provider_keyfile: str, 
                    crypto_key_file: str, 
                    crypto_password: str,
                    token_address: str) -> ProtocolAssetsPublishService:

        """
            Initializes a service used to publish assets in NVMs
            It works as a fluent API, so it returns the very same instance of the object

            :param nvm_config_file: path to config file to instance NVM SDK
            :param gateway_address:  address of the gateway
            :param provider_address: address of the account used by the provider in NVM
            :param provider_password: password of the account of the provider
            :param provider_keyfile: path to the provider's account key file
            :param crypto_key_file: path to key file used to encryt/decrypt
            :param crypto_password: password of the key file used to encryt/decrypt
            :param token_address: address of the contract that holds the token used in NVM deployment

            :return: self instance
        """
    

        self._publish_service = ProtocolAssetsPublishService ( 
                nvm_config_file, 
                gateway_address, 
                provider_address, 
                provider_password, 
                provider_keyfile, 
                crypto_key_file, 
                crypto_password,
                token_address)

        return self




