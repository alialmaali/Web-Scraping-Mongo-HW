from flask import Flask, render_template, redirect
import scrape_mars



# Import our pymongo library, which lets us connect our Flask app to our Mongo database.

import pymongo



# Create an instance of our Flask app.

app = Flask(__name__)



# Create connection variable

conn = 'mongodb://localhost:27017'



# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)



# Connect to a database. Will create one if not already available.

db = client.mars_db



# Drops collection if available to remove duplicates

#db.mars.drop()



# Creates a collection in the database and inserts two documents





# Set route

@app.route('/')
def index():
    mars_news = list(db.mars_news.find())
    mars_images = list(db.mars_images.find())
    mars_weather = list(db.marsweather.find())
    mars_facts = list(db.mars_facts.find())
    mars_facts2 = list(db.mars_facts2.find())
    mars_hemisphere = list(db.mars_hemisphere.find())
    lst = {

        "mars_news":mars_news,

        "mars_images":mars_images,

        "mars_weather":mars_weather,

        "mars_facts":mars_facts,

        "mars_facts2":mars_facts2[0]["facts"],

        "mars_hemisphere":mars_hemisphere

    }

    #print(mars_hemisphere)





    # Return the template with the teams list passed in

    return render_template('index.html', mars_info=lst)



@app.route('/scrape')

def scrape():



    # Run scraped functions

    surf = scrape_mars.scrape()

    # Redirect back to home page

    return redirect("/", code=302)







if __name__ == "__main__":

    app.run(debug=True)