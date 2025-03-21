"""
Complete Script for Facebook Automation

Features:
1. Login to multiple Facebook accounts and save cookies for session reuse.
2. Load cookies for auto-login if available.
3. Like and comment on a specific Facebook post using Selenium.
4. Alternatively, like and comment on the post using the Facebook Graph API with a token.

Note: Use responsibly and ensure compliance with Facebook's terms of service.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# CONFIGURATION
# -------------------------------

# Update with your Facebook account credentials
FB_ACCOUNTS = [
    {"email": "vishesh@brancosoft.com", "password": "Brancosoft@1234"},
    
]

# URL of the Facebook post you want to interact with
POST_URL = "https://www.facebook.com/photo/?fbid=623100420433417&set=a.282440087832787"  # Replace with actual post URL

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

def login_and_save_cookies(account):
    """
    Logs into Facebook with the given account credentials
    and saves the session cookies to a file for later reuse.
    """
    driver.get("https://www.facebook.com/")
    time.sleep(3)  # Wait for page to load

    # Enter credentials and log in
    driver.find_element(By.ID, "email").send_keys(account["email"])
    driver.find_element(By.ID, "pass").send_keys(account["password"])
    driver.find_element(By.NAME, "login").click()
    time.sleep(20)

    time.sleep(5)  # Wait for login to complete

    # Save cookies to a file named after the account's username (part before @)
    cookie_file = f"cookies_{account['email'].split('@')[0]}.pkl"
    with open(cookie_file, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"Login successful for {account['email']} and cookies saved to {cookie_file}")


def load_cookies(account):
    """
    Loads saved cookies for the given account if available.
    If not found, performs a manual login and saves the cookies.
    """
    driver.get("https://www.facebook.com/")
    time.sleep(3)

    cookie_file = f"cookies_{account['email'].split('@')[0]}.pkl"
    try:
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            # Add cookie to the current browser session
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(3)
        print(f"Logged in using cookies for {account['email']}")
    except FileNotFoundError:
        print(f"No cookies found for {account['email']}, logging in manually.")
        login_and_save_cookies(account)


def like_and_comment(post_url, comment_text):
    """
    Opens the specified Facebook post URL, clicks the Like button,
    and posts a comment using Selenium.
    """
    driver.get(post_url)
    time.sleep(5)  # Wait for post to load

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

def logout():
    try:
        # Open account settings menu
        driver.get("https://www.facebook.com/")
        time.sleep(3)

        WebDriverWait(driver, 10).until(
            lambda d : d.find_elements(By.CSS_SELECTOR, "span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x4k7w5x.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j")
        )

        menu_button = driver.find_elements(By.CSS_SELECTOR, "span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x4k7w5x.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j")
        if menu_button : 
            profile_menu = menu_button[6]
            profile_menu.click()
            time.sleep(5)
        else : 
            print("profile menu not found")


        

        time.sleep(3)

        # Click on logout button
        logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log out')]"))
        )
        logout_button.click()
        

        # Clear browser cookies to remove saved session
        
        print("Logged out successfully and cleared cookies.")

    except Exception as e:
        print(f"Error while logging out: {e}")
def selenium_workflow():
    """
    Logs in each account using cookies (or manual login if needed),
    then likes and comments on a Facebook post.
    """
    # Loop through each Facebook account
    for account in FB_ACCOUNTS:
        load_cookies(account)
        # For each account, perform the like and comment actions
        # like_and_comment(POST_URL, COMMENT_TEXT)
        logout()
    # After processing all accounts, quit the browser
    driver.quit()



# -------------------------------
# MAIN EXECUTION
# -------------------------------

def main():
    # Choose one of the workflows:
    selenium_workflow()  # Use Selenium-based workflow
if __name__ == "__main__":
    main()
