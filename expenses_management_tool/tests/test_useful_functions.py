import pytest
import pandas as pd
import useful_functions as uf

def test_split_date():
    # df with formatted date
    from datetime import date
    today = date.today()
    df = pd.DataFrame({"DATE": [str(today)]})
    
    # split the date in DATE column
    df = uf.split_DATE(df)
    #drop DATE column
    df = df.drop("DATE", axis=1)
    
    # expected df
    day = date.today().day
    month = date.today().month
    year = date.today().year
    
    expected_df = pd.DataFrame({
        "day": [str(day).zfill(2)],  # leading zero format. 2 --> 02
        "month": [str(month).zfill(2)],
        "year": [str(year).zfill(2)]})
    
    assert df.equals(expected_df)
