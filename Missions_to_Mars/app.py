from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape


app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars_dict = scrape.scrape()
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)