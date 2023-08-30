from classes.Network import *
from classes.DeviceInfo import *

def main():
    D = DeviceInfo().set_device_info()
    Device = NetDevice(D[0], D[1], D[2], D[3], D[4])
    
    host = D[0]
    port = D[1]
    
    print(f'Connecting to {host}: {port}')
    print("#" * 60)
    
    try:
        Device.NetConnect()
        print(f"Successfully connected to {host}:{port}")
        print("#" * 60)
        Device.NetEnable()
        Device.NetShVer()
        print("#" * 60)
        Device.NetDisconnect()
        print(f"Disconnected from {host}:{port}")
        print("#" * 60)
        
    except Exception as e:
        print("Error: " + str(e))
        print("===================================")
        print(f"Unable to connect to {host}:{port}")

if __name__ == '__main__':
    main()