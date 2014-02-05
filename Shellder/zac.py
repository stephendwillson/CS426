import steve
import re
import os
import sys

def parse(command):
	executePattern = re.compile(r'\s')
	pathPattern = re.compile(r'=')
	redirectPattern = re.compile(r'\s[<|>]\s')
    
	if pathPattern.search(command) != None:
		args = pathPattern.split(command)
		steve.setEnv(args)
	elif redirectPattern.search(command) != None:
		redirect(command,redirectPattern,executePattern)
	else:
		args = tildeReplace(executePattern.split(command))
		if args[0]=="cd":
		    if len(args) < 2:
		        print 'Invalid syntax: must provide an argument.'
		        return
		    else:
		        steve.cd(args)
		else:
			steve.execute(args)
		
def redirect(command,pattern,executePattern):
	operators = pattern.findall(command)
	commands = tildeReplace(pattern.split(command))
	if len(operators) == 1:
		args = executePattern.split(commands[0])
		if not os.access(findPath(args[0]), os.X_OK):
			print args[0]+': command not found'
			return	
		elif operators[0] == " > ":
			fdOrig = os.dup(1)
			fd = os.open(commands[1], os.O_WRONLY|os.O_TRUNC|os.O_CREAT)
			os.dup2(fd, 1)
			steve.execute(args)
			os.dup2(fdOrig,1)
		elif operators[0] == " < ":
			fdOrig = os.dup(0)
			fd = os.open(commands[1], os.O_RDONLY)
			os.dup2(fd, 0)
			steve.execute(args)
			os.dup2(fdOrig,0)
		elif operators[0] == " | ":
			piping(commands,executePattern)
	elif len(operators) == 2:
		if operators == [" | ", " > "]:
			piping(commands,executePattern)
		else:
			print 'Unsupported'
			return
	else:
		print 'Unsupported'
		return
			
def piping(commands,executePattern):
	pid = os.fork()
	if pid == 0:
		args1 = tildeReplace(executePattern.split(commands[0]))
		args2 = tildeReplace(executePattern.split(commands[1]))
		if not os.access(findPath(args1[0]), os.X_OK):
			print args1[0]+': command not found'
			sys.exit()	
		if not os.access(findPath(args2[0]), os.X_OK):
			print args2[0]+': command not found'
			sys.exit()
		pipe = os.pipe()
		pid2 = os.fork()
		if pid2 > 0:
			os.close(pipe[1])
			file = []
			if len(commands) == 3:
				file = tildeReplace([commands[2]])
				fd = os.open(file[0], os.O_WRONLY|os.O_TRUNC|os.O_CREAT)
				os.dup2(fd,1)
			os.dup2(pipe[0],0)
			os.execvp(args2[0],args2)
			print 'exec failed: '
			sys.exit()
		elif pid2 == 0:
			os.close(pipe[0])
			os.dup2(pipe[1],1)
			os.execvp(args1[0],args1)
			print 'exec failed: '
			sys.exit()
		else:
			print 'Piping failed'
			sys.exit()
	else:
		os.wait()
		
def findPath(filename):
	paths = re.compile(r':').split(os.environ["PATH"])
	for x in paths:
		if os.access(x+"/"+filename, os.F_OK):
			return x+"/"+filename
	return filename
		
def tildeReplace(args):
	returnArgs = []
	for x in args:
		if x[0] == '~':
			returnArgs.append(os.getenv("HOME")+x[1:])
		else:
			returnArgs.append(x)
	return returnArgs
