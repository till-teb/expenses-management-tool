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
    1. check if a folder for datasets already exists?
            ---> If not, create one
            ---> If yes, go into the folder directory
    2. check if a dataset already exists?
            ---> If not, create one
            ---> If yes, save the query in the dataset.
    """
    # save all the datasets into one folder "datasets"
    folder = "datasets"
    folder_PATH = os.path.join(root, folder)
    # create folder "datasets"
    if not os.path.exists(folder_PATH):
        os.mkdir(folder_PATH)
    # path to csv file in datasets folder
    datasets_PATH = os.path.join(folder_PATH, FILENAME)

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
        to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        data = data.drop(to_drop, axis=1)
        data.to_csv(datasets_PATH, index=False)
        return data

    # check if a dataset already exist
    try:
        df = split_DATE(df)  # day, month, year as new columns
        data = pd.read_csv(datasets_PATH)
        frames = [df, data]
        data = pd.concat(frames)
        to_drop = ["DATE"]  # only columns: day, month, year column are nessesary
        data = data.drop(to_drop, axis=1)
        data.to_csv(datasets_PATH, index=False)
        return data

    # if not, create one
    except:
        store_in_new_ds(df)

    return

# get the right working directory
root = os.getcwd()
FILENAME = "expenses_dataset.csv"
