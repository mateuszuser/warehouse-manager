from flask import Flask, render_template, request, redirect, url_for
#from warehouse_new import ITEMS, SOLD_ITEMS, Product, sell_item, load_items_from_csv, export_sales_to_csv, get_costs, get_incomes
from models import todos
from forms import ProductForm, SellForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "klucz"

@app.route("/", methods = ["GET"])
def homepage():
    return render_template("homepage.html")

@app.route("/products", methods = ["GET", "POST"])
def show():
    form = ProductForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():   
            todos.add_item(form.data["name"], form.data["quantity"], form.data["unit"], form.data["unit_price"])       
            #item_to_add = Product(name = form.data["name"], quantity = form.data["quantity"], unit= form.data["unit"], unit_price= form.data["unit_price"])
            #ITEMS[form.data["name"]] = item_to_add
        
        return redirect(url_for("show")) 
    return render_template("product_list.html", form=form, ITEMS=todos.ITEMS, error=error)

@app.route("/sold_products", methods = ["GET"])
def show_sold():
    return render_template("sold_product_list.html", SOLD_ITEMS=todos.SOLD_ITEMS)

@app.route("/sell/<product>", methods = ["GET", "POST"])
def sell(product):
    form = SellForm()
    error = ""
    avaible_quantity = todos.ITEMS[product].quantity
    if request.method == "POST":
        if form.validate_on_submit():
            todos.sell_item(product, form.data["quantity_to_sell"])
            return redirect(url_for("show"))

    
    return render_template("sell.html", form=form, product=product, avaible_quantity=avaible_quantity, ITEMS=todos.ITEMS, error=error)

#@app.route("/load", methods = ["GET"])
#def load(): 
#    global ITEMS
#    form = ProductForm()
#    error = ""
#    load_items_from_csv()
#    return render_template("product_list.html", form=form, ITEMS=ITEMS, error=error)

#@app.route("/export", methods = ["GET"])
#def export():
#    export_sales_to_csv()
#    return redirect(url_for("show"))

@app.route("/revenue", methods = ["GET"])
def revenue():
    costs = round(todos.get_costs(), 2)
    incomes = round(todos.get_incomes(), 2)
    revenue_round = round((round(todos.get_incomes(), 2) - round(todos.get_costs(), 2)), 2)
    return render_template("revenue.html", costs=costs, incomes=incomes, revenue_round=revenue_round)


if __name__ == "__main__":
    app.run(debug=True)