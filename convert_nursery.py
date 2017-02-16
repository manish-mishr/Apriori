Attribute_length = 8
Total_length = 27
Attribute_list = [["usual", "pretentious", "great_pret"],["proper","less_proper","improper", "critical", "very_crit"],["complete", "completed", "incomplete", "foster"],["1", "2", "3", "more"],["convenient", "less_conv", "critical"],["convenient", "inconv"],["nonprob", "slightly_prob", "problematic"],["recommended", "priority", "not_recom"]]
Length_list = [0,3,8,12,16,19,21,24]


def ReadData(filename):
	global Attribute_length,Total_length,Attribute_list,Length_list
	
	with open(filename,"r") as rfile:
		output = open("nursery_matrix.txt","w")
		lines = rfile.readlines()
		for line in lines:
			line = line.strip()
			data = line.split(",") 
			output_line = [0 for i in range(Total_length)]
			if len(data) > 1:
				for ind in range(Attribute_length):
					# print "data: ",data
					# raw_input("check data")
					value = data[ind]
					index = Attribute_list[ind].index(value)
					index = index + Length_list[ind]
					output_line[index] = 1
				for value in output_line:
					output.write(str(value))
					output.write(" ")
				output.write("\n")
		output.close()
	rfile.close()

if __name__=="__main__":
	ReadData("nursery.data")





