import xml.etree.ElementTree as ET
import sys
import os
from validation import initials_check, calculate_points, get_team_name
def uk(ndt_entries_list,ndt_points):
	#########Kentucky
	dir = os.path.dirname(__file__)
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
		code_reversed= initials_check(code)
		#if NDT team then do things
		if code in ndt_entries_list:
		#I now have all of the team codes
			uk_entries_list.append(code)
			uk_codes.setdefault(id, []).append(code)
			uk_codes.setdefault(id, []).append('UK')
			uk_points.setdefault(id,[])
		elif code_reversed in ndt_entries_list:
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
				uk_points.setdefault(value[0], []).append(score)
	for key, value in uk_points.iteritems():
		#value is a list of points that need to be converted
		#key is the id that we append to when we're done
		total=calculate_points(value)
		uk_codes.setdefault(key,[]).append(total)
		team_name=get_team_name(uk_codes,key)
		###this is where i can append to the ndt points one
		ndt_points.setdefault(team_name,[]).append('UK')
		ndt_points.setdefault(team_name,[]).append(total)
	#merge UK and GSU results
