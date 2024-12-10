import csv
import os
import locale
from time import sleep



def load_data(filename): 
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(        #list
                {                    #dictionary
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products


class bcolors:
    #ANSI escape sequences for terminal text formatting.

    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # @staticmethod
    # def color_text(text, color):
    #     return f"{color}{text}{BColors.DEFAULT}"

#gör en funktion som hämtar en produkt
def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break  # Avsluta loopen så snart produkten hittas
    
    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found, please try again"


def view_product(products, id, bcolor = bcolors):
    # Go through each product in the list
    for product in products:
        # Check if the product's id matches the given id
        if product["id"] == id:
            # If it matches, return the product's name and description
            return f"{bcolors.BOLD}(Viewing product):{bcolors.DEFAULT} \n {product['name']} \n \n Price: {bcolors.UNDERLINE}{locale.currency(product['price'], grouping=True)}{bcolors.DEFAULT} \n Quantity: {bcolors.UNDERLINE}{product['quantity']} {('left')}{bcolors.DEFAULT} \n \n {bcolors.BOLD}{bcolors.UNDERLINE}Descreption:{bcolors.DEFAULT} \n {product['desc']} \n "
    
    # If no matching product is found, return this message
    return "Product could not be found"

def view_products(products, max_desc_length=20, max_name_length=17, bcolors = bcolors):
    product_list = []

    # Header och separator
    header = f" {bcolors.BOLD}{'ID':>2} \t {'Name'} \t {'Description':>27} \t {'Price':>21} \t {'Quantity':>16}{bcolors.DEFAULT}"
    separator = "--" * 45

    # Lägg till header och separator i listan
    product_list.append(header)
    product_list.append(separator)
    
    for index, product in enumerate(products, 1):
        
        

        shorten_name = product['name']                #gör namnet kortare
        if len(shorten_name) > max_name_length:       
            shorten_name = shorten_name[:max_name_length] + "..." 
        
        shorten_desc = product['desc']                #gör desc kortare
        if len(shorten_desc) > max_desc_length:
            shorten_desc = shorten_desc[:max_desc_length] + "..."

        product_info = f"(#{product['id']}) \t {bcolors.BOLD}{shorten_name:<17}{bcolors.DEFAULT} \t {shorten_desc:<25} \t {bcolors.UNDERLINE}{locale.currency(product['price'], grouping=True)}{bcolors.DEFAULT} \t {product['quantity']:>1} {('left'):>1}"
        product_list.append(product_info)
    
    product_list.append(separator)
      

    return "\n".join(product_list)


    
def add_products(products, name, desc, price, quantity):
    max_id = max(products, key=lambda x: x['id']) #lambda är liten funktion utan namn som hämtar nycklels värde från dictionary

    id_value = max_id['id']     #id_value är största id:t i hela databasen

    new_id = id_value + 1   #skapa ett större och unikt id


    products.append(
        {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
        }
    )
    
    return f"Added item: {id}"


#TODO: gör om så du slipper använda global-keyword (flytta inte "product = []")
#TODO: skriv en funktion som returnerar en specifik produkt med hjälp av id


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('lokes_products.csv')


while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        

        
        print(view_products(products))  # Show ordered list of products

        choice = input("Would you like to (A) Add a product, (V) View , (R) Remove a product or (C) Cancel ").strip().upper()

        

        if choice == "A":
            #skapa ett nytt id
            #ta in information som jag ska spara
            #sen måste jag spara allt i products (lista med dictonaries inuti)

            name = input("Name of product: ")
            desc = input("Descreption: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))

            print(add_products(products, name, desc, price, quantity))
        
        elif choice == "C":
            print("Shutting down...")
            sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Thanks for shopping with us!")
            sleep(1)
            break

        elif choice in ["V", "R"]: 
        
            index = int(input("Enter product ID: "))
            os.system('cls' if os.name == 'nt' else 'clear')

            if choice == "V":   #visa
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product
                    print(view_product(products, id))  # Remove product using the actual ID
                    done = input("(G) Go back?")
                    if done == "G":
                        print("Returning...")
                        sleep(1)
                       
                else:
                    print("Invalid product")
                    sleep(1)
                
                    
            elif choice == "R": #ta bort
                if 1 <= index <= len(products):  # Ensure the index is within the valid range
                    selected_product = products[index - 1]  # Get the product using the list index
                    id = selected_product['id']  # Extract the actual ID of the product

                    print(remove_product(products, id))  # Remove product using the actual ID
                    sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')            

                else:
                    print("Invalid product")
                    sleep(1)
        
    except ValueError:
        print("Choose a prouct with a number")
        sleep(1)


    # Define the CSV file path
    csv_file_path = "lokes_products.csv"

    # Write the products data to a CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()  # Write the header row
        writer.writerows(products)  # Write the product data

    print(f"Data successfully saved to {csv_file_path}")