#!/usr/bin/env python3 -tt
#-*- coding: UTF-8 -*-
"""
RELASE THE KRAKEN!!!
If you release the kraken, it will find and destroy any folder or files you want to eliminate. 
10/16/2018
"""
import sys
import argparse
import os
import re
import time
import shutil

try:
	input = raw_input
except:
	pass


def main():
	"Release the KRAKEN"
	parser=argparse.ArgumentParser(description='Remove Files or Folders. (e.g. kraken -path "C:\Program Files" -F "some folder" OR kraken -path "C:\Program Files" -LF "folders.txt")')
	parser.add_argument('--path',required=True,help='Directory path where to start looking. Use quotes (e.g. "C:\Program Files\folder")',dest='path')
	parser.add_argument('--folder',required=False,help='Folder name to search and destroy',dest='folder')
	parser.add_argument('--file',required=False,help='File name to search and destroy',dest='file')
	parser.add_argument('--listfolders',required=False,help='Text file with a list of folders to search and destroy',dest='list_of_folders')
	parser.add_argument('--listfiles',required=False,help='Text file with a list of files to search and destriy',dest='list_of_files')
	parser.add_argument('--force',required=False,help='Don\'t ask for confirmation. Just search and destroy',dest='force',default=False, action='store_true')
	args=parser.parse_args()
	
	print(args) 
	print("\n				-------  THE KRAKEN   --------- \n")

	if not os.path.isdir(args.path):
		print("Folder location (" + args.path + ") does not exist. ")
		print("Use Kraken --help for more information on how to use this program")
		quit()
		
	elif args.folder != None:
		#print("looking for a folder")
		
		if args.force != False:
			find_folder_force(args.path, args.folder)
		else:
			find_folder(args.path, args.folder)
		
		quit()
		
	elif args.file != None:
		#print("looking for a file")
		find_file(args.path, args.file)
		quit()
		
	elif args.list_of_folders != None:
		#print("looking for a list of folders")
		find_folder_list(args.path, args.list_of_folders)
		quit()
		
	elif args.list_of_files != None:
		#print("looking for a list of files")
		find_file_list(args.path, args.list_of_files)
		quit()
		
	else:
		print("You need to tell the kraken what to search and destroy!!")
	
		
##### END OF MAIN - ALL FUNCTIONS BELOW  ######
	
def find_folder(path, name):
	"This will search for the name of a folder"
	
	print("[+] Kraken will look for all instances of (" + name + ") inside the folder (" + path + ") and delete all findings.\n")
	choise = query_yes_no("Do you want to continue?")
	prey_found = []
	#print(choise)
	
	if choise:
		#print("You chouse yes! "+ str(choise))		
		# List one at a time
		print("[*] The Kraken is looking for prey.\n")
		for path, listofdirs, listoffiles in os.walk(path):
			#print("[*] Current Directory is :",path)
			#print("			has directories:",listofdirs)
			#print("			has files:",listoffiles)
			prey=name.lower()
			location=path.lower()
			
			find = re.compile('\\\(%s)$' % prey)
			found = find.findall(location)
			
			if found:
				prey_found.append(path)
			else:
				continue
		
		if prey_found:
			print("[*] The Kraken found prey!!")
			for x in prey_found:
				print("--> " + x)
			
			release = query_yes_no("\nALL THIS FOLDERS WILL BE DELETED!! ARE YOU SURE YOU WANT TO CONTINUE?: ")
			if release:
				print("\n!!! RLEASE THE KRAKEN !!!\n")
				for folder in prey_found:
					print("[*] Deleting ("+ folder +") .....", end="", flush=True)
					result = devour_prey(folder)
					print("["+result+"]")
				
			else:
				print("\nKraken goes back to his cave.... ")
				quit()
				
			
		else:
			print("[*] The Kraken didn't find any folders with that name")
			
			
	else:
		print("\nKraken goes back to his cave.... ")
		quit()
	
	return

def find_folder_force(path, name):
	"This will search for the name of a folder, then delete all. No questions asked"
	print("[+] Kraken is looking for all instances of (" + name + ") inside the folder (" + path + ") and will delete all findings. (NO QUESTIONS ASKED!!)\n")
	prey_found = []
	
	print("\n!!! RLEASE THE KRAKEN !!!\n")
	for path, listofdirs, listoffiles in os.walk(path):
		#print("[*] Current Directory is :",path)
		#print("			has directories:",listofdirs)
		#print("			has files:",listoffiles)
		prey=name.lower()
		location=path.lower()
			
		find = re.compile('\\\(%s)$' % prey)
		found = find.findall(location)
			
		if found:
			prey_found.append(path)
			print("[*] Deleting ("+ path +") .....", end="", flush=True)
			result = devour_prey(path)
			print("["+result+"]")
		else:
			continue
		
	if prey_found:
		print("[*] All the prey has been devour!!")
	else:
		print("[*] The Kraken didn't find any folders with that name")		
	
def devour_prey(path):
	"DELETE FOUND FOLDERS"
		
	filehandle = open('kraken.log','a')
		
	try:
		shutil.rmtree(path, ignore_errors=False, onerror=None)
		result = "SUCCESS"
	except Exception as e:
		result = "ERROR"
		filehandle.write("Folder: "+ path +" | Error: "+ str(e))
	
	
	filehandle.close()
	return result

	
def find_folder_list(path, list_of_folders):
	"This will search for a list of folders and delete them all"
	
	print("Delete list of folders function not yet implemented")
	return
	
def find_file(path, name):
	"This will search for a file and delete if"
	
	print("Delete file function not yet implemented")
	return
	
def find_file_list(path, list_of_files):
	"This will search for a list of files and delete them all"
	
	print("Delete list of files function not yet implemented")
	return
	
def query_yes_no(question, default="no"):

	valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
	
	if default is None:
		prompt = " [y/n]: " 
	elif default == "yes":
		prompt = " [Y/n]: "
	elif default == "no":
		prompt = " [y/N]: "
	else:
		raise ValueError("Invalid default answer: '%s'" % default)
	
	while True:
		sys.stdout.write(question + prompt)
		choice = input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
	else:
			sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

if __name__=="__main__":

	main()
