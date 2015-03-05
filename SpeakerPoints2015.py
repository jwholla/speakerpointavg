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
speaks_avg= os.path.join(dir,'output\speaker_average.txt')
speaker_points= open(speaks, 'r+')
speaker_points.truncate()
speaker_avg=open(speaks_avg, 'r+')
speaker_avg.truncate()
key_array=[]

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
ndt_average={}

#ndt_points contains a dictionary with a list
#for each entry in the dictionary, i want to create an entry in a new dictionary that contains that average points
for key, value in ndt_points.iteritems():
	#calculate total average
	i=0
	running_sum=0
	running_count=0
	if len(value) >= 1:
		while i < len(value):
			#value[0] is GSU
			counter1=float(value[i+1])
			#print counter1
			#value[1] is 16
			counter2=float(value[i+2])
			#print counter2
			#value[2] is average from GSU
			counter3=counter1*counter2
			#print counter3
			running_sum=running_sum+counter3
			running_count=running_count+counter1
			#the order is tourn_name, num_rounds, average
			#take value[1], cast as float
			#create a sum of values
			#take value[2], cast as float
			#multiply
			#create a sum of these values
			#divide at end
			#this gives average
			i+=3
			#print running_count
		#print running_count
		average=running_sum/running_count
		ndt_average.setdefault(key,[]).append(average)
	else:
		ndt_average.setdefault(key,[]).append('No tournaments attended')

key_array2=[]
for key, value in ndt_average.iteritems() :
	key_array2.append(key)
	key_array2.sort()

for i in key_array2:
	speaker_avg.write(i)
	speaker_avg.write(' ')
	speaker_avg.write(str(ndt_average[i]))
	speaker_avg.write('\n')
speaker_avg.close()
for key, value in ndt_average.iteritems():
	print key, value

input("Press Enter to continue...")
