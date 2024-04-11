#csv file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
from datetime import datetime
from selenium.webdriver.chrome.service import Service
import json

with open('twitter_keys.json', 'r') as file:
    data = json.load(file)

uname = data['username']
passwd = data['password']

s = "C:\Drivers\Chrome\chromedriver.exe"
driver = webdriver.Chrome(s)
driver.get("https://twitter.com/login")

subject = "Elon Musk"
start_date = "2024-01-01T00:00:00Z"
end_date = "2024-02-01T00:00:00Z"

# Setup the log in
sleep(3)
username = driver.find_element(By.XPATH, "//input[@name='text']")
username.send_keys(uname)
next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
next_button.click()

sleep(3)
password = driver.find_element(By.XPATH, "//input[@name='password']")
password.send_keys(passwd)
log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
log_in.click()

# Search for the subject
sleep(5)  # Added sleep to allow page to load
search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(subject)
search_box.send_keys(Keys.ENTER)

UserTags = []
Tweets = []
Replys = []
retweets = []
likes = []

articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
while True:
    for article in articles:
        try:
            UserTag = article.find_element(By.CSS_SELECTOR, "span.css-1qaijid.r-bcqeeo.r-qvutc0.r-poiln3").text
            UserTags.append(UserTag)
            #print(UserTag)
            
            Tweet = article.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
            Tweets.append(Tweet)
            #print(Tweet)
            
            Reply = article.find_element(By.CSS_SELECTOR, "span[data-testid='app-text-transition-container']").text
            Replys.append(Reply)
            #print(Reply)

            retweet = article.find_element(By.CSS_SELECTOR, "div[data-testid='retweet']").text
            retweets.append(retweet)
            print(retweet)

            like = article.find_element(By.CSS_SELECTOR, "div[data-testid='like']").text
            likes.append(like)
            print(like)
            
        except:
            continue


    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(3)
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    Tweets2 = list(set(Tweets))
    if len(Tweets2) > 5:
        break

    if len(UserTags) >= 5:
        break

# Combine lists into a list of dictionaries
tweet_list = []
for i in range(len(UserTags) - 1):
    tweet_dict = {
        'UserTag': UserTags[i],
        'Tweet': Tweets[i],
        'Reply': Replys[i],
        'Retweet': retweets[i],
        'Likes' : likes[i]
    }
    tweet_list.append(tweet_dict)
    print(tweet_list)

# Save tweets to CSV
csv_file = "twitter_data.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['UserTag', 'Tweet', 'Reply', 'Retweet', 'Likes'])
    writer.writeheader()
    for tweet in tweet_list:
        writer.writerow(tweet)

print(f"Data saved to {csv_file}")

driver.quit()