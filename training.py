import pandas as pd
import numpy as np
import matplotlib.pyplot as pt
from sklearn import linear_model
from sklearn import metrics
from keras import models
from keras import layers
import pickle


df=pd.read_csv("C://Users//Dell//Desktop//SNU//Seventh Semester//Data Mining//Project//Data//finalData.csv")
dfW=pd.read_csv("C://Users//Dell//Desktop//SNU//Seventh Semester//Data Mining//Project//Data//Wastage.csv")
itemset=df["Menu"].str.upper().unique()
#print(sorted(itemset))
hm={}
dates=df["Date"].unique()
print(len(itemset))

mean=dfW["TOTAL"].mean()
sd=dfW["TOTAL"].std()
#print(mean)
#print(sd)
def check(wastage):
    #print(wastage)
    if wastage>=(mean-(.5*sd)) and wastage<=(mean+(.5*sd)):
        #print(wastage)
        #print(1)
        return 1
    elif wastage<(mean-(.5*sd)):
        #print(wastage)
        #print(0)
        return 0
    elif wastage>(mean+(.5*sd)):
        #print(wastage)
        #print(2)
        return 2


df1=pd.DataFrame(columns=range(len(itemset)))
df2=pd.DataFrame(columns=["Date","Output"])

for i in range(len(itemset)):
    hm[itemset[i]]=i
#print(hm[itemset[0]])


for i in range(len(dates)):
    #print(i)
    #print("==========================================================")
    day_Items=df.groupby("Date").get_group(dates[i])
    #print(dfW.groupby("DATE").get_group(dates[i])["TOTAL"])
    x1=dfW.groupby("DATE").get_group(dates[i])["TOTAL"].tolist()
    #print(x1[0])
    df2.loc[i]=[dates[i],check(x1[0])]
    #print(day_Items)
    lst = [0] * len(itemset)
    for j in range(len(day_Items)):  
        #print(hm[day_Items["Menu"].iloc[j]])
        lst[hm[day_Items["Menu"].iloc[j].upper()]]=1
    #print("==========================================================")
    #print(lst[68])    
    df1.loc[i]=np.array(lst)

#print(df1)
#print(df2["Output"]==0)
#print(df2.iloc(df2["Output"]==0))
#print(len(df2.iloc(df2["Output"]==2)))
'''
print("===============================================")
print(df2.groupby('Output').get_group(0)["Date"])
print("===============================================")
print(df2.groupby('Output').get_group(1)["Date"])
print("===============================================")
#print()
print("===============================================")
print()
'''
del df2["Date"]
df2=pd.get_dummies(df2,prefix=['Output'])
msk = np.random.rand(len(df1)) < 0.8
train_X=df1[msk]
train_X = train_X.reset_index(drop=True)

train_Y=df2[msk]
train_Y = train_Y.reset_index(drop=True)

test_X=df1[~msk]
test_X = test_X.reset_index(drop=True)

test_Y=df2[~msk]
test_Y = test_Y.reset_index(drop=True)


#NeuralNetwork
model = models.Sequential()
# Input - Layer
model.add(layers.Dense(50, activation = "relu", input_shape=(len(itemset),)))
# Hidden - Layers
model.add(layers.Dropout(0.3, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))
model.add(layers.Dropout(0.2, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))
model.add(layers.Dropout(0.2, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))
# Output- Layer
model.add(layers.Dense(3, activation = "sigmoid"))
model.summary()
# compiling the model
model.compile( optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])

results = model.fit( train_X, train_Y, epochs= 100, batch_size = 2, validation_data = (test_X, test_Y))
model.save("trained_weights.h5")
print("Test-Accuracy:", np.mean(results.history["val_acc"]))

