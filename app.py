from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_elements = mongo.db.mars_elements.find_one()
    return render_template("index.html", mars_elements=mars_elements)


@app.route("/scrape")
def scrape():
    mars_elements = mongo.db.mars_elements
    mars_data = scrape_mars.scrape()
    mars_elements.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
