import xml.etree.ElementTree as ET
import sys
import os
from validation import initials_check, calculate_points, get_team_name
def usc(ndt_entries_list,ndt_points):
	dir = os.path.dirname(__file__)
	usc_results= os.path.join(dir,'results\usc_results_3_4.xml')

	usc=ET.parse(usc_results)
	usc_root=usc.getroot()
	usc_entries_list=[]
	usc_codes={}
	usc_points={}
	for entry in usc_root.findall('ENTRY'):
		code = entry.find('CODE').text #Emory KS
		id=entry.find('ID').text #team ID
		#check both initials
		code_reversed=initials_check(code)
		#if NDT team then do things
		if code in ndt_entries_list:
			usc_entries_list.append(code)
			usc_codes.setdefault(id, []).append(code)
			usc_codes.setdefault(id, []).append('usc')
			usc_points.setdefault(id,[])
		elif code_reversed in ndt_entries_list:
		#I now have all of the team codes
			usc_entries_list.append(code)
			usc_codes.setdefault(id, []).append(code_reversed)
			usc_codes.setdefault(id, []).append('usc')
			usc_points.setdefault(id,[])
	#primary key is now the ID

	#umkc_entries_txt.close()
	usc_students={} #this corresponds to their team id in tabroom and the debater id
	for entry_student in usc_root.findall('ENTRY_STUDENT'):
		id=entry_student.find('ID').text #student ID
		entry=entry_student.find('ENTRY').text #team ID
		if entry in usc_codes:
			usc_students.setdefault(id, []).append(entry)
		#now the student is the primary key
	temp_score=0.0
	for ballots in usc_root.findall('BALLOT_SCORE'):
		score_id=ballots.find('SCORE_ID').text #points or not
		temp_score=float(ballots.find('SCORE').text)
		score=ballots.find('SCORE').text #speaker points
		debater=ballots.find('RECIPIENT').text #something
		if temp_score > 25:
		
			if score_id=='POINTS':
				if debater in usc_students:
					#look up team id
					value=usc_students[debater]
					usc_points.setdefault(value[0], []).append(score)
	for key, value in usc_points.iteritems():
		#value is a list of points that need to be converted
		#key is the id that we append to when we're done
		total=calculate_points(value)
		usc_codes.setdefault(key,[]).append(total)
		team_name=get_team_name(usc_codes,key)
		###this is where i can append to the ndt points one
		ndt_points.setdefault(team_name,[]).append('usc')
		ndt_points.setdefault(team_name,[]).append(total)
	#merge usc
