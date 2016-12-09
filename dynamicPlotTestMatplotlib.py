# An elementary example of dynamically updating plotter with only Matplotlib 
# This is not a very nice option and it tends to freeze 
# because Matplotlib is designed for presentation plots, not for dynamic plotting


import matplotlib.pyplot as plt
import numpy as np
import time
plt.ion() ## Note this correction
#fig=plt.figure()
#plt.axis([0,1000,0,1])

i=0
x=np.linspace(0,3)
#y=list()

while i <1000:
    temp_y=np.random.random()
    #x.append(i)
    #y.append(temp_y)
    plt.axis([0,3,0,20])
    #plt.scatter(i,temp_y)
    y = (x+i)**2
    plt.scatter(x,y)
    i+=1
    plt.draw()
    plt.pause(0.0001) #Note this correction
    time.sleep(1)
    plt.cla()