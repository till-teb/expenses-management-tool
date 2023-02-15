
import expenses_management_tool.data_generator as dd

Category = ["Food and Beverages", "Consumables", "Leisure and Entertainment", "Transport", "Extraordinary Expenses", "Financial Fees", "Living Area"]

# Define a dictionary that maps categories to lists of subcategories
subcategories = {
    "Food and Beverages": ["Supermarkt", "Kiosk", "Bakery", "Market", "Other"],
    "Consumables": ["Drugstore","Clothing", "Electronics", "Furniture", "Pets", "Education", "Stationery", "Medicines", "Narcotics", "Other"],
    "Leisure and Entertainment": ["Cinema", "Restaurant", "Party", "Event", "Hairdresser", "Hobby", "Vacation", "Other"],
    "Transport": ["Public Transportation", "Private Transportation", "Other"],
    "Extraordinary Expenses": ["Additional Costs", "Investments", "Other"],
    "Financial Fees": ["Financial Fees"],
    "Living Area": ["Rent", "Other"]}


def test_dummy_data():
    data = dd.dummy_data(50)
    for row in data:
        assert row["Subcategory"] in dd.subcategories.get(row["Category"], "subcategories are not mathing")
