"""
Complete Script for Facebook Automation Using Provided Cookies

Features:
1. Use an array of cookie strings to simulate logged-in sessions.
2. For each cookie, load Facebook, set the cookie, refresh the session,
   and perform like and comment actions on a specific Facebook post.

Note: Ensure these cookies represent valid, complete session data.
Use responsibly and ensure compliance with Facebook's terms of service.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# -------------------------------
# CONFIGURATION
# -------------------------------

# Array of cookie strings (each string represents one account's session cookie)
FB_COOKIES = [
    "61573949003413:cv1BU9MuQA:YSIGNEBX344OFYXN5R4AHXB5HTYC66NJ",
    "61573687806689:GRvClBpg20:ZOSGNBME7QBCRHIJU3OQALVEBQ5WV44O",
    "61573723444944:mmJr8dFfLF:AFKSLPKFOGGOZT6MYKIGWTSDUYW34ZX6",
    "61573906285513:uQkfrjEu3E:2AUFRHHOGUEWUVNUFRTPYVJTXXX4IHUR",
    "61573836209356:474NTqiB4L:KAAKIVBSLCDCLCADOWDUGTCMAIJJ2LQ4",
    "61573883486915:5FDU0RLf82:3BDMCUD3LS3DKTLPAMCTVXWMB7YAPS35",
    "61573834079334:aJy0PNoy4j:CNFHGTDIJGEK4675UXA23ZNUZT333HB6",
    "61573906795526:odZWNRVa5S:P3NF7JMS6WPPO7IP3RD5YCTJ7BPLQPJQ",
    "61573439897500:8FZOqEdxNz:MSNOHY24SHUVXBWCGIRKKLVANC4BZSBI",
    "61573774562311:uQIyg1VB2V:SKYXTSJGDDXAUTCA7SCZ6JQXOPNMKMAA",
    "61573968802483:mht8Xma8Ih:DZBP2DUKKPXMVCUCSIIBW4MC6P4MO4YT",
    "61573957763037:5FSEskXTQK:CI6JJNX2L7HQGZO57KN7AAVX5YM5QN4K",
    "61573716094965:4nq453WQ8P:Q7LCFSWXKHV6HGDVG5J5DHCAH4AM34DP",
    "61573926174642:hroLLrXv0d:2THK3MAZYZRHGDI6L5UYAH2T4DZ3VOWE",
    "61573890746555:8mr7tUEtLQ:3OEWZZGK43QRJKQO7UGUKDKVTYLO7X3S",
    "61573960912950:T2MhjG652E:4XNMUAPM43KWCQPUX3K5PRVXMDPARYBW",
    "61573920204941:hljjZUsm6y:NBFZD5FIGODJNETAS44QK4UJ5DBN3PO5",
    "61573887086672:7XHZkvbylC:DQCH33PR3622HN7D7CFSO2OFV6MUTUL7",
    "61573841219099:1hEJ3ZyZT5:2HGV755EQP6MQHDMYUUNJFF24KIZPPYB"
]

# URL of the Facebook post to interact with
POST_URL = "https://www.facebook.com/photo/?fbid=623100420433417&set=a.282440087832787"  # Replace with the actual post URL

# Comment text for Selenium automation
COMMENT_TEXT = "Great post!"

# -------------------------------
# SELENIUM SETUP
# -------------------------------

# Initialize Chrome options and disable notifications
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")

# Create a new WebDriver instance
driver = webdriver.Chrome(options=options)

# -------------------------------
# FUNCTION DEFINITIONS
# -------------------------------

def like_and_comment(post_url, comment_text):
    """
    Opens the specified Facebook post URL, clicks the Like button,
    and posts a comment using Selenium.
    """
    driver.get(post_url)
    time.sleep(5)  # Wait for the post to load

    # Attempt to click the Like button
    try:
        like_button = driver.find_element(By.XPATH, "//div[@aria-label='Like']")
        like_button.click()
        print("Liked the post!")
    except Exception as e:
        print("Like button not found.", e)

    time.sleep(2)

    # Attempt to post a comment
    try:
        comment_box = driver.find_element(By.XPATH, "//div[@aria-label='Write a comment…']")
        comment_box.click()
        time.sleep(2)
        comment_box.send_keys(comment_text)
        comment_box.send_keys(Keys.RETURN)
        print("Commented on the post!")
    except Exception as e:
        print("Comment box not found.", e)


def cookie_workflow():
    """
    Iterates over the provided cookie strings, sets each as the session cookie,
    and then likes and comments on the Facebook post.
    """
    for cookie_str in FB_COOKIES:
        # Start fresh by clearing any existing cookies
        driver.delete_all_cookies()

        # Open Facebook to set the domain for cookies
        driver.get("https://www.facebook.com/")
        time.sleep(3)

        # Here we assume the cookie string represents the value of a cookie named 'fbcookie'.
        # If you have multiple key/value pairs, you would need to parse them accordingly.
        driver.add_cookie({
            "name": "c_user",
            "value": cookie_str,
            "domain": ".facebook.com",
            "path": "/"
        })
        time.sleep(5)

        # Refresh to apply the cookie and load the logged-in session
        driver.refresh()
        time.sleep(3)

        # Now interact with the post
        like_and_comment(POST_URL, COMMENT_TEXT)
    
    driver.quit()

# -------------------------------
# MAIN EXECUTION
# -------------------------------

def main():
    cookie_workflow()  # Use the workflow that uses the provided cookies

if __name__ == "__main__":
    main()
