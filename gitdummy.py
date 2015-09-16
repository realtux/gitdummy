#!/usr/bin/env python3

import os
import json
import re
import subprocess
import uuid
import base64

# check for repos.json
if not os.path.isfile('repos.json'):
    print('No repos.json found, please create one')
    quit()

repos = json.load(open('repos.json'))

origWD = os.getcwd() # remember our original working directory

def init():
    subprocess.call([
        'git',
        'init'
    ])
    readme = open(repo['dummy_repo'] + os.path.sep + 'README.md', 'w+')
    readme.write(repo['dummy_readme'])
    readme.close()

    ignore = open(repo['dummy_repo'] + os.path.sep + '.gitignore', 'w+')
    ignore.write(".DS_Store\n")
    ignore.close()
    
    subprocess.call([
        'git',
        'add',
        '-A'
    ])
    subprocess.call([
        'git',
        'commit',
        '-m',
        'README'
    ])
    subprocess.call([
        'git',
        'remote',
        'add',
        'origin',
        repo['remote']
    ])
    subprocess.call([
        'git',
        'push',
        '-u',
        'origin',
        'master'
    ])

for repo in repos:

    commits = []

    if os.path.isdir(repo['dummy_repo']):
        # directory exists
        os.chdir(repo['dummy_repo'])

        if not os.path.isdir(repo['dummy_repo_data']):
            os.mkdir(repo['dummy_repo_data'])
        if not os.path.isdir(repo['dummy_repo'] + os.path.sep + '.git'):
            # but it hasn't been inited yet
            init()
    else:
        # directory didn't exist, so make the directory
        os.mkdir(repo['dummy_repo'])
        os.mkdir(repo['dummy_repo_data'])
        os.chdir(repo['dummy_repo'])
        init()

    since = ''
    if os.path.isfile(repo['dummy_repo'] + os.path.sep + '.gitdummy'):
        dotgitdummy = open(repo['dummy_repo'] + os.path.sep + '.gitdummy', 'r')
        since = dotgitdummy.read()
        dotgitdummy.close()

    for targetrepo in repo['target_repo']:

        os.chdir(targetrepo) # switch back to the target repo

        print('since: '+since)
        if since == '':
            log_output = subprocess.check_output([
                'git',
                'log',
                '--reverse',
                '--pretty=format:%an||||%ae||||%ad||||%s||||%f-%h'
            ])
        else:
            log_output = subprocess.check_output([
                'git',
                'log',
                '--since',
                since,
                '--reverse',
                '--pretty=format:%an||||%ae||||%ad||||%s||||%f-%h'
            ])

        log_split = log_output.decode('utf-8').split('\n')

        print("Log Split Length: {}".format(len(log_split)))

        if (len(log_split) > 1):

            line_re = re.compile(r'^(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)', re.DOTALL)

            commits = []

            for line in log_split:
                if '||||||||' in line: continue
                if '||||||||||||' in line: continue
                if '||||||||||||||||' in line: continue
                if '||||||||||||||||||||' in line: continue

                commit_line = line_re.search(line).groups()

                commits.append({
                    'name': commit_line[0],
                    'email': commit_line[1],
                    'date': commit_line[2],
                    'message': commit_line[3],
                    'filename': commit_line[4]
                })

    if len(commits) > 0:
        for commit in commits:
            private_commit_message = 'Commit message is private'
            
            #this modification checks if commit message has a greater character length than Mac OS limit for filenames (=255)
            #may be useful for other OS
            #without this change, for very long commit messages it will throw error: IOError: [Errno 63] File name too long 
            if len(commit['filename']) > 200:
               fullStr =  commit['filename']; commit['filename'] = fullStr[:200]

            if repo['random_file_name']:
                commit['filename'] = base64\
                    .urlsafe_b64encode(uuid.uuid4().bytes) \
                    .decode('UTF-8') \
                    .replace('=', '') \
                    .replace('-', '') \
                    .replace('_', '')

            os.chdir(repo['dummy_repo_data'])
            if not os.path.isfile(repo['dummy_repo_data'] + os.path.sep + commit['filename'] + repo['dummy_ext']):
                emailcheck = False
                for email in repo['target_email']:
                    if email == commit['email']:
                        emailcheck = True

                if emailcheck:
                    # file doesn't already exist
                    if repo['hide_commits'] is not True:
                        private_commit_message = commit['filename']+"\n"+commit['message'].replace("@","[at]")
                    print("PRIVATE COMMIT MESSAGE: "+private_commit_message)
                    dummyfile = repo['dummy_repo_data'] + os.path.sep + commit['filename'][:120] + repo['dummy_ext']
                    dummyfile = open(dummyfile, 'w+')
                    dummyfile.write(repo['dummy_code'])
                    dummyfile.close()
                    subprocess.call([
                        'git',
                        'add',
                        commit['filename']+repo['dummy_ext']
                    ])
                    dotgitdummy = open(repo['dummy_repo'] + os.path.sep + '.gitdummy', 'w+')
                    dotgitdummy.write(commit['date'])
                    dotgitdummy.close()
                    subprocess.call([
                        'git',
                        'add',
                        repo['dummy_repo'] + os.path.sep + '.gitdummy'
                    ])
                    os.environ['GIT_COMMITTER_DATE'] = commit['date']
                    subprocess.call([
                        'git',
                        'commit',
                        '-m',
                        private_commit_message,
                        '--date',
                        commit['date']
                    ])

        if repo['auto_push'] is True:
            if repo['force'] is True:
                subprocess.call([
                    'git',
                    'push',
                    '-u',
                    'origin',
                    'master',
                    '--force'
                ])
            else:
                subprocess.call([
                    'git',
                    'push',
                    '-u',
                    'origin',
                    'master'
                ])

        try:
            del os.environ['GIT_COMMITTER_DATE']
        except:
            pass
    else:
        print("Length of commits was zero, nothing to update")

os.chdir(origWD)
