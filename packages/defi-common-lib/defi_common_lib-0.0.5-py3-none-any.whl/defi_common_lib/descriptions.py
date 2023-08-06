from pydoc import describe

from defi_common_lib.nvm.periodicity import Periodicity


class Descriptions:
    def __init__(self, category: str, subcategory: str, from_date: str, to_date: str, protocol: str, version: str, blockchain: str, periodicity:Periodicity=Periodicity.OTHER):
        self.category = category
        self.subcategory = subcategory
        self.from_date = from_date
        self.to_date = to_date
        self.protocol = protocol
        self.version = version
        self.blockchain = blockchain
        self.periodicity = periodicity
        self.COMMON_TEXT = (
            "This dataset contains all the {} events between the dates {} and {} "
            "in the the {} protocol version {} in the {} blockchain in CSV format. "
            "\nThe fields contained in this file are:"
        )  if not self.periodicity.MONTH else (
            "This dataset contains all the {} events for {} "
            "in the the {} protocol version {} in the {} blockchain in CSV format. "
            "\nThe fields contained in this file are:"
        ) 


        self.LENDING_DEPOSITS = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- Token: Token deposited"
            "- Amount: Amount of token deposited"
            "- Timestamp: Block timestamp where the transaction was included"          
        )
        self.LENDING_BORROWS = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- Token: Token borrowed"
            "- Amount: Amount of token borrowed"
            "- Timestamp: Block timestamp where the transaction was included"          
        )
        self.LENDING_LIQUIDATIONS = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- Timestamp: Block timestamp where the transaction was included"          
        )
        self.LENDING_REPAY = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- Token: Token repayed"
            "- Amount: Amount of token repayed"
            "- Timestamp: Block timestamp where the transaction was included"          
        )
        self.LENDING_REDEM = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- Token: Token redeemed"
            "- Amount: Amount of token redeemed"
            "- Timestamp: Block timestamp where the transaction was included"     
        )
        self.LENDING_FLASHLOANS = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- Token: Token borrowed"
            "- Amount: Amount of token borrowed"
            "- Timestamp: Block timestamp where the transaction was included"          
        )
        self.DEX_TRADES = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- From token: Origin token swap"
            "- To token: Token destination swap"
            "- From token amount: Origin token amount"
            "- To token amount: Origin token amount"
            "- Pool: Pool id where the token was executed"
            "- Timestamp: Block timestamp where the transaction was included"
        )
        self.DEX_LIQUIDITY = (
            self.COMMON_TEXT +
            "- User: User that sent the swap"
            "- Protocol: Protocol where the swap was executed"
            "- Blockchain: Blochain where the swap was executed"
            "- Version: version of the protocol"
            "- TrasactionId: Transaction id where the trade was executed"
            "- Token0: Left side token"
            "- Token1: Right side token"
            "- Amount Token0: Total amount of token0 deposited or withdrawn"
            "- Amount Token1: Total amount of token1 deposited or withdrawn"
            "- Type: Type of liquidity providing mint or burn"
            "- Timestamp: Block timestamp where the transaction was included"          
        )
        self.DEX_VOLUMES = (
            self.COMMON_TEXT 
        )
        self.DEX_APY = (
            self.COMMON_TEXT 
        )
        self.BUNDLE = (
            "Bundle of several datasets"
        )

        self.DESCRIPTION_TYPES = {
            'Lending': {
                'Deposits': self.LENDING_DEPOSITS,
                'Borrows': self.LENDING_BORROWS,
                'Liquidations': self.LENDING_LIQUIDATIONS,
                'Repays': self.LENDING_REPAY,
                'Redeems': self.LENDING_REDEM,
                'Flashloans': self.LENDING_FLASHLOANS
            },
            'Dex': {
                'Trades': self.DEX_TRADES,
                'Liquidity': self.DEX_LIQUIDITY,
                'Volumes': self.DEX_VOLUMES,
                'Apy': self.DEX_APY,
                'ApyMonth': self.DEX_APY
            },
            'bundle': {
                'bundle': self.BUNDLE
            }
        }

    def get_description(self):
        description = self.DESCRIPTION_TYPES[self.category][self.subcategory].format(
            self.subcategory,
            self.from_date,
            self.to_date,
            self.protocol,
            self.version,
            self.blockchain
        ) if not self.periodicity.MONTH else self.DESCRIPTION_TYPES[self.category][self.subcategory].format(
            self.subcategory,
            self.from_date,
            self.protocol,
            self.version,
            self.blockchain
        ) 

        return description
