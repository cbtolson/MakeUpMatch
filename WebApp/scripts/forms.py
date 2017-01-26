##########################################################################################################
#Class for forms used on input page
##########################################################################################################
from wtforms import Form, StringField

class InputForm(Form):

    #required input
    brand_name = StringField('brand_name', default=None)
    product_name = StringField('product_name', default=None)
    ingred_name = StringField('ingred_name', default=None)
