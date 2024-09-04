# CS50 Properties
## Video Demo: https://youtu.be/lldS6b01CcA
## Description:

My project was to gather property data from off Rightmove and Zoopla of properties for sale in London and use this data to create a web application which will allow you to search using the postcode, prices and sort by price ascending and descending.

To get the data I used a python library called Scrapy. Scrapy allowed me to use web crawlers and direct them to data I wanted to retrieve. Within the repository tehre are 4 spiders in total. This is because I first had to get the id's and links to the properties before I could get their data.

#### Listing spiders
The listing spiders return the id's and links to each property on the site within London. By adding a command in the terminal, the spiders can write the data to a json file in my specified format. This will allow me to use another spider to get the links from the json files and get the actual property data. These are stores within the listing jsons. Due to not all properties being on the same page, I needed to direct the spider to the next page once it finishes scraping one. I found that Rightmove increamented a number in their url by 24, each time you increased a page. Using this I was able to iterate through each page and return all the data. Zoopla on the other hand was easier, as on each pagination button, it had a link which I could just extract and use.

#### Details spiders
One thing to note is that on each properties individual site, they have a json storing all the data for that property within the HTML. After finding I was able to get the spiders to navigate to it and return the data I wanted. After validating the Jsons I was able to use the json library and format the data as a json and return the data required. This data was then stored in the property_details jsons respectively.


#### Database
Using bit.io, I uploaded both property_detail jsons and it created 2 tables for me. I then joined these 2 tables to create 1 containing data from both rightmove and zoopla using a SQL JOIN statement. However, one issue that arose was that the price had a data type of text. This was because the price of some properties were labelled as "POA". So I first changed all POA's to a 0 value using UPDATE and SET. This allowed me to change the data type of the price column to an int.

#### Flask
##### app.py
This is the application file of my website. The database uses PostgreSQL and so I needed to import the psycopg2 library. This will allow me to run SQL queried on my database through the script.
On the home page, I query the database for 3 random properties to be "featured" and they will be displayed on the home page. They change every time the user refreshes the page.
For the searching, the data from the form needed to be validated so I set values for the max price and min price to include all data if the user has not entered any values for them.
I set the value for postcode to "" if the user has not entered any value for it, so it does not results in a null error.
Next it will render an error page if the max and min price aren't valid and if the postcode does not exist.
Finally I query the database depening on what they chose to sort by and return it to the html file.

##### main.html
For the html I am using Bootstrap CSS and JS. This creates a navbar form which is what allows the user to search. The form contains dropdown sliders for the max and min price, and a text input for postcode. It also contains a select input for how they want their data sorted.

##### home.html
Displays the featured listings. Using Boostrap cards to display 3 randomly featured properties. By iterating over the data returned from the database I can write them into the cards.

##### error.html
Displays an error card due to an invalid input.

##### search.html
Similar home.html however instead it is displaying data from the search query and formats the cards so they go down rather than across.
