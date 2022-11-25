from datetime import date
date = str(date.today())

def input_query(date):
    expense = str(input("Ausgabe für : "))
    amount = float(input("Wie viel € hast du ausgegeben? : "))
    importance = int(input("Wichtigkeit der Ausgabe? (1-4) : "))
    category = int(input(''' please choose category:

                       (1) x
                       (2) x
                       (3) x
                       ...
                       '''))

    df = pd.DataFrame({"category": [category],
                       "importance": [importance],
                       "amount":[amount] ,
                       "expense": [expense],
                       "date": [date]})
    return(df)




if __main__ == '__name__':
    input_query(date)