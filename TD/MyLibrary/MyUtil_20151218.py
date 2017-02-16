import os,xlrd
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
		if len(pbook.sheet_names())!= len(sbook.sheet_names()):
			error_flag = True
			error_info = error_info+ "tab name diff \n" 	
		else:		
			for i  in range(0, len(pbook.sheet_names())):
				psh = pbook.sheet_by_index(i)
				ssh = sbook.sheet_by_index(i) 
				minrows = min(psh.nrows, ssh.nrows)
				maxrows = max(psh.nrows, ssh.nrows)
				mincols = min(psh.ncols, ssh.ncols)		
				maxcols = max(psh.ncols, ssh.ncols)		
				if (psh.name == ssh.name and psh.nrows==ssh.nrows and psh.ncols==ssh.ncols):
					for t in range(0, psh.nrows):
						if (psh.row_values(t) != ssh.row_values(t) ):
							error_flag = True
							error_info = error_info+("\n diff---%r---row%d" %(psh.name,t+1))
							for p in range(0, psh.ncols):
								if (psh.cell(t,p).value != ssh.cell(t,p).value):
									error_info = error_info+("---col%d[%r,%r]" %(p+1,ssh.cell(t,p).value,psh.cell(t,p).value))					
				else:
					error_flag = True
					error_info = error_info+("diff ---  %r\ %r; ---- rows:\  %r\%r;---- cols:\  %r\%r.\n" %(ssh.name, psh.name ,ssh.nrows,psh.nrows,ssh.ncols,psh.ncols))			 
					for j in range(0, maxrows):
						if (j< minrows and psh.row_values(j) != ssh.row_values(j) ):
							error_info = error_info+("\n diff---%r\ %r---row%d" %(ssh.name,psh.name,j+1))
							for k in range(0, maxcols):
								if (k< mincols and psh.cell(j,k).value != ssh.cell(j,k).value):
									error_info = error_info+("---col%d[%r,%r]" %(k+1,ssh.cell(j,k).value,psh.cell(j,k).value))
								if (k>= mincols and psh.ncols == maxcols ):
									error_info = error_info+("---col%d[ ,%r]" %(k+1,psh.cell(j,k).value))
								if (k>= mincols and ssh.ncols == maxcols ):
									error_info = error_info+("---col%d[%r, ]" %(k+1,ssh.cell(j,k).value))
						if (j>= minrows and psh.nrows == maxrows ):
							error_info = error_info+("\n diff---%r---row%d is not in stage." %(psh.name,j+1))
						if (j>= minrows and ssh.nrows == maxrows ):
							error_info = error_info+("\n diff---%r---row%d is not in prod." %(ssh.name,j+1))	
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
							error_info = error_info+("\n Hidden Diff---%r---col%d" %(psh.name,ct+1))		
					for t in range(0, psh.nrows):
						if (psh.rowinfo_map[t].hidden != ssh.rowinfo_map[t].hidden):
							error_flag = True
							error_info = error_info+("\n Hidden Diff---%r---row%d" %(psh.name,t+1))						
						if (psh.row_values(t) != ssh.row_values(t) ):
							error_flag = True
							error_info = error_info+("\n diff---%r---row%d" %(psh.name,t+1))
							for p in range(0, psh.ncols):
								if (psh.cell(t,p).value != ssh.cell(t,p).value):
									error_info = error_info+("---col%d" %(p+1))					
				else:
					error_flag = True
					error_info = error_info+("diff ---  %r\ %r; ---- rows:\  %r\%r;---- cols:\  %r\%r.\n" %(psh.name, ssh.name ,psh.nrows,ssh.nrows,psh.ncols,ssh.ncols))			 
					for cj in range(0, minclos):
						if (psh.colinfo_map[cj].hidden != ssh.colinfo_map[cj].hidden):						
							error_info = error_info+("\n Hidden Diff---%r---col%d" %(psh.name,cj+1))
					for j in range(0, minrows):
						if (psh.rowinfo_map[j].hidden != ssh.rowinfo_map[j].hidden):
							error_info = error_info+("\n Hidden Diff---%r---row%d" %(psh.name,j+1))	
						if (psh.row_values(j) != ssh.row_values(j) ):
							error_info = error_info+("\n diff---%r---row%d" %(psh.name,j+1))
							for k in range(0, minclos):
								if (psh.cell(j,k).value != ssh.cell(j,k).value):
									error_info = error_info+("---col%d" %(k+1))
	if(error_flag):
		raise Exception, error_info
	else:	
		print  "Same excels!"	
		
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
