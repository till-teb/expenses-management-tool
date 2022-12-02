# split DATE into seperatet columns
def split_DATE(data):
    # splits the DATE column in to three new_columns:
    new_columns = data["DATE"].str.split("-", expand=True)
    data["day"] = new_columns[2]
    data["month"] = new_columns[1]
    data["year"] = new_columns[0]
    return data

