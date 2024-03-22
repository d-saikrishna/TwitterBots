from decouple import config
from requests_oauthlib import OAuth1
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')
bearer_token = config('bearer_token')

oauth = OAuth1(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
        )

# Get all tweet IDs
username = 'chaotic__neuron'
url = 'https://twitter.com/search?q=from%3A{}&src=typed_query&f=live'.format(username)
# Start a Chrome WebDriver session
driver = webdriver.Chrome()

# Open the webpage
driver.get(url)
time.sleep(15)
# Find the button element by its XPath

for i in range(3,10):
    analytics_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, 
                                        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[{}]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div/div[4]/a".format(i)
                                        )))
    
    # Click the button
    href = analytics_element.get_attribute('href')
    print(href)
    id = href.split('/')[-2]
    print(id)
    tweet_url = 'https://api.twitter.com/2/tweets'
    tweet_url = tweet_url+"/{}".format(id)
    response = requests.delete(tweet_url,
                            auth=oauth, 
                            )
    print(response)

# Close the WebDriver session
driver.quit()
exit()
tweets_list1 = []
scrapedtweets = sntwitter.TwitterSearchScraper('from:'+username).get_items()
print("***")
sliced = itertools.islice(scrapedtweets, 10)
df = pd.DataFrame(sliced)[['id']]
for i, tweet in enumerate(scrapedtweets):  # declare a username
    if i%1000==0:
        print(i) #number of tweets scraped in 1000s
    tweets_list1.append(tweet.id)  # declare the attributes to be returned

print(tweets_list1)
exit()
# Making the request
id = '1754895653740937553'
dont = '1506259564034809861'
# Twitter API endpoints
tweet_url = 'https://api.twitter.com/2/tweets'
tweet_url = tweet_url+"/{}".format(id)
print(tweet_url)

response = requests.delete(tweet_url,
                           auth=oauth, 
                           )
print(response)