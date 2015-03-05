import xml.etree.ElementTree as ET
import sys
import os
from validation import initials_check, calculate_points, get_team_name
from gsuresults import gsu
from ukresults import uk
from umkcresults import umkc
from harvardresults import harvard
from wakeresults import wake
from uscresults import usc
from fullertonresults import fullerton
from texasresults import texas

dir = os.path.dirname(__file__)
ndt_data = os.path.join(dir, 'results\\ndt_data_3_3.xml')
ndt_entries = os.path.join(dir, 'entries\\ndt_entries.txt')

#creates a tree of the team list for the NDT
ndt = ET.parse(ndt_data)
ndt_root = ndt.getroot()
ndt_entries_list=[]
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

#adds each tournament
gsu(ndt_entries_list,ndt_points)
uk(ndt_entries_list,ndt_points)
umkc(ndt_entries_list,ndt_points)
harvard(ndt_entries_list,ndt_points)
wake(ndt_entries_list,ndt_points)
usc(ndt_entries_list,ndt_points)
fullerton(ndt_entries_list,ndt_points)
texas(ndt_entries_list,ndt_points)

#build a table that links code to ID

combined_entries= os.path.join(dir,'entries\combined_entries.txt')
combined_entries_txt = open(combined_entries, 'r+')

###print values at the end
speaks= os.path.join(dir,'output\speaker_points.txt')

speaker_points= open(speaks, 'r+')
speaker_points.truncate()
key_array=[]
#for key, value in ndt_points.iteritems() :
#	speaker_points.write(key)
#	speaker_points.write(' ')
#	k=0
#	while k < len(value):
#		temp=str(value[k])
#		speaker_points.write(temp)
#		speaker_points.write(' ')
#		k+=1
#	speaker_points.write('\n')
#print sorted list
for key, value in ndt_points.iteritems() :
	key_array.append(key)
	key_array.sort()

for i in key_array:
	speaker_points.write(i)
	speaker_points.write(' ')
	k=0
	while k < len(ndt_points[i]):
		temp2=ndt_points[i]
		temp=str(temp2[k])
		speaker_points.write(temp)
		speaker_points.write(' ')
		k+=1
	speaker_points.write('\n')
speaker_points.close()

#for key, value in ndt_points.iteritems():
#	print key, value

input("Press Enter to continue...")
