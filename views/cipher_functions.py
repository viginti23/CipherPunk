import random
import string
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from apps import cipher_app

security_scheme = HTTPBasic()


class CipherCrypt:
    """
    Implementation of a simple XOR encrypting symmetric algorithm.
    """

    @staticmethod
    def random_key_string_generator(string_length: int = 10):
        random_key_string = ''.join(random.choices(string.printable[:97], k=string_length))
        return random_key_string

    @staticmethod
    def encrypt(message: str, key: str = None) -> tuple:
        # If user doesn't provide their own key, generate one randomly
        if not key:
            key = CipherCrypt.random_key_string_generator()

        encrypted_message = ""
        # Assuming a case when len(key) < len(message), we must make sure that the key letters repeat
        key_counter = 0
        for i in range(len(message)):
            temp = ord(message[i]) ^ ord(key[key_counter])
            # zfill pads a single letter hex with 0 making it two letter pair
            encrypted_message += hex(temp)[2:].zfill(2)
            key_counter += 1
            if key_counter >= len(key):
                # once all of the key's letters are used, repeat the key
                key_counter = 0
        return encrypted_message, key

    @staticmethod
    def decrypt(encrypted_message: str, key: str) -> str:

        hex_to_uni = ""
        for i in range(0, len(encrypted_message), 2):
            hex_to_uni += bytes.fromhex(encrypted_message[i:i + 2]).decode('utf-8')

        key = str(key)
        decrypted_message = ""
        key_itr = 0
        for i in range(len(hex_to_uni)):
            # # XORing each characters' ASCII number representation against the generated key char
            temp = ord(hex_to_uni[i]) ^ ord(key[key_itr])
            decrypted_message += chr(temp)
            key_itr += 1
            if key_itr >= len(key):
                # once all of the key's letters are used, repeat the key
                key_itr = 0
        return decrypted_message


@cipher_app.post('/encipher')
def encipher(message: str, key: Optional[str], credentials: HTTPBasicCredentials = Depends(security_scheme)):
    if credentials.username == 'XYZ' and credentials.password == "XYZ":
        enciphered_message, actual_key = CipherCrypt.encrypt(message, key)
        return {
            "enciphered_message": enciphered_message,
            "key": actual_key
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@cipher_app.post('/decipher')
def decipher(message: str, key: str, credentials: HTTPBasicCredentials = Depends(security_scheme)):
    if credentials.username == 'XYZ' and credentials.password == "XYZ":
        deciphered_message = CipherCrypt.decrypt(message, key)
        return {
            "deciphered_message": deciphered_message
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
