import pysam
from pysam import VariantFile
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from K_Means_Cluster_Source.k_means import *
from PIL import Image
from PIL import ImageDraw
from BAM_CLASS import BAM
from VCF_CLASS import VCF
from FILE_CLASS import FILE
from Features import *
from Init_Image import *
from Candidate_Image import *


# draw deletion image
def draw_del_pic(vcf_del,sam_file,del_name):
	print(vcf_del[0][0])
	chr_id = vcf_del[0][0]
	del_pos = call_del(vcf_del,sam_file,del_name)
	num_del_pos = len(del_pos)
	del_pos_np = np.array(del_pos)
	print("num_del_pos %d"%num_del_pos)
	for i in range(num_del_pos):
		print(chr_id)
		clip_record = get_clip_num(sam_file,chr_id, del_pos_np[i,0], del_pos_np[i,1])
		clip_dict_record = dict(clip_record)
		print(clip_dict_record)

		gene_pic = gene_point_pic(chr_id, del_pos_np[i,0], del_pos_np[i,1])

		for each_pic in gene_pic:
			pile_record = pipeup_column(sam_file,each_pic[0], each_pic[1],each_pic[2])
			deletion_length =  each_pic[2] - each_pic[1]
			draw_pic(clip_dict_record, pile_record, each_pic[1], deletion_length)


def main():
	file = File()
	vcf_path = "your file path"
	vcf_file = file.get_vcf_file(vcf_path,'deletion')   
		print("vcf_file is []")
		return
	
	bam_path = "your file path"
	sam_file = file.get_sam_file(bam_path)
	vcf = VCF(vcf_file)
	vcf.vcf_class()  
	# --del_length: del_50_200 del_200_700 del_700_1000 del_1000 ...
	parser.add_argument("--del_length", required=True)
	args = parser.parse_args()

	if (args.del_length == "del_50_200"):
		if vcf.del_50_200 !=[]:
			draw_del_pic(vcf.del_50_200,sam_file, del_len=args.del_length)
	elif (args.del_length == "del_200_700"):
		if vcf.del_200_700 !=[]:
			draw_del_pic(vcf.del_200_700,sam_file, del_len=args.del_length)
	elif (args.del_length == "del_700_1000"):
		if vcf.del_700_1000 !=[]:
			draw_del_pic(vcf.del_700_1000,sam_file, del_len=args.del_length)
	elif (args.del_length == "del_1000"):
		if vcf.del_1000 !=[]:
			draw_del_pic(vcf.del_1000,sam_file, del_len=args.del_length)
	


if __name__ == '__main__':
	main()







