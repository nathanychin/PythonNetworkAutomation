from netmiko import ConnectHandler

# Get Device information from user
device = {
    #'device_type': input("Enter device type (cisco_ios, cisco_xe, cisco_nxos, cisco_aci, cisco_asa): "),
    'device_type': 'cisco_ios_telnet',
    'ip': input("Enter IP address: "), #Hostname
    'port': input('Port number: '), #Port number
    'username': input("Enter username: "),
    'password': input("Enter password: "),
}

try:
    connection = ConnectHandler(**device)
    print(f"Connecting to device {device['ip']}: {device['port']}")
    
    print(f"Connected to {device['ip']}")
    
    commands = ['show version']
    
    for command in commands:
        print(f'Sending command: {command}')
        output = connection.send_command(command)
        print(f'\n{output}\n')
    
    connection.disconnect()
    print(f"Disconnected from {device['ip']}")

except Exception as e:
    print("Exception: ", str(e))