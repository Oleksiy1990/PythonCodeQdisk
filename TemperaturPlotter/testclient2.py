# Import socket module
import socket
import ast
import sys
import os
import numpy as np


### This function is not used! It was written earlier for test purposes
def get_datatuple_board(comport="COM9",boardnum=1):

    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect
    port = 12345

    # connect to the server on local computer
    s.connect(('127.0.0.1', port))

    received_data = s.recv(1024).decode() #result is a string object

    data_astuple = ast.literal_eval(received_data)
    if isinstance(data_astuple,tuple):
        pass
    else:
        print("The data cannot be converted into tuple")
        return None

    print(received_data) #decoding results in a string
    # close the connection
    s.close()
    return data_astuple

class TCBoard:

	self.TCvalues = np.zeros(12) #initialize an array of 12 TC values to be filled with the actual temperatures later

    def __init__(self,comport_arg=None,address_arg=None,nameslist_arg=None,folder_tosave_arg=None):
        
        if isinstance(comport_arg,str):
            self.comport = comport_arg
        else:
            sys.exit("Comport argument is not a string. String required. Exiting")
        if isinstance(address_arg,int):
            self.address = address_arg
        else:
            sys.exit("Board address argument is not an integer. Integer required. Exiting")
        if isinstance(nameslist_arg,list):    
            self.namelist = nameslist_arg
        else:
            sys.exit("Thermocouple names are not a list. List required. Exiting")
        if isinstance(folder_tosave_arg,str):
            if os.path.isdir(folder_tosave_arg):
                print("Saving temperature data into ",folder_tosave_arg)
                self.folder_tosave = folder_tosave_arg
            else:
                sys.exit("The directory for saving data does not exist. Exiting")
        else:
            sys.exit("Folder name is not a string. String required. Exiting")

    def __connect(self):
        """
        Connects through the RS 232 serial port and checks if the connection 
        is established 
        """
        self.__ser = serial.Serial()
        self.__ser.port = self.comport
        
        self.__ser.baudrate = 9600 #baudrate and timeout are hard-coded for now for these particular boards
        self.__ser.timeout = 2

        if self.__ser.isOpen():
            return (True,self.__ser)

        try:
            self.__ser.open()     
        except SerialException:
            print("Cannot connect to gauge reader at serial port "+self.__ser.port)
            return (False,None)

        if self.__ser.isOpen():
            print("Connection established at port "+self.__ser.port)
            return (True,self.__ser)



    def __disconnect(self):
        """
        Disconnects from the RS 232 serial port. It's important to not leave connections hanging
        """
        try:
            status = self.__ser.isOpen()
            if status:
                self.__ser.close()
            else:
                print("Gauge reader at port "+self.__ser.port+" was not open and thus cannot be closed")
        except: # Any exception will be caught, also if self.__ser hasn't been defined before 
            print("Exception raised at disconnecting from port "+self.__ser.port)

    def __read_allTC_raw(self):

        """
        This returns a data tuple that the board produces. It's in the form

        (num_tc1to12,temp,...) that is repeated 12 times, so the tuple is supposed to be 24 entries long 

        the TCs are listed in a random order that changes from reading to reading, so they must be manually put in the correct order 
        
		NOT FINISHED
        """

        (connectionStatus,connection) = self.__connect()

        if not connectionStatus: 
            print("Did not establish connection to port "+self.__ser.port)
            return None

        
        initial_command = ("PR"+self.gaugenumber+_CR+_LF).encode("ascii")
        connection.write(initial_command)

        necessary_reply = (_ACK+_CR+_LF).encode("ascii")
        reply = connection.read(3)
        
        if reply != necessary_reply:
            print("Communication failed at ACK stage")
            self.__disconnect()
            return None

        connection.write(_ENQ.encode("ascii")) #Making the enquiry
        
        reply = connection.read(15)
        if len(list(reply)) != 15:
            print("Unexpected length of the reply")
            self.__disconnect()
            return None
        
        reply_asString = reply.decode("ascii").strip()

        self.__disconnect()

        m = re.search(r"(\d)..(\d\.\d{4}E[-+]\d{2})", reply_asString) #Correct regular expression matching 
        
        if(m == None):
            print("Failed to match the reply by regular expression matching")
            return None

        pressure = float(m.group(2))
        return pressure

    ### NOTE! This is only for debugging by generating random data from a socket on the same computer! 
    def __read_allTC_debug(self):

        """
        This returns a data tuple that the board produces. It's in the form

        (num_tc1to12,temp,...) that is repeated 12 times, so the tuple is supposed to be 24 entries long 

        the TCs are listed in a random order that changes from reading to reading, so they must be manually put in the correct order 
        """

        s = socket.socket()

        # Define the port on which you want to connect
        port = 12345

        # connect to the server on local computer
        s.connect(('127.0.0.1', port))

        received_data = s.recv(1024).decode() #result is a string object

        data_astuple = ast.literal_eval(received_data)
        if isinstance(data_astuple,tuple):
            pass
        else:
            print("The data cannot be converted into tuple")
            return None

        # close the connection
        s.close()
        #print(data_astuple)
        return data_astuple

    def read_allTC(self):

        """
        This produces an ordered Numpy list of temperatures, where the position in the list 
        is the number of the thermocouple 
        (well, apart from counting starting from 0, so 0-11 corresponds to 1-12 in the real board thermocouples)
        """

        mixed_datatuple = self.__read_allTC_debug()
        dataarray = np.zeros(len(mixed_datatuple)/2)

        for n in range(len(mixed_datatuple)):

            if n%2 == 0:
                current_TC_number = mixed_datatuple[n]
                current_TC_temp = mixed_datatuple[n+1]

                dataarray[current_TC_number-1] = current_TC_temp
            elif n%2 == 1:
                pass

            else:
                print("Something went quite wrong in read_allTC function")
        self.TCvalues = dataarray

        return self.TCvalues

    def save_allTC(self):
        
        data = self.read_allTC()
        names = self.namelist

        info_line = np.ravel(np.column_stack((names,data))) ### Note: somehow this returns every array entry as a string. This is in principle OK for writing to a file
        print(info_line)
        return info_line





u = TCBoard(comport_arg="COM9",address_arg=1,nameslist_arg=["a","b","c","d"],folder_tosave_arg="Q:\qgases\groups\strontium\Oleksiy\PythonCodeQdisk\TemperaturPlotter")
q = u.save_allTC()
print(type(q[0]))
print(type(q[1]))
#print(u.read_allTC())
#print(type(u.read_allTC()))


def save_datatuple_tofile(filepath,datatuple):
    pass




