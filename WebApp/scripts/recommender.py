import mysql.connector
import pandas as pd
import numpy as np

####################################################
#Class for finding and returning products
####################################################
class Products():

    ################################################
    #Function to initialze Products objects
    ################################################
    def __init__(self):
        pass

    ################################################
    #Function to find product in database
    #Input: brand name, product name
    #Output: product id
    ################################################
    @staticmethod
    def findProduct(brand_name, product_name):
        
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
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
    #Output: image urls, webpage urls
    ################################################
    @staticmethod
    def getTop(product_id, distances):
        
        #initialize variables
        top = 10
        
        #check distances
        if len(distances.index) < 1:
            return False
        elif len(distances.index) < top:
            top = len(distances.index)
        
        #get top distances
        dist = distances.sort_values(str(product_id))
        dist = dist.head(top)
        product_ids = dist["product_id"].tolist()
        product_ids = [str(x) for x in product_ids]
        product_ids = ','.join(product_ids)
        
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
        cursor = cnx.cursor()
        
        #query products
        query = ("SELECT url "
                 "FROM Product "
                 "WHERE product_id in ("+product_ids+") "
                 "ORDER BY FIELD(product_id, "+product_ids+") "
                 )
        cursor.execute(query)
        
        #close mysql server
        cnx.close()
        
        #clean data
        output = [x[0] for x in cursor]
        
        #return page urls
        return ','.join(output)

    ################################################
    #Function to get reference product data
    #Input: product id
    #Output: image urls, webpage urls
    ################################################
    @staticmethod
    def getRef(product_id):
        
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
        cursor = cnx.cursor()
        
        #query products
        query = ("SELECT url "
                 "FROM Product "
                 "WHERE product_id = '"+product_id+"' "
                 )
        cursor.execute(query)
                 
        #close mysql server
        cnx.close()
                     
        #clean data
        output = [x[0] for x in cursor]
                                         
        #return page urls
        return output


####################################################
#Class for finding and returning ingredients
####################################################
class Ingredients():
    
    ################################################
    #Function to initialze Ingredient objects
    ################################################
    def __init__(self):
        pass
    
    ################################################
    #Function to find ingredient in database
    #Input: ingredient name
    #Output: product ids
    ################################################
    @staticmethod
    def findIngred(ingred_name):
        
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
        cursor = cnx.cursor()
        
        #query products
        query = ("SELECT distinct product_id "
                 "FROM Product_Ingredient AS P "
                 "JOIN Ingredients AS I "
                 "ON P.ingredient_id = I.ingredient_id "
                 "WHERE (P.ingredient_name LIKE '%"+ingred_name+"%' "
                 "OR I.ingredient_name LIKE '%"+ingred_name+"%' "
                 "OR I.alt_names LIKE '%"+ingred_name+"%') ")
        cursor.execute(query)
        
        #clean data
        output = [str(x[0]) for x in cursor]

        #check if empty
        if output == []:
            return False
                 
        #close mysql server
        cnx.close()
                     
        #return train and test sets
        return ','.join(output)


    ################################################
    #Function drop products from list
    #Input: product_ids, distance matrix
    #Output: distance matrix
    ################################################
    @staticmethod
    def dropIngreds(product_ids, distances):
        
        #split ingredients
        ids = [int(x) for x in product_ids.split(',')]
    
        #get top distances
        dist = distances.loc[~distances["product_id"].isin(ids)]
        
        #return distances
        return dist










