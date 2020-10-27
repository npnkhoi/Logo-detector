"""
Backend of the system
	facilitate the data flow 
	between camera, models and frontend
"""

from models.bottle import predict as is_bottle_visible
from models.logo import predict as is_logo_visible
from time import sleep
import cv2 

INTERVAL = 200 # 200 miliseconds as system's interval

def detect_logo():
	"""
	Detect logo on the bottle
	- Record in log file
	- Send request to Frontend (by creating new file)
	"""

if __name__ == "__main__":
	vid = cv2.VideoCapture(0) 
	while True:
		# get an image, show it out

		# Capture the video frame by frame 
		ret, frame = vid.read()
		# Display the resulting frame
		cv2.imshow('frame', frame)
		print(type(frame))

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if is_bottle_visible(frame):
			print("Bottle visible? YES!")
			detect_logo()
			# TODO: notify Frontend about the bottle's appearance
			
			# wait until new bottle appears
			sleep(3000)
		else:
			print("Bottle visible? NO ...")

		# WARNING: system interval = INTERVAL 
		# + time wait for new bottle + processing time
	
	# After the loop release the cap object 
	vid.release() 
	# Destroy all the windows 
	cv2.destroyAllWindows() 