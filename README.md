RestaurantWeekYelpScraper
=========================

Quick python script to pull out yelp ratings for restaurant week restaurants

UPDATE: The yelp html has been changed, and the code will need to be
	modified to accomodate the changes.

The sequence of commands to create the csv is as follows:

python restaurantweekparser.py
python parsemulti.py
python manipyelpdict.py

This will create a .csv file with restaurant information and yelp scores.
