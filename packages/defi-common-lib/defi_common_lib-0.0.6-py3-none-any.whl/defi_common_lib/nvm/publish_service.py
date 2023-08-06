from calendar import c
from nevermined_sdk_py import (
    Nevermined,
    Config
)
from common_utils_py.utils.crypto import encryption, get_keys_from_file
from common_utils_py.ddo.ddo import DDO
from contracts_lib_py.account import Account
from web3 import Web3
from typing import Any
import logging
logger = logging.getLogger(__name__) 



class PublishService:

    def __init__(self,
                config_file: str, 
                gateway_address: str, 
                provider_address: str, 
                provider_password: str, 
                provider_keyfile: str, 
                crypto_key_file: str, 
                crypto_password: str,
                token_address: str):
       
       
        self.__init_nevermined(config_file, gateway_address, provider_address, provider_password, provider_keyfile)
        """
        self.nevermined = Nevermined(Config(config_file))
        self.gateway_address = Web3.toChecksumAddress(gateway_address)
        self.config = self.nevermined.config
        self.account = Account(
            Web3.toChecksumAddress(provider_address),
            provider_password,
            provider_keyfile
        )
        """
        self.crypto_key_file = crypto_key_file
        self.crypto_password = crypto_password
        self.provider_address = provider_address
        self.token_address = token_address

        self.__init_public_key()


    def __init_nevermined(self, config_file: str, gateway_address:str, provider_address:str, provider_password:str, provider_keyfile:str):
        self.nevermined = Nevermined(Config(config_file))
        self.gateway_address = Web3.toChecksumAddress(gateway_address)
        self.config = self.nevermined.config
        self.account = Account(
            Web3.toChecksumAddress(provider_address),
            provider_password,
            provider_keyfile
        )

    def __init_public_key(self) -> None:

        (public_key_hex, _) = get_keys_from_file(
           self.crypto_key_file, self.crypto_password
        )
        self.public_key_hex = public_key_hex


    def get_encrypted_key(self, encode: str) ->bytes:
        
        return  encryption(
            self.public_key_hex, encode
        )

    def publish(self, metadata:str, price:int) -> DDO:

        ddo = self.nevermined.assets.create(
            metadata=metadata,
            publisher_account=self.account,
            providers=[self.gateway_address],
            asset_rewards={
                "_amounts": [str(price)],
                "_receivers": [self.provider_address],
                "_tokenAddress": self.token_address
            }        
        )

        logger.debug(f'Published DDO with id {ddo.did}')
        return ddo