@echo off
d:
del ..\..\..\robot\Allocation\output\*.* /q
del ..\..\..\robot\Allocation\prod_download\*.* /q
del ..\..\..\robot\Allocation\stage_download\*.* /q
del ..\..\..\robot\Allocation\diff\*.html /q
del ..\..\..\robot\Allocation\diff\*.txt /q
::call AllocationCPCompare.bat
::call AllocationBPCompare.bat
call AllocationSBCompare.bat
::call AllocationAMCompare.bat
::call AllocationDTCompare.bat
::call AllocationOBCompare.bat
::call AllocationOBSingleCompare.bat