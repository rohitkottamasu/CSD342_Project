import pandas as pd
from keras import models
from keras import layers
import numpy as np

df=pd.read_csv("C://Users//Dell//Desktop//SNU//Seventh Semester//Data Mining//Project//Data//finalData.csv")
dfW=pd.read_csv("C://Users//Dell//Desktop//SNU//Seventh Semester//Data Mining//Project//Data//Wastage.csv")
itemset=df["Menu"].str.upper().unique()
hm={}
#print(itemset)

for i in range(len(itemset)):
    hm[itemset[i]]=i


def take_input():
    input_file = open('input_menu.txt')
    input_menu = input_file.readlines()
    #print(input_menu)
    input_fin=[0]*len(itemset)
    for i in range(len(input_menu)):
        check=input_menu[i].split("\n")[0].upper()
        input_fin[hm[check]]=1
    return input_fin


model = models.Sequential()
# Input - Layer
model.add(layers.Dense(50, activation = "relu", input_shape=(164,)))
# Hidden - Layers
model.add(layers.Dropout(0.3, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))
model.add(layers.Dropout(0.2, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))
model.add(layers.Dropout(0.2, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))
# Output- Layer
model.add(layers.Dense(3, activation = "sigmoid"))
#model.summary()

model.load_weights('trained_weights.h5')

input = take_input()
input=np.array(input)
#print(input.shape)
check=np.reshape(input,(1,164,))
#print(check)
pred=model.predict(check)
pred=np.reshape(pred,(3,))
#print(pred.argmax(axis=0))
pred=pred.argmax(axis=0)
if(pred==0):
    print("Low Wastage for the given Menu")
elif(pred==1):
    print("Medium Wastage for the given Menu")
else:
    print("High Wastage for the given Menu Pls take care")
