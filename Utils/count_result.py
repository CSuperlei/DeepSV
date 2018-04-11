import numpy as np
import pandas as pd
def count_0(filepath):
	file_content = open(filepath,'r+')
	count = 0
	label_0 = 0
	for row in file_content:
		each_col = row.split('\t')
		count += 1
		if each_col[-4] == 'label 0':
			label_0 += 1

	print("total_0 is %d "%count)
	print("correct judge is %d"%label_0)
	print("correct rate %.3f%%"%(label_0/count*100))
	return count, label_0


def count_1(filepath):
	file_content = open(filepath,'r+')
	count = 0
	label_1 = 0
	for row in file_content:
		each_col = row.split('\t')
		count += 1
		if each_col[-4] == 'label 1':
			label_1 += 1
	
	print("total_1 is %d "%count)
	print("correct judge is %d"%label_1)
	print("correct rate %.3f%%"%(label_1/count*100))
	return count, label_1

def count(filepath, file_result, chr_num, chr_id):
	file_content = open(filepath,'r+')
	count = 0
	count_0 = 0
	count_1 = 0
	label_0 = 0
	label_1 = 0

	for row in file_content:
		each_col = row.split('\t')
		isdel = each_col[1].split('/')
		is_del = isdel[-1].split('_')
		count += 1
		if is_del[0] == 'un':
			count_0 += 1
			if each_col[-4] == 'label 0':
				label_0 += 1
		elif is_del[0] == 'del':
			count_1 += 1
			if each_col[-4] == 'label 1':
				label_1 += 1


	file_result.write("statistic "+chr_num+" individuals "+chr_id+"\n")
	file_result.write("*"*25 + "\n")
	file_result.write("all in images %d "%count + "\n")
	file_result.write('*'*25 + "\n")
	file_result.write("0 images %d "%count_0 + "\n")
	file_result.write("right 0 imags %d "%label_0 + "\n")
	file_result.write('*'*25 + "\n")
	file_result.write("1 images %d "%count_1 + "\n")
	file_result.write("right images %d "%label_1 + "\n")
	file_result.write("*"*25 + "\n")


def main():
	chrArray = ['NA18525', 'NA19017', ...] #individuals
	chrID = ['1','2',...] # chromosome
	for chr_num in chrArray:
		for chr_id in chrID:
			filepath = "your file path"+chr_num+"\\result\\"+chr_num+"_result_chr"+chr_id+".txt"
			file_result = open("your file path"+chr_num+"_static_res_chr"+chr_id+".txt","w+")
			count(filepath, file_result, chr_num, chr_id)

if __name__ == '__main__':
	main()
