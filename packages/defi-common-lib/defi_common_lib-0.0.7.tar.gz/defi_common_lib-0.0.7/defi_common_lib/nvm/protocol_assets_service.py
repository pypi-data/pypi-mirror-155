from defi_common_lib.nvm.publish_service import PublishService

from defi_common_lib.descriptions import Descriptions
from defi_common_lib.constants import Samples
from defi_common_lib.constants import Constants
from defi_common_lib.nvm.periodicity import Periodicity
from datetime import datetime
from datetime import timedelta
from defi_common_lib.version import __version__
import uuid
from common_utils_py.ddo.ddo import DDO
from typing import Any

class ProtocolAssetsPublishService(PublishService):

    def __init__(self,
                config_file: str, 
                gateway_address: str, 
                provider_address: str, 
                provider_password: str, 
                provider_keyfile: str, 
                crypto_key_file: str, 
                crypto_password: str,
                token_address: str):


        super().__init__(config_file, 
                    gateway_address, 
                    provider_address, 
                    provider_password, 
                    provider_keyfile, 
                    crypto_key_file, 
                    crypto_password,
                    token_address)
       
       
    def publish_protocol_asset(self,
                            url: str,
                            filename: str,
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

        
        delta = timedelta(days=1)
        #file_name = filename.split('-')
        now = datetime.now()
        date_created = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        data_published = data_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        #from_date = data_date.strftime('%b %d %Y')
        #to_date = (data_date + delta) .strftime('%b %d %Y')
        version = __version__

        description = Descriptions(
            protocol=protocol,
            category=category,
            subcategory=subcategory,
            from_date=from_date,
            to_date=to_date,
            version=protocol_version,
            blockchain=blockchain,
            periodicity= periodicity
        ).get_description()
       
        key =  super().get_encrypted_key(url.encode())
        sample_url = Samples.SAMPLE_URL[category][subcategory]

        metadata = {
            "main": {
                "name": filename,
                "dateCreated": date_created,
                "author": "Keyko GmbH",
                "license": "CC0: Public Domain",
                "price": price,
                "datePublished": data_published,
                "network": blockchain,
                "files": [
                    {
                        "index": 0,
                        "contentType": "text/csv",
                        "checksum": str(uuid.uuid4()),
                        "checksumType": "MD5",
                        "contentLength": file_size,
                        "url": url
                    }
                ],
                "type": "dataset"
            },
            "additionalInformation": {
                "description": description,
                "categories": [
                    f'ProtocolType:{category}',
                    f'EventType:{subcategory}',
                    f'Blockchain:{blockchain}',
                    f'UseCase:defi-datasets',
                    f'Version:{version}'
                ],
                "blockchain": blockchain,
                "version": version,
                "source": "filecoin",
                "file_name": filename,
                "key": key.hex(),
                "sampleUrl": sample_url,
                "customData": {
                    "periodicity" : periodicity.value
                }
            },
        }

        return super().publish(metadata, price)



    def publish_protocol_bundle(self,
                            filename: str,
                            file_size:str,
                            url: str,
                            data_date: datetime,
                            price: int)-> DDO:

        periodicity=Periodicity.OTHER,
        blockchain=Constants.NA,
        category=Constants.BUNDLE,
        protocol=Constants.NA,
        subcategory=Constants.BUNDLE,
        protocol_version='NA',
        
        return super().publish_protocol_asset(url,
                            filename,
                            category,
                            subcategory,
                            blockchain,
                            protocol,
                            periodicity,
                            file_size,
                            data_date,
                            protocol_version,
                            price)