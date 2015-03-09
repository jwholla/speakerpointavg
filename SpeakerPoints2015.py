import xml.etree.ElementTree as ET
import sys
import os
import tournament_code.validation
import tournament_code.gsuresults
import tournament_code.ukresults
import tournament_code.umkcresults
import tournament_code.harvardresults
import tournament_code.uscresults
import tournament_code.wakeresults
import tournament_code.fullertonresults
import tournament_code.texasresults

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
continue1=0
while continue1==0:
	tournaments=raw_input("Which tournaments would you like to enter? Type ALL for majors, type SOME for fewer tournaments")
	if tournaments=='ALL':
		#adds each tournament
		continue1=5
		tournament_code.gsuresults.gsu(ndt_entries_list,ndt_points)
		tournament_code.ukresults.uk(ndt_entries_list,ndt_points)
		tournament_code.umkcresults.umkc(ndt_entries_list,ndt_points)
		tournament_code.harvardresults.harvard(ndt_entries_list,ndt_points)
		tournament_code.wakeresults.wake(ndt_entries_list,ndt_points)
		tournament_code.uscresults.usc(ndt_entries_list,ndt_points)
		tournament_code.fullertonresults.fullerton(ndt_entries_list,ndt_points)
		tournament_code.texasresults.texas(ndt_entries_list,ndt_points)
	elif tournaments=='SOME':
		subset=raw_input("GSU? Type Y or N")
		continue1=1
		if subset=='Y':
			tournament_code.gsuresults.gsu(ndt_entries_list,ndt_points)
	elif (tournaments!='ALL' and tournaments!='SOME'):
		continue1==0
		raw_input("Please use correct usage")

###print values at the end
speaks= os.path.join(dir,'output\speaker_points.txt')
speaks_avg= os.path.join(dir,'output\speaker_average.txt')
speaker_points= open(speaks, 'r+')
speaker_points.truncate()
speaker_avg=open(speaks_avg, 'r+')
speaker_avg.truncate()
speaks_avg_order=os.path.join(dir,'output\speaker_average_order.txt')
speaker_avg_order=open(speaks_avg_order, 'r+')
speaker_avg_order.truncate()

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
			counter1=float(value[i+1])
			counter2=float(value[i+2])
			counter3=counter1*counter2
			running_sum=running_sum+counter3
			running_count=running_count+counter1
			i+=3
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

#create a new dict that goes the other direction
counter_print=1
#count number of teams that have No tournaments attended
teamsWithNoMajors=0
for w in ndt_average:
	print str(ndt_average[w])
	if 'tournaments' in str(ndt_average[w]):
		teamsWithNoMajors+=1
		print teamsWithNoMajors
for w in sorted(ndt_average, key=ndt_average.get, reverse=True):
	speaker_avg_order.write(str(counter_print-teamsWithNoMajors))
	speaker_avg_order.write(' ')
	speaker_avg_order.write(w)
	speaker_avg_order.write(' ')
	speaker_avg_order.write(str(ndt_average[w]))
	speaker_avg_order.write('\n')
	counter_print=counter_print+1
speaker_avg_order.close()
print("Files have been generated")
raw_input("Press Enter to continue...")
