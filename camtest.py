import cv2
import time
import sys

print("Capturing images from the camera")
print("Press CTRL+C to terminate the program")
counter = 0
try:
	while True:
		cam = cv2.VideoCapture(0)
		s, img = cam.read()
		cam.release()
		imgtime = time.localtime()
		cv2.imwrite("%s%s%s_%s%s%s.bmp" %  imgtime[0:6],img)
		time.sleep(5)


#line1 = float(input("first number "))
#line2 = float(input("second "))
#res = line1 + line2
#print(res)
		
except KeyboardInterrupt:
	print("OK, done")
	sys.exit(0)