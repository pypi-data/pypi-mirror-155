from typing import AnyStr
import bcrypt

PASSWORD_BCRYPT = 1
PASSWORD_DEFAULT = PASSWORD_BCRYPT

PASSWORD_BCRYPT_DEFAULT_COST = 10


def password_hash(password: AnyStr, algorithm=PASSWORD_DEFAULT) -> str:

    password_data: bytes
    if isinstance(password, str):
        password_data = password.encode()
    elif isinstance(password, bytes):
        password_data = password_data
    else:
        raise TypeError('The password argument must be str or bytes.')

    salt = bcrypt.gensalt(PASSWORD_BCRYPT_DEFAULT_COST, prefix=b'2a')
    return bcrypt.hashpw(password_data, salt=salt).decode()


def password_verify(password: AnyStr, hashed_password: AnyStr) -> bool:

    password_data: bytes
    if isinstance(password, str):
        password_data = password.encode()
    elif isinstance(password, bytes):
        password_data = password
    else:
        raise TypeError('The password argument must be str or bytes.')

    hashed_password_data: bytes
    if isinstance(hashed_password, str):
        hashed_password_data = hashed_password.encode()
    elif isinstance(hashed_password, bytes):
        hashed_password_data = hashed_password
    else:
        raise TypeError('The hashed_password argument must be str or bytes.')

    return bcrypt.checkpw(password_data, hashed_password_data)
