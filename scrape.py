from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import json
import requests

def run():
    username = input("")
    myUrl = "https://twitter.com/"+username
    uClient = urlopen(myUrl)
    pageHtml = uClient.read()
    uClient.close()
    pageSoup = soup(pageHtml, 'html.parser')

    file = "output/"+username+".csv"
    f = open(file, "w")

    header = "Time, Date, TweetText\n"
    f.write(header)

    f.close()

    next_pointer = pageSoup.find(
        "div", {"class": "stream-container"})["data-min-position"]

    while True:
        next_url = "https://twitter.com/i/profiles/show/" + username + \
            "/timeline/tweets?include_available_features=1&" \
            "include_entities=1&max_position=" + next_pointer + "&reset_error_state=false"

        next_response = None
        next_response = requests.get(next_url)

        tweets_data = next_response.text
        tweets_obj = json.loads(tweets_data)

        if not tweets_obj["has_more_items"] and not tweets_obj["min_position"]:
            print("\nNo more tweets returned")
            break

        next_pointer = tweets_obj["min_position"]
        html = tweets_obj["items_html"]
        pageSoup = soup(html, 'html.parser')
        pageTweets(pageSoup, file)


def pageTweets(pageSoup, file):
    f = open(file, "a")

    tweets = pageSoup.find_all("li", {"data-item-type": "tweet"})

    for tweet in tweets:
        timeclass = tweet.find("small", {"class": "time"})
        timestamp = timeclass.a["title"]
        time = timestamp.split(' - ')[0]
        date = timestamp.split(' - ')[1]

        tweetBox = tweet.find(
            "p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
        tweetText = tweetBox.text.strip()

        f.write(time.replace(",", " ") + "," + date.replace(",", " ") +
                "," + tweetText.replace(",", " ").replace("\n", " ") + "\n")
    
    f.close()

if __name__== "__main__":
    run()