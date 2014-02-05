import zac
import steve

import readline
import os
import re
import sys
import glob

def main(command):
    queue = re.compile(r' ; ')
    if command == '':
	    return
    elif command=="exit":
        sys.exit(0)
    elif command[0] == ".":
	    file = open(command[2:], 'r')
	    inp = re.compile(r'\n').split(file.read())
	    for x in inp:
		    if x != "":
			    main(x)
    elif queue.search(command) != None: #somewhere in command is ' ; '
        inp = queue.split(command)
        for x in inp:
	        if x != "":
		        main(x)
    else:
        n = readline.get_current_history_length()
        while command[0] == '!':
            if command[1:] == 'l':
                newCommand = readline.get_history_item(n-1)
                if newCommand != command:
                    command = newCommand
                else:
                    print "There are no more commands"
                    return
            elif int(command[1:]) < 1 or int(command[1:]) >= n:
                print 'invalid input'
                return
            else:
                newCommand = readline.get_history_item(int(command[1:]))
                if newCommand != command:
                    command = newCommand
                else:
                    print 'There are no more commands'
                    return
        zac.parse(command)

readline.get_line_buffer()
readline.parse_and_bind("tab: complete")

username=os.getenv("USERNAME")
prompt="$"

while(True):
    try:
        workdir=os.getcwd()
        command=raw_input(username + ": " +workdir+ "\n  " +prompt+ " ")
        command=command.strip()
        try:
            if command[0:4] == 'PS1=':
                prompt=command[4:]
                if prompt[0] == '$':
                    prompt = os.environ[prompt[1:]]
            else: 
                main(command)
        except Exception as e:
            print e
    except KeyboardInterrupt:
        print '\n'
        continue
