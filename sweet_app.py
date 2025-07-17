import os
import pandas as pd

df = pd.read_csv("sweet_data2.csv")

def get_sweets(df):
    return "\nAll the available sweets are:\n\n" + df[['id', 'name', 'category', 'price', 'quantity']].to_string(index=False)

def price_filter_sweets(df, min_price, max_price):
    if max_price == '' and min_price == '':
        return get_sweets(df)
    elif max_price == '' and min_price != '':
        return df[df['price'] >= int(min_price)].to_string(index=False)
    elif max_price != '' and min_price == '':
        return df[df['price'] <= int(max_price)].to_string(index=False)
    elif max_price != '' and min_price != '':
        return df[(df['price'] >= int(min_price)) & (df['price'] <= int(max_price))].to_string(index=False)

def category_filter_sweets(df, category):
    if category in df['category'].to_string(index=False):
        result = f"\nSweets from {category} category are :\n"
        result += df[df['category'] == category].to_string(index=False)
        return result
    else:
        return "\nIncorrect Category! Please enter valid category!!\n"

def get_sorted(df, id, asc):
    if asc == 1:
        a = True
    elif asc == 2:
        a = False
    else:
        return 'Please enter either 1 or 2..!!'
    
    match id:
        case 1:
            return "\nID Wise sorted menu: \n\n" + df.sort_values(by='id', ascending=a).to_string(index=False)
        case 2:
            return "\nSweet Wise sorted menu: \n\n" + df.sort_values(by='name', ascending=a).to_string(index=False)
        case 3:
            return "\nCategory Wise sorted menu: \n\n" + df.sort_values(by='category', ascending=a).to_string(index=False)
        case 4:
            return "\nPrice Wise sorted menu: \n\n" + df.sort_values(by='price', ascending=a).to_string(index=False)
        case 5:
            return "\nQuantity Wise sorted menu: \n\n" + df.sort_values(by='quantity', ascending=a).to_string(index=False)

def get_category(df):
    return "\nCategories available at shop are:\n\n" + pd.DataFrame(df['category'].unique(), columns=['category']).to_string(index=False)

def get_price(df, sweet):
    if sweet in df['name'].to_string(index=False):
        price = df[df['name'] == sweet].iloc[0]['price']
        return f"\nPrice of {sweet} is Rs. {price} per 100gm"
    else:
        return "\nSweet not available!"

def enter_new(df, id, name, category, price, quantity):
    if str(id) in df['id'].to_string(index=False):
        return "ID already exists! Enter a different ID."
    elif name.lower() in df['name'].to_string(index=False).lower():
        return f"{name} already exists! But you can restock it."
    else:
        new_row = pd.DataFrame([[id, name, category, price, quantity]], columns=['id', 'name', 'category', 'price', 'quantity'])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('sweet_data2.csv', index=False)
        return f"Successfully added {name}!\n\n" + get_sweets(df)

def delete_sweet(df, id):
    if int(id) in df['id'].values:
        df = df[df['id'] != int(id)]
        df.to_csv("sweet_data2.csv", index=False)
        return "\nSuccessfully deleted record!\n\n" + get_sweets(df)
    else:
        return "\nPlease enter a valid ID!"

def buy_sweets(df, sweet, quantity):
    if sweet.lower() not in df['name'].to_string(index=False).lower():
        return "\nInvalid sweet name! Please choose from the available stock!\n"

    sweet_row = df[df['name'].str.lower() == sweet.lower()].iloc[0]
    price = int(sweet_row['price'])
    available = int(sweet_row['quantity'])

    if quantity >= available:
        return f"\nSorry! Only {available} packets of {sweet} are available.\nChoose less or equal quantity."
    else:
        df.loc[df['name'].str.lower() == sweet.lower(), 'quantity'] = available - quantity
        df.to_csv('sweet_data2.csv', index=False)
        return (
            f"\nThank you for buying {sweet}!\n"
            "******** BILL *********\n"
            f"Sweet Name : {sweet}\n"
            f"Weight     : {quantity * 100}gm\n"
            f"Amount     : Rs.{quantity * price}/-\n"
            "Thank you for choosing us!\nWe hope to see you again!"
        )

def restock(df, sweet, quantity):
    if sweet.lower() in df['name'].to_string(index=False).lower():
        available = int(df[df['name'].str.lower() == sweet.lower()].iloc[0]['quantity'])
        if quantity > 0:
            df.loc[df['name'].str.lower() == sweet.lower(), 'quantity'] = available + quantity
            df.to_csv('sweet_data2.csv', index=False)
            return f"Stock updated successfully! Total stock of {sweet} is now {available + quantity}."
        else:
            return "Please enter a valid quantity!"
    else:
        return "Invalid sweet! Please enter a valid name from the stock."

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def sweet_shop(df):
    while True:
        clear_screen()
        print("\n********** WELCOME TO SWEET SHOP **********")
        print("\nPlease enter the number for the service you want:")
        print("1. Sweet Menu")
        print("2. Show Available Categories")
        print("3. Sweet Menu Price Range wise")
        print("4. Sweet Menu Category wise")
        print("5. Sorted Sweet Menu")
        print("6. Get price of a Sweet")
        print("7. Buy a sweet")
        print("8. Add a sweet")
        print("9. Delete a sweet")
        print("10. Restock a sweet")
        print("11. Exit\n")

        inp = input(" --> ")

        try:
            match int(inp):
                case 1:
                    clear_screen()
                    print(get_sweets(df))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 2:
                    clear_screen()
                    print(get_category(df))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 3:
                    clear_screen()
                    min_price = input("Enter minimum price: --> ")
                    max_price = input("Enter maximum price: --> ")
                    print(price_filter_sweets(df, min_price, max_price))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 4:
                    clear_screen()
                    category = input("Enter category: --> ")
                    print(category_filter_sweets(df, category))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 5:
                    clear_screen()
                    id = int(input("Sort by (1-ID, 2-Name, 3-Category, 4-Price, 5-Quantity): --> "))
                    asc = int(input("Ascending[1] or Descending[2]: --> "))
                    print(get_sorted(df, id, asc))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 6:
                    clear_screen()
                    sweet = input("Enter sweet name: --> ")
                    print(get_price(df, sweet))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 7:
                    clear_screen()
                    sweet = input("Enter sweet name to buy: --> ")
                    quantity = int(input("Enter number of 100gm packets: --> "))
                    print(buy_sweets(df, sweet, quantity))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 8:
                    clear_screen()
                    id = int(input("Enter ID: --> "))
                    name = input("Enter Sweet Name: --> ")
                    category = input("Enter Category: --> ")
                    price = int(input("Enter Price per 100gm: --> "))
                    quantity = int(input("Enter Quantity: --> "))
                    print(enter_new(df, id, name, category, price, quantity))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 9:
                    clear_screen()
                    id = input("Enter Sweet ID to delete: --> ")
                    print(delete_sweet(df, id))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 10:
                    clear_screen()
                    sweet = input("Enter Sweet name to restock: --> ")
                    quantity = int(input("Enter number of 100gm packets: --> "))
                    print(restock(df, sweet, quantity))
                    menu = input("\nPress ENTER to go to service menu")
                    clear_screen()
                    sweet_shop(df)
                case 11:
                    clear_screen()
                    print("Thank you! Visit again!\n")
                    break
                case _:
                    print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    sweet_shop(df)
