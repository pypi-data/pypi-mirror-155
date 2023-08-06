from defi_common_lib.factory.object_factory import ObjectFactory
from defi_common_lib.storage.filecoin_service import FilecoinServiceBuilder
from defi_common_lib.storage.s3_service import S3ServiceBuilder


factory = ObjectFactory()
factory.register_builder('FILECOIN', FilecoinServiceBuilder())
factory.register_builder('S3', S3ServiceBuilder())


"""
Example of use

def initS3Service():
       
    config = {
        's3_access_key': Constants.AWS_ACCESS_KEY_ID,
        's3_secret_key': Constants.AWS_SECRECT_ACCESS_KEY
    }

    return factory.create('S3', **config)

def initFilecoinService():
       
    config = {
        'crypto_key_file': Constants.CRYPTO_KEY_FILE,
        'crypto_password': Constants.CRYPTO_PASSWORD,
        'gateway_url': Constants.GATEWAY_URL
    }

    return factory.create('FILECOIN', **config)

"""