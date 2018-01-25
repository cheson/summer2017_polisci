#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: July 31, 2017
# Complete script for scraping speeches of entities from Votesmart.com
# Usage:
# 1. set get_urls to True, set get_speeches to True
# Note that you can get the urls of speeches and speech bodies separately
# 2. set a results folder 
# 3. provide a list of targets structured with 'firstname_lastname'
#	 if target_list is None, program defaults to target_list_alt

# Two common reasons for failure are duplicate names in the votesmart database, 
# and both require manual searching for the correct name to id match 
# in votesmart_id_matrix.csv
# 1. Make sure that the id used corresponds to the correct entity you're looking for.
# 2. Some names are not listed by official first/last name.  

import os
import time
import sys

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from find_votesmart_ids import find_votesmart_ids
from parse_governors import parse_old_governors, parse_current_governors

main_driver = webdriver.Chrome('./chromedriver')
helper_driver = webdriver.Chrome('./chromedriver')

################ SETTINGS ################
get_urls = True 
get_speeches = True
verbose = False
results_folder = 'outputs/current_governors/'
target_list_alt = parse_current_governors
target_list = None # eg. ['hillary_clinton', 'barack_obama']
################ SETTINGS ################

# https://votesmart.org/candidate/public-statements/50344/gary-herbert#.WYk0D9PytTY
# from a page like ^, harvest all the urls on just that page
def harvest_urls(driver, urls_list):
	tables = driver.find_elements_by_tag_name("table")
	if len(tables) < 2:
		return
	link_table = tables[1]
	rows = link_table.find_elements_by_tag_name("tr")
	rows = rows[1:] #the first row is just the date / title header row, should be chopped

	for row in rows:
		row_data = row.find_elements_by_tag_name("td")
		date = row_data[0]
		headline = row_data[1]
		link = row_data[1].find_element_by_tag_name("a").get_attribute("href")
		if verbose == True:
			print "headline: " + headline.text
			print "link: " + link
		urls_list.append(link)

# saves the results for one target
def save_results(target, speech_urls, results_folder):
	print "saving for " + target
	with open (results_folder + target + '.txt', 'w') as results_file:
		for url in speech_urls:
	  		print>>results_file, url


def scrape_all_speech_urls(target_list):
	# use find_votesmart_ids(governor_list) to generate this id map
	# governor_list = parse_current_governors()

	if target_list == None:
		target_list = target_list_alt()
	internal_ids = find_votesmart_ids(target_list)
	
	targets_not_found = []

	main_driver.get("https://votesmart.org/")
	print "main driver finished loading votesmart homepage"

	targets = internal_ids.keys()

	for target in targets:
		if (os.path.isfile(results_folder + "/" + target + ".txt")):
			print target, "file exists already"
			continue
		try:
			print "starting scraping for: " + target

			speech_urls = []
			internal_id = internal_ids[target]

			# get ids from find_votesmart_ids function, then generate the following url:
			# example: https://votesmart.org/candidate/public-statements/15723
			target_url = "https://votesmart.org/candidate/public-statements/" + str(internal_id)
			helper_driver.get(target_url)

			# PAGINATION:
			# get the len of find_elements_by_tag_name("li") 
			try: 
				pagination = helper_driver.find_element_by_class_name("range")
				line_nums = pagination.text.splitlines()
				num_pages = int(line_nums[len(line_nums) - 1])

			# edge case: if no pagination for ZERO speeches or just ONE page
			# ZERO SPEECHES: https://votesmart.org/candidate/public-statements/4761/colleen-garry#.WXt5ztMrJTa
			# ONE PAGE: https://votesmart.org/candidate/public-statements/24685/jeff-van-drew#.WXt5vdMrJTY
			except: 

				try: 
					notice = helper_driver.find_element_by_class_name("notice")
					if notice.text == 'No matching public statements found.':
						print "[votesmart] " + notice.text
						print target + " has no speeches in votesmart database"
						targets_not_found.append(target)
						continue
				except: 
					harvest_urls(helper_driver, speech_urls)
					save_results(target, speech_urls, results_folder)
					continue
			print "num pages: " + str(num_pages)

			#For each page, GRAB ALL THE LINKS and save them in speech_urls
			current_url = helper_driver.current_url
			current_url = current_url[:current_url.index("#")] # helps to generate paginated link
			
			# python range(start, stop) includes the start number but excludes the stop number
			for i in range(1, num_pages + 1): 
				print "scraping page " + str(i)
				# for pagination, just take the url returned by driver.current_url(), remove everything after the # sign
				# https://votesmart.org/candidate/public-statements/15723/donald-trump#.WXRd-NMrKRs
				# then append '//?s=date&p=2' where 2 is replaced by i
				paginated_url = current_url + "//?s=date&p=" + str(i)
				helper_driver.get(paginated_url)
				print "page " + str(i) + " loaded"

				harvest_urls(helper_driver, speech_urls)

				# saves results after each round of scraping speech links (more robust to failure)
				# results stored in text files with same name as politician
			save_results(target, speech_urls, results_folder)
		except: 
			print "Unexpected error: ", sys.exc_info()[0]
	print "list of targets not found: ", targets_not_found

# https://votesmart.org/public-statement/1170550/wasatch-resource-recovery-groundbreaking#.WYk0XdPytTY
# given a list of urls like ^, go to each url and harvest the body text
def scrape_all_speeches():
	# for link_file in url_results folder:
	for filename in os.listdir(results_folder):
		if filename == '.DS_Store': # ignore DS_Store
			continue
		name = filename.replace(".txt", "")
		if os.path.isdir(results_folder + "/" + name) == True:
			print name, "speech directory already exists"
			continue

		print "scraping speeches of " + name
		os.makedirs(results_folder + name)
		print results_folder + filename
		with open(results_folder + filename) as f:
			print "f: ", f
			counter = 0
			for link in f:
				counter += 1
				time.sleep(0.5) #courtesy pause to votesmart server, could remove or set to 0.
				helper_driver.get(link)
        		### METADATA ###
        			#headline
	        		#author
	        		#date
	        		#location
	        		#source
	        	### CONTENT ###
	        		# all the paragraphs

	        	# easier solution - just use (note there are multiple sections but the first is the article:
	        	# article_section = helper_driver.find_element_by_class_name("section")
	        	# print article_section.text
				try:
					article_section = helper_driver.find_element_by_class_name("section")	     
					with open(results_folder + name + "/" + str(counter) + ".txt", 'w') as article:
						print>>article, article_section.text.encode('utf-8')
				except:
					print "article not found for link: " + link
	
def main():
	if get_urls:
		scrape_all_speech_urls(target_list)
	if get_speeches:
		scrape_all_speeches()

main()



####################################################################################################
### FAILED APPROACH DUE TO NOT BEING ABLE TO GET INTERNAL ID ###
	# elem = main_driver.find_element_by_name("q")

	# elem.clear()
	# elem.send_keys(target)
	# elem.send_keys(Keys.RETURN)

	# FAIL: Keys.RETURN doesn't actually select
	# speech_id = main_driver.find_element_by_id("folder-speech")
	# #print speech_id.get_attribute("href") 
	# #this should give something like: 
	# #https://votesmart.org/candidate/public-statements/15723
	# #where 15723 is the internal ID of this candidate for the website
	# print "speech url for " + target + " is: " + speech_id.get_attribute("href")

	# FAIL: SELECT doesn't print out option text to match politician name
	# dropdown_menu = main_driver.find_element_by_id("webmenu")
	# dropdown_menu = Select(main_driver.find_element_by_id("webmenu"))
	# options = dropdown_menu.options
	# # https://stackoverflow.com/questions/18515692/listing-select-option-values-with-selenium-and-python
	# options = [x for x in dropdown_menu.find_elements_by_tag_name("option")]
	# for element in options:
 	# 	internal_id = element.get_attribute("value")
 	# 	name = element.text
 	# 	print name

	# helper_driver.get(speech_id.get_attribute("href"))

	# figure out error processing if this doesn't exist

### SOLUTION: get ids separately, then generate the following url: ###
	#target_url = "https://votesmart.org/candidate/public-statements/" + str(internal_id)


### MISC + PSEUDOCODE ### 

# driver.get("article link")
# use xpath or direct string matching to capture the itemprops
# first check for all metadata if available: date (<span itemprop="datePublished">), author(s) (<span itemprop="author">)
#  , location (<span itemprop="contentLocation">)
#  , title (class=public-statements-title", source
# for the body with <div itemprop="articleBody">
# 	get all the <p> //find_elements_by_tag_name("p")
# 	print all the paragraphs out

# ==


# for each politician: //figure out how to get the politician id number DONE
# 	for each page: //figure out pagination 
# 		get all the links on this page //DONE 
# 	for all the links of this politician:
# 		navigate to the page containing this speech
# 		report all the metadata
# 		report all the body text of the speech


# now figure out how to get all the links on this page, then the pagination 

# for each itemprop, grab the properties of the article
# then in itemprop "articleBody", grab all the paragraphs as well as the source. 


# folder-speech
