import os
import re
import subprocess
import pprint
from distutils.util import strtobool

git_directory = raw_input('Where is your Git repo: ')

if not os.path.isdir(git_directory.strip() + '/.git'):
    print 'Sorry, this doesn\'t appear to be a Git repo';
    quit()

target_directory = raw_input('Where should the dummy repo be created: ')

if os.path.isdir(target_directory.strip()):
    print 'Sorry, the target directory already exists, please specify an empty one';
    quit()

commit_email = raw_input('Which email address should commits be checked against: ')
new_email = raw_input('Which email address should be used in the dummy commits: ')
new_name = raw_input('Which name should be used in the dummy commits: ')
private_repo = raw_input('Hide commit messages? (yes/no): ')

is_private = strtobool(private_repo)

log_output = subprocess.check_output([
    'git',
    '-C',
    git_directory,
    'log',
    '--reverse',
    '--pretty=format:%an||||%ae||||%ad||||%s'
])

log_split = log_output.split('\n')

line_re = re.compile(r'^(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)', re.DOTALL)

commits = []

for line in log_split:
    if '||||||||' in line: continue
    if '||||||||||||' in line: continue
    if '||||||||||||||||' in line: continue

    commit_line = line_re.search(line).groups()

    commits.append({
        'name' : commit_line[0],
        'email' : commit_line[1],
        'date' : commit_line[2],
        'message' : commit_line[3]
    })

os.makedirs(target_directory)

subprocess.call([
    'git',
    '-C',
    target_directory,
    'init'
])

subprocess.call([
    'git',
    '-C',
    target_directory,
    'config',
    'user.name',
    '\'' + new_name + '\''
])

subprocess.call([
    'git',
    '-C',
    target_directory,
    'config',
    'user.email',
    '\'' + new_email + '\''
])

i = 1

private_commit_message = 'Commit message is private'

for commit in commits:
    if is_private != 1:
        private_commit_message = commit['message']

    if commit['email'] == commit_email:
        file = open(target_directory + '/commit' + str(i).zfill(5) + '.txt', 'w+')
        file.write(private_commit_message)    
        file.close()

        subprocess.call([
            'git',
            '-C',
            target_directory,
            'add',
            '-A',
        ])

        subprocess.call([
            'env',
            'GIT_AUTHOR_DATE=\'' + commit['date'] + '\'',
            'GIT_COMMITTER_DATE=\'' + commit['date'] + '\'',
            'git',
            '-C',
            target_directory,
            'commit',
            '-m',
            private_commit_message
        ])

        i += 1