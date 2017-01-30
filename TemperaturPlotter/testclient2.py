# Import socket module
import socket
import ast
import sys


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
    def __init__(self,comport=None,address=None,namesList=None):
        if isinstance(comport,str):
            self.comport = comport
        else:
            sys.exit("Comport argument is not a string. String required. Exiting")
        if isinstance(address,int):
            self.address = address
        else:
            sys.exit("Board address argument is not an integer. Integer required. Exiting")
            
        self.namelist = namelist


def save_datatuple_tofile(filepath,datatuple):
    pass


get_datatuple_board()

