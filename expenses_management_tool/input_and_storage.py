import pandas as pd
from datetime import date
date = str(date.today())



def storage(df):
    i = 1
    if i == 1:
        data = pd.DataFrame()
    else:
        data = pd.read_csv("expenses_dataset.csv")
        frames = [df, data]
        data = pd.concat(frames)
        data.to_csv("expenses_dataset.csv", index=False)
        print('--saved--')
        return (data)
    yield  





def input_query(date):
    expense = str(input("what have you spent money on : "))
    amount = float(input("how much money have you spent : "))
    importance = int(input("how important was your expense? (1-4) : "))
    category = int(input('''please choose the category:

                       (1) x
                       (2) x
                       (3) x
                       ...
                       '''))

    df = pd.DataFrame({"category": [category],
                       "importance": [importance],
                       "amount":[amount] ,
                       "expense": [expense],
                       "date": [date]})
    return(df)










storage(input_query(date))