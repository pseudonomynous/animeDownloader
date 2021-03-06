import os
from os import listdir
from os.path import isfile, join
from os import walk

import time
import requests
import urllib.request

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

import sys

#====================================================================================================#

display = Display(visible=0, size=(800, 800))
display.start()

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#====================================================================================================#

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
print ("Headless Chrome Initialized")

params = {'behavior': 'allow', 'downloadPath': r''}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
download_dir = '/Downloads'

#====================================================================================================#

def enable_download(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)

def setting_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    return chrome_options;
def isFileDownloaded():
    file_path = download_dir+"\python_samples-master.zip"
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.isfile(file_path):
        print("File Downloaded successfully..")

#====================================================================================================#

myAnimeDir = "/home/myAnime.txt"
myAnime = open(myAnimeDir, "a+")
print(myAnime.read())

#====================================================================================================#

def existsInList(link):
	with open(myAnimeDir) as f:
		if link in f.read():
			return True
		else:
			return False

#====================================================================================================#

def addToList(link, title, season, loc, subOrDub):
	if not existsInList(link):
		myAnime.write(title + ', ' + link + ', ' + season + ', ' + subOrDub + '\n')
		print(myAnime.read())

#====================================================================================================#

def updateAnime():
	with open(myAnimeDir) as file:
		for myline in file:
			if(len(myline) == 1):
				print('', end = '')
				# print('Empty Line')
			elif(myline.lstrip()[0] == '#'):		# Entire line is a comment, possibly some leading whitespace
				print('', end = '')
				# print('Comment: ' + myline.lstrip())
			else:
				array = myline.split(',', 3)	# Splits into 4 parts just in case comment contains, uh, a few, uh, commas
				title = array[0].lstrip()
				link = array[1].lstrip()
				season = array[2].lstrip()
				if('#' in array[3]):		# second part of the line is a comment, after the anime info, possibly with leading whitespace.
					subOrDub = array[3].split('#', 1)[0].rstrip().lstrip()
					# print('Comment: #' + array[3].split('#', 1)[1])
				else:
					subOrDub = array[3].lstrip().rstrip()
				loc = '/home'
				download(link, title, season, loc, subOrDub)

#====================================================================================================#

def download(link, title, season, loc, subOrDub):

	#================================================================================================#

	addToList(link, title, season, loc, subOrDub)
	# with open(myAnimeDir) as f:
	# 	if link not in f.read():
	# 		myAnime.write(title + ', ' + link + ', ' + season + ', ' + subOrDub + '\n')
	# 	print(myAnime.read())

	#================================================================================================#

	if(subOrDub == 's'):
		title += ' (Sub)'
	if(subOrDub == 'd'):
		title += ' (Dub)'

	#================================================================================================#

	loc = loc + "/" + title
	loc = Path(loc)
	if not os.path.exists(loc):
		os.mkdir(loc)

	#================================================================================================#

	driver.get(link)
	time.sleep(20)
	epList = driver.find_element_by_xpath("//ul[contains(@id, 'episode_related')]")

	linkArray = []
	epNumArray = []

	eps = epList.find_elements_by_tag_name('li')
	for ep in eps:
		temp = ep.find_element_by_tag_name('a')
		linkArray.append(temp.get_attribute('href'))
		temp2 = temp.find_element_by_tag_name('div')
		epNumArray.append(temp2.text.split("EP ", 1)[1])

	linkArray = linkArray[::-1]
	epNumArray = epNumArray[::-1]

	#================================================================================================#
	# ADD FUNCTIONALITY FOR EPISODES THAT ARE WEIRD FORMATS LIKE 24.5 OR 24.9
	print("================================================================================\n")
	print('Downloading Episodes ' + str(epNumArray[0]) + '-' + str(epNumArray[len(epNumArray) - 1]) + ' of ' + title)
	for i in range(0, len(linkArray)):

		if(int(float(epNumArray[i])) < 10):
			if(int(float(season)) < 10):
				fileName = title + ' ' + 'S0' + season + 'E' + '0' + epNumArray[i] + '.mp4'
			else:
				fileName = title + ' ' + 'S' + season + 'E' + '0' + epNumArray[i] + '.mp4'
		else:
			if(int(float(season)) < 10):
				fileName = title + ' ' + 'S0' + season + 'E' + epNumArray[i] + '.mp4'
			else:
				fileName = title + ' ' + 'S' + season + 'E' + epNumArray[i] + '.mp4'

		fileToOpen = loc / fileName

		if(not os.path.exists(fileToOpen)):		# Checks to see if the file is already downloaded.
			link = linkArray[i]
			driver.get(link);

			elems = driver.find_elements_by_xpath("//a[@href]")
			for elem in elems:
				if(elem.get_attribute("href").find('gogo-play') != -1):
					print('Found Season ' + season + " Episode " + str(epNumArray[i]) + " of " + title + " on gogoanime.so")
					link = elem.get_attribute("href")

			driver.get(link)

			elems = driver.find_elements_by_xpath("//a[@href]")
			for elem in elems:
				if(elem.get_attribute("href").find('gogo-play') == -1):
					print('Found download link for Season ' + season + " Episode " + str(epNumArray[i]) + " of " + title)
					link = elem.get_attribute("href")
					file = elem
					break	# default to picking first one

			urllib.request.urlretrieve(link, fileToOpen)
		else:
			print(fileName + ' was already downloaded.')

#====================================================================================================#

arg1 = ''
shouldUpdate = ''
if(len(sys.argv) > 1):
	if(sys.argv[1] == 'update'):
		arg1 = 'update'
	if(sys.argv[1] == 'addAnime'):
		arg1 = 'addAnime'
shouldQuit = False
while(not shouldQuit):
	if(arg1 == ''):
		shouldUpdate = input('Update your anime [1] \nAdd a new anime [2]\nSearch for anime [3]\nQuit [4]\nInput: ')
	else:
		shouldQuit = True
	if(shouldUpdate == '1' or arg1 == 'update'):
		updateAnime()
	if(shouldUpdate == '2' or arg1 == 'addAnime'):
		link = input('Enter the gogoanime.so URL of the anime: ')
		if(not existsInList(link)):
			title = input('Enter the title you want: ')
			season = input('Enter the season of this anime: ')
			loc = '/home'
			subOrDub = input('Subbed or Dubbed (s/d): ')
			download(link, title, season, loc, subOrDub)
		else:
			print('Anime already exists on your list.')
	if(shouldUpdate == '3'):
		search = input('Enter the title of the anime you want to search for on gogoanime: ')
		words = search.split(' ')
		searchLink = 'https://gogoanime.so//search.html?keyword='
		for i in range(0, len(words)):
			searchLink = searchLink + words[i] + '%20'
		# print(searchLink)
		driver.get(searchLink)
		pageList = driver.find_element_by_class_name("items")

		linkArray = []

		pages = pageList.find_elements_by_tag_name('li')
		for page in pages:
			temp = page.find_element_by_tag_name('a')
			linkArray.append(temp.get_attribute('href'))
		for i in range(0, len(linkArray)):
			print(str(i + 1) + ': ' + linkArray[i])

		selection = input('Your download choice (enter 0 to cancel): ')
		if(selection == '0'):
			print('canceled')
		else:
			link = linkArray[int(selection) - 1]
			if(not existsInList(link)):
				title = input('Enter the title you want: ')
				season = input('Enter the season of this anime: ')
				loc = '/home'
				subOrDub = input('Subbed or Dubbed (s/d): ')
				addToList(link, title, season, loc, subOrDub)
				updateAnime()
			else:
				print('Anime already exists on your list.')
	if(shouldUpdate == '4'):
		shouldQuit = True

driver.quit()
print("Headless Chrome Instance Ended.")

#====================================================================================================#
