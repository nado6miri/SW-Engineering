import sys
import os
#for Jira control
from jira import JIRA
#for excel control
import xlsxwriter as xlswt
import openpyxl as xlsrd
#for time
from datetime import datetime
#for UI
from PyQt5 import uic, QtWidgets, QtGui


DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'

#[Rest API]
#http://hlm.lge.com/issue/rest/api/2/issue/GSWDIM-22476/
#http://hlm.lge.com/issue/rest/api/2/issue/TVPLAT-3963/

#http://hlm.lge.com/qi/rest/api/2/issue/QEVENTSEVT-7232/ - Q


userID = 'sungbin.na'
userPasswd = 'Sungbin'


'''
# 엑셀파일 열기
excel_file = xlsrd.load_workbook('hello.xlsx')
excel_sheet = excel_file['Initiative']

for row in excel_sheet.rows :
    print(row[0].value)
'''

if __name__ == "__main__" :
    dev_jira = JIRA(DevTracker, basic_auth = (userID, userPasswd))
    q_jira = JIRA(QTracker, basic_auth = (userID, userPasswd))





    '''
    dissue = dev_jira.issue("GSWDIM-22479")
    comment = dissue.raw['fields']['comment']
    comments = comment['comments']
    for c in comments :
        print(c)
        print("===================================")
        print(c['body'])
        print("===================================")

    #====================================================================================================================
    # How to Create Jira Issue and Subtask........
    #====================================================================================================================
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

    #====================================================================================================================
    #Create SubTask
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
    # How to update Jira Info........
    #====================================================================================================================
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

    '''
