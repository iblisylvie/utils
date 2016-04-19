# utils
python/extract_projects is used to clone the all the projects from a designated gitlab group.
To use this script, we need the gitlab group's html source page and be sure you already have the access to the projects.
This is a sample command to execute this script.
# python python/extract_projects.py --input gitlab.backend.sourcepage.htm --group backend --dir ~/Gitlab/backend
