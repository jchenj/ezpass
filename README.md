# getpass

Command-line password manager written in Python

## Features:

* Copy password of specified account from file to paste buffer
* Print password of specified account to screen
* Add account (with password) to file
* Delete account (and password) from file
* Change password for specified account
* Create a new file for account information, formatted with columns for "Account" and "Password"

## Data file
To run this program you will need a valid password file in CSV format. To be valid, the file must contain the account names in Column A and passwords in Column B. 

## Dependencies
* Requires [pyperclip](https://pypi.org/project/pyperclip/)

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
