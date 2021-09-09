import pexpect
import time
import sys

list_of_devices_ip = open('list_of_devices.txt', 'r')
ip_addresses = list_of_devices_ip.readlines()

auth_file = open('auth.txt', 'r')
credentials = auth_file.readlines()
switch_usr = credentials[0].strip()
switch_pwd = credentials[1].strip()

for device_ip in ip_addresses:
	try:
		try:
			child = pexpect.spawn('ssh %s@%s' % (switch_usr,device_ip))
			child.logfile = sys.stdout.buffer
			child.timeout = 8
			child.expect('Password:')
		except pexpect.TIMEOUT:
			raise OurException("Couldn't log on to the switch")
		child.sendline(switch_pwd)
		child.expect('#')
		child.sendline('conf t')
		child.expect('\(config\)#')
		child.sendline('feature nxapi')
		child.expect('#')
		child.sendline('nxapi http port 8800')
		child.expect('#')
		time.sleep(10)
		child.sendline('quit')
	except(pexpect.EOF, pexpect.TIMEOUT):
		error("Error while trying to enable NX-API.")
		raise