Attribute_length = 10
Total_length = 29
Attribute_list = [["x","o","b"],["x","o","b"],["x","o","b"],["x","o","b"],["x","o","b"],["x","o","b"],["x","o","b"],["x","o","b"],["x","o","b"],["positive","negative"]]
Length_list = [0,3,6,9,12,15,18,21,24,27]

def ReadData(filename):
	global Attribute_length,Total_length,Attribute_list,Length_list
	
	with open(filename,"r") as rfile:
		output = open("tic_tac_matrix.txt","w")
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
	ReadData("tic-tac-toe.data")