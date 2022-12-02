import os
from datetime import date
import pandas as pd

DATE = str(date.today())

# get the right working directory
root = os.getcwd()
FILENAME = "expenses_dataset.csv"

# dataset
file = os.path.join(root, FILENAME)


# Execute query
def query(DATE):
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
        #data = split_DATE(data)  # day, month, year as new column
        print("--saved--")
        #to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        #data = data.drop(to_drop, axis=1)
        data.to_csv("expenses_dataset.csv", index=False)
        print(data)
        return data

    # check if a dataset already exist
    try:
        data = pd.read_csv(file)
        frames = [df, data]
        data = pd.concat(frames)
        #data = split_DATE(data)  # day, month, year as new columns
        print("--saved--")
        #to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        #data = data.drop(to_drop, axis=1)
        data.to_csv("expenses_dataset.csv", index=False)
        print(data)
        return data

    # if not, create one
    except:
        store_in_new_ds(df)
        print('\n--->new dataset "expenses_dataset.csv"  was successfully created.\n')


# useful functions: ( later outscourced to own file: "mainly_used_functions" )


if __name__ == "__main__":
    store(DATE, query(DATE))