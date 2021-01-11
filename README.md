# Introduction
Python script used to commit and push files to github classroom repos. 
Useful for instructors with automarkers to mass update student repos with results and feedback.

I made this script after I discovered github classroom lets you clone repos, but not push to them... This is because they use temporary clone tokens by design. Yikes!

``
remote: Temporary clone tokens are read-only.
fatal: unable to access ‘https://github.com/2019-BIT-142/bit-142-lesson-10-amberleemin.git/ 7’: The requested URL returned error: 403
``

https://education.github.community/t/how-to-push-changes-to-student-repos/48751

# Before You Run
- change the following environment variables in `env.yml`
- python_dir: ensure this points to python3
- working_directory: this is the absolute root directory where the script and submissions are located
- github_organization_url: the fixed part of the URL where you want to clone repos from, see example in env.yml
- assignment_name: what you named the assignment plus an extra `-` to satisfy git repo naming conventions
- items_to_add: what you want to upload to the repo

# Features
## Update all repos
```shell
python3 upload_github.py
```
## Update select repos from a .txt file
```shell
python3 upload_github.py -c custom.txt
```
- sample custom.txt file in repo, each line represents a student's submission folder.