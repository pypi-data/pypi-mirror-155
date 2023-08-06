class DefiMarketplaceException(Exception):
    """Defi Marketplace Base Exception"""
    pass

class NotProtocolFilesException(DefiMarketplaceException):
    """Raised when not protocol files are found in S3"""
    pass

class NotDependencyProvidedException(DefiMarketplaceException):
    """Raised when not protocol files are found in S3"""
    pass

