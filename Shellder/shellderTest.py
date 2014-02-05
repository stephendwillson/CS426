import os
import re
import steve
import zac

def parse(command):
	pattern = re.compile(r'\s')
	pathPattern = re.compile(r'=')
	if pathPattern.search(command) != None:
		return pathPattern.split(command)
	return pattern.split(command)
def printTest(test):
	print "\nend test",test," \n"

#executing programs
steve.execute(parse("ls -l"))
printTest(1)
steve.execute(parse("/bin/ls"))
printTest(2)
steve.cd(parse("cd /home/"))
printTest(3)
steve.execute(parse("/bin/ls"))
printTest(4)

#changing directories
steve.cd(parse("cd /home"))
print os.getcwd()
printTest(5)
#change the next one to fit your system
steve.cd(parse("cd /home/swillson/Documents/"))
print os.getcwd()
printTest(6)

#setting environment variables
#save the current PATH variable to set it back later
currentPath = os.environ['PATH']
print currentPath
steve.setEnv(parse("PATH=:/bin:/sbin:/usr/sbin:/usr/bin"))
print os.environ['PATH'],"\n"
printTest(7)
steve.setEnv(['PATH',currentPath])
print os.environ['PATH'],"\n"
printTest(8)

#expand environment variables
#will be called from in other methods later
print steve.expandEnv('$HOME')
printTest(9)

#not sure how to write a test for keyboard interrupt, tabs/arrows,
	#queue/& commands, and bg(background).  it's up to you to find 
	#a way to test them.  what might help with bg and interrupt is
	#to make a short program the infinity loops
