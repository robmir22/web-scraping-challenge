import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url + relative_image_path

    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = df.iloc[0]
    comparison = df[1:]
    comparison.set_index('Mars - Earth Comparison')
    html_table = comparison.to_html()
    html_table.replace('\n', '')

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    names = soup.find_all('div', class_='item')

    hemispheres = []

    for hemis in h_names: 
        itemtitle = hemis.find('div', class_='description').find('a').find('h3').text
        baseurl = hemis.find('a')['href']
        usgs_url = 'https://marshemispheres.com/'
        image_url = usgs_url + baseurl
        browser.visit(image_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        final_image = usgs_url + image
        hemispheres.append({'title':itemtitle, 'img_url':final_image})

    browser.quit()
    
    mars_dict = {'news_title': news_title,
        'news_teaser': news_teaser,
        'featured_image_url': featured_image_url,
        'mars_facts': html_table,
        'hemisphere_images': hemispheres}

    return mars_dict