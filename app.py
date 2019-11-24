# 1. import Flask and PyMongo
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars2

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


# image = scrape_mars.function-name()
# return image = image


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars2.scrape_all()
    mars.update({},mars_data, upsert=True)
    return "Done"

if __name__ == "__main__":
    app.run()

