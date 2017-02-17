# coding=UTF-8
from collections import Counter

with open("happiness_seg.txt", "rt") as textfile:
	# open and read file
	text =  textfile.read()

	# delete punctuation marks
	striped_text = text.replace("，", "")
	striped_text = striped_text.replace("。", "")
	striped_text = striped_text.replace("“", "")
	striped_text = striped_text.replace("”", "")
	striped_text = striped_text.replace("?", "")
	striped_text = striped_text.replace("；", "")
	striped_text = striped_text.replace(":", "")
	striped_text = striped_text.replace("(", "")
	striped_text = striped_text.replace(")", "")
	striped_text = striped_text.replace("―", "")

	# split words
	seg_list = striped_text.split()

output_list = []
def combine_short (input):
	# a recursive function but only workable when input list is not too long
	global output_input
	if len(input) <= 1:
		pass
	else:
		output_input.append(input[0] + input[1])
		combine(input[1:])


def combine_long (input):
	# combine two words into a list
	empty = []
	for n in range(len(input)-1):
		empty.append(input[n] + " " + input[n+1])
	return empty

word_counts = Counter(combine_long(seg_list))
# use class in collections.Counter
top_ten = word_counts.most_common(10)

for word in top_ten:
	print "词组：「%s」 频率：%d" % (word[0], word[1])