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
_ASTER = "\x2A"
_CR  = "\x0D"

## This is the old stuff from turbo gauge reader 
#_ACK = "\x06" # bytes(6)
#\_ENQ = "\x05" # bytes(5)
#_LF  = "\x0A"



class IonPumpReader:
    """
    Sets up a class which queries the gauge reader and can be used 
    directly to read the pressure 

    """

    command_dict = { "ModelNumber":"MO",
                    "FirmwareVersion":"VE",
                    "Current":"CU",
                    "Pressure":"PR",
                    "Voltage":"VO",
                    "Status":"ST",
                    "PressureUnits":"UN",
                    "PumpSize":"PS",
                    "Polarity":"PO",
                    "HVONOFF":"HV",
                    "MaxCurrent":"MC",
                    "SetPoint":"SP",
                    "MaxVoltage":"MV"}

    OK_reply = "OK:" # This is the string at the beginning of any legal reply from the ion pump controller


    def __init__(self,porttoconnect,num=1,baudrate=9600,timeout=2):
        self.port = porttoconnect
        self.baud = baudrate
        self.time_out = timeout


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

    def __string_analysis(self,data_string,query):
        
        if query in ["Current"]:
            reply_analysis = re.search(r"(OK:)(\d{1}.\d{2}e[-+]\d{2})", data_string)
        elif query in ["Voltage"]:
            reply_analysis = re.search(r"(OK:)(\d{4})", data_string)
        else:
            print("Sorry, string formatting for this case has not been written yet. Returning full string")
            return (False,data_string)

        if reply_analysis == None: #None is returned when string matching fails and nothing is found
            print("String matching failed, the reply is illegal or none")
            return (False,None)
        elif reply_analysis.group(1) != self.OK_reply: # The != compares values of the strings 
            print("Reply is illegally formatted, something is wrong")
            return (False,None)
        elif reply_analysis.group(1) == self.OK_reply:
            reply_float = float(reply_analysis.group(2))
            return (True,reply_float)
        else:
            return (False,None)


    def read(self,query="Current"):

        if query in self.command_dict:
            pass
        else:
            print("Such query is undefined. Check p. 25 of controller manual for allowed queries")
            return None

        (connectionStatus,connection) = self.__connect()

        if not connectionStatus: 
            print("Connection to port "+self.__ser.port+" not established")
            self.__disconnect()
            return None
        else:
            print("Connection established at port "+self.__ser.port)


        #The next lines send the command to read the ion pump controller and then receive the reply 

        reading_command = (_ASTER+self.command_dict[query]+"?,"+_CR).encode("ascii")
        connection.write(reading_command)

        reply = connection.read(15)
        self.__disconnect() # Connections should not be left hanging open


        reply_asString = reply.decode("ascii").strip()
        #print(reply_asString)

        (readingCheck, result) = self.__string_analysis(reply_asString,query)

        print(query,result)
        return (readingCheck, result)

        
if __name__ == '__main__':
    
    comportSciencePumps = "COM5"
    comportPreparationPumps = "COM8"
    
    readerScience = IonPumpReader(comportSciencePumps)
    readerPreparation = IonPumpReader(comportPreparationPumps)
    #readerScience.read("Current")
    #readerPreparation.read("Voltage")
    #sys.exit(0)


    folder_tosave = "C:\\Users\\QGMPC1\\Dropbox\\IonPumpLog\\"
    #folder_tosave = "C:\\Users\\SrBEC\\Dropbox\\IonPumpLog\\"
    #folder_tosave = "C:\\Users\\SrBEC\\Desktop\\"
    time_between_measurements = 60 # given in seconds

    while True:
        print("Running infinite loop")
        datenow = datetime.datetime.now().strftime("%d%m%Y")
        timestamp_now = datetime.datetime.now()
        full_timestamp = timestamp_now.strftime("%H:%M:%S")
        hour_now = timestamp_now.strftime("%H")
        minute_now = timestamp_now.strftime("%M")
        second_now = timestamp_now.strftime("%S")
        
        file_tosave_SciencePumps = folder_tosave+datenow+"SciencePumps.txt"
        file_tosave_PreparationPumps = folder_tosave+datenow+"PreparationPumps.txt"
        
        checkScience,currentScience = readerScience.read("Current")
        checkScience,voltageScience = readerScience.read("Voltage")

        checkPreparation,currentPreparation = readerPreparation.read("Current")
        checkPreparation,voltagePreparation = readerPreparation.read("Voltage")




        if checkScience is False or checkPreparation is False:
            print("Could not read whatever was asked. Not saving anything")
            time.sleep(time_between_measurements)
            continue # Takes the code back to the beginning of the while-loop
        

        file_output_Science = open(file_tosave_SciencePumps,"a")
        file_output_Science.write("%s %s %s %s Current %.3e A Voltage %.3e V\n"%(full_timestamp,hour_now,minute_now,second_now,currentScience,voltageScience))
        file_output_Science.close()

        file_output_Preparation = open(file_tosave_PreparationPumps,"a")
        file_output_Preparation.write("%s %s %s %s Current %.3e A Voltage %.3e V\n"%(full_timestamp,hour_now,minute_now,second_now,currentPreparation,voltagePreparation))
        file_output_Preparation.close()


        print("Press CTRL+C to terminate")
        time.sleep(time_between_measurements)



