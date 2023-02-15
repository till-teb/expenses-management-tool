from faker import Faker
import pandas as pd 
import random
import os

fake = Faker()

Category = ["Consumables", "Food & Beverages", "Leisure & Entertainment", "Transportation", "Other & Extraordinary", "Financial fees", "Living area"]
Amount = []
Date = []
Importance = ["Not Important", "Less Important", "Important", "Most Important"]
Feeling = ["Good", "Bad"]

# Define a dictionary that maps categories to lists of subcategories
subcategories = {
    "Consumables": ["Clothing","Drugstore","Education","Electronics","Furniture","Medicines","Narcotics","Pets","Stationery","Other",],
    "Food & Beverages": ["Bakery", "Kiosk", "Market", "Supermarket", "Other"],
    "Leisure & Entertainment":  ["Cinema","Event","Hairdresser","Hobby","Party","Restaurant","Vacation","Other"],
    "Transportation": ["Public Transportation", "Private Transportation", "Other"],
    "Other & Extraordinary": ["Additional Costs", "Investment", "Other"],
    "Financial fees": ["Taxes", "Insurance", "Bank", "Other"],
    "Living area": ["Energy", "Rent", "Household Appliances", "Decoration", "Other"]
}

# Define a dictionary that maps subcategories to example items
items = {
    "Supermarket": ["Milk", "Bread", "Eggs", "Cheese", "Fruits", "Vegetables"],
    "Other": ["Random Item"],
    "Kiosk": ["Newspaper", "Magazine", "Snacks", "Soda", "Candy"],
    "Bakery": ["Bread", "Croissant", "Pastry", "Cake", "Sandwich"],
    "Market": ["Fruits", "Vegetables", "Fish", "Meat"],
    "Drugstore": ["Toothpaste", "Shampoo", "Soap", "Deodorant", "Toilet paper", "Razor", "Moisturizer", "Comb"],
    "Clothing": ["T-Shirt", "Jeans", "Dress", "Shoes", "Hat",  "Hoodie", "Joggers"],
    "Electronics": ["Phone", "Tablet", "Laptop", "Headphones", "TV"],
    "Furniture": ["Table", "Chair", "Sofa", "Bed", "Shelf"],
    "Pets": ["Food", "Toys", "Vet"],
    "Education": ["Books", "Courses"],
    "Stationery": ["Notebook", "Pen", "Pencil", "Eraser"],
    "Medicines": ["Painkiller", "Vitamins", "Prescription"],
    "Narcotics": ["Alcohol", "Tobacco", "Vape"],
    "Cinema": ["Ticket", "Popcorn", "Drink", "Snack"],
    "Restaurant": ["Meal", "Drink", "Dessert"],
    "Party": ["Food", "Drink", "Decorations", "Ticket"],
    "Event": ["Ticket", "Food", "Drink", "Merchandise"],
    "Hairdresser": ["Haircut", "Coloring"],
    "Hobby": ["Craft Supplies", "Gaming", "Instrument", "Sports equipment"],
    "Vacation": ["Accommodation", "Flight", "Transportation", "Sightseeing"],
    "Public Transportation": ["Ticket", "Pass"],
    "Private Transportation": ["Gasoline", "Car Wash", "Tires", "Oil Change"],
    "Additional Costs": ["Delivery fees", "Installation fees", "Late payment fees"],
    "Investment": ["Stocks", "Real Estate"],
    "Taxes": ["Income tax", "Property tax", "Sales tax"],
    "Insurance": ["Health insurance", "Car insurance", "Home insurance"],
    "Bank": ["ATM fees", "Overdraft fees", "Wire transfer fees"],
    "Energy": ["Electricity", "Gas", "Water"],
    "Rent": ["Monthly rent"],
    "Household Appliances": ["Refrigerator", "Washing machine", "Vacuum cleaner", "Oven"],
    "Decoration": ["Furniture", "Painting", "Curtains", "Carpets"]
}

# Define a dictionary that maps categories to ranges of possible costs
cost_ranges = {
    "Consumables": (10, 100),
    "Food & Beverages": (5, 100),
    "Leisure & Entertainment": (20, 100),
    "Transportation": (5, 35),
    "Other & Extraordinary": (150, 700),
    "Financial fees": (10, 50),
    "Living area": (150, 600)
}

def Subcategory(row):
    # Look up the list of subcategories for the current category
    subcat_list = subcategories.get(row["Category"], [])
    
    if subcat_list:
        # Choose a random element from the list of subcategories
        return random.choice(subcat_list)
    else:
        # Return a default value if the list is empty
        return "N/A"

def get_random_item(row):
    # Get the subcategory for the current row
    subcategory = row["Subcategory"]
    
    # Look up the list of items for the current subcategory
    item_list = items.get(subcategory, [])
    
    if not item_list:
        return ""
    
    # Choose a random element from the list of items
    return random.choice(item_list)



# Define a function that generates a random cost within the range for the given category
def generate_cost(row):
    # Look up the range of possible costs for the current category
    cost_range = cost_ranges.get(row["Category"], (0, 0))
    
    # Generate a random cost within the range
    cost = random.uniform(*cost_range)

 # Round the cost to two decimal places
    return round(cost, 2)



def dummy_data(amount): 
    data = []
    for i in range(amount):
        row = {}
        row["Category"] = random.choice(Category)
        row["Amount"] = generate_cost(row)
        row["Date"] = fake.date_time_between_dates("-8w", "now")
        row["Importance"] = fake.random_element(Importance)
        row["Feeling"] = fake.random_element(Feeling)
        row["Subcategory"] = Subcategory(row)
        data.append(row)
    return data

data = dummy_data(50)
df = pd.DataFrame(data, columns=["Item","Amount","Category","Subcategory","Importance","Date","Feeling"])

# Use the apply() method to add the "Subcategory" column to the DataFrame
df["Subcategory"] = df.apply(Subcategory, axis=1)

# Add a new column "Item" by applying the function "get_random_item" to each row of the DataFrame
df["Item"] = df.apply(get_random_item, axis=1)

# Use the apply() method to apply the generate_cost() function to each row of the DataFrame
df["Amount"] = df.apply(generate_cost, axis=1)



df["Day"] = df["Date"].dt.day
df["Month"] = df["Date"].dt.strftime('%b')
df["Year"] = df["Date"].dt.year

df = df.drop("Date", axis=1)

# Print the resulting DataFrame




def save_dataframe_to_csv(df, filename):

    if not filename.endswith('.csv'):
        filename += '.csv'
    filepath = os.path.join(os.getcwd(), filename)
    df.to_csv(filepath, index=False)
    print(f"DataFrame saved to {filename}")

save_dataframe_to_csv(df, 'expenses_management_tool')


print(df)
