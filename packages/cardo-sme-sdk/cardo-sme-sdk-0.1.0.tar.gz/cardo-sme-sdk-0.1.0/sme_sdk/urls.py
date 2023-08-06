from enum import Enum, unique


@unique
class Url(Enum):
    login = 'auth/login'
    company = 'company'
    new_batch = f'{company}/new_batch'
    batch_result = f'{company}/batch_result'
