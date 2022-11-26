import os
from datetime import date
import pandas as pd

date = str(date.today())

# get the right working directory
root = os.getcwd()
filename = "expenses_dataset.csv"

# dataset
file = os.path.join(root, filename)


# Execute query
def query(date):
    expense = str(input("what have you spent money on : ")).lower()
    amount = float(input("how much money have you spent : "))
    importance = int(input("how important was your expense? (1-4) : "))
    category = int(
        input(
            """please choose the category:

                       (1) x
                       (2) x
                       (3) x
                       ...
                       """
        )
    )

    df = pd.DataFrame(
        {
            "expense": [expense],
            "amount": [amount],
            "category": [category],
            "importance": [importance],
            "date": [date]
            
            
            
            ,
        }
    )
    return df


# store query in dataset (ds)
def store(date, df):
    """
    check if a dataset already exists? 
    
    
            ---> If not, create one
            
            ---> If yes, save the query in the dataset. 
    """

    def store_in_new_ds(df):
        """
        stores the query-result in a new dataset.
        
        """
        data = pd.DataFrame(
            columns=["expense", "amount", "importance", "category", "date"]
        )
        frames = [df, data]
        data = pd.concat(frames)
        data = split_dates(data)  # day, month, year as new columns
        data.to_csv("expenses_dataset.csv", index=False)
        print("--saved--")
        to_drop = ['date'] # only columns: day, month, year column are nessesary
        data = data.drop(to_drop, axis=1)
        print(data)
        return data

    # check if a dataset already exist
    try:
        data = pd.read_csv(file)
        frames = [df, data]
        data = pd.concat(frames) 
        split_dates(data) # day, month, year as new columns
        data.to_csv("expenses_dataset.csv", index=False)
        print("--saved--")
        to_drop = ['date']  # only columns: day, month, year column are nessesary
        data = data.drop(to_drop, axis=1)
        print(data)
        return data

    # if not, create one
    except:
        store_in_new_ds(df)
        print('\n--->new dataset "expenses_dataset.csv"  was successfully created.\n')
    
    
    
    
# useful functions: ( later outscourced to own file: "mainly_used_functions" )
    
    
# split date into seperatet columns
def split_dates(data):
    #splits the date column in to three new_columns:
    new_columns = data['date'].str.split('-', expand= True) 
    data['day'] = new_columns[2]
    data['month'] =new_columns[1]
    data['year'] =new_columns[0]
    return data
    
    
    
    
    
    
    
    
    
    
    
    
    

if __name__ == "__main__":
    store(date, query(date))
