# This is a short script which keeps track of how many local builds were made
# and the overall line count of the project

import re
import datetime

import os
from os import listdir
from os.path import isfile, join

from datetime import datetime, date, time

PROJECT_NAME = 'Empty Project'

def GetFileLineCount(filename):
    f = open(filename)
    lineCount = 0
    
    for line in f:
        lineCount += 1
        
    return lineCount

if __name__ == "__main__":
    buildVersion = 0
    lineCount = 0
    buildLog = []

    mypath = os.path.dirname(os.path.realpath(__file__)) + "/../"

    directories = ['src', 'test', 'include', 'scripts', 'opencl_programs', 'demos', 'utilities/src', 'utilities/include']
    
    # Find the right file (previous versions used different naming conventions)
    possible_file_names = ['build_version.txt', 'BuildVersion.txt']
    actual_file_name = possible_file_names[0]
    for fname in possible_file_names:
        try:
            with open(mypath + '/workspace/tracking/' + fname, 'r') as f:
                actual_file_name = fname
                break
        except FileNotFoundError:
            pass

    try:
        with open(mypath + '/workspace/tracking/' + actual_file_name, 'r') as f:    
            headerLine1 = f.readline()
            headerLine2 = f.readline()
        
            fileVersionLine = f.readline()
            match = re.search('BUILD VERSION:\s*(\d+)', fileVersionLine)

            if match is not None:
                buildVersion = int(match.group(1))
            
            # Save the build log
            for line in f:
                # Check if the line is empty
                if line.strip():
                    buildLog.append(line)
    except FileNotFoundError:
        # File does not currently exist which is okay
        try:
            os.makedirs(mypath + '/workspace/tracking/')
        except FileExistsError:
            pass
        
    # Increment the build version
    buildVersion += 1
    
    # Calculate line count    
    ignoreFiles = ['sqlite3ext.h', 'sqlite3.h', 'shell.c', 'sqlite3.c']

    for directory in directories:
        for root, subFolders, files in os.walk(mypath + directory):
            for fileEntry in files:
                if (fileEntry.endswith('.h') or fileEntry.endswith('.cpp') or fileEntry.endswith('.py') or fileEntry.endswith('.cl')):
                    if (fileEntry not in ignoreFiles):
                        lineCount += GetFileLineCount(os.path.join(root, fileEntry.strip()))
        
    # Rewrite the file
    f = open(mypath + '/workspace/tracking/build_version.txt', 'w')
    
    f.write('%s 2019 Build Information\n' % PROJECT_NAME)
    f.write('Ange Yaghi | 2019 | Every now and then, some rain must fall\n')
    
    f.write('BUILD VERSION: %d\n\n' % (buildVersion))
    
    dt = datetime.now()   
    dateString = dt.strftime('%Y-%m-%d %H:%M')
    f.write('Build\t%s\t%d\t%d\n' % (dateString, lineCount, buildVersion))
    
    for logEntry in buildLog:
        f.write(logEntry)
    
    f.close()
