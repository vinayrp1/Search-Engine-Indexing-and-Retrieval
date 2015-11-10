#!/usr/bin/python

import sys
import math

k1 = 1.2
k2 = 100
b = 0.75
avdl = 0
total_tokenNo = 0
total_docs = 0

results = {}
inverted_list = {}
doc_len = {}

#####################################################################

# reads inverted index from index.out and populates the data into 
# a dictionary "inverted_list"
def populate_inverted_list(content):

	lines = content.split('\n')
	lines.remove('')
	for l in lines:
		split_lines = l.split('->')
		inverted_list[split_lines[0]] = []
		tf_arr = split_lines[1].split(' ')
		tf_arr.remove('')
		for t in tf_arr:
			doc_tup = t.split(',')
			doc_id = doc_tup[0][1:]
			tf = int(doc_tup[1][:-1])
			doc_tup = []
			doc_tup.append(doc_id)
			doc_tup.append(tf)
			inverted_list[split_lines[0]].append(doc_tup)

#####################################################################

# reads the doc length from index.out and populates the data into
# a dictionary "doc_len"
def populate_doc_len(content):

	global total_tokenNo 
	global total_docs
	global avdl
	lines = content.split('\n')
	lines.remove('')
	for l in lines:
		doc_info = l.split(':')
		doc_len[doc_info[0]] = int(doc_info[1])
		total_tokenNo += int(doc_info[1])
		total_docs += 1
	avdl = total_tokenNo/float(total_docs)

#####################################################################

# calculates the bm25 score of each document for the given query and 
# returns the same list as dictionary "scored_docs"
def populate_results(tokens):

	scored_docs = {}
	doc_list = get_union_doclist(tokens)
	qf = 1
	N = float(total_docs)
	for d in doc_list:
		total = 0
		K = float(getK_val(doc_len[d]))
		for t in tokens:
			ni = float(len(inverted_list[t]))
			fi = float(get_tf(d, t))
			if fi > 0: 
				prod = ((N - ni + 0.5) / (ni + 0.5)) * (((k1 + 1) * fi) / (K + fi)) * (((k2 + 1) * qf) / (k2 + qf))
				total += math.log(prod)
		if total != 0:
			scored_docs[d] = total	
	return scored_docs

#####################################################################

def getK_val(dl):

	return k1 * ((1 - b) + b * (dl / avdl))

def get_union_doclist(tokens):

	doc_list = []
	for t in tokens:
		lst = inverted_list[t]
		for tup in lst:
			if tup[0] not in doc_list:
				doc_list.append(tup[0])
	return doc_list

def get_tf(d, t):

	lst = inverted_list[t]
	for l in lst:
		if d == l[0]:
			return float(l[1])
	return 0		

#####################################################################

if __name__ == '__main__':

	index_filename = "index.out"
	query_file = "queries.txt"
	results_len = 100
	if len(sys.argv) > 1:
		index_filename = sys.argv[1]
	if len(sys.argv) > 2:
		query_file = sys.argv[2]
	if len(sys.argv) > 3:
		results_len = int(sys.argv[3])		
	index_file = open(index_filename, 'r')
	outfile_content = index_file.read()
	content = outfile_content.split('|')
	inverted_index_content = content[0]
	doc_len_content = content[1]
	populate_inverted_list(inverted_index_content)
	populate_doc_len(doc_len_content)
	queries_content = open(query_file, 'r')
	queries = queries_content.read().split('\n')
	if '' in queries:
		queries.remove('')
	for q in queries:
		query_tokens = q.split(' ')
		if '' in query_tokens:
			query_tokens.remove('')
		results[q] = populate_results(query_tokens)
	j = 1
	for q in queries:
		i = 0
		for docId, score in sorted(results[q].items(), key=lambda (k, v): v, reverse=True):
			i += 1
			if i > results_len:
				j += 1
				break
			print str(j) + ' Q0 ' + str(docId) + ' ' + str(i) + ' ' + str(score) + ' ' + 'vinayrp'