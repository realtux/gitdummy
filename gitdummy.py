import os
import json
import re
import subprocess

# check for repos.json
if not os.path.isfile('repos.json'):
    print 'No repos.json found, please create one'
    quit()

repos = json.load(open('repos.json'))

for repo in repos:
    # make sure dummy repo doesn't exist or does exist with a .gitdummy file
    if os.path.isdir(repo['dummy_repo'].strip()):
        if not os.path.isfile(repo['dummy_repo'] + os.path.sep + '.gitdummy'):
            print '##############################################'
            print \
                'Warning: ' + \
                repo['dummy_repo'] + \
                ' exists but doesn\'t contain a .gitdummy file, are you sure this is a dummy repo?'
            print '##############################################'
            quit()
    else:
        os.mkdir(repo['dummy_repo'])

        dotgitdummy = open(repo['dummy_repo'] + os.path.sep + '.gitdummy', 'w+')
        dotgitdummy.write('')
        dotgitdummy.close()

        dotgitignore = open(repo['dummy_repo'] + os.path.sep + '.gitignore', 'w+')
        dotgitignore.write('.gitdummy')
        dotgitignore.close()

    log_output = subprocess.check_output([
        'git',
        '-C',
        repo['target_repo'],
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
            'name': commit_line[0],
            'email': commit_line[1],
            'date': commit_line[2],
            'message': commit_line[3]
        })

    subprocess.call([
        'git',
        '-C',
        repo['dummy_repo'],
        'init'
    ])

    subprocess.call([
        'git',
        '-C',
        repo['dummy_repo'],
        'config',
        'user.name',
        '\'' + repo['dummy_name'] + '\''
    ])

    subprocess.call([
        'git',
        '-C',
        repo['dummy_repo'],
        'config',
        'user.email',
        '\'' + repo['dummy_email'] + '\''
    ])

    i = 1

    private_commit_message = 'Commit message is private'

    for commit in commits:
        if repo['hide_commits'] is not True:
            private_commit_message = commit['message']

        if commit['email'] == repo['target_email']:
            file = open(repo['dummy_repo'] + '/commit' + str(i).zfill(5) + '.txt', 'w+')
            file.write(private_commit_message)
            file.close()

            subprocess.call([
                'git',
                '-C',
                repo['dummy_repo'],
                'add',
                '-A',
            ])

            subprocess.call([
                'env',
                'GIT_AUTHOR_DATE=\'' + commit['date'] + '\'',
                'GIT_COMMITTER_DATE=\'' + commit['date'] + '\'',
                'git',
                '-C',
                repo['dummy_repo'],
                'commit',
                '-m',
                private_commit_message
            ])

            i += 1

    if repo['auto_push'] is True:
        subprocess.call([
            'git',
            '-C',
            repo['dummy_repo'],
            'remote',
            'add',
            'origin',
            repo['remote'],
        ])

        subprocess.call([
            'git',
            '-C',
            repo['dummy_repo'],
            'remote',
            'set-url',
            'origin',
            repo['remote'],
        ])

        subprocess.call([
            'git',
            '-C',
            repo['dummy_repo'],
            'push',
            'origin',
            'master',
        ])