#!/usr/bin/env python
# coding: utf-8
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time


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
    results = soup.find(class_="slide")
    print(results)

    mars = {}

    title = results.find('div', class_='content_title')
    desc = results.find('div', class_='rollover_description_inner')
    news_title = title.a.text
    news_p = desc.text
    #     print(news_title)
    try:
        print('\n-----------------\n')
        print(news_title)
        print(news_p)
    except AttributeError as e:
        print(e)
    mars["news_title"]=news_title
    mars["news_paragraph"]=news_p

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    # Retrieve page with the requests module
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    # look for full image tag
    full_image = browser.find_by_id('full_image')

    #Click through on link
    full_image.click()
    html=browser.html
    #soup=bs(html, 'html.parser')
    #print(soup.prettify())

    #Get more information tag next.
    browser.is_element_present_by_text('more info', wait_time=2)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    #Grabbing the full image link here
    soup = bs(browser.html, "html.parser")
    featured_img = soup.find('img', class_='main_image')['src']
    #can use f string to contenaint as well as + method.
    featured_img_url = f'{base_url}{featured_img}'
    mars["featured_image"]= featured_img_url

    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())

    mars_weather = soup.find('div', class_="js-tweet-text-container").text.strip()
    mars_weather


    mars["weather"]=mars_weather
    mars

    #Pandas table HTML parsing
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    table[1]

    mars_table = table[1]
    mars_facts = mars_table.drop(columns=['Earth'])

    mars_facts.rename(columns = {'Mars - Earth Comparison': 'Facts'}, inplace = True)
   

    #Convert Pandas's DataFrame to HTML Table
    mars_html=mars_facts.to_html(index=False, header=False)
   

    mars["facts"]=mars_html

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser') 

    results = soup.find('div', class_="full-content")

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
        mars["hemisphere"]=hemisphere_image_urls
        
        browser.back()



    return mars
    browser.quit()


    
