#statistic feature numbers
def get_clip_num(sam_file,chr_id, pos_l, pos_r):
	clip_temp = []
	for read in sam_file.fetch(chr_id, pos_l, pos_r):
		if None != read.cigarstring:
			base_pos = read.get_reference_positions(True)
			read_len = len(read.get_reference_positions(True))
			index=0
			for read_map_pos in range(read_len):
				if base_pos[read_map_pos]!=None:
					break
				else:
					index += 1
			read_start = read.reference_start-index
			read_end = read_start+read_len-1

			for i in range(pos_r-pos_l+1):
				if pos_l+i<=read_end and pos_l+i >= read_start:
					index_ptr=0
					map_type = -1
					for cigar in read.cigartuples:
						if(pos_l+i>index_ptr):
							index_ptr = cigar[1]+index_ptr
							map_type=cigar[0]
					clip_temp.append((pos_l+i,-map_type))

	clip_record_np = np.array(clip_temp)				
	df = pd.DataFrame(clip_record_np)
	clip_record_df = df.groupby(0).sum()
	clip_record_df = clip_record_df//4
	temp = clip_record_df.reset_index()
	clip_record = np.array(temp).tolist()
	return clip_record

#statistic depth
def get_depth(sam_file, chr_id, pos_l, pos_r):
	read_depth = sam_file.count_coverage(chr_id,pos_l,pos_r)
	depth = np.array(list(read_depth)).sum(axis=0)   
	depth = list(depth)
	return depth
