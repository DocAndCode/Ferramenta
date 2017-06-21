import requests
import json
import os
import re
import datetime
import shutil

#######################################################
################     CONFIGURATION     ################
####    Set below variables before running this    ####
#######################################################
# @OAUTHTOKEN: Your GitHub Personal Access Token
# @repoOwner: Repository Owner
#   e.g. torvalds
# @repoName: Repository Name
#   e.g. linux
#######################################################
OAUTHTOKEN = ''
repoOwner = ''
repoName = ''
#######################################################

repoInfo = '{}/{}'.format(repoOwner, repoName)
dirPath = ''
reportDir = '{}Report'.format(dirPath)
headers = {
    'User-Agent': 'request'
}
issuesJSON = {}
commitsJSON = {}

def cleanFiles():
    print('Preparando arquivos.', end=' ')

    if os.path.exists(reportDir):
        shutil.rmtree(reportDir)

    print('OK')


def checkIfDirExists():
    if not os.path.exists(reportDir):
        os.makedirs(reportDir)


def getIssues():
    print("Coletando informações de Issues.", end=' ')

    url = 'https://api.github.com/repos/{}/issues?state=all'.format(repoInfo)
    r = requests.get(url = url, headers = headers)
    issues = r.json()

    checkIfDirExists()

    for issue in issues:
        assignees = []

        for assignee in issue['assignees']:
            assignees.append({
                'login': assignee['login'],
                'url': assignee['html_url']
            })

        issuesJSON[issue['number']] = {
            'number': issue['number'],
            'title': issue['title'],
            'body': issue['body'],
            'url': issue['url'],
            'assignees': assignees,
            'labels': issue['labels']
        }

        printIssuesToFile(issuesJSON[issue['number']])
        updateReport(issuesJSON[issue['number']])

    print("OK")


def printIssuesToFile(myjson):
    issueFile = open(reportDir + '/' + 'issue_' + str(myjson['number']) + '.md', 'w+')

    issueFile.write('## [#{} - {}]({})\n\n'.format(myjson['number'], myjson['title'], myjson['url']))
    issueFile.write('{}\n\n'.format(myjson['body']))
    issueFile.write('* **Assignees**:\n')

    if len(myjson['assignees']) != 0:
        for assignee in myjson['assignees']:
            issueFile.write('    * [{}]({})\n'.format(assignee['login'], assignee['url']))
        issueFile.write('\n')
    else:
        issueFile.write('\n')

    issueFile.write('* **Labels**:\n')

    if len(myjson['labels']) != 0:
        for label in myjson['labels']:
            issueFile.write('    * <span style=\"background-color:#{};\">{}</span>\n'.format(label['color'], label['name']))
        issueFile.write('\n')
    else:
        issueFile.write('\n')

    issueFile.write('## Commits\n')
    issueFile.close()


def getCommits():
    print("Coletando informações de Commits.", end=' ')

    url = 'https://api.github.com/repos/{}/commits?access_token={}'.format(repoInfo, OAUTHTOKEN)
    r = requests.get(url = url, headers = headers)
    commits = r.json()

    checkIfDirExists()

    for commit in commits:
        url = 'https://api.github.com/repos/{}/commits/{}?access_token={}'.format(repoInfo, commit['sha'], OAUTHTOKEN)
        r = requests.get(url = url, headers = headers)
        commitData = r.json()

        additions = 0;
        deletions = 0;
        files = []

        for commitFiles in commitData['files']:
            files.append({
                'filename': commitFiles['filename'],
                'url': commitFiles['blob_url']
            })

            additions += commitFiles['additions']
            deletions += commitFiles['deletions']

        date = commitData['commit']['author']['date'].split('T')[0]
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%y')

        commitsJSON[commitData['sha']] = {
            'date': date,
            'message': commitData['commit']['message'],
            'author': {
                'login': commitData['author']['login'],
                'url': commitData['author']['html_url'],
            },
            'link': commitData['html_url'],
            'files': files,
            'additions': additions,
            'deletions': deletions
        }

        printCommitsToFile(commitsJSON[commitData['sha']])

    print('OK')


def printCommitsToFile(myjson):
    tags = re.findall(r"#[0-9]+", myjson['message'])

    for tag in tags:
        filePath = '{}/issue_{}.md'.format(reportDir, tag.replace('#', ''))

        if os.path.exists(filePath):
            issueFile = open(filePath, 'a')

            issueFile.write('\n**[{}]({})**\n'.format(myjson['message'], myjson['link']))
            issueFile.write('* **Data**: {}\n'.format(myjson['date']))
            issueFile.write('* **Autor**: [{}]({})\n'.format(myjson['author']['login'], myjson['author']['url']))
            issueFile.write('* **Adições**: {}\n'.format(myjson['additions']))
            issueFile.write('* **Remocões**: {}\n'.format(myjson['deletions']))
            issueFile.write('* **Arquivos alterados**:\n')

            for fileData in myjson['files']:
                issueFile.write('    * [{}]({})\n'.format(fileData['filename'], fileData['url']))

            issueFile.close()


def createReportFile():
    report = open('{}DocAndCode.md'.format(dirPath), 'w+')
    report.write('## Relatório Doc&Code\n\n')
    report.write('### Issues:\n\n')
    report.close()


def updateReport(myjson):
    report = open('{}DocAndCode.md'.format(dirPath), 'a')
    report.write('[#{} - {}](issue_{})\n\n'.format(myjson['number'], myjson['title'], myjson['number']))
    report.close()


cleanFiles()
createReportFile()
getIssues()
getCommits()
print('Processo Finalizado\n\nRelatório Doc&Code gerado em {}\n'.format(dirPath))
