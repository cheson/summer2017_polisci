#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: Aug 3, 2017
# Given a list of documents to run LDA, the preprocessing file 
# is responsible for stemming (here we use a Porter stemmer), removing
# stop words, and filtering out words with low frequency. 
# Then, a word to index mapping Dictionary is generated. Based on the 
# indices assigned to words, a bag of words corpus is also generated 
# where each document is represented as a list of the words it contains
# along with their frequency. 

# READING RESOURCES:
# https://radimrehurek.com/gensim/tut1.html
# http://radimrehurek.com/topic_modeling_tutorial/2%20-%20Topic%20Modeling.html
# https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html

from stop_words import get_stop_words #pip install stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from collections import defaultdict
import os

documents = []

d = '../votesmart_scraper/outputs/current_governors'
directories = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

# this specifically traverses the current_governors folder, but what
# is important is just filling the documents list with the appropriate
# body text
counter = 0
for directory in directories:
	for speech in os.listdir(directory):
		speech = directory + '/' + speech
		with open(speech, 'r') as f:
			counter += 1
			sections = f.read().split("\n\n")
			metadata = sections[0]
			body = sections[1]
			print body
			if len(sections) == 3:
				source = sections[2]
			documents.append(body.decode('utf-8'))

		f.close()
print counter, "documents created from speeches"

# Get English stoplist 
stoplist = get_stop_words('en')
# consider adding proper nouns / governor names to stop words

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# TODO: could convert to list comprehension to increase efficiency
# texts = [[word for word in document.lower().split() if word not in stoplist] \
# 		for document in documents]

counter = 0
texts = []
for document in documents: 
	tokens = []
	counter += 1
	if counter % 1000 == 0:
		print counter, "documents stemmed"
	for word in document.lower().split():
		if word not in stoplist:
			tokens.append(p_stemmer.stem(word))
	texts.append(tokens)
print "stemmed and lowered"

frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1
print "frequency counted"

minFrequency = 2 # tokens with frequency < minFrequency are cut
texts = [[token for token in text if frequency[token] >= minFrequency] \
		for text in texts]
print "words with frequency < " + str(minFrequency) + " removed"

dictionary = corpora.Dictionary(texts)

# consider filtering with the following function: 
dictionary.filter_extremes(no_below=20, no_above=0.1)
# https://radimrehurek.com/gensim/corpora/dictionary.html

dictionary.save('governors_extra_filter.dict')  # store the dictionary, for future reference
print "dictionary created and saved"

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('governors_extra_filter.mm', corpus)  # store to disk, for later use
print "corpus created and saved"

# NOTES #
# plan:
# group all the speeches into two folders, where each txt file 
# is just the text of the speeches and nothing else
# name, data, source, metadata associated with id. 
# governor speeches: name_date_id.txt
# senator speeches: name_date_id.txt

# source: https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
# come up with intuitive lda explanation 

# use naive word filtering to identify environmental policy speeches
# use lda clustering + automatic cluster environmental policy to determine speeches

# use lda to generate key words? 

# then given the filtered set of speeches
# how do we actually determine stance?

# clarify stance detection vs sentiment analysis
# sentiment analysis: strip out all sentences with certain keywords
# run sentiment analysis on that and take an average 
# not a really good approximation because regardless of stance you can speak 
# with positive or negative sentiment depending on whether you are 
# supporting your own position or attacking other positions

# :( 

# http://alt.qcri.org/semeval2016/task6/
# http://www.cs.cornell.edu/people/pabo/papers/emnlp06_convote.pdf *****
# http://www.cs.cornell.edu/home/llee/papers/tpl-convote.dec06.pdf
# https://www.govtrack.us/congress/members for congressional data

# llee@cs.cornell.edu
# justin grimmer
# email them both today.

# take from preprocessing:
# 	for each document:
# 		create bow models
# 		ldamodel.topic(bow)
# 		make map from string of bow title to topic 

#http://sappingattention.blogspot.com/2013/04/how-not-to-topic-model-introduction-for.html

# Lillian Lee:
# Each debate consists of a series of speech segments,
# where each segment is a sequence of uninterrupted
# utterances by a single speaker. Since
# speech segments represent natural discourse units,
# we treat them as the basic unit to be classified.
# Each speech segment was labeled by the vote
# (“yea” or “nay”) cast for the proposed bill by the
# person who uttered the speech segment

# we can use some seeding technique to get the set of words we use to define 
# an environmental speech. so we start with [environment, climate]
# of all the speeches that contain these two words, what other words frequently occur
# remove the stop words and keep the remaining ones, perhaps this could be done by
# just having a high and low threshold, although thats just an approximate way to solve
# this problem. 
