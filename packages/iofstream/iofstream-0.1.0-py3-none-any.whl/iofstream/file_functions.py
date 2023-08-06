# def write_file(filename:str, text:str, newline:bool = True):
# 	try:	
# 		with open(filename, 'w') as f:
# 			if newline == True:
# 				f.writelines(text)
# 			else:
# 				f.write(text)
# 	except Exception as e:
# 		print(e)
		
# def append_file(filename:str, text:str, newline:bool=True):
# 	try:
# 		if newline == True:
# 			with open(filename, 'a') as f:
# 				f.writelines('\n')
# 				f.writelines(text)
# 		elif newline == False:
# 			with open(filename, 'a') as f:
# 				f.writelines(text)
# 	except Exception as e:
# 		print(e)
		
# def clear_file(filename:str):
# 	try:
# 		with open(filename, 'w') as f:
# 			f.writelines('')
# 	except Exception as e:
# 		print(e)
		
# def create_file(filename:str):
# 	try:
# 		with open(filename, 'x') as f:
# 			return True
# 	except Exception as e:
# 		print(e)
# def write_and_read_file(filename:str, text:str='', seek_number:int=0):
# 	try:
# 		with open(filename, 'w+') as f:
# 			f.writelines(text)
# 			f.seek(seek_number)
# 			listLines = f.readlines()
# 			lines = listLines[0]
# 			return lines
# 	except Exception as e:
# 		print(e)
		
# def read_and_write_file(filename:str, text:str=''):
# 	try:
# 		with open(filename, 'w+') as f:
# 			f.writelines(text)
# 			lines = f.readlines()
# 			return lines
# 	except Exception as e:
# 		print(e)