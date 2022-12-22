import os
import pandas as pd

# split DATE into seperatet columns
def split_DATE(data):
    # splits the DATE column in to three new_columns:
    new_columns = data["DATE"].str.split("-", expand=True)
    data["day"] = new_columns[2]
    data["month"] = new_columns[1]
    data["year"] = new_columns[0]
    return data

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
        
        # save all the datasets into one folder "datasets"
        # folder = "datasets"
        # folder_PATH = os.path.join(root, folder)
        # if not os.path.exists(folder_PATH):
        #     os.mkdir(folder_PATH)  # create folder "datasets" 

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

# get the right working directory
root = os.getcwd()
FILENAME = "expenses_dataset.csv"

# dataset
file = os.path.join(root, FILENAME)