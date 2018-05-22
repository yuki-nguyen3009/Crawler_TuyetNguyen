#!/usr/bin/python
import sys, os, re
from datetime import datetime
import HTML


def readFile(fileName):
    try:
        history = {}
        with open(fileName,'r') as f:
            for line in f:
                data = line.split('=')
                if len(data) > 1:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                    history[key] = value
        f.close()
    except IOError:
        print 'Fail to read file ' + fileName
        sys.exit(2)
    return history

def update(fileName, pre, last, repo, preBuild, buildNum):
    history = readFile(fileName)
    data =[]
    repo = repo.lower()
    for x in history:
        if x == '%s.previous.commit' % repo:
            history[x] = pre
        elif x == '%s.last.commit' % repo:
            history[x] = last
        elif x == 'last.build':
            history[x] = buildNum
        elif x == 'previous.build':
            history[x] = preBuild
        else:
            continue

    for y in history:
        key = y.lower()
        value = history[y]
        row = "%s=%s" % (key, value)
        data.append(row)
        data.sort()
    f = open(fileName, 'w')
    for line in data:
        f.write("%s\n" %line)
    f.close()

###get argument
projectName = sys.argv[1]
buildNum = str(sys.argv[2])
workspace = sys.argv[3]
source_path = sys.argv[4]

###Define varible
htmlFile = '%sCommitChange.html' % workspace
historyFile="%scommit-history" % workspace
commitsChange = "%scommits-change.csv" % workspace
currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
lastBuild = readFile(historyFile)['last.build']
htmlCode = []
reports = []
commitInfo = []
listRepo = os.listdir(source_path)
if buildNum == lastBuild:
    preBuild = readFile(historyFile)['previous.build']
else:
    preBuild = lastBuild

if os.path.exists(htmlFile):
    os.system("del %s" % htmlFile)

###Define command
fetchCmd = "git fetch --no-tags --depth 200"
newCommitCmd = "git log --pretty=format:%h -n 1"
print "-"*20 +"SCRIPT STARTING"+ "-"*20
###Get commit change
for repo in listRepo:
    if re.search('^[Ss]yn', repo):
        repoPath = source_path + repo
        os.chdir(repoPath)
        print "Fetch commits change to local %s repository.\n %s" % (repo, fetchCmd)
        gitFetch = os.system(fetchCmd)

        print "Get newest and latest commits ID on %s." % (repo)
        newCommit = os.popen(newCommitCmd).read().strip('\n')
        print "Newest commit ID is %s " % newCommit
        
        lastCommit = readFile(historyFile)[repo +".last.commit"]
        if newCommit == lastCommit:
            continue
        else:
            preCommit= lastCommit
            print "Last commit ID on previous build is %s" % preCommit

        print "Getting all commit between previous and current build on %s..." % repo
        diffCommitCmd = 'git log --merges --first-parent --pretty=format:%ci;%h;%s;%ae'+" %s..%s " % (preCommit, newCommit)
        diffCommit = os.popen(diffCommitCmd).read()

        #Insert commit information into HTML table
        print "Inserting all commits change on %s into HTML table..." % repo
        commits = diffCommit.split('\n')
        if len(commits) >= 1:
            reports.append(['Commit Date', 'Commit ID', 'Commit Comment', 'Author Email'])
            for commit in commits:
                commitInfo.append(repo +";"+ commit)
                fields = commit.split(';')
                reports.append(fields[0:4])

            #Generate html code
            tables = HTML.table(reports, repo, len(fields))
            htmlCode.append(tables)
            reports = []

        update(historyFile, preCommit, newCommit, repo, preBuild, buildNum)
    else:
        continue

f = open(htmlFile, 'w')

if len(commitInfo) < 1:
    print "Generating HTML report..."
    titles = HTML.title(projectName, buildNum, preBuild, currentTime, "There is no commit change.")
    f.write(titles)
    f.close()
    
    print "Backup all changes to use for post-build..."
    h = open(commitsChange, 'w')
    h.write("There is no commit change.")
    h.close()
else:
    print "Generating HTML report..."
    titles = HTML.title(projectName, buildNum, preBuild, currentTime, "There are %s commits change." % len(commitInfo))
    # Generate HTML file
    f.write(titles)
    for code in htmlCode:
        f.write(code)
    f.close()
    
    print "Backup all changes to use for post-build..."
    h = open(commitsChange, 'w')
    for line in commitInfo:
        h.write(line+";\n")
    h.close()

print "-"*20 +"SCRIPT FINISHED SUCCESSFUL"+ "-"*20