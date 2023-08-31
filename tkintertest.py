import tkinter as tk
from netmiko import *

class NetmikoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Netmiko Device Info")
        self.connection = None # Initialize connection as None
        
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
        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect_from_device)
        
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
        
        self.output_label = tk.Label(root, text="Output:")
        self.output_text = tk.Text(root, background="dark gray", fg="white")
        
        self.command_label = tk.Label(root, text="Command:")
        self.command_entry = tk.Entry(root)
        self.command_entry.bind("<Return>", lambda event=None: self.send_command())
        self.send_button = tk.Button(root, text="Send", command=self.send_command)
        
        # Configure the Text widget to expand with the window
        self.output_label.grid(row=6, column=0, sticky=tk.W)
        self.output_text.grid(row=6, column=1, columnspan=2, sticky="nsew")
        
        # Configure row and column weights for dynamic resizing
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.command_label.grid(row=7, column=0, sticky=tk.W)
        self.command_entry.grid(row=7, column=1, sticky="ew")
        self.send_button.grid(row=7, column=2)
        
        self.connect_button.grid(row=5,columnspan=2)
        self.disconnect_button.grid(row=5, column=1, columnspan=2)
        
    def connect_to_device(self):
        device = {
            'device_type': self.device_type_entry.get(),
            'ip': self.ip_entry.get(),
            'port': self.port_entry.get(),
            'username': self.username_entry.get(),
            'password': self.password_entry.get()
        }
        
        try:
            self.connection = ConnectHandler(**device)
            prompt = self.connection.find_prompt()
            self.prompt_text.set(prompt)
            self.output_text.insert(tk.END, prompt + "\n")
        except Exception as e:
            print("An error occurred:", str(e))
            
    def send_command(self):
        if self.connection:
            try:
                custom_command = self.command_entry.get().strip()
                prompt = self.prompt_text.get()
                # Clear the command_entry widget
                self.command_entry.delete(0, tk.END)
            
                print(prompt)
                # Handle mode transitions
                if custom_command.startswith("en"):
                    
                    if ">" in prompt:  # Check if in exec mode
                        self.connection.enable()  # Enter enable mode
                        prompt = self.connection.find_prompt()  # Update prompt
                        print(prompt)
                elif custom_command.startswith("conf"):
                    if "#" in prompt:  # Check if in enable mode
                        self.connection.config_mode()  # Enter config mode
                        prompt = self.connection.find_prompt()  # Update prompt
                elif custom_command == "exit" or custom_command == "end":
                    print(prompt)
                    if "#" in prompt:  # Check if in config mode
                        self.connection.exit_config_mode()  # Exit config mode
                        prompt = self.connection.find_prompt()  # Update prompt
                        print(prompt)
            
                self.prompt_text.set(prompt)
                output = ""
                if "conf" in custom_command:
                    pass
                else:
                    output = self.connection.send_command_timing(custom_command)
                #full_command = f"{prompt} {custom_command}"
                self.output_text.insert(tk.END,custom_command + "\n" + output + "\n" + prompt)
                
                # Scroll to the end of the Text widget
                self.output_text.see(tk.END)
                
                # Bind the spacebar event to the output_text Text widget
                self.command_entry.bind("<space>", self.scroll_output)
                
            except NetmikoTimeoutException:
                print("Pattern not detected. Command may have failed.")    
            
            except Exception as e:
                print("An error occurred:", str(e))
        else:
            print("Not connected to a device.")

    def scroll_output(self, event):
        # Check if command_entry widget is empty and spacebar is pressed
        print("scroll_output executed")
        if not self.command_entry.get() and event.char == " ":
            self.output_text.yview_scroll(1, "pages")  # Scroll down by one page

    def disconnect_from_device(self):
        if self.connection:
            try:
                self.connection.disconnect()  # Disconnect if connection exists
                print("Disconnected from device")
            except Exception as e:
                print("An error occurred during disconnect:", str(e))
            finally:
                self.connection = None  # Set connection to None
    
if __name__ == "__main__":
    root = tk.Tk()
    app = NetmikoApp(root)
    root.mainloop()