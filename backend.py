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

# FUNCTIONS ===================================================================

def is_bottle_visible(key_pressed, img, method):
	"""
	MANUAL: pressing 'C' to notify that a bottle is going through
	AUTO: using ML to detect
	"""
	if method == 'MANUAL':
		return key_pressed == 'c'
	else:
		return detect_bottle(img)

def detect_logo(model, image):
	"""
	Detect logo on the bottle
	- Record in log file
	- Send request to Frontend (by creating new file)
	"""
	verdict = is_logo_visible(model, image)
	print('OK' if verdict else 'NG')
	global count_ok, count_ng
	if verdict:
		count_ok += 1
	else:
		count_ng += 1

def get_frame(vid):
	ret, frame = vid.read()
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, now.strftime("%d/%m/%Y %H:%M:%S.%f"), (20, 20), font, 0.5, (0, 0, 0), 2)
	cv2.putText(frame, 'Total: ' + str(count_ok + count_ng), (20, 40), font, 0.5, (0, 0, 0), 2)
	cv2.putText(frame, 'OK: ' + str(count_ok), (20, 60), font, 0.5, (0, 255, 0), 2)
	cv2.putText(frame, 'NG: ' + str(count_ng), (20, 80), font, 0.5, (0, 0, 255), 2)
	cv2.imshow('frame', frame)
	return frame

def destroy_cam():
	vid.release() 
	cv2.destroyAllWindows() 


# CONSTANTS =========================================================================

MODEL_PATH = "models\\efficient_net_v3.h5"
METHOD = "MANUAL"

model = load_model(MODEL_PATH)
vid = cv2.VideoCapture(0) 
is_bottle_passing = False
count_ng = 0
count_ok = 0

# MAIN  ================================================================================

if __name__ == "__main__":

	while True:
		now = datetime.now()
		image = get_frame(vid)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if keyboard.is_pressed('c'):
			print('Bottle is passing')
			detect_logo(model, image)
	
	destroy_cam()