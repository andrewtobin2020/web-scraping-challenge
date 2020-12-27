from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars.py

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = client.db.collection.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape(): 

        # Run the scrape function
    mars_info = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    client.db.collection.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True) 