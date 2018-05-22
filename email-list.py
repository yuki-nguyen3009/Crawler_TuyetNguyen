#!/usr/bin/python
import sys, os, re


workspace = sys.argv[1]
commitsChange = "%scommits-change.csv" % workspace
emailFile = "%semailList.txt" % workspace
devNamelFile = "%sdevEmail.txt" % workspace
devEmails = []
emailList = []
emails = ""
print '-'*10 +'Starting create environment file which was used to send email notification for postbuild.'+ '-'*10
###Get developer email from list of dev email
f = open(devNamelFile, 'r')
for line in f:
    devEmails.append(line.strip('\n'))

###Get email from csv file
h = open(commitsChange, 'r')
for line in h:
    if line.upper() == 'There is no commit change.'.upper():
        continue
    else:
        repEmail = line.split(';')[-2]
        for devEmail in devEmails:
            if repEmail.split('@gbst.com')[0].upper() == devEmail.upper():
                emailList.append(repEmail)
            else:
                continue
h.close()

###Remove duplicate email
newEmailList = list(set(emailList))

###Add all email into varible which was used for postbuild
for num in range(len(newEmailList)):
     emails = emails + newEmailList[num] + ','

### Create environment file which was used for postbuild
f = open(emailFile, 'w')
f.write('devEmail=')
f.write(emails.strip(','))
f.close()
print '-'*10 +'Create environment file successfully'+ '-'*10