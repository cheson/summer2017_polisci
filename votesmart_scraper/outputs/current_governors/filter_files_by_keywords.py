#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: July 24, 2017
# This script takes the directory with files to filter, a set of words to filter,
# and a directory where filtered files will be stored. 
# The purpose is to search through all the files and save only those that contain
# the target words. 

# Example usage:
# python filter_files_by_keywords.py -fd [filedir] -rd [resultsdir] -tw targetword1 targetword2 ...
# python filter_files_by_keywords.py -tw targetword1 targetword2 ...

# After running, check out the results folder as well as the RESULTS_SUMMARY.txt

import os, sys, shutil
from argparse import ArgumentParser
from sys import version_info
from collections import defaultdict, Counter
from utils import get_date
import json

py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2

parser = ArgumentParser(description="File filtering")

parser.add_argument('--files-dir', '-fd',
                    type=str,
                    help='Directory containing files to filter.',
		    		default='.')

parser.add_argument('--results-dir', '-rd',
                    type=str,
                    help='Directory where results will be stored.',
                    default="filtered_results")

parser.add_argument('--target-words', '-tw',
					nargs='+',
					help='Words to search for in files.',
					required=True)

args = parser.parse_args()
results_dir = args.results_dir

target_author = "jerry brown"
target_date = "2016-01-11"

def directory_check(results_dir):
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
	print "results dir: " + results_dir 

directory_check(results_dir)

# file-word-count map
all_file_counts = {}

for filename in os.listdir(args.files_dir):
	print filename
	if (os.path.isdir(filename)):
		if (filename is not results_dir):
			print filename + " is directory"
	else: 
		file = open(filename, "r")
		all_words = file.read()
		sections = all_words.split("\n\n")
		metadatas = sections[0].split("\n")
		author = ""
		date = ""
		for md in metadatas:
			print "md", md
			if "By: " in md:
				author = md.replace("By: ", "").lower()
			if "Date: " in md:
				print md.replace("Date: ", "").lower()
				date = get_date(md.replace("Date: ", "").lower(), 'month')
				print "date: ", date
		found = False
		file_count = defaultdict(int)
		for target_word in args.target_words:
			if target_word in all_words:
				word_counts = Counter(all_words.split())
				file_count[target_word] += word_counts[target_word]
				found = True
		# print "target_date", target_date
		# print "date", date
		# print "author", author
		if author != target_author.lower() or date != target_date:
			found = False
		if found:
			print target_word + " found in " + filename
			destination = "./" + results_dir
			shutil.copy2(filename, destination)
			all_file_counts[filename] = file_count;
		file.close()

result_file = open(results_dir + "/RESULTS_SUMMARY.txt","w")

result_file.write("target words: ")
for word in args.target_words:
  result_file.write("%s " % word)  
result_file.write("\n\n")

for key in all_file_counts:
	result_file.write(key + " : " + json.dumps(all_file_counts[key]) + "\n")
result_file.write("\n\n")

result_file.write("json format: " + json.dumps(all_file_counts))

result_file.close() 



