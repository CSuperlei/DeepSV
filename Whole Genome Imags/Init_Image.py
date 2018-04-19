# generate pileup sequence
def pipeup_column(sam_file,chr_id,pos_l,pos_r):
	pile_record=[]
	for pileupcolumn in sam_file.pileup(chr_id, pos_l, pos_r):
		if(pileupcolumn.pos>=pos_l and pileupcolumn.pos <= pos_r):
			for pileupread in pileupcolumn.pileups:
				if None != pileupread.alignment.cigarstring and None != pileupread.query_position:
					index = 0
					map_type = -1
					for cigar in pileupread.alignment.cigartuples:
						if (pileupread.query_position > index):
							index = cigar[1] + index
							map_type = cigar[0]

					pile_result = (pileupcolumn.pos,pileupread.alignment.is_paired,pileupread.alignment.is_proper_pair,pileupread.alignment.mapping_quality,map_type,pileupread.alignment.query_sequence[pileupread.query_position])
					pile_record.append(pile_result)

	print("pilelen is %d"%len(pile_record))
	return pile_record

# init image
def init_pic(row,col,th,fig, flag):
	if flag=='2d':
		ax = fig.add_subplot(row, col, th)
		ax.get_xaxis().get_major_formatter().set_useOffset(False)
		return ax
	elif flag == '3d':
		ax = fig.add_subplot(row, col, th, projection='3d')
		ax.get_xaxis().get_major_formatter().set_useOffset(False)
		return ax


# generate colors
def get_rgb(clip_value,every_pile_record):
	if every_pile_record[5] == 'A':

		# Red
		base_A = [255,0,0]  
		if every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_A = [255,0,0]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_A = [255,60,60]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_A = [255,70,70]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_A = [255,80,80]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_A = [255,90,90]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_A = [255,100,100]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_A = [255,110,110]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_A = [255,120,120]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_A = [255,130,130]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_A = [255,140,140]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_A = [255,150,150]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_A = [255,160,160]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_A = [255,170,170]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_A = [255,180,180]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_A = [255,190,190]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_A = [255,200,200]

		base_A[1] = base_A[1] + clip_value
		base_A[2] = base_A[2] + clip_value
		base_A = tuple(base_A)
		return base_A

	elif every_pile_record[5] == 'T':
		#green
		base_T = [0,255,0]  
		if every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_T = [0,255,0]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_T = [60,255,60]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_T = [70,255,70]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_T = [80,255,80]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_T = [90,255,90]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_T = [100,255,100]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_T = [110,255,110]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_T = [120,255,120]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_T = [130,255,130]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_T = [140,255,140]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_T = [150,255,150]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_T = [160,255,160]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_T = [170,255,170]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_T = [180,255,180]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_T = [190,255,190]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_T = [200,255,200]

		base_T[0] = base_T[0] + clip_value
		base_T[2] = base_T[2] + clip_value
		base_T = tuple(base_T)
		return base_T

	elif every_pile_record[5]  == 'C':
		#blue
		base_C = [0,0,255] 
		if every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_C = [0,0,255]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_C = [60,60,255]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_C = [70,70,255]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_C = [80,80,255]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_C = [90,90,255]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_C = [100,100,255]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_C = [110,110,255]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_C = [120,120,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_C = [130,130,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_C = [140,140,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_C = [150,150,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_C = [160,160,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_C = [170,170,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_C = [180,180,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_C = [190,190,255]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_C = [200,200,255]

		base_C[0] = base_C[0] + clip_value
		base_C[1] = base_C[1] + clip_value
		base_C = tuple(base_C)
		return base_C

	elif every_pile_record[5]  == 'G':
		#black
		base_G = [0,0,0]  
		if every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_G = [0,0,0]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_G = [60,60,60]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_G = [70,70,70]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_G = [80,80,80]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_G = [90,90,90]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_G = [100,100,100]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_G = [110,110,110]
		elif every_pile_record[1] == 'True' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_G = [120,120,120]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_G = [130,130,130]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_G = [140,140,140]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_G = [150,150,150]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'True' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_G = [160,160,160]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] != 4:
			base_G = [170,170,170]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] >= 20 and every_pile_record[4] == 4:
			base_G = [180,180,180]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] != 4:
			base_G = [190,190,190]
		elif every_pile_record[1] == 'False' and every_pile_record[2] == 'False' and every_pile_record[3] < 20 and every_pile_record[4] == 4:
			base_G = [200,200,200]

		base_G = np.array(base_G)
		base_G = base_G + clip_value
		base_G = tuple(base_G)
		return base_G