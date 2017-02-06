##########################################################################################################
#Functions for viewing html templates
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for
from forms import InputForm
from recommender import Products as prod
from recommender import Ingredients as ingr
import pandas as pd
from flask_jsglue import JSGlue

#create Flask app
app = Flask(__name__)
JSGlue(app)

#pre-load distances
distances = pd.read_csv('flask_mm/static/data/dist_reviews.csv', header=0)


#process products and ingredients
@app.route('/output')
def output(product_id=None, ingred=None):
    
    #restrict access
    if request.referrer is None:
        return render_template("403.html")

    #initialize variables
    product_id = request.args.get('product_id')
    ingred = request.args.get('ingred')

    #drop ingredients
    dists = ingr.dropIngreds(ingred, distances)
    if len(dists.index) == 0:
        return render_template("soap.html")

    #find nearest products
    recommended = prod.getTop(product_id, dists)

    #find reference product
    reference = prod.getRef(product_id)

    #get graph
    pids = [x['name'] for x in recommended]
    rate = [x['rating'] for x in recommended]
    graph = prod.getGraph(reference['name'], pids, rate)

    #return output page
    return render_template("output.html", reference=reference, recommended=recommended, graph=graph)


#display homepage
@app.route('/inputs', methods=('GET', 'POST'))
def inputs():
    form = InputForm()
    error = None
    
    if request.method == 'POST':
        
        #check brand name
        brand_name = request.form.get('brand_name')
        if brand_name =='':
            return render_template("homepage.html", form=form, error="ERROR: Brand name required.")
        
        #check product name
        product_name = request.form.get('product_name')
        if product_name =='':
            return render_template("homepage.html", form=form, error="ERROR: Product name required.")
        
        #check ingredient name
        ingred_name = request.form.get('ingred_name')
        if ingred_name =='':
            return render_template("homepage.html", form=form, error="ERROR: Ingredient name required.")
                
        #query for product
        product = prod.findProduct(brand_name, product_name)
        if product == False:
            return render_template("homepage.html", form=form, error="Sorry, we do not have that product.")
        
        #query for ingredient
        ingred = ingr.findIngred(ingred_name, product)
        if ingred == False:
            return render_template("homepage.html", form=form, error="Sorry, we do not have that ingredient.")

        return redirect(url_for("output", product_id=product, ingred=ingred))
    else:
        return render_template("homepage.html", form=form, error=error)


#display homepage
@app.route('/auto')
def auto(brand_name=None, product_name=None, ingred_name=None):
    #restrict access
    if request.referrer is None:
        return render_template("403.html")
    
    #initialize variables
    brand_name = request.args.get('brand_name')
    product_name = request.args.get('product_name')
    ingred_name = request.args.get('ingred_name')
    
    #query for product
    product = prod.findProduct(brand_name, product_name)
    
    #query for ingredient
    ingred = ingr.findIngred(ingred_name, product)
    
    return redirect(url_for("output", product_id=product, ingred=ingred))


#display soap
@app.route('/soap')
def soap():
    #restrict access
    if request.referrer is None:
        return render_template("403.html")
    
    #return soap page
    return render_template("soap.html")

#display about
@app.route('/examples')
def examples():
    return render_template("examples.html")

#display about
@app.route('/about')
def about():
    return render_template("about.html")


#display contact
@app.route('/contact')
def contact():
    return render_template("contact.html")


#display 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#display 403
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

#display homepage
@app.route('/homepage', methods=('GET', 'POST'))
def homepage():
    form = InputForm()
    error = None
    return render_template("homepage.html", form=form, error=error)

#display index
@app.route('/', methods=('GET', 'POST'))
def index():
    form = InputForm()
    error = None
    return render_template("homepage.html", form=form, error=error)














