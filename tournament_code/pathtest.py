import xml.etree.ElementTree as ET
import sys
import os

dir = os.path.dirname(__file__)
ndt_data = os.path.join(dir, 'results\\ndt_data_3_3.xml')
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

for entry in ndt_root.findall('ENTRY'):
	code = entry.find('CODE').text
	ndt_entries_list.append(code)
	ndt_points.setdefault(code,[])
	ndt_tournaments.setdefault(code,[])
print ndt_root.keys()
print ndt_root.items()
input("Press Enter to continue...")
