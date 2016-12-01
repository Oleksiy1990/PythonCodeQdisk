"""
This script reads and parses the settings from the OvenControl1.dat or another number 
and produces the output with the thermocouple number and the corresponding 
settings from the program
"""




import re
import time
import numpy as np
import sys
import datetime



filenames_ovensettings = ["C:\\SrMic\\TempControl\\Version 1\\OvenControl1",
	"C:\\SrMic\\TempControl\\Version 2\\OvenControl2",
	"C:\\SrMic\\TempControl\\Version 3\\OvenControl3"]
#filenames_ovensettings = ['OvenControl1','OvenControl2',"OvenControl3"] #don't put .dat here
directory_for_saving = ["SavedSettings\\"]

while True:

	lines = []
	for file in filenames_ovensettings:
		with open(file+".dat","r") as f:
		    lines.append(f.readlines()) #with statement automatically closes file
	
	
	"""
	Save the data from all thermocouples, including those which are not controlled
	"""
	for numl,l in enumerate(lines): # this loops through the results from different files
	#sys.exit(0)
		thermocouple_num = []
		min_Tlimit = []
		max_Tlimit = []
		percent_permin = []

		for num,q in enumerate(l):
			m = re.match("\d{1,2}[c ]",q) #Must be "c" OR one space after the number

			if m is not None:
				m = m.group()
				m = re.sub("c","",m)
				thermocouple_num.append(int(m))
				min_Tlimit.append(float(l[num+5]))
				max_Tlimit.append(float(l[num+6]))
				percent_permin.append(float(l[num+9]))

		datenow = datetime.datetime.now().strftime("%d%m%Y")
		filename_towrite = "Version %.i\\SavedSettings\\"%(numl+1)+"settings"+datenow+".txt"
		filename_explanation = "Version %.i\\SavedSettings\\"%(numl+1)+"structure"+datenow+".txt"
		timestamp_now = datetime.datetime.now().strftime("%H:%M:%S") 
		data_output = np.column_stack([thermocouple_num,percent_permin,min_Tlimit,max_Tlimit])


		structure_output = "timestamp thermocouple percentchange_per_min set_minTlimit set_maxTlimit\n"
		#DO NOT change this line unless the structure of the output has changed

		datafile_out = open(filename_towrite,"a")
		
		for iline in data_output:
		 	datafile_out.write("%s %.i %.5f %.3f %.3f"%(timestamp_now,iline[0],iline[1],iline[2],iline[3])+"\n")
		
		datafile_out.close()

		expl_file = open(filename_explanation,"a")
		expl_file.write(timestamp_now+" "+structure_output)
		expl_file.close()

	"""
	Save data only from the thermocouples that have a controlling MOSFET at them, so with "c"
	"""

	for numl,l in enumerate(lines): # this loops through the results from different files

		

		thermocouple_num = []
		min_Tlimit = []
		max_Tlimit = []
		percent_permin = []

		for num,q in enumerate(l):
			m = re.match("\d{1,2}[c]",q) #Must be "c" after the number

			if m is not None:
				m = m.group()
				m = re.sub("c","",m)
				thermocouple_num.append(int(m))
				min_Tlimit.append(float(l[num+5]))
				max_Tlimit.append(float(l[num+6]))
				percent_permin.append(float(l[num+9]))

		datenow = datetime.datetime.now().strftime("%d%m%Y")
		filename_towrite = "Version %.i\\SavedSettings\\"%(numl+1)+"settings"+datenow+"MOSFET.txt" 
		filename_explanation = "Version %.i\\SavedSettings\\"%(numl+1)+"structure"+datenow+"MOSFET.txt"

		timestamp_now = datetime.datetime.now().strftime("%H:%M:%S") 
		data_output = np.column_stack([thermocouple_num,percent_permin,min_Tlimit,max_Tlimit])


		structure_output = "timestamp thermocouple percentchange_per_min set_minTlimit set_maxTlimit\n"
		#DO NOT change this line unless the structure of the output has changed

		datafile_out = open(filename_towrite,"a")
		
		for iline in data_output:
		 	datafile_out.write("%s %.i %.5f %.3f %.3f"%(timestamp_now,iline[0],iline[1],iline[2],iline[3])+"\n")
		
		datafile_out.close()

		expl_file = open(filename_explanation,"a")
		expl_file.write(timestamp_now+" "+structure_output)
		expl_file.close()


	print("Running in an infinite loop\n Press CTRL+C to stop\n")
	print("Saved at "+timestamp_now)
	time.sleep(5*60) # 5 minutes 
		
		

