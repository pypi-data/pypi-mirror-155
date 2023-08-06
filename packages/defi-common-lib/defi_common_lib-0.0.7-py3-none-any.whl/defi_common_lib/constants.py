class Constants:
    PENDING_STATUS = 'PENDING'
    PROCESSING_STATUS = 'PROCESSING'
    COMPLETED_STATUS = 'COMPLETED'
    ZIP_EXTENSION = 'zip'
    BUNDLE = 'bundle'
    NA = 'NA'

class Samples:
    SAMPLE_URL = {
            'Lending': {
                'Deposits': "https://bafkreihli7bq6ikp3kfpdsd35s3edxkx7jakcdth6chjadwjw5ujg35tja.ipfs.dweb.link",
                'Borrows': "https://bafkreihli7bq6ikp3kfpdsd35s3edxkx7jakcdth6chjadwjw5ujg35tja.ipfs.dweb.link",
                'Liquidations': "https://bafkreifrcoupu3jzjm5wksqkwoqir6dnccshq437kyd3hg4inojcba3juu.ipfs.dweb.link/",
                'Repays': "https://bafkreifrcoupu3jzjm5wksqkwoqir6dnccshq437kyd3hg4inojcba3juu.ipfs.dweb.link/",
                'Redeems': "https://bafkreigl5qisozc7nicpjavae7houhkgfrspwnb6tliienndzvm3eybwdy.ipfs.dweb.link/",
                'Flashloans': "https://bafkreib7wob6j5yu5u6bhmo24syzdqqyozydrptke243nrkgi2lbc6ups4.ipfs.dweb.link/"
            },
            'Dex': {
                'Trades': "https://bafkreietuquqyatfp4tmkj4qalb6jlzo7wnu67umw64bgvi2dct6ehuqmq.ipfs.dweb.link/",
                'Liquidity': "https://bafkreia5dwqawr5i33nptbqgksnta7gjvvuj2pcrkqqdiw235uqeehuqhm.ipfs.dweb.link/",
                'Volumes': "https://bafkreia5dwqawr5i33nptbqgksnta7gjvvuj2pcrkqqdiw235uqeehuqhm.ipfs.dweb.link/",
                'Apy': "https://bafkreia5dwqawr5i33nptbqgksnta7gjvvuj2pcrkqqdiw235uqeehuqhm.ipfs.dweb.link/",
                'ApyMonth': "https://bafkreia5dwqawr5i33nptbqgksnta7gjvvuj2pcrkqqdiw235uqeehuqhm.ipfs.dweb.link/"
            },
            'bundle': {
                'bundle': ""
            }
        }


class AgentIds:
    DEX_LIQUIDITY='DEXLIQUI'
    DEX_TRADES='DEXTRAD'
    DEX_VOLUMES='DEXVOL'
    DEX_POOL='DEXPOOL'
    DEX_APY='DEXAPY'
    LENDING_BORROWS='LENDBOR'
    LENDING_DEPOSITS='LENDDEP'
    LENDING_FLASHLOANS='LENDFLAS'
    LENDING_LIQUIDATIONS='LENDLIQ'
    LENDING_PRICES='LENDPRICE'
    LENDING_REDEEMS='LENDRED'
    LENDING_REPAYS='LENDREP'