from bs4 import BeautifulSoup 
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()  
    
    # Nasa News
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    news_soup = BeautifulSoup(browser.html, 'html.parser')
    news_title = news_soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    browser.quit() 
    
    # Images
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    nasa_url =  "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    featured_image_url  = image_soup.find('div', class_='carousel_container').find('article')['style']
    featured_image_url = featured_image_url[23:-3]
    shortened_url = 'https://www.jpl.nasa.gov'
    featured_image_url = prefix_url + featured_image_url
    browser.quit()    

    # Nasa Facts
    facts_url = 'https://space-facts.com/mars/'
    html_table = pd.read_html(facts_url)
    df = html_table[0]
    df.columns = ["Facts", "Value"]
    df.set_index(["Facts"])
    facts_html = df.to_html()
    facts_html = facts_html.replace("\n","")
   

    # Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')
    imgs = hemisphere_soup.find_all('h3')
    hemisphere_url_prefix = 'https://astrogeology.usgs.gov/'

    hemisphere_image_urls = []

    for img in imgs:
        browser.click_link_by_partial_text(img.text)
        html= browser.html
        page_soup = BeautifulSoup(html, 'html.parser')
        img_url_suffix = page_soup.find('img', class_='wide-image')['src']
        img_url = hemisphere_url_prefix + img_url_suffix
        title = page_soup.find('h2', class_='title').text
        img_dict = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(img_dict)
        browser.back()
        


    # Store data in a dictionary

    mars_data = {
        'News title': news_title,
        'News paragraph': news_p,
        'Featured image url': featured_image_url,
        'Facts html': facts_html,
        'Hemisphere image urls' : hemisphere_image_urls 
    }


     # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data