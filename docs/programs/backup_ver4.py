import os
import time
import zipfile

# 1. The files and directories to be backed up are
# specified in a list.
# Example on Windows:
# source = [r'C:\My Documents', r'C:\Code']
# Example on macOS and Linux:
source = ['/Users/swa/notes']

# 2. The backup must be stored in a
# main backup directory
# Example on Windows:
# target_dir = r'E:\Backup'
# Example on macOS and Linux:
target_dir = '/Users/swa/backup'
# Remember to change this to which folder you will be using

# Create target directory if it is not present
if not os.path.exists(target_dir):
    os.mkdir(target_dir)  # make directory

# 3. The files are backed up into a zip file.
# 4. The current day is the name of the subdirectory
# in the main directory.
today = os.path.join(target_dir, time.strftime('%Y%m%d'))
# The current time is the name of the zip archive.
now = time.strftime('%H%M%S')

# Take a comment from the user to
# create the name of the zip file
comment = input('Enter a comment --> ')
# Check if a comment was entered
if len(comment) == 0:
    zip_name = now + '.zip'
else:
    zip_name = now + '_' + \
        comment.replace(' ', '_') + '.zip'
target = os.path.join(today, zip_name)

# Create the subdirectory if it isn't already there
if not os.path.exists(today):
    os.mkdir(today)
    print('Successfully created directory', today)

# 5. We use the zipfile module to put the files in a zip archive
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
    for item in source:
        for folder, subfolders, filenames in os.walk(item):
            for filename in filenames:
                backup_zip.write(os.path.join(folder, filename))

print('Successful backup to', target)
