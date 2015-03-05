import xml.etree.ElementTree as ET
import sys
import os
from validation import initials_check, calculate_points, get_team_name, rounds
def umkc(ndt_entries_list,ndt_points):
	dir = os.path.dirname(__file__)
	#####add umkc
	umkc_results= os.path.join(dir,'results\umkc_results_3_4.xml')

	umkc=ET.parse(umkc_results)
	umkc_root=umkc.getroot()
	umkc_entries_list=[]
	umkc_codes={}
	umkc_points={}
	for entry in umkc_root.findall('ENTRY'):
		code = entry.find('CODE').text #Emory KS
		id=entry.find('ID').text #team ID
		#check both initials
		code_reversed=initials_check(code)
		#if NDT team then do things
		if code in ndt_entries_list:
			umkc_entries_list.append(code)
			umkc_codes.setdefault(id, []).append(code)
			umkc_codes.setdefault(id, []).append('umkc')
			umkc_points.setdefault(id,[])
		elif code_reversed in ndt_entries_list:
			umkc_entries_list.append(code)
			umkc_codes.setdefault(id, []).append(code_reversed)
			umkc_codes.setdefault(id, []).append('umkc')
			umkc_points.setdefault(id,[])
	#primary key is now the ID

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
				umkc_points.setdefault(value[0], []).append(score)
	for key, value in umkc_points.iteritems():
		#value is a list of points that need to be converted
		#key is the id that we append to when we're done
		total=calculate_points(value)
		umkc_codes.setdefault(key,[]).append(total)
		team_name=get_team_name(umkc_codes,key)
		rounds_count=rounds(value)
		###this is where i can append to the ndt points one
		ndt_points.setdefault(team_name,[]).append('UMKC')
		ndt_points.setdefault(team_name,[]).append(rounds_count) #append number of data points		
		ndt_points.setdefault(team_name,[]).append(total)
	#merge umkc
