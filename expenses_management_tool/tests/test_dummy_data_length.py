import expenses_management_tool.data_generator as dd

def test_dummy_data_length():
    expected_rows = 50
    data = dd.dummy_data(expected_rows)
    
    # Check if the number of rows in the data is matching the expected value
    assert len(data) == expected_rows, f"Expected rows: {expected_rows} rows -> but got: {len(data)} rows."
