from datetime import date

import requests
import MySQLdb
import pickle

class YelpParser:
    def __init__(self):
        self.contents = ''
        self.filename = ''
        self.star_rating = 'Not Found'
        self.url = "http://www.yelp.com/search?find_desc="
        self.cursor = 0

    def get_yelp_contents(self, search_target, location="manhattan"):
        #this will remove the "location" part of the name.
        if search_target.find(" - ") != -1:
            search_target = search_target[:search_target.find(" - ")]
        if search_target.find(" / ") != -1:
            search_target = search_target[:search_target.find(" / ")]
        search_target.replace('&amp;', '&')
        self.target = search_target
        self.location = location
        split_target = search_target.split()
        self.url = self.url + split_target[0]
        if len(split_target) > 1:
            #If there is more than one word in search term,
            #Use yelp's convention for multiword searches.
            for i in range(1,len(split_target)):
                self.url = self.url + '+' + split_target[i]
        self.url += '&find_loc=' + self.location
        r = requests.get(self.url)
        self.contents = r.text
                
    def pickle_contents(self):
        if self.contents:
            pickle.dump(self.contents, open("yelp_contents.p", "wb"))
            print "Sucessfully pickled contents from Yelp search of"
            print self.target + " to yelp_contents.p"
        else:
            print "Something went wrong (booo!)"
        
    def load_pickled_yelp(self):
        if not self.contents:
            self.contents = pickle.load(open("yelp_contents.p", "rb"))
            print "Successfully loaded pickled content into working memory"
        else:
            print "Looks like you already have something in contents"
            print "Make a new object before loading in to it."

    def pick_out_stars(self):
        #if the first link wasn't the best, then that's yelp's fault, not mine
        first_result_tag = '<a id="bizTitleLink0"'
        start_first_result_location = self.contents.find(first_result_tag, self.cursor)
        self.cursor = start_first_result_location
        if self.cursor == -1:
            self.yelp_name = 'Not Found'
            self.highlighted = False
            self.star_rating = 0
            return self.star_rating
        end_first_result_location = self.contents.find('</a>', start_first_result_location)
        #check if there is highlighted text in the first search result
        self.yelp_name = self.get_words('">1.','</a>')
        if self.yelp_name.find("highlighted") == -1:
            self.highlighted = False
        else:                   # Parse the string if highlighted.
            self.highlighted = True
            self.yelp_name = self.yelp_name.replace('<span class="highlighted">', '')
            self.yelp_name = self.yelp_name.replace('</span>', '').strip()
            self.yelp_name = self.yelp_name.replace('&amp;', '&')
            if self.yelp_name.find(" - ") != -1:
                self.yelp_name = self.yelp_name[:self.yelp_name.find(" - ")]
            if self.yelp_name.find(" / ") != -1:
                self.yelp_name = self.yelp_name[:self.yelp_name.find(" / ")]
        star_tag = '<span class="star-img stars_'
        third_tag = '"><'
        raw_star_rating = self.get_words(star_tag,third_tag)
        if len(raw_star_rating) == 1:
            self.star_rating = float(raw_star_rating)
        else:
            self.star_rating = float(raw_star_rating[0]) + .5
        return self.star_rating
        
    def get_words(self, tag1, tag2):
        #this function will get a word from self.contents using find with tags
        location1 = self.contents.find(tag1,self.cursor)
        location2 = self.contents.find(tag2, location1)
        if location1 == -1 or location2 == -1:
            return "Not Found"
        self.cursor = location2 + 1
        #returns the words found
        return self.contents[location1 + len(tag1): location2]

if __name__ == '__main__':
    Y = YelpParser()
    Y.get_yelp_contents("Gordon Ramsay at The London")
    Y.pick_out_stars()
    print Y.yelp_name
    print Y.star_rating
    print Y.highlighted
    X = YelpParser()
    X.get_yelp_contents("Aureole")
    X.pick_out_stars()
    print X.yelp_name
    print X.star_rating
    print X.highlighted
