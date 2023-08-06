def write_file(filename:str, text:str, newline:bool = True):
	try:	
		with open(filename, 'w') as f:
			if newline == True:
				f.writelines(text)
			else:
				f.write(text)
	except Exception as e:
		print(e)
		
def append_file(filename:str, text:str, newline:bool=True):
	try:
		if newline == True:
			with open(filename, 'a') as f:
				f.writelines('\n')
				f.writelines(text)
		elif newline == False:
			with open(filename, 'a') as f:
				f.writelines(text)
	except Exception as e:
		print(e)
		
def clear_file(filename:str):
	try:
		with open(filename, 'w') as f:
			f.writelines('')
	except Exception as e:
		print(e)
		
def create_file(filename:str):
	try:
		with open(filename, 'x') as f:
			return True
	except Exception as e:
		print(e)
def write_and_read_file(filename:str, text:str='', seek_number:int=0, unlist:bool=True):
	try:
		with open(filename, 'w+') as f:
			f.writelines(text)
			f.seek(seek_number)
			if unlist == True:
				listLines = f.readlines()
				lines = listLines[0]
			else:
				lines = f.readlines()
		return lines
	except Exception as e:
		print(e)
		
def read_and_write_file(filename:str, text:str='', unlist:bool=True):
	try:
		with open(filename, 'r+') as f:
			if unlist == True:
				listLines = f.readlines()
				lines = listLines[0]
			else:
				lines = f.readlines()
			f.writelines(text)	
		return lines
	except Exception as e:
		print(e)
  
def read_file(filename:str, start_number:int=0, unlist:bool=True):
	try:
		with open(filename, 'r') as f:
			f.seek(start_number)
			if unlist == True:
				listLines = f.readlines()
				lines = listLines[0]
			else:
				lines = f.readlines()
		return lines
	except Exception as e:
		print(e)

##############################################################################LOGGER##############################################################################
  
from colorama import Fore
import datetime as dt
from sty import fg, bg, ef, rs, Style, RgbFg

class Log():
	def __init__(self, name:str, message:str, level:str, filenamewithlogtype:str=None, willprint:bool=True):
		self.message = message
		self.level = level.upper()
		self.name = name.upper()
		self.filename = filenamewithlogtype
		self.willprint = willprint
		
		if self.filename == 'default':
			today = dt.datetime.today()
			self.filename = f"{today.month:02d}-{today.day:02d}-{today.year}.log"
		
		elif self.filename != 'default' and self.filename != None:
			self.filename = filenamewithlogtype
		
		else:
			pass
		
		if self.level == 'CRITICAL' and self.willprint:
			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			print(Fore.RED + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
			
		elif self.level == 'WARNING' and self.willprint:
			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			# Red In Colorama print(Fore.RED + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
			fg.orange = Style(RgbFg(255, 150, 50))
			text = fg.orange + self.name + ' --> ' + self.level + ' --> ' + self.message + fg.rs
			print(text)
			
		elif self.level == 'ERROR' and self.willprint:
			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			print(Fore.YELLOW + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
			
		elif self.level == 'CRITICAL' and not self.willprint:
			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			
		elif self.level == 'WARNING' and not self.willprint:
			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			
		elif self.level == 'ERROR' and not self.willprint:
			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			
		#TODO Add More Logger Methods
	
	# The Following Lines Are For Testing
				
	#def print_attributes(self):
		#print(self.message)
		#print(self.level)
		#print(self.filename)
		#print(self.willprint)

class Logger():
	def __init__(self:str, name:str):
		self.name = name.upper()

	def send_error(self, message:str, filename:str, willprint:bool=True):
		self.message = message
		self.filename = filename
		self.willprint = willprint
		append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
		if willprint == True:
			print(Fore.YELLOW + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
		else:
			pass

	def send_warning(self, message:str, filename:str, willprint:bool=True):
		self.message = message
		self.filename = filename
		self.willprint = willprint
		append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
		if willprint == True:
			# Red In Colorama print(Fore.RED + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
			fg.orange = Style(RgbFg(255, 150, 50))
			text = fg.orange + self.name + ' --> ' + self.level + ' --> ' + self.message + fg.rs
			print(text)
		else:
			pass

	def send_critical(self, message:str, filename:str, willprint:bool=True):
		self.message = message
		self.filename = filename
		self.willprint = willprint
		append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
		if self.willprint == True:
			print(Fore.RED + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
		else:
			pass

		