"""
Backend -- facilitate data flow between camera, models and frontend
"""

from models.detect_bottle import detect_bottle
from models.logo import predict as is_logo_visible
from time import sleep
from datetime import datetime
import cv2
from keras.models import load_model
import keyboard

INTERVAL = 200 # 200 miliseconds as system's interval

def is_bottle_visible(key_pressed, img, method):
	"""
	MANUAL: pressing 'C' to notify that a bottle is going through
	AUTO: using ML to detect
	"""
	if method == 'MANUAL':
		return key_pressed == 'c'
	else:
		return detect_bottle(img)

def detect_logo():
	"""
	Detect logo on the bottle
	- Record in log file
	- Send request to Frontend (by creating new file)
	"""
	pass

MODEL_PATH = "models\\efficient_net_v3.h5"
METHOD = "MANUAL"

if __name__ == "__main__":
	# Init
	model = load_model(MODEL_PATH)
	vid = cv2.VideoCapture(0) 
	is_bottle_passing = False

	while True:
		now = datetime.now()
		
		ret, frame = vid.read()
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, now.strftime("%Y:%d:%m %H:%M:%S.%f"), (30, 30), font, 0.5, (0, 0, 0),1)
		cv2.imshow('frame', frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		if keyboard.is_pressed('c'):
			print('Bottle is passing')

		# if is_bottle_visible(frame):
		# 	if is_bottle_passing:
		# 		continue
			
		# 	is_bottle_passing = True
		# 	print("Bottle visible? YES!")

		# 	# TODO: call logo detector
		# 	print(cv2.imwrite('bottle_images\\' + now + '.jpg', frame))

		# 	# TODO: notify Frontend about the bottle's appearance
		# elif is_bottle_passing:
		# 	is_bottle_passing = False
		# 	print("Bottle visible? NO ...")
	
	vid.release() 
	cv2.destroyAllWindows() 