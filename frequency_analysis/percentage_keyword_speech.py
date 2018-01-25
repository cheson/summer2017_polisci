#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: August 15, 2017
# [DESCRIPTION]

import os, string, re, csv
import pandas as pd 
import numpy as np
from collections import defaultdict, Counter
from utils import get_documents, get_date

############### INPUTS ###############
# data source for get_documents() function
src = '../votesmart_scraper/outputs/current_governors/'
# keywords to search for, separated by commas. eg. ['energy', 'oil fields', 'fracking']
keywords = ['energy', 'oil fields', 'fracking']
# "day", "month" or "year" granularity for the counts
granularity = "month" 
# output path 
output = "./outputs/demo.csv"
################# END #################

def main():
	documents, all_names = get_documents(src)
	total_speeches, keyword_speeches, all_dates = count_speeches(documents, all_names)
	generate_csv(total_speeches, keyword_speeches, all_dates, all_names)

def count_speeches(documents, all_names):
	month_translation = {"jan":"01", "feb":"02", "march":"03", "april":"04", "may":"05", \
	"june":"06", "july":"07", "aug":"08", "sept":"09", "oct":"10", \
	"nov":"11", "dec":"12"} 

	total_speeches = defaultdict(int)
	keyword_speeches = defaultdict(int)
	all_dates = []

	for document in documents:
		name = document[0] # By:
		date = get_date(document[1], granularity) # Date:
		all_dates.append(date)

		body = document[2]
		for gov in all_names:
			if gov in name: #often times there are multiple authors listed
				total_speeches[(date, gov)] += 1
				for keyword in keywords:
					if keyword in body:
						keyword_speeches[(date, gov)] += 1
						break #if any of keywords found, break

	all_dates = sorted(list(set(all_dates)))
	# print "dates", all_dates
	return total_speeches, keyword_speeches, all_dates

def output_shiran_csv_format(raw_data, all_names, all_dates):
	# hard coded for now, you would have to make your own for other candidates
	state_map = {"alabama": "kay ivey", "alaska": "bill walker", "arizona": "doug ducey", "arkansas": "asa hutchinson", "california": "jerry brown", "colorado": "john hickenlooper", "connecticut": "dannel malloy", "delaware": "john carney", "florida": "rick scott", "georgia": "nathan deal", "hawaii": "david ige", "idaho": "butch otter", "illinois": "bruce rauner", "indiana": "eric holcomb", "iowa": "kim reynolds", "kansas": "sam brownback", "kentucky": "matt bevin", "louisiana": "john bel edwards", "maine": "paul lepage", "maryland": "larry hogan", "massachusetts": "charlie baker", "michigan": "rick snyder", "minnesota": "mark dayton", "mississippi": "phil bryant", "missouri": "eric greitens", "montana": "steve bullock", "nebraska": "pete ricketts", "nevada": "brian sandoval", "new hampshire": "chris sununu", "new jersey": "chris christie", "new mexico": "susana martinez", "new york": "andrew cuomo", "north carolina": "roy cooper", "north dakota": "doug burgum", "ohio": "john kasich", "oklahoma": "mary fallin", "oregon": "kate brown", "pennsylvania": "tom wolf", "rhode island": "gina raimondo", "south carolina": "henry mcmaster", "south dakota": "dennis daugaard", "tennessee": "bill haslam", "texas": "greg abbott", "utah": "gary herbert", "vermont": "phil scott", "virginia": "terry mcauliffe", "washington": "jay inslee", "west virginia": "jim justice", "wisconsin": "scott walker", "wyoming": "matt mead"}
	slash_index = output.rfind("/")
	shiran_output = output[:slash_index+1] + "shiran_" + output[slash_index+1:]

	with open(shiran_output, 'w') as csvfile:
	    fieldnames = ['NAME', 'STATE', 'DATE', 'PROPORTION']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for name in all_names:
	    	proportions = raw_data[name]
	    	counter = 0
	    	state = ""
	    	for state_curr in state_map:
	    		if state_map[state_curr] == name:
	    			state = state_curr
	    	for date in all_dates:
	    		proportion = proportions[counter]
	    		writer.writerow({'NAME': name, 'STATE' : state, 'DATE' : date, 'PROPORTION' : proportion})
	    		counter += 1


def generate_csv(total_speeches, keyword_speeches, all_dates, all_names):
	raw_data = {"Date":all_dates}
	raw_total_counts = defaultdict(int)
	raw_keyword_counts = defaultdict(int)
	raw_republican_total_counts = defaultdict(int)
	raw_republican_keyword_counts = defaultdict(int)
	raw_democratic_total_counts = defaultdict(int)
	raw_democratic_keyword_counts = defaultdict(int)
	# hard coded for now, you would have to make your own for other candidates
	party_map = {"kay ivey": "republican", "bill walker": "independent", "doug ducey": "republican", "asa hutchinson": "republican", "jerry brown": "democratic", "john hickenlooper": "democratic", "dannel malloy": "democratic", "john carney": "democratic", "rick scott": "republican", "nathan deal": "republican", "david ige": "democratic", "butch otter": "republican", "bruce rauner": "republican", "eric holcomb": "republican", "kim reynolds": "republican", "sam brownback": "republican", "matt bevin": "republican", "john bel edwards": "democratic", "paul lepage": "republican", "larry hogan": "republican", "charlie baker": "republican", "rick snyder": "republican", "mark dayton": "democratic", "phil bryant": "republican", "eric greitens": "republican", "steve bullock": "democratic", "pete ricketts": "republican", "brian sandoval": "republican", "chris sununu": "republican", "chris christie": "republican", "susana martinez": "republican", "andrew cuomo": "democratic", "roy cooper": "democratic", "doug burgum": "republican", "john kasich": "republican", "mary fallin": "republican", "kate brown": "democratic", "tom wolf": "democratic", "gina raimondo": "democratic", "henry mcmaster": "republican", "dennis daugaard": "republican", "bill haslam": "republican", "greg abbott": "republican", "gary herbert": "republican", "phil scott": "republican", "terry mcauliffe": "democratic", "jay inslee": "democratic", "jim justice": "democratic", "scott walker": "republican", "matt mead": "republican"}
	for name in all_names:
		counts = []
		raw_counts = []
		curr_date = ""
		for date in all_dates:
			curr_date = date
			if total_speeches[(date, name)] == 0:
				counts.append(0)
				raw_counts.append("raw count: 0")
			else:
				num = float(keyword_speeches[(date, name)])
				denom = float(total_speeches[(date, name)])
				counts.append(num/denom) 
				raw_counts.append("raw count: " + str(keyword_speeches[(date,name)]))
				raw_total_counts[date] += total_speeches[(date, name)]
				raw_keyword_counts[date] += keyword_speeches[(date, name)]
				if party_map.get(name) == "republican":
					raw_republican_total_counts[date] += total_speeches[(date, name)]
					raw_republican_keyword_counts[date] += keyword_speeches[(date, name)]
				if party_map.get(name) == "democratic":
					raw_democratic_total_counts[date] += total_speeches[(date, name)]
					raw_democratic_keyword_counts[date] += keyword_speeches[(date, name)]
		raw_data[name] = counts
		raw_data["raw_" + name] = raw_counts
	
	overall_trend = []
	overall_raw_counts = []
	republican_trend = []
	republican_raw_counts = []
	democratic_trend = []
	democratic_raw_counts = []

	for date in all_dates:
		if raw_total_counts[date] == 0:
			overall_trend.append(0)
			overall_raw_counts.append("raw count: 0")
		else:
			overall_trend.append(float(raw_keyword_counts[date]) / float(raw_total_counts[date]))
			overall_raw_counts.append("raw count: " + str(raw_keyword_counts[date]))
		if raw_democratic_total_counts[date] == 0:
			democratic_trend.append(0)
			democratic_raw_counts.append("raw count: 0")
		else:
			democratic_trend.append(float(raw_democratic_keyword_counts[date]) / float(raw_democratic_total_counts[date]))
			democratic_raw_counts.append("raw count: " + str(raw_democratic_keyword_counts[date]))	
		if raw_republican_total_counts[date] == 0:
			republican_trend.append(0)
			republican_raw_counts.append("raw count: 0")
		else:
			republican_trend.append(float(raw_republican_keyword_counts[date]) / float(raw_republican_total_counts[date]))
			republican_raw_counts.append("raw count: " + str(raw_republican_keyword_counts[date]))	
	
	raw_data["overall_trend"] = overall_trend
	raw_data["raw_overall_trend"] = overall_raw_counts
	raw_data["democratic_trend"] = democratic_trend
	raw_data["raw_democratic_trend"] = democratic_raw_counts
	raw_data["republican_trend"] = republican_trend
	raw_data["raw_republican_trend"] = republican_raw_counts
	
	raw_names = ["raw_" + name for name in all_names]
	columns = ["Date", "overall_trend", "democratic_trend", "republican_trend"] + all_names + ["raw_overall_trend", "raw_democratic_trend", "raw_republican_trend"] + raw_names
	df = pd.DataFrame(raw_data, columns = columns)
	df.to_csv(output)

	output_shiran_csv_format(raw_data, all_names, all_dates)

# MAIN FUNCTION CALL
main()

# EXAMPLE PANDA DATAFRAME CREATION
# ---------------------------------
# raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
#         'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
#         'age': [42, 52, 36, 24, 73],
#         'preTestScore': [4, 24, 31, ".", "."],
#         'postTestScore': ["25,000", "94,000", 57, 62, 70]}
# df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])

