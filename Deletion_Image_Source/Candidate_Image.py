# generate candidate deletion
def call_del(vcf_del,sam_file,del_name):
	vcf_len = len(vcf_del)
	print("vcf_len %d"%vcf_len)
	del_pos = []
	for i in range(vcf_len):
		print("i = %d"%i)
		read_depth = get_depth(sam_file,vcf_del[i][0],int(vcf_del[i][1]-200),int(vcf_del[i][2]+200))
		seq_depth = []

		len_deletion = len(read_depth)
		for j in range(len_deletion):
			seq_depth.append((int(vcf_del[i][1]-200+j), int(read_depth[j])))

		clip_pic = get_clip_num(sam_file,vcf_del[i][0],vcf_del[i][1]-200,vcf_del[i][2]+200)
		plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
		fig = plt.figure()
		ax = init_pic(6,1,1,fig,'2d')
		seq_depth_array = np.array(seq_depth)
		ax.plot(seq_depth_array[:,0],seq_depth_array[:,1],color='r')  
		seq_clip_array = np.array(clip_pic)
		ax.plot(seq_clip_array[:,0],seq_clip_array[:,1]*2,color='g')

		result = kmeans(seq_depth_array,3,100000)
		result = np.nan_to_num(result)

		class_one = result[result[:,-1]==1,:-1]
		class_two = result[result[:,-1]==2,:-1]
		class_three= result[result[:,-1]==3,:-1]


		ax2 = init_pic(6,1,2,fig,'2d')
		ax2.bar(class_one[:,0],class_one[:,1],color='r')
		ax2.bar(class_two[:,0],class_two[:,1],color='g')
		ax2.bar(class_three[:,0],class_three[:,1],color='b')

	
		df_depth = pd.DataFrame(seq_depth_array)
		df_clip = pd.DataFrame(seq_clip_array)

		df_merge = pd.merge(df_depth, df_clip, on=[0], how='left')
		df_merge_fill = df_merge.fillna(0)
		df_merge_np_roll = np.array(df_merge_fill)

		df_merge_fill_re = pd.rolling_median(df_merge_np_roll[:,1],61,center=True)
		df_merge_fill_re = np.nan_to_num(df_merge_fill_re)
		df_merge_fill_re = df_merge_fill_re[30:-30]*5
		smooth_kmeans = np.c_[df_merge_np_roll[30:-30,0],df_merge_fill_re]
		smooth_kmeans = np.c_[smooth_kmeans, df_merge_np_roll[30:-30,2]]

		# cluster
		result_3D = kmeans(smooth_kmeans,3,100000)
		result_3D = np.nan_to_num(result_3D)

		class_one_3D = result_3D[result_3D[:,-1]==1,:-1]
		class_two_3D = result_3D[result_3D[:,-1]==2,:-1]
		class_three_3D= result_3D[result_3D[:,-1]==3,:-1]

		class_one_3D = class_one_3D[np.lexsort(class_one_3D[:,::-1].T)]
		class_two_3D = class_two_3D[np.lexsort(class_two_3D[:,::-1].T)]
		class_three_3D = class_three_3D[np.lexsort(class_three_3D[:,::-1].T)]


		class_one_3D_mean = np.mean(class_one_3D[:,1])//5
		class_two_3D_mean = np.mean(class_two_3D[:,1])//5
		class_three_3D_mean = np.mean(class_three_3D[:,1])//5

		class_one_3D_min = np.min(class_one_3D[:,1])//5
		class_two_3D_min = np.min(class_two_3D[:,1])//5
		class_three_3D_min = np.min(class_three_3D[:,1])//5

		class_array_min = [class_one_3D_min, class_two_3D_min, class_three_3D_min]

		class_array = [class_one_3D_mean, class_two_3D_mean, class_three_3D_mean]

		class_sort = np.sort(class_array)
		del_left_pos = 0
		del_right_pos = 0
		if class_sort[0] < 4*class_sort[1]//5 and class_sort[0] < 4*class_sort[2]//5:

			class_min_index = np.argmin(class_array)
			class_max_index = np.argmax(class_array)
			class_mid_index = 3-class_max_index-class_min_index
			seq_depth_dict = dict(seq_depth)
		
			if class_min_index == 0 and int(class_one_3D[0,0]) != smooth_kmeans[0,0] and int(class_one_3D[-1,0]) != smooth_kmeans[-1,0]:
				del_left_pos = int(class_one_3D[0,0])
				del_right_pos = int(class_one_3D[-1,0])

				while del_left_pos:
					if seq_depth_dict[del_left_pos] > class_array_min[class_mid_index] or del_left_pos == seq_depth[0][0]:
						break
					del_left_pos -= 1
				while del_right_pos:
					if seq_depth_dict[del_right_pos] > class_array_min[class_mid_index] or del_right_pos == seq_depth[-1][0]:
						break
					del_right_pos += 1

				del_left_diff = int(class_one_3D[0,0] - del_left_pos)
				del_right_diff = int(del_right_pos - class_one_3D[-1,0])
				del_pos.append((del_left_pos, del_right_pos, int(class_one_3D[0,0]), int(class_one_3D[-1,0])))

			elif class_min_index == 1 and int(class_two_3D[0,0]) != smooth_kmeans[0,0] and int(class_two_3D[-1,0]) != smooth_kmeans[-1,0]:
				del_left_pos = int(class_two_3D[0,0])
				del_right_pos = int(class_two_3D[-1,0])

				while del_left_pos:
					if seq_depth_dict[del_left_pos] > class_array_min[class_mid_index] or del_left_pos == seq_depth[0][0]:
						break
					del_left_pos -= 1
				while del_right_pos:
					if seq_depth_dict[del_right_pos] > class_array_min[class_mid_index] or del_right_pos == seq_depth[-1][0]:
						break
					del_right_pos += 1

				del_left_diff = int(class_two_3D[0,0] - del_left_pos)
				del_right_diff = int(del_right_pos - class_two_3D[-1,0])
				del_pos.append((del_left_pos, del_right_pos, int(class_two_3D[0,0]), int(class_two_3D[-1,0])))

			elif class_min_index == 2 and int(class_three_3D[0,0]) != smooth_kmeans[0,0] and int(class_three_3D[-1,0]) != smooth_kmeans[-1,0]:
				del_left_pos = int(class_three_3D[0,0])
				del_right_pos = int(class_three_3D[-1,0])

				while del_left_pos:
					if seq_depth_dict[del_left_pos] > class_array_min[class_mid_index] or del_left_pos == seq_depth[0][0]:
						break
					del_left_pos -= 1
				while del_right_pos:
					if seq_depth_dict[del_right_pos] > class_array_min[class_mid_index] or del_right_pos == seq_depth[-1][0]:
						break
					del_right_pos += 1

				del_left_diff = int(class_three_3D[0,0] - del_left_pos)
				del_right_diff = int(del_right_pos - class_three_3D[-1,0])
				del_pos.append((del_left_pos, del_right_pos, int(class_three_3D[0,0]), int(class_three_3D[-1,0])))


			ax3 = init_pic(6,1,3,fig,'3d')
			ax3.scatter(class_one_3D[:,0],class_one_3D[:,1],class_one_3D[:,2],color='r')
			ax3.scatter(class_two_3D[:,0],class_two_3D[:,1],class_two_3D[:,2],color='g')
			ax3.scatter(class_three_3D[:,0],class_three_3D[:,1],class_three_3D[:,2],color='b')
			ax3.set_xlabel('X')
			ax3.set_zlabel('Z') 
			ax3.set_ylabel('Y')
			
			ax4 = init_pic(6,1,4,fig,'2d')
			ax4.plot(class_one_3D[:,0],class_one_3D[:,1],color='r')  
			ax4.plot(class_two_3D[:,0],class_two_3D[:,1],color='g')  
			ax4.plot(class_three_3D[:,0],class_three_3D[:,1],color='b')  
			
			print("left_pos %d"%del_left_pos)
			print("right_pos %d"%del_right_pos)
			if del_right_pos - del_left_pos != 0  and del_right_pos + del_left_pos != 0:

				del_len = del_right_pos - del_left_pos + 1
				del_pic = []
				for del_i in range(del_len):
					del_pic.append((del_left_pos+del_i, seq_depth_dict[del_left_pos+del_i]))

				del_pic = np.array(del_pic)
				ax5 = init_pic(6,1,5,fig,'2d')

				ax5.plot(del_pic[:,0],del_pic[:,1],color='r')  


		fig.set_size_inches(18.5, 20.5)
		print("last_i= %d"%i)
		if os.path.exists('your file name'):
			fig.savefig("your file name" + del_name+"_"+str(i) + '_' + str(del_left_pos) + '_' + str(del_right_pos)+".png")
		else:
			os.mkdir('your file name')
			fig.savefig("your file name" + del_name+"_"+str(i) + '_' + str(del_left_pos) + '_' + str(del_right_pos)+".png")

		plt.close('all')
	return del_pos

# divide image
def draw_pic(clip_dict_record, pile_record,del_pos_np_start, deletion_length):
	blank = Image.new("RGB",[256, 256],"white")

	pile_record_len = len(pile_record)
	drawObject = ImageDraw.Draw(blank)
	y_start_index = 0
	old_x_start = 5
	for j in range(pile_record_len):
			print("-- %d"%pile_record[j][0])
			print("--- %d"%del_pos_np_start)
			x_start = (pile_record[j][0] - del_pos_np_start)*5 + 5
			print("x_start %d "%x_start)
			if old_x_start == x_start:
				old_x_start = x_start
				print("x_pic_start %d"%x_start)
				y_start = 5 + y_start_index*5
				print("y_pic_start %d"%y_start)
				print("y_index %d"%y_start_index)
				y_start_index += 1
				x_end = x_start + 5
				y_end = y_start + 5
				if pile_record[j][0] in clip_dict_record:
					base_rgb = get_rgb(-clip_dict_record[pile_record[j][0]],pile_record[j])
				else:
					base_rgb = get_rgb(0,pile_record[j])
				print("rgb")
				print(base_rgb)
				drawObject.rectangle((x_start,y_start, x_end, y_end),fill=base_rgb)
			elif old_x_start != x_start:
				old_x_start = x_start
				print("x_pic_start %d"%x_start)
				y_start_index = 0
				y_start = 5 + y_start_index*5
				print("y_pic_start %d"%y_start)
				y_start_index += 1
				x_end = x_start + 5
				y_end = y_start + 5

				if pile_record[j][0] in clip_dict_record:
					base_rgb = get_rgb(-clip_dict_record[pile_record[j][0]],pile_record[j])
				else:
					base_rgb = get_rgb(0,pile_record[j])
				print("rgb")
				print(base_rgb)
				drawObject.rectangle((x_start,y_start, x_end, y_end),fill=base_rgb)

	#../NA20845/true_gene_pic/gene_pic/del_chr2_50_200
	if os.path.exists('your filepath'):
		blank.save("your filepath"+'del_1_' + str(del_pos_np_start) + '_' +str(del_pos_np_start + deletion_length) + ".png","PNG")
	else:
		os.mkdir('your filepath')
		blank.save("your filepath"+'del_1_' + str(del_pos_np_start) + '_' +str(del_pos_np_start + deletion_length) + ".png","PNG")

# get position
def gene_point_pic(chr_id, pos_l, pos_r):
	gene_pic = []
	every_len = pos_l
	while every_len < pos_r:
		gene_tuple = (chr_id, every_len, every_len+50)
		gene_pic.append(gene_tuple)
		every_len = every_len + 50
	if every_len >= pos_r:
		gene_tuple = (chr_id, every_len-50, pos_r)
		gene_pic.append(gene_tuple)
	return gene_pic