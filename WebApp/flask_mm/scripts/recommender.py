import mysql.connector
import pandas as pd
import numpy as np
import re

####################################################
#Class for finding and returning products
####################################################
class Products():

    ################################################
    #Function to initialze Products
    ################################################
    def __init__(self):
        return(self)
    
    
    ################################################
    #Function set graph distances
    #Input: distances, topdistances
    #Output: graph
    ################################################
    @staticmethod
    def getGraph(ref, pids, rate):
        
        #create nodes
        nodes = []
        nodes.append({"name":str(ref), "group":0})
        for i in range(0,len(pids)):
            r = rate[i]
            nodes.append({"name":pids[i], "group":float(r[:-1])})
        
        #create links
        links = []
        links.append({"source":0, "target": 0, "value":0})
        for i in range(0,len(rate)):
            r = rate[i]
            links.append({"source": 0, "target": i+1, "value":float(r[:-1])})
        
        #return graph
        return{"nodes":nodes, "links":links}


    ################################################
    #Function to find product in database
    #Input: brand name, product name
    #Output: product id
    ################################################
    @staticmethod
    def findProduct(brand_name, product_name):
        
        #process input
        product_name = product_name.strip()
        brand_name = brand_name.strip()
        
        #connect to mysql
        cnx = mysql.connector.connect(host='localhost', user='ctolson', password='lDONTd5!', database='sephora_cosmetics')
        cursor = cnx.cursor()
        
        #query products
        query = ("SELECT product_id "
                 "FROM Product "
                 "WHERE brand LIKE '"+brand_name+"%' AND name LIKE '"+product_name+"%' ")
        cursor.execute(query)

        #clean data
        output = [x[0] for x in cursor]
        
        if output == []:
            return False

        #close mysql server
        cnx.close()

        #return product id
        return output[0]
        

    ################################################
    #Function to get top recommended product data
    #Input: product id, distance matrix
    #Output: urls, brand, name
    ################################################
    @staticmethod
    def getTop(product_id, distances):
        
        #initialize variables
        top = 12
        
        #check distances
        if len(distances.index) < 1:
            return False
        elif len(distances.index) < top:
            top = len(distances.index)
        
        #get top products
        dist_sort = distances.sort_values(str(product_id), ascending=False)
        dist = dist_sort.head(top)
        ids = dist["product_id"].tolist()
        ids = [str(x) for x in ids]
        product_ids = ','.join(ids)
        
        #get top distances
        rate = [dist.ix[x,str(product_id)]*280 for x in dist.index]
        rating = [str("{0:.2f}".format(x))+'%' for x in rate]
        
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
        cursor = cnx.cursor()
        
        #query products
        query = ("SELECT product_id, url, brand, name "
                 "FROM Product "
                 "WHERE product_id in ("+product_ids+") "
                 "ORDER BY FIELD(product_id, "+product_ids+") "
                 )
        cursor.execute(query)
        
        #close mysql server
        cnx.close()
        
        #clean data
        i=0
        output = []
        for (x, y, z, w) in cursor:
            output.append({'id':str(x), 'url':y, 'brand':z.split('"}')[0], 'name':" ".join(re.findall("[a-zA-Z]+", w)), 'rating':rating[i]})
            i += 1

        #return page urls
        return output

    ################################################
    #Function to get reference product data
    #Input: product id
    #Output: url, brand, name
    ################################################
    @staticmethod
    def getRef(product_id):
        
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
        cursor = cnx.cursor()
        
        #query products
        query = ("SELECT url, brand, name "
                 "FROM Product "
                 "WHERE product_id = '"+product_id+"' "
                 )
        cursor.execute(query)
                 
        #close mysql server
        cnx.close()
                     
        #clean data
        url = []
        brand = []
        name = []
        for (x, y, z) in cursor:
            url.append(x)
            brand.append(y)
            name.append(z)
                                         
        #return page urls
        return{'url':url[0], 'brand':brand[0], 'name':name[0], 'id':product_id}



####################################################
#Class for finding and returning ingredients
####################################################
class Ingredients():
    
    ################################################
    #Function to initialze Ingredients
    ################################################
    def __init__(self):
        pass
    
    ################################################
    #Function to find ingredient in database
    #Input: ingredient name
    #Output: product ids
    ################################################
    @staticmethod
    def findIngred(ingred_name, product):
        
        #split ingredients
        ingred_name = [x.strip() for x in ingred_name.split(',')]
        output = []
        
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
        cursor = cnx.cursor()
        
        for iname in ingred_name:

            #query products
            query = ("SELECT distinct product_id "
                     "FROM Product_Ingredient AS P "
                     "JOIN Ingredients AS I "
                     "ON P.ingredient_id = I.ingredient_id "
                     "WHERE P.ingredient_name LIKE '%"+iname+"%' "
                     "OR I.ingredient_name LIKE '%"+iname+"%' "
                     "OR I.alt_names LIKE '%"+iname+"%' ")
            cursor.execute(query)
        
            #clean data
            out = [str(x[0]) for x in cursor]
        
            #check if empty
            if out == []:
                return False

            #append output
            output = output+out+[product]
    
        #close mysql server
        cnx.close()
                     
        #return train and test sets
        return ','.join(np.unique(output))


    ################################################
    #Function drop products from list
    #Input: product_ids, distance matrix
    #Output: distance matrix
    ################################################
    @staticmethod
    def dropIngreds(product_ids, distances):
        
        #split ingredients
        ids = [int(x) for x in product_ids.split(',')]
        
        if len(ids) == len(distances.index):
            return pd.DataFrame({'A' : []})
    
        #get top distances
        dist = distances.loc[~distances["product_id"].isin(ids)]
        
        #return distances
        return dist










