# -*- coding: utf-8 -*- 

import os,xlrd,xlwt,openpyxl,paramiko,types
import math,string,time,sys,zipfile
from pyPdf import PdfFileReader
from scp import SCPClient

def findUploadErrorMessageFile(path,upload_type):
	current_time = time.time()
#	print time.strftime("%Y-%m-%d %H:%M:%S"),upload_type
#	print path
	temp_dirs = [rt for rt,dirs,files in os.walk(path)if abs(os.path.getmtime(rt) - current_time)<60 and os.path.abspath(rt) <> path] 
	target_file= ""    	
#	print temp_dirs
	if(len(temp_dirs)>0):
		for temp_path in temp_dirs:
			for temp_files in [files for rt,dirs,files in os.walk(temp_path)]:
#				print temp_files
				t=[temp for temp in temp_files if (temp.count(".txt") >0 and (temp.count("Warnings of "+upload_type.replace(" ",""))>0 or temp.count("Error of "+upload_type.replace(" ",""))>0))]
				if(len(t)==1):
					target_file=temp_path+"\\"+ t[0]
				elif(len(t)>1):
					zipFile=[tmp for tmp in temp_files if (tmp.count(".zip") >0)]
					zipName=zipFile[0].strip('\n').replace('.zip','')
					msgFile=[tmp for tmp in temp_files if (tmp.count(zipName) >0 and tmp.count(".txt") >0)]
					target_file=temp_path+"\\"+ msgFile[0].strip('\n')
#				target_file=msgFile[0].strip('\n')
#				print t	
#	print target_file	
	else:
		raise Exception, "get Error File Fail!"
	if(len(target_file) >0):
		return target_file
	else:
		print "No Error/Warning File!"	
	return target_file
	
def findUploadErrorDataFile(path,upload_type):
	current_time = time.time()
	temp_dirs = [rt for rt,dirs,files in os.walk(path)if abs(os.path.getmtime(rt) - current_time)<60 and os.path.abspath(rt) <> path] 
	target_file= ""    	
	if(len(temp_dirs)>0):
		for temp_path in temp_dirs:
			for temp_files in [files for rt,dirs,files in os.walk(temp_path)]:
				t=[temp for temp in temp_files if (temp.count("Error data")>0)]
				if(len(t)>0):
					target_file=temp_path+"\\"+ t[0]
	else:
		raise Exception, "get Error Data File Fail!"
	if(len(target_file) >0):
		return target_file
	else:
		print "No Error Data File!"	
	return target_file	
	
def findUploadSourceFile(path,upload_type,sourceUploadFile):
	current_time = time.time()
	temp_dirs = [rt for rt,dirs,files in os.walk(path)if abs(os.path.getmtime(rt) - current_time)<60 and os.path.abspath(rt) <> path] 
	target_file= ""    	
	if(len(temp_dirs)>0):
		for temp_path in temp_dirs:
			for temp_files in [files for rt,dirs,files in os.walk(temp_path)]:
				t=[temp for temp in temp_files if (temp.count(sourceUploadFile)>0)]
				if(len(t)>0):
					target_file=temp_path+"\\"+ t[0]
	else:
		raise Exception, "get Source Upload File Fail!"
	if(len(target_file) >0):
		return target_file
	else:
		print "No Source Upload File!"	
	return target_file		
	
def findLastFile(prod_path,prod_time):
	print prod_path
	print os.walk(prod_path)
	files = map(lambda t : prod_path+"\\"+t,[pfiles for rt,dirs,pfiles in os.walk(prod_path)][0]);
	prod_files = [f for f in files if os.path.getmtime(f)-prod_time >=0]	
	print prod_files
	if len(prod_files)==1:
		return prod_files[0]
	else:
		raise Exception, "Do not find!"			
		
def getLinuxUploadErrorMessageFile(linux_ip, linux_user,linux_passwd,local_dir,test_user,upload_type):
	Host = linux_ip
	user = linux_user
	passwd = linux_passwd
	port =22
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(Host,port,user, passwd)
	(stdin, stdout, stderr) = ssh.exec_command("find /usr/local/7thonline/7thOnline/data/temp -name *"+test_user+"* -mmin -1 -type d")
	dir = stdout.readlines();
	remotepath=''
	target_file=''
#	print dir
	for dir_tmp in dir:
		(stdin, stdout, stderr) = ssh.exec_command("ls "+dir_tmp.strip('\n'))
		file_tmp = stdout.readlines();
#		print file_tmp
		file = [tmp for tmp in file_tmp if (tmp.count(".txt") >0 and (tmp.count("Warnings of "+upload_type.replace(" ",""))>0 or tmp.count("Error of "+upload_type.replace(" ",""))>0))]
		if(len(file)==1):
			remotepath=dir_tmp.strip('\n')+"/"+ file[0].strip('\n')
			target_file=file[0].strip('\n')
		elif(len(file)>1):
			zipFile=[temp for temp in file_tmp if (temp.count(".zip") >0)]
			zipName=zipFile[0].strip('\n').replace('.zip','')
			msgFile=[temp for temp in file_tmp if (temp.count(zipName) >0 and temp.count(".txt") >0)]
			remotepath=dir_tmp.strip('\n')+"/"+ msgFile[0].strip('\n')
			target_file=msgFile[0].strip('\n')
	if (len(remotepath)>0):
		scpclient = SCPClient(ssh.get_transport(), socket_timeout=15.0)
		localpath=local_dir+target_file
		scpclient.get(remotepath, localpath)  
		ssh.close()
		return localpath
	elif (len(dir) >0):
		ssh.close()
		print "No Error/Warning File!"	
	else:
		ssh.close()
		raise Exception, "get Error File Fail!"			
		
def getLinuxUploadErrorDataFile(linux_ip, linux_user,linux_passwd,local_dir,test_user,upload_type):
	Host = linux_ip
	user = linux_user
	passwd = linux_passwd
	port =22
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(Host,port,user, passwd)
	(stdin, stdout, stderr) = ssh.exec_command("find /usr/local/7thonline/7thOnline/data/temp -name *"+test_user+"* -mmin -1 -type d")
	dir = stdout.readlines();
	remotepath=''
	target_file=''
	for dir_tmp in dir:
		(stdin, stdout, stderr) = ssh.exec_command("ls "+dir_tmp.strip('\n'))
		file_tmp = stdout.readlines();
		file = [tmp for tmp in file_tmp if (tmp.count("Error data")>0)]
		if(len(file)>0):
			remotepath=dir_tmp.strip('\n')+"/"+ file[0].strip('\n')
			target_file=file[0].strip('\n')
	if (len(remotepath)>0):
		scpclient = SCPClient(ssh.get_transport(), socket_timeout=15.0)
		localpath=local_dir+target_file
		scpclient.get(remotepath, localpath)  
		ssh.close()
		return localpath
	elif (len(dir) >0):
		ssh.close()
		print "No Error Data File!"	
	else:
		ssh.close()
		raise Exception, "get Error Data File Fail!"		

def getLinuxUploadSourceFile(linux_ip, linux_user,linux_passwd,local_dir,test_user,upload_type, sourceUploadFile):
	Host = linux_ip
	user = linux_user
	passwd = linux_passwd
	port =22
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(Host,port,user, passwd)
	(stdin, stdout, stderr) = ssh.exec_command("find /usr/local/7thonline/7thOnline/data/temp -name *"+test_user+"* -mmin -1 -type d")
	dir = stdout.readlines();
	remotepath=''
	target_file=''
	for dir_tmp in dir:
		(stdin, stdout, stderr) = ssh.exec_command("ls "+dir_tmp.strip('\n'))
		file_tmp = stdout.readlines();
		file = [tmp for tmp in file_tmp if (tmp.count(sourceUploadFile)>0)]
		if(len(file)>0):
			remotepath=dir_tmp.strip('\n')+"/"+ file[0].strip('\n')
			target_file=file[0].strip('\n')
	if (len(remotepath)>0):
		scpclient = SCPClient(ssh.get_transport(), socket_timeout=15.0)
		localpath=local_dir+target_file
		scpclient.get(remotepath, localpath)  
		ssh.close()
		return localpath
	elif (len(dir) >0):
		ssh.close()
		print "No Source Upload File!"	
	else:
		ssh.close()
		raise Exception, "get Source Upload File Fail!"			
		
def compareXLSX(prodf,stagef,diff_dir):	
	error_flag = False
	dir = diff_dir.replace(".xlsx",".txt")
	error_info=""
	if(prodf == None or stagef == None ):
		error_flag = True
		error_info="Report isn't generated!"
	elif (prodf.find("xlsx") == -1 or stagef.find("xlsx") == -1 ) :
		error_flag = True
		error_info="Report isn't XLSX!"
	else:		
		pbook= openpyxl.load_workbook(prodf)
		sbook= openpyxl.load_workbook(stagef)	
		if (len(pbook.get_sheet_names()) != len(sbook.get_sheet_names()) ):
			error_flag = True
			error_info = error_info+ "tabs count diff \n" 	
		else:	
			for i  in range(0,len(sbook.get_sheet_names())):
				psh = pbook.worksheets[i]
				ssh = sbook.worksheets[i] 		
				maxrows = max(psh.max_row, ssh.max_row)			
				maxcols = max(psh.max_column, ssh.max_column)		
				if (psh.title == ssh.title):
					for j in range(1, maxrows+1):	
						row_diffCount = 0
						for k in range(1, maxcols+1):	
							if (psh.cell(row=j, column=k).value != ssh.cell(row=j, column=k).value ):
								error_flag = True
								row_diffCount +=1
								if(row_diffCount == 1):
									error_info = error_info+("\n diff---%s---row%d" %(psh.title,j))
								error_info = error_info+("---col%d[%s,%s]" %(k,ssh.cell(row=j, column=k).value,psh.cell(row=j, column=k).value ))
				else:
					error_flag = True
					error_info = error_info+("diff ---  %s\ %s; ---- rows:\  %s\%s;---- cols:\  %s\%s.\n" %(ssh.title, psh.title ,ssh.max_row,psh.max_row,ssh.max_column,psh.max_column))			 
					for m in range(1, maxrows+1):		
						row_diffCount = 0
						for n in range(1, maxcols+1):	
							if (psh.cell(row=m, column=n).value != ssh.cell(row=m, column=n).value ):
								row_diffCount +=1;
								if(row_diffCount == 1):
									error_info = error_info+("\n diff---row%d" %(m))
								error_info = error_info+("---col%d[%s,%s]" %(n,ssh.cell(row=m, column=n).value ,psh.cell(row=m, column=n).value))		
	if(error_flag):
		diff_file = open(dir,"w")
		diff_file.write(error_info)	
		diff_file.close()
		raise Exception, "Excels are diff or not generated!"
	else:	
		print  "Same excels!"	

def copyZKVisibleXLSX(source_excel):
	new_excel = source_excel.replace('.xlsx','_visible.xlsx',1)
	source =  openpyxl.load_workbook(source_excel)
	new = openpyxl.Workbook(encoding='utf-8')
	newTabsCount=0
	for i in range(0, len(source.get_sheet_names())):
		if(source.worksheets[i].title.find("_template") > 0):
			continue
		else:
			s_sheet= source.worksheets[i]			
			n_sheet = new.create_sheet(index=newTabsCount, title=source.worksheets[i].title)			
			colsCount=1
			for j in range(1,s_sheet.max_column + 1):	
				col_title = openpyxl.cell.get_column_letter(j)
				if(s_sheet.column_dimensions[col_title].hidden):
					continue
				for k in range(1,s_sheet.max_row + 1):
					n_cell = ("%s%d" %(openpyxl.cell.get_column_letter(colsCount),k))
					s_cell = ("%s%d" %(col_title,k))
					n_sheet.cell(n_cell).value = s_sheet.cell(s_cell).value				
				colsCount+=1
			newTabsCount+=1
	new.save(new_excel)		
	return new_excel
		
def copyVisibleXLSX(source_excel,new_excel,tabs):
	tabNames = tabs.split(",")
	source =  openpyxl.load_workbook(source_excel)
	new = openpyxl.Workbook(encoding='utf-8')
	for i in range(0,len(tabNames)):
		s_sheet= source.get_sheet_by_name(tabNames[i])
		if (s_sheet):
			n_sheet = new.create_sheet(index=i, title=tabNames[i])			
	#		cinfo_map=s_sheet.colinfo_map
			colsCount=1
			for j in range(1,s_sheet.max_column + 1):	
				col_title = openpyxl.cell.get_column_letter(j)
				if(s_sheet.column_dimensions[col_title].hidden):
					continue
				for k in range(1,s_sheet.max_row + 1):
					n_cell = ("%s%d" %(openpyxl.cell.get_column_letter(colsCount),k))
					s_cell = ("%s%d" %(col_title,k))
					n_sheet.cell(n_cell).value = s_sheet.cell(s_cell).value
				#	print("%s[row%d,col%d]" %(tabNames[i],k,colsCount))	
				colsCount+=1
	#	print("%s[row%d,col%d]--%d" %(tabNames[i],k,colsCount,j))			
	new.save(new_excel)
		
def copyVisibleXLS(source_excel,new_excel,tabs):
	tabNames = tabs.split(",")
	source = xlrd.open_workbook(source_excel)
	new = xlwt.Workbook(encoding='utf-8')
	for i in range(0,len(tabNames)):
		s_sheet= source.sheet_by_name(tabNames[i])
		if (s_sheet):
			n_sheet = new.add_sheet(tabNames[i])
			cinfo_map=s_sheet.colinfo_map
			colsCount=0
			for j in range(0,s_sheet.ncols):	
				
				if(cinfo_map.get(j,0) and cinfo_map[j].hidden == 1):
					continue
				for k in range(0,len(s_sheet.col_values(j))):
					n_sheet.write(k,colsCount,s_sheet.cell(k,j).value)
					print("%s[row%d,col%d]" %(tabNames[i],k,colsCount))	
				colsCount+=1
	new.save(new_excel)
		
		
def compareExcel(pf,sf,diff_dir):	
	error_flag = False
	dir = diff_dir.replace(".xlsx","_download_ws_diff.txt").replace(".xls","_download_ws_diff.txt")
	error_info=""
	if(pf == None or sf == None):
		error_flag = True
		error_info="Report isn't generated!"
	else:		
		pbook=xlrd.open_workbook(pf)
		sbook=xlrd.open_workbook(sf)	
		if len(pbook.sheet_names())!= len(sbook.sheet_names() ):
			error_flag = True
			error_info = error_info+ "tabs count or name diff \n" 	
		else:	
		#	print("tabCount(%d,%d)" %(len(pbook.sheet_names()),len(sbook.sheet_names())));
			for i  in range(0, len(pbook.sheet_names())):
				psh = pbook.sheet_by_index(i)
				ssh = sbook.sheet_by_index(i) 
				minrows = min(psh.nrows, ssh.nrows)
				maxrows = max(psh.nrows, ssh.nrows)
			#	mincols = min(psh.ncols, ssh.ncols)		
			#	maxcols = max(psh.ncols, ssh.ncols)		
				if (psh.name == ssh.name and psh.nrows==ssh.nrows and psh.ncols==ssh.ncols):
				#	print("tabName:%s,rows(%d,%d),cols(%d,%d)" %(psh.name,psh.nrows,ssh.nrows,psh.ncols,ssh.ncols));
					for t in range(0, psh.nrows):						
						if (psh.row_values(t) != ssh.row_values(t) ):
					#		print("tabName:%s,rows(%d,%d),cols(%d,%d)" %(psh.name,t,t,len(psh.row_values(t)),len(ssh.row_values(t))));
					#		print("tabName:%s,rows(%d,%d),ncols(%d,%d)" %(psh.name,t,t,psh.ncols,ssh.ncols));
							error_flag = True
							error_info = error_info+("\n diff---%s---row%d" %(psh.name,t+1))
							if(len(psh.row_values(t)) == len(ssh.row_values(t))):
								for p in range(0, len(psh.row_values(t))):
							#		print("cell(%d,%d)" %(t,p));
									if (psh.cell(t,p).value != ssh.cell(t,p).value):
										error_info = error_info+("---col%d[%s,%s]" %(p+1,ssh.cell(t,p).value,psh.cell(t,p).value))
							else:
								for p in range(0, max(len(psh.row_values(t)),len(ssh.row_values(t)))):
							#		print("cell(%d,%d)" %(t,p));
									if (p < min(len(psh.row_values(t)),len(ssh.row_values(t))) and psh.cell(t,p).value != ssh.cell(t,p).value):
										error_info = error_info+("---col%d[%s,%s]" %(p+1,ssh.cell(t,p).value,psh.cell(t,p).value))
									if (p >= min(len(psh.row_values(t)),len(ssh.row_values(t))) and len(psh.row_values(t)) > len(ssh.row_values(t))):
										error_info = error_info+("---col%d[ ,%s]" %(p+1,psh.cell(t,p).value))
									if (p>= min(len(psh.row_values(t)),len(ssh.row_values(t))) and len(psh.row_values(t)) < len(ssh.row_values(t))):
										error_info = error_info+("---col%d[%s, ]" %(p+1,ssh.cell(t,p).value))
				else:
					error_flag = True
					error_info = error_info+("diff ---  %s\ %s; ---- rows:\  %s\%s;---- cols:\  %s\%s.\n" %(ssh.name, psh.name ,ssh.nrows,psh.nrows,ssh.ncols,psh.ncols))			 
					for j in range(0, maxrows):
						if (j< minrows and psh.row_values(j) != ssh.row_values(j) ):
							error_info = error_info+("\n diff---%s\ %s---row%d" %(ssh.name,psh.name,j+1))
							for k in range(0, max(len(psh.row_values(j)),len(ssh.row_values(j)))):
								if (k< min(len(psh.row_values(j)),len(ssh.row_values(j))) and psh.cell(j,k).value != ssh.cell(j,k).value):
									error_info = error_info+("---col%d[%s,%s]" %(k+1,ssh.cell(j,k).value,psh.cell(j,k).value))
								if (k>= min(len(psh.row_values(j)),len(ssh.row_values(j))) and len(psh.row_values(j)) > len(ssh.row_values(j)) ):
									error_info = error_info+("---col%d[ ,%s]" %(k+1,psh.cell(j,k).value))
								if (k>= min(len(psh.row_values(j)),len(ssh.row_values(j))) and len(psh.row_values(j)) < len(ssh.row_values(j))  ):
									error_info = error_info+("---col%d[%s, ]" %(k+1,ssh.cell(j,k).value))
						if (j>= minrows and psh.nrows == maxrows ):
							error_info = error_info+("\n diff---%s---row%d is not in stage." %(psh.name,j+1))
						if (j>= minrows and ssh.nrows == maxrows ):
							error_info = error_info+("\n diff---%s---row%d is not in prod." %(ssh.name,j+1))	
	if(error_flag):
		diff_file = open(dir,"w")
		diff_file.write(error_info)	
		diff_file.close()
		raise Exception, "Excels are diff or not generated!"
	else:	
		return  "Same excels!"		
		
def getEnvironmentSetting(fpath,tabName):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	env= [sheet.cell(0,1).value]
	env.append(sheet.cell(1,1).value)
	return env			
	
def getUsersCount(fpath,tabName):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	count = sheet.nrows-3
	return count		
	
def getUserCriteria(fpath,tabName,user_number,startCol):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (user_number >= (sheet.nrows-3) or user_number < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:		
		criteria = sheet.row_values(user_number+3)	
		del criteria[0:int(startCol)]		
		return [criteria for criteria in criteria if criteria.strip() != ""]
	#	return criteria
		
def getUser(fpath,tabName,user_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (user_number >= (sheet.nrows-3) or user_number < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:		
		return sheet.cell(user_number+3,0).value
		
def getCompanyInfo(fpath,tabName,user_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (user_number >= (sheet.nrows-3) or user_number < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:	
		info= [str(sheet.cell(user_number+3,1).value)]
		info.append(str(sheet.cell(user_number+3,2).value))
		return info		
	
def getYears(fpath,tabName,user_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (user_number >= (sheet.nrows-3) or user_number < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:	
		year= str(sheet.cell(user_number+3,6).value).replace(".0","").split(",")		
		return year
		
def getMonths(fpath,tabName,user_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (user_number >= (sheet.nrows-3) or user_number < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:	
		month= str(sheet.cell(user_number+3,7).value).replace(".0","").split(",")		
		return month	
	
def getDownloadType(fpath,tabName,user_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (user_number >= (sheet.nrows-3) or user_number < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:	
		return sheet.cell(user_number+3,3).value	
		
def getDownloadOption(fpath,tabName,user_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (user_number >= (sheet.nrows-3) or user_number < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:	
		return sheet.cell(user_number+3,4).value			
		
def getCellValues(fpath,tabName,user_number,col_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (int(user_number) >= (sheet.nrows-3) or int(user_number) < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:	
		return str(sheet.cell(int(user_number)+3,int(col_number)).value).strip().split(",")
		
def getCellValuesListByRowCol(fpath,tabName,row_number,col_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (int(row_number) < 1 or int(col_number) < 1):
		raise Exception, error_message+"cell does not existing in sheet!" 	
	else:	
		return str(sheet.cell(int(row_number)-1,int(col_number)-1).value).strip().split(",")	

def getCellValueByRowCol(fpath,tabName,row_number,col_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (int(row_number) < 1 or int(col_number) < 1):
		raise Exception, error_message+"cell does not existing in sheet!" 	
	else:	
		return str(sheet.cell(int(row_number)-1,int(col_number)-1).value).strip()			
		
def getWSIDList(WSID_string, replace_str):
	WSid = WSID_string.replace(replace_str,"").split(",")
	return [WSid for WSid in WSid if WSid.strip()!=""]	
	
def getListSize(options):
	return len(str(options).split(","))

def diffText(stage_text,prod_text):
	if(stage_text == prod_text):
		return False		
	else:
		return True 
		
def comparePDF(pf,sf):	
	reload(sys)
	sys.setdefaultencoding( "UTF-8" )
	error_flag = False
	error_info=""	
	if(pf == None and sf == None):
		print "Prod and Stage WS PDF DON'T EXIST!"
	elif(pf != None and sf == None):	
		error_flag = True
		error_info = error_info+"Stage WS PDF DOESN'T EXIST!"
	elif(pf == None and sf != None):	
		error_flag = True
		error_info = error_info+ "Prod WS PDF DOESN'T EXIST!"	
	else:
		pPdf = PdfFileReader(file(pf, "rb")) 	
		sPdf = PdfFileReader(file(sf, "rb"))
		if (pPdf.getNumPages() != sPdf.getNumPages()):
			error_flag = True
			error_info = error_info+("Diff WS PDF Page Numbers! ---stage pages: %d---prod pages: %d \n"  % (sPdf.getNumPages(),pPdf.getNumPages()))
		else:
			for p in range (0, sPdf.getNumPages()):
				ptext = pPdf.getPage(p).extractText()
				stext = sPdf.getPage(p).extractText()
				ptag = ptext[ptext.find("[")+1 : ptext.find("]")]
				stag = stext[stext.find("[")+1 : stext.find("]")]				
				ptag1 = ptext[ptext.find("Createdby")-23 : ptext.find("Createdby")]
				stag1 = stext[stext.find("Createdby")-23 : stext.find("Createdby")]				
				ptxt = ptext.replace(ptag,"").replace(ptag1,"")		
				stxt = stext.replace(stag,"").replace(stag1,"")
				if (ptxt != stxt):
					error_flag = True
					error_info = error_info+("Diff WS PDF Page %d! \n"  % (p+1))			
	if (error_flag):
		raise Exception, error_info
	else:
		print  "Same WS PDF!"	
		
def extractZIP(pf,path,prefix):	
	z = zipfile.ZipFile(pf, 'r') 
	fileNameList = ""
	for f in z.namelist():
		fileName = path +prefix+ f
		output = open(fileName, 'wb')
		output.write(z.read(f))
		output.close()
		if(len(fileNameList) == 0):
			fileNameList= fileName
		else:
			fileNameList=fileNameList + "," +fileName		
	return	fileNameList
	
def compareExcelWithXls(pf,sf):	
	error_flag = False
	error_info=""
	if(pf == None or sf == None):
		error_flag = True
		error_info="Report isn't generated!"
	else:		
		pbook=xlrd.open_workbook(pf,formatting_info=True)
		sbook=xlrd.open_workbook(sf,formatting_info=True)	
		if len(pbook.sheet_names())!= len(sbook.sheet_names()):
			error_flag = True
			error_info = error_info+ "tab name diff \n" 	
		else:		
			for i  in range(0, len(pbook.sheet_names())):
				psh = pbook.sheet_by_index(i)
				ssh = sbook.sheet_by_index(i) 
				minrows = min(psh.nrows, ssh.nrows)
				minclos = min(psh.ncols, ssh.ncols)			
				if (psh.name == ssh.name and psh.nrows==ssh.nrows and psh.ncols==ssh.ncols):
					for ct in range(0, psh.ncols):
						if (psh.colinfo_map[ct].hidden != ssh.colinfo_map[ct].hidden):
							error_flag = True
							error_info = error_info+("\n Hidden Diff---%s---col%d" %(psh.name,ct+1))		
					for t in range(0, psh.nrows):
						if (psh.rowinfo_map[t].hidden != ssh.rowinfo_map[t].hidden):
							error_flag = True
							error_info = error_info+("\n Hidden Diff---%s---row%d" %(psh.name,t+1))						
						if (psh.row_values(t) != ssh.row_values(t) ):
							error_flag = True
							error_info = error_info+("\n diff---%s---row%d" %(psh.name,t+1))
							for p in range(0, psh.ncols):
								if (psh.cell(t,p).value != ssh.cell(t,p).value):
									error_info = error_info+("---col%d" %(p+1))					
				else:
					error_flag = True
					error_info = error_info+("diff ---  %s\ %s; ---- rows:\  %s\%s;---- cols:\  %s\%s.\n" %(psh.name, ssh.name ,psh.nrows,ssh.nrows,psh.ncols,ssh.ncols))			 
					for cj in range(0, minclos):
						if (psh.colinfo_map[cj].hidden != ssh.colinfo_map[cj].hidden):						
							error_info = error_info+("\n Hidden Diff---%s---col%d" %(psh.name,cj+1))
					for j in range(0, minrows):
						if (psh.rowinfo_map[j].hidden != ssh.rowinfo_map[j].hidden):
							error_info = error_info+("\n Hidden Diff---%s---row%d" %(psh.name,j+1))	
						if (psh.row_values(j) != ssh.row_values(j) ):
							error_info = error_info+("\n diff---%s---row%d" %(psh.name,j+1))
							for k in range(0, minclos):
								if (psh.cell(j,k).value != ssh.cell(j,k).value):
									error_info = error_info+("---col%d" %(k+1))
	if(error_flag):
		raise Exception, error_info
	else:	
		print  "Same excels!"	
		
def getCellValue(fpath,tabName,user_number,col_number):
	book=xlrd.open_workbook(fpath)
	sheet=book.sheet_by_name(tabName)
	if (int(user_number) >= (sheet.nrows-3) or int(user_number) < 0):
		raise Exception, error_message+"user does not existing!" 	
	else:	
		return sheet.cell(int(user_number)+3,int(col_number)).value
		
def writeZKLoadTestingParamForDT(userName, passwd, receiver, editCell, file_dir):
	reload(sys)
	sys.setdefaultencoding( "UTF-8" )
	dir= file_dir.replace("/", " ")
	config_head= "userName,passwd,reciver_0,reciver_0_Y,reciver_1,reciver_1_Y,reciver_2,reciver_2_Y,reciver_3,reciver_3_Y,reciver_4,reciver_4_Y,reciver_5,reciver_5_Y,reciver_6,reciver_6_Y,reciver_7,reciver_7_Y,reciver_8,reciver_8_Y,reciver_9,reciver_9_Y,selectedReceiver,openStockCol,openStockRow,openStockNum,openStockX,openStockY,prepackTotalCol,prepackTotalRow,prepackTotalNum,prepackTotalX,prepackTotalY\n"	
	config_file = open(dir,"a+")
	config_data = config_file.read();	
	if(len(receiver)> 0):
		userInfo = userName+","+passwd+","
		receiverList = receiver.split(";")
		for i in range(0,10):
			if(i < len(receiverList)):
				userInfo+=receiverList[i]+","
			else:	
				userInfo+=" ,"
		userInfo+=editCell+"\n"		
	else:
		userInfo = userName+","+passwd+","+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+","+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+editCell+"\n"
	if(len(config_data)==0):
		config_file.write(config_head)	
	config_file.seek(0,2)	
	config_file.write(userInfo)	
	config_file.close()
	
def writeZKLoadTestingParamForTransfer(userName, passwd, title, styleCount, editBtnRowInfo, modifyRow, addDoorRowInfo, fromDoorInfo, toDoorInfo, fromDoorSize, file_dir):
	reload(sys)
	sys.setdefaultencoding( "UTF-8" )
	dir= file_dir.replace("/", " ")
	config_head= title+"\n"	
	config_file = open(dir,"a+")
	config_data = config_file.read();	
	if(len(fromDoorInfo)> 0):
		userInfo = userName+","+passwd+","+styleCount+","+editBtnRowInfo+","+addDoorRowInfo+","+fromDoorInfo+","+toDoorInfo+","+modifyRow+","+fromDoorSize+"\n"			
	if(len(config_data)==0):
		config_file.write(config_head)	
	config_file.seek(0,2)	
	config_file.write(userInfo)	
	config_file.close()	
	
def saveDBQueryDataToFile(filePath, data, fileType='', delimete=''):
	os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
	reload(sys)
	sys.setdefaultencoding( "UTF-8" )
	if (delimete) :
		config_file = open(filePath,"a+")
		config_data = config_file.read();	
		for row in data:		
			config_file.seek(0,2)	
			for item in row:
				if (item == None):	
					item = ''
				config_file.write(str(item)+delimete)	
			config_file.write('\n')	
		config_file.close()	
	else:
		w = xlwt.Workbook()
		ws = w.add_sheet('Sheet1')
		for row_num in range (0,len(data)):
			row = list(data[row_num])
			for col_num in range (0,len(row)):
				if type(row[col_num]) is types.StringType :
					row[col_num]=row[col_num].decode('utf-8')
				if (row[col_num] != None):	
					ws.write(row_num,col_num, row[col_num])
		w.save(filePath)		
	
def comprareStringToSortByAscending (str1, str2):
	strList=[str1,str2]
	strList.sort()
	if(str1 == strList[0]):
		flag = True
	else:
		flag = False
	return flag

	
if __name__ == "__main__":	
	findUploadErrorMessageFile()
	compareExcel()
	findLastFile()
	getEnvironmentsetting()
	getUsersCount()
	getUserCriteria()
	getUser()
	getCompanyInfo()
	getYears()
	getMonths()
	getDownloadType()	
	getDownloadOption()
	getWSIDList()
	diffText()
	comparePDF()
	getCellValues()
	getListSize()
	extractZIP()
	compareExcelWithXls()
	getCellValue()
	copyVisibleXLS()
	copyVisibleXLSX()
	compareXLSX()
	copyZKVisibleXLSX()
	writeZKLoadTestingParamForDT()
	writeZKLoadTestingParamForTransfer()
	comprareStringToSortByAscending()
	getLinuxUploadErrorMessageFile()
	getCellValuesListByRowCol()
	getCellValueByRowCol()
	saveDBQueryDataToFile()
	getLinuxUploadErrorDataFile()
	findUploadErrorDataFile()
	getLinuxUploadSourceFile()
	findUploadSourceFile()