#!/bin/bash

####################
# Integration tests that manipulate ezpass in encrypted mode
####################

echo "Running tests..."

rm -f testfile

# Create new file
yes | python3 ezpass.py -f testfile -nf
# Create new account
yes | python3 ezpass.py -f testfile -no bob
# Get password for account
yes | python3 ezpass.py -f testfile -g bob
# Change password, specifying password length
#! TODO: consider how to determine if prog creating a PW of correct length
yes | python3 ezpass.py -f testfile -cp bob -l 4
# Change password with specified password
#! TODO: consider how to determine if prog creating correct PW
yes | python3 ezpass.py -f testfile -cp bob -sp
# Get password, printing to screen
yes | python3 ezpass.py -f testfile -g bob -print
#! Delete account
yes | python3 ezpass.py -f testfile -d bob

rm testfile

echo "Done running tests"