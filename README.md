# utils
# python/extract_projects is used to clone the whole designated group from gitlab given a group html page's source code. here we assume you already have the rights to access the projects.
# here is the sample command to execute this script.
python python/extract_projects.py --input gitlab.backend.sourcepage.htm --group backend --dir ~/Gitlab/backend
