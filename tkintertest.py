import tkinter as tk
from netmiko import ConnectHandler

class NetmikoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Netmiko Device Info")
        
        # Create labels and entry fields
        self.device_type_label = tk.Label(root, text="Device Type:")
        self.device_type_entry = tk.Entry(root)
        self.device_type_entry.insert(0, "cisco_ios_telnet")
        
        self.ip_label = tk.Label(root, text="IP Address:")
        self.ip_entry = tk.Entry(root)
        self.ip_entry.insert(0, "f241-04-10-comm.cisco.com")
        
        self.port_label = tk.Label(root, text="Port:")
        self.port_entry = tk.Entry(root)
        self.port_entry.insert(0, "2017")
        
        self.username_label = tk.Label(root, text="Username:")
        self.username_entry = tk.Entry(root)
        self.username_entry.insert(0, "admin")
        
        self.password_label = tk.Label(root, text="Password:")
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.insert(0, "Cisco!123")
        
        self.prompt_label = tk.Label(root)
        
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_device)
        
        # Arrange widgets using grid layout
        self.device_type_label.grid(row=0, column=0, sticky=tk.W)
        self.device_type_entry.grid(row=0, column=1)
        
        self.ip_label.grid(row=1, column=0, sticky=tk.W)
        self.ip_entry.grid(row=1, column=1)
        
        self.port_label.grid(row=2, column=0, sticky=tk.W)
        self.port_entry.grid(row=2, column=1)
        
        self.username_label.grid(row=3, column=0, sticky=tk.W)
        self.username_entry.grid(row=3, column=1)
        
        self.password_label.grid(row=4, column=0, sticky=tk.W)
        self.password_entry.grid(row=4, column=1)
        
        self.prompt_label.grid(row=5, column=0, sticky=tk.W)
        self.prompt_text = tk.StringVar()  # Define the instance variable here
        self.prompt_output = tk.Label(root, textvariable=self.prompt_text)
        self.prompt_output.grid(row=5, column=1, sticky=tk.W)
        
        self.version_label = tk.Label(root, text="Output:")
        self.version_text = tk.Text(root)
        
        self.command_label = tk.Label(root, text="Command:")
        self.command_entry = tk.Entry(root)
        self.send_button = tk.Button(root, text="Send", command=self.connect_to_device)
        
        # Configure the Text widget to expand with the window
        self.version_label.grid(row=6, column=0, sticky=tk.W)
        self.version_text.grid(row=6, column=1, columnspan=2, sticky="nsew")
        
        # Configure row and column weights for dynamic resizing
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.command_label.grid(row=7, column=0, sticky=tk.W)
        self.command_entry.grid(row=7, column=1, sticky="ew")
        self.send_button.grid(row=7, column=2)
        
        self.connect_button.grid(row=5,columnspan=2)
        
    def connect_to_device(self):
        device = {
            'device_type': self.device_type_entry.get(),
            'ip': self.ip_entry.get(),
            'port': self.port_entry.get(),
            'username': self.username_entry.get(),
            'password': self.password_entry.get()
        }
        
        custom_command = self.command_entry.get()
        
        try:
            connection = ConnectHandler(**device)
            prompt = connection.find_prompt()
            self.prompt_text.set(prompt)
            
            output = connection.send_command(custom_command)
            self.version_text.insert(tk.END, output)
            
            connection.disconnect()
        except Exception as e:
            print("An error occurred:", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = NetmikoApp(root)
    root.mainloop()