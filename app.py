from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    news_results = mongo.db.news_results.find_one()
    return render_template("index.html", news_results=news_results)


@app.route("/scrape")
def scraper():
    news_results = mongo.db.news_results
    news_results_data = scrape_mars.scrape()
    news_results.update({}, news_results_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
