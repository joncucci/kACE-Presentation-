
# Extranneous Imports
import sys, os, urllib3, math, csv, copy
from prettytable import PrettyTable
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TOKEN retrieval
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')

# python-GitLab imports
import gitlab
from gitlab.v4.objects import branches, discussions

# GitLab connection established
gl = gitlab.Gitlab('https://gitlab.cad.local/', TOKEN, api_version = 4, ssl_verify = False)
project = gl.projects.get('kace-fxo/kace')
branches = project.branches.list(all = True, state = 'opened')

def commit_information(jira_numbers):

    table = PrettyTable()
    table.field_names = ["Branch", "Hash ID", "Message", "Date"]
    table._max_width = {"Message": 50}

    for branch in branches:
        for commit in project.commits.list(ref_name = branch.name):
            for jira_number in jira_numbers:

                if jira_number in commit.title:

                    table.add_row(
                        [
                            branch.name, 
                            commit.short_id, 
                            commit.title, 
                            commit.committed_date.split("T")[0]
                        ])

    with open('one.csv', 'r') as file:
        reader = csv.reader(file, delimiter = ",")
        for row in reader:
            if row == []:
                continue
            else:
                for jira_number in jira_numbers:
                    if jira_number in row[3]:
                        table.add_row(
                        [
                            "Perforce" , 
                            row[0], 
                            row[3], 
                            row[1]
                        ])
        file.close()

    print(table)

# Testing
# commit_information(["FA-3358"])

def commit_comments(jira_numbers):

    table = PrettyTable()
    table.field_names = ["Branch", "Hash ID", "Jira Number", "Comment","Author", "Date"]
    table._max_width = {"Comment": 50}

    for branch in branches:
        for commit in project.commits.list(ref_name = branch.name):
            for jira_number in jira_numbers:

                if jira_number in commit.title:

                    discussion = commit.discussions.list(all=True, state = 'opened')

                    for num_comment in range(len(discussion)):

                        info = discussion[num_comment].attributes['notes'][0]
                        table.add_row(
                            [
                                branch.name,
                                commit.short_id,
                                jira_number,
                                info['body'],
                                info['author']['name'],
                                info['created_at'].split("T")[0]
                            ])
    print(table)

# Testing
#commit_comments(["FA-7227"])

def choice():
    args = input("").split(" ")
    if "commits" == args[0]:
        commit_information(args[1:])
    elif "comments" == args[0]:
        commit_comments(args[1:])
    else:
        pass

if __name__ == '__main__':
    while True:
        try:
            choice()
        except:
            pass

