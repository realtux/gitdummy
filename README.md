GitDummy v2
========

Ever wanted to include your private repository contributions to your contribution panel? Well now you can. This script will read from an existing repository and transcribe all of the commit messages into a dummy repository that you can then add publicly to your GitHub account. This script transfers no source code, only commit stubs and their associated dates.

Usage is simple (after you've created your JSON file):
```
python gitdummy.py
```
Your JSON file will look similiar to:
```json
[
    {
        "target_repo"  : "/home/brian/myrepo",
        "target_email" : "brian@example.org",
        "dummy_repo"   : "/home/brian/dummy_myrepo",
        "dummy_email"  : "brian@example.org",
        "dummy_name"   : "Brian Seymour"
    }
]
```

#### Where is your Git repo (target_repo)
Here you must provide the Git repo that you want to transcribe from. The directory must exist and contain a .git folder inside.

#### Which email address should commits be checked against (target_email)
Here you must provide the email address the script should search for in the repo being transcribed from. This makes it so only your commits will come out and into the repo being transcribed to.

#### Where should the dummy repo be created (dummy_repo)
Here you must provide the folder you want the script to transcribe to. The directory must not exist.

#### Which email address should be used in the dummy commits (dummy_email)
Here you must provide a new email address the dummy commits will be made as. This will most likely be your GitHub email address so GitHub can properly associate the commits with your account.

#### Which name should be used in the dummy commits (dummy_name)
Here you must provide the name the dummy commits will be made as. This really has no bearing, but, it should be your name.
