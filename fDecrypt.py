import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys

password = b'mypassword'
# salt = os.urandom(16)
salt = b'1\xf6I\xf3\xce\xd4\x02^\x94\xbe\xb0\xe4\x8bO\x04\x1d'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
 )
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

with open("myText.enc", "r") as enc_file:
    cipher_text = enc_file.read()

enc_cipher_text = cipher_text.encode()
message = f.decrypt(enc_cipher_text)
print(message)
