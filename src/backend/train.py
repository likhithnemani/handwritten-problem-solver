import pandas as pd
import numpy as np
import pickle
np.random.seed(1212)
import keras
from keras.models import Model
from keras.layers import *
from keras import optimizers
from keras.layers import Input, Dense
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_data_format('channels_last')
from keras.models import model_from_json
from keras.utils.np_utils import to_categorical
from preprocessing import convert_img_to_csv

def train_model():
    if 1:
        df_train=pd.read_csv('model/train_final.csv',index_col=False)
        labels=df_train[['784']]
        df_train.drop(df_train.columns[[784]],axis=1,inplace=True)
        df_train.head()
        labels=np.array(labels)
        cat=to_categorical(labels,num_classes=24)
        print(cat[0])
        x = len(df_train.axes[0])
        l=[]
        for i in range(x):
            l.append(np.array(df_train[i:i+1]).reshape(28,28,1))
        np.random.seed(7)

        model = Sequential()
        model.add(Conv2D(30, (5, 5), input_shape=(28,28,1), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(15, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(24, activation='softmax'))
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        model.fit(np.array(l), cat, epochs=30, shuffle=True)

        model_json = model.to_json()
        with open("model/model_final.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("model/model_final.h5")

if __name__ == '__main__':
    train_model()