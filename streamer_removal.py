#!/usr/bin/env python3 -tt
#-*- coding: UTF-8 -*- 
"""
Remove all instances (Folders and links) of streamerdata malware. 
"""
import re
import os
import shutil

def main():
	print("[*] REMOVING ALL INSTANCES OF STREAMER.") 
	dir_path = os.path.dirname(os.path.realpath(__file__))
	#print(dir_path)
	devour_streamer(dir_path)


def devour_streamer(path):
	"Find and destroy streamer malware"
	
	evil = b'\x73\x00\x74\x00\x61\x00\x72\x00\x74\x00\x20\x00\x73\x00\x74\x00\x72\x00\x65\x00\x61\x00\x6D\x00\x65\x00\x72\x00\x64' \
		+ b'\x00\x61\x00\x74\x00\x61\x00\x5C\x00\x73\x00\x74\x00\x72\x00\x65\x00\x61\x00\x6D\x00\x65\x00\x72\x00\x2E\x00\x65\x00' \
		 + b'\x78\x00\x65\x00\x20\x00\x2F\x00\x41\x00\x75\x00\x74\x00\x6F\x00\x49\x00\x74\x00\x33\x00\x45\x00\x78\x00\x65\x00\x63' \
		 + b'\x00\x75\x00\x74\x00\x65\x00\x53\x00\x63\x00\x72\x00\x69\x00\x70\x00\x74\x00\x20\x00\x22\x00\x73\x00\x74\x00\x72\x00' \
		 + b'\x65\x00\x61\x00\x6D\x00\x65\x00\x72\x00\x64\x00\x61\x00\x74\x00\x61\x00\x5C\x00\x73\x00\x74\x00\x72\x00\x65\x00\x61' \
		 + b'\x00\x6D\x00\x2E\x00\x74\x00\x78\x00\x74\x00\x22'
	
	#print(evil.decode('utf-8'))

	for path, listofdirs, listoffiles in os.walk(path):
		#print("[*] Current Directory is :",path)
		#print("			has directories:",listofdirs)
		#print("			has files:",listoffiles)
				
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
					print(e)
		

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
	
	return
	
	
def devour_prey(path, file=False):
	"DELETE FOUND FOLDERS OR FILES"
		
	filehandle = open('kraken.log','a')
	

	if file == False:
		try:
			shutil.rmtree(path, ignore_errors=False, onerror=None)
			result = "SUCCESS"
		except Exception as e:
			result = "ERROR"
			filehandle.write("Folder: "+ path +" | Error: "+ str(e))
	else:
		try:
			os.remove(path)
			result = "SUCCESS"
		except Exception as e:
			result = "ERROR"
			filehandle.write("File: "+ path +" | Error: "+ str(e))
	
	filehandle.close()
	return result
	
if __name__=="__main__":

	main()
