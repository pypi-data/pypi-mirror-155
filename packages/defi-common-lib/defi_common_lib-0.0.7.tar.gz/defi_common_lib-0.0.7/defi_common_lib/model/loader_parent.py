from datetime import date, datetime
from typing import Any
from retry import retry
import os
import boto3
import uuid
from datetime import timedelta


from defi_common_lib.model.agent import Agent
from defi_common_lib.model.agent_state import AgentState
from defi_common_lib.nvm.publish_service import PublishService
from defi_common_lib.storage.filecoin_service import FilecoinService
from defi_common_lib.storage.s3_service import S3Service
from defi_common_lib.descriptions import Descriptions
from defi_common_lib.constants import Samples
from defi_common_lib.version import __version__


class LoadParent:

    def __init__(self, agent: Agent, state: AgentState, entity: str, end_date: datetime) -> None:
        self.agent = agent
        self.state = state
        self.entity = entity
        self.end_date = end_date
        self.publish_service = PublishService(
            gateway_address=os.getenv('GATEWAY_ADDRESS'),
            config_file=os.getenv('CONFIG_FILE'),
            crypto_key_file=os.getenv('CRYPTO_KEY_FILE'),
            crypto_password=os.getenv('CRYPTO_PASSWORD'),
            provider_address=os.getenv('PROVIDER_ADDRESS'),
            provider_keyfile=os.getenv('PROVIDER_KEYFILE'),
            provider_password=os.getenv('PROVIDER_PASSWORD'),
            token_address=os.getenv('TOKEN_ADDRESS')
        )
        self.s3_session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRECT_ACCESS_KEY')
        )
        self.bucket = os.getenv('BUCKET_NAME')
        self.s3_service = S3Service(
            session=self.s3_session
        )
        self.filecoin_service = FilecoinService(
            gateway_url=os.getenv('GATEWAY_URL')
        )

    def create_metadata(self,
                        file_name: str,
                        data_date: datetime,
                        url: str,
                        file_size: str,
                        price: str):

        delta = timedelta(days=1)
        file_name = file_name.split('-')
        now = datetime.now()
        date_created = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        data_published = data_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        from_date = data_date.strftime('%b %d %Y')
        to_date = (data_date + delta) .strftime('%b %d %Y')
        version = __version__

        description = Descriptions(
            protocol=self.state.protocol_name,
            category=self.agent.category,
            subcategory=self.agent.subcategory,
            from_date=from_date,
            to_date=to_date,
            version=self.state.protocol_version,
            blockchain=self.state.protocol_chain
        ).get_description()

        key = self.publish_service.get_encrypted_key(url.encode())

        sample_url = Samples.SAMPLE_URL[self.agent.category][self.agent.subcategory]

        metadata = {
            "main": {
                "name": file_name[0] + " " + file_name[1],
                "dateCreated": date_created,
                "author": "Keyko GmbH",
                "license": "CC0: Public Domain",
                "price": price,
                "datePublished": data_published,
                "network": self.state.protocol_chain,
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
                    f'ProtocolType:{self.agent.category}',
                    f'EventType:{self.agent.subcategory}',
                    f'Blockchain:{self.state.protocol_chain}',
                    f'UseCase:defi-datasets',
                    f'Version:{version}'
                ],
                "blockchain": self.state.protocol_chain,
                "version": version,
                "source": "filecoin",
                "file_name": file_name,
                "key": key.hex(),
                "sampleUrl": sample_url
            },
        }

        return metadata

    @retry(Exception, tries=3, delay=1)
    def publish_asset(self, metadata: str, price: int):
        return self.publish_service.publish(
            metadata=metadata,
            price=price
        )

    def update_last_state(self, date, last_entry):
        self.state.update_last_state(
            date=date,
            last_entry=last_entry
        )

    def generate_file_name(self, date: datetime):

        date_path = (
            str(date.year) +
            str('%02d' % date.month) +
            str('%02d' % date.day)
        )

        file_key = (
            f'{self.state.protocol_name}-'
            f'v{self.state.protocol_version}-'
            f'{self.agent.id}-'
            f'{self.state.protocol_chain}_{date_path}_{str(date.time())[0:5]}.csv'
        )

        return file_key

    def generate_file_key(self, date: datetime, file_name: str):

        date_path = (
            str(date.year) +
            str('%02d' % date.month) +
            str('%02d' % date.day)
        )

        key = (
            f'{self.agent.id}'
            f'/{self.agent.category}'
            f'/{date_path}'
            f'/{self.agent.id}'
            f'/{file_name}'
        )

        return key

    def save_file_s3(self, file_content: Any,  key: str):
        return self.s3_service.save_file(
            file_content=file_content,
            config={
                'key': key,
                'bucket_name': self.bucket
            }
        )

    def save_file_filecoin(self, file_content: Any, file_name: str):
        return self.filecoin_service.save_file(
            file_content=file_content,
            file_name=file_name
        )
