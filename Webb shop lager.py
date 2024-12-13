import csv
import os
import locale
from time import sleep


# laddar in filen och gör om den så att den kan ändras och användas
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
            
            products.append(        # lista
                {                    # dictionary
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

# färger och format för att ändra text
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

# gör en funktion som hämtar en produkt
def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break  # avsluta loopen så snart produkten hittas
    
    # gör så att produkten tas bort
    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found, please try again"


def view_product(products, id, bcolor = bcolors):
    # går igenom listan av produkter
    for product in products:
        # kollar om den matchar
        if product["id"] == id:
            # om produkten matchar id, så retunerar den en snygg liten lista med produktes name och beskrivning 
            return f"{bcolors.BOLD}(Viewing product):{bcolors.DEFAULT} \n {product['name']} \n \n Price: {bcolors.UNDERLINE}{locale.currency(product['price'], grouping=True)}{bcolors.DEFAULT} \n Quantity: {bcolors.UNDERLINE}{product['quantity']} {('left')}{bcolors.DEFAULT} \n \n {bcolors.BOLD}{bcolors.UNDERLINE}Descreption:{bcolors.DEFAULT} \n {product['desc']} \n "
    
    # om den inte matchar så retunerar den, denna nedre text 
    return "Product could not be found"


def view_products(products, max_desc_length=20, max_name_length=17, bcolors = bcolors):
    product_list = []

    # headern och separatorn
    header = f" {bcolors.BOLD}{'ID':>2} \t {'Name'} \t {'Description':>27} \t {'Price':>21} \t {'Quantity':>16}{bcolors.DEFAULT}"
    separator = "--" * 45

    # lägger till en header och separator i listan
    product_list.append(header)
    product_list.append(separator)
    
    for index, product in enumerate(products, 1):
        
        

        shorten_name = product['name']                # gör namnet kortare
        if len(shorten_name) > max_name_length:       
            shorten_name = shorten_name[:max_name_length] + "..." 
        
        shorten_desc = product['desc']                # gör desc kortare
        if len(shorten_desc) > max_desc_length:
            shorten_desc = shorten_desc[:max_desc_length] + "..."
        
        # många \t, bcolors och :<X/:>X användes har för att ge listan en mer snygare utseende
        product_info = f"(#{product['id']}) \t {bcolors.BOLD}{shorten_name:<17}{bcolors.DEFAULT} \t {shorten_desc:<25} \t {bcolors.UNDERLINE}{locale.currency(product['price'], grouping=True)}{bcolors.DEFAULT} \t {product['quantity']:>2} {('left'):>5}"
        product_list.append(product_info)
    
    product_list.append(separator) # lägger in samma header men under listan men över instruktionerna 
      

    return "\n".join(product_list)


# lägger in producterna i produkt listan och ger den ett eget nytt id
def add_products(products, name, desc, price, quantity):
    max_id = max(products, key=lambda x: x['id']) # lambda är liten funktion utan namn som hämtar nycklels värde från dictionary

    id_value = max_id['id']     # id_value är största id:t i hela databasen

    new_id = id_value + 1   # skapa ett större och unikt id

    # lägger till och formaterar den tillagda produkten in i listan 
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


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('lokes_products.csv')


while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        

        
        print(view_products(products))  # printar ut listan 

        choice = input("Would you like to (A) Add a product, (V) View , (R) Remove a product or (C) Cancel ").strip().upper() # ett input som också ger dig instruktioner om knapparna

        

        if choice == "A":
            # skapa ett nytt id
            # tar in information som ska sparas
            # sen sparar allt i products (listan med dictonaries inuti)

            name = input("Name of product: ")
            desc = input("Descreption: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))

            print(add_products(products, name, desc, price, quantity))
        
        # stänger av programmet 
        elif choice == "C":
            print("Shutting down...")
            sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Thanks for shopping with us!")
            sleep(1)
            break
        
        # V låter dig vissa en produkt som du har valt och visar all info om produkten. R tar bort en produkt som du har valt
        elif choice in ["V", "R"]: 
        
            index = int(input("Enter product ID: "))
            os.system('cls' if os.name == 'nt' else 'clear')

            if choice == "V":   #visa
                if 1 <= index <= len(products):  # ser till att indexet ligger inom det giltiga intervallet
                    selected_product = products[index - 1]  # tar produkten med hjälp av listindexet
                    id = selected_product['id']  # extrahera produktens id
                    print(view_product(products, id))  # printar ut så du kan see hela sidan för produkt infot
                    done = input("(G) Go back?")    # låter användaren att gå tillbaka till listan
                    if done == "G":
                        print("Returning...")
                        sleep(1)

                # error check      
                else:
                    print("Invalid product")
                    sleep(1)
                
                    
            elif choice == "R": #ta bort
                if 1 <= index <= len(products):  # ser till att indexet ligger inom det giltiga intervallet
                    selected_product = products[index - 1]  # tar produkten med hjälp av listindexet
                    id = selected_product['id']  # extrahera produktens ID
                    print(remove_product(products, id))  # tar bort produkten med hjälp av id
                    sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')            

                # error check
                else:
                    print("Invalid product")
                    sleep(1)
    # error check    
    except ValueError:
        print("Choose a prouct with a number")
        sleep(1)


    # definerar file vägen
    csv_file_path = "lokes_products.csv"

    # skriver ut produktens data till en CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()  # skriver ut header row
        writer.writerows(products)  # skriver produkt datan

    print(f"Data successfully saved to {csv_file_path}")