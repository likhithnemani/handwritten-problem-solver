import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
# %matplotlib inline
import os
from os import listdir
from os.path import isfile, join
import pandas as pd


def load_images_from_folder(folder):
    train_data = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
        img = ~img
        if img is not None:
            ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            ctrs, ret = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
            w = int(28)
            h = int(28)
            maxi = 0
            for c in cnt:
                x, y, w, h = cv2.boundingRect(c)
                maxi = max(w*h, maxi)
                if maxi == w*h:
                    x_max = x
                    y_max = y
                    w_max = w
                    h_max = h
            im_crop = thresh[y_max:y_max+h_max+10, x_max:x_max+w_max+10]
            im_resize = cv2.resize(im_crop, (28, 28))
            im_resize = np.reshape(im_resize, (784, 1))
            train_data.append(im_resize)
    return train_data


def convert_img_to_csv():
    j = 0 
    for filename in os.listdir('model/dataset/extracted_images/'):
        print(filename)
        temp_data=load_images_from_folder('model/dataset/extracted_images/'+filename)
        len(temp_data)
        for i in range(0,len(temp_data)):
            temp_data[i]=np.append(temp_data[i],[j])
        if j == 0:
            data = temp_data
        else:
            data=np.concatenate((data,temp_data))
        j = j + 1
        print(len(data))
    df=pd.DataFrame(data,index=None)
    df.to_csv('model/train_final.csv',index=False)
    return True