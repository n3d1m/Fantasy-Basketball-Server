from rest_framework import viewsets
from django.shortcuts import render
from .serializers import HeroSerializer
from .models import Hero
from django.http import HttpResponse
import os
import time
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from webdriver_manager.chrome import ChromeDriverManager


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer


def test(request):
    value = 'hello this is a function call'

    return HttpResponse(value)


def get_cookies(request):

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

    return_val = {"swid": swid, "espn_s2": espn_s2}

    return HttpResponse(return_val)


# class CookieViewSet(viewsets.ModelViewSet):
#     queryset = Cookies.objects.all().order_by('id')
#     serializer_class = CookieSerializer
