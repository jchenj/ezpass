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
* Interactive mode

## Dependencies
* Requires [pyperclip](https://pypi.org/project/pyperclip/)
* Requires [cryptography](https://pypi.org/project/cryptography/)

## Command line usage:
````
usage: passman.py [-h] -f FILE [-g GET_ACPASS] [-na NEW_ACCOUNT]
                  [-d DELETE_ACCOUNT] [-nf] [-cp CHANGE_ACPASS]
                  [-sp SET_ACPASS] [-print] [-l PASSWORD_LENGTH] [-e]
                  [-a ALPHABET] [-i]

Password manager

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file name
  -g GET_ACPASS, --get-acpass GET_ACPASS
                        org name
  -na NEW_ACCOUNT, --new-account NEW_ACCOUNT
                        new org name
  -d DELETE_ACCOUNT, --delete-account DELETE_ACCOUNT
                        delete account for specified org
  -nf, --new-file       whether or not to create new file
  -cp CHANGE_ACPASS, --change-acpass CHANGE_ACPASS
                        org to change password for
  -sp SET_ACPASS, --set-acpass SET_ACPASS
                        set specified password
  -print, --print-to-screen
                        print password to screen
  -l PASSWORD_LENGTH, --password-length PASSWORD_LENGTH
                        password length
  -e, --encrypt         whether or not file is encrypted
  -a ALPHABET, --alphabet ALPHABET
                        full alphabet
  -i, --interactive     whether or not to use interactive mode
````
