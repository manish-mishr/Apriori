from collections import defaultdict
from collections import OrderedDict
from copy import deepcopy as deep


# Decalring all the global variables
transaction_data = {}  #Global dictionary which keeps track of all the item purchased in each transaction.
Minsup = 0.05
Item_number = 0
Item_count = {}
Transaction_number = 0
Minsup_count = 0
Min_confidence = 0.03
Support_data = {}
Candidate_num = 0 
#--------------------------------------------------------------------------------------->>>>


#---------------------------------------------------------------------------------------------->>>>>>

# Read the sparse matrix data and fill the transaction data entry 
def ReadMatrix(filename):
	global transaction_data, Item_count,Minsup_count,Item_number,Minsup
	with open(filename,"r") as file:
		matrix = file.readlines()
		count = 0
		item_track = defaultdict(int)
		for row in matrix:
			items = row.split()
			if count == 0:
				Item_number = len(items)  #calculating the total number of items present in the data just once.

			transaction_data[count] = []
			for index in range(Item_number):
				if items[index] == '1':
					transaction_data[count].append(index) #Append all those item number in the transaction which are present
					item_track[(index,)] += 1
			count += 1

		Item_count = OrderedDict(sorted(item_track.items()))
		Transaction_number = len(transaction_data)
		Minsup_count = int(Minsup * Transaction_number)
		Item_number = len(Item_count)
	file.close()
#----------------------------------------------------------------------------------------->>>>

def calculate_frequent_itemset(itemset):
	global Minsup_count,Item_number,Minsup_count
	frequent_item = {}
	for key in itemset.keys():
		if itemset[key] >= Minsup_count:
			frequent_item[key] = itemset[key]
	return frequent_item

#------------------------------------------------------------------------------------------->>>>
def F1(itemset):
	global Minsup_count,Item_count,Item_number
	candidate_list = []
	if len(itemset) > 0:
		for key_tuple in itemset.keys():
			key_list = sorted(key_tuple)
			last = key_list[-1] + 1
			for index in range(last,Item_number):
				try:
					if Item_count[(index,)] >= Minsup_count:
						new_key_tuple = key_tuple + (index,)
						candidate_list.append(new_key_tuple)
				except:
					continue
	return candidate_list

#-------------------------------------------------------------------------------------------->>>>>

def FK_1(itemset):
	global Minsup_count,Item_count,Item_number
	candidate_list = []
	if len(itemset) > 0:
		key_list = sorted(itemset.keys())
		length = len(key_list)
		len_item = len(key_list[0])
		for ind1 in range(length):
			begin = ind1+1
			for ind2 in range(begin,length):
				itemset1 = key_list[ind1]
				itemset2 = key_list[ind2]
				match = True
				for count in range(len_item-1):	
					if itemset1[count] != itemset2[count]:
						match = False
						break
				if match:
					if itemset1[-1] == itemset2[-1]:
						continue
					elif itemset1[-1] < itemset2[-1]:
						k_itemset = itemset1 + (itemset2[-1],)
					else:
						k_itemset = itemset2 + (itemset1[-1],)
					candidate_list.append(k_itemset)
	return candidate_list

#-------------------------------------------------------------------------------------------------->>>>>
def enumerate(sofar,remaining,count,total_list,fixed):
	if count == 0:
		new_tuple = tuple(deep(sofar))
		total_list.append(new_tuple)
		return  
	elif len(remaining) < count:
		return 
	else:
		rest = deep(remaining[:])
		for ind in range(len(remaining)):
			item = remaining[ind]
			rest.remove(item)
			sofar.append(item)
			new_count = count - 1
			enumerate(sofar,rest,new_count,total_list,fixed)
			sofar.remove(item)
	return total_list



#---------------------------------------------------------------------------------------------------->>>>
def subset_count(candidate_set,transaction,count):
	length = len(transaction)
	itr_transaction = sorted(transaction)
	candidate_list = []
	if count > length:
		return None
	else:
		enumerated_list = enumerate([],itr_transaction,count,[],count)
		for candidate in candidate_set:
			if candidate in enumerated_list:
				candidate_list.append(candidate)
	return candidate_list

#---------------------------------------------------------------------------------------------------->>>>
def candidate_generation(itemset,algo):
	if algo == "F1":
		return F1(itemset)
	elif algo == "FK_1":
		return FK_1(itemset)
	else:
		print "Invalid algo input"
		return
#--------------------------------------------------------------------------------------------------->>>>>
def frequent_itemset_generation(itemset,algo):
	global Support_data,Candidate_num
	frequent_universal_dict = {}
	count = 1
	frequent_itemset = calculate_frequent_itemset(Item_count)
	level = 1
	while True:
		frequent_universal_dict[level]={}
		for key in frequent_itemset.keys():
			frequent_universal_dict[level][key] = frequent_itemset[key]
			Support_data[key] = frequent_itemset[key]
		count += 1
		candidate_set = candidate_generation(frequent_itemset,algo)
		Candidate_num += len(candidate_set)
		support_itemset = defaultdict(int)
		for transaction in transaction_data.values():
			candidate_transaction = subset_count(candidate_set,transaction,count)
			if candidate_transaction != None:
				for candidate in candidate_transaction:
					support_itemset[candidate] += 1
		if len(support_itemset) == 0:
			break
		frequent_itemset = calculate_frequent_itemset(support_itemset)
		level += 1
	return frequent_universal_dict
#----------------------------------------------------------------------------------------------->>>>>
def Maximal_frequent_itemset(itemset):
	maximal_list = []
	for level in itemset.keys():
		for key in itemset[level].keys():
			maximal_list.append(key)
	# print maximal_list
	length = len(itemset)
	for level in range(1,length):
		next_level = level +1
		for key_prev in itemset[level].keys():
			for key_next in itemset[next_level].keys():
				if set(key_prev) < set(key_next):
					maximal_list.remove(key_prev)
					break
					
	return maximal_list

#-------------------------------------------------------------------------------------------------->>>>>>
def Closed_frequent_itemset(itemset):
	closed_list = []
	# for level in itemset.keys():
	# 	for key in itemset[level].keys():
	# 		maximal_list.append(key)
	# print maximal_list
	length = len(itemset)
	# print length
	for level in range(1,length):
		next_level = level + 1
		for key_prev in itemset[level].keys():
			flag = False
			for key_next in itemset[next_level].keys():
				if set(key_prev) < set(key_next):
					if itemset[level][key_prev] == itemset[next_level][key_next]:
						flag == True
						break
			if flag == True:
				closed_list.append(key_prev)

	for key in itemset[length-1].keys():
		closed_list.append(key)			

			
	return closed_list

#--------------------------------------------------------------------------------------------------->>>>>
def apriori_rule(itemset,support_data):
	rules = []
	for  level in range(2,len(itemset)+1):
		# print "level: ", itemset[level]
		# raw_input("level")
		for item_tuple in itemset[level].keys():
			superset = []
			for item in range(level):
				superset.append((item_tuple[item],))
			if (level > 2):
				# print "further"
				generate_rules(item_tuple, superset, support_data, rules)
			else:
				# print "direct confidence"
				confidence_prune(item_tuple, superset, support_data, rules)
	return rules


#-------------------------------------------------------------------------------------------------->>>>>
def confidence_prune(item_tuple, indiv, support_data, rules):
	global Min_confidence
	confient_list = []
	for consequent  in indiv:
		antcedent = subtract(item_tuple,consequent)
		# print "antcedent: ",antcedent
		confidence = float(support_data[item_tuple]) / support_data[antcedent]
		if confidence >= Min_confidence:
			rules.append(tuple((antcedent, consequent, confidence)))
			confient_list.append(consequent)
	return confient_list
#-------------------------------------------------------------------------------------------------->>>>>
def generate_rules(item_tuple, indiv, support_data, rules):
	"Generate a set of candidate rules"
	global Min_confidence
	# print "idi: ",indiv
	length = len(indiv[0]) + 1
	if (len(item_tuple) > (length )):
		candidate_list = apriorigen(indiv)
		candidate_list = confidence_prune(item_tuple, candidate_list,  support_data, rules)
		if len(candidate_list) > 1:
			generate_rules(item_tuple, candidate_list, support_data, rules)
	else:
		consequent = []
		for ind in indiv:
			item = subtract(item_tuple,ind)
			consequent.append(item)
		confidence_prune(item_tuple,consequent,support_data,rules)

#-------------------------------------------------------------------------------------------------->>>>>
def apriorigen(itemset):
	candidate_list = []
	key_list = sorted(itemset)
	length = len(key_list)
	len_item = len(key_list[0])
	for ind1 in range(length):
		begin = ind1+1
		for ind2 in range(begin,length):
			itemset1 = key_list[ind1]
			itemset2 = key_list[ind2]
			match = True
			for count in range(len_item-1):	
				if itemset1[count] != itemset2[count]:
					match = False
					break
			if match:
				if itemset1[-1] == itemset2[-1]:
					continue
				elif itemset1[-1] < itemset2[-1]:
					k_itemset = itemset1 + (itemset2[-1],)
				else:
					k_itemset = itemset2 + (itemset1[-1],)
				candidate_list.append(k_itemset)
	return candidate_list

#--------------------------------------------------------------------------------------------------->>>>>>

def subtract(tuple1, tuple2):
	sub_list = []
	for ind in range(len(tuple1)):
		if tuple1[ind] not in tuple2:
			sub_list.append(tuple1[ind])
	return tuple(sub_list)
#--------------------------------------------------------------------------------------------------->>>>>>
def lift_prune(item_tuple, indiv, support_data, rules):
	global Min_confidence,Transaction_number
	confident_list = []
	for consequent  in indiv:
		antcedent = subtract(item_tuple,consequent)
		# print "antcedent: ",antcedent
		confidence = float(support_data[item_tuple] * Transaction_number) / (support_data[antcedent]*support_data[consequent])
		if confidence >= Min_confidence:
			rules.append(tuple((antcedent, consequent, confidence)))
			confident_list.append(consequent)
	return confident_list



#-------------------------------------------------------------------------------------------------->>>>>
def top10_rules(rules):
	if len(rules) == 0:
		print "For this support and confidence, there no rule exist"
		exit()
	else:
		rules.sort(key=lambda x: x[2],reverse=True)
		if len(rules) <= 10:
			for rule in rules:
				print "item"+str(rule[0])+"\t------>\t"+str(rule[1])+"\tConfidence:\t"+str(rule[2])
		else:
			for ind in range(10):
				rule = rules[ind]
				print "item"+str(rule[0])+"\t------>\t"+str(rule[1])+"\tConfidence:\t"+str(rule[2])
#--------------------------------------------------------------------------------------------------->>>>>>
def total_frequent_item(itemset):
	count = 0
	for level in itemset.keys():
		count += len(itemset[level].keys())

	return count



#--------------------------------------------------------------------------------------------------->>>>>>
def main():
	filename=raw_input("Enter filename: ")
	ReadMatrix(filename)
	algo=raw_input("Enter F1/FK_1 for frequent_itemset: ") 
	itemset = frequent_itemset_generation(Item_count,algo)
	# print itemset

	print "Total Number  of Candidate itemset are: ", Candidate_num
	
	total_frequent = total_frequent_item(itemset)
	print "Total Number of  frequent itemset are: ",total_frequent
	
	maximal_list = Maximal_frequent_itemset(itemset)
	# print "Total Number of Maximal frequent itemset are: ", len(maximal_list)
	
	close_list = Closed_frequent_itemset(itemset)
	# print "Total Number of Closed frequent itemset are: ", len(close_list)
	
	rules = apriori_rule(itemset,Support_data)
	print "Number of total rules: ", len(rules)
	top10_rules(rules)
#--------------------------------------------------------------------------------------------------->>>>>>
if __name__=='__main__':
	main()