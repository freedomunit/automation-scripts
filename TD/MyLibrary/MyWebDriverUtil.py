from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time,math,string,sys
import os
import robot
from robot.errors import DataError
from Selenium2Library import webdrivermonkeypatches
from Selenium2Library.utils import BrowserCache
from Selenium2Library.locators import WindowManager

def openChromeBrowser(url,chrome_profile): 	
	chromedriver = "C:\Python27\chromedriver.exe";
	os.environ["webdriver.chrome.driver"] = chromedriver;
	options = webdriver.ChromeOptions();
	chrome_args = chrome_profile.split(";");
	for arg in chrome_args:
		options.add_argument(arg);
	browser = webdriver.Chrome(chromedriver,chrome_options=options);
	browser.get(url);
	return browser

if __name__ == "__main__":		
	openChromeBrowser()		

