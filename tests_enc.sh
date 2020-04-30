  #!/bin/bash

  echo "Running tests..."

#! TODO: add -e encrypted flag to relevant commands
#! TODO: enter pw manually when prompted, or pipe in pws from another file

# Create new file
  python3 passman.py -f testfile -nf
# Create new account
  python3 passman.py -f testfile -na bob
# Get password for account
  python3 passman.py -f testfile -g bob
# Change password, specifying password length
#! TODO: check below - how do I know if it's creating a PW of correct length?
  python3 passman.py -f testfile -cp bob -l 4
# Change password with specified password
#! TODO: check below - how do I know if it's creating correct PW?
  python3 passman.py -f testfile -cp bob -sp 8080boat
# Get password, printing to screen
  python3 passman.py -f testfile -g bob -print
#! Delete account
  python3 passman.py -f testfile -d bob

  rm testfile

  echo "Done running tests"