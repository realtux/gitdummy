GitDummy (v1/v2)
========

Ever wanted to include your private repository contributions to your contribution panel? Well now you can. This script will read from an existing repository and transcribe all of the commit messages into a dummy repository that you can then add publicly to your GitHub account. This script transfers no source code, only commit stubs and their associated dates.

Usage is simple:
```
python gitdummy.py
```
### If you're running version 2 (json based multi conversion), no questions will be asked.

### If you're running version 1 (one-time conversion), you'll be asked the following 5 questions:

#### Where is your Git repo
Here you must provide the Git repo that you want to transcribe from. The directory must exist and contain a .git folder inside.

#### Where should the dummy repo be created
Here you must provide the folder you want the script to transcribe to. The directory must not exist.

#### Which email address should commits be checked against
Here you must provide the email address the script should search for in the repo being transcribed from. This makes it so only your commits will come out and into the repo being transcribed to.

#### Which email address should be used in the dummy commits
Here you must provide a new email address the dummy commits will be made as. This will most likely be your GitHub email address so GitHub can properly associate the commits with your account.

#### Which name should be used in the dummy commits
Here you must provide the name the dummy commits will be made as. This really has no bearing, but, it should be your name.
