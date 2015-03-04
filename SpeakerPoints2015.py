import xml.etree.ElementTree as ET
import sys
import os

dir = os.path.dirname(__file__)
print dir
ndt_data = os.path.join(dir, 'results\\ndt_data_3_3.xml')
print ndt_data
ndt_entries = os.path.join(dir, 'entries\\ndt_entries.txt')
gsu_results= os.path.join(dir, 'results\\gsu_results_3_3.xml')
gsu_entries= os.path.join(dir,'entries\\gsu_entries.txt')

#creates a tree of the team list for the NDT
ndt = ET.parse(ndt_data)
ndt_root = ndt.getroot()
ndt_entries_list=[]
gsu_entries_list=[]
texas_entries_list=[]
combined_entries_list=[]
ndt_points={} #contains the team code as primary key, average points
ndt_tournaments={} #contains the team code as primary key, list of tournaments that were attended

ndt_entries_txt = open(ndt_entries, 'r+')
for entry in ndt_root.findall('ENTRY'):
	code = entry.find('CODE').text
	ndt_entries_txt.write(code)
	ndt_entries_txt.write('\n')
	ndt_entries_list.append(code)
	ndt_points.setdefault(code,[])
	ndt_tournaments.setdefault(code,[])
ndt_entries_txt.close()

#now that I have ndt part done, i ONLY care about NDT teams


gsu=ET.parse(gsu_results)
gsu_root=gsu.getroot()
gsu_entries_txt = open(gsu_entries, 'r+')
gsu_codes={} #this dictionary takes their id in tabroom and corresponds to team code
gsu_points={} #this corresponds team id to points

for entry in gsu_root.findall('ENTRY'):
	code = entry.find('CODE').text #Emory KS
	id=entry.find('ID').text #team ID
	#check both initials
	initials=code[-2:]
	code_reversed=code[:-2]+initials[1]+initials[0]
	#if NDT team then do things
	if code in ndt_entries_list:
	# or (code_reversed in ndt_entries_list)
		gsu_entries_txt.write(code)
		gsu_entries_txt.write('\n')
	#I now have all of the team codes
		gsu_entries_list.append(code)
		gsu_codes.setdefault(id, []).append(code)
		gsu_codes.setdefault(id, []).append('GSU')
		gsu_points.setdefault(id,[])
	elif code_reversed in ndt_entries_list:
		gsu_entries_txt.write(code_reversed)
		gsu_entries_txt.write('\n')
	#I now have all of the team codes
		gsu_entries_list.append(code)
		gsu_codes.setdefault(id, []).append(code_reversed)
		gsu_codes.setdefault(id, []).append('GSU')
		gsu_points.setdefault(id,[])
#primary key is now the ID

gsu_students={} #this corresponds to their team id in tabroom and the debater id
for entry_student in gsu_root.findall('ENTRY_STUDENT'):
	id=entry_student.find('ID').text #student ID
	entry=entry_student.find('ENTRY').text #team ID
	if entry in gsu_codes:
		gsu_students.setdefault(id, []).append(entry)
	#now the student is the primary key
	
for ballots in gsu_root.findall('BALLOT_SCORE'):
	score_id=ballots.find('SCORE_ID').text #points or not
	score=ballots.find('SCORE').text #speaker points
	debater=ballots.find('RECIPIENT').text #something
	
	if score_id=='POINTS':
		if debater in gsu_students:
			#look up team id
			value=gsu_students[debater]
			#tel['jack'] returns the value, which means i need the team id as the key
			gsu_points.setdefault(value[0], []).append(score)




for key, value in gsu_points.iteritems():
	#value is a list of points that need to be converted
	#key is the id that we append to when we're done
	j=0
	test=value
	for i in value:
		test[j]= float(i)
		j+=1
	total = sum(test)/len(test)
	gsu_codes.setdefault(key,[]).append(total)
	key2=gsu_codes[key]
	key3=key2[0]
	###this is where i can append to the ndt points one
	ndt_points.setdefault(key3,[]).append('GSU')
	ndt_points.setdefault(key3,[]).append(total)
	#	gsu_points.setdefault(value[0], []).append(score)

#build a table that links code to ID

#for key, value in gsu_codes.iteritems() :
#	print key, value
#for key, value in gsu_students.iteritems():
#	print key, value
#for key, value in gsu_points.iteritems():
#	print key, value
gsu_entries_txt.close()
combined_entries= os.path.join(dir,'entries\combined_entries.txt')

combined_entries_txt = open(combined_entries, 'r+')
#need to make a change here to account for reverse partnerships


#########Kentucky
uk_entries= os.path.join(dir,'entries\combined_entries.txt')
uk_results= os.path.join(dir,'results\kentucy_results_3_3.xml')

uk=ET.parse(uk_results)
uk_root=uk.getroot()
uk_entries_txt = open(uk_entries, 'r+')
uk_entries_list=[]
uk_codes={}
uk_points={}
for entry in uk_root.findall('ENTRY'):
	code = entry.find('CODE').text #Emory KS
	id=entry.find('ID').text #team ID
	#check both initials
	initials=code[-2:]
	code_reversed=code[:-2]+initials[1]+initials[0]
	#if NDT team then do things
	if code in ndt_entries_list:
	# or (code_reversed in ndt_entries_list)
		uk_entries_txt.write(code)
		uk_entries_txt.write('\n')
	#I now have all of the team codes
		uk_entries_list.append(code)
		uk_codes.setdefault(id, []).append(code)
		uk_codes.setdefault(id, []).append('UK')
		uk_points.setdefault(id,[])
	elif code_reversed in ndt_entries_list:
		uk_entries_txt.write(code_reversed)
		uk_entries_txt.write('\n')
	#I now have all of the team codes
		uk_entries_list.append(code)
		uk_codes.setdefault(id, []).append(code_reversed)
		uk_codes.setdefault(id, []).append('UK')
		uk_points.setdefault(id,[])
#primary key is now the ID

uk_entries_txt.close()
uk_students={} #this corresponds to their team id in tabroom and the debater id
for entry_student in uk_root.findall('ENTRY_STUDENT'):
	id=entry_student.find('ID').text #student ID
	entry=entry_student.find('ENTRY').text #team ID
	if entry in uk_codes:
		uk_students.setdefault(id, []).append(entry)
	#now the student is the primary key
	
for ballots in uk_root.findall('BALLOT_SCORE'):
	score_id=ballots.find('SCORE_ID').text #points or not
	score=ballots.find('SCORE').text #speaker points
	debater=ballots.find('RECIPIENT').text #something
	
	if score_id=='POINTS':
		if debater in uk_students:
			#look up team id
			value=uk_students[debater]
			#tel['jack'] returns the value, which means i need the team id as the key
			uk_points.setdefault(value[0], []).append(score)
for key, value in uk_points.iteritems():
	#value is a list of points that need to be converted
	#key is the id that we append to when we're done
	j=0
	test=value
	for i in value:
		test[j]= float(i)
		j+=1
	total = sum(test)/len(test)
	uk_codes.setdefault(key,[]).append(total)
	key2=uk_codes[key]
	key3=key2[0]
	###this is where i can append to the ndt points one
	ndt_points.setdefault(key3,[]).append('UK')
	ndt_points.setdefault(key3,[]).append(total)
#merge UK and GSU results
#for key, value in uk_codes.iteritems():
#	gsu_codes.setdefault(key,[]).append(value)

#####add umkc
#uk_entries= os.path.join(dir,'entries\combined_entries.txt')
umkc_results= os.path.join(dir,'results\umkc_results_3_4.xml')

umkc=ET.parse(umkc_results)
umkc_root=umkc.getroot()
#umkc_entries_txt = open(umkc_entries, 'r+')
umkc_entries_list=[]
umkc_codes={}
umkc_points={}
for entry in umkc_root.findall('ENTRY'):
	code = entry.find('CODE').text #Emory KS
	id=entry.find('ID').text #team ID
	#check both initials
	initials=code[-2:]
	code_reversed=code[:-2]+initials[1]+initials[0]
	#if NDT team then do things
	if code in ndt_entries_list:
	# or (code_reversed in ndt_entries_list)
#		umkc_entries_txt.write(code)
#		umkc_entries_txt.write('\n')
	#I now have all of the team codes
		umkc_entries_list.append(code)
		umkc_codes.setdefault(id, []).append(code)
		umkc_codes.setdefault(id, []).append('umkc')
		umkc_points.setdefault(id,[])
	elif code_reversed in ndt_entries_list:
#		umkc_entries_txt.write(code_reversed)
#		umkc_entries_txt.write('\n')
	#I now have all of the team codes
		umkc_entries_list.append(code)
		umkc_codes.setdefault(id, []).append(code_reversed)
		umkc_codes.setdefault(id, []).append('umkc')
		umkc_points.setdefault(id,[])
#primary key is now the ID

#umkc_entries_txt.close()
umkc_students={} #this corresponds to their team id in tabroom and the debater id
for entry_student in umkc_root.findall('ENTRY_STUDENT'):
	id=entry_student.find('ID').text #student ID
	entry=entry_student.find('ENTRY').text #team ID
	if entry in umkc_codes:
		umkc_students.setdefault(id, []).append(entry)
	#now the student is the primary key
	
for ballots in umkc_root.findall('BALLOT_SCORE'):
	score_id=ballots.find('SCORE_ID').text #points or not
	score=ballots.find('SCORE').text #speaker points
	debater=ballots.find('RECIPIENT').text #something
	
	if score_id=='POINTS':
		if debater in umkc_students:
			#look up team id
			value=umkc_students[debater]
			#tel['jack'] returns the value, which means i need the team id as the key
			umkc_points.setdefault(value[0], []).append(score)
for key, value in umkc_points.iteritems():
	#value is a list of points that need to be converted
	#key is the id that we append to when we're done
	j=0
	test=value
	for i in value:
		test[j]= float(i)
		j+=1
	total = sum(test)/len(test)
	umkc_codes.setdefault(key,[]).append(total)
	key2=umkc_codes[key]
	key3=key2[0]
	###this is where i can append to the ndt points one
	ndt_points.setdefault(key3,[]).append('UMKC')
	ndt_points.setdefault(key3,[]).append(total)
#merge umkc


###print values at the end
speaks= os.path.join(dir,'output\speaker_points.txt')

speaker_points= open(speaks, 'r+')
speaker_points.truncate()
for key, value in ndt_points.iteritems() :
	speaker_points.write(key)
	speaker_points.write(' ')
	k=0
	while k < len(value):
		temp=str(value[k])
		speaker_points.write(temp)
		speaker_points.write(' ')
		k+=1
	speaker_points.write('\n')
speaker_points.close()
#for key, value in uk_codes.iteritems():
#	print key, value
for key, value in ndt_points.iteritems():
	print key, value

input("Press Enter to continue...")
