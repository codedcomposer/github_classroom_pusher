# Introduction
Python script used to commit and push files to github classroom repos. 
Useful for instructors with automarkers to mass update student repos with results and feedback.

I made this script after I discovered github classroom lets you clone repos, but not push to them... Yikes! This is because they use temporary clone tokens by design.

The following error will come up when trying to push.
`
remote: Temporary clone tokens are read-only.
fatal: unable to access ‘https://github.com/UTSCCSCC01/great-project-123/ 7’: The requested URL returned error: 403
`

https://education.github.community/t/how-to-push-changes-to-student-repos/48751

# Walkthrough
1. Download student submissions from github classroom
2. Unzip it, and move submissions to `github_classroom_pusher/submissions`
3. Look at the 'Before You Run' section, and change important env & user variables
4. Run the script, i.e. 
```shell
python3 upload_github.py
```
5. Enter your commit message, or use the default one
6. The script should now be cloning directories from `github_classroom_pusher/submissions` to `github_classroom_pusher/upload_to_github`
7. The script should then git add, commit, and push to repos
8. If you've already cloned and pushed and want to push again, you will need to manually delete the folders from `github_classroom_pusher/upload_to_github` and based on what you want to do, change `items_to_add` in  `env.yml` (possible improvement in future)

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
- this option allows you to upload exclusively to submissions in custom.txt
- sample custom.txt file in repo, each line represents a student's submission folder
- may be useful for re-marks, where only a subsection of submissions needs to be changed

# Other Stuff
- to find python directory run the comman 'which python' on commandline, then enter the location into python_dir', do not include trailing slash
`python_dir = '/usr/local/bin'`