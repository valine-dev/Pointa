from os import path

from cryptography.hazmat.backends import \
    default_backend as crypto_default_backend
from cryptography.hazmat.primitives import \
    serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa

paths = [
    './Pointa_CLI_Client/Keys/private_key.pem',
    './Pointa_CLI_Client/Keys/public_key.pem'
]


def checkNew():
    global paths
    return not(path.isfile(path.abspath(paths[0])))


def newUser():
    'Generate a new Keypair then write it into files'

    global paths

    Key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    pvKey = Key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())

    pbKey = Key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH)

    with open(path.abspath(paths[0]), 'wb') as pv:
        pv.write(pvKey)

    with open(path.abspath(paths[1]), 'wb') as pb:
        pb.write(pbKey)

    return [pbKey, pvKey]


def getKeys():
    keys = []

    global paths

    with open(path.abspath(paths[1]), 'r') as pb:
        keys.append(pb.read())

    with open(path.abspath(paths[0]), 'r') as pv:
        keys.append(pv.read())

    return keys


def load():
    if checkNew():
        return newUser()
    else:
        return getKeys()
