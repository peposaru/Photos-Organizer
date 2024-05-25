# Title: Photos Organization
# Description: This program is for organizing all my photos into Year -> Month

import PIL.Image,time
import os, datetime, re, calendar, shutil
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS


class FolderManager:
    # Check if this is a valid directory / give stats of directory
    def __init__(self,inputDir):
        self.inputDir = inputDir

    def dirValid(self,inputDir):
        if os.path.exists(inputDir) is True:
            os.chdir(inputDir)
            return True
        elif os.path.exists(inputDir) is False:
            return False

    # Give stats for the directory
    def dirStats(self,inputDir):
        allFiles  = 0
        valFile   = 0
        invalFile = 0


        for subdir, dirs, files in os.walk(inputDir):
            for file in files:
                allFiles += 1
                try: 
                    Image.open(os.path.join(subdir, file))
                    valFile += 1
                except:
                    invalFile += 1
        print (
f"""
VALID FILES                        : {valFile}
INVALID FILES                      : {invalFile}
TOTAL FILES                        : {allFiles}
""")

# Make the month / year directories
class DirectoryManager:
    def __init__(self,inputDir):
        self.inputDir = inputDir
    def validFilesOrg(self,inputDir):
        validFilesList   = []

        for subdir, dirs, files in os.walk(inputDir):
            for file in files:
                try: 
                    Image.open(os.path.join(subdir, file))
                    validFilesList += [(os.path.join(subdir, file))]
                except:
                    pass
        return validFilesList
    def processingFolder(self,inputDir):
        try:
            os.makedirs('Output Folder')
        except:
            pass
        return
    def dateExtractor(self,file):
        dateRegex = re.compile(r"([1-2][0-9][0-9][0-9]):([0-1][0-9]):([0-3][0-9])")
        try:
            image      = Image.open(file)
            exifData   = image.getexif()
            dateExif   = exifData[306]

            # Read the exif taken date data
            mo         = dateRegex.search(dateExif)
            yearDate   = mo.group(1)
            monthDate  = mo.group(2)
            monthDate  = calendar.month_name[int(monthDate)]
            dayDate    = mo.group(3)
            return monthDate,yearDate
        except Exception as err:
            print (err)
            pass
    def fileDateDirMkr(self,validFilesList,inputDir):
        yearFolder  = 0
        monthFolder = 0
        for file in validFilesList:
            try:
                monthDate,yearDate = self.dateExtractor(file)
            except Exception as err:
                print(err)
                continue

            try:
                os.mkdir(f'{yearDate}')
                yearFolder += 1
            except:
                pass

            try:
                os.mkdir(f'{inputDir}/{yearDate}/{monthDate}')
                monthFolder += 1
            except Exception as err:
                pass

        print (
f"""
YEAR FOLDER(S) MADE                : {yearFolder}
MONTH FOLDER(S) MADE               : {monthFolder}
""")
        
class FileLocationManager:
    def __init__(self,inputDir,dirMgr):
        self.inputDir = inputDir
        self.dirMgr   = dirMgr

    def photoToFolder(self,validFilesList,inputDir,dirMgr):
        for file in validFilesList:
            try:
                monthDate,yearDate = dirMgr.dateExtractor(file)
            except Exception as err:
                print(err)
                continue

            try:
                sourceFile = f'{file}'
                destinationDir = (f'{inputDir}/{yearDate}/{monthDate}')
                shutil.move(sourceFile, destinationDir)
            except Exception as err:
                print(err)

def main():

    #inputDir = input("INPUT DIRECTORY FOR PROCESSING... \n")
    inputDir = r'C:\OutputFolder'
    os.chdir(inputDir)

    folderMgr  = FolderManager(inputDir)
    dirMgr     = DirectoryManager(inputDir)
    fileDirMgr = FileLocationManager(inputDir,dirMgr)

    while True:

        # Check validity of directory
        if folderMgr.dirValid(inputDir) == True:
            print (f"""VALID DIRECTORY                    : TRUE""")
            pass
        elif folderMgr.dirValid(inputDir) == False:
            print (f"""VALID DIRECTORY                    : FALSE""")
            continue

        # Print out stats for the input directory
        folderMgr.dirStats(inputDir)

        # Make a list of all valid files in dir / subdir
        validFilesList = dirMgr.validFilesOrg(inputDir)

        # Make the folders for year / month
        dirMgr.fileDateDirMkr(validFilesList,inputDir)

        # Put files in correct locations
        fileDirMgr.photoToFolder(validFilesList,inputDir,dirMgr)

# CHECK FOR DUPLICATE PHOTOGRAPHS

        break





main()
