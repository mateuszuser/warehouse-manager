from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField

class ProductForm(FlaskForm):
    name = StringField("Name: ")
    quantity = FloatField("Quantity: ")
    unit = StringField("Unit: ")
    unit_price = FloatField("Unit price (PLN)")

class SellForm(FlaskForm):
    quantity_to_sell = FloatField("Quantity to sell: ")
