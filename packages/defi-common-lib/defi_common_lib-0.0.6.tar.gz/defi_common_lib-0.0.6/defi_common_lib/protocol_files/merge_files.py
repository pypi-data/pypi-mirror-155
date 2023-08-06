from collections import defaultdict
from datetime import datetime
import sys
from defi_common_lib.nvm.protocol_assets_service import ProtocolAssetsPublishService
from defi_common_lib.storage.filecoin_service import FilecoinService
from defi_common_lib.storage.s3_service import S3Service 
from defi_common_lib.nvm.periodicity import Periodicity
from typing import List, Set, Dict, Tuple, Optional
from defi_common_lib.exceptions import DefiMarketplaceException, NotProtocolFilesException
from common_utils_py.ddo.ddo import DDO


import logging
logger = logging.getLogger(__name__) 


class MergeProtocolFilesService:
    """It provides functions to read protocol files from S3 and merge them together by some periodicity """

    def __init__(self, s3Service: S3Service, filecoinService: FilecoinService, publishService: ProtocolAssetsPublishService):
        self.s3Service = s3Service
        self.filecoinService = filecoinService
        self.publishService = publishService

    # returns a map where the key is protocol_network (ex: Aave-v2_Ethereum) and the value an array of files found in the path for that protocol and network
    def get_files_by_protocol_network(self, bucket: str, agent: str, year: str, month: str, protocols_to_filter: List[str]) -> Dict[str, List[str]]:
        """
            Finds the files stored in S3 for that match the criteria of agent, year, month and protocol indicated by the parameters

            :param bucket: Name of the s3 bucket
            :param agent: Name of the agent (Loader agent)
            :param year: Year
            :param month: Month (represented as a number)
            :param protocols_to_filter: List of the name of the protocols to find ("ALL" to find all )
            :return: Dictionary which contains a list of the file paths found by each protocol_network
        """

        logger.debug("Getting protocol files from S3. Bucket: {} Agent: {} Year: {} Month: {}".format(bucket, agent, year, month))

        files = self.s3Service.list_protocol_files(bucket, agent, year, month, protocols_to_filter)
    
        files_by_protocol = defaultdict(list)
        for protocol, network, name, path in files: 
            files_by_protocol[f'{protocol}_{network}'].append({'name': name,'path': path})
        
        logger.debug("Found files for Protocols and Nertworks: {}".format(files_by_protocol.keys()))
        
        return files_by_protocol
    
    
    def merge_protocol_files_by_month_inS3(self, bucket_name :str, agent: str, year: str, month: str, protocols: List[str], base_path:str) -> List[str]:  
        """
            Merge files of the same protocol and network by year and month  and saves the merged files in S3
            :param bucket_name: Name of the s3 bucket
            :param agent: Name of the agent (Loader agent)
            :param year: Year
            :param month: Month (represented as a number)
            :param protocols: List of the name of the protocols to find ("ALL" to find all )
            :return: List of the s3 paths with the merged files
        
        """

        # Example of parameters:
        # agent='LENDPRICE'
        # month='04'
        # year='2022'
        # protocol=['Aave-v2']
        # protocols=['Aave-v2','Compound-v2']
        # protocols=['ALL']
        
        logger.debug("Merging protocol files. Bucket: {} Agent: {} Year: {} Month: {}".format(bucket_name, agent, year, month))

        files =  self.get_files_by_protocol_network(bucket_name, agent, year, month, protocols)

        if files == {}:
            logger.info("No Protocol files found")
            raise NotProtocolFilesException

        merged_paths = []

        for protocol in files.keys():
            logger.debug("Getting data from s3 for Protocol: {}".format(files[protocol]))
           
            paths = list(map(lambda obj: obj['path'] , files[protocol]))
            df= self.s3Service.get_dataframe_from_files(paths)
            
            path = f'{base_path}/{protocol}_{agent}_{year}{month}.csv'

            logger.debug("Saving merged csv in s3 path: {}".format(path))
            self.s3Service.save_dataframe(df, path)
            del df
            merged_paths.append(path)

        return merged_paths


    def __get_data_from_filename(self, file_name:str)-> Tuple :
        """ 
            Extracts protocol, version and network from a file name
            :param file_name: name of the file
            :return: Tuple with protocol, version, network
        """

         # example of name: Aave-v2_Polygon_LENDFLAS_202204.csv
        splits = file_name .split( '_')
        protocol =  splits[0][:splits[0].find('-')]
        version =  splits[0][splits[0].find('-')+1:]
        network = splits[1]

        return (protocol, version, network)



    def publish_monthly_protocol_files(self,
                                    category: str,
                                    subcategory: str, 
                                    year: str, 
                                    month: str, 
                                    price: int,
                                    paths: List[str]) -> List[DDO]: 

        """
            Publish in NVM files of the same protocol and network by year and month
            :param category: Category
            :param subcategory: Subcategory 
            :param year: Year
            :param month: Month (represented as a number)
            :param price: price of the NVM asset 
            :param paths: s3 paths where the merged files are located
            :return: List of DIDs of the published assets
        
        """
                                                
        logger.info("Publish in NVM monthly agg of protocol files. Category: {} Subcategory: {} Year: {} Month: {}".format(category, subcategory, year, month))
        ddos = []

        for path in paths:
           logger.debug("Reading merged file {} ".format(path))
           df= self.s3Service.get_dataframe_from_files(path)
           file_name = path[path.rfind('/')+1:]

           # example of name: Aave-v2_Polygon_LENDFLAS_202204.csv
           protocol, version, network = self.__get_data_from_filename(file_name)

           csv = df.to_csv() 
           file_size = sys.getsizeof(csv)
           
           logger.debug("Uploading file {} to Filecoin".format(file_name))
           url = self.filecoinService.save_file(file_content= csv, file_name = file_name)
           logger.debug("filecoin ID {}".format(url))
        
           month_date = datetime.strptime(f'{year}{month}', '%Y%m').strftime('%b_%Y')
           asset_name= f'{protocol} {version} {month_date}'    
           
           logger.debug("Publishing Asset {} in Nevermined".format(asset_name))

           ddo = self.publishService.publish_protocol_asset(
                           url,
                           asset_name,
                           category,
                           subcategory,
                           network,
                           protocol,
                           Periodicity.MONTH,
                           file_size,
                           datetime.now(),
                           month_date,
                           '',
                           version,
                           price
                        )

           ddos.append(ddo) 
           logger.info("Asset {} published in Nevermined with did {}".format(asset_name, ddo.did))   
           del df

        return ddos