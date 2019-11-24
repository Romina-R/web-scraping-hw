#!/usr/bin/env python
# coding: utf-8


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import numpy as np




def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)

    data = {
    "news_title": news_title,
    "news_paragraph": news_p,
    "featured_image": featured_image(browser),
    "hemispheres": hemispheres(browser),
    "weather": twitter_weather(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now()
}
    browser.quit()
    return data

### NASA Mars News

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    try: 
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find('div',class_="content_title").text.strip()
        news_p = slide_elem.find('div',class_="article_teaser_body").text.strip()
    except AttributeError:
        return None, None
    return news_title, news_p


# except AttributeError:
#     return None, None
# return news_title, news_p
# print(news_title)
# print("--------")
# print(news_p)



### JPL Mars Space Images - Featured Image


def featured_image(browser):
#with Browser() as browser:
    # Visit URL
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    # browser.fill('q', 'splinter - python acceptance testing for web applications')
    # # Find and click the 'search' button
    # browser.check("full image")

    #button = browser.find_by_name('full_image')
    # full_image_elem = browser.click_link_by_id('full_image')

    # moreinfo = browser.click_link_by_partial_text("more info", wait_time=1)

    browser.click_link_by_id('full_image')
    #browser.click_link_by_partial_text("more info", wait_time=1)
    moreinfoelement = browser.find_link_by_partial_text("more info")
    moreinfoelement.click()

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        img_link = img_soup.select_one('figure.lede a img').get("src")
        img_link
    except AttributeError:
        return None
    img_url = f'https://www.jpl.nasa.gov{img_link}'
    img_url

    return img_url

## TWITTER

def twitter_weather(browser):

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html = browser.html
    twitter_soup = BeautifulSoup(html, 'html.parser')

    tweet = twitter_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    tweet

    mars_weather = tweet.find('p', 'tweet-text').get_text()
    mars_weather

    return mars_weather

### Mars Facts

def mars_facts():

    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)

    html = browser.html
    facts_soup = BeautifulSoup(html, 'html.parser')

    facts_table= pd.read_html(html, attrs = {'id': 'tablepress-p-mars'}, match='.+', flavor=None, header=None, index_col=None, skiprows=None, parse_dates=False, tupleize_cols=None, thousands=', ', encoding=None, decimal='.', converters=None, na_values=None, keep_default_na=True, displayed_only=True)
    facts_table

    df = facts_table[0]

    #df = pd.DataFrame(data = facts_table[0], index=None, columns=["Parameter","Value"])
    df = df.rename(columns={0:"Parameter", 1:"Value"})
    df = df.set_index("Parameter", inplace=True)
    

    return df.to_html(classes="table table-striped")


### Hemispheres


def hemispheres(browser):

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    html = browser.html
    USGS_soup = BeautifulSoup(html, 'html.parser')

    image_urls = []


    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[i].click()
        
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
        hemisphere['title'] = browser.find_by_css("h2.title").text
        
        image_urls.append(hemisphere)
        
        browser.back()
        

    return image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
