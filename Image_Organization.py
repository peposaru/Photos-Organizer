# Title: Photos Organization
# Description: This program is for organizing all my photos into Year -> Month

import PIL.Image,time
import os, datetime, re, calendar, shutil
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from tqdm import tqdm

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

        for subdir, dirs, files in tqdm(os.walk(inputDir), desc='VALIDATING FILES...'):
            for file in files:
                try: 
                    Image.open(os.path.join(subdir, file))
                    validFilesList += [(os.path.join(subdir, file))]
                except:
                    pass
        return validFilesList 
    def processingFolder(self):
            os.makedirs('Output Folder',exist_ok=True)
            print('OUTPUT FOLDER CREATED...')
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
            print (f'ERROR WHILE EXTRACTING DATE ON FILE : {file}\n ERROR : {err}')
            pass
        return None, None
    def fileDateDirMkr(self,validFilesList,inputDir):
        yearFolderCount  = set()
        monthFolderCount = set()

        for file in validFilesList:
                monthDate,yearDate = self.dateExtractor(file)
                if not monthDate or not yearDate:
                    continue
                
                yearFolder = os.path.join(inputDir,yearDate)
                monthFolder = os.path.join(yearFolder,monthDate)

                os.makedirs(yearFolder, exist_ok=True)
                yearFolderCount.add(yearFolder)

                os.makedirs(monthFolder,exist_ok=True)
                monthFolderCount.add(monthFolder)

        print (
f"""
YEAR FOLDER(S) MADE                : {len(yearFolderCount)}
MONTH FOLDER(S) MADE               : {len(monthFolderCount)}
""")
        
class FileLocationManager:
    def __init__(self,inputDir,dirMgr):
        self.inputDir = inputDir
        self.dirMgr   = dirMgr

    def photoToFolder(self,validFilesList,inputDir,dirMgr):
        for file in tqdm(validFilesList, desc='MOVING FILES TO FOLDERS...'):
            monthDate,yearDate = dirMgr.dateExtractor(file)
            if not monthDate or not yearDate:
                continue

            sourceFile = f'{file}'
            destinationDir = os.path.join(inputDir, yearDate, monthDate)

            try:
                shutil.move(sourceFile, destinationDir)
            except Exception as err:
                print(f' ERROR MOVING {file} TO {destinationDir} : {err}')

    
def main():
    
    #inputDir = input("INPUT DIRECTORY FOR PROCESSING... \n")
    inputDir = r'C:\Users\keena\Desktop\Photos Processing\Test Files'
    os.chdir(inputDir)

    folderMgr  = FolderManager(inputDir)
    dirMgr     = DirectoryManager(inputDir)
    fileDirMgr = FileLocationManager(inputDir,dirMgr)

    print('INITIALIZING... PLEASE WAIT...')
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
        break
# CHECK FOR DUPLICATE PHOTOGRAPHS


if __name__ == "__main__":
    main()
