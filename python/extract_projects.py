#! /usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'iblisylvie'
__email__ = 'iblisylvie@gmail.com'

import argparse 
import os
import subprocess
import sys

from bs4 import BeautifulSoup as BS

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', 
            help = 'input file which is the downloaded source page \
                    for a given gitlab group, where group projects are listed',
            required = True)
    parser.add_argument('--group',
            help = 'the groupname for the projects listed in the input file', 
            required = True)
    parser.add_argument('--dir', 
            help = 'output directory where cloned git reository is saved',
            required = True)
    return parser.parse_args()

def read_file_to_str(file):
    with open(file, 'r') as fin:
        lines = [line for line in fin]
    return '\n'.join(lines)

def find_projects(content):
    soup = BS(content, "html.parser")
    alls = soup.findAll('span')
    projects = set()
    for s in alls:
        if (s['class'] == ['project-name']):
            if s.string:
                projects.add(s.string.strip())
    return projects

# projects = (x, y, z)
# gitlab_path = "git@gitlab.mobvoi.com:${group}/${project}.git"
def clone_projects(abs_dir, projects, group):
    clone_cmd = "git clone git@gitlab.mobvoi.com:{group}/{project}.git {dir}"
    for project in projects:
        project_local_dir = abs_dir + '/' + project
        if os.path.exists(project_local_dir):
            continue
        real_clone_cmd = clone_cmd.format(group = group, 
            project = project, dir = project_local_dir)
        print real_clone_cmd
        subprocess.call(real_clone_cmd, shell = True)

if __name__ == '__main__':
    args = parse_args()
    content = read_file_to_str(args.input)
    projects = find_projects(content)
    try:
        clone_projects(args.dir, projects, args.group)
    except KeyboardInterrupt:
        sys.exit()
