#!/bin/sh
echo "$(uname -a)  $(date)" >> backups.log
git pull
python backup.py
git add .
SO=$(cat settings.cfg | grep OLD | awk -F= '{print $2}' | cut -c4-100)
git commit -m "$SO update"
git push