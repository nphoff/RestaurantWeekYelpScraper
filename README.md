RestaurantWeekYelpScraper
=========================

Quick python script to pull out yelp ratings for restaurant week restaurants

The program uses the requests library to scrape the restaurant week site,
and then subsequently scrape each link found in the correct section.

It then queries yelp to extract the yelp ratings from each link.

Finally, it performs a verification step to make sure that the link
actually corresponds to the correct yelp page and rating for that restaurant.

The sequence of commands to create the csv is as follows:

python restaurantweekparser.py

python parsemulti.py

python manipyelpdict.py

This will create a .csv file with restaurant information and yelp scores.
