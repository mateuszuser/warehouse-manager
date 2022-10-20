import csv
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import *
from tkinter import Tk

SOLD_ITEMS = {}

ITEMS = {}

class Product:
        def __init__(self, name, unit, unit_price, quantity):
                self.name = name
                self.unit = unit
                self.unit_price = unit_price
                self.quantity = quantity
        def __str__(self):
                return f"{self.name} {self.quantity} {self.unit} {self.unit_price}"
        def __repr__(self):
                return f"Name:{self.name} Quantity:{self.quantity} Unit:{self.unit} Unit price (PLN):{self.unit_price}"

product1 = Product(name = "Milk", quantity = 120, unit= "l", unit_price= 2.3)
product2 = Product(name = "Sugar", quantity = 1000, unit= "kg", unit_price= 3)
product3 = Product(name = "Flour", quantity = 12000, unit= "kg", unit_price= 1.2)
product4 = Product(name = "Coffee", quantity = 120, unit= "kg", unit_price= 40)

ITEMS[product1.name] = product1
ITEMS[product2.name] = product2
ITEMS[product3.name] = product3
ITEMS[product4.name] = product4

product5 = Product(name = "Flour", quantity = 70, unit= "kg", unit_price= 1.2)
product6 = Product(name = "Coffee", quantity = 111, unit= "kg", unit_price= 40)

SOLD_ITEMS[product5.name] = product5
SOLD_ITEMS[product6.name] = product6

def get_items():
        print("Name\tQuantity\tUnit\tUnit Price (PLN)")
        print("____\t________\t____\t________________")
        for key, ITEM in ITEMS.items():
                first_key = ITEM.name
                second_key = ITEM.quantity
                third_key = ITEM.unit
                fourth_key = ITEM.unit_price
                print(f"{first_key}\t{second_key}\t\t{third_key}\t{fourth_key}")

def add_item():
        new_item = Product(name = input("Item name: "), quantity = input("Item quantity: "), unit= input("Item unit of measure. Eg. l, kg, pcs: "), unit_price= input("Item price in PLN: "))
        print("Adding to warehouse...")
        ITEMS[new_item.name] = new_item
        print("Successfully added to warehouse. Current status:")
        get_items()
                
def sell_item(product, sell_quantity):
        get_items()
        if product == ITEMS[product].name:
                first_key = ITEMS[product].name
                second_key = float(ITEMS[product].quantity)
                third_key = ITEMS[product].unit
                fourth_key = ITEMS[product].unit_price
                print(f"Quantity availble: {second_key}")                                                               
                if sell_quantity <= second_key:
                        second_key -= sell_quantity
                        ITEMS[product].quantity = second_key
                        if product in SOLD_ITEMS:
                                new_quantity = SOLD_ITEMS[product].quantity + sell_quantity
                                SOLD_ITEMS[product] = Product(name = first_key, quantity = new_quantity, unit = third_key, unit_price = fourth_key)
                        
                        else:
                                SOLD_ITEMS[product] = Product(name = first_key, quantity = sell_quantity, unit = third_key, unit_price = fourth_key)
                        print(f"Successfully sold {sell_quantity} {third_key} of {first_key}")                                                                                                      
                else:
                        print(f"The quantity of {first_key} is lower then you need.")

def get_costs():
        list_of_costs = [float(cost_item.quantity) * float(cost_item.unit_price) for key, cost_item in ITEMS.items()]
        costs = sum(list_of_costs)
        
        return costs

def get_incomes():
        list_of_incomes = [income_item.quantity * income_item.unit_price for key, income_item in SOLD_ITEMS.items()]
        incomes = sum(list_of_incomes)
        return incomes

def show_revenue():
        print("Revenue breakedown (PLN)")
        print("Income", round(get_incomes(), 2))
        print("Costs: ", round(get_costs(), 2))
        print("---------")
        revenue_round = round((round(get_incomes(), 2) - round(get_costs(), 2)), 2)
        print("Revenue " + str(revenue_round))

def export_items_to_csv():
        with open('magazyn.csv', 'w', newline='') as csvfile:
                fieldnames = ["Name", "Quantity", "Unit", "Unit price (PLN)" ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for key, ITEM in ITEMS.items():
                        writer.writerow({"Name": ITEM.name, "Quantity": ITEM.quantity, "Unit": ITEM.unit, "Unit price (PLN)": ITEM.unit_price})

def export_sales_to_csv():
    try:
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        data = [("csv file(*.csv)","*.csv")]
        file = asksaveasfilename(parent=root, filetypes = data, defaultextension = data)
        with open(file, "w", newline='') as csvfile:
            fieldnames = ["Name", "Quantity", "Unit", "Unit price (PLN)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, SOLD_ITEM in SOLD_ITEMS.items():
                writer.writerow({"Name": SOLD_ITEM.name, "Quantity": SOLD_ITEM.quantity, "Unit": SOLD_ITEM.unit, "Unit price (PLN)": SOLD_ITEM.unit_price})
    except FileNotFoundError:
                print("File not found. Check the path variable and filename")

def load_items_from_csv():   
        try:
                root = Tk()
                root.attributes("-topmost", True)
                root.withdraw()
                data = [("csv file(*.csv)","*.csv")]    
                file = askopenfilename(parent=root, filetypes = data, defaultextension = data)
                
                with open(file, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                                print(row["Name"])
                                if row["Name"] in ITEMS:
                                        new_quantity = float(ITEMS[row["Name"]].quantity) + float(row["Quantity"])
                                        work_dict = Product(name = row["Name"], quantity = new_quantity, unit= row["Unit"], unit_price= row["Unit price (PLN)"])
                                        ITEMS[work_dict.name] = work_dict
                                else:
                                        work_dict = Product(name = row["Name"], quantity = row["Quantity"], unit= row["Unit"], unit_price= row["Unit price (PLN)"])                    
                                        ITEMS[work_dict.name] = work_dict
        except FileNotFoundError:
                print("File not found. Check the path variable and filename")