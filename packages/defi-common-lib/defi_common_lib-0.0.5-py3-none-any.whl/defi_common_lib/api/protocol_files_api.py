from defi_common_lib.exceptions import NotDependencyProvidedException
from defi_common_lib.nvm.protocol_assets_service import ProtocolAssetsPublishService
from defi_common_lib.storage.filecoin_service import FilecoinService
from defi_common_lib.storage.s3_service import S3Service 
from defi_common_lib.protocol_files.merge_files import MergeProtocolFilesService
from typing import List, Set, Dict, Tuple, Optional
from common_utils_py.ddo.ddo import DDO

import logging
logger = logging.getLogger(__name__) 

class ProtocolFilesApi:
    """ API to handle files with Defi Protocols Data"""
    def __init__(self,  
            s3_service: S3Service = None, 
            filecoin_service: FilecoinService = None, 
            publish_service: ProtocolAssetsPublishService = None
            )-> None:

        self._s3_service = s3_service
        self._filecoin_service = filecoin_service
        self._publish_service = publish_service
        self._merge_files_service = None       


    def __get_merge_files_service(self) -> MergeProtocolFilesService:
        """
            Initializes an instance of the MergeFiles Service
            It needs instances of S3Service, FilecoinSErvice and PublishAssetsService

            :return: instance of MergeProtocolFilesService
        """

        if not self._s3_service:
            raise NotDependencyProvidedException("S3Service not Provided")

        if not self._filecoin_service:
            raise NotDependencyProvidedException("FilecoinService not Provided")

        if not self._publish_service:
            raise NotDependencyProvidedException("PublishAssetsService not Provided")

        if not self._merge_files_service:
            logger.info("Creating new MergeProtocolFilesService ")
            self._merge_files_service = MergeProtocolFilesService(self._s3_service, self._filecoin_service, self._publish_service)

        return self._merge_files_service


    def publish_monthly_protocol_assets(self,
                                        bucket_name: str, 
                                        agent: str, 
                                        category: str,
                                        subcategory: str, 
                                        year: str, 
                                        month: str, 
                                        protocols: List[str], 
                                        price: int,
                                        base_path: str) -> List[DDO]:

        """
            Merge and publish in NVM files of the same protocol and network by year and month and saves the merged files in S3
            :param bucket_name: Name of the s3 bucket where the protocol files are located
            :param agent: Name of the agent (Loader agent)
            :param category: Category
            :param subcategory: Subcategory 
            :param year: Year
            :param month: Month (represented as a number)
            :param protocols: List of the name of the protocols to find ("ALL" to find all )
            :price price of the NVM asset 
            :base_path base s3 path where the merged files will be stored (s3://{bucket}/{key}/)
            :return: List of DDOs of the published assets
        
        """            
        
        merge_service = self.__get_merge_files_service()

        if not merge_service:
            raise NotDependencyProvidedException("MergesService not Provided")

        logger.info("Merging and Publishing monthly agg of  protocol files. Bucket: {} Agent: {} Category: {} Subcategory: {} Year: {} Month: {}".format(bucket_name, agent, category, subcategory, year, month))

        files_paths = merge_service.merge_protocol_files_by_month_inS3(bucket_name, agent, year, month, protocols, base_path)
        return merge_service.publish_monthly_protocol_files( category, subcategory, year, month, price, files_paths)


    def publish_monthly_protocol_asset(self,
                                        bucket_name: str, 
                                        agent: str, 
                                        category: str,
                                        subcategory: str, 
                                        year: str, 
                                        month: str, 
                                        protocol: str, 
                                        price: int,
                                        base_path: str) -> DDO:

        """
            Merge and publish in NVM a file of the same protocol and network by year and month and saves the merged files in S3
            :param bucket_name: Name of the s3 bucket where the protocol files are located
            :param agent: Name of the agent (Loader agent)
            :param category: Category
            :param subcategory: Subcategory 
            :param year: Year
            :param month: Month (represented as a number)
            :param protocols: Protocol to find 
            :price price of the NVM asset 
            :base_path base s3 path where the merged files will be stored (s3://{bucket}/{key}/)
            :return: DDO of the published asset
        
        """            
        
        ddos = self.publish_monthly_protocol_assets(bucket_name, agent, category, subcategory, year, month, [protocol], price, base_path)
        return ddos.pop()

       