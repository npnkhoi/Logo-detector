import cv2
import numpy as np
import matplotlib.pyplot as plt
# from keras.utils.np_utils import to_categorical
# from keras.models import Sequential, load_model
# from keras.layers import Dense, Conv2D, MaxPool2D, Dropout, Flatten, BatchNormalization
# from keras.optimizers import Adam
# from keras.preprocessing.image import ImageDataGenerator
# from keras.callbacks import ReduceLROnPlateau


def start_crop(img, h, w):
  edge = cv2.Canny(img.astype(np.uint8), 50, 60)
  whole_area = h * w
  count_all = np.count_nonzero(edge)
  thick_area = h * 5
  for c_l in range(0, w-5, 5):
    thick_c = edge[:, c_l:c_l+5]
    count = np.count_nonzero(thick_c)
    if count / thick_area > count_all / whole_area:
      if w - c_l < h:
        c_l = c_l - (h - (w - c_l))
      return c_l
  return abs(h - w) // 2

def crop_center(img):
  h = img.shape[0]
  w = img.shape[1]
  upper_bound = start_crop(img, h, w)
  if (h > w):
      return img[(upper_bound) : (upper_bound + w), :, :]
  else:
      return img[:, (upper_bound) : (upper_bound + h), :]

def predict(model, img_dir):
  test_tensor = plt.imread(img_dir)
  test_tensor = cv2.resize(crop_center(test_tensor), (380, 380))
  test_batch = test_tensor.reshape([1] + list(test_tensor.shape))
  predict_arr = model.predict(test_batch)
  predict = np.argmax(predict_arr[0])
  return "OK" if predict == 1 else "NG"