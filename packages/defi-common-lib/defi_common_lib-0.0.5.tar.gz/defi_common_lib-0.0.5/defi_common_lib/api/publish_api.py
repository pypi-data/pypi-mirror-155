from re import sub
from async_timeout import Any
from defi_common_lib.exceptions import NotDependencyProvidedException
from defi_common_lib.nvm.protocol_assets_service import ProtocolAssetsPublishService
from defi_common_lib.storage.filecoin_service import FilecoinService
from defi_common_lib.nvm.periodicity import Periodicity
from typing import List, Set, Dict, Tuple, Optional
from common_utils_py.ddo.ddo import DDO
from datetime import datetime


import logging
logger = logging.getLogger(__name__) 

class PublishApi:
    """ API to publish assets in NVM """

    def __init__(self,  
            filecoin_service: FilecoinService = None, 
            publish_service: ProtocolAssetsPublishService = None
            )-> None:

        self._filecoin_service = filecoin_service
        self._publish_service = publish_service
        self._merge_files_service = None 

    def publish_asset_in_nvm(self, metadata:str, price:int) -> DDO:
        """
            Publish asset in NVM

            It needs an instance of ProtocolAssetsPublishService

            :param metadata: metadata of the asset
            :param price: price of the asset
            :return: DDO Published in NVM
        """

        if not self._publish_service:
            raise NotDependencyProvidedException("ProtocolAssetsPublishService not Provided")

        return self._publish_service.publish(metadata, price)

    def publish_protocol_asset(self,
                            url: str,
                            file_name: str,
                            category: str,
                            subcategory: str,
                            blockchain: str,
                            protocol: str,
                            periodicity: Periodicity,
                            file_size: str,
                            data_date: datetime,
                            from_date: datetime,
                            to_date: datetime,
                            protocol_version: str,
                            price: int )-> DDO:
        
        """
            Publish an asset that represent a defi protocol dataset in NVM

            It needs an instance of ProtocolAssetsPublishService

            :param url: decentralized url (filecoin) where the data is located
            :param file_name: name of the file
            :param category: Category
            :param subcategory: Subcategory
            :param blockchain: Name of the blockchain network
            :param protocol: Name of the protocol
            :param periodicity: Periodicity of the data contained in the file
            :param file_size: Size of the file (in bytes)
            :param data_date: Date of Publishing
            :param from_date: Start date of the data
            :param to_date: End date of the data
            :param price: price of the asset
            :return: DDO Published in NVM
        """

        if not self._publish_service:
            raise NotDependencyProvidedException("ProtocolAssetsPublishService not Provided")

        return self._publish_service.publish_protocol_asset(url,
                                                file_name,
                                                category,
                                                subcategory,
                                                blockchain,
                                                protocol,
                                                periodicity,
                                                file_size,
                                                data_date,
                                                from_date,
                                                to_date,
                                                protocol_version,
                                                price)
                                            

    def publish_protocol_asset_from_content(self,
                                    file_content: Any,
                                    file_name: str,
                                    category: str,
                                    subcategory: str,
                                    blockchain: str,
                                    protocol: str,
                                    periodicity: Periodicity,
                                    file_size: str,
                                    data_date: datetime,
                                    from_date: datetime,
                                    to_date: datetime,
                                    protocol_version: str,
                                    price: int)-> DDO:

        """
            Publish an asset that represent a defi protocol dataset in NVM.
            It will upload the content in Filecoin before publishing the asset in NVM

            It needs  instances of ProtocolAssetsPublishService and FilecoinService

            :param file_content: content of the file 
            :param file_name: name of the file
            :param category: Category
            :param subcategory: Subcategory
            :param blockchain: Name of the blockchain network
            :param protocol: Name of the protocol
            :param periodicity: Periodicity of the data contained in the file
            :param file_size: Size of the file (in bytes)
            :param data_date: Date of Publishing
            :param from_date: Start date of the data
            :param to_date: End date of the data
            :param price: price of the asset
            :return: DDO Published in NVM
        """
        
        if not self._publish_service:
            raise NotDependencyProvidedException("ProtocolAssetsPublishService not Provided")

        if not self._filecoin_service:
            raise NotDependencyProvidedException("FilecoinService not Provided")

        logger.debug("Uploading file {} to Filecoin".format(file_name))
        url = self.filecoinService.save_file(file_content= file_content, file_name = file_name)
        logger.debug("filecoin ID {}".format(url))

        return self.publish_protocol_asset(url, 
                                file_name,
                                category,
                                subcategory, 
                                blockchain, 
                                protocol, 
                                periodicity, 
                                file_size, 
                                data_date, 
                                from_date, 
                                to_date, 
                                protocol_version, 
                                price)

        

    

