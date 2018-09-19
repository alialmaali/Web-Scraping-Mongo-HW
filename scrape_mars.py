
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# In[2]:


## Mac Users
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
#!which chromedriver


# In[3]:


# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path, headless=False)


# ## Windows User

# ## NASA Mars News

# In[4]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[5]:


url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)


# In[6]:


# Iterate through all pages
News = []
for x in range(1):
    # HTML object
    html = browser.html
    # HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # all elements that contain title information
    News_titles = soup.find_all('div', class_='content_title')

    # Iterate through each title
    for div in News_titles:
        # Beautiful Soup's find() method to navigate and retrieve attributes
        a = div.find('a')
        news_title = a.text
        News.append({
            "news_title":news_title})

        print()
        print('-----------')
        print()
        print('news_title: ' + news_title)
        


# In[7]:


# Iterate through all pages
for x in range(1):
    # HTML object
    html = browser.html
    # HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # all elements that contain title information
    news_ps = soup.find_all('div', class_='article_teaser_body')

    # Iterate through each title
    for div in news_ps:
        # Beautiful Soup's find() method to navigate and retrieve attributes
        news_p = div.text
        News.append({
            "news_p":news_p})
        print()
        print('----------------------------------')
        print()
        print('news_p: ' + news_p)


# ## JPL Mars Space Images - Featured Image

# In[8]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[9]:


url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url1)


# In[10]:


# Iterate through all pages
image_url = []
for x in range(1):
    # HTML object
    html = browser.html
    # HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # all elements that contain image information
    images = soup.find_all('div', class_='img')

    # Iterate through each title
    for div in images:
        # Beautiful Soup's find() method to navigate and retrieve attributes
        img = div.find('img')
        featured_image_url = img['src']
        image_url.append({
            "featured_image_url":featured_image_url})
        print()
        print('-----------')
        print()
        print('featured_image_url = ' + 'https://www.jpl.nasa.gov'+featured_image_url)


# ## Mars Weather

# In[11]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[12]:


url2 = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url2)


# In[13]:


# Iterate through all pages
weather =[]
for x in range(50):
    # HTML object
    html = browser.html
    # HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # all elements that contain weather information
    tweets = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    # Iterate through each title
    for p in tweets:
        # Beautiful Soup's find() method to navigate and retrieve attributes
        mars_weather = p.text
        weather.append({"mars_weather": mars_weather})
        print()
        print('-----------')
        print()
        print('mars_weather = ' + mars_weather)


# ## Mars Facts 

# In[14]:


url = 'https://space-facts.com/mars/'


# In[15]:


tables = pd.read_html(url)
tables


# In[16]:


df = tables[0]
df.columns = ['Fact','Value']
df.head()


# In[17]:


html_table = df.to_html()
html_table


# In[18]:


html_table.replace('\n', '')


# In[19]:


df.to_html('table.html')


# In[20]:


l={}
for x in tables[0]:
    #print(x)
    l[x]=[]
    for y in tables[0][x]:
        l[x].append(y)
        #print(y)
#print(l)
MarsFacts=[]
for i in range(len(l["Fact"])):
    MarsFacts.append((l["Fact"][i].replace(":", ""),l["Value"][i]))
    
print(MarsFacts)


# ## Mars Hemispheres

# In[21]:


url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


# In[22]:


images = soup.find_all('div', class_='item')

hemisphere_image_urls = []
for div in images:
    title = div.find('a', class_='itemLink').find('h3').text
    image = div.find('a', class_='itemLink').find('img')
    link = div.find('a', class_='itemLink')
    link = "https://astrogeology.usgs.gov" + link["href"]
    news_image = "https://astrogeology.usgs.gov" + image["src"]
    response2 = requests.get(link)
    soup2 = BeautifulSoup(response2.text, "html.parser")
    image2 = soup2.find('div', class_='downloads').find('li').find('a')
    link2 = image2["href"]
    #print(news_image, link2)
    hemisphere_image_urls.append({
        "title":title,
        "link":link,
        "full_image":link2,
        "img_url":news_image
    })
print("-"*64)
print(hemisphere_image_urls)

import pymongo

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.mars_db



db.mars_news.drop()

db.mars_news.insert_many(News)



db.mars_images.drop()

db.mars_images.insert_many(image_url)



db.mars_weather.drop()

db.mars_weather.insert_many(weather)



    # Mars Facts

     



db.mars_facts.drop()

db.mars_facts.insert_many([{"facts":html_table}])



db.mars_facts2.drop()

db.mars_facts2.insert_many([{"facts":MarsFacts}])



    # Mars Hemispheres

db.mars_hemisphere.drop()

db.mars_hemisphere.insert_many(hemisphere_image_urls)