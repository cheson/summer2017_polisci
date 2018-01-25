#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: July 31, 2017
# Helper functions to be used in the scraper responsible for parsing out the
# governors names in FIRSTNAME_LASTNAME format from two different files:
# a) current_us_governors.csv b) old_us_governors.txt

import os
import csv

def parse_current_governors():
	target_file = 'inputs/current_us_governors.csv'
	processed_names = {}
	with open(target_file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		next(csvfile)
		for row in reader:
			state = row[0]
			target = row[1].lower().split()
			first_name = target[0]
			last_name = target[len(target)-1] #ignore middle names
			search_term = first_name + "_" + last_name
			processed_names[search_term] = 1
		csvfile.close()
	print len(processed_names.keys()), "governors in list"
	return processed_names.keys()

def parse_old_governors():
	governors_file = "inputs/old_us_governors.txt"
	with open(governors_file, 'rb') as f:
		next(f)
		processed_names = {}
		for line in f:
			# file structure test
			# if len(tokens) != 2:
			# 	print "rogue tokens!", tokens
			
			tokens = line.split("\t")

			name = tokens[0]
			year_in_office = tokens[1].strip()

			tokens = name.split(",")

			if len(tokens) == 2:
				last_name = tokens[0].split()
				first_name = tokens[1].split()
				processed_names[first_name[0].lower() + "_" + last_name[0].lower()] = 1
			else:
				continue

		f.close()
	print len(processed_names.keys()), "governors in list"
	return processed_names.keys()
