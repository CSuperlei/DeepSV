class VCF:
	def __init__(self, vcf_file):
		self.vcf_file = vcf_file
		self.del_50_200 = []
		self.del_200_700 = []
		self.del_700_1000 = []
		self.del_1000 = []
		self.del_other = []


	def vcf_class(self):
		for vcf in self.vcf_file:
			if(abs(vcf[1]-vcf[2])>=50 and abs(vcf[1]-vcf[2])<200):
				self.del_50_200.append(vcf)
			elif(abs(vcf[1]-vcf[2])>=200 and abs(vcf[1]-vcf[2])<700):
				self.del_200_700.append(vcf)
			elif(abs(vcf[1]-vcf[2])>=700 and abs(vcf[1]-vcf[2])<1000):
				self.del_700_1000.append(vcf)
			elif(abs(vcf[1]-vcf[2])>=1000):
				self.del_1000.append(vcf)
			else:
				self.del_other.append(vcf)
