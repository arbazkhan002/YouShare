import os, struct, sys, commands, copy
import glob
import stat
from time import sleep
import socket
import string
import pickle
import copy

'''
How it works:
Users can upload files to the server by two methods:
-By browser
-By their disk synced folder
Changes done to the synced foldr in the disk are reflected
as it is on the server. So the same user can download files to some 
other computers which are exactly same as they were on his
disk synced folder
Uploads via browser at the server are synced with the disk folder
so that user can also upload files from other computers and the uploads 
can then be seen on his own computer
Shared folders which are empty are deleted while synicing from server
i.e. Empty Links are deleted.. I think should be changed 

**Changed : In logs.txt dont put a trailing '/' in directories
 '''

######################### GLOBAL VARIABLES #############################
##################### defined in the code itself #######################
#	USERNAME			eg: mayank
#	USERDIR_ADDR		eg: users/mayank
#	LOGFILE_ADDR		eg: logs/mayank.txt
SHARED_PICKLE_ADDR = "share_log.pkl"
		
########################### CODE STARTS ##################m##############

Connects=[]				#Connections active
#hashes={}
def converter(path):			# Converts Sync/a.txt to users/mayank/a.txt
	return USERDIR_ADDR + path[4:]
	
def reverse_converter(path):	# Converts users/mayank/a.txt to Sync/a.txt
	return ( "Sync" + path[len(USERDIR_ADDR):] )

def list_files(path, file_array, dir_array):
	pass
	temp = glob.glob(path+"*")				# lists all the files and folderss in the path folder.
	for i in temp:
		if not os.path.isdir(i):
			file_array.append(i)
		else:
			dir_array.append(i+os.path.sep)
			list_files(i+os.path.sep,file_array, dir_array)
	
def create_path(data):
	path=os.path.split(data)
	if path[0]:
		if not os.path.exists(path[0]):
			create_path(path[0])
			os.mkdir(path[0])
			os.chmod(path[0],stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
def send_file(client_socket,i):		#i is path of the file
	#i="Sync"+os.path.sep+"sword.mp3"
	#client_socket.sendall("Size")
	#client_socket.sendall(os.path.getsize(i))
	#client_socket.sendall(i)	#was part of simple one file transfer
	
	try:
		size=os.path.getsize(i)
		print "STARTED"
		a = open(i,"rb")
		print "STARTED"
		a = open(i,"rb")
		sent=0;
		reply=''
		client_socket.sendall("Fine.")
		print "fine sent"
		client_socket.recv(10)
		client_socket.settimeout(None)		#As make it wait sufficiently, message WILL arrive from server
		while(1):
			string = a.read()
			print "sending" , len(string)
			sent=client_socket.sendall(string)	# Here, I am sending the 2044 bytes string, with an ack "asdf" before it.	
			while(reply!="##\n"):
				print reply
				reply=client_socket.recv(4)
			if not string:	break
				#sleep(0.4)
		a.close()
		print "FINISHED SENDING", reply	
	except OSError:
		client_socket.sendall("No file. Sorry.")
		print "sorry sent"
		client_socket.recv(10)	
	
def recv_file(client_socket,data):		#receives files tested
	#data = client_socket.recv(2048)
	#print data
	print "STARTED"
	stat = client_socket.recv(20)
	if (stat=="Fine."):
		client_socket.sendall('OK.')
	elif (stat == "No file. Sorry."):
		client_socket.sendall("NOK.")
		if (os.path.isfile(data)):
			os.remove(data)
		return
	
	client_socket.settimeout(0.1)
	create_path(data)
	a = open(data,"wb")
	while(1):				# looping to get packets.
		try:
			data = client_socket.recv(2048)
			print "Writing data", len(data)
			if not data:
				#client_socket.send("zero recieved.")	# mdchecksum will come here.
			#	print "zr"
				a.close()
				break
			a.write(data)
			client_socket.sendall("wait")
		except socket.timeout:
			print "timing out"
			a.close()
			break		
			
	client_socket.sendall("##\n")	# mdchecksum will come here.
	print "FINISHED RECEIVING"
	
def md5sum(path):	
	##Computing the check sum at one end
	newpath=''
	for i in path:
		if i==" ":
			newpath+='\\'
		newpath+=i
	#	print "as %si %s" % (i,newpath)	
	if path.find(' ')==-1:
		string="md5sum %s" % (newpath)
	else:	
		string = "md5sum %s" % (newpath )
		
	print 'string is',string, newpath	
		
	cmd = os.popen(string,"r")

	while 1:
		line = cmd.readline()
		if not line: break
		return line.split()[0]
		
def dumpConnects():
	while Connects:
		pid = os.waitpid(0, os.WNOHANG)[0]
		if not pid: break
		if pid in Connects:
			Connects.remove(pid)
			


def recv_msg(client_socket):
	#data = client_socket.recv(2048)
	print data
	#client_socket.settimeout(2)
	#a = open(data,"wb")
	while(1):				# looping to get packets.
		try:
			data = client_socket.recv(2048)
			print "Writing data", len(data)
			if not data:
				#client_socket.send("zero recieved.")	# mdchecksum will come here.
			#	print "zr"
		#		a.close()
				break
		#	a.write(data)
		#	client_socket.sendall("wait")
		except socket.timeout:
			break		
	#client_socket.sendall("##")	# mdchecksum will come here.



def sync_ker_server(client_socket,Path,array):
	print "********** In sync_ker_server ************"
	
	# Preparing a list of all the non-dir files anywhere in Path.
	file_array = []							# the list that saves all the files.
	dir_array = []							# the list that saves all the directories.
	list_files(Path, file_array, dir_array)
	dir_array.sort()
	dir_array.reverse()
	print file_array
	print dir_array	
	
	while(1):
		print "At root "
		#sleep(2)
		data=0
		tobedeleted=0
		client_socket.settimeout(None)
		#while not data:
		data = client_socket.recv(1024)
		print "data read ", len(data)
		#sleep(1)
		print "At root "#, data
		if 1:
			if data == "Sync_End in this folder":
				break		
			if data[:12] == ".Directory: ":					# we've been notified of a Directory. Create this directory so that making files directory can be easy.
				print "directory incoming. data is-", data
				dir_tory = data[12:]
				dir_tory = converter(dir_tory)
				
				fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
				hashes = pickle.load(fd)				# .
				print hashes
				fd.close()
				if not os.path.isdir(dir_tory):
					if dir_tory not in hashes.keys():
						print 'making'	
						os.mkdir(dir_tory)						# created the directory, if no directory was there originally.
						os.chmod(dir_tory,stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
					else:	
						print 'Said delete'
						tobedeleted=1
							
				else:
					print "mayank says bla bla bla"
					dir_array.remove(dir_tory)				# removed the directory from the listing if we have this directory in the client file structure.
				
				print "roger sent from server"			
				
				if dir_tory in hashes.keys():
					print "already in hashes"
					pass
				else:
					print "creating new dictionary entry.", dir_tory
					hashes[dir_tory] = ['1','1']	# each key stores a 2-member array.	#########################check.
					fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
					pickle.dump(hashes,fd)					# .
					fd.close()								# .
			
				if not tobedeleted:
					print 'Roger'
					on=client_socket.send("Roger!")
				else:
					print 'Cut sent'
					on=client_socket.send("Cut!")	
				#s=client_socket.recv(512)	#receive ack	 
			elif data[:6]=="File :":	# this(data) is the address of a file.
				print "sending ack"
				client_socket.sendall("aye")
				data_read=data[6:]
				print "file incoming. data is-", data_read
				data_read = converter(data_read)			# now, data_read is the address of the file here.
				if data_read:
					print "Yes it is"
					hashsum='0'
					isitlink = 0							# 0 if it is not link, 1 if it is a link.
					if data_read in file_array:				# the server has this path.
						file_array.remove(data_read)		# removing the file from the list if it has come. Even if it is updated, we need to do this.
						hashsum=md5sum(data_read)
						if not (os.path.realpath(data_read) == os.path.abspath(data_read)):		# if it is a link
							print "link obtained."
							isitlink = 1
							print "isitlink is..", isitlink
						else:					# it is not a link
							print "not a link."
							print "isitlink is..", isitlink
					hashsum_client=client_socket.recv(32)	#Check for hashsum value to note the changes
					synced='0'
					print 'Well, You know what : client', hashsum_client, 'server ',hashsum, md5sum(data_read)
					print hashsum_client==hashsum
					if (hashsum_client==hashsum):
						synced='1'	
					if (isitlink == 1):
						fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
						hashes = pickle.load(fd)				# .
						print hashes
						fd.close()								# .
						if data_read in hashes.keys():
							print "already in hashes"
							pass
						else:
							print "creating new dictionary entry.", data_read
							hashes[data_read] = [hashsum,hashsum]	# each key stores a 2-member array.	#########################check.							
							f=[]
							d=[]
							list_files("",f,d)	
							flag=0
							print ' ******$$$$***** f is with filearray ****$$$$******', f, '\n'
							
							for j in f:
								print 'Searching for j ', j
								#print os.path.realpath(x), os.path.abspath(j)
								if os.path.realpath(data_read) == os.path.abspath(j):		#Find the target of the link
									flag=1
									print 'We caught you ', j
									break
							
							#sleep(4)
							if (flag==1) and (j not in hashes.keys()):
								 hashes[j]=[hashsum, hashsum]
							fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
							pickle.dump(hashes,fd)					# .
							fd.close()								# .
							
						fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
						hashes = pickle.load(fd)				# .
						fd.close()								# .
						hashes[data_read][1] = hashsum
						fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
						pickle.dump(hashes,fd)					# .
						fd.close()								# .
					
					'Dont be afraid by the redundancy here, its meant for just the master link'
					
					fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
					hashes = pickle.load(fd)				# .
					fd.close()

					if data_read in hashes.keys():				#This is where we need to treat the case when not a link but in hashes.keys() i.e. master target
						hashes[data_read][1] = hashsum
						fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
						pickle.dump(hashes,fd)					# .
						fd.close()						
						if (hashes[data_read][0] == hashes[data_read][1] == hashsum_client):
							synced = '1'						# synced = 1, that is, do nothing
							print "setting synced as 1. No change to be done."
						elif (hashes[data_read][0] == hashsum_client):
							synced = '2'						# synced = 2, that is, send_file
							print "setting synced as 2. Sending file back from server."
						elif (hashes[data_read][1] == -1):
							synced = '4'						# signal client to delete the file.
							print "setting synced as 4. signal the client to delete the file."
						else:
							synced = '3'
							print "setting synced as 3. Recieving file from client."
							
					fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
					hashes = pickle.load(fd)				# .
					print '************************************'
					print hashes, data_read
					fd.close()								# .		
					if data_read in hashes.keys():
						if (hashes[data_read][1] == '-1'):
							synced = '4'						# signal client to delete the file.
							print "setting synced as 4. signal the client to delete the file."
					fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
					pickle.dump(hashes,fd)					# .
					fd.close()								# .
						
					
					client_socket.sendall(synced)
					print "data is ", data_read	, hashsum_client==hashsum , '\n synced: ', synced
					if (synced=='0' or synced == '3'):							#Skippping unchanged files
						recv_file(client_socket,data_read)
					if (synced=='3'):
						fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
						hashes = pickle.load(fd)				# .
						fd.close()								# .
						hashes[data_read][0] = hashsum_client
						hashes[data_read][1] = hashsum_client
						fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
						pickle.dump(hashes,fd)					# .
						fd.close()								# .
					if (synced=='2'):
						############ send file first.
						# recv ack
						# send_file
						# send ack
						if not (client_socket.recv(20) == "commence sending"):
							print "error in recieving ack."
							exit(0)
						send_file(client_socket,data_read)			
						client_socket.sendall("Thanks.")
						############ file sent.
						fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
						hashes = pickle.load(fd)				# .
						fd.close()								# .
						hashes[data_read][0] = hashes[data_read][1] 
						fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
						pickle.dump(hashes,fd)					# .
						fd.close()								# .
						
			else:
				continue
	
		else: #except IOError:
			print "Error receiving files "
			return			
	
	
	print "\n&&&^^^ while loop over. starting logfile code. ^^^&&&\n"
	
	print "FILE ARRAY IS:", file_array
	print "DIR ARRAY IS:", dir_array
	
	global LOGFILE_ADDR
	LOGFILE_ADDR = "logs" + os.path.sep + USERNAME + ".txt"
	f=open(LOGFILE_ADDR,"r")
	lines=f.read().split()
	f.close()
	start=md5sum(LOGFILE_ADDR)
	changes=[]	
	for i in file_array:												# deleting all those files we do not have a record of.
		print "checking for extra files in server: ", i, lines, file_array
		if i in lines:
			print "yes sending ","YES "+i
			client_socket.sendall("YES "+reverse_converter(i))
			response=client_socket.recv(8)								#Just so that we alternate between send and receive
			print 'received', response
			send_file(client_socket,i)		
			print "Lets send " , lines
			changes.append(i)
			print 'just then', lines, dir_array
			temp=copy.deepcopy(dir_array)
			for dir_tory in temp:										#Remove from the dir_array the directory pertaining to this file as else it would be unwantedly
				print 'Compares', dir_tory, dir_tory in i						#deleted later
				if dir_tory in i:
					print 'there u r mydir'
					dir_array.remove(dir_tory)
					print 'it became',dir_array
				print 100	
			lines.remove(i)		
		
		else:
			print 'abs : ', os.path.abspath(i)	#, 'rel',os.path.realpath(i)
			condition=0
			
			fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
			hashes = pickle.load(fd)				# .
			fd.close()								# 	
			
			for j in hashes.keys():
				print "Get j: ", j, os.path.realpath(j), os.path.realpath(j) in os.path.abspath(i)	, (os.path.abspath(i)==os.path.realpath(i))
				#You have the realpath of some link surely as hashes contains all directories as well
				if os.path.realpath(j) in os.path.abspath(i):
					print 'in t'
					if not os.path.abspath(j)==os.path.realpath(j):
						print 'now set'	
						condition=1	
			print "condition is ", condition		
			if (not os.path.abspath(i)==os.path.realpath(i)) or (condition == 1) :					#if a link
				fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
				hashes = pickle.load(fd)				# .
				fd.close()	
				print "Before deleting",  i, " \n hashes : ", hashes, '\n\n\t',i in hashes.keys()
				if not i in hashes.keys():									# file not in hashes but still a link => not read by client, so send	
					print "yes sending ","YES "+i
					client_socket.sendall("YES "+reverse_converter(i))
					response=client_socket.recv(8)								#Just so that we alternate between send and receive
					print 'received', response
					send_file(client_socket,i)		
					print "Lets send " , lines
					changes.append(i)
					print 'just then', lines, dir_array
					temp=copy.deepcopy(dir_array)
					for dir_tory in temp:										#Remove from the dir_array the directory pertaining to this file as else it would be unwantedly
						print 'Compares', dir_tory, dir_tory in i						#deleted later
						if dir_tory in i:
							print 'there u r mydir'
							dir_array.remove(dir_tory)
							print 'it became',dir_array
						print 100	
					#lines.remove(i)		

				else:													#Comes here when read by client, but at present not with client => deleted by client
					os.remove(i)					
					
					
			else:														#In case you have a folder in logs but not the file
				flag=0
				for j in lines:
					if j in i:
						flag=1
						print 'flag set', flag
						print "yes sending ","YES "+i
						client_socket.sendall("YES "+reverse_converter(i))
						response=client_socket.recv(8)						#Just so that we alternate between send and receive
						print 'received', response
						send_file(client_socket,i)		
						print "Lets send " , lines
						changes.append(i)
						print 'just then', lines, dir_array
						temp=copy.deepcopy(dir_array)
						for dir_tory in temp:								#Remove from the dir_array the directory pertaining to this file as else it would be unwantedly
							print 'Compares', dir_tory, dir_tory in i						#deleted later
							if dir_tory in i:
								print 'there u r mydir'
								dir_array.remove(dir_tory)
								print 'it became',dir_array
							print 100	
						lines.remove(j)	
																	#below statements reqd if u want to reflect the changes of deleting the shared file
				'''if os.path.abspath(i)!=os.path.realpath(i):
					if not os.islink(i):
						os.remove(i)
					else:				#You cant delete a master link directly as the changes wont be reflected	
						f=open("i","wb")
						f.write("")
						f.close()
						os.remove(i)'''
				print 'value of flag', flag												
				if not flag:
					os.remove(i)			
	print 'I have', lines, string.join(lines), "dirs", dir_array 
	if start!=md5sum(LOGFILE_ADDR):
		f=open(LOGFILE_ADDR,"r")
		lines=f.read().split()
		f.close()
		for line in lines:
				if line in changes:	lines.remove(i)
	f=open(LOGFILE_ADDR,"w")		
	f.write(string.join(lines,'\n'))
	f.close()	
	start=md5sum(LOGFILE_ADDR)
	f=open(LOGFILE_ADDR,"r")
	lines=f.read().split()
	f.close()
	dir_array.sort()
	dir_array.reverse()
	
	print " **************** CHECK TO DELETE  ************************"
	
	for i in dir_array:
		print "i is " , i
		if i in lines:
				client_socket.sendall("YES "+reverse_converter(i))
				response=client_socket.recv(8)							#Just so that we alternate between send and receive
				print 'NOT A LINK TO USER ' , response 
				lines.remove(i)
				continue
				
		print 'abs : ', os.path.abspath(i)	#, 'rel',os.path.realpath(i)
		condition=0
		for j in hashes.keys():
			print "j: ", j, os.path.realpath(j), os.path.realpath(j) in os.path.abspath(i)	, (os.path.abspath(i)==os.path.realpath(i))
			#You have the realpath of some link surely as hashes contains all directories as well
			if os.path.realpath(j) in os.path.abspath(i):
				print 'in t'
				if not os.path.abspath(j)==os.path.realpath(j):
					print 'now set'	
					condition=1			
			
		if not (os.path.abspath(i)==os.path.realpath(i)) or condition==1:
			fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
			hashes = pickle.load(fd)				# .
			fd.close()								# .
					
			if not (i in hashes.keys()):									#directory not read by client even once
				client_socket.sendall("YES "+reverse_converter(i))
				response=client_socket.recv(8)							#Just so that we alternate between send and receive
				print 'SENT TO USER' , response 	
				continue
				
		print "\t\t**********SKIPPED EVERYTHING******"		
		path=os.path.split(i)[0]
		print i,'path is ', path
		if os.path.islink(path):										#Sync/dir/ not accepted, need Sync/dir
			newpath=''
			for j in path:
				if j==" ":
					newpath+='\\'
				newpath+=j
			i=newpath
			print i
			print "removing extra directories from server: ", i
			cmd='rm %s' % (i)
			commands.getoutput(cmd)	
		else:	
			os.rmdir(i)
	if start!=md5sum(LOGFILE_ADDR):
		f=open(LOGFILE_ADDR,"r")
		lines=f.read().split()
		f.close()
	for line in lines:
			if line in changes:	lines.remove(i)
	f=open(LOGFILE_ADDR,"w")		
	f.write(string.join(lines,'\n'))
	f.close()		
	client_socket.sendall("Over")
	
	#global hashes
	############# deleting entry from pkl file if shortcut has been deleted. ############
	
	
	fd = open(SHARED_PICKLE_ADDR,"rb")		# code for reading from file.
	hashes = pickle.load(fd)				# .
	print "####### MY DICT ######", hashes
	fd.close()	
	hashlist=copy.deepcopy(hashes.keys())							# .
	for i in hashlist:
		if 'users/'+USERNAME in i:
			if not os.path.isfile(i):
				print " deleting entry from pkl file coz shortcut has been deleted:", i
				for j in hashlist:
					#print 'j is', j
					if os.path.realpath(j)== os.path.realpath(i):
						print 'same links' , j
						hashes[j][1] = '-1'		# next time, delete the file
				if not os.path.exists(i):							
					del hashes[i]
	print hashes			
	fd = open(SHARED_PICKLE_ADDR,"w")		# code for writing to the file.
	pickle.dump(hashes,fd)					# .
	fd.close()								# 
	
	
	
	############# deleted entries ##############
	print "Synced. Now waiting for 20 seconds!"
	sleep(30)	# wait before you sync further!

def main():
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Port = 5028

	# reusable socket code. (Free the port) I dont have this line of code. :/

	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("", Port))
	server_socket.listen(3)												# it can only listen to 1 incoming connection at a time. :)
	
	
	global hashes
	hashes={}
	fd = open(SHARED_PICKLE_ADDR,"wb")		# code for writing to the file.
	pickle.dump(hashes,fd)					# .
	fd.close()
	
	
	
	Id=os.fork()	
	if(not Id):
		print "Hello World! "
		print commands.getoutput("python as_client.py")		
	else:
		while 1:
			print "TCPServer Waiting for client on port", Port
			client_socket, address = server_socket.accept()
			dumpConnects();													#dump exited processes
			pid=os.fork()
			if(not pid):
				# waiting for connection.
				server_socket.close()
				print "I got a connection from ", address
				# connected! :)

				#	data = client_socket.recv(2048)
				#	size = client_socket.recv(2048)

				'''data = client_socket.recv(2048)
				recv_file(client_socket,data)
				client_socket.close()'''
				global USERNAME
				global USERDIR_ADDR
				data = client_socket.recv(30)									# first, getting name from client.
				if ( (data[:5] == "Name:") and (os.path.isdir("users"+os.path.sep+data[5:])) ):
					USERNAME = data[5:]
					USERDIR_ADDR = "users" + os.path.sep + USERNAME 			# in which data is to be saved.
					print "Username recieved:", USERNAME
					print "Ack sent"
					client_socket.send("Ack")
				else:
					print "Data is", data
					print "Nack sent"
					client_socket.send("Nack")
					client_socket.close()
					print "Socket closed."
					exit(0)
				print "Will sync endlessly."
				
				while (1):
					array = []												# the array that tells all the files or dirs in a dir.
					Path = USERDIR_ADDR + os.path.sep						# This depends on the user that has logged in now.
					
					print " \n ************* On a loop again ****************** \n"
					
					try:
						data = client_socket.recv(512)
						if ( data == "Lets sync." ):
							print "RECIEVED:" , data
							client_socket.send("Proceed sync.")
							sync_ker_server(client_socket,Path,array)	
							continue										# start recieveing again, as in sync_ker(), we had sent the last packet.
						else:
							print "RECIEVED:" , data
							if not data: raise socket.error
																			#client_socket.send("random message obtained")
					
					except socket.error:
						print "Client disconnected"
						client_socket.close()
						break
				exit(0)		
			else:
				Connects.append(pid)
				client_socket.close()			
		
if __name__ == '__main__':
  main()
