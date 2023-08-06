# from colorama import Fore
# import datetime as dt
# from sty import fg, bg, ef, rs, Style, RgbFg

# class Log():
# 	def __init__(self, name:str, message:str, level:str, filenamewithlogtype:str=None, willprint:bool=True):
# 		self.message = message
# 		self.level = level.upper()
# 		self.name = name.upper()
# 		self.filename = filenamewithlogtype
# 		self.willprint = willprint
		
# 		if self.filename == 'default':
# 			today = dt.datetime.today()
# 			self.filename = f"{today.month:02d}-{today.day:02d}-{today.year}.log"
		
# 		elif self.filename != 'default' and self.filename != None:
# 			self.filename = filenamewithlogtype
		
# 		else:
# 			pass
		
# 		if self.level == 'CRITICAL' and self.willprint:
# 			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
# 			print(Fore.RED + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
			
# 		elif self.level == 'WARNING' and self.willprint:
# 			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
# 			# Red In Colorama print(Fore.RED + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
# 			fg.orange = Style(RgbFg(255, 150, 50))
# 			text = fg.orange + self.name + ' --> ' + self.level + ' --> ' + self.message + fg.rs
# 			print(text)
			
# 		elif self.level == 'ERROR' and self.willprint:
# 			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
# 			print(Fore.YELLOW + self.name + ' --> ' + self.level + ' --> ' + self.message + Fore.RESET)
			
# 		elif self.level == 'CRITICAL' and not self.willprint:
# 			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			
# 		elif self.level == 'WARNING' and not self.willprint:
# 			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			
# 		elif self.level == 'ERROR' and not self.willprint:
# 			append_file(self.filename, f'{self.name} --> {self.level} --> + {self.message}')
			
# 		#TODO Add More Logger Methods
	
# 	# The Following Lines Are For Testing
				
# 	#def print_attributes(self):
# 		#print(self.message)
# 		#print(self.level)
# 		#print(self.filename)
# 		#print(self.willprint)
