import pandas as pd
from datetime import date
import os


root = os.getcwd()
filename = 'expenses_dataset.csv'
file = os.path.join(root,filename)

date = str(date.today())









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
    
   data = pd.read_csv(file)
   frames = [df, data]
   data = pd.concat(frames)
   data.to_csv("expenses_dataset.csv", index=False)
   print('--saved--')
   print(data)
   return data 














storage(query(date))
print('------------------')
