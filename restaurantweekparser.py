from datetime import date
import requests
import MySQLdb
import pickle
import string
       
class RWParser:
    def __init__(self):
        self.contents = ''
        self.filename = ''
        self.url = "http://www.nycgo.com/restaurantweek/"
        self.restaurants = {}
        
    def get_contents_from_web(self):
        r = requests.get(self.url)
        self.contents = r.text
        pickle.dump(self.contents, open("restaurant_week.p","wb"))
        print "Dumped raw html into restaurant_week.p"

    def get_pickled_contents(self):
        self.contents = pickle.load(open("restaurant_week.p","rb"))
        print "Retreived info from restaurant_week.p"

    def get_restaurant_info(self):
        start_tag = '<tbody>'
        end_tag = '</tbody>'
        start_relevant = self.contents.find(start_tag)
        end_relevant = self.contents.find(end_tag)
        relevant = self.contents[start_relevant + len(start_tag):end_relevant]
        #throw the loop in here.
        i = 0
        anchor_tag = '<a href="'
        print "Size of file being processed (characters): "
        print len(relevant)
        while(1):
            anchor_tag_loc = relevant.find(anchor_tag,i)
            if anchor_tag_loc == -1:
                break
            end_anchor_tag_loc = relevant.find('">',anchor_tag_loc)
            end_name = relevant.find('</a>',end_anchor_tag_loc)
            food_type_start = relevant.find('"90">', end_name)
            food_type_end = relevant.find('</td>', food_type_start)
            food_type = relevant[food_type_start+5:food_type_end].strip()
            meals_start = relevant.find('"80">', food_type_end)
            meals_end = relevant.find('</td>', meals_start)
            meals = relevant[meals_start+5:meals_end].strip()
            location_start = relevant.find('"133">', meals_end)
            location_end = relevant.find('</td>', location_start)
            location = relevant[location_start+6:location_end].strip()
            name = relevant[end_anchor_tag_loc + 2: end_name]
            i = relevant.find("<tr>", i+1)
            self.restaurants[name] = {'Type of Food':food_type,
                                      'Meals Served': meals,
                                      'Location': location
                                      }
        return self.restaurants        

def main():
    #get_contents_from web will automatically pickle.
    RW = RWParser()
    #comment this next line if the script has been run before
    RW.get_contents_from_web()
    #uncomment next line if the script has been run before
    #RW.get_pickled_contents()
    RW.get_restaurant_info()
    print ("Relevant information found, and loaded into RWdata.p")
    pickle.dump(RW.restaurants, open("RWdata.p", "wb"))

if __name__ == '__main__':
    main()
