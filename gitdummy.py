import os
import re
import subprocess
import pprint

git_directory = raw_input('Where is your Git repo: ')

if not os.path.isdir(git_directory.strip() + '/.git'):
    print 'Sorry, this doesn\'t appear to be a Git repo';
    quit()

target_directory = raw_input('Where should I create the dummy repo: ')

if os.path.isdir(target_directory.strip()):
    print 'Sorry, the target directory already exists, please specify an empty one';
    quit()

commit_email = raw_input('Which email address should commits be checked against: ')
new_email = raw_input('Which email address should be used in the dummy commits: ')
new_name = raw_input('Which name should be used in the dummy commits: ')

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

for commit in commits:
    if commit['email'] == commit_email:
        file = open(target_directory + '/commit' + str(i) + '.txt', 'w+')
        file.write(commit['message'])
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
            commit['message']
        ])

        i += 1