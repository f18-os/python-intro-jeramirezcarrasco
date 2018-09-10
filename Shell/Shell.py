#Jorge Ramirez Carrasco
#9/10/2018
#Theory of Operating Systems

import os, sys, time, re

pid = os.getpid()

os.write(1, ("Initial pid is (pid:%d)\n" % pid).encode())

while 1:
    Command = input("Write wanted command\n")
    Command = Command.split()
    if Command[0] == "exit" or Command[0] == "Exit":
        sys.exit(1)
    elif Command [0] == "wc" or Command[0] == "WC":
        if len(Command) > 2 and Command[1] == "<":
            os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
            rc = os.fork()
            if rc < 0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)

            elif rc == 0:  # child
                os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                             (os.getpid(), pid)).encode())
                args = ["wc", Command[2]]
                if len(Command) > 3 and Command[3] == ">":
                    os.close(1)  # redirect child's stdout
                    sys.stdout = open(Command[4], "w")
                    fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                    os.set_inheritable(fd, True)
                    os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

                    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
                        program = "%s/%s" % (dir, args[0])
                        try:
                            os.execve(program, args, os.environ)  # try to exec program
                        except FileNotFoundError:  # ...expected
                            pass
                else:
                    for dir in re.split(":", os.environ['PATH']):
                        program = "%s/%s" % (dir, args[0])
                        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
                        try:
                            os.execve(program, args, os.environ)
                        except FileNotFoundError:
                            pass

                os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
                sys.exit(1)
            else:
                os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                             (pid, rc)).encode())
                childPidCode = os.wait()
                os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                             childPidCode).encode())
        else:
            print("command not found, write help for available commands")
    elif Command [0] == "Help" or Command [0] == "help":
        print("WC for word count\n")
        print("< to specify input\n")
        print("> to specify output\n")
        print("Exit for exit\n")
    else:
        print("command not found, write help for available commands")



