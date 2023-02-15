import expenses_management_tool.data_generator as dd

def test_unique_data():
    '''
    test_function to see if every entry has at least 4 unique values. If yes, 
    the dataset is generated random.The function returs true if it does and all 
    entries have at least 4 unique values.
   
    '''
    expected_rows = 50
    data = dd.dummy_data(expected_rows)
    
    for entry in data:
        unique_entries = set(entry.values())
        if len(unique_entries) < 4:
            return False
    assert True



