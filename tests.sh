  #!/bin/bash

  echo "Running tests..."

  python3 passman.py -f testfile -nf
  python3 passman.py -f testfile -na bob
  python3 passman.py -f testfile -cp bob

  rm testfile

  echo "Done running tests"