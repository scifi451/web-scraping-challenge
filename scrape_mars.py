from splinter import Browser
from bs4 import BeautifulSoup as bs


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    news_results = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    news_results["title"] =  soup.find_all(class_="slide").find('div', class_='content_title')
    news_results["desc"] = result.find('div', class_='rollover_description_inner')
    news_results["news_title"] = title.a.text
    news_results["news_p"] = desc.text

    return results