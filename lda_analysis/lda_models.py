#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: Aug 3, 2017
# [DESCRIPTION]

#https://www.umiacs.umd.edu/~jbg/docs/nips2009-rtl.pdf (word intrusion verification)

from gensim import corpora, models
import gensim
import os

# Set up log to external log file
import logging
logging.basicConfig(filename='lda_model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

generate = True
analyze = True
num_topics_low = 4
num_topics_high = 10

if generate == True:
	dictionary = corpora.Dictionary.load("governors_extra_filter.dict")
	print "dictionary loaded from memory"
	corpus = corpora.MmCorpus('governors_extra_filter.mm')
	print "corpus loaded from memory"

	for num_topics in range(num_topics_low, num_topics_high):
		print "running for num topics: ", num_topics
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20)
		ldamodel.save("results/" + str(num_topics) + "_" + "governors_lda_model_extra_filtered")
if analyze == True:
	for num_topics in range(num_topics_low, num_topics_high):
		print "================ " + str(num_topics) + " TOPICS ================"
		ldamodel = models.LdaModel.load("results/" + str(num_topics) + "_" + "governors_lda_model_extra_filtered")
		list_of_topics = ldamodel.print_topics(num_topics=-1, num_words=10)
		for topic in list_of_topics:
			print topic[1]
			print "\n"
		print "\n\n\n"


# corpus = [dictionary.doc2bow(text) for text in texts] //from preprocessing segment
# for each text, record which topic gets assigned to it

# lda_model.get_document_topics(bow, minimum_probability=None, minimum_phi_value=None, per_word_topics=False)
# Return topic distribution for the given document bow, as a list of (topic_id, topic_probability) 2-tuples.

# Ignore topics with very low probability (below minimum_probability).

# If per_word_topics is True, it also returns a list of topics, sorted in descending order of most likely topics for that word.

# record each title with its predicted cluster :(

# ===================

# also run naive filter for specific word approach to identifying topical speeches.

# ===================

# compare the frequencies per governor of topical speeches. if within some range (even though
	# i know im bad at actual stats), we say they are acceptable approximations

# ===================

# make line graph where the dot is larger for more topical speeches that month
