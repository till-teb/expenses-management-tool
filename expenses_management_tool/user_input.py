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
    item = str(input("what have you spent money on : ")).lower()
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
            "item": [item],
            "amount": [amount],
            "category": [category],
            "importance": [importance],
            "DATE": [DATE],
            "regular": [regular_exp]
        }
    )
    return df


# store query in dataset (ds)
def store(df):
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
            columns=["item", "amount", "importance", "category", "DATE"]
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
            os.mkdir(folder_PATH)  # create folder "datasets"

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

    return





def query_regular_expenses():
    regular_exp = int(1)
    expense = str(input("what is your regular expense: ")).lower()
    amount = float(input("how much money do you need to speend regular: "))
    importance = int(input("how important is your regular expense? (1-4) : "))
    every_x_month = int(input(""" 
                              1 = every month
                              2 = every second month
                              3 = every third month 
                              ...
                              
                              how often does the expense occur monthly? :
                                  
                              """))
    every_x_day = int(input("""
                              1 = first day of month
                              2 = second day of month
                              3 = third day of month 
                              ...
                              
                              On which day of the month the expense is debited? :
                                  
                              """))
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

    start_date = str(
        input("""should the entry start 
              (1) from today 
              (2) retroactively to 1.1.  
              
              """)
              )
              
    regular_bookings = pd.DataFrame(
        {
            "expense": [expense],
            "amount": [amount],
            "category": [category],
            "importance": [importance],
            "DATE": [DATE],
            "regular": [regular_exp],
            "frequency_monthly": [every_x_month],
            "frequency_dayly": [every_x_day]
        }
    )
    
#    ....
    
    
    
    
    

# useful functions: ( later outscourced to own file: "mainly_used_functions" )


if __name__ == "__main__":
    store(query(DATE))
