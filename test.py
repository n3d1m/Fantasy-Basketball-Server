import os
import time
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from webdriver_manager.chrome import ChromeDriverManager


def get_credentials(user=None):
    '''
    This function identifies the SWID and ESPN_S2 for a user using Selenium.

    The function will identify the default Chrome profile for a user on the
    machine, and open up a browser using this account.

    The user will be prompted to sign in to their ESPN account if they are
    not auto-signed in by their browser.

    The swid and espn_s2 cookies are identified and returned.
    '''
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    except InvalidArgumentException as e:
        if "user data directory is already in use" in str(e):
            # driver.close()  # Close window
            raise Exception(
                "Chrome is already open in another window. Please close all other Chrome windows and re-launch.")

    # Navigate to ESPN website for league and login
    driver.get('https://fantasy.espn.com/')

    # Check if user is logged in automatically by browser
    cookies = [cookie["name"]
               for cookie in driver.get_cookies()]  # Get list of cookie names
    if ("SWID" not in cookies) or ("espn_s2" not in cookies):
        # Wait for user to log in maunally
        print("[FETCHING CREDENTIALS] Login to ESPN account in browser.")
        driver.find_element_by_xpath('//*[@id="global-user-trigger"]').click()
        # driver.find_element_by_xpath('//*[@id="global-viewport"]/div[3]/div/ul[1]/li[7]/a').click()
        while True:
            time.sleep(5)
            # Get updated list of cookie names
            cookies = [cookie["name"] for cookie in driver.get_cookies()]
            if ("SWID" in cookies) and ("espn_s2" in cookies):
                print("[FETCHING CREDENTIALS] Login detected.")
                break
            print("[FETCHING CREDENTIALS] Login not detected... waiting 5 seconds...")
    else:
        print("[FETCHING CREDENTIALS] Login detected.")
        pass

    # Identify cookies for user
    swid, espn_s2 = None, None
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'SWID':
            swid = cookie['value'][1:-1]
        if cookie['name'] == 'espn_s2':
            espn_s2 = cookie['value']

    # return driver
    if swid is None:
        raise Exception("[FETCHING CREDENTIALS] ERROR: SWID cookie not found.")
    if espn_s2 is None:
        raise Exception("[FETCHING CREDENTIALS] ERROR: SWID cookie not found.")

    # Close the browser
    driver.close()

    print("[FETCHING CREDENTIALS] ESPN Credenitals:\n[FETCHING CREDENTIALS] ---------------------")
    print("[FETCHING CREDENTIALS] swid: {}\n[FETCHING CREDENTIALS] espn_s2: {}".format(
        swid, espn_s2))
    return swid, espn_s2


values = get_credentials()

print(values)
