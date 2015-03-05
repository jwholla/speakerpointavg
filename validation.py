
def initials_check(code):
	initials=[]
	initials=code[-2:]
	return code[:-2]+initials[1]+initials[0]
	
def calculate_points(value):
	j=0
	test=value
	for i in value:
		test[j]= float(i)
		j+=1
	return sum(test)/len(test)
	
def get_team_name(codes,key):
	key2=codes[key]
	return key2[0]