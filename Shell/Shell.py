#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()


def Command_List(Command , Command_Line):

    if Command == "exit":
        sys.exit(0)
    elif Command == "help":

        print("wc for word count\n")
        print("cat to print file\n")
        print("echo to repeat word\n")
        print("ls for all the files in a path\n")
        print("< need to always follow the first command\n")
        print("> to specify output\n")
        print("| for piping\n")
        print("exit to exit\n")

    else:
        Exec1(Command, Command_Line)


def Command_List2(Command , Command_Line):

    Exec2(Command, Command_Line)

def Redirects(Command_Line, args):
    if Command_Line[0] == ">":
        There_string(Command_Line[1:], args)
    elif Command_Line[0] == "|":
        Pipe_String(Command_Line[1:], args)
    else:
        os.write(2, ("command not found, write help for available commands\n".encode()))
        sys.exit(1)

def Exec1(Command , Command_Line):
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:  # child
        if len(Command_Line) > 1 and Command_Line[0] == "<":
            Here_string(Command, Command_Line[1:])
        if len(Command_Line) > 1 :
            Here_string(Command, Command_Line)
        elif len(Command_Line) == 1:
            args = [Command, Command_Line[0]]
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execv(program, args)
                except FileNotFoundError:
                    pass
            os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
            sys.exit(1)
        elif len(Command_Line) == 0 and (Command !="cat" and Command != "wc" and Command != "cd" and Command != "mv" and Command != "cp"):
            args = [Command]
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execv(program, args)
                except FileNotFoundError:
                    pass
            os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
            sys.exit(1)
        else:
            os.write(2, ("Missing file input\n".encode()))
    else:  # parent (forked ok)
        childPidCode = os.wait()

def Exec2(Command , Command_Line):
    if len(Command_Line) > 1 and ((Command_Line[1] == ">" or Command_Line[1] == "|")):
        args = [Command, Command_Line[0]]
        Redirects(Command_Line[1:], args)
    else:
        args = [Command]
        for dir in re.split(":", os.environ['PATH']):  # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass
        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)




def Here_string(Command , Command_Line):
    args = [Command, Command_Line[0]]
    if len(Command_Line) > 1 :
        Redirects(Command_Line[1:], args)
    else:
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execv(program, args)
            except FileNotFoundError:
                pass

    os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
    sys.exit(1)


def There_string(Command_Line, args):
    os.close(1)  # redirect child's stdout
    sys.stdout = open(Command_Line[0], "w")
    fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
    os.set_inheritable(fd, True)
    os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execv(program, args)  # try to exec program
        except FileNotFoundError:  # ...expected
            pass

    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)

def Pipe_String(Command_Line, args):
    pr, pw = os.pipe()
    for f in (pr, pw):
        os.set_inheritable(f, True)
    fc = os.fork()
    if fc == 0:
        os.close(0)  # redirect child's stdout
        fdzero = os.dup(pr)
        for fd in (pw, pr):
            os.close(fd)
        sys.stdout = os.fdopen(fdzero)
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)
        Command_List2(Command_Line[0], Command_Line[0:])
        sys.exit(1)  # terminate with error

    else:
        os.close(1)
        d = os.dup(pw)
        os.set_inheritable(d, True)
        for fd in (pr, pw):
            os.close(fd)
        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execv(program, args)  # try to exec program

            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

    os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
    sys.exit(1)



while 1:
    Command = input("$\n")
    Command = Command.split()
    Command_List(Command[0],Command[1:])




