# CipherPunk
A recruitment assigment for a cipher API.

This simple FastAPI app contains just two endpoints: 
- enciphering a message,
- deciphering a message.

To encipher a message one must enter the following hardcoded credentials:
username: XYZ
password: XYZ

Enciphering endpoint requires a message and optionally a selected key (in the form of string) and it returns both the enciphered message as well as used key 
(if a custom one was not provided initially).
Deciphering endpoint requires the encrypted message and the key used to cipher the message and it return the original message.

To run the code:
- open the project in your IDE,
- change directory to /CipherPunk
- run command: uvicorn views.cipher_functions:cipher_app --reload
- open a browser at localhost:8000 to enjoy the docs. 
