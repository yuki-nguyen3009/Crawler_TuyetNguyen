#!/usr/bin/python
import sys, os, re
import urllib2, smtplib
import json

def send_mail(to_addr, commitID, fileName, stackTrace, repo):
    smtpHost = 'crox-casarray.gbst.net'
    from_addr = 'Jenkins <no-reply@gbst.com>'
    Cc_addr = 'thanh.nguyen@gbst.com'
    receiver = to_addr[:to_addr.index('.')].title()
    subject = "Commit ID %s have failure test on" % commitID
    content = "Hi %s, \
    \n\n%s file, which was merged from %s commit, was failed after unit test as below. \
    \n\n%sPlease help to take a look. \
    \n\nIf you have any question, please contact CI Team \
    \n\nThanks." % (receiver, fileName, repo, commitID, stackTrace)
    message = "From: %s\r\nTo: %s\r\nCC: %s\r\nSubject: %s\r\n\r\n%s" % (from_addr,to_addr, Cc_addr, subject, content)
    try:
        smtpObj = smtplib.SMTP(smtpHost)
        smtpObj.sendmail(from_addr, to_addr, message)         
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"
    finally:
        smtpObj.quit()

def read_file(fileName):
    try:
        fileData = []
        with open(fileName,'r') as f:
            for line in f:
                data = line.split(';')
                fileData.append(data)
        f.close()
    except IOError:
        print 'Fail to read file ' + fileName
        sys.exit(2)
    return fileData

def get_commit_info(commitData, fileName):
    commitsInfo = []
    f = open(commitData)
    datas = json.load(f)
    for data in datas:
        repo = data["repositories"]
        for commits in data["commit"]:
            if re.search(fileName, commits["file"]):
                fileInfo = [commits["ID"], commits["mail"], repo]
                commitsInfo.append(fileInfo)
                
    return commitsInfo
#                 fileNames = commits["file"].strip(';').split(';')
#                 for fileName in fileNames:
#                     print fileName
#     for element in datas:
#         repoPath = workspace + element[0]
#         os.chdir(repoPath)
#         commitID = element[1]
#         emailAddress = element[3]
#         listFileCmd = 'git show --pretty= --name-only %s' % commitID
#         listFile = os.popen(listFileCmd).read().strip().split('\n')
#         for line in listFile:
#             if re.search(line, fileName):
#                 emailData.append(commitID, line, emailAddress)
#             else:
#                 continue
#     return emailData


def get_error_file(resultFile):
    # Read result from Json API
    jsonData = urllib2.urlopen(resultFile)
    #Parse Json data to varible
    datas = json.loads(jsonData.read())
    errorFiles = []
    #Get "name" and "status" tag
    for suites in datas['suites']:
        for suite in suites['cases']:
            status = suite['status']
            fileName = suite['name']
            if (status.upper() == "FAILED") or (status.upper() == "REGRESSION"):
                fileName = suite['name']
                errorTraces = suite['errorStackTrace']
                errorDatas = [fileName, errorTraces]
                errorFiles.append(errorDatas)
 
    print "Reading result from Json API successful."
    return errorFiles

"""-----------------------------------
---------###Main func###--------------
-----------------------------------"""

"""Get argument"""
workspace = sys.argv[1]
#commitData= sys.argv[2]
buildURL = sys.argv[2]
resultData = buildURL +"testReport/api/json?pretty=true"
# workspace = "D:\\Bitbucket\\thanh8850\\"
commitData="%scommitData.json" % workspace
# buildURL = 'http://jenkins-sg.gbst.net:8080/job/Linux%20MC%20test%20block%201%20(Core)/lastCompletedBuild'
# resultData = buildURL +"/testReport/api/json?pretty=true"
#http://jenkins-sg.gbst.net:8080/job/Linux%20MC%20test%20block%201%20(Core)/lastCompletedBuild/testReport/api/json?pretty=true
#Get name of file which was failed unit test
errorsInfo = get_error_file(resultData)
for errorInfo in errorsInfo:
    fileName = str(errorInfo[0])
    stackTrace = str(errorInfo[1])
    #fileName = "test2.txt"
    commitsInfo = get_commit_info(commitData, fileName)
    for commitInfo in commitsInfo:
        commitID = commitInfo[0]
        #committerEmail = commitInfo[1]
        committerEmail = "thanh.nguyen@gbst.com"
        commitRepo = commitInfo[2]
        #Email Address, Commit ID, Error File, Error Stack Trace
        send_mail(committerEmail, commitID, fileName, stackTrace, commitRepo)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    