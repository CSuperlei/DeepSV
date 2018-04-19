class File:
	def get_vcf_file(self,vcf_path, isdel):
		deletion_pos = open(vcf_path,'r')
		if deletion_pos == None:
			print('vcf is empty')
			return
		vcf_detail = []
		vcf_upAnchor = []
		vcf_downAnchor = []

		if isdel == 'deletion':
			for temp in deletion_pos:
				tmp = temp.split('\t')
				chr_id = tmp[0]
				scan_l_pos = int(tmp[1])
				scan_r_pos = int(tmp[2])
				vcf_tuples = (chr_id,scan_l_pos,scan_r_pos)
				vcf_detail.append(vcf_tuples)
			return vcf_detail

		elif isdel == 'non_deletion_upAnchor':
			for temp in deletion_pos:
				tmp = temp.split('\t')
				chr_id = tmp[0]
				scan_l_pos = int(tmp[1])
				scan_r_pos = int(tmp[2])
				print("scan_l_pos %d"%scan_l_pos)
				print("scan_r_pos %d"%scan_r_pos)
				del_length = scan_r_pos - scan_l_pos + 1
				if del_length >700:
					del_length = 4 * del_length // 5
				upAnchor_l_pos = scan_l_pos - del_length - 150
				upAnchor_r_pos = upAnchor_l_pos + del_length
				print("upAnchor_l_pos %d"%upAnchor_l_pos)
				print("upAnchor_r_pos %d"%upAnchor_r_pos)
				vcf_tuples = (chr_id, upAnchor_l_pos, upAnchor_r_pos)
				vcf_upAnchor.append(vcf_tuples)
			return vcf_upAnchor

		elif isdel == 'non_deletion_downAnchor':
			for temp in deletion_pos:
				tmp = temp.split('\t')
				chr_id = tmp[0]
				scan_l_pos = int(tmp[1])
				scan_r_pos = int(tmp[2])
				print("scan_l_pos %d"%scan_l_pos)
				print("scan_r_pos %d"%scan_r_pos)
				del_length = scan_r_pos - scan_l_pos + 1
				if del_length >700:
					del_length = 4 * del_length // 5
				downAnchor_l_pos = scan_r_pos + 150
				downAnchor_r_pos = downAnchor_l_pos + del_length
				print("upAnchor_l_pos %d"%downAnchor_l_pos)
				print("upAnchor_r_pos %d"%downAnchor_r_pos)
				vcf_tuples = (chr_id, downAnchor_l_pos, downAnchor_r_pos)
				vcf_downAnchor.append(vcf_tuples)
			return vcf_downAnchor

	def get_sam_file(self,bam_path):
		sam_file = pysam.AlignmentFile(bam_path,"rb")
		if sam_file == None:
			print("bam_file is empty")
			return
		return sam_file



