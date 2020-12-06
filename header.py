# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    header.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: flegg <flegg@student.21-school.ru>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/09 19:45:26 by flegg             #+#    #+#              #
#    Updated: 2020/12/06 19:57:04 by flegg            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
from datetime import datetime
max_fname_len = 0

def spaced_str(s:str, max_len:int) -> str:
	sp_int = int(max_len - len(s))
	if sp_int < 0:
		sp_int = 0
	sp_str = sp_int * ' '
	return (s + sp_str)

def get_header(info:list) -> list:
	# info = {'filename', 'username', 'mail', 'created' (datetime), 'creator', 'updated'(datetime), 'updater'}
	max_str = 40
	
	header = ['/* ************************************************************************** */\n',
			'/*                                                                            */\n',
			'/*                                                        :::      ::::::::   */\n']
	header.append('/*   ' + spaced_str(info['filename'], max_str) + '           :+:      :+:    :+:   */\n')
	header.append('/*                                                    +:+ +:+         +:+     */\n')
	header.append('/*   ' + spaced_str('By: ' + info['username'] + ' <' + info['mail'] + '>', max_str) + '       +#+  +:+       +#+        */\n')
	header.append('/*                                                +#+#+#+#+#+   +#+           */\n')
	header.append('/*   Created: ' + spaced_str(info['created'].strftime("%Y/%m/%d %H:%M:%S") + ' by ' + info['creator'], max_str) + ' #+#    #+#             */\n')
	header.append('/*   Updated: ' + spaced_str(info['updated'].strftime("%Y/%m/%d %H:%M:%S") + ' by ' + info['updater'], max_str) + '###   ########.fr       */\n')
	header.append('/*                                                                            */\n')
	header.append('/* ************************************************************************** */\n')
	
	return header
	
# IMPORTANT: it is NOT a validation function, it just checks that "it seems like 42 Header"
# Return int - probability of 42 header
# If line is static (0, 1, 2, 4, 6, 9, 10) and fully correct -> ADD 2 to score
# If line is dynamic ADD 1 for len==81 and ADD 1 for correct ending and begining

MAXPOINTS = 11*2 # 11 rows in header * 2 points

def header_probability(lines:list) -> int:
	score = 0
	
	if len(lines) < 11:
		return 0
	
	if lines[0] == '/* ************************************************************************** */\n':
		score += 2
	if lines[1] == '/*                                                                            */\n':
		score += 2
	if lines[2] == '/*                                                        :::      ::::::::   */\n':
		score += 2
	
	if lines[3][:5] == '/*   ' and lines[3][-25:] == ':+:      :+:    :+:   */\n':
		score += 1
	if len(lines[3]) == 81:
		score += 1
	
	if lines[4] == '/*                                                    +:+ +:+         +:+     */\n':
		score += 2
	
	if lines[5][:9] == '/*   By: ' and lines[5][-29:] == '+#+  +:+       +#+        */\n':
		score += 1
	if len(lines[5]) == 81:
		score += 1
	
	if lines[6] == '/*                                                +#+#+#+#+#+   +#+           */\n':
		score += 2
		
	if lines[7][:14] == '/*   Created: ' and lines[7][-26:] == '#+#    #+#             */\n':
		score += 1
	if len(lines[7]) == 81:
		score += 1
		
	if lines[8][:14] == '/*   Updated: ' and lines[8][-27:] == '###   ########.fr       */\n':
		score += 1
	if len(lines[8]) == 81:
		score += 1
		
	if lines[9] == '/*                                                                            */\n':
		score += 2
	if lines[10]== '/* ************************************************************************** */\n':
		score += 2
		
	return score

def is_there_42header(lines:list, percent:int) -> bool:
	global MAXPOINTS
	if header_probability(lines) >= MAXPOINTS/100*percent: #11 rows * 2 points
			return True
	else:
			return False
	
def get_header_info(lines:list) -> list:
	res = {}
	res['filename'] = lines[3].split()[1]
	res['username'] = lines[5].split()[2]
	res['mail'] = lines[5].split()[3][1:-1]
	res['created'] = datetime.strptime(lines[7].split()[2] + ' ' + lines[7].split()[3], "%Y/%m/%d %H:%M:%S")
	res['creator'] = lines[7].split()[5]
	res['updated'] = datetime.strptime(lines[8].split()[2] + ' ' + lines[8].split()[3], "%Y/%m/%d %H:%M:%S")
	res['updater'] = lines[8].split()[5]
	return res
	

def file_proc(filename:str, username:str, percent:int, path:str=''):
	mail = 'marvin@42.fr'
	with open(path + filename, 'r') as f:
		global max_fname_len
		print(spaced_str(filename + ' ', max_fname_len + 1), end='')
		lines = f.readlines()
		
		file_mod_timestamp = os.path.getmtime(filename)
		dt_file_mod = datetime.fromtimestamp(file_mod_timestamp)
		
		if is_there_42header(lines, percent):
			print('[H+]  ', end='')
			info = get_header_info(lines)
			
			if info['filename'] != filename:
				info['filename'] = filename
				print('[File] ', end='')
				
			if info['username'] != username:
				info['username'] = username
				print('[By] ', end='')
			
			if info['mail'] != mail:
				info['mail'] = mail
				print('[@] ', end='')
				
			if info['updated'].date() < dt_file_mod.date() or \
				(info['updated'].date() == dt_file_mod.date() and \
				info['updated'].time() < dt_file_mod.time()):
				
				info['updated'] = dt_file_mod
				print('[UpdTime] ', end='')
				info['updater'] = username
				print('[UpdName] ', end='')
			
			#check that User was creator or updater!
			if info['updater'] != username and info['creator'] != username:
				print('What is', username, 'doing here?', end='')
			
			header = get_header(info)
			for i in range(0, 11):
				lines[i] = header[i]
		else:
			print('[Header not found!] Creating new...', end='')
			info = {}
			info['filename'] = filename
			info['username'] = username
			info['mail'] = mail
			info['created'] = dt_file_mod
			info['creator'] = username
			info['updated'] = dt_file_mod
			info['updater'] = username
			
			if not lines[0].isspace():
				lines.insert(0, '\n')
			
			header = get_header(info)
			for i in range(10, -1, -1):
				lines.insert(0, header[i])
		f.close()
		with open(path + filename, 'w') as f:
			f.writelines(lines)
			f.close()
		print()
		
def file_proc_remove(filename:str, percent:int, path:str=''):
	with open(path + filename, 'r') as f:
		global max_fname_len
		print(spaced_str(filename + ' ', max_fname_len + 1), end='')
		lines = f.readlines()
		
		if is_there_42header(lines, percent):
			print('[Header found!] Deleting...', end='')
			for i in range(0, 11):
				lines.pop(0)
		else:
			print('[Header NOT found!]', end='')
		
		while lines[0].isspace():
			lines.pop(0)
		f.close()
		
		with open(path + filename, 'w') as f:
			f.writelines(lines)
			f.close()
		print()
		

# Input template:
# FILES_PATH
# [upd, del] username
# file1 file2 file3 [\]
# file4... (expecting .c and .h files for now)
# (filetype doesn't matter for algorithm, but it's checking
# and writing in C-style syntax)

with open('hinfo', 'r') as f:
	valid_task_list = ['upd', 'del']
	# ignoreheader - I don't care if there's 42 header (>= 0% prob)
	# minimumcheck - at least all static lines correct (>= 60% prob)
	# fewmistakes - do not check len() of 4 (>= 80% prob)
	# full (default) - 100% (Header tests do not guarantee 100% correct header!!!)
	valid_percent_list = {'ignoreheader': 0, 'minimumcheck': 60, 'fewmistakes': 80, 'full': 100}
	percent = valid_percent_list['full']
	
	path = f.readline()[:-1]
	if len(path) == 0:
		raise ValueError('path length == 0')
	args = f.readline()
	args = args.split()
	
	# check for additional args
	i = 2
	while i < len(args):
		if args[i] in valid_percent_list:
			percent = valid_percent_list[args[i]]
			print('flag =', args[i], 'found. Error percent set to', percent)
		i += 1
	
	flist = f.read().split()
	f.close()
	i = 0
	while i < len(flist):
		if flist[i] == '\\':
			flist.pop(i)
			i -= 1
		i += 1
	
	# added before checking args to avoid asking user for username when no files found
	if len(flist) < 1:
		print("No files found!")
		sys.exit()
	
	if len(args) < 2:
		if len(args) == 1 and args[0] in valid_task_list:
			print("You seem to have forgotten the username. You can enter it now:")
			args.append(input())
			if args[1] == '':
				raise ValueError('second line args count is not 2')
		else:
			raise ValueError('second line args count is not 2')
	if args[0] not in valid_task_list:
		raise ValueError('incorrect first arg in second line args', args[0])
	if not args[1].isalnum():
		raise ValueError('username seems incorrect (not alphanumeric)', args[1])
	
	for i in flist:
		if len(i) > max_fname_len:
			max_fname_len = len(i)
	
	i = 0
	if args[0] == 'upd':
		while i < len(flist):
			file_proc(flist[i], args[1], percent)
			i += 1
		
	elif args[0] == 'del':
		while i < len(flist):
			file_proc_remove(flist[i], percent)
			i += 1

