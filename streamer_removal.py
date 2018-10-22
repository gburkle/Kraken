#!/usr/bin/env python3 -tt
#-*- coding: UTF-8 -*- 
"""
Remove all instances (Folders and links) of streamerdata malware. 
"""
import re
import os
import shutil
import datetime


## GET DATE ANT TIME FOR LOG FILE IN CASE OF ERRORS
dateandtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
log_file = "streamer_removal_"+dateandtime+".log"

def main():
	print("[*] REMOVING ALL INSTANCES OF STREAMER.")
	global log_file
	
	## GET PRESENT WORKING DIRECTORY. SCAN WILL START FROM HERE. 
	dir_path = os.path.dirname(os.path.realpath(__file__))
		
	## START THE SCAN
	results = devour_streamer(dir_path)
	
	if results == "CLEAN":
		print("[*] SCAN COMPLETED WITH NO ERRORS")
	elif results == "ERRORS":
		print("[*] SCAN COMPLETED WITH ERRORS!!. Check "+log_file+" file for more details.")
	else:
		print("\nSomething weird happened.\n")
	


def devour_streamer(path):
	"Find and destroy streamer Malware"
	
	global log_file

	evil = b'\x73\x00\x74\x00\x61\x00\x72\x00\x74\x00\x20\x00\x73\x00\x74\x00\x72\x00\x65\x00\x61\x00\x6D\x00\x65\x00\x72\x00\x64' \
		+ b'\x00\x61\x00\x74\x00\x61\x00\x5C\x00\x73\x00\x74\x00\x72\x00\x65\x00\x61\x00\x6D\x00\x65\x00\x72\x00\x2E\x00\x65\x00' \
		 + b'\x78\x00\x65\x00\x20\x00\x2F\x00\x41\x00\x75\x00\x74\x00\x6F\x00\x49\x00\x74\x00\x33\x00\x45\x00\x78\x00\x65\x00\x63' \
		 + b'\x00\x75\x00\x74\x00\x65\x00\x53\x00\x63\x00\x72\x00\x69\x00\x70\x00\x74\x00\x20\x00\x22\x00\x73\x00\x74\x00\x72\x00' \
		 + b'\x65\x00\x61\x00\x6D\x00\x65\x00\x72\x00\x64\x00\x61\x00\x74\x00\x61\x00\x5C\x00\x73\x00\x74\x00\x72\x00\x65\x00\x61' \
		 + b'\x00\x6D\x00\x2E\x00\x74\x00\x78\x00\x74\x00\x22'
	
	#print(evil.decode('utf-8'))

	for path, listofdirs, listoffiles in os.walk(path):				
		### EAT THE LINKS 
		links = []
		
		for item in listoffiles:
			#print(item)
			find_link = re.compile('(.+%s)$' % ".lnk")
			link_found = find_link.findall(item.lower())
			if link_found:
				links.append(link_found)
				
		if links:
			for link in links:
				clean_link = (''.join(link))
				full_link = (path+"\\"+clean_link)
			
				
				try:
					with open(full_link, 'rb') as f:
						s = f.read()
					result = s.find(evil)	
					
					if result != -1:
						print("[*] FOUND STREAMER LINK AT ("+ full_link +") PROCEADING TO ELIMINATE....", end="", flush=True)
						result = devour_prey(full_link, True)
						print("["+result+"]")
					else:
						continue				
				except Exception as e:
					log_errors(full_link, e)		

		### EAT THE FOLDERS
		location=path.lower()	
		find_folder = re.compile('\\\\(%s)$' % "streamerdata")
		folder_found = find_folder.findall(location)
		
		if folder_found:
			print("[*] FOUND STREAMER FOLDER AT ("+ path +") PROCEADING TO ELIMINATE....", end="", flush=True)
			result = devour_prey(path)
			print("["+result+"]")
		else:
			continue
	

	if not os.path.isdir(log_file):
		return('CLEAN')
	else:
		return('ERRORS')

	
def devour_prey(path, file=False):
	"DELETE FOUND FOLDERS OR FILES"

	if file == False:
		try:
			shutil.rmtree(path, ignore_errors=False, onerror=None)
			result = "SUCCESS"
		except Exception as e:
			result = "ERROR"
			log_errors(path, e)
	else:
		try:
			os.remove(path)
			result = "SUCCESS"
		except Exception as e:
			result = "ERROR"
			log_errors(path, e)
	
	return result
	
def log_errors(path, log):
	"Log errors to streamer_removal.log"
	
	global log_file
	
	filehandle = open(log_file,'a')
	filehandle.write("PATH: "+ path +" | ERROR: "+ str(log) +"\n")
	filehandle.close()
	
if __name__=="__main__":

	main()
