import glob
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from datetime import datetime
from keras.models import load_model
from predictor import predict

# from keras.utils.np_utils import to_categorical
# from keras.models import Sequential, load_model
# from keras.layers import Dense, Conv2D, MaxPool2D, Dropout, Flatten, BatchNormalization
# from keras.optimizers import Adam
# from keras.preprocessing.image import ImageDataGenerator
# from keras.callbacks import ReduceLROnPlateau

# def predict(pathname):
# 	return "NG"

def get_current_time(filename=False):
	now = datetime.now()
	if filename:
		return now.strftime("%Y-%d-%m-%H-%M-%S")
	return now.strftime("%d/%m/%Y %H:%M:%S")

def save_ng(file):
	current_time = get_current_time()

	report = "-"*70 + "\n\
	No-logo detected\n\
	Time: " + current_time + "\n\
	Location: Saigon Hi-Tech Park\n\
	Filename: " + latest_file + "\n"

	file.write(report)

MODEL_PATH = "efficient_net_v3.h5"

if __name__ == "__main__":
	model = load_model(MODEL_PATH)
	log_filename = get_current_time(filename=True) + ".txt"
	with open(log_filename, "w+") as log_file:
		count_total = 0
		count_ng = 0
		print("Logo detector")

		while True:
			print("="*79)
			user_request = input("Press Enter to continue, S + Enter to stop ...")
			if (user_request != ""):
				break

			""" Load the latest photo """
			IMAGE_DIR = "C:\\Users\\Pazabol\\Downloads"
			list_of_files = glob.glob(IMAGE_DIR + '\\*')
			latest_file = max(list_of_files, key=os.path.getctime)
			print("Image path:", latest_file)

			""" Predict """
			verdict = predict(model, latest_file)
			print("Verdict:", verdict)
			count_total += 1
			print("Total:", count_total)
			if verdict == "NG":
				count_ng += 1
			print("NG:", count_ng, "-- OK:", count_total -count_ng)

			""" Save NG """
			if (verdict == "NG"):
				save_ng(log_file)

	print("Log file saved at " + log_filename)
