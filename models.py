import pickle

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



class Todos:
    def __init__(self):
        try:
            with open("ITEMS.pickle", "rb") as f:
                #self.ITEMS = pickle.load(f)
                #self.ITEMS = {self.ITEMS}
                file = pickle.load(f)
                temp_dict = {}
                for key, value in file.items():
                    temp_dict[key] = Product(name = value.name,
                                            quantity = value.quantity,
                                            unit= value.unit,
                                            unit_price= value.unit_price)
                self.ITEMS = temp_dict
        except FileNotFoundError:
            self.ITEMS = {}
            product1 = Product(name = "Milk", quantity = 120, unit= "l", unit_price= 2.3)
            product2 = Product(name = "Sugar", quantity = 1000, unit= "kg", unit_price= 3)
            product3 = Product(name = "Flour", quantity = 12000, unit= "kg", unit_price= 1.2)
            product4 = Product(name = "Coffee", quantity = 120, unit= "kg", unit_price= 40)
            self.ITEMS[product1.name] = product1
            self.ITEMS[product2.name] = product2
            self.ITEMS[product3.name] = product3
            self.ITEMS[product4.name] = product4     

        try:
            with open("SOLD_ITEMS.pickle", "rb") as f:
                #self.SOLD_ITEMS = pickle.load(f)
                #self.SOLD_ITEMS = {self.SOLD_ITEMS}
                file = pickle.load(f)
                temp_dict = {}
                for key, value in file.items():
                    temp_dict[key] = Product(name = value.name, 
                                            quantity = value.quantity, 
                                            unit= value.unit, 
                                            unit_price= value.unit_price)
                self.SOLD_ITEMS = temp_dict
                
        except FileNotFoundError:
            self.SOLD_ITEMS = {}
            product5 = Product(name = "Flour", quantity = 70, unit= "kg", unit_price= 1.2)
            product6 = Product(name = "Coffee", quantity = 111, unit= "kg", unit_price= 40)
            self.SOLD_ITEMS[product5.name] = product5
            self.SOLD_ITEMS[product6.name] = product6

    def save_ITEMS(self):
        with open("ITEMS.pickle", 'wb') as f:
            pickle.dump(self.ITEMS, f)
    
    def save_SOLD_ITEMS(self):
        with open("SOLD_ITEMS.pickle", 'wb') as f:
            pickle.dump(self.SOLD_ITEMS, f)

    def get_items(self):
        print("Name\tQuantity\tUnit\tUnit Price (PLN)")
        print("____\t________\t____\t________________")
        for key, ITEM in self.ITEMS.items():
            first_key = ITEM.name
            second_key = ITEM.quantity
            third_key = ITEM.unit
            fourth_key = ITEM.unit_price
            print(f"{first_key}\t{second_key}\t\t{third_key}\t{fourth_key}")

    def add_item(self, input_name, input_quantity, input_unit, input_unit_price):       
        if input_name in self.ITEMS:
            new_item = Product(name = input_name, 
                                quantity = float(self.ITEMS[input_name].quantity) + float(input_quantity), 
                                unit = input_unit, 
                                unit_price = input_unit_price)
            print("Adding to warehouse...")
            self.ITEMS[new_item.name] = new_item
            print("Successfully added to warehouse. Current status:")
            self.get_items()
            self.save_ITEMS()
        else:
            new_item = Product(name = input_name, 
                                quantity = input_quantity,
                                unit = input_unit, 
                                unit_price = input_unit_price)
            print("Adding to warehouse...")
            self.ITEMS[new_item.name] = new_item
            print("Successfully added to warehouse. Current status:")
            self.get_items()
            self.save_ITEMS()
                
    def sell_item(self, product, sell_quantity):
        self.get_items()
        if product == self.ITEMS[product].name:
            first_key = self.ITEMS[product].name
            second_key = float(self.ITEMS[product].quantity)
            third_key = self.ITEMS[product].unit
            fourth_key = self.ITEMS[product].unit_price
            print(f"Quantity availble: {second_key}")                                                               
            if sell_quantity <= second_key:
                second_key -= sell_quantity
                self.ITEMS[product].quantity = second_key
                if product in self.SOLD_ITEMS:
                    new_quantity = self.SOLD_ITEMS[product].quantity + sell_quantity
                    self.SOLD_ITEMS[product] = Product(name = first_key, quantity = new_quantity, unit = third_key, unit_price = fourth_key)
                    self.save_SOLD_ITEMS()
                    self.save_ITEMS()
                    self.get_items()
                else:
                    self.SOLD_ITEMS[product] = Product(name = first_key, quantity = sell_quantity, unit = third_key, unit_price = fourth_key)
                    print(f"Successfully sold {sell_quantity} {third_key} of {first_key}")   
                    self.save_SOLD_ITEMS()
                    self.save_ITEMS()
                    self.get_items()                                                                                               
            else:
                print(f"The quantity of {first_key} is lower then you need.")

    def get_costs(self):
        list_of_costs = [float(cost_item.quantity) * float(cost_item.unit_price) for key, cost_item in self.ITEMS.items()]
        costs = sum(list_of_costs)
        
        return costs

    def get_incomes(self):
        list_of_incomes = [float(income_item.quantity) * float(income_item.unit_price) for key, income_item in self.SOLD_ITEMS.items()]
        incomes = sum(list_of_incomes)
        return incomes

    def show_revenue(self):
        print("Revenue breakedown (PLN)")
        print("Income", round(self.get_incomes(), 2))
        print("Costs: ", round(self.get_costs(), 2))
        print("---------")
        revenue_round = round((round(self.get_incomes(), 2) - round(self.get_costs(), 2)), 2)
        print("Revenue " + str(revenue_round))

todos = Todos()

if __name__ == "__main__":
    step = 1
    while step > 0:
        choice = input("What would you like to do? ")
                                
        if choice == "exit":
            print("Exiting... Bye!")
            break
        if choice == "show":
            todos.get_items()
        if choice == "add":
            input_name = input("Item name: ")
            input_quantity = input("Item quantity: ")
            input_unit= input("Item unit of measure. Eg. l, kg, pcs: ")
            input_unit_price= input("Item price in PLN: ")
            todos.add_item(input_name, input_quantity, input_unit, input_unit_price)
        if choice == "sell":
            product = input("Item to sell: ")
            sell_quantity = float(input("Quantity to sell: "))
            todos.sell_item(product, sell_quantity)
        if choice == "sold":
            print(todos.SOLD_ITEMS)
        if choice == "sold_items":
            print("Name\tQuantity\tUnit\tUnit Price (PLN)")
            print("____\t________\t____\t________________")
            for key, SOLD_ITEM in todos.SOLD_ITEMS.items():
                sold_first_key = SOLD_ITEM.name
                sold_second_key = SOLD_ITEM.quantity
                sold_third_key = SOLD_ITEM.unit
                sold_fourth_key = SOLD_ITEM.unit_price
                print(f"{sold_first_key}\t{sold_second_key}\t\t{sold_third_key}\t{sold_fourth_key}")
        if choice == "get_costs":
            print("Costs: ", todos.get_costs())
        if choice == "get_incomes":
            print("Incomes: ", todos.get_incomes())
        if choice == "show_revenue":
            todos.show_revenue()
        if choice == "save":
            todos.export_items_to_csv()
            todos.export_sales_to_csv()
        if choice == "load":
            todos.ITEMS.clear()
            todos.load_items_from_csv()
                
        step += 1