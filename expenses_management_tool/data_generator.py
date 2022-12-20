from faker import Faker
import pandas as pd 
import random


fake = Faker(["de_DE"])


Category = ["Food and Beverages", "Consumables", "Leisure and Entertainment", "Transport", "Extraordinary Expenses"]
Name = []
Cost = []
Date = []
Importance = []
GorB = ["Good", "Bad"]

# Define a dictionary that maps categories to lists of subcategories
subcategories = {
    "Food and Beverages": ["Supermarkt", "Kiosk", "Bakery", "Market", "Other"],
    "Consumables": ["Drugstore","Clothing", "Electronics", "Furniture", "Pets", "Education", "Stationery", "Medicines", "Narcotics", "Other"],
    "Leisure and Entertainment": ["Cinema", "Restaurant", "Party", "Event", "Hairdresser", "Hobby", "Vacation", "Other"],
    "Transport": ["Public Transportation", "Private Transportation", "Other"],
    "Extraordinary Expenses": ["Additional Costs", "Investments", "Other"]
}

# Define a dictionary that maps categories to ranges of possible costs
cost_ranges = {
    "Food and Beverages": (5, 200),
    "Consumables": (10, 450),
    "Leisure and Entertainment": (20, 200),
    "Transport": (5, 35),
    "Extraordinary Expenses": (150, 700)
}


# Define the Subcategory based on the main Category
def Subcategory(row):
    # Look up the list of subcategories for the current category
    subcat_list = subcategories.get(row["Category"], [])
    
    # Choose a random element from the list of subcategories
    return random.choice(subcat_list)



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
        row["Name"] = fake.name()
        row["Cost"] = generate_cost(row)
        row["Date"] = fake.date_time_between_dates("-2y", "now")
        row["Importance"] = fake.random_int(0, 4)
        row["GorB"] = fake.random_element(GorB)
        row["Subcategory"] = Subcategory(row)
        data.append(row)
    return data

data = dummy_data(20)

df = pd.DataFrame(data, columns=["Category","Name","Cost","Date","Importance","GorB","Subcategory"])

# Use the apply() method to add the "Subcategory" column to the DataFrame
df["Subcategory"] = df.apply(Subcategory, axis=1)

# Use the apply() method to apply the generate_cost() function to each row of the DataFrame
df["Cost"] = df.apply(generate_cost, axis=1)

# Print the resulting DataFrame
print(df)
