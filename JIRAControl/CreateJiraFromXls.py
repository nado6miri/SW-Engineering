import sys
import os

#for Jira control
from jira import JIRA
#for excel control
import xlsxwriter as xlswt
import openpyxl as xlsrd
#for time
from datetime import datetime
# for UI
from PyQt5 import uic, QtWidgets, QtGui

#http://hlm.lge.com/issue/rest/api/2/issue/GSWDIM-22476/
#http://hlm.lge.com/issue/rest/api/2/issue/TVPLAT-3963/

#http://hlm.lge.com/qi/rest/api/2/issue/QEVENTSEVT-7232/ - Q


DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'

userID = 'sungbin.na'
userPasswd = 'Sungbin'

dissue_dict = {
    'project': {'key': 'GSWDIM'},
    'components' : [ ],
    'summary': 'New issue from jira-python',
    'description': 'Look into this one',
    'parent' : { 'id' :  ''},
    'issuetype' : { 'name' : 'Sub-task' },
    #'issuetype': {'id': '5'},
    'assignee': {"name":"sungbin.na", "emailAddress":"sungbin.na@lge.com"},
    'labels' : ['Default_label'],
    'duedate' : '2018-04-30',
    #'customfield_10105' :[{"name":"sungbin.na","key":"sungbin.na","emailAddress":"sungbin.na@lge.com" },] #watchers
    'customfield_10105' :[ {"name":"sungbin.na" }, {"name":"insun.song" }] #watchers
}

def makeKeyList() :
    # read header and make key list to make jira json file
    keylist = []
    j = 1
    cols = ws.columns
    for col in cols :
        val = ws.cell(row = 1, column = j).value
        if(val is not None):
            keylist.append(val)
            j+=1
        else :
            pass
    return keylist

def setProject(keyword, value) :
    print(keyword, " = ", value)
    dissue_dict[keyword]['key'] = value

def setComponents(keyword, value) :
    print(keyword, " = ", value)
    comp_list = value.split(',')
    print(comp_list)
    comp = { 'name' : ''}
    for cl in comp_list :
        comp['name'] = cl
        dissue_dict[keyword].append(comp)
        print(comp)
    print(dissue_dict[keyword])

def makeJSON(key, value) :
    if (key == 'project') :
        setProject(key, value)
    elif (key == 'components'):
        setComponents(key, value)
    elif (key == 'issuetype'):
        print("Set issuetype")
        dissue_dict[key] = value
    elif (key == 'parent'):
        print("Set parent")
    elif (key == 'summary'):
        print("Set summary")
    elif (key == 'description'):
        print("Set description")
    elif (key == 'Assignee'):
        print("Set Assignee")
    elif (key == 'Reporter'):
        print("Set Reporter")
    elif (key == 'watcher'):
        print("Set watcher")
    elif (key == 'duedate'):
        print("Set duedate")
    elif (key == 'labels'):
        print("Set labels")
    elif (key == 'comment'):
        print("Set comment")
    elif (key == 'attachment'):
        print("Set attachment")
    elif (key == 'Common Notice'):
        print("Set Common Notice")
    else :
        print("[Error] Set default="+key)



if __name__ == "__main__" :

    # 엑셀파일 열기
    excel_file = xlsrd.load_workbook('Jira_Issue.xlsm')
    ws = excel_file['Dev Tracker']

    jira_keylist = makeKeyList()
    print(jira_keylist)

    i = 1
    j = 1
    rows = ws.rows
    for row in rows :
        if(i == 1) : i+=1; j = 1; continue
        for key in jira_keylist :
            if(key == 'Key') :
                j = 2; continue
            val = ws.cell(row = i, column = j).value
            #print("=====================")
            #print(key, val)
            #print("=====================")
            makeJSON(key, val)
            j += 1
        i += 1

    '''
    cols = ws.columns
    rows = ws.rows
    i = j = 1
    for row in rows :
        j = 2
        for col in cols :
            makeJSON(ws.cell(row = i, column = j).value, ws.cell(row = i, column = j).value)
            j+=1
        i+=1
    '''







    '''
    # 모든 row 접근
    rows = ws.rows
    for row in rows :
        print(row[0].value)
        print(row[1].value)
        print(row[2].value)

    # 모든 col 접근
    cols = ws.columns
    for col in cols :
        print(col[0].value)
        print(col[1].value)
        print(col[2].value)
    '''

    '''
    dev_jira = JIRA(DevTracker, basic_auth = (userID, userPasswd))
    q_jira = JIRA(QTracker, basic_auth = (userID, userPasswd))

    #====================================================================================================================
    # Dev Trakcer
    #====================================================================================================================
    # Get issue with All Fields in Dev Tracker
    dissue = dev_jira.issue("LEADSWETDI-1")
    print("[Dev Tracker] Get JIRA Issue with All fields")


    #====================================================================================================================
    # How to create Jira Issue in Dev Tracker
    #====================================================================================================================
    # Case 1:
    new_dissue = dev_jira.create_issue(project='GSWDIM', summary='New issue from jira-python', description='Look into this one', issuetype={'name': 'Bug'})

    # Case 2:
    issue_dict = {
        'project': {'key': 'GSWDIM'},
        'components' : [ { 'name' : 'JIRATEST' } ],
        'summary': 'New issue from jira-python',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
        'assignee': {"name":"sungbin.na", "emailAddress":"sungbin.na@lge.com"},
        'labels' : ['Default_label'],
        'duedate' : '2018-04-30',
        #'customfield_10105' :[{"name":"sungbin.na","key":"sungbin.na","emailAddress":"sungbin.na@lge.com" },] #watchers
        'customfield_10105' :[ {"name":"sungbin.na" }, {"name":"insun.song" }] #watchers

    }
    issue_dict['labels'].append("VTASK")
    new_dissue = dev_jira.create_issue(fields=issue_dict)

    # Case 3:
    issue_list = [
    {
        'project': {'key': 'GSWDIM'},
        'components' : [ { 'name' : 'JIRATEST' } ],
        'summary': 'New issue from jira-python1',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
        'assignee': {"name":"sungbin.na", "emailAddress":"sungbin.na@lge.com"},
        'labels' : ['Default_label'],
        'duedate' : '2018-04-30',
        #'customfield_10105' :[{"name":"sungbin.na","key":"sungbin.na","emailAddress":"sungbin.na@lge.com" },] #watchers
        'customfield_10105' :[ {"name":"sungbin.na" }, ] #watchers
    },
    {
        'project': {'key': 'GSWDIM'},
        'components' : [ { 'name' : 'JIRATEST' } ],
        'summary': 'New issue from jira-python2',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
        'assignee': {"name":"sungbin.na", "emailAddress":"sungbin.na@lge.com"},
        'labels' : ['Default_label'],
        'duedate' : '2018-04-30',
        #'customfield_10105' :[{"name":"sungbin.na","key":"sungbin.na","emailAddress":"sungbin.na@lge.com" },] #watchers
        'customfield_10105' :[ {"name":"sungbin.na" }, ] #watchers
    },
    {
        'project': {'key': 'GSWDIM'},
        'components' : [ { 'name' : 'JIRATEST' } ],
        'summary': 'New issue from jira-python3',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
        'assignee': {"name":"sungbin.na", "emailAddress":"sungbin.na@lge.com"},
        'labels' : ['Default_label'],
        'duedate' : '2018-04-30',
        #'customfield_10105' :[{"name":"sungbin.na","key":"sungbin.na","emailAddress":"sungbin.na@lge.com" },] #watchers
        'customfield_10105' :[ {"name":"sungbin.na" }, ] #watchers
    },
    ]
    new_dissue = dev_jira.create_issue(fields=issue_list)

    #====================================================================================================================
    # How to create SubTask in Dev Tracker
    #====================================================================================================================
    subissue_dict = {
        'project': {'key': 'GSWDIM'},
        'components' : [ { 'name' : 'JIRATEST' } ],
        'summary': 'New issue from jira-python',
        'description': 'Look into this one',
        'parent' : { 'id' :  ''},
        'issuetype' : { 'name' : 'Sub-task' },
        #'issuetype': {'id': '5'},
        'assignee': {"name":"sungbin.na", "emailAddress":"sungbin.na@lge.com"},
        'labels' : ['Default_label'],
        'duedate' : '2018-04-30',
        #'customfield_10105' :[{"name":"sungbin.na","key":"sungbin.na","emailAddress":"sungbin.na@lge.com" },] #watchers
        'customfield_10105' :[ {"name":"sungbin.na" }, {"name":"insun.song" }] #watchers
    }

    subissue_dict['parent']['id'] = new_dissue.key
    subissue_dict['labels'].append("VTASK")
    new_dissue = dev_jira.create_issue(fields=subissue_dict)


    #====================================================================================================================
    # How to update Jira Info in Dev Tracker
    #====================================================================================================================
    # Case 1:
    dissue = dev_jira.issue("LEADSWETDI-1")
    dissue.update(notify=True, summary='new summary', description='A new summary was added')

    # Case 2:
    dissue = dev_jira.issue("GSWDIM-22479")
    updateissue_dict = {
        'components' : [ { 'name' : 'JIRATEST' } ],
        'summary': 'New issue from jira-python - Update',
        'description': 'Look into this one - Update',
        'assignee': {"name":"insun.song"},
        'labels' : ['Default_label_Update'],
        'duedate' : '2018-05-30',
        #'customfield_10105' :[{"name":"sungbin.na","key":"sungbin.na","emailAddress":"sungbin.na@lge.com" },] #watchers
        'customfield_10105' :[{"name":"insun.song" }] #watchers

    }
    dissue.update(notify=True, fields = updateissue_dict)
    #issue.update(notify=True, assignee={'name': 'insun.song'})
    dissue.update(labels=['AAA', 'BBB'])


    #====================================================================================================================
    # How to reassign an Issue in Dev Tracker
    #====================================================================================================================
    issue = dev_jira.issue("GSWDIM-22479")
    dev_jira.assign_issue(issue, 'sungbin.na')


    #====================================================================================================================
    # How to delete an Issue in Dev Tracker
    #====================================================================================================================
    issue = dev_jira.issue("GSWDIM-22475") # if the issue has subtasks, can't delete it.
    issue.delete()


    #====================================================================================================================
    # How to add comment to Issue in Dev Tracker
    #====================================================================================================================
    # Case 1:
    comment = dev_jira.add_comment('GSWDIM-22479', 'new comment')    # no Issue object required

    # Case 2:
    issue = dev_jira.issue("GSWDIM-22479")
    comment = dev_jira.add_comment(issue, 'new comment', visibility={'type': 'role', 'value': 'Administrators'})  # for admins only
    comment.update(body = 'updated comment body')
    comment.delete()

    # Case 3:
    dissue = dev_jira.issue("GSWDIM-22479")
    comment = dissue.raw['fields']['comment']
    comments = comment['comments']
    for c in comments :
        print(c)
        print("===================================")
        print(c['body'])
        print("===================================")


    #====================================================================================================================
    # How to Add / Remove Watcher to Issue in Dev Tracker
    #====================================================================================================================
    issue = dev_jira.issue("GSWDIM-22479")
    watcher = dev_jira.watchers(issue)
    print("Issue has {} watcher(s)".format(watcher.watchCount))
    for watcher in watcher.watchers:
        print(watcher)
        # watcher is instance of jira.resources.User:
        print(watcher.emailAddress)

    dev_jira.add_watcher(issue, 'sungbin.na')
    dev_jira.revmove_watcher(issue, 'sungbin.na')



    #===========================================================================
    # Attachment control in Dev Tracker
    issue = dev_jira.issue("GSWDIM-22479")
    #jira.add_attachment(issue=issue, attachment='Jira_자동_등록 - webOS4.0 Issue.xlsm')

    # read and upload a file (note binary mode for opening, it's important):
    with open('Jira_자동_등록 - webOS4.0 Issue.xlsm', 'rb') as f:
        jira.add_attachment(issue=issue, attachment=f)

    # attach file from memory (you can skip IO operations). In this case you MUST provide `filename`.
    import StringIO
    attachment = StringIO.StringIO()
    attachment.write(data)
    jira.add_attachment(issue=issue, attachment=attachment, filename='content.txt')


    #===========================================================================
    # Q Trakcer
    #===========================================================================
    # Get issue with All Fields in Q Tracker
    qissue = q_jira.issue("WOSLQEVENT-98853")
    print("[Dev Tracker] Get JIRA Issue with All fields")

    # Get issue with specific Fields in Q Tracker
    setfield = ('summary, comment, assignee')
    qissue = q_jira.issue("LEADSWETDI-1", fields=setfield)
    print("[Dev Tracker] Get JIRA Issue with Specific fields")

    #===========================================================================
    # Get filtered issue with Filter ID in Q Tracker
    setFilterID = 'filter = 95949'
    qissue = q_jira.search_issues(setFilterID)
    print("[QTracker] Get JIRA Issue with Specific Filter ID: " + setFilterID)

    # Get Filtered issue with JQL Querfy String in Q Tracker
    setFilter = 'Filter in (M3.LK61.EU.QA1, M3.LK61.EU.QA2, M3.LK61.EU.QA3, M3.LK61.EU.QA4)'
    qissue = q_jira.search_issues(setFilter)
    print("[QTracker] Get JIRA Issue with Specific Filter String: " + setFilter)
    '''
