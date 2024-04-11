from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import mysql.connector
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
            
            Tweet = article.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
            Tweets.append(Tweet)
            
            Reply = article.find_element(By.CSS_SELECTOR, "span[data-testid='app-text-transition-container']").text
            Replys.append(Reply)

            retweet = article.find_element(By.CSS_SELECTOR, "div[data-testid='retweet']").text
            retweets.append(retweet)

            like = article.find_element(By.CSS_SELECTOR, "div[data-testid='like']").text
            likes.append(like)
            
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

# Combine lists into a list of tuples
tweet_data = []
for i in range(len(UserTags) - 1):
    tweet_data.append((UserTags[i], Tweets[i], Replys[i], retweets[i], likes[i]))

# Connect to MySQL and insert data
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="tweets"
    )

    cursor = connection.cursor()

    # Insert data into MySQL
    sql = "INSERT INTO tweets (UserTag, Tweet, Reply, Retweet, Likes) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, tweet_data)
    connection.commit()

    print(f"{cursor.rowcount} records inserted successfully.")

except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table:", error)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

driver.quit()