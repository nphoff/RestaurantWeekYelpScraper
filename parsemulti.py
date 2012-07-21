import time
import pickle

from yelpparser import YelpParser

#Parsing all of the entries in the dictionary which was pickled

RWdict = pickle.load(open("RWdata.p", "rb"))
YelpRWdict = {}


for restaurant in RWdict:
    print "Parsing %s" % restaurant
    X = YelpParser()
    X.get_yelp_contents(restaurant)
    YelpRWdict[X.target] = RWdict[restaurant]
    YelpRWdict[X.target]['Yelp Rating'] =  X.pick_out_stars()
    YelpRWdict[X.target]['Yelp returned name'] = X.yelp_name
    YelpRWdict[X.target]['Good match in Yelp?'] = X.highlighted

pickle.dump(YelpRWdict, open("yelpRWdata.p", "wb"))
pickle.dump(YelpRWdict, open("yelpRWdata2.p", "wb"))
print RWdict
print "Great Success!!"
    

