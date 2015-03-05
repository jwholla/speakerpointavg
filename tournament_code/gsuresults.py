import xml.etree.ElementTree as ET
import sys
import os
from validation import initials_check, calculate_points, get_team_name, rounds
def gsu(ndt_entries_list,ndt_points):
	dir = os.path.dirname(__file__)
	gsu_results= os.path.join(dir, 'results\\gsu_results_3_3.xml')
	gsu_entries_list=[]
	gsu=ET.parse(gsu_results)
	gsu_root=gsu.getroot()
	gsu_codes={} #this dictionary takes their id in tabroom and corresponds to team code
	gsu_points={} #this corresponds team id to points
	for entry in gsu_root.findall('ENTRY'):
		code = entry.find('CODE').text #Emory KS
		id=entry.find('ID').text #team ID
		#check both initials
		code_reversed= initials_check(code)
		if code in ndt_entries_list: 	#if NDT team then do things
			gsu_entries_list.append(code)
			gsu_codes.setdefault(id, []).append(code)
			gsu_codes.setdefault(id, []).append('GSU')
			gsu_points.setdefault(id,[])
		elif code_reversed in ndt_entries_list:
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
		#student is the primary key
		
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
		total=calculate_points(value)
		gsu_codes.setdefault(key,[]).append(total)
		team_name=get_team_name(gsu_codes,key)
		rounds_count=rounds(value)
		###this is where i can append to the ndt points one
		ndt_points.setdefault(team_name,[]).append('GSU')
		ndt_points.setdefault(team_name,[]).append(rounds_count) #append number of data points
		ndt_points.setdefault(team_name,[]).append(total)
		#	gsu_points.setdefault(value[0], []).append(score)