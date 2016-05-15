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
        project_local_dir = abs_dir + '/' + group + '/' + project
        if os.path.exists(project_local_dir):
            sync_project(project_local_dir)
        else:
            clone_project(group, project, project_local_dir)

def sync_project(project_path):
    cmd = "git --git-dir={project_path}/.git --work-tree={project_path} pull -a"
    cmd = cmd.format(project_path = project_path)
    print cmd
    subprocess.call(cmd, shell = True)

def clone_project(group, project, project_path):
    pwd = os.getcwd()
    os.makedirs(project_path)
    cmd = "cd {project_path} && \
            git clone --mirror git@gitlab.mobvoi.com:{group}/{project}.git .git && \
            git config --bool core.bare false && \
            git reset --hard"
    cmd = cmd.format(group = group, project = project, project_path = project_path)
    print cmd
    subprocess.call(cmd, shell = True)
    subprocess.call("cd " + pwd, shell = True)

if __name__ == '__main__':
    args = parse_args()
    content = read_file_to_str(args.input)
    projects = find_projects(content)
    try:
        clone_projects(args.dir, projects, args.group)
    except KeyboardInterrupt:
        sys.exit()
