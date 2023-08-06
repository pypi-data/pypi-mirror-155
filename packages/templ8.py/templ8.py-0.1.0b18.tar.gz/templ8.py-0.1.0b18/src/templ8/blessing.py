import os
import textile
import pypandoc
import time

TEMPL8_ASCII = """
    ###                                                                 
    ###                                                               ###
    ###                                                               ###       #####
###########        ###                                                ###     ##    ###
###########     #########      ### ####    #####      ### ######      ###    ##      ###
    ###        ###     ###     ###################    ############    ###    ##     ####
    ###       ###       ###    ###    ####    ####    ###      ####   ###     ##   ####
    ###       #############    ###     ###     ###    ###       ###   ###      #######
    ###       #############    ###     ###     ###    ###      ####   ###    ####    ##
  #######     ###              ###     ###     ###    ############    ###   ####       ##
    ###       ####      ###    ###     ###     ###    ##########      ###   ###        ##
    ###         ##########     ###     ###     ###    ###             ###    ###     ###
    ##            ######       ###     ###     ###    ###             ###      ####### 
    ##                                                ###
    #"""
    
# Misnomer: This is the default blogbase
DEF_BASEHTML_CONTENT = """PAGETITLE=##TITLE##
-BEGINFILE-
h2. ##TITLE##

^##AUTHORS## - ##TAGS## - ##DATE##^

##CONTENT##

-BEGININDEX-
h2. "##TITLE##":##LINK##

^##AUTHORS## - ##TAGS## - ##DATE##^

##INTRO##
-BEGININDEX-
PAGETITLE=Blog"""

DEF_INPUT = "input"
DEF_OUTPUT = "output"
DEITY_PATH = "d8y"
DEF_BASEHTML_PATH = "basehtml"
DEF_REPLACE_PATH = "repl8ce"


# Checks if a directory exists and make it if not
def makedir(path, warning = ""):
	if not os.path.exists(path):
		if warning != "":
			print("WARNING: " + warning)
		os.mkdir(path)


# Processes the repl8ce of a header
def mod_replaces(input_replaces, header):
	# These variables are used for multiline keys
	current_multikey = "" # The current key being edited
	multiline = False
	
	for i in header.split("\n"):
		# Split it in the single line way
		keyval = [i]
		if not multiline:
			keyval = i.split("=", 1)
		# If we're not processing multilines, and the current line is single line, set key
		if len(keyval) == 2 and not multiline:
			input_replaces[keyval[0]] = keyval[1].replace(r"\n", "\n")
		# If it's not a valid single line
		elif len(keyval) == 1 and keyval[0] != "":
			# If it's a valid multiline, start a new multiline tag
			if keyval[0].startswith(";;"):
				multiline = True
				current_multikey = keyval[0].replace(";;", "", 1)
				input_replaces[current_multikey] = ""
			# If it's not, continue the current multiline
			elif multiline:
				input_replaces[current_multikey] += keyval[0] + "\n"
			else:
				raise Exception("what")


def parse_content(content, ext):
	if ext == ".textile":
		return textile.textile(content)
	elif ext == ".md":
		return pypandoc.convert_text(content, "html5", format="md")
	else:
		raise Exception("Can't recognize the extension in " + os.join(subdir, file))
		return ""

	
ifkey_start = "$$IF_"
ifnkey_start = "$$IF!"
forkey_start = "$$FOR_"
fkey_end = "$$END$$"


class Token:
	def __init__(self, end, type, text, start):
		self.end = end
		self.type = type
		self.text = text
		self.start = start
	def __repr__(self):
		return f"[ C: {self.start} - {self.end} T: {self.type} Tx: {self.text} ]"
	def __eq__(self, other):
		return (self.end == other.end and self.start == other.start)


def parts(input_base):
	start = 0
	tokens = {}
	ifk_find = input_base.find(ifkey_start, start)
	ifn_find = input_base.find(ifnkey_start, start)
	end_find = input_base.find(fkey_end, start)
	for_find = input_base.find(forkey_start, start)
	while ifk_find != -1 or end_find != -1 or for_find != -1:
		token_start = 0
		token_end = 0
		token_type = "void"
		top = len(input_base)
		for i in [ifk_find, end_find, for_find, ifn_find]:
			if i < top and i != -1:
				top = i
		if top == ifk_find:
			token_start = input_base.find(ifkey_start, start)
			token_end = input_base.find("$$", token_start + 1) + 2
			token_type = "IF"
		elif top == end_find:
			token_start = input_base.find(fkey_end, start)
			token_end = token_start + len(fkey_end)
			token_type = "END"
		elif top == for_find:
			token_start = input_base.find(forkey_start, start)
			token_end = input_base.find("$$", token_start + 1) + 2
			token_type = "FOR"
		elif top == ifn_find:
			token_start = input_base.find(ifnkey_start, start)
			token_end = input_base.find("$$", token_start + 1) + 2
			token_type = "IFN"
			
		tokens[token_start] = Token(token_end, token_type, input_base[token_start:token_end], token_start)
		start = token_end 
				
		
		ifk_find = input_base.find(ifkey_start, start)
		ifn_find = input_base.find(ifnkey_start, start)
		end_find = input_base.find(fkey_end, start)
		for_find = input_base.find(forkey_start, start)
	return tokens


def funkeys(input_base, keys, tokens):
	out = input_base
	tokpos = sorted(tokens.keys())
	index = 0
	for_deletion = []
	for_duplication = {}
	while True:
		if index >= len(tokpos):
			break
		ctoken = tokens[tokpos[index]]
		if tokpos[index+1] in tokens:
			ntoken = tokens[tokpos[index+1]]
			if ntoken.type == "END":
				if ctoken.type == "IF":
					if ctoken.text.find("%%") == -1:
						if_key = ctoken.text[len(ifkey_start):-2]
						if if_key in keys and keys[if_key] != "":
							for_deletion.append(ctoken)
							for_deletion.append(ntoken)
						else:
							for_deletion.append(Token(ntoken.end, "CONTENT", "aaa", tokpos[index]))
					
					tokpos.pop(index)
					tokpos.pop(index)
					index -= 1
				elif ctoken.type == "IFN":
					if ctoken.text.find("%%") == -1:
						if_key = ctoken.text[len(ifkey_start):-2]
						if not if_key in keys or keys[if_key] == "":
							for_deletion.append(ctoken)
							for_deletion.append(ntoken)
						else:
							for_deletion.append(Token(ntoken.end, "CONTENT", "aaa", tokpos[index]))
					
					tokpos.pop(index)
					tokpos.pop(index)
					index -= 1
				elif ctoken.type == "FOR":
					for_key = ctoken.text[len(forkey_start):-2]
					n = 0
					while True:
						if for_key + str(n) in keys:
							if n == 0:
								for_deletion.append(ctoken)
								for_deletion.append(ntoken)
							if not ctoken.start in for_duplication:
								for_duplication[ctoken.start] = [Token(ntoken.start-1, "CONTENT", "aaa", ctoken.end), 0]
							for_duplication[ctoken.start][1] += 1
							n += 1
						else:
							if n == 0:
								for_deletion.append(Token(ntoken.end, "CONTENT", "aaa", tokpos[index]))
							break
					
					tokpos.pop(index)
					tokpos.pop(index)
					index -= 1
			else:
				index += 1
		if index >= len(tokpos) - 1:
			break
	
	delbars = []
	if len(for_deletion) > 0:
		delclumps = [for_deletion[0]]
		
		old_delclumps = for_deletion
		while True:
			index = 0
			for tk in old_delclumps:
				ntk_start = tk.start
				ntk_end = tk.end
				if delclumps[index].start >= ntk_start and delclumps[index].end <= ntk_end:
					delclumps[index].start = ntk_start
					delclumps[index].end = ntk_end
				else:
					delclumps.append(Token(ntk_end, "CONTENT", "AAA", ntk_start))
					index += 1
			if old_delclumps == delclumps:
				break
			else:
				old_delclumps = delclumps
				delclumps = [old_delclumps[0]]
				
		for tk in delclumps:
			start = tk.start
			end = tk.end
			for i in delbars:
				if start > i[0]:
					start -= i[1]
				if end > i[0]:
					end -= i[1]
			out = out[:start] + out[end:]
			delbars.append([start, end - start])
	
	if len(for_duplication) > 0:
		for tk in for_duplication:
			start = for_duplication[tk][0].start
			end = for_duplication[tk][0].end
			for i in delbars:
				if start > i[0]:
					start -= i[1]
				if end > i[0]:
					end -= i[1]
			beginning = out[:start]
			content = out[start:end]
			ending = out[end:]
			out = beginning
			for i in range(for_duplication[tk][1]):
				out += content.replace("%%", f"{i}")
			delbars.append([start, -len(content)*(for_duplication[tk][1]-1)])
			out += ending
	
	return out
	

def into_html(content, keys, state):
	# By default, use the default base
	base = state.basehtml_content
	# Use a custombase if it's specified
	if "CUSTOMBASE" in keys:
		if os.path.exists(keys["CUSTOMBASE"]):
			base = open(keys["CUSTOMBASE"], "r").read()
		else:
			raise Exception(os.path.join(subdir, file) + " uses a CUSTOMBASE that doesn't exist")
	
	# Tokenize for function keys and apply them
	tokens = parts(base)
	if len(tokens) != 0:
		base = funkeys(base, keys, tokens)
	tokens = parts(base)
	if len(tokens) != 0:
		base = funkeys(base, keys, tokens)
		
	# Put the content in the file
	base = base.replace("##CONTENT##", content)
	
	# Replace special keys
	base = base.replace("#!DATE!#", time.ctime(time.time()))
	
	return base


def full_parse(state, file_content, file_extension, file_headers, dir_replace):
	# Process repl8ce
	filerepl = state.replacements.copy()
	for i in dir_replace:
		filerepl[i] = dir_replace[i]
	mod_replaces(filerepl, file_headers)
	
	# Turn the content into HTML
	contents = parse_content(file_content, file_extension)
	
	# Put the content in the base HTML
	contents = into_html(contents, filerepl, state)
	
	# Put the keys there
	for key in filerepl:
		if key.startswith("TX-"):
			contents = contents.replace("##"+key+"##", parse_content(filerepl[key], ".textile"))
		elif key.startswith("MD-"):
			contents = contents.replace("##"+key+"##", parse_content(filerepl[key], ".md"))
		else:
			contents = contents.replace("##"+key+"##", filerepl[key])
	
	return contents


def parse_keys(page, keys):
	base = page
	tokens = parts(base)
	if len(tokens) != 0:
		base = funkeys(base, keys, tokens)
	tokens = parts(base)
	if len(tokens) != 0:
		base = funkeys(base, keys, tokens)
	
	for key in keys:
		if key.startswith("TX-"):
			base = base.replace("##"+key+"##", parse_content(keys[key], ".textile"))
		elif key.startswith("MD-"):
			base = base.replace("##"+key+"##", parse_content(keys[key], ".md"))
		else:
			base = base.replace("##"+key+"##", keys[key])
	
	return base