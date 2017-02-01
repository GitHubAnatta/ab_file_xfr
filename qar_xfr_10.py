

#==============================================================================
# # -*- coding: utf-8 -*-
# """
# Created on Wed Jun 01 17:05:07 2016
# 
# @author: anatta
# """
# 
#==============================================================================
import sys
import logging
import win32api

#==============================================================================
# read pcmcia card label windows api
#==============================================================================
card_label = win32api.GetVolumeInformation("H:\\")

#==============================================================================
# who is transferring the files
#==============================================================================
name = raw_input("Please enter your name.")
print 'Hi ', name, 'Please go ahead and transfer files - Press Enter'


#==============================================================================
# Save the current stream
#==============================================================================
save_out = sys.stdout

# Define the log file

f = "QAR_card_data_xfr.log"

#==============================================================================
# Change 'a' to 'w' to recreate the log file each time.
# Change 'a' to 'a' to to append existing log file.
#==============================================================================
fsock = open(f, 'a')

# Set stream to file

sys.stdout = fsock

###
# do something here 
# any print function will send the stream to file f
###


# Required module
import os
import shutil
import datetime

#####
logging.getLogger('').handlers = [] ##clear handler##
logging.basicConfig(filename='D://xfr/qar_xfr_10_current/QAR_XFR_run.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running QAR Card Data Transfer")
###


now = datetime.datetime.now()
print"_________________________________________________________________________"
print"_________________________________________________________________________"
print 'File Transferred by:' , name, 'Aviation Safety Cargolux'
print 'PCMCIA Card Lable: ', card_label
print 'QAR Data Transfer Log File created on:', now.strftime("%Y-%m-%d %H:%M")


#==============================================================================
# Function for getting files from a folder
#==============================================================================
def fetchFiles(pathToFolder, flag, keyWord):
#==============================================================================
# fetchFiles() requires three arguments: pathToFolder, flag and keyWord flag. 
# 'ENDS_WITH' keyWord is a string to search the file's name.
# The keyWord is case sensitive and must be exact.  
# Example: fetchFiles('H://','ENDS_WITH','.FLD'). Returns: _pathToFiles and _fileNames
#==============================================================================
	
	_pathToFiles = []
	_fileNames = []

	for dirPath, dirNames, fileNames in os.walk(pathToFolder):
		if flag == 'ENDS_WITH':
			selectedPath = [os.path.join(dirPath,item) for item in fileNames if item.endswith(keyWord)]
			_pathToFiles.extend(selectedPath)
			
			selectedFile = [item for item in fileNames if item.endswith(keyWord)]
			_fileNames.extend(selectedFile)

#==============================================================================
# 		elif flag == 'STARTS_WITH':
# 			selectedPath = [os.path.join(dirPath,item) for item in fileNames if item.startswith(keyWord)]
# 			_pathToFiles.extend(selectedPath)
# 			
# 			selectedFile = [item for item in fileNames if item.startswith(keyWord)]
# 			_fileNames.extend(selectedFile) 
#==============================================================================
			    
		else:
			print fetchFiles.__doc__
			break
						
		# Try to remove empty entries if none of the required files are in directory
		try:
			_pathToFiles.remove('')
			_imageFiles.remove('')
		except ValueError:
			pass
			
		
#==============================================================================
#             Warn if nothing was found in the given path
# 		if selectedFile == []: 
# 			print 'No files with given parameters were found in:\n', dirPath, '\n'
#                 
#                 print len(_fileNames), 'files were found is searched folder(s)' 
#       		
#        
#         return _pathToFiles, _fileNames
#         print _pathToFiles, _fileNames
#==============================================================================
       
        str1 = ' '.join(_pathToFiles [0]) #convert tuple element 0 to string
        str2 = str1.replace(" ", "") #remove white spaces
        global str3

        str3 = str2[13:16] #extract registration
        str4 = 'FLDAT'
        
        str5 = str3.__add__(str4)
        
        str6 = 'H://'
       
        global str7
        str7 = str6.__add__(str5)
       
            
        
        print 'Number of .FLD files found on the card:', len(_fileNames)
        print
fetchFiles('H://','ENDS_WITH','.FLD')

sourcePath = str7
str8 = 'LX-'
str9 = str8.__add__(str3)
print 'Aircraft registration: ', str9


str10 = '//aerobytesprod/AerobytesLoad/'

str11 = str10.__add__(str9)

print 'Source path is: ', sourcePath
print
destPath = str11
print 'Destination path is: ', destPath
print

for root, dirs, files in os.walk(sourcePath):

#==============================================================================
#     figure out where we're going
#==============================================================================
    dest = destPath + root.replace(sourcePath, '')

#==============================================================================
#     if we're in a directory that doesn't exist in the destination folder
#     then create a new folder
#==============================================================================
    if not os.path.isdir(dest):
        os.mkdir(dest)
        print 'Destination Directory created at:' + dest
    else:
        print 'Destination Directory already exists:' + dest
        print

for root, dirs, files in os.walk(sourcePath):
#==============================================================================
#   figure out where we're going
#==============================================================================
    dest = destPath + root.replace(sourcePath, '')
    filetype = '.FLD'# name the file ext to be copied    
    print 'All files of this type' , filetype, 'will be copied to destination directory.'
    print"_________________________________________________________________________"
#==============================================================================
#     loop through all files in the directory
#==============================================================================
    for f in files:

        #compute current (old) & new file locations
        oldLoc = root + '\\' + f
        newLoc = dest + '\\' + f


        if not os.path.isfile(newLoc):
            try:
                filename, file_ext = os.path.splitext(oldLoc)
                print 'filename is:', filename
   
                if file_ext == filetype:
                    statinfo = os.stat(oldLoc)
                    shutil.copy2(oldLoc, newLoc)
                    print 'File ' + f + ' copied.'
                    print 'size: ', statinfo.st_size
                    print
                else:
                    print 'File ' + f + ' not copied'
            except IOError:
                print 'file "' + f + '" already exists'

#==============================================================================
# #==============================================================================
# # Reset back the stream to what it was
# #==============================================================================
# sys.stdout = save_out
# fsock.close()
# 
#==============================================================================
#==============================================================================
# compare files
#==============================================================================
from filecmp import dircmp

def main():
    dcmp = dircmp(sourcePath, destPath)
    if diffs_found(dcmp):
        print "CAREFUL CHECK AGAIN DIFFS FOUND!"
        print
    else:
        print "NO DIFFS FOUND"
        print


def diffs_found(dcmp):
    if len(dcmp.left_only) > 0:
        print dcmp.report_full_closure()
        return True
    elif len(dcmp.right_only) > 0:
        print dcmp.report_full_closure()
        return True
    else:
        for sub_dcmp in dcmp.subdirs.values():
            if diffs_found(sub_dcmp):
                return True
    return False

if __name__ == '__main__':
    main()
#==============================================================================
# delete files
#the statements do not show up in the console, but recorded in log.
#==============================================================================
import shutil


filelist = [ f for f in os.listdir(r"H:\\")]
#file_list = 0
if not filelist:
    print "There were no files/Folders to delete"
    print 'Deleted number of files = :', 0
file_count = 0
for f in filelist:
    if f:
        f= os.path.join(r"H:\\", f)
        file_count = file_count+1

print file_count, "root files & folders will be deleted"
raw_input('Press Enter to delete files')
raw_input('Are you sure?  If so Press Enter again o delete all files')
shutil.rmtree(r'H:\\', ignore_errors=True)
print "It is done!.  Wish you a nice day"
#==============================================================================
# Reset back the stream to what it was
#==============================================================================
sys.stdout = save_out
fsock.close()

    