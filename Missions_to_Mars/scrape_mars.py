import os
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    mars_data = {}

    # # Enter whatever URL you like
    browser.visit("https://redplanetscience.com/")

    # Add the page source to the variable `content`.
    content = browser.html
    # Load the contents of the page, its source, into BeautifulSoup 

    soup = BeautifulSoup(content,features="lxml")
    # print (soup.prettify)

    # Object is “results”, brackets make the object an empty list.
    # We will be storing our data here.
    results = []
    for element in soup.findAll(attrs={'class': 'list_text'}):
        news={}
        title = element.find(attrs={'class':'content_title'})
    #     print (title.text)
        para = element.find(attrs={'class':'article_teaser_body'})
    #     print (para.text)
        news['news_title']=title.text
        news['news_p']=para.text

        results.append(news)

    mars_data["news"] = results
    print(results)

    browser.visit("https://spaceimages-mars.com/")

    # Add the page source to the variable `content`.
    content = browser.html
    # Load the contents of the page, its source, into BeautifulSoup 
    # class, which analyzes the HTML as a nested data structure and allows to select
    # its elements by using various selectors.
    soup = BeautifulSoup(content,features="lxml")
    print(soup.prettify)

    imgtag = soup.find(attrs={'class':'headerimage fade-in'})
    featured_image_url = imgtag['src']

    mars_data["space_img"] = featured_image_url

    #pulling table using pandas to scrap
    #then exporting to be used later in flask
    tables = pd.read_html("https://galaxyfacts-mars.com")
    mars_facts = tables[1]
    mars_facts.columns = ["Data Type", "Info"]
    mars_facts.drop(index=mars_facts.index[0], axis=0,inplace=True)
    mars_facts = mars_facts.set_index("Data Type")

    mars_data["facts_table"] = mars_facts.to_html()

    #connecting to the hemisphere page
    browser.visit("https://marshemispheres.com/")
    content = browser.html

    soup = BeautifulSoup(content,features="lxml")


    # In[37]:


    #grabbing the headers text of images on home page that have links
    mars_hemispheres = []

    for x in soup.findAll("div", attrs={"class": "item"}):
        ltext = x.find("h3")
        if ltext:
            mars_hemispheres.append(ltext.text)

    #making connection with browser to run the click loop
    browser.visit("https://marshemispheres.com/")

    #click loop that finds the name and url of the original images
    hemis_imgs = []

    for m in mars_hemispheres:
        hemis = {}
        
        browser.find_by_text(m).first.click()
        visit = browser.links.find_by_partial_href(".tif").first
        hemis["tif_url"] = visit["href"]
        hemis["title"] = browser.find_by_css("h2.title").text
        
        hemis_imgs.append(hemis)
        
        browser.back()
        
        
    browser.quit()

    mars_data["hemi_pics"] = hemis_imgs
    return mars_data