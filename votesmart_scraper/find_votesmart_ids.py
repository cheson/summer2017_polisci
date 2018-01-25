#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: July 31, 2017
# The find_votesmart_id function takes a list of targets with each target
# structured as the format "firstname_lastname". 
# If you call this function, you will get in return a map from the target
# name to the votesmart id associated with that target. If the target is 
# not found, a message is outputted. You can also choose to have the function
# return a tuple that contains the list of unfound targets. 

import csv

def find_votesmart_ids(target_list = None):
	### CREATE MAP OF VOTESMART PEOPLE TO THEIR DATABASE IDS ###
	id_matrix = 'inputs/votesmart_id_matrix.csv'
	id_map_all = {}

	if target_list == None:
		return []

	with open(id_matrix, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		next(csvfile)
		for row in reader:
			entry = row[0]
			columns = entry.split(";")
			# print columns
			if len(columns) == 12: 
				politician_id = columns[0]
				first_name = columns[5].lower().replace("\"", "")
				last_name = columns[8].lower().replace("\"", "")
				full_name = first_name + "_" + last_name
				id_map_all[full_name] = int(politician_id)
		csvfile.close()
	# print id_map_all

	### FIND IDS OF TARGETS ### 
	all_names = id_map_all.keys()
	targets_found = {}
	targets_not_found = []

	for target in target_list:
		if target in all_names:
			targets_found[target] = id_map_all[target]
		else:
			print target + " not in votesmart database [please double check manually]"
			targets_not_found.append(target)

	# print targets_found
	# print len(targets_found)
	print len(targets_found), "found |", len(targets_not_found), "not found"
	return targets_found
	#return (targets_found, targets_not_found)

