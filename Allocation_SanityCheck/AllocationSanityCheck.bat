@echo off
d:
del ..\..\..\Robot\Allocation_SanityCheck\output\*.* /q
del ..\..\..\Robot\Allocation_SanityCheck\prod_download\*.* /q
del ..\..\..\Robot\Allocation_SanityCheck\diff\*.html /q
del ..\..\..\Robot\Allocation_SanityCheck\diff\*.txt /q
call PybotAllocationSanityCheck.bat
set backupDir=D:\Robot\Allocation_SanityCheck\%date:~6,4%%date:~0,2%%date:~3,2%\output
set backupDir1=D:\Robot\Allocation_SanityCheck\%date:~6,4%%date:~0,2%%date:~3,2%\prod_download
md %backupDir%
md %backupDir1%
xcopy D:\Robot\Allocation_SanityCheck\output %backupDir% /S
xcopy D:\Robot\Allocation_SanityCheck\prod_download %backupDir1% /S

