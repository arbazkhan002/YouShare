import glob, stat
import os, sys, struct
from time import sleep
import socket
########################### CODE STARTS ################################

USERNAME = ""				# global variable that is specific to each client.

def authen_code():
	pass
	# CODE USING urllib. USER, PASSWORD, ENTER.
	# IN THIS CODE, THE CLIENT WAITS EVEN IF IT DOES NOT HAVE A NET CONNECTION. WHEN NET CONNECTS, IT TRIES TO SEND ITS LOGIN INFO.
	
	
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

def list_files(path, file_array, dir_array):
	#pass
	temp = glob.glob(path+"*")				# lists all the files and folderss in the path folder.
	print temp 
	sleep(2)
	for i in temp:
		if not os.path.isdir(i):
			file_array.append(i)
		else:
			dir_array.append(i+os.path.sep)
			list_files(i+os.path.sep,file_array, dir_array)



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

def create_path(data):
	path=os.path.split(data)
	if path[0]:
		if not os.path.exists(path[0]):
			create_path(path[0])
			os.mkdir(path[0])
			os.chmod(path[0],stat.S_IRWXO)
	

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
	a.close()
	client_socket.sendall("##\n")	# mdchecksum will come here.
	print "FINISHED RECEIVING"
			

def recv_data(sock, length):
	data = ''
	sock.settimeout(2)
	try:
		while len(data) < length:
			bytes_read = sock.recv(length - len(data))
			if not bytes_read:
				raise EOFError('socket closed %d bytes into a %d-byte message'
			% (len(data), length))
			data += bytes_read
		return data
	except socket.timeout:
		return data

def recv_size(the_socket):
    #data length is packed into 4 bytes
    total_len=0;total_data=[];size=sys.maxint
    size_data=sock_data='';recv_size=8192
    while total_len<size:
        sock_data=the_socket.recv(recv_size)
        if not total_data:
            if len(sock_data)>4:
                size_data+=sock_data
                size=struct.unpack('>i', size_data[:4])[0]
                recv_size=size
                if recv_size>524288:recv_size=524288
                total_data.append(size_data[4:])
            else:
                size_data+=sock_data
        else:
            total_data.append(sock_data)
        total_len=sum([len(i) for i in total_data ])
    return ''.join(total_data)

def list_files(path, file_array, dir_array):
	pass
	temp = glob.glob(path+"*")				# lists all the files and folderss in the path folder.
	for i in temp:
		if not os.path.isdir(i):
			file_array.append(i)
		else:
			dir_array.append(i+os.path.sep)
			list_files(i+os.path.sep,file_array, dir_array)

def delete_dir(path):
	print "in delete_dir function. Path is:", path
	f=[]
	d=[]
	list_files(path+os.path.sep,f,d)
	for i in f:
		os.remove(i)
	d.sort()
	d.reverse()
	for i in d:
		os.rmdir(i)
	os.rmdir(path)
	print "delete_dir completed!"

def sync_ker_client(client_socket,Path,array):
	print "********** In sync_ker_client ************"
	counter = 0 # counter is 0 if not syncing/just sent file name.
				# when syncing (actual packets being sent), it is set to 1.
	array = (glob.glob(Path+"*"))				# lists all the files and folders in the path folder.
	print array
	#sleep(2)
	
	for i in array:		# taking each file/directory in Path
		x=''
		if i=="server2.py" or i=="as_client.py":
			continue
		for j in i:
			if (j!="\\"):	x+=j
			else:	x+= os.path.sep
		if os.path.isdir(i):	# if it's a directory.
			print 'i is ', i, os.path.abspath(i), os.path.realpath(i)
			if os.path.abspath(i)==os.path.realpath(i):
				print "sending directory:",i,x
				message=".Directory: " + x + os.path.sep
				print message, len(message)
				client_socket.sendall(message)
				reply=0
				#sleep(1)
				while(not reply):
					reply = client_socket.recv(512)
					#client_socket.send("SENDING ACK")
					#sleep(1)
					#print reply
				if(reply == "Roger!"):
					print "roger recieved by client"
					th = []
					sync_ker_client(client_socket,i+os.path.sep,th)		# recurse inside the directory, base Path is dir's Path.
				elif(reply=='Cut!'):
					print '*******USED********'
					delete_dir(x)
					continue
				else:	
					print "Directory not recognised." , reply
					exit(0)
			else:				#While sending directory links, you need to instruct to create a link and the target folder
				print "sending linked directory:",i,x	
				parent = os.path.split(x)[0]
				if os.path.realpath(parent)== os.path.abspath(parent): 	#If it is the link, only the root level of the link needs to be sent, rest all will be taken care of by the target
					f=[]
					d=[]
					list_files("",f,d)	
					flag=0
					print 'd is with dirarray', d, '\n'
					for j in d:
						#print os.path.realpath(x), os.path.abspath(j)
						if os.path.realpath(x) == os.path.abspath(j):		#Find the target of the link
							flag=1
							break
					print os.path.realpath(x), os.path.abspath(j), flag		
					#sleep(0.5)		
					message=".LinkDir: " + j
					print message, len(message)
					client_socket.sendall(message)
					reply = client_socket.recv(512)	#Wait for server to respond
					message=x
					print message, len(message)
					client_socket.sendall(message)	#Send the link path
					reply=0
					#sleep(1)
					while(not reply):
						reply = client_socket.recv(512)
						#client_socket.send("SENDING ACK")
						#sleep(1)
						#print "\n\t\t\t", reply
					print reply	
					if(reply == "Roger!"):
						print "roger recieved by client"
					else:
						print 'Oh mY! Severe Network error'; sleep(20)			##################################################### TESTING PURPOSES	
				else:
					continue		
		else:					# if its a file.
			# Now, send the file. First, its name & address.
			#response=client_socket.recv(4)
			if os.path.abspath(x)==os.path.realpath(x):
				#print "received ack", response
				hashsum=md5sum(x)
				print "sending file:", x,len("File :" + x)
				#sleep(2)
				client_socket.sendall("File :" + x)
				#sleep(2)
				response=0
				while(not response):	
					response=client_socket.recv(4)
					print 'Ack received :', response
					#sleep(2)
				
				client_socket.sendall(hashsum)
				synced=0
				synced=(int)(client_socket.recv(2))
				print 'Ack received : ', synced
				#reply=client_socket.recv(512)
				#print "reply is ", reply
				if (synced==0 or synced==3):
					send_file(client_socket,i)
				elif (synced==1):
					pass			# do nothing
				elif (synced==2):
					####### for receiving file
					# first send ack.
					# then recv_file
					# then recv ack.
					client_socket.sendall("commence sending")
					recv_file(client_socket,x)
					if not (client_socket.recv(20) == "Thanks."):
								print "error in recieving ack-'Thanks'."
								exit(0)
					####### recieving file ends.
				elif (synced==4):
					print "Removing file:", x
					os.remove(x)
				
			else:
				print "sending linked File:",i,x	
				parent = os.path.split(x)[0]
				if os.path.realpath(parent)== os.path.abspath(parent): 	#Files which are themselves the master links only need to be taken care
					f=[]
					d=[]
					list_files("",f,d)	
					flag=0
					print 'f is with filearray', f, '\n'
					for j in f:
						#print os.path.realpath(x), os.path.abspath(j)
						if os.path.realpath(x) == os.path.abspath(j):		#Find the target of the link
							flag=1
							break
					print os.path.realpath(x), os.path.abspath(j), flag		
					#sleep(0.5)		
					message=".LinkFile: " + j
					print message, len(message)
					client_socket.sendall(message)
					reply = client_socket.recv(512)	#Ask whether do u have the master file or just the link will do
					#if reply == "Negative":
					#	send_file(client_socket, j)		#just make the file available there
					message=x
					print message, len(message)
					client_socket.sendall(message)	#Send the link path
					reply=0
					#sleep(1)
					while(not reply):
						reply = client_socket.recv(512)
						#client_socket.send("SENDING ACK")
						#sleep(1)
						#print "\n\t\t\t", reply
					print reply	
					sleep(10)
					if(reply == "Roger!"):
						print "roger recieved by client"
					else:
						print 'Oh mY! Severe Network error'; sleep(20)			##################################################### TESTING PURPOSES	
				else:
					continue
	
	####### end syncing if all the files of the main folder (and hence of all its subfolders) have been completed. :)
	respnse=0
	if Path == "":	
		client_socket.sendall("Sync_End in this folder")
		print 'Did I exit'
		'''Wait for a response if server requires sending of files'''
		while 1:
			print 'Did I exit'
			response=client_socket.recv(1024)
			if(response[:3]=="YES"):
				client_socket.sendall("READY")
				print "received ",response
				if not os.path.split(response[4:])[1]:
						create_path(response[4:])
				else:
					recv_file(client_socket,response[4:])
				print "Responded "
			else:
				break	
			
		print response
	
		print "Synced. Now waiting for 20 seconds!"
		sleep(5)	# wait before you sync further!

def main():
	
	authen_code()		
	#sleep(2)

	# What if the user provided wrong info? It will try to connect forever, as it wont see any socket on the server side?? :/
	# SOLVE ABOVE PROBLEM. 
	# or 
	# FIND SOME CODE IN WHICH THE CLIENT TRIES TO CONNECT FOR 15 SECS, ELSE IT TERMINATES. (MODIFICATION IN BELOW CODE)

	# trying to connect now.
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Port = 6028
	client_socket.connect(('', Port))
	print "Connection established."
	# connection established.
	
	client_socket.send("Name:"+USERNAME)	# first sends the username and recieves ack.
	print "Username sent:", USERNAME
	data = client_socket.recv(10)	
	if (data == "Ack"):
		print "Ack recieved."
	else:
		print "Problems recieving ack from server."
		exit(0)
	
	print "Will sync endlessly."
	'''
	i="Sync"+os.path.sep+"sword.mp3"	

	send_file(client_socket,i)	

	client_socket.close()'''
	
	while(1):
		
		# can apply non-blocking scanf, so if a person wants to quit, he just types something in the terminal. Think. :)
		# if ( non-blocking scanf captures anything <or q/Q, depends on implementation> )
		#		client_socket.send('q')
		#		client_socket.close()
		#		break;
		
		try:
			Path = ""		# This is the user's 'to-sync' directory.
			array = []				# the array that tells all the files or dirs in a dir.

			data = "Lets sync."
			client_socket.send(data)
			data = recv_data(client_socket, 512)
			print data
			if ( data == "Proceed sync." ):
				sync_ker_client(client_socket,Path,array)
		except socket.error:
			print "Server disconnected"	
			break;	


if __name__ == '__main__':
  main()

