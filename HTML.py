#!/usr/bin/python

def title(project, buildnum, latestbuild, currentTime, description):
    header =    '<header>\n<title>Commit Changes - %s Project</title>\n \
                <style type="text/css">\n \
                .pass {background:green;}\n \
                .success {background:#ACF0AC;}\n \
                .fail {background:red;}\n \
                .warn {background:yellow;}\n \
                .exist {background:orange;}\n \
                .normal {background: #e0e0e0;}\n \
                .centered {text-align: center;}\n \
                tr {background-color: #E0E0E0;}\n \
                td {padding: 2px 15px 2px 15px;}\n \
                th {padding: 5px 10px 5px 10px; font-weight: normal; background-color: #696969; color: #F0F0F0;}\n \
                </style>\n \
                </header>\n' % project

    body = '<body>\n<center>\n<h2>Commit Changes - %s Project</h2>\n' % project
    desc = '<table>\n \
            <tr>\n \
            <th>Current Build</th>\n \
            <th>Last Build</th>\n \
            <th>Build Time</th>\n \
            <th>Description</th>\n \
            </tr>\n \
            <tr>\n \
            <td align="center">%s</td>\n \
            <td align="center">%s</td>\n \
            <td align="center">%s</td>\n \
            <td align="center">%s</td>\n \
            </tr>\n \
            </table><p>\n' % (buildnum, latestbuild, currentTime, description)

    return header + body + desc

def table(data, repo, colspan):
    reports = data
    table = '<TABLE cellpadding="4" style="border: 1px solid #000000; border-collapse: collapse;" border="1">\n'
    repoName = '<tr>\n<th colspan="%s" align="center">%s</th>\n</tr>\n' % (colspan, repo)
    code= table + repoName
    
    for arrs in reports:
        code += '\n<tr>\n'
        for arr in arrs:
            row = '\n<td>%s</td>\n' % arr
            code += row
        code += '\n</tr>\n'
    code += '</TABLE><p>'
    return code