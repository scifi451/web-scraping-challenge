#!/usr/bin/env python
# coding: utf-8




from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests



def scrape_info ():



    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)



    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')




    # Examine the results, then determine element that contains sought info
    print(soup.prettify())




    # results are returned as an iterable list
    results = soup.find_all(class_="slide")
    print(results)



    mars_data = {}



    # Loop through returned results
    #for result in results:

    # Retrieve the thread title
    title = result.find('div', class_='content_title')
    desc = result.find('div', class_='rollover_description_inner')
    # Access the thread's text content
    #.a would call it from the <a href area if we need to.
    news_title = title.a.text
    news_p = desc.text
    #     print(news_title)
    try:
    print('\n-----------------\n')
    print(news_title)
    print(news_p)
    except AttributeError as e:
    print(e)
    mars_data["title"]=news_title
    mars_data["paragraph"]=news_p



    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    print(soup.prettify())



    # results are returned as an iterable list
    #results = soup.find('a', class_="button fancybox")["data-fancybox-href"]
    #print(f'https://www.jpl.nasa.gov{results}')
    results = soup.find('article', class_="carousel_item")["style"].strip("background-image: url(' .jpg' );")
    link=https://www.jpl.nasa.gov + {results} + .jpg'
    featured_image_url="https://www.jpl.nasa.gov"+result.a.img["src"]    

    mars_data["featured_image"]=link


    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')



    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())


    mars_weather = soup.find('div', class_="js-tweet-text-container").text.strip()
    mars_weather



    mars_data["weather"]=mars_weather


    #Pandas table HTML parsing
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    table[1]





    mars = table[1]
    mars_facts = mars.drop(columns=['Earth'])



    mars_facts.rename(columns = {'Mars - Earth Comparison': 'Facts'}, inplace = True)




    #Convert Pandas's DF to HTML Table
    mars_table=mars_facts.to_html('mars_facts_table.html', index=False, justify="center")
    #!open mars_facts_table.html




    mars_data["facts"]=mars_table


    # ## Hemisphere Images


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')




    # Examine the results, then determine element that contains sought info
    print(soup.prettify())




    results = soup.find('div', class_="full-content")
    results



    #Going to the main page for the Mars Hemisphere's
    hemisphere_image_urls = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    hemispheres = soup.find_all('div', class_="item")
    for hemisphere in hemispheres:

    hemisphere_dict = {}
    link = hemisphere.find('a')
    href = link['href']
    print('--------------------------------------')
    #print(hemisphere.text)
    #print(href)
    browser.visit('https://astrogeology.usgs.gov/' + href)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    #Finding the link for the hemisphere image once you click into the individual page
    hem_image = soup2.find('div', class_="downloads").find('li').find('a')
    hem_title= soup2.find('h2', class_="title").text
    print(hem_image.get('href'))
    #if want tiff image  print(hem_image.get('href').strip("full.jpg"))
    print(hem_title)

    #Adding the elements we just grabbed to a dictionary.
    hemisphere_dict['img_url'] = hem_image.get('href')
    hemisphere_dict['title'] = hem_title= soup2.find('h2', class_="title").text
    hemisphere_image_urls.append(hemisphere_dict)

    browser.back()



    mars_data["hemisphere"]=hemisphere_image_urls
    return mars_data

if __name__ == "__main__":
    print(scrape_info())

    

