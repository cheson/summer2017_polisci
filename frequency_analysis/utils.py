import os, string, re

def get_date(dateline, granularity):
	month_translation = {"jan":"01", "feb":"02", "march":"03", "april":"04", "may":"05", \
	"june":"06", "july":"07", "aug":"08", "sept":"09", "oct":"10", \
	"nov":"11", "dec":"12"} 

	date = dateline.replace(".", "") # Date: 
	date = date.split(",")
	year = date[1].replace(" ", "")
	month_day = date[0].split(" ")
	month = month_day[0]
	day = month_day[1]
	if len(day) == 1:
		day = "0" + day
	#YYYY-MM-DD
	if granularity.lower() == 'day':
		date = year + "-" + month_translation[month] + "-" + day
	#YYYY-MM
	if granularity.lower() == 'month':
		date = year + "-" + month_translation[month]
	#YYYY
	if granularity.lower() == 'year':
		date = year
	return date

# documents are each (author, date, body) tuples
def get_documents(src):
	documents = []
	directories = [os.path.join(src,o) for o in os.listdir(src) if os.path.isdir(os.path.join(src,o))]
	counter = 0
	all_names = []

	for directory in directories:
		all_names.append(directory.replace(src, "").replace("_", " "))
		for speech in os.listdir(directory):
			speech = directory + '/' + speech
			with open(speech, 'r') as f:
				counter += 1
				sections = f.read().split("\n\n")
				metadatas = sections[0].split("\n")
				for md in metadatas:
					if "By: " in md:
						author = md.replace("By: ", "").lower()
					if "Date: " in md:
						date = md.replace("Date: ", "").lower()
				# title = metadata[1]
				# if len(metadata) == 6:
				# 	location = metadata[5]
				body = sections[1].translate(None, string.punctuation)
				body = body.replace("\n", " ")
				if len(sections) == 3:
					source = sections[2]
				documents.append((author, date, body.lower().decode('utf-8')))
			f.close()
	print counter, "documents created from speeches"
	return documents, sorted(all_names)