import requests
import json

client_cert_auth = False

auth_file = open('auth.txt', 'r')
credentials = auth_file.readlines()
switchuser = credentials[0].strip()
switchpassword = credentials[1].strip()

client_cert = 'PATH_TO_CLIENT_CERT_FILE'
client_private_key='PATH_TO_CLIENT_PRIVATE_KEY_FILE'
ca_cert = 'PATH_TO_CA_CERT_THAT_SIGNED_NXAPI_SERVER_CERT'

myheaders = {'content-type':'application/json-rpc'}

conf_file = open('configuration.txt', 'r')
Commands = conf_file.readlines()

list_of_devices_ip = open('list_of_devices.txt', 'r')
ip_addresses = list_of_devices_ip.readlines()

payload = []
instance_id = 0

for command in Commands:
    if command.strip():
        instance_id += 1
        command = command.rstrip()
        payload_dict = {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
              "cmd": command.strip(),
              "version": 1
            },
            "id": instance_id,
        }
        payload.append(payload_dict)
    else:
       continue

for device_ip in ip_addresses:
        
        url="http://" + device_ip.strip() + ":8800/ins"
        print(url)

        if client_cert_auth is False:
            response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
        else:
            response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword),cert=(client_cert,client_private_key),verify=ca_cert).json()