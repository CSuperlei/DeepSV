import os

'''

1、
os.path.abspath("文件名")：
2、
os.path.dirname("文件名"):

'''


def getFile(file_path, f1, f2):
	files = os.listdir(file_path)
	for fi in files:
		fi_sub = os.path.join(file_path, fi)
		if os.path.isdir(fi_sub):
			getFile(fi_sub, f1, f2)
		else:
			# print(fi_sub)
			print(fi_sub.split('/')[-2].split('_')[-3])
			if(fi_sub.split('/')[-2].split('_')[-3] == "chr1"):
				f1.write(os.path.abspath(fi_sub) + "\n")
			elif(fi_sub.split('/')[-2].split('_')[-3] == "chr2"):
				f2.write(os.path.abspath(fi_sub) + "\n")

def main():
	f1 = open("your file path", "w+")
	f2 = open("your file path", "w+")

	
	file_path = "./gene_pic"

	
	getFile(file_path, f1, f2)
	f1.flush()
	f1.close()
	f2.flush()
	f2.close()


if __name__ == '__main__':
	main()

