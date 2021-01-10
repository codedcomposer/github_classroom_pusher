# Last Modified by Daniel Z. Jan 2021
import os
import subprocess as cmd
import signal
import time
import requests
import json
from shutil import copyfile
import datetime
import sys, getopt
import re

def create_dir(new_directory):
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
        print("Directory ", new_directory," created.")
    else:
        print("Directory ", new_directory," already exists.")

def usage():
    print('Usage:	' + os.path.basename(__file__) + ' option file ')
    print('Options:')
    print('\t -c, --custom')
    sys.exit(2)

def replace_special_chars(git_dir_name):
    git_dir_name = git_dir_name.replace(' ', '-')
    git_dir_name = git_dir_name.replace(')', '-')
    git_dir_name = git_dir_name.replace('(', '-')
    git_dir_name = git_dir_name.replace('\'', '-')
    git_dir_name = git_dir_name.replace('&', '-')
    git_dir_name = git_dir_name.replace('%', '-')
    git_dir_name = git_dir_name.replace('.', '-')

    # use regex to fix multiple --'s after replacing special chars with -
    x = re.search("--+", git_dir_name)
    #print("DEBUG: occurences: " + x.start())
    while x:
        x = re.search("--+", git_dir_name)
        git_dir_name = git_dir_name.replace("--","-")
    #print("DEBUG: final txt: " + git_dir_name)

    if (git_dir_name[-1] == '-'):
        git_dir_name = git_dir_name[:len(git_dir_name)-1]
        #print("DEBUG: " + git_dir_name)
    
    return git_dir_name


########### Path to needed directories. Change them as needed##########
#working_directory = '/home/gabrian/University/CSCC01/TA/A1/marking/'
working_directory = '/Users/danielzhao/Downloads/auto_restart/'
submissions_directory = working_directory + 'submissions'
upload_to_github_dir = working_directory + 'upload_to_github'

create_dir(upload_to_github_dir)

#######################################################################
python_dir = '/usr/local/bin'

response_received = False
message = "script testing 1"

custom_submissions = []
custom_submissions_status = False

items_to_copy = list()
items_to_copy.append('report.html')
items_to_copy.append('output.xml')
items_to_copy.append('log.html')
#######################################################################

# extract parameters
try:
    opts, args = getopt.getopt(sys.argv[1:], "hc:", [
                                "help", "custom"])
except getopt.GetoptError as err:
    print(err)
    usage()
filename = args[0] if len(args) > 0 else None
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
    elif opt in ("-c", "--custom"):
        if (arg is not None):
            # run the command
            inputStream = open(arg, "r")
            Lines = inputStream.readlines() 
            for line in Lines: 
                #print("DEBUG: line: " + line)
                custom_submissions.append(line.strip('\n'))
            custom_submissions_status = True
    elif opt is None:
        print("ERROR: Brother. You did not enter an option!")


# decide the list of submissions to go through
if (custom_submissions):
    to_be_processed_submissions = custom_submissions
else:
    to_be_processed_submissions = os.listdir(submissions_directory)

# go through all submissions
for studentSubmission in to_be_processed_submissions:
    if studentSubmission[:9] != ".DS_Store":
        
        current_wkdir = upload_to_github_dir + "/"

        # get link and modify the repo to clone
        git_dir_name = 'a1-' + studentSubmission.lower()

        git_dir_name = replace_special_chars(git_dir_name)

        git_ssh = 'https://github.com/UTSCCSCC01/' + git_dir_name + '.git'
        print('INFO: git_directory: ' + git_ssh)
        
        # change to working directory of all submissions to clone project
        os.chdir(current_wkdir)
        
        # clone repo only if it does not exist already (important)
        if (os.path.isdir(git_dir_name)):
            continue
        else:
            try:
                cmd.run("git clone {}".format(git_ssh), check=True, shell=True)
            except:
                print("ERROR: could not clone " + git_ssh)

                
        # change directory to individual git folder
        dest_dir = upload_to_github_dir + '/' + git_dir_name
        os.chdir(dest_dir)

        # go through all items to copy over and upload eg. report.html, log.html
        for item in items_to_copy:
            # copy .html from unzipped to upload_to_github_dir
            src = submissions_directory + '/' + studentSubmission + '/' + item
            dest = dest_dir + '/' + item

            print("INFO: src: " + src)
            print("INFO: dest_dir: " + dest_dir)
        
            # # check if report.html already exists, remove if it does
            # if (os.path.isfile(dest)):
            #     cmd.run("ls -ltr", check=True, shell=True)
            #     cmd.run("rm -f " + item, check=True, shell=True)
            try:
                copyfile(src, dest)
            except:
                print("ERROR: could not copy from " + src + " to " + dest)
        
        # specify report update time
        report_time_filename = 'report_times.txt'
        current_time = datetime.datetime.utcnow()
        
        # append curr time to report_time_filename
        cp = cmd.run("echo {} >> {}".format(current_time, report_time_filename), check=True, shell=True)
        print("INFO: current time: {}".format(current_time))
        
        # git add changed files and report time txt
        cmd.run("git add {}".format(report_time_filename), check=True, shell=True)
        for item in items_to_copy:
            cmd.run("git add " + item, check=True, shell=True)        
        
        # git commit msg
        # NOTE: if there are no changes, commit and push will not do anything (perfect) #
        if (not response_received):
            print("INFO: commit_message: " + message)
            response = input("Do you want to use this message for this commit?([y]/n)\n")   
                 
            if response.startswith('n'):
                message = input("What message you want?\n")
        
        # git commit and push
        cmd.run(f"git commit -m '{message}'", check=True, shell=True)
        cmd.run("git push", check=True, shell=True)
        
        # setter such that only need to type commit msg once for all uploads        
        response_received = True
        
