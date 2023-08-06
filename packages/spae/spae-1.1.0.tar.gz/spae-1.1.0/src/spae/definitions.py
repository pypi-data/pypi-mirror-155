from enum import Enum, unique


@unique
class DataBaseType(Enum):
    '''
    used for spae.register_db
    '''
    MONGODB = 1
    POSTGRES = 2
