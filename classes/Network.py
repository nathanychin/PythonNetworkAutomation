#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from netmiko import Netmiko, ConnectHandler
from datetime import datetime
"""
class NetServers:
    def __init__(self, FTP, USER, PASSWD, TFTP):
        self.FTPServer = FTP
        self.FTPUser = USER
        self.FTPPassWd = PASSWD
        self.TFTPServer = TFTP
        self.TransType = {
                        "FTP": "ftp://{0}:{1}@{2}".format(self.FTPUser, self.FTPPassWd, self.FTPServer),
                        "TFTP": "tftp://{0}".format(self.TFTPServer)
                        }"""

class NetDevice:
    def __init__(self, IP, PORT, USER, PASSWD, TYPE, GLOBAL = 2):
    # Index Names for Structures
        self.BootDrive = ""
        self.DirDictionary = [""]
        self.Directory = ""
        self.DiskFree = 0
        self.File = [""]
        self.FileBoot = [""]
        self.FileCount = 0
        self.FileName = ""
        self.Hostname = ""
        self.StartTime = ""
        self.EndTime = ""
        self.Command = ""
        self.Output = ""
        self.Newline ="\n"
        #self.TransType = TRANSTYPE
        self.Device = {
            "ip": IP,
            "port": PORT,
            "username": USER,
            "password": PASSWD,
            #"enable": ENABLE,
            "device_type": TYPE,
            'global_delay_factor': GLOBAL,
        }
    
    def FindPrompt(self):
        return self.net_connect.find_prompt()

    def SendCmd(self):
        self.StartTime = datetime.now()
        self.Output = self.net_connect.send_command_timing(self.Command)
        self.Output += self.FindPrompt()
        self.EndTime = datetime.now()

    def PrintOutput(self):
        print("#" * 60) 
        print(self.Command)
        print(self.Output)
        print("#" * 60) 

    def DevBoot(self):
        for File in self.Directory.split("\n"):
            Line = File.split(" ")   
            if len(Line) > 8:
                if ".bin" in Line[8]:
                    self.FileBoot.append(Line[8])
        del self.FileBoot[0]

    def DirStruct(self):
        Directory = self.Output.split("\n")
        Location = Directory[0].split(' ')
        self.BootDrive = Location[-1]
        self.BootDrive = self.BootDrive[0:-1]
        for Line in Directory:
            Line = Line.split(' ')
            if "bytes" in Line:
                self.TotalDisk = Line[0]
                self.DiskFree = Line[3]
                self.DiskFree = self.DiskFree[1:]
            Append = ""
            if len(Line) > 6:
                for Section in Line:
                    if Section != '':
                        Append += Section
                        Append += " "    
                Append += self.Newline
                self.Directory += Append

    def DirBreakdown(self): 
        Directory = self.Directory.split("\n")
        for Line in Directory:
            if Line != '':
                Line = Line.split(" ")
                if "d" in Line[1]:
                    Line[0] = "\'Directory\'"
                if "-" in Line[1]:
                    Line[0] = "\'File\'"
                Line[1] = "\'Size:\'"
                Line[2] = "\'" + Line[2] + "\'"
                Line[4] = " ".join(Line[3:6])
                Line[4] = "\'" + Line[4] + "\'"
                Line[3] = "\'Date:\'"
                Line[5] = "\'Time:\'"
                Line[7] = "\'Filename:\'"
                Line[8] = "\'" + Line[8] + "\'"
                Line.insert(0, "\'Type:\'")
                Line[0] = " ".join(Line[0:2])
                Line[1] = " ".join(Line[2:4])
                Line[2] = " ".join(Line[4:6])
                Line[3] = " ".join(Line[6:8])
                Line[4] = " ".join(Line[8:-1])
        
                del Line[5:]
                Count = str(self.FileCount)
                Count = "\'Num:\' ""\'" + Count + "\'"
                Line.insert(0, Count)
                Line = ", ".join(Line)
                self.DirDictionary.append(Line)
                self.FileCount += 1 
        del self.DirDictionary[0]

    def SetHostname(self):
        self.Output = self.FindPrompt()
        if "(" in self.Output:
            list1 = self.Output.split("(")
        if "#" in self.Output:
            list1 = self.Output.split("#")
        if ">" in self.Output:
            list1 = self.Output.split(">")
        self.Hostname = list1[0]

    def FileSet(self):
        self.NetDir()
        self.SetHostname()

    #######################################################################################
    # CONNECT AND DISCONNECT TO DEVICE
    #######################################################################################

    def NetConnect(self):
        self.net_connect = Netmiko(**self.Device)

    def NetDisconnect(self):
        self.net_connect.disconnect()

    def NetCommand(self, Command):
        self.Command = Command
        self.SendCmd()
    
    #######################################################################################
    # CISCO COMMANDS
    #######################################################################################
    
    def NetDir(self):
        self.Command = "dir"
        self.SendCmd()
        self.DirStruct()
        self.DirBreakdown()
        self.DevBoot()
        self.PrintOutput()
        
    def NetInv(self):
        self.Command = "show inventory"
        self.PrintOutput()

    def NetShVer(self):
        self.Command = "show version"
        self.SendCmd()
        self.PrintOutput()

    def NetCdp(self):
        self.Command = "show cdp n"
        self.SendCmd()
        self.PrintOutput()

    def NetConfig(self):
        self.Command = "show running-config"
        self.SendCmd()
        self.PrintOutput()

    def NetInt(self):
        self.Command = "show ip int br"
        self.SendCmd()
        self.PrintOutput()

    def NetHostName(self, new_name):
        self.Command = "conf t\n hostname " + new_name +"\n exit"
        self.SendCmd()

    def NetEnable(self):
        self.FindPrompt()
        if self.FindPrompt()[-1] == ">":
            self.Command = "enable"
            self.SendCmd()
            self.PrintOutput()
            substring = self.FindPrompt()
            pswrd_string = "Password:"
            if pswrd_string in substring:
                self.Command = input("Enter device enable password: ")
                self.SendCmd()
                self.PrintOutput()

    def NetPrintPrompt(self):
        self.Command = "Current Prompt is:"
        self.Output = self.net_connect.find_prompt()
        self.PrintOutput()
    
    def NetDelete(self, Location, FileName):
        self.Command = "delete {0}{1}".format (Location, FileName)
        self.SendCmd()
        #self.PrintOutput()
    
    def NetCopy(self, Filename, Location, Direction, Service):
        if Direction == "GET":
            self.Command = "copy {0}/{1} {2}{1}"
        else:
            if Direction == "PUT":
                self.Command = "copy {2}{1} {0}/{1}"
        self.Command = self.Command.format(self.TransType[Service], Filename, Location)
        self.SendCmd()
        self.PrintOutput()