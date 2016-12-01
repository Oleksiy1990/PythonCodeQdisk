import numpy as np 
import scipy as sp 
import matplotlib.pyplot as plt 
import time
import os.path

from bokeh.plotting import figure, output_file, show

import configparser 

configs = configparser.ConfigParser()
configs.read("settings.ini")
date = configs.get("General","DayToStart")

if date == "today" or date == "Today":
	date = time.strftime("%d%m%Y")
	filename_pump = date+"pump2.txt"
else:
	filename_pump = date+"pump2.txt"
	file_exists = os.path.isfile(filename_pump)
	if not file_exists:
		print("That date doesn't exist, plotting for today")
		date = time.strftime("%d%m%Y")
		filename_pump = date+"pump2.txt"

with open(filename_pump) as file_imp:
	data = file_imp.readlines()

file_imp.close()



p_values = []
x_vals = []

for line in data: 
	wrds = line.split()
	val = float(wrds[5])
	xv = wrds[1]
	p_values.append(val)
	x_vals.append(xv)

x = np.arange(len(p_values))

while True:
	
	output_file("lines.html")
	p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
	p.line(x, p_values, legend="Temp.", line_width=2)
	show(p)
	time.sleep(5)

print(p_values)
