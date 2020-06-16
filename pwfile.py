"""
Defines a Pwfile class for creating & managing password files in ezpass
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os
import pickle
import base64


class PwFile:
    '''
    Represents a password file that is optionally password-protected.
    The file stores data in pickled format.
    '''

    def __init__(self, fname: str, fpass: str, encrypt: bool) -> None:
        """
        :param fname: name of file (str)
        :param fpass: password for file fname (str)
        :param encrypt: whether or not file is encrypted (bool)
        """
        if not os.path.isfile(fname):
            raise RuntimeError("File '{}' does not exist".format(fname))
        self.fname = fname
        self.fpass = fpass
        self.encrypt = encrypt
        # try to read file w/o storing output. If fails (e.g. wrong
        # password or no password), will raise exception that must be handled
        # by caller (Could store output here & refactor)
        self.readFile()

    @staticmethod
    def _encryptFile(fname, fpass, data: list) -> None:
        # Pickle data (list of Account instances)
        pickledData = pickle.dumps(data)
        encodedPassword = fpass.encode()

        # salt = os.urandom(16)
        salt = b"1\xf6I\xf3\xce\xd4\x02^\x94\xbe\xb0\xe4\x8bO\x04\x1d"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(encodedPassword))
        f = Fernet(key)
        cipher_text = f.encrypt(pickledData)

        with open(fname, "wb") as enc_file:
            enc_file.write(cipher_text)
        return

    def _decryptFile(self) -> str:
        encodedPassword = self.fpass.encode()

        # salt = os.urandom(16)
        salt = b'1\xf6I\xf3\xce\xd4\x02^\x94\xbe\xb0\xe4\x8bO\x04\x1d'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(encodedPassword))
        f = Fernet(key)

        with open(self.fname, "r") as enc_file:
            cipher_text = enc_file.read()

        enc_cipher_text = cipher_text.encode()
        message = f.decrypt(enc_cipher_text)
        return message

    def readFile(self) -> list:
        """
        Opens self.fname and loads data for accounts. If wrong password,
        :return: list of Account instances
        """
        if self.encrypt:
            decryptedMessage = self._decryptFile()
            data = pickle.loads(decryptedMessage)
        else:
            with open(self.fname, 'rb') as file:
                data = pickle.load(file)

        return data

    def writeFile(self, data: list) -> None:
        """
        Writes data for accounts to PwFile.fname
        :param data: list of Account instances
        :return: None
        :side effect: updated file
        """
        if self.encrypt:
            PwFile._encryptFile(self.fname, self.fpass, data)
        else:
            with open(self.fname, 'wb') as file:
                pickle.dump(data, file)
        return

    def get_fname(self) -> str:
        return self.fname

    def get_fpass(self) -> str:
        return self.fpass

    def change_fpass(self, new_password: str) -> None:
        """
        Changes password for file
        :param new_password: new password for file
        :return: None
        :side effect: file updated with new password
        """
        if not self.fpass():
            raise RuntimeError("Password for file '{}' does not exist".format(self.fname))
        if new_password == "":
            raise RuntimeError("Password cannot be empty")
        self.fpass = new_password
        return

    @staticmethod
    def create_new_file(fname: str, fpass: str, encrypt: bool):
        """
        Given a file name, password and encryption value, creates a new file with those values and an empty
        list for storing accounts
        Assumes that the file name doesn't already exist in the current directory
        :return: PwFile  instance
        :side effect: new file with specified file name, password and encryption value
        """
        # ! TODO: add an option to overwrite file or enter new fname
        # ! TODO: what's best  way to ensure that file is desired format?
        if os.path.isfile(fname):
            raise RuntimeError("File '{}' already exists".format(fname))
        fd = os.open(fname, os.O_CREAT)
        os.close(fd)

        if encrypt:
            PwFile._encryptFile(fname, fpass, [])
        else:
            with open(fname, 'wb') as file:
                pickle.dump([], file)

        new_file = PwFile(fname, fpass, encrypt)
        return new_file





