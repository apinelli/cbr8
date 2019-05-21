# Open SSHv2 connection to devices

import sys
import os
import os.path
import time
import paramiko

date = (time.strftime("%d-%m-%Y"))

print(" ")
print("=====================================================================")
print("****** TROUBLESHOOT CBR8 RPHY FOR VIDEO ******")
print("****** The program will gather show commands from CBR8 and RPD")
print("****** The whole process may take more than 15 minutes******")
print("=====================================================================")
print(" ")

ip = raw_input('Enter CBR8 ip address : ')
rpd_ip = raw_input('Enter RPD ip address : ')
username = raw_input('Enter CBR8 username : ')
password = raw_input('Enter CBR8 password : ')
file_cbr8 = raw_input('Enter the file name for show commands in cbr8 : ')
file_rpd = raw_input('Enter the file name for show commands in rpd : ')
print '\n'
print '\n'

def open_ssh_rpd(ip, rpd_ip, file_rpd):
    channel_data = str()
    rpd_pw = 'admin'
    temp = 0
    try:
        session = paramiko.SSHClient()
        # For testing purposes, this allows auto-accepting unknown host keys
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(ip, username=username, password=password)
        
	connection = session.invoke_shell()

	print '\n'
	print '\n'
	print 'Collecting RPD info...'
	print 'It may take more than 5 minutes to complete'

	while True:
		if connection.recv_ready():
			print '*',
			channel_data += connection.recv(9999)
			save_output = open('rpd_collection_' + rpd_ip + '_' + date, 'w')
			save_output.write(str(channel_data.decode()))
		        save_output.write('\n')
      			time.sleep(1)
        		save_output.close()
		else:
			continue

		if channel_data.endswith('F241-36-12-cBR8-1#'):
			temp += 1
			if temp <= 1:
			    connection.send('ssh -l admin ' + rpd_ip + '\n')
			else:
			    print 'RPD info collected!!!'
			    print '\n'
			    print '\n'
			    connection.close()
			    break

		elif channel_data.endswith('Password: '):
			connection.send(rpd_pw)
			connection.send('\n')
                elif channel_data.endswith('R-PHY>'):
                	connection.send('enable')
			connection.send('\n')
		elif channel_data.endswith('R-PHY#'):
		        with open(file_rpd, mode='r') as d:
            			for line in d.readlines():
                		    connection.send(line)
                		    connection.send('\n')
				    time.sleep(2)
		
    except paramiko.AuthenticationException:
        print(
            "* Invalid username or password. \n* Please check the username/password file or the device configuration!")
        print("* Closing program...\n")

def open_ssh_conn(ip, username, password, file_cbr8):
    channel_data = str()
    rpd_pw = str()
    try:
        session = paramiko.SSHClient()
        # For testing purposes, this allows auto-accepting unknown host keys
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(ip, username=username, password=password)
        
	connection = session.invoke_shell()

	print 'Collecting CBR8 info...'
	print 'It will take several minutes to complete'
	print '\n'

        with open(file_cbr8, mode='r') as d:
            for line in d.readlines():
                connection.send(line)
                connection.send('\n')
		time.sleep(2)
		print '*',
       	save_output = open('cbr8_collection_' + ip + '_' + date, 'a')
	output = connection.recv(1000000000000000000000000000000000000000000000000000)
	save_output.write(str(output.decode()))
        save_output.write('\n')
        save_output.close()
        time.sleep(1)
        print "CBR8 info collected!!!"
	print '\n'

		
    except paramiko.AuthenticationException:
        print(
            "* Invalid username or password. \n* Please check the username/password file or the device configuration!")
        print("* Closing program...\n")

if __name__ == "__main__":
    open_ssh_conn(ip, username, password, file_cbr8)
    open_ssh_rpd(ip, rpd_ip, file_rpd)
