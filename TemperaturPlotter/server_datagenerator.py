# first of all import the socket library
import socket
import random

# next create a socket object
s = socket.socket()         
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345                

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('localhost', port))        
print("socket bound to %s" %(port))

# put the socket into listening mode
s.listen(5)     
print("socket is listening")            

# a forever loop until we interrupt it or 
# an error occurs
while True:
   # Establish connection with client.
   c, addr = s.accept()     
   print('Got connection from', addr)

   # send a random number to the client and print what number it is in the server console
   # this is done in order


   rdt = random.sample(range(1,100),12)
   #randomnumber = random.randint(0,10)
   #print("The random number sent is: ",randomnumber)


   #c.send(b'Thank you for connecting')
   #c.send(b'%i'%randomnumber)
   bytes_to_send = b"(%i,%i,%i,%i,%i,%i)"%(1,rdt[0],2,rdt[1],3,rdt[2])
   print("sent this stuff",bytes_to_send)
   c.send(bytes_to_send)




   # Close the connection with the client
   c.close()