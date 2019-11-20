from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    result = bs(html, "html.parser")

    #Get Headline and description of news item.
    title = result.find('div', class_='content_title')
    desc = result.find('div', class_='rollover_description_inner')

    #Capturing featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    print(soup.prettify())
    results = soup.find('article', class_="carousel_item")["style"].strip("background-image: url(' .jpg' );")
    featured_image = (f'https://www.jpl.nasa.gov{results}.jpg')
    
    #Get current tweet with Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    print(soup.prettify())

    mars_weather = soup.find('div', class_="js-tweet-text-container").text.strip()
    
    #Pandas table HTML parsing for Mars information table
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    print(table[1])
    mars = table[1]
    mars_facts = mars.drop(columns=['Earth'])
    mars_facts.rename(columns = {'Mars - Earth Comparison': 'Facts'}, inplace = True)
    print(mars_facts)
    #Convert Pandas's DF to HTML Table
    mars_facts_html = mars_facts.to_html('mars_facts_table.html', index=False, justify="center")

    #Getting Hemisphere images
    hemisphere_image_urls = []
    #Going to the main page for the Mars Hemisphere's
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')   

    #get a list of all the hemispheres
    url_links = browser.find_by_css("a.product-item h3")

    #Loop through the links and click links to get image
    for i in range(len(url_links)):
        hemisphere = {}

        #We need to find the elements in each loop
        browser.find_by_css("a.product-item h3")[i].click()

        #next find the sample image anchor tag and get href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        #get hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text

        #Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)

        #Finally navigate back to start again on loop
        browser.back()

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

    #,hemisphere_image_urls,mars_facts_html
