#!/bin/bash

echo "Running tests..."

# Create new file
yes | python3 passman.py -f testfile -nf -e

# Create new account
yes | python3 passman.py -f testfile -na bob -e
# Get password for account
yes | python3 passman.py -f testfile -g bob -e
# Change password, specifying password length
#! TODO: check below - how do I know if it's creating a PW of correct length?
yes | python3 passman.py -f testfile -cp bob -l 4 -e
# Change password with specified password
#! TODO: check below - how do I know if it's creating correct PW?
yes | python3 passman.py -f testfile -cp bob -sp 8080boat -e
# Get password, printing to screen
yes | python3 passman.py -f testfile -g bob -print -e
#! Delete account
yes | python3 passman.py -f testfile -d bob -e

rm testfile

echo "Done running tests"