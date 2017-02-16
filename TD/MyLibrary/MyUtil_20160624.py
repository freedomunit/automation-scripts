import os,xlrd,xlwt,openpyxl
import math,string,time,sys,zipfile
from pyPdf import PdfFileReader

def findUploadErrorMessageFile(path,upload_type):
	current_time = time.time()
	print time.strftime("%Y-%m-%d %H:%M:%S"),upload_type
	temp_dirs = [rt for rt,dirs,files in os.walk(path)if abs(os.path.getmtime(rt) - current_time)<60 and os.path.abspath(rt) <> path] 
	target_file= "error"    	
	print temp_dirs
	if(len(temp_dirs)>0):
		for temp_path in temp_dirs:
			for temp_files in [files for rt,dirs,files in os.walk(temp_path)]:
				print temp_files
				t=[temp for temp in temp_files if (temp.count(".txt") >0 and temp.count("Warnings of "+upload_type.replace(" ",""))>0)]
				if(len(t)==1):
					target_file=temp_path+"\\"+ t[0]
				print t	
	print target_file					
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
		print  "Same excels!"		
		
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
	config_head= "userName,passwd,reciver_0,reciver_1,reciver_2,reciver_3,reciver_4,reciver_5,reciver_6,reciver_7,reciver_8,reciver_9,selectedReceiver,openStockCol,openStockRow,openStockNum,openStockX,openStockY,prepackTotalCol,prepackTotalRow,prepackTotalNum,prepackTotalX,prepackTotalY\n"	
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
		userInfo = userName+","+passwd+","+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+" ,"+editCell+"\n"
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