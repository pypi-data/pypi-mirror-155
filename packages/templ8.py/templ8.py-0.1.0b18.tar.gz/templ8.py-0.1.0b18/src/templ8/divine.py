import os
import shutil
import textile
from pathlib import Path
import templ8.programstate
from templ8.blessing import makedir
from templ8.blessing import mod_replaces
from templ8.blessing import parse_content
from templ8.blessing import into_html
from templ8.blessing import full_parse
import time

# Divines a website
def divine():
	# Load the state of the program (important files and stuff)
	state = templ8.programstate.ProgramState()
	last_change_list = {}
	if os.path.exists("chlist"):
		for i in open("chlist", "r").readlines():
			spl = i.split("<<")
			if len(spl) != 2:
				continue
			last_change_list[Path(spl[0])] = float(spl[1])
	
	finalprint = ""
	for subdir, dirs, files in os.walk(state.input_folder):
		# Copy all the folders in case they're not there yet
		for dir in dirs:
			path = os.path.join(subdir, dir).replace(state.input_folder, state.output_folder, 1)
			makedir(path)
		
		dir_replace = {}
		# Find a global repl8ce thing
		if "repl8ce" in files:
			path = os.path.join(subdir, "repl8ce")
			mod_replaces(dir_replace, open(path, "r").read())
		
		# Process the files
		for file in files:
			path = os.path.join(subdir, file)
			file_extension = os.path.splitext(path)[1]
			outpath = path.replace(state.input_folder, state.output_folder, 1)
			outhtml = outpath.replace(file_extension, ".html", -1)
			
			
			
			
			# Only process textile and md files
			if file_extension in [".textile", ".md"]:
				current_content = ""
				if os.path.exists(outhtml):
					current_content = open(outhtml, "r").read()
						
				
				with open(path, "r") as f:
					contents = ""
					# Get the headers and the content
					file_split = f.read().split("-BEGINFILE-",1)
					file_headers = ""
					file_content = ""
					if len(file_split) >= 2:
						file_headers = file_split[0]
						file_content = file_split[1]
					elif len(file_split) == 1:
						file_headers = ""
						file_content = file_split[0]
					else:
						raise Exception("Issue regarding -BEGINFILE- markers.")
					
					# Check if the folder is in txignore
					in_txignore = False
					for i in state.txignore:
						if os.path.join(state.input_folder, os.path.normpath(i)) == path or os.path.join(state.input_folder, os.path.normpath(i)) == subdir:
							in_txignore = True
							break
						  
					
					if not in_txignore:
						contents = full_parse(state, file_content, file_extension, file_headers, dir_replace)
						
						
						if os.path.exists(outhtml):
							contents = contents.replace("#!CDATE!#", time.ctime(os.path.getctime(outhtml)))
						else:
							contents = contents.replace("#!CDATE!#", time.ctime(time.time()))
						
						if contents == current_content:
							continue
						
						finalprint += outhtml + "\n"
						with open(outhtml, "w") as f:
							f.write(contents)
						
						
					else:
						finalprint += outpath + "\n"
						with open(outpath, "w") as f:
							f.write(file_content)
					
					
					
			else:
				if os.path.exists(outpath):
					if open(path, "rb").read() == open(outpath, "rb").read():
						continue
				finalprint += outpath + "\n"
				shutil.copy(path, outpath)
	
	print(finalprint)

	print("Finished assembling")