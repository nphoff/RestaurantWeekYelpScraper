import pickle
import csv

def check_similar_name(s1, s2):
    #deletions
    s1l = s1.lower()
    s2l = s2.lower()
    words_to_check = ['restaurant', 'bar', 'grill', 'new york', "'", "the", "soho", ",", "wine", "harlem" ]
    s1l.replace("&amp;", "&")
    s2l.replace("&amp;", "&")
    for word in words_to_check:
        s1l = s1l.replace(word, '')
        s2l = s2l.replace(word, '')
    if s1l.strip() == s2l.strip():
        return True
    else:
        return False

def main():
    yelpdict = pickle.load(open("yelpRWdata.p", "rb"))

    good_matches = 0
    decent_matches = 0
    fail_matches = 0
    
    for restaurant in yelpdict:
        if yelpdict[restaurant]['Good match in Yelp?']:
            if check_similar_name(restaurant, yelpdict[restaurant]['Yelp returned name']):
            #print "Good match found for %s" % restaurant
                good_matches = good_matches + 1
            else:
                print "Decent, matched %s with %s" % (restaurant, yelpdict[restaurant]['Yelp returned name'])
                decent_matches = decent_matches + 1
        else:
            print "Fail -- %s is not %s" % (restaurant, yelpdict[restaurant]['Yelp returned name'])
            fail_matches = fail_matches + 1
            
            print "Good matches\tDecent matches\tFail matches"
            print "%s\t\t%s\t\t%s" % (good_matches, decent_matches, fail_matches)
            print yelpdict['The Strand Bistro']
            
##################################################
#     The Output to CSV part
            
            c = csv.writer(open("Yelp_csv_file.csv", "wb"))
            c.writerow(["Restaurant Name", "Yelp Rating", "Meals Served", "Location", "Type of Food"])
            for r in yelpdict:
                r.replace('&amp;', '')
                if check_similar_name(r, yelpdict[r]['Yelp returned name']):
                    row = [r.encode("utf-8"),
                           yelpdict[r]['Yelp Rating'],
                           yelpdict[r]['Meals Served'].encode("utf-8"),
                           yelpdict[r]['Location'].encode("utf-8"), 
                           yelpdict[r]['Type of Food'].encode("utf-8")
                           ]
                    c.writerow(row)
    # for restaurant in yelpdict:
    
if __name__ == '__main__':
    main()
