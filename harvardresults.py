import xml.etree.ElementTree as ET
import sys
import os
from validation import initials_check, calculate_points, get_team_name, rounds
def harvard(ndt_entries_list,ndt_points):
	dir = os.path.dirname(__file__)
	####add Harvard
	harvard_results= os.path.join(dir,'results\harvard_results_3_4.xml')

	harvard=ET.parse(harvard_results)
	harvard_root=harvard.getroot()
	harvard_entries_list=[]
	harvard_codes={}
	harvard_points={}
	for entry in harvard_root.findall('ENTRY'):
		code = entry.find('CODE').text #Emory KS
		id=entry.find('ID').text #team ID
		#check both initials
		code_reversed=initials_check(code)
		#if NDT team then do things
		if code in ndt_entries_list:
			harvard_entries_list.append(code)
			harvard_codes.setdefault(id, []).append(code)
			harvard_codes.setdefault(id, []).append('harvard')
			harvard_points.setdefault(id,[])
		elif code_reversed in ndt_entries_list:
		#I now have all of the team codes
			harvard_entries_list.append(code)
			harvard_codes.setdefault(id, []).append(code_reversed)
			harvard_codes.setdefault(id, []).append('harvard')
			harvard_points.setdefault(id,[])
	#primary key is now the ID

	#umkc_entries_txt.close()
	harvard_students={} #this corresponds to their team id in tabroom and the debater id
	for entry_student in harvard_root.findall('ENTRY_STUDENT'):
		id=entry_student.find('ID').text #student ID
		entry=entry_student.find('ENTRY').text #team ID
		if entry in harvard_codes:
			harvard_students.setdefault(id, []).append(entry)
		#now the student is the primary key
	temp_score=0.0
	for ballots in harvard_root.findall('BALLOT_SCORE'):
		score_id=ballots.find('SCORE_ID').text #points or not
		temp_score=float(ballots.find('SCORE').text)
		score=ballots.find('SCORE').text #speaker points
		debater=ballots.find('RECIPIENT').text #something
		if temp_score > 25:
		
			if score_id=='POINTS':
				if debater in harvard_students:
					#look up team id
					value=harvard_students[debater]
					harvard_points.setdefault(value[0], []).append(score)
	for key, value in harvard_points.iteritems():
		#value is a list of points that need to be converted
		#key is the id that we append to when we're done
		total=calculate_points(value)
		harvard_codes.setdefault(key,[]).append(total)
		team_name=get_team_name(harvard_codes,key)
		rounds_count=rounds(value)
		###this is where i can append to the ndt points one
		ndt_points.setdefault(team_name,[]).append('harvard')
		ndt_points.setdefault(team_name,[]).append(rounds_count) #append number of data points

		ndt_points.setdefault(team_name,[]).append(total)
	#merge harvard
