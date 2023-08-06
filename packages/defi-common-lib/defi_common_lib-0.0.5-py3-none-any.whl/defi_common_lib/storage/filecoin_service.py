import os
from metadata_driver_filecoin.data_plugin import Plugin
from common_utils_py.utils.crypto import decryption, get_keys_from_file
from common_utils_py.http_requests.requests_session import get_requests_session
from nevermined_sdk_py.gateway.gateway import Gateway
from defi_common_lib.storage.storage_service import StorageService
from typing import Any

import logging
logger = logging.getLogger(__name__) 


class FilecoinService(StorageService):

    def __init__(self, gateway_url:str, crypto_key_file:str='', crypto_password:str= '') -> None:
        self.plugin = Plugin()
        self.crypto_key_file = crypto_key_file
        self.crypto_password = crypto_password
        self.gateway_url = gateway_url

    # overriding abstract method
    def save_file(self, file_content: Any, file_name:str= '', **config)-> str:

        Gateway.set_http_client(get_requests_session())
        files = {'file': (file_name, file_content)}

        response = Gateway._http_client.post(
            f'{self.gateway_url}/api/v1/gateway/services/upload/filecoin',
            files=files,
        )

        url = response.json()['url']
        logger.debug(
            f'Dataset saved in filecoin repository at {url}'
        )
        return url


    # overriding abstract method
    # config -> fileKey
    def download_file(self, path, file_name, **config) -> None:

        fileKey = config['fileKey']
        cid = self.__getCID(fileKey)
        logger.debug(f'CID to download: {cid}')

        self.plugin.download(cid.decode(), local_file=os.path.join(path, file_name))


    # overriding abstract method
    # config -> fileKey, crytoKeyFile, crytoPassword
    def getContent_file(self, **config)-> Any:
       
        fileKey = config['fileKey']
        cid = self.__getCID(fileKey)
        print(f'CID to download: {cid}')

        return self.plugin.download_bytes(cid.decode()) 

    def __getCID(self, fileKey:str)-> Any:
    
        (_, private_key_hex) = get_keys_from_file(
            self.crypto_key_file, self.crypto_password
        )

        return decryption(private_key_hex, bytes.fromhex(fileKey))
        

class FilecoinServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self,  gateway_url:str, crypto_key_file:str='', crypto_password:str='', **_ignored)-> FilecoinService:
        if not self._instance:
            self._instance = FilecoinService(gateway_url, crypto_key_file, crypto_password)
        return self._instance
