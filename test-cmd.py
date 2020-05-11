import cmd, sys

class PassShell(cmd.Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '(turtle) '
    file = None

    # ----- basic turtle commands -----
    def do_account_create(self, arg):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        print(arg)

    def do_right(self, arg):
        'Turn turtle right by given number of degrees:  RIGHT 20'
        print(arg)

if __name__ == '__main__':
    sh = PassShell()
    sh.cmdloop()