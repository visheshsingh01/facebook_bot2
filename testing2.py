import time  
import pickle
import pyotp
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# CONFIGURATION: MULTIPLE ACCOUNTS
# -------------------------------
ACCOUNTS = [
    # {
    #     # "email": "61573906285513",
    #     # "password": "uQkfrjEu3E",
    #     # "totp_secret": "2AUFRHHOGUEWUVNUFRTPYVJTXXX4IHUR",
    #     # "cookie_file": "fb_cookies_1.pkl"
    # },
    {
        "email": "61573836209356",
        "password": "474NTqiB4L",
        "totp_secret": "KAAKIVBSLCDCLCADOWDUGTCMAIJJ2LQ4",
        "cookie_file": "fb_cookies_2.pkl"
    },
    {
        "email": "61573883486915",
        "password": "5FDU0RLf82",
        "totp_secret": "3BDMCUD3LS3DKTLPAMCTVXWMB7YAPS35",
        "cookie_file": "fb_cookies_3.pkl"
    },
    {
        "email": "61573834079334",
        "password": "aJy0PNoy4j",
        "totp_secret": "CNFHGTDIJGEK4675UXA23ZNUZT333HB6",
        "cookie_file": "fb_cookies_4.pkl"
    },
    {
        "email": "61573906795526",
        "password": "odZWNRVa5S",
        "totp_secret": "P3NF7JMS6WPPO7IP3RD5YCTJ7BPLQPJQ",
        "cookie_file": "fb_cookies_5.pkl"
    },
    {
        "email": "61573439897500",
        "password": "8FZOqEdxNz",
        "totp_secret": "MSNOHY24SHUVXBWCGIRKKLVANC4BZSBI",
        "cookie_file": "fb_cookies_6.pkl"
    },
    {
        "email": "61573774562311",
        "password": "uQIyg1VB2V",
        "totp_secret": "SKYXTSJGDDXAUTCA7SCZ6JQXOPNMKMAA",
        "cookie_file": "fb_cookies_7.pkl"
    },
    {
        "email": "61573968802483",
        "password": "mht8Xma8Ih",
        "totp_secret": "DZBP2DUKKPXMVCUCSIIBW4MC6P4MO4YT",
        "cookie_file": "fb_cookies_8.pkl"
    },
    {
        "email": "61573957763037",
        "password": "5FSEskXTQK",
        "totp_secret": "CI6JJNX2L7HQGZO57KN7AAVX5YM5QN4K",
        "cookie_file": "fb_cookies_9.pkl"
    },
    {
        "email": "61573716094965",
        "password": "4nq453WQ8P",
        "totp_secret": "Q7LCFSWXKHV6HGDVG5J5DHCAH4AM34DP",
        "cookie_file": "fb_cookies_10.pkl"
    },
    {
        "email": "61573926174642",
        "password": "hroLLrXv0d",
        "totp_secret": "2THK3MAZYZRHGDI6L5UYAH2T4DZ3VOWE",
        "cookie_file": "fb_cookies_11.pkl"
    },
    {
        "email": "61573890746555",
        "password": "8mr7tUEtLQ",
        "totp_secret": "3OEWZZGK43QRJKQO7UGUKDKVTYLO7X3S",
        "cookie_file": "fb_cookies_12.pkl"
    },
    {
        "email": "61573960912950",
        "password": "T2MhjG652E",
        "totp_secret": "4XNMUAPM43KWCQPUX3K5PRVXMDPARYBW",
        "cookie_file": "fb_cookies_13.pkl"
    },
    {
        "email": "61573920204941",
        "password": "hljjZUsm6y",
        "totp_secret": "NBFZD5FIGODJNETAS44QK4UJ5DBN3PO5",
        "cookie_file": "fb_cookies_14.pkl"
    },
    {
        "email": "61573887086672",
        "password": "7XHZkvbylC",
        "totp_secret": "DQCH33PR3622HN7D7CFSO2OFV6MUTUL7",
        "cookie_file": "fb_cookies_15.pkl"
    },
    {
        "email": "61573841219099",
        "password": "1hEJ3ZyZT5",
        "totp_secret": "2HGV755EQP6MQHDMYUUNJFF24KIZPPYB",
        "cookie_file": "fb_cookies_16.pkl"
    }
]

POST_URL = "https://www.facebook.com/share/p/1A3LuMuomY/"
COMMENT_TEXT = "Great post!"
# -------------------------------
# SELENIUM SETUP
# -------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
# (Removed the global driver)

# -------------------------------
# FUNCTION DEFINITIONS
# -------------------------------

def login_with_2fa(account, driver):
    """
    Logs in to Facebook using credentials and a TOTP 2FA code,
    then saves the cookies to a unique file for each account.
    """
    print(f"🔄 Logging in for {account['email']}...")
    
    driver.get("https://www.facebook.com/")
    time.sleep(3)
    
    # Enter credentials
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys(account["email"])
    driver.find_element(By.ID, "pass").send_keys(account["password"])
    driver.find_element(By.NAME, "login").click()
    time.sleep(20)
    
    # Try to handle the 2FA prompt
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x3nfvp2.x1n2onr6.xh8yej3"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        element.click()
        print("✅ Clicked on element successfully!")
        try:
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, "label.x1lliihq.x1n2onr6.x19cbwz6.x79zeqe.xgugjxj.x2oemzd")) >= 2
            )
            elements = driver.find_elements(By.CSS_SELECTOR, "label.x1lliihq.x1n2onr6.x19cbwz6.x79zeqe.xgugjxj.x2oemzd")
            if len(elements) >= 2:
                second_element = elements[1]  
                driver.execute_script("arguments[0].scrollIntoView();", second_element)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(second_element)).click()
                print("✅ Clicked the second element")
                element2 = driver.find_element(By.CSS_SELECTOR, "div.x1ja2u2z.x78zum5.x2lah0s.x1n2onr6.xl56j7k.x6s0dn4.xozqiw3.x1q0g3np.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.xtvsq51.xdalh5k.x15astrn.x199f2m0.x1p366e6.x1otv196.x1tqnv13.x1db66uq")
                element2.click()
                time.sleep(5)
            else:
                print("❌ Still less than two elements found!")
        except Exception as e:
            print("⏳ Timeout: Elements did not appear in time.", e)
        # Generate and enter TOTP code
        totp = pyotp.TOTP(account["totp_secret"])
        twofa_code = totp.now()
        print(f"🔑 Generated 2FA code: {twofa_code}")
        otp_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.x1vr9vpq"))
        )
        otp_input.send_keys(twofa_code)
        time.sleep(3)
        submit = driver.find_element(By.CSS_SELECTOR, "div.x3nfvp2.x1n2onr6.xh8yej3")
        submit.click()
        time.sleep(5)
        try:
            driver.find_element(By.ID, "checkpointSubmitButton").click()
            time.sleep(10)
        except Exception:
            pass
    except Exception as e:
        print("No 2FA prompt found or could not locate the code input.", e)
    
    time.sleep(5)
    
    if "login" not in driver.current_url.lower():
        print(f"✅ Login successful for {account['email']}!")
        cookies = driver.get_cookies()
        with open(account["cookie_file"], "wb") as f:
            pickle.dump(cookies, f)
        print(f"🍪 Cookies saved to {account['cookie_file']}")
    else:
        print(f"❌ Login failed for {account['email']}.")

def load_cookies(account, driver):
    """
    Loads cookies from a file and refreshes the session.
    """
    driver.get("https://www.facebook.com/")
    time.sleep(3)
    
    try:
        with open(account["cookie_file"], "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(3)
        print(f"🔄 Logged in via saved cookies for {account['email']}!")
    except FileNotFoundError:
        print(f"⚠️ No cookie file found for {account['email']}. Logging in...")
        login_with_2fa(account, driver)

def logout(driver):
    try:
        # Open account settings menu
        driver.get("https://www.facebook.com/")
        time.sleep(3)
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, 
                "span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x4uap5.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j")
        )
        menu_buttons = driver.find_elements(By.CSS_SELECTOR, 
            "span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x4uap5.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j")
        if menu_buttons:
            profile_menu = menu_buttons[6]
            profile_menu.click()
            time.sleep(5)
        else:
            print("Profile menu not found")
        time.sleep(3)
        logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log out')]"))
        )
        logout_button.click()
        time.sleep(10)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        print("Logged out successfully and cleared cookies.")
    except Exception as e:
        print(f"Error while logging out: {e}")


def like_and_comment(driver, post_url, comment_text):
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

def process_account(account, options):
    driver = webdriver.Chrome(options=options)
    try:
        if os.path.exists(account["cookie_file"]):
            print("📝 Cookie file found. Attempting to load cookies...")
            load_cookies(account, driver)
        else:
            print("🔐 No cookie file found. Logging in with credentials and 2FA...")
            login_with_2fa(account, driver)
        time.sleep(5)
        like_and_comment(driver,POST_URL, COMMENT_TEXT)
        
    finally:
        driver.quit()

def main():
    for account in ACCOUNTS:
        print("=" * 50)
        print(f"🔹 Processing Account: {account['email']}")
        process_account(account, options)
    print("\n🎉 All accounts processed!")

if __name__ == "__main__":
    main()
