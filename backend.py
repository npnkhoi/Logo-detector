"""
Script to facilitate data flow between camera, models and frontend.

For user:
- Press 'C' to detect logo on a passing bottle (manual mode)
- Press 'Q' to exit the program

For dev:
- `pip install` all the packages
- create a folder named `Logs\\` in the same level as this file
- make sure the model 'efficient_net_v3.h5' is put in 'models\\' folder
- You can either choose to detect the bottle manually or automatically by changing the constant `MANUAL`
"""

from models.detect_bottle import detect_bottle
from models.logo import predict as is_logo_visible
from time import sleep
from datetime import datetime
import cv2
from keras.models import load_model
import keyboard
from copy import deepcopy

# CONSTANTS =========================================================================

MODEL_PATH = "models\\efficient_net_v3.h5"
MANUAL = False

model = load_model(MODEL_PATH)
vid = cv2.VideoCapture(0) # PRODUCTION: maybe change 0 to 1
is_bottle_passing = False
count_ng = 0
count_ok = 0
last_bottle_status = False

# FUNCTIONS ===================================================================

def is_bottle_visible(img, manual):
	"""
	MANUAL: pressing 'C' to notify that a bottle is going through
	AUTO: using ML to detect
	"""
	if manual:
		return keyboard.is_pressed('c')
	else:
		visible = detect_bottle(img)
		global last_bottle_status
		if visible != last_bottle_status:
			last_bottle_status = visible
			return visible
		else:
			return False

def detect_logo(model, image, time):
	"""
	Detect logo on the bottle
	- Record in log file
	- Send request to Frontend (by creating new file)
	"""
	verdict = is_logo_visible(model, image)
	print('Verdict:', 'OK' if verdict else 'NG')
	global count_ok, count_ng
	if verdict:
		count_ok += 1
	else:
		count_ng += 1
		file_path = 'Logs\\' + format_time(time, 2) + '.jpg'
		cv2.imwrite(file_path, image)
		save_ng(LOG_PATH, file_path, time)

def get_frame(vid):
	ret, frame = vid.read()
	image = deepcopy(frame)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, format_time(now, 1), (20, 20), font, 0.5, (0, 0, 0), 2)
	cv2.putText(frame, 'Total: ' + str(count_ok + count_ng), (20, 40), font, 0.5, (0, 0, 0), 2)
	cv2.putText(frame, 'OK: ' + str(count_ok), (20, 60), font, 0.5, (0, 255, 0), 2)
	cv2.putText(frame, 'NG: ' + str(count_ng), (20, 80), font, 0.5, (0, 0, 255), 2)
	cv2.imshow('frame', frame)
	return image

def destroy_cam():
	vid.release() 
	cv2.destroyAllWindows() 

def format_time(time, type):
	if type == 1:
		return time.strftime("%d/%m/%Y %H:%M:%S.%f")
	else:
		return time.strftime("%Y-%d-%m-%H-%M-%S")

def save_ng(log_path, image_path, time):
	with open(log_path, 'a') as file:
		report = "-"*70 + "\n\
		No-logo detected\n\
		Time: " + format_time(time, 1) + "\n\
		Location: Saigon Hi-Tech Park\n\
		Filename: " + image_path + "\n"
		file.write(report)

# MAIN  ================================================================================

LOG_PATH = "Logs\\" + format_time(datetime.now(), 2) + ".txt"

if __name__ == "__main__":
	open(LOG_PATH, 'w+')
	while True:
		now = datetime.now()
		image = get_frame(vid)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		# if keyboard.is_pressed('c'):
		if is_bottle_visible(image, manual=MANUAL):
			print('Bottle is passing')
			detect_logo(model, image, now)
	
	destroy_cam()