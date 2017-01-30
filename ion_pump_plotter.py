import matplotlib.pyplot as plt
import numpy as np
import time
import os.path
import datetime


# Reading configurations settings and data


import configparser 


def data_collection():
	
	configs = configparser.ConfigParser()
	configs.read("settings.ini")
	date = configs.get("General","DayToStart")
	dropboxpath = configs.get("General","DropboxPath")
	timetoplot = float(configs.get("General","TimeToPlot"))

	if date == "today" or date == "Today":
		date = time.strftime("%d%m%Y")
		filename_pump = dropboxpath+date+"pump2.txt"
	else:
		filename_pump = dropboxpath+date+"pump2.txt"
		file_exists = os.path.isfile(filename_pump)
		if not file_exists:
			print("That date doesn't exist, plotting for today")
			date = time.strftime("%d%m%Y")
			filename_pump = dropboxpath+date+"pump2.txt"

	with open(filename_pump) as file_imp:
		data = file_imp.readlines()

	file_imp.close()

	return (data,timetoplot)


def format_data(data,plottingtime):
	time_standard = datetime.datetime.now()
	timenow = (time_standard.hour,time_standard.minute)
	pressure_values = []

	for line in data: 
		wrds = line.split()
		pressure_val = float(wrds[5])
		hour_val = float(wrds[2])
		minute_val = float(wrds[3])
		totalminutes = 60*hour_val + minute_val
		if totalminutes >= (timenow[0]*60 + timenow[1] - plottingtime):
			pressure_values.append(pressure_val)

	return pressure_values
	


plt.ion() ## Note this correction
fig=plt.figure()


while True:
    #x.append(i)
    #y.append(temp_y)
    #plt.axis([0,3,0,20])
    #plt.scatter(i,temp_y)

    dt1 = data_collection()
    pvs = format_data(dt1[0],dt1[1])
   
    plt.plot(pvs)
    plt.title("Pump 2, pressure in mbar")
    plt.draw()
    plt.pause(0.0001) #Note this correction
    time.sleep(60)
    plt.clf()
    print("Plotting next data point, everything is good")