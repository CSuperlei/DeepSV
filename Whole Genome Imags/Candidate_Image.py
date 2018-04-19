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