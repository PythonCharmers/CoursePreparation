import os
import time
import zipfile

# 1. The files and directories to be backed up are
# specified in a list.
# Example on Windows:
# source = [r'C:\My Documents']
# Example on macOS and Linux:
source = ['/Users/swa/notes']
# Notice we use a raw string \(the r prefix\) for the
# Windows path so that the backslashes are not treated
# as escape sequences.

# 2. The backup must be stored in a
# main backup directory
# Example on Windows:
# target_dir = r'E:\Backup'
# Example on macOS and Linux:
target_dir = '/Users/swa/backup'
# Remember to change this to which folder you will be using

# 3. The files are backed up into a zip file.
# 4. The name of the zip archive is the current date and time
target = os.path.join(target_dir,
                      time.strftime('%Y%m%d%H%M%S') + '.zip')

# Create target directory if it is not present
if not os.path.exists(target_dir):
    os.mkdir(target_dir)  # make directory

# 5. We use the zipfile module to put the files in a zip archive
print('Backing up to', target)
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
    for item in source:
        for folder, subfolders, filenames in os.walk(item):
            for filename in filenames:
                path = os.path.join(folder, filename)
                print('  adding:', path)
                backup_zip.write(path)

print('Successful backup to', target)
