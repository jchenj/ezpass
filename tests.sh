#!/bin/bash

####################
# Integration tests that manipulate ezpass in unencrypted mode
####################

echo "Running tests..."

rm -f testfile

# Create new file
python3 ezpass.py -f testfile -nf --no-encrypt
# Create new account
python3 ezpass.py -f testfile -no bob --no-encrypt
# Get password for account
python3 ezpass.py -f testfile -g bob --no-encrypt
# Change password, specifying password length
#! TODO: consider how to determine if prog creating a PW of correct length
python3 ezpass.py -f testfile -cp bob -l 4 --no-encrypt
# Change password with specified password
#! TODO: consider how to determine if prog creating correct PW
python3 ezpass.py -f testfile -cp bob -sp --no-encrypt
# Get password, printing to screen
python3 ezpass.py -f testfile -g bob -print --no-encrypt
#! Delete account
python3 ezpass.py -f testfile -d bob --no-encrypt

rm testfile

echo "Done running tests"