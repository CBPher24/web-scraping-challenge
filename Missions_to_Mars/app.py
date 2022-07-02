import os
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# template_fol = os.path.abspath("../templates")
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdata_app")


@app.route("/")
def main():
    marsdb = mongo.db.marsc.find_one()
    return render_template("index.html", mars_data=marsdb)


@app.route("/scrape")
def scrape():
    mars_coll = scrape_mars.scrape()
    mongo.db.marsc.update_one({}, {"$set": mars_coll}, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)