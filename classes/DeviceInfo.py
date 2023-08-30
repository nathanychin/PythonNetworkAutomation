class DeviceInfo:
    
    def __init__(self, HOST = "", PORT = "", USER = "", PASSWD = "", IMAGE = "cisco_ios_telnet"):
        self.host = HOST
        self.port = PORT
        self.username = USER
        self.password = PASSWD
        self.image = IMAGE
        self.list = [self.host, self.port, self.username, self.password, self.image]
    
    # Input helper
    # _input("Only input interger: ", int)
    def _input(self, message, input_type=str):
        while True:
            try:
                return input_type(input(message))
            except:
                pass

    # Set HOST and PORT
    def _host(self):
        while self.host == "":
            print("Enter host: ")
            self.host = self._input(str)
            self.host = self.host.upper()
        return self.host

    def _port(self):
        self.port = self._input("Enter port (Must be a number between 2002 and 2999): ", int)
        while self.port < 2002 or self.port > 2999:
            self.port = self._input("Enter port (Must be a number between 2002 and 2999): ", int)
        return self.port

    # Set username
    def _username(self):
        self.username = self._input("Enter username: [admin] ")
        if self.username == "":
            self.username = "admin"
        return self.username

    #Get password
    def _password(self):
        self.password = self._input("Enter password: [cisco!123] ")
        if self.password == "":
            self.password = "cisco!123"
        return self.password

    # Set os_image
    def _image(self):
        image_accepted = False
        while image_accepted == False:
            self.image = self._input(
                "Enter OS image type (IOS, XR) (Not case sensitive): [IOS] ", str)
            if self.image == "":
                self.image = "cisco_ios_telnet"
            else:
                self.image = self.image.lower()
                if self.image == "xr":
                    self.image = "cisco_xr_telnet"
                    image_accepted = True
                else:
                    print("Invalid OS image: %s" % self.image)
            return self.image

    # Set device info
    def set_device_info(self):
        correct = False
        while correct == False:
            self.host = self._host()
            self.port = self._port()
            self.username = self._username()
            self.password = self._password()
            self.image = self._image()

            # Verify information
            print("Is this information correct?")
            print("%s" % self.host)
            print("Port: %s" % self.port)
            print("Username: %s" % self.username)
            print("Password: %s" % self.password)
            print("Image: %s" % self.image)
            correct = self._input("(Y or N): [Yes]", str)
            correct.lower()

            if correct == "y" or correct == "":
                correct = True
                self.list = [self.host, self.port, self.username, self.password, self.image]
                return self.list
            else:
                correct = False
                continue