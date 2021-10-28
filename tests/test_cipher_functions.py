import unittest
from requests.auth import HTTPBasicAuth
from views.cipher_functions import CipherCrypt as _CipherCrypt, cipher_app
from fastapi.testclient import TestClient


class TestCipherCrypt(unittest.TestCase):

    def test_encrypt_function(self):
        """
        The test checks if the input message actually alters from the returned allegedly ciphered output.
        """
        message: str = "This is a test message."
        enciphered_message, key = _CipherCrypt.encrypt(message, key='50')
        assert message != enciphered_message

    def test_decrypt_function(self):
        """
        The test checks if the decrypting function actually gives back the initially encoded message.
        """
        message: str = "This is a test message."
        cipher, key = _CipherCrypt.encrypt(message, key='50')
        deciphered_message = _CipherCrypt.decrypt(cipher, key)
        assert message == deciphered_message

    def test_encipher_view(self):
        """
        The test checks if the encipher view generates a response with expected format and values.
        """
        # Encipher function config
        client = TestClient(cipher_app)
        username = "XYZ"
        password = "XYZ"
        plain_message_payload = {"message": "This is a test message.",
                                 "key": "[h&*xW:zhs"}
        encipher_view_response = client.post('/encipher', auth=HTTPBasicAuth('XYZ', 'XYZ'), params=plain_message_payload)

        # Checks if the status code of response is 200 also checking correctness of its URL address.
        assert encipher_view_response.status_code == 200

        assert encipher_view_response.json() == {"enciphered_message": "0f004f59583e495a09532f0d555e583a5f091b123c0d08",
                                                 "key": "[h&*xW:zhs"}

    def test_decipher_view(self):
        """
        The test checks if the decipher view generates a response with expected format and values.
        """
        client = TestClient(cipher_app)
        # Decipher function config
        message_to_decipher_payload = {"message": "0f004f59583e495a09532f0d555e583a5f091b123c0d08",
                                       "key": "[h&*xW:zhs"}

        decipher_view_response = client.post('/decipher', auth=HTTPBasicAuth('XYZ', 'XYZ'),
                                             params=message_to_decipher_payload)

        assert decipher_view_response.json() == {"deciphered_message": "This is a test message."}
        # Checks if the status code of response is 200 also checking correctness of its URL address.
        assert decipher_view_response.status_code == 200


if __name__ == "__main__":
    unittest.main()
