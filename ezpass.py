"""
Main file for running ezpass. For more instructions, see repo's README:
https://github.com/jchenj/ezpass
"""

import shlex
import argparse
import cmd
import getpass
import os
import sys
import pprint

from util import *
from pwfile import PwFile
from account import Account

#! TODO - rename class to AcList?
#! TODO - take acname out of class?
#! TODO - rename acname to username?
#
# class AccountDB:
#     def __init__(self, pwfile: PwFile) -> None:
#         """
#         :param pwfile: PwFile instance
#         :param org: name of organization that account belongs to (e.g. Bank of America)
#         # :param acname: account name (cannot contain spaces, newlines or tabs)
#         """
#         assert pwfile is not None
#         self.pwfile = pwfile
#         # TODO read the pwfile,
#         # populate a local representation of the accounts
#         self.accounts = self.pwfile.readFile()
#
#     def get_account_pass(self, orgname):
#         # 1. find account with orgname
#         # 2. print/copy account's username/pass


class PassShell(cmd.Cmd):
    intro = 'Welcome to the ezpass interactive shell. Type "help" or "?" to ' \
            'list commands.\n'
    prompt = '(ezpass) '
    file = None

    def __init__(self, pfile):
        cmd.Cmd.__init__(self, 'tab', sys.stdin, sys.stdout)
        self.pfile = pfile

    # ----- basic ezpass commands -----
    # Must have pwfile before interactive mode can be used

    #! TODO improve docstrsing help for new_account
    def do_newac(self, line):
        """Add a new org: NEWAC --org-name --pw-length --set-acpass"""
        parser = argparse.ArgumentParser()
        parser.add_argument('-on', '--org-name', type=str, help='new org name')
        parser.add_argument('-pl', '--pw-length', type=int, required=False,
                            default=8, help='password length')
        parser.add_argument('-sp', '--set-acpass', action='store_true',
                            help='set specified password')
        args = parser.parse_args(shlex.split(line))

        if args.pw_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(self.pfile, args.org_name)
        print("Creating new account for:", args.org_name)
        acname = input("Enter username: ")
        account.create_new_account(acname, ALPHABET, args.pw_length)
        if args.set_acpass is not None:
            specified_pass = getpass.getpass(prompt="Enter password: ")
            account.set_acpass(specified_pass)
        print("Account created for:", args.org_name)

    def do_delac(self, line):
        """Delete account for specified org: DELAC --org-name"""
        parser = argparse.ArgumentParser()
        parser.add_argument('-on', '--org-name', type=str, help='org name')
        args = parser.parse_args(shlex.split(line))

        account = Account(self.pfile, args.org_name)
        account.delete_account()
        print("Deleted account for:", args.org_name)

    def do_getacpass(self, line):
        """Get password for specified org: GETACPASS --org-name --print"""
        parser = argparse.ArgumentParser(prog='getacpass')
        parser.add_argument('-on', '--org-name', type=str, help='org name',
                            required=True)
        parser.add_argument('-p', '--print', action='store_true',
                            help='print password to screen', required=False,
                            default=False)
        try:
            args = parser.parse_args(shlex.split(line))
            account = Account(self.pfile, args.org_name)
            account.get_password_from_file(args.print)
            if args.print is False:
                print("Password for org {} in paste buffer".format(args.org_name))
        except SystemExit as error:
            # catching parse_args errors
            return
        except:
            pprint.pprint(sys.exc_info())
            parser.print_help()
            return

    def do_chacpass(self, line):
        """Change password for specified org: CHACPASS --org-name set-acpass pw-length"""
        parser = argparse.ArgumentParser()
        parser.add_argument('-on', '--org-name', type=str, help='org name')
        parser.add_argument('-sp', '--set-acpass', action='store_true',
                            help='set specified password')
        parser.add_argument('-pl', '--pw-length', type=int, required=False,
                            default=8, help='password length')
        args = parser.parse_args(shlex.split(line))

        account = Account(self.pfile, args.org_name)
        if args.set_acpass is None:
            account.set_acpass_rand(ALPHABET, args.pw_length)
        else:
            specified_pass = getpass.getpass(prompt="Enter password: ")
            account.set_acpass(specified_pass)
        print("Password changed for account:", args.org_name)

    def do_quit(self, line):
        """Quit the program"""
        print("")
        print("Goodbye!")
        sys.exit(0)


def mainfunc():
    parser = argparse.ArgumentParser(description='Password manager')
    # required
    parser.add_argument('-f', '--file', type=str, help='file name', required=True)
    # choose one
    parser.add_argument('-g', '--get-acpass', type=str,
                        help='org name to get account password for')
    parser.add_argument('-no', '--new-org', type=str, help='new org name')
    parser.add_argument('-d', '--delete-account', type=str,
                        help='org to delete account for')
    parser.add_argument('-nf', '--new-file', action='store_true',
                        help='whether or not to create new file')
    parser.add_argument('-cp', '--change-acpass', type=str,
                        help='org to change password for')
    parser.add_argument('-sp', '--set-acpass', action='store_true',
                        help='whether or not to use specified password')
    # optional
    parser.add_argument('-print', '--print-to-screen', action='store_true',
                        help='print password to screen', required=False,
                        default=False)
    parser.add_argument('-l', '--password-length', type=int,
                        help='password length', required=False, default=8)
    parser.add_argument('--no-encrypt', default=False, action='store_true',
                        help='if specified, no encryption will be used')
    parser.add_argument('-a', '--alphabet', type=str, help='full alphabet',
                        required=False)
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='whether or not to use interactive mode')

    args = parser.parse_args()

    assert args.file is not None
    fname = args.file

    if args.no_encrypt:
        password = None
    else:
        # if file encrypted, new file requested & file already exists
        if args.new_file and os.path.isfile(fname):
            raise RuntimeError("File '{}' already exists".format(fname))
        password = getpass.getpass(prompt="Enter password for file {}: ".format(fname))

    print(args)

    get_acpass_int = int(args.get_acpass is not None)
    new_org_int = int(args.new_org is not None)
    delete_account_int = int(args.delete_account is not None)
    change_acpass_int = int(args.change_acpass is not None)
    new_file_int = int(args.new_file is True)
    interactive_int = int(args.interactive is True)
    param_sum = get_acpass_int + new_org_int + delete_account_int + \
                change_acpass_int + new_file_int + interactive_int
    if param_sum > 1:
        parser.print_help()
        raise RuntimeError("Error. Can only use one of these flags at a time")
    if param_sum == 0:
        parser.print_help()
        raise RuntimeError("Error. Must use --file and "
                           "at least one additional flag")

    if args.new_file is True:
        # negating no_encrypt to match semantics of 3rd param of create_new_file()
        PwFile.create_new_file(fname, password, not args.no_encrypt)
        print("New file created:", fname)
        return

    # Create PwFile instance based on file name & password
    # negating no_encrypt to match semantics of 3rd param of PwFile constructor
    pfile = PwFile(fname, password, not args.no_encrypt)

    if args.interactive is True:
        shell = PassShell(pfile)
        shell.cmdloop()
        return

    if args.get_acpass is not None:
        account = Account(pfile, args.get_acpass)
        account.get_password_from_file(args.print_to_screen)
        if args.print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(args.get_acpass))
    elif args.new_org is not None:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(pfile, args.new_org)
        print("Creating new account for:", args.new_org)
        acname = input("Enter username: ")
        account.create_new_account(acname, ALPHABET, args.password_length)
        if args.set_acpass is not None:
            specified_pass = getpass.getpass(prompt="Enter password: ")
            account.set_acpass(specified_pass)
        print("Account created")
    elif args.delete_account is not None:
        account = Account(pfile, args.delete_account)
        account.delete_account()
        print("Deleted account for:", args.delete_account)
    elif args.change_acpass is not None:
        account = Account(pfile, args.change_acpass)
        if args.set_acpass is None:
            account.set_acpass_rand(ALPHABET, args.password_length)
        else:
            specified_pass = getpass.getpass(prompt="Enter password: ")
            account.set_acpass(specified_pass)
        print("Password changed for account:", args.change_acpass)
    return


if __name__ == "__main__":
    mainfunc()
