import os
from datetime import date
import pandas as pd
from useful_functions import split_DATE


DATE = str(date.today())

# get the right working directory
root = os.getcwd()
FILENAME = "expenses_dataset.csv"

# dataset
file = os.path.join(root, FILENAME)


# Execute query
def query(DATE):
    regular_exp = 0
    expense = str(input("what have you spent money on : ")).lower()
    amount = float(input("how much money have you spent : "))
    importance = int(input("how important was your expense? (1-4) : "))
    category = int(
        input(
            """
(1) Food 
(2) consumer goods
(3) transportation
(4) house expenses
(5) free time expenses
(6) insurance + taxes
(7) bank + savings investments
(8) other + extraordinary expenses 
                       """
        )
    )

    df = pd.DataFrame(
        {
            "expense": [expense],
            "amount": [amount],
            "category": [category],
            "importance": [importance],
            "DATE": [DATE],
            "regular": [regular_exp]
        }
    )
    return df


# store query in dataset (ds)
def store(DATE, df):
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
            columns=["expense", "amount", "importance", "category", "DATE"]
        )
        frames = [df, data]
        data = pd.concat(frames)
        data = split_DATE(data)  # day, month, year as new column
        print("--saved--")
        to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        data = data.drop(to_drop, axis=1)
        
        folder = "datasets"
        folder_PATH = os.path.join(root, folder) 
        if not os.path.exists(folder_PATH):
            os.mkdir(folder_PATH) #create folder "datasets"
        
        data.to_csv(FILENAME, index=False)
        print(data)
        return data

    # check if a dataset already exist
    try:
        df = split_DATE(df)  # day, month, year as new columns
        data = pd.read_csv(file)
        frames = [df, data]
        data = pd.concat(frames)
        print("--saved--")
        to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        data = data.drop(to_drop, axis=1)
        data.to_csv(FILENAME, index=False)
        print(data)
        return data

    # if not, create one
    except:
        store_in_new_ds(df)
        print('\n--->new dataset "expenses_dataset.csv"  was successfully created.\n')





def query_regular_expenses():
     pass
    
    
    
    
    

# useful functions: ( later outscourced to own file: "mainly_used_functions" )


if __name__ == "__main__":
    store(DATE, query(DATE))    # fuction to query and store expense