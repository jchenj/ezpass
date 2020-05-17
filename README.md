# passman

Command-line password manager written in Python

## Features:

* Maintains passwords in a password-protected file
* Copy password of specified account from file to paste buffer
* Print password of specified account to screen
* Add account (with password) to file
* Delete account (and password) from file
* Change password for an account
* Create a new passwords

## Dependencies
* Requires [pyperclip](https://pypi.org/project/pyperclip/)
* Requires [pycrypto](https://pypi.org/project/pycrypto/)

## Command line usage:
````
passman.py [-h] [--get-pass GET_PASS] [--new-account NEW_ACCOUNT]
                  [--print-to-screen] [--password-length PASSWORD_LENGTH]
                  [--delete-account DELETE_ACCOUNT]
                  [--change-pass CHANGE_PASS] [--new-file NEW_FILE]
                  [--alphabet ALPHABET]

Retrieve password.

optional arguments:
  -h, --help                               show this help message and exit
  --get-pass GET_PASS                      account name
  --new-account NEW_ACCOUNT                new account name
  --print-to-screen                        print password to screen
  --password-length PASSWORD_LENGTH        password length
  --delete-account DELETE_ACCOUNT          delete specified account
  --change-pass CHANGE_PASS                change password for specified account
  --new-file NEW_FILE                      create new file for passwords
  --alphabet ALPHABET                      full alphabet
````
