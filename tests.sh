#!/bin/bash

####################
# Integration tests that manipulate ezpass in unencrypted mode
####################

echo "Running tests..."

# Create new file
python3 ezpass.py -f testfile -nf
# Create new account
python3 ezpass.py -f testfile -no bob
# Get password for account
python3 ezpass.py -f testfile -g bob
# Change password, specifying password length
#! TODO: consider how to determine if prog creating a PW of correct length
python3 ezpass.py -f testfile -cp bob -l 4
# Change password with specified password
#! TODO: consider how to determine if prog creating correct PW
python3 ezpass.py -f testfile -cp bob -sp 8080boat
# Get password, printing to screen
python3 ezpass.py -f testfile -g bob -print
#! Delete account
python3 ezpass.py -f testfile -d bob

  rm testfile

  echo "Done running tests"