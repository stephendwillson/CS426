import os
import sys
import signal
import glob
import string

import zac

def execute(args):
    pid = os.fork()
    
    try:
        if pid==0: #if child, execute whatever
        
            globindex = None
            for i,x in enumerate(args): #check for '*'
                if contains(args[i],"*"):
                    globindex = x
                    
            if len(args) > 1 and args[1][0]=='$':
                args[1] = os.environ[args[1][1:]]
            try: #catch things like 'ls &', removes & from arguments when executed
                if globindex != None: #filename expansion execute
                    globlist = glob.glob(globindex)
                    args+=globlist
                    args.remove(x)
                    os.execvp(args[0],args)
                elif args[len(args)-1] != '&': #normal execute
                    os.execvp(args[0],args)
                else: #don't pass '&' as an argument
                    os.execvp(args[0],args[:len(args)-1])
            except OSError,e:
                print e
                sys.exit();
        else: #if parent, wait for kid to die, unless args ends with '&'
            if args[len(args)-1] != '&':
                os.waitpid(pid,0)
    except KeyboardInterrupt:
        if pid==0:
            sys.exit()
        else:
            os.waitpid(pid,0)

        
def cd(args):
    globl=None
    try:
        if len(args) > 1:
            if contains(args[1],"*"):
                globl = glob.glob(args[1])
                if len(globl) > 1:
                    dircount=0
                    for x in globl:
                        if os.path.isdir(x)==True:
                            dircount+=1
                            isdir=x
                    if dircount > 1:
                        print "More than one relevant folder"
                        return
                    elif dircount==1:
                        os.chdir(isdir)
            else:
                if args[1][0]=="$":
                    os.chdir(os.environ[args[1][1:]])
                else:
                    os.chdir(args[1])
        else:
            print "Must specify a directory."
    except OSError,e:
        print e
        
def setEnv(env):
    os.environ[env[0]]=env[1]   

def contains(str,set):
    for i in set:
        if set in str:
            return True
    return False
