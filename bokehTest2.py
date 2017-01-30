import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models.sources import ColumnDataSource
from bokeh.client import push_session
from bokeh.driving import linear

def data_collection():
	
	configs = configparser.ConfigParser()
	configs.read("settings.ini") # This needs to have the correct path!
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


p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)