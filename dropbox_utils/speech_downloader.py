#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: July 24, 2017
# The speech downloader is a tool to automate the process of downloading folders from 
# a Dropbox repository. For this project, we needed to download the list of House and Senate
# speeches from the following links:

# https://www.dropbox.com/sh/z0jg216gx1l4omk/AABOzjnNSoqj0SQNEm24PG0Pa?dl=0 [HOUSE PRESS RELEASES]
# https://www.dropbox.com/sh/vdufknfreoljqp2/AAAZ6HYfAzySLaxbG3rAxMzJa?dl=0 [SENATE SPEECHES]

# You can call this program with the following terminal command: 
# python speech_downloader.py

import sys
import re
import os
import shutil
import urllib2
from sys import version_info
py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2

# Ensure that a folder exists to save the downloaded zip files.
results_dir = "zip_files"
if os.path.isdir(results_dir):
	print "The results directory: " + "\"" + results_dir + "\"" + " already exists."
	if py3:
  		response = input("Do you want to overwrite the current directory (y/n)? ")
	else:
  		response = raw_input("Do you want to overwrite the current directory (y/n)? ")
  	if 'y' in response:
  		shutil.rmtree(results_dir)
  	else:
  		results_dir = ""
  		while (not results_dir): # while results_dir is empty
  			if py3:
  				results_dir = input("Please enter an alternate results directory name: ")
			else:
  				results_dir = raw_input("Please enter an alternate results directory name: ")
os.mkdir(results_dir)

# You could inspect the source code of the dropbox page and copy over the relevant sections
# containing the links to the various folders into a file in this folder. "dropbox_src_code"
# is an example of doing so. However, this is written so that we parse out the links 
# automatically. The code may be not robust enough for other links so would need modification
# if it doesn't run automatically. 

# filename = "dropbox_src_code" 
# with open(filename) as f:
# 	page_source = f.read()
# 	link_blocks = page_source.split("<a ");

response = urllib2.urlopen("https://www.dropbox.com/sh/vdufknfreoljqp2/AAAZ6HYfAzySLaxbG3rAxMzJa?dl=0")
page_source = response.read()
page_source = page_source[page_source.find("<div class=\"sl-grid\""):]

link_blocks = page_source.split("<a ");
link_blocks = link_blocks[2:]

verbose = True # could modify this to False to remove console logs

for line in link_blocks:
	link = re.match(r'href=\"(.*?)\"', line, re.I)
	if link:
		link = link.group(1)[:-1] + "1"
		if verbose:
			print "link: ", link
	else:
		if verbose:
	   		print "No link!"

	name_regex = re.search(r'alt=\"(.*?)\"', line, re.I)
	full_name = ""
	if name_regex:
		tokens = name_regex.group(1).split("_")
		if tokens:
			if verbose:
				print "tokens", tokens
			full_name = ""
			for i in range(len(tokens)):
				full_name += tokens[i]
				if i < len(tokens) - 1:
					full_name += "_"
			if verbose:
				print "name: ", full_name
	else:
		if verbose:
			print "No name!"

	if (full_name and link):
		bash_command = 'curl -4 -L -o zip_files/' + full_name + '.zip ' + link
		if verbose:
			print bash_command
		os.system(bash_command) 


# NOTES + misc: 

# curl -L -o AARON_SCHOCK.zip https://www.dropbox.com/sh/z0jg216gx1l4omk/AABFc6T2ji2TJ0eBNiGqBXyza/AARON_SCHOCK_20914?dl=1
# curl -L -o test.zip https://www.dropbox.com/sh/z0jg216gx1l4omk/AAAHStGOd-W9xIWkbTyFlaq5a/ARTHUR_DAVIS_20302?dl=1
# import subprocess
# bash_com = 'curl -k -H "Authorization: Bearer xxxxxxxxxxxxxxxx" -H "hawkular-tenant: test" -X GET https://www.example.com/test | python -m json.tool'
# subprocess.Popen(bash_com)
# output = subprocess.check_output(['bash','-c', bash_com])