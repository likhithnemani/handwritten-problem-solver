from sympy import *
import json
from keras.models import model_from_json
from PIL import Image
import cv2
import os
import cv2
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_data_format('channels_last')

dic = ['3',   
'(',   
'1',   
'4',   
'!',   
'A',   
'7',   
'9',   
'0',   
'+',   
'6',   
'5',   
'X',   
'e',   
']',   
'pi',
')',
'8',  
'*',   
'-',   
'/',
'2',
'z',
'[']


def load_model():
    json_file = open('model/model_final.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model/model_final.h5")
    return loaded_model


model = load_model()


def identify_letters_and_append(img):
    if img is not None:
        # images.append(img)
        img = ~img
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        ctrs, ret = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w = int(28)
        h = int(28)
        train_data = []
        # print(len(cnt))
        rects = []
        for c in cnt:
            x, y, w, h = cv2.boundingRect(c)
            rect = [x, y, w, h]
            rects.append(rect)
        # print(rects)
        bool_rect = []
        for r in rects:
            l = []
            for rec in rects:
                flag = 0
                if rec != r:
                    if r[0] < (rec[0]+rec[2]+10) and rec[0] < (r[0]+r[2]+10) and r[1] < (rec[1]+rec[3]+10) and rec[1] < (r[1]+r[3]+10):
                        flag = 1
                    l.append(flag)
                if rec == r:
                    l.append(0)
            bool_rect.append(l)
        # print(bool_rect)
        dump_rect = []
        for i in range(0, len(cnt)):
            for j in range(0, len(cnt)):
                if bool_rect[i][j] == 1:
                    area1 = rects[i][2]*rects[i][3]
                    area2 = rects[j][2]*rects[j][3]
                    if(area1 == min(area1, area2)):
                        dump_rect.append(rects[i])
        # print(len(dump_rect))
        final_rect = [i for i in rects if i not in dump_rect]
        # print(final_rect)
        for r in final_rect:
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            im_crop = thresh[y:y+h+10, x:x+w+10]

            im_resize = cv2.resize(im_crop, (28, 28))
            # cv2_imshow(im_resize)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            im_resize = np.reshape(im_resize, (1, 28, 28))
            train_data.append(im_resize)

        return train_data


def recognize_identified_characters(train_data, loaded_model):
    s = ''
    for i in range(len(train_data)):
        train_data[i] = np.array(train_data[i])
        train_data[i] = train_data[i].reshape(1, 28, 28, 1)
        result = np.argmax(loaded_model.predict(train_data[i]), axis=-1)
        s = s+dic[result[0]]

    s = s.replace("--", "=")
    s = s.replace("pi", "π")
    s = s.replace("times", "*")
    return s


def reconstruct_equation(s):
    t = ""
    for i in range(0, len(s)):
        if i != 0:
            if s[i].isdigit() and s[i-1].isalpha():
                t = t + '**'
            elif s[i].isalpha() and s[i-1].isdigit():
                t = t + '*'
        t = t + s[i]
    return t


def solve_linear_equation(s):
  t = reconstruct_equation(s)
  y = t
  t = t.replace('π','3.14')
  p = t.split('=')
  print(p)
  if len(p) >= 2:
    t = p[0]
    if p[1] != '+' or p[1] != '-':
      p[1] = '+' + p[1] 
    if p[1] != '0':
      for i in range(0,len(p[1])):
        if p[1][i] == '-':
          t = t + '+'
        elif p[1][i] == '+':
          t = t + '-'
        else:
          t = t + p[1][i]
  
  A,e,z = symbols('A e z')
  sol = solve(simplify(t))
  print(t)
  return sol,y


def basic_calculation(s):
    t = reconstruct_equation(s)
    t = t.replace('π', '3.14')
    print(s)
    x = eval(t)
    return x, s


def predict_solution(img):
    Image.open(img).save('temp.png')
    img = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)
    train_data = identify_letters_and_append(img)
    s = recognize_identified_characters(train_data, model)
    if (s.find('=') == -1):
        x, t = basic_calculation(s)
    else:
        print(s)
        print(len(s)-s.find('='))
        if len(s)-s.find('=')-1 == 0:
            x, t = basic_calculation(s[0:len(s)-1])
        else:
            x, t = solve_linear_equation(s)
    os.remove('temp.png')
    return x,t
