from efficient_apriori import apriori
import pandas as pd
import numpy as np 


def check(wastage,df,dfW):
    #print(wastage)
    mean=dfW["TOTAL"].mean()
    sd=dfW["TOTAL"].std()
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

def unique(highwst_data,lowwst_data):
    high = set()
    low = set()
    for items in highwst_data:
        for item in items:
            high.add(item)
    for items in lowwst_data:
        for item in items:
            low.add(item)
    high_intersection = high.intersection(low)
    #print(high_intersection)
    # print("==========================================================")
    # print(high_intersection)
    # print("==========================================================")
    
    high_list = []
    for items in highwst_data:
        #print("my list is :=============================")
        temp = []
        for i in range(len(items)):
            if(high_intersection.__contains__(items[i])==False):
                temp.append(items[i])
                #print(item)
        # print("AAfter List is:=============")
        # print(items)
        high_list.append(tuple(temp))
    #print(high_list)
    return high_list




def apr():
    df=pd.read_csv("Data//finalData.csv")
    dfW=pd.read_csv("Data//Wastage.csv")
    itemset=df["Menu"].str.upper().unique()
    dates=df["Date"].unique()
    df1=pd.DataFrame(columns=range(len(itemset)))
    df2=pd.DataFrame(columns=["Date","Output"])
    for i in range(len(dates)):
        #print(i)
        #print("==========================================================")
        day_Items=df.groupby("Date").get_group(dates[i])
        #print(dfW.groupby("DATE").get_group(dates[i])["TOTAL"])
        x1=dfW.groupby("DATE").get_group(dates[i])["TOTAL"].tolist()
        #print(x1[0])
        df2.loc[i]=[dates[i],check(x1[0],df,dfW)]
        #print(day_Items)
        lst = [0] * len(itemset) 
        df1.loc[i]=np.array(lst)
    df_dates = df2.groupby('Output').get_group(2)["Date"].reset_index(drop=True)
    df_dates_low = df2.groupby('Output').get_group(0)["Date"].reset_index(drop=True)
    highwst_data = []
    lowwst_data = []
    #apr_data = []
    for i in range(len(df_dates)):
        #print(df_dates[i])
        highwst_data.append(list(df.groupby('Date').get_group(df_dates[i])['Menu'].str.upper().unique()))
    # print("==========================================================")
    #print(highwst_data)
    # print("==========================================================")
    for j in range(len(df_dates_low)):
        lowwst_data.append(list(df.groupby('Date').get_group(df_dates_low[j])['Menu'].str.upper().unique()))
    
    apr_data = unique(highwst_data,lowwst_data)

    itemsets, rules = apriori(apr_data, min_support=0.1,  min_confidence=0.5)
    print(itemsets)
    print(rules)
apr()



