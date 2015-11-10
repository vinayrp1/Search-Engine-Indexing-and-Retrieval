#!/usr/bin/python

import sys

inverted_list = {}
doc_len = {}

#################################################################################

class TermFrequency:
	'This class holds document ID and term freuency associated with the query'

	def __init__(self, docID, tf):

		self.docID = docID
		self.tf = tf

#################################################################################

def tokenize(doc):

	inv_single_doc = {}
	doc_lines = doc.split('\n')
	doc_id = doc_lines[0]
	doc_len[doc_id] = 0	
	for line in doc_lines:
		tokens = line.split(' ')
		if '' in tokens:
			tokens.remove('')
		for t in tokens:
			try:
   				val = int(t)
			except ValueError:   				
   				if not inv_single_doc.has_key(t):
   					inv_single_doc[t] = 1
   				else:
   					inv_single_doc[t] += 1
   				doc_len[doc_id] += 1
	return doc_id, inv_single_doc

def add_to_inverted_list(info):

	doc_id = info[0]
	dic = info[1]
	dlist = []
	for key, value in dic.iteritems():
		if not inverted_list.has_key(key):
			dlist = []
			dlist.append(TermFrequency(doc_id, value))
			inverted_list[key] = dlist
		else:	
			inverted_list[key].append(TermFrequency(doc_id, value))	
	return

#################################################################################

if __name__ == '__main__':

	corpus_name = "tccorpus.txt"
	index_filename = "index.out"
	if len(sys.argv) > 1:
		corpus_name = sys.argv[1]
	if len(sys.argv) > 2:
		index_filename = sys.argv[2]
	index_file = open(index_filename, 'wb')
	corpus = open(corpus_name, 'r')
	doc_list = corpus.read().split('# ')
	if '' in doc_list:
		doc_list.remove('')
	for d in doc_list:
		add_to_inverted_list(tokenize(d))
	for k, v in inverted_list.iteritems():
		index_file.write(k + "->")
		for tf in v:
			index_file.write('(' + tf.docID + ',' + str(tf.tf) +') ')
		index_file.write('\n')
	index_file.write('|')
	for k,v in doc_len.iteritems():
		index_file.write(k + ':' + str(v) + '\n')