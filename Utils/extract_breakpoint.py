def statistic_breakpoint(filepath, file_result, chr_num, chr_id):
	file_content = open(filepath, 'r+')
	left = '0'
	right = '0'

	breakpoints = []

	for row in file_content:
		each_col = row.split("\t")
		info = each_col[1].split("/")
		is_del = info[-1].split("_")
		if is_del[0] == 'del':
			if each_col[-4] == 'label 1':
				if(left=='0' and right=='0'):
					left = is_del[2]
					right = is_del[3].split('.')[0]
				else:
					l = is_del[2]
					r = is_del[3].split('.')[0]
					if(right != l):
						breakpoints.append(("chr"+chr_id, int(left), int(right)))
						left = l
						right = r 
					else:
						right = r
	breakpoints_result = sorted(breakpoints, key=lambda x:x[1])
	for each_point in breakpoints_result:
		file_result.write(each_point[0] + "\t" + str(each_point[1]) +"\t"+ str(each_point[2] + "\n")


def main():
	chrArray = ['NA18525', 'NA19017', 'NA19238', 'NA19239', 'NA19625', 'NA19648', 'NA20502', 'NA20845']
	chrID = ['1','2']
	for chr_num in chrArray:
		for chr_id in chrID:
			filepath = "e:\\PythonProject\\mySVfeature_2\\Multiple_Sample\\"+chr_num+"\\result\\"+chr_num+"_result_chr"+chr_id+".txt"
			file_result = open("e:\\PythonProject\\mySVfeature_2\\Multiple_Sample\\statistic_breakpoint\\"+chr_num+"_static_breakpoint_chr"+chr_id+".txt","w+")
			statistic_breakpoint(filepath, file_result, chr_num, chr_id)


if __name__ == '__main__':
	main()











