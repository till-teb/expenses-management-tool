import os
import datetime
import pandas as pd
import calendar
from useful_functions import split_DATE

DATE = (datetime.date.today())
DAY = calendar.day_name[DATE.weekday()]


# get the right working directory
root = os.getcwd()
FILENAME = "datasets\\day_label.csv"

# dataset
file = os.path.join(root, FILENAME)

def day_input(date, day):
    """
    Function to give input for day label.
    """
    print(f"Today is {day}, {date}")
    day_label = input(
        """
        How do you feel today?
        1 - good
        0 - bad
        
        Your answer:
        """)
        
    df = pd.DataFrame({
        "DATE": [str(DATE)],
        "day_name": [DAY],
        "label": [day_label]
        })
    
    print(df)
    return df


def store(df):
    """
    check if a dataset already exists? 
    
    
            ---> If not, create one in datasets folder
            
            ---> If yes, save the query in the dataset. 
    """
    def store_in_new_ds(df):
        """
        stores the day_label in a new dataset.
        
        """
        df = split_DATE(df)  # day, month, year as new columns
        print("--saved--")
        to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        df = df.drop(to_drop, axis=1)
        
        folder = "datasets"
        folder_PATH = os.path.join(root, folder) 
        if not os.path.exists(folder_PATH):
            os.mkdir(folder_PATH) #create folder "datasets"
            
        df.to_csv(FILENAME, index=False)
        print(df)
        return df
    
    # check if a dataset already exist
    try:
        df = split_DATE(df)  # day, month, year as new columns
        data = pd.read_csv(file)
        frames = [df, data]
        data = pd.concat(frames)
        to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        data = data.drop(to_drop, axis=1)
        data.to_csv(FILENAME, index=False)
        print("--saved--")
        print(data)
        return data

    # if not, create one
    except:
        store_in_new_ds(df)
        print('\n--->new dataset "day_label.csv"  was successfully created.\n')
        

store(day_input(DATE, DAY))
        