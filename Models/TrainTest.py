import mysql.connector
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np

####################################################
#Class for getting the train and test sets
####################################################
class TrainTest():

    ################################################
    #Function to initialze TestTrain object
    ################################################
    def __init__(self):
        pass

    ################################################
    #Function to create training and test set
    #Output: training set (list), test set (list)
    ################################################
    @staticmethod
    def getSet():
        #connect to mysql
        cnx = mysql.connector.connect(host='152.19.68.141', user='ctolson', password='ilaYOU5!', database='sephora_cosmetics')
        cursor = cnx.cursor()

        #query reviewers
        query = ("SELECT reviewer, type "
                 "FROM Reviews "
                 "JOIN Product "
                 "ON Product.product_id=Reviews.product_id "
                 "GROUP BY reviewer "
                 "HAVING COUNT(review)>1"
                 )
        cursor.execute(query)

        #clean data
        reviewer = []
        types = []
        for (x, y) in cursor:
            reviewer.append(x)
            types.append(y)

        #set stratified split
        X = np.array(reviewer)
        y = np.array(types)
        ss = StratifiedShuffleSplit(n_splits=2, test_size=0.2, random_state=0)
        ss.get_n_splits(X, y)

        #get train and test sets
        for train_index, test_index in ss.split(X,y):
            X_train, X_test = X[train_index], X[test_index]
 
        #convert training set to dictionary
        x_test = dict(zip(X_test, range(0, len(X_test))))

        #query review ids
        query = ("SELECT review_id, reviewer "
                 "FROM Reviews ")
        cursor.execute(query)

        #close mysql server
        cnx.close()

        #clean data
        review_id = []
        reviewer = []
        for (x, y) in cursor:
            review_id.append(x)
            reviewer.append(y)

        #convert to dictionary
        review_list = {}
        for i in range(0, len(review_id)):
            review_list[review_id[i]] = reviewer[i]

        #split review ids
        train = []
        test = []
        for i in range(0, len(review_id)):
            if review_list[review_id[i]] in x_test:
                test.append(review_id[i])
            else:
                train.append(review_id[i])

        #return train and test sets
        return{'train':train, 'test':test}


