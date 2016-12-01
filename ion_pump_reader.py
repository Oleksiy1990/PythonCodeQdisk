"""

This script reads a Pferfer Vacuum TPG 262 Dual Gauge Measurement unit 
through an RS 232 serial port and produces a file with timestamped 
values in mbar. 

A new file is created for every calendar day 


"""





import serial
from serial.serialutil import SerialException
import re
import sys
import time
import datetime


#These are the ASCII hexadecimals representing these characters
#We need these characters for commands sent by RS 232
_ACK = "\x06" # bytes(6)
_ENQ = "\x05" # bytes(5)
_CR  = "\x0D"
_LF  = "\x0A"
_ASTER = "\x2A"


class IonPumpReader:
    """
    Sets up a class which queries the gauge reader and can be used 
    directly to read the pressure 

    """
    def __init__(self,porttoconnect,num=1,baudrate=9600,timeout=2):
        self.port = porttoconnect
        self.baud = baudrate
        self.time_out = timeout
        self.gaugenumber = str(num)


    def __connect(self):
        """
        Connects through the RS 232 serial port and checks if the connection 
        is established 
        """
        self.__ser = serial.Serial()
        self.__ser.port = self.port
        self.__ser.baudrate = self.baud
        self.__ser.timeout = self.time_out

        if self.__ser.isOpen():
            return (True,self.__ser)

        try:
            self.__ser.open() 
        except SerialException:
            print("Cannot connect to ion pump reader at serial port "+self.__ser.port)
            return (False,None)
        
        #print("Opened serial port")
        return (self.__ser.isOpen(),self.__ser) 


    def __disconnect(self):
        """
        Disconnects from the RS 232 serial port. It's important to not leave connections hanging
        """
        try:
            status = self.__ser.isOpen()
            if status:
                self.__ser.close()
            else:
                print("Connection at port "+self.__ser.port+" cannot be closed")
        except SerialException:
            print("Exception raised at disconnecting from port "+self.__ser.port)

    def read(self,query="ModelNumber"):

        (connectionStatus,connection) = self.__connect()

        if not connectionStatus: 
            print("Connection to port "+self.__ser.port+" not established")
            self.__disconnect()
            return None
        else:
            print("Connection established at port "+self.__ser.port)

        
        #initial_command = ("PR"+self.gaugenumber+_CR+_LF).encode("ascii")
        initial_command = (_ASTER+"VE?,"+_CR).encode("ascii")
        connection.write(initial_command)

        necessary_reply = (_ACK+_CR+_LF).encode("ascii")
        reply = connection.read(15)
        print(reply)
        
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

def get_pressure(comport,gaugenum = 1):
    reader1 = GaugeReader(comport,num=gaugenum)
    current_pressure = reader1.read()
    return current_pressure
        
if __name__ == '__main__':
    comport = "COM12"
    rdr = GaugeReader(comport)
    rdr.read()
    sys.exit(0)


    #folder_tosave = "C:\\Users\\QGMPC1\\Dropbox\\PressureLog\\"
    folder_tosave = "C:\\Users\\SrBEC\\Desktop\\"
    time_between_measurements = 2#60*5 #5 min, given in seconds

    while True:
        print("Running infinite loop")
        datenow = datetime.datetime.now().strftime("%d%m%Y")
        timestamp_now = datetime.datetime.now()
        full_timestamp = timestamp_now.strftime("%H:%M:%S")
        hour_now = timestamp_now.strftime("%H")
        minute_now = timestamp_now.strftime("%M")
        second_now = timestamp_now.strftime("%S")
        
        file_tosave = folder_tosave+datenow+"pump2.txt"
        
        pressure = get_pressure(comport)

        if pressure is None:
            print("Could not read the pressure. Not saving anything")
            time.sleep(time_between_measurements)
            continue
        
        print("Pressure is %.3e mbar"%pressure)
        file_output = open(file_tosave,"a")
        file_output.write("%s %s %s %s %.4e mbar\n"%(full_timestamp,hour_now,minute_now,second_now,pressure))
        file_output.close()
        print("Press CTRL+C to terminate")
        time.sleep(time_between_measurements)



