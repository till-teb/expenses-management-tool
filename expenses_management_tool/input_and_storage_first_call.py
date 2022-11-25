# first time

import pandas as pd
from datetime import date
date = str(date.today())

#data = pd.read_csv("expenses_dataset.csv")                          !!!












def query(date):
    expense = str(input("what have you spent money on : "))
    amount = float(input("how much money have you spent : "))
    importance = int(input("how important was your expense? (1-4) : "))
    category = int(input('''please choose the category:

                       (1) x
                       (2) x
                       (3) x
                       ...
                       '''))

    df = pd.DataFrame({"expense": [expense],
                       "amount":[amount] ,
                        "category": [category],
                       "importance": [importance],
                       "date": [date]})
    return(df)


def storage(df):
    
    
   data = pd.DataFrame(df)
    
    #data = pd.read_csv("expenses_dataset.csv")
    #frames = [df, data]
    # data = pd.concat(frames)
   data.to_csv("expenses_dataset.csv", index=False)
   print('--saved--')
   print(data)
   return data 














data = storage(query(date))
print('------------------')
print(data)