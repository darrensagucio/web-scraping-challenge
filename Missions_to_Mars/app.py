from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars_data = mongo.db.marsdict.find_one()
    return render_template("index.html", mars_dict=mars_data)

@app.route("/scrape")
def scrape_mars():
    
    mars_data = scrape_mars.scrape()
    
    mongo.db.marsdict.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)