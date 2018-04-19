class BAM:
	def __init__(self):
		self.read_len = 0  
		self.read_cnt = 0
		self.bam_record = []
		self.pile_record = []
		self.clip_record = []
		self.depth = []


	def read_record(self, sam_file, chr_id, pos_l, pos_r):
		for read in sam_file.fetch(chr_id,pos_l,pos_r):
			if None != read.cigarstring:
				self.bam_record.append(read)
				print(read.reference_start)
				print(read)

			self.read_cnt = len(self.bam_record)
			self.read_len = self.bam_record[self.read_cnt-1].infer_read_length()
