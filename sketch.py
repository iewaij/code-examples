# coding=UTF-8

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
	striped_text = striped_text.replace("：", "")
	striped_text = striped_text.replace("(", "")
	striped_text = striped_text.replace(")", "")
	striped_text = striped_text.replace("―", "")
	striped_text = striped_text.replace("　", "")

	# split words
	seg_list = striped_text.split()

input_list = seg_list[:900]
output_list = []
def combine_short (input):
	# a recursive function but only workable when input list is not too long
	global output_list
	if len(input) <= 1:
		pass
	else:
		output_list.append(input[0] + input[1])
		combine_short(input[1:])

combine_short(input_list)
for word in output_list:
	print (word)