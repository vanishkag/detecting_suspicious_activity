from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from hdfs import InsecureClient
import json

with open('twitter_keys.json', 'r') as file:
    data = json.load(file)

uname = data['username']
passwd = data['password']

client = InsecureClient('http://localhost:9870', user='vanis')

s = "C:\\Drivers\\Chrome\\chromedriver.exe"
driver = webdriver.Chrome(s)
driver.get("https://twitter.com/login")

subject = "@SheroneDSouza"
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
sleep(40)  # Added sleep to allow page to load
search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(subject)
search_box.send_keys(Keys.ENTER)

sleep(5)

first_account = driver.find_element(By.CSS_SELECTOR, ".css-175oi2r.r-1awozwy.r-18u37iz.r-1wtj0ep")
first_account.click()

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
    if len(Tweets2) > 25:
        break

    if len(UserTags) >= 25:
        break

# Combine lists into a list of dictionaries
tweet_data = []
for i in range(len(UserTags)):
    tweet_dict = {
        'UserTag': UserTags[i],
        'Tweet': Tweets[i],
        'Reply': Replys[i],
        'Retweet': retweets[i],
        'Likes': likes[i]
    }
    tweet_data.append(tweet_dict)

# Save data to JSON file with error handling
json_file = "C:\\Users\\vanis\\Downloads\\twitter_data.json"
try:
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(tweet_data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {json_file}")
except Exception as e:
    print(f"Error saving data to {json_file}: {str(e)}")

driver.quit()

hdfs_file_path = '/twitter_data/twitter_data.json'

# Check if file exists
try:
    if client.status(hdfs_file_path, strict=False):
        # Delete the existing file
        client.delete(hdfs_file_path)
        print(f"Existing file {hdfs_file_path} deleted.")
except Exception as err:
    if 'not a directory' in str(err):
        print(f"Error: {err}")
    else:
        raise err

# Upload new file to HDFS

try:
    client.upload(hdfs_file_path, json_file)
    print(f"File {json_file} uploaded to {hdfs_file_path}.")
except Exception as err:
    print(f"Error uploading file to HDFS: {err}")

