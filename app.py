from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars
​
app = Flask(__name__)
​
# Use flask_pymongo to set up mongo connection
mongo=PyMongo(app, uri="mongodb://localhost:27017/mars_app")
​
@app.route("/")
def index():
    mars_page = mongo.db.mars.find_one()
    return render_template("index_html",mars=mars_page)
​
@app.route("/scrape")
def scrape():
    mars_page = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert = True)
    return "Sceaping Successful"
​
if __name =="__main__":
    app.run()