import hashlib
from datetime import datetime


def generate(key=None, amount=None):
    """
    Generates random hash
    @param key: string
    @param amount: int
    @return: string
    """
    hash = hashlib.sha1()
    salt = key if key is not None else str(datetime.now().timestamp())
    hash.update(salt.encode('utf-8'))
    hash.hexdigest()
    return hash.hexdigest()[:(amount if amount is not None else 10)]
