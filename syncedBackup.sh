#!/bin/sh

#Stores current backup time and system
echo "$(uname -a)  $(date)" >> backups.log

#Get new stuff just in case
git pull

#Do all backups locally
python backup.py

#Stage all changes (excluding old folders)
git add .

#Grab what SO is being used
SO=$(cat settings.cfg | grep OLD | awk -F= '{print $2}' | cut -c4-100)

#Commit the staged changes
git commit -m "$SO update"

#Saves the push success or failure messages to a log file, cat it and then make an error code if necessary
git push &> lastpush.log
cat lastpush.log
! cat lastpush.log | grep -E 'rejected'
