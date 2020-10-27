"""
Backend of the system
	facilitate the data flow 
	between camera, models and frontend
"""

from models.detect_bottle import detect_bottle as is_bottle_visible
from models.logo import predict as is_logo_visible
from time import sleep
from datetime import datetime
import cv2
from keras.models import load_model

INTERVAL = 200 # 200 miliseconds as system's interval

def detect_logo():
	"""
	Detect logo on the bottle
	- Record in log file
	- Send request to Frontend (by creating new file)
	"""
MODEL_NAME = "models\\efficient_net_v3.h5"

if __name__ == "__main__":
	model = load_model(MODEL_NAME)
	vid = cv2.VideoCapture(0) 
	while True:
		# Capture the video frame by frame 
		ret, frame = vid.read()
		# Display the resulting frame
		cv2.imshow('frame', frame)
		# print(type(frame))

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		print('Time:', str(datetime.now()))
		if is_bottle_visible(frame):
			print("Bottle visible? YES!")
			if is_logo_visible(model, frame):
				print('OK')
				
			else:
				print('NG')
			# TODO: notify Frontend about the bottle's appearance
		else:
			print("Bottle visible? NO ...")

		# WARNING: system interval = INTERVAL 
		# + time wait for new bottle + processing time
	
	# After the loop release the cap object 
	vid.release() 
	# Destroy all the windows 
	cv2.destroyAllWindows() 