import pandas as pd
from datetime import date
import os

date = str(date.today())

# get the right working directory
root = os.getcwd()
filename = 'expenses_dataset.csv'

# dataset
file = os.path.join(root,filename)


# Execute query
def query(date):
    expense = str(input("what have you spent money on : ")).lower()
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

# store query in dataset (ds)
def store(date, df):
    '''
    check if a dataset already exists? 
    
    
            ---> If not, create one
            
            ---> If yes, save the query in the dataset. 
    '''  
      
    def store_in_new_ds(df):
        '''
        stores the query-result in a new dataset.
        
        '''
        data = pd.DataFrame(columns= ["expense", "amount",  "importance", "category","date"]) 
        frames = [df, data]
        data = pd.concat( frames)
        data.to_csv("expenses_dataset.csv", index=False)
        print('--saved--')
        print(data)
        return data 

    # check if a dataset already exist 
    try:
        data = pd.read_csv(file)
        frames = [df, data]
        data = pd.concat(frames)
        data.to_csv("expenses_dataset.csv", index=False)
        print('--saved--')
        print(data)
        return data 
    
    # if not, create one 
    except:
        store_in_new_ds(df)
        print('\n--->new dataset "expenses_dataset.csv"  was successfully created.\n')
        
        


  
if __name__ == "__main__":
    store(date, query(date))
