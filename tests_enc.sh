#!/bin/bash

####################
# Integration tests that manipulate ezpass in encrypted mode
####################

echo "Running tests..."

# Create new file
yes | python3 ezpass.py -f testfile -nf -e

# Create new account
yes | python3 ezpass.py -f testfile -no bob -e
# Get password for account
yes | python3 ezpass.py -f testfile -g bob -e
# Change password, specifying password length
#! TODO: consider how to determine if prog creating a PW of correct length
yes | python3 ezpass.py -f testfile -cp bob -l 4 -e
# Change password with specified password
#! TODO: consider how to determine if prog creating correct PW
yes | python3 ezpass.py -f testfile -cp bob -sp 8080boat -e
# Get password, printing to screen
yes | python3 ezpass.py -f testfile -g bob -print -e
#! Delete account
yes | python3 ezpass.py -f testfile -d bob -e

rm testfile

echo "Done running tests"