import sys
import os
import copy
import time

#for Jira control
from jira import JIRA
from jira.exceptions import JIRAError

#for excel control
import xlsxwriter as xlswt
from xlsxwriter.utility import xl_rowcol_to_cell
import openpyxl as xlsrd

import json

#for time
from datetime import datetime

# dir(jira)
# dir(jira.JIRA)
# hasattr(JIRA, crete_issue)

#http://hlm.lge.com/issue/rest/api/2/issue/GSWDIM-22476/
#http://hlm.lge.com/issue/rest/api/2/issue/TVPLAT-3963/
#http://hlm.lge.com/issue/rest/api/2/issue/TVPLAT-4013/editmeta

#http://hlm.lge.com/qi/rest/api/2/issue/QEVENTSEVT-7232/ - Q

DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'
userID = 'sungbin.na'
userPasswd = 'Sungbin@1801'

# filter를 통해 가져오고자 하는 Field 설정
initative_setfield = ('summary, comment, assignee, reporter, customfield_15228, customfield_15710, customfield_16988, customfield_16984, customfield_16987, customfield_15711, customfield_16986, duedate, labels, updated, created, duedate, resolutiondate, resolution, status, components, description, issuetype, fixVersions, customfield_15926, issuelinks, customfield_15104, customfield_16986, parent')

'''
'customfield_15228' : [ { 'name' : ''}, ]   # STE/QE 담당자
'customfield_15710' : 'Status Summary'      # Status Summary
'customfield_16988' : { 'value' : 'Green' } # SE_Delivery
'customfield_16984' : 'D_Comment'           # D_Comment
'customfield_16987' : { 'value' : 'Green' } # SE_Quality
'customfield_16983' : 'Q_Comment'           # Q_Comment
'customfield_15711' : { 'value' : 'Green' } # Status Color
'customfield_16986' : 10    # Initiative Order
'duedate' : "2018-04-03T08:53:10.000+0900"
'comment' : { 'startAt' : '', 'maxResults' : '', 'total' : '', 'comments' : [ { },]} }
'labels' : ['', ],
'updated' : "2018-04-03T08:53:10.000+0900"
'created' : "2018-04-03T08:53:10.000+0900"
'duedate' : "2018-04-03T08:53:10.000+0900"
'resolutiondate' : "2018-04-03T08:53:10.000+0900"
'status' : { 'name' : "In Progress"}
'components' : [ { 'id' : "30780", 'name' : "comp_name" }, ]
'description' : "description......"
'issuetype' : { 'name' : '' }
'project': {'key': ''},
'fixVersions' : [ { 'name' : ''}, ]
'customfield_15926' = [] # Release Sprint
'issuelinks' = [ { '' : ''}, ]
'customfield_15104' : "Local Change"
'customfield_16986' : 89  # Initiative Score
'parent' : { 'id' :  ''},
'customfield_10436' :'', # Epic Name
'resolution' :'',
'''

maxResultCnt = 1000

#===========================================================================
# Get filtered issue with Filter ID in Dev Tracker
# filter 지정을 통한 Initiative 검색
#===========================================================================
def getFilterIDResult(jiraHandle, filterId, getFieldList=()) :
    setFilterID = 'filter =' + str(filterId)
    print('strFilterID = ', setFilterID)
    #resultIssue = jiraHandle.search_issues(setFilterID, startAt = 0, maxResults = 1000, fields = setfield, expand=None)
    resultIssue = jiraHandle.search_issues(setFilterID, startAt = 0, maxResults = maxResultCnt, fields = getFieldList, expand=None)
    print("[Tracker] Get JIRA Issue with Specific Filter ID: " + setFilterID)
    return resultIssue


#===========================================================================
# Get filtered issue with Filter ID in Dev Tracker
# Query 지정을 통한 Initiative 검색
#===========================================================================
def getFilterQueryResult(jiraHandle, filterQuery, getFieldList=None) :
    # Get Filtered issue with JQL Querfy String in Q/Dev Tracker
    #setFilter = 'Filter in (M3.LK61.EU.QA1, M3.LK61.EU.QA2, M3.LK61.EU.QA3, M3.LK61.EU.QA4)'
    resultIssue = jiraHandle.search_issues(filterQuery, startAt = 0, maxResults = maxResultCnt, fields = getFieldList, expand=None)
    print("[Tracker] Get JIRA Issue with Specific Filter String: " + filterQuery)
    return resultIssue


#===========================================================================
# Get Key of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getKey(jiraIssue) :
    value = jiraIssue.raw['key']
    if(value != None) :
        print("key = ", value)
        return value

    print("key = Null")
    return None


#===========================================================================
# Get Summary of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getSummary(jiraIssue) :
    value = jiraIssue.raw['fields']['summary']
    if(value != None) :
        print("summary = ", value)
        return value

    print("summary = Null")
    return None


#===========================================================================
# Get Status of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getStatus(jiraIssue) :
    value = jiraIssue.raw['fields']['status']['name']
    print("status = ", value)
    return value


#===========================================================================
# Get issuetype of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getIssuetype(jiraIssue) :
    value = jiraIssue.raw['fields']['issuetype']['name']
    print("issuetype = ", value)
    return value


#===========================================================================
# Get resolution of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getResolution(jiraIssue) :
    value = jiraIssue.raw['fields']['resolution']
    print("resolution = ", value)
    return value


#===========================================================================
# Get components of jira
# [param] jiraIssue : json object of jira
# [return] components[]
#===========================================================================
def getComponents(jiraIssue) :
    value = jiraIssue.raw['fields']['components']

    if(value != None) :
        print("components = ", json.dumps(value))
        return value

    print("components = Null")
    return None


#===========================================================================
# Get Release Sprint of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getReleaseSprint(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_15926']
    if(value != None) :
        print("Release Sprint = ", value)
        return value

    print("Release Sprint = Null")
    return None


#===========================================================================
# Get Status Summary of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getStatusSummary(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_15710']
    if(value != None) :
        print("Status Summary = ", value)
        return value

    print("Status Summary = Null")
    return None


#===========================================================================
# Get Status Color of jira
# [param] jiraIssue : json object of jira
# [return] str (RGB)
#===========================================================================
def getStatusColor(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_15711']
    if(value != None) :
        print("Status Color = ", json.dumps(value['value']))
        return value['value']

    print("Status Color = Null")
    return None


#===========================================================================
# Get SE_Delivery of jira
# [param] jiraIssue : json object of jira
# [return] str (RGB)
#===========================================================================
def getSE_Dilivery(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_16988']['value']
    if(value != None) :
        print("SE_Delivery = ", json.dumps(value))
        return value

    print("SE_Delivery = Null")
    return None


#===========================================================================
# Get SE_Quality of jira
# [param] jiraIssue : json object of jira
# [return] str (RGB)
#===========================================================================
def getSE_Quality(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_16987']
    if(value != None) :
        value = value['value']
        print("SE_Quality = ", json.dumps(value))
        return value

    print("SE_Quality = Null")
    return None

#===========================================================================
# Get D_Comment of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getD_Comment(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_16984']
    print("D_Comment = ", value)
    return value


#===========================================================================
# Get Q_Comment of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getQ_Comment(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_16983']
    print("Q_Comment = ", value)
    return value


#===========================================================================
# Get STE Member List of jira
# [param] jiraIssue : json object of jira
# [return] QE[]
#===========================================================================
def getSTEList(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_15228']
    if(value != None) :
        print("STE_List[] = ", json.dumps(value))
        return value

    print("STE_List[] = Null")
    return None


#===========================================================================
# Get Initiative Order of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getInitiativeOrder(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_16986']
    print("Initiative Order = ", value)
    return value


#===========================================================================
# Get Initiative Score of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getInitiativeScore(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_16985']
    print("Initiative Score = ", value)
    return value

#===========================================================================
# Get Created Date of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getCreatedDate(jiraIssue) :
    value = jiraIssue.raw['fields']['created']
    print("Created Date = ", value)
    return value


#===========================================================================
# Get Updated Date of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getUpdatedDate(jiraIssue) :
    value = jiraIssue.raw['fields']['updated']
    print("Updated Date = ", value)
    return value


#===========================================================================
# Get Due Date of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getDueDate(jiraIssue) :
    value = jiraIssue.raw['fields']['duedate']
    print("Due Date = ", value)
    return value

#===========================================================================
# Get Resolution Date List of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getResolutionDate(jiraIssue) :
    value = jiraIssue.raw['fields']['resolutiondate']
    print("Resolutiondate Date = ", value)
    return value


#===========================================================================
# Get Created Date List of jira
# [param] jiraIssue : json object of jira
# [return] labels []
#===========================================================================
def getLabels(jiraIssue) :
    value = jiraIssue.raw['fields']['labels']
    print("labels = ", value)
    return value

#===========================================================================
# Get Description List of jira
# [param] jiraIssue : json object of jira
# [return] labels [ 'a', 'b', .... ]
#===========================================================================
def getDescription(jiraIssue) :
    value = jiraIssue.raw['fields']['description']
    #print("description = ", value)
    return value

#===========================================================================
# Get fixVersions of jira
# [param] jiraIssue : json object of jira
# [return] fixVersions [ { 'name' : '' } ]
#===========================================================================
def getFixVersions(jiraIssue) :
    value = jiraIssue.raw['fields']['fixVersions']
    print("fixVersions = ", value)
    return value


#===========================================================================
# Get Scope of Change of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getScopeOfChange(jiraIssue) :
    value = jiraIssue.raw['fields']['customfield_15104']
    if(value != None) :
        print("Scope of Change = ", value['value'])
        return value['value']

    print("Scope of Change = Null")
    return None


#===========================================================================
# Get Issue Links of jira
# [param] jiraIssue : json object of jira
# [return] issuelinks[ {}, .... ]
#===========================================================================
def getIssueLinks(jiraIssue) :
    value = jiraIssue.raw['fields']['issuelinks']
    print("Issue Links = ", value)
    return value

#===========================================================================
# Get Reporter of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getReporter(jiraIssue) :
    value = jiraIssue.raw['fields']['reporter']['name']
    print("reporter = ", value)
    return value


#===========================================================================
# Get Assignee of jira
# [param] jiraIssue : json object of jira
# [return] str
#===========================================================================
def getAssignee(jiraIssue) :
    value = jiraIssue.raw['fields']['assignee']['name']
    print("assignee = ", value)
    return value


#===========================================================================
# Get Reporter of jira
# [param] jiraIssue : json object of jira
# [return] Watchers [ ] <== [ { 'name' : ''}, { 'emailAddress' : '' }, .... ]
#===========================================================================
def getWatchers(jiraIssue) :
    watchers = jiraIssue.raw['fields']['customfield_10105']
    results = []
    for watcher in watchers :
        results.append(watcher)

    print("Watcher List = ", results)
    return results

#===========================================================================
# Get Epics / Milestone block from Description of jira
# [param] description : description string
# [param] fieldtitle : Title of block like '*Milestone*'
# [return] str or None
#===========================================================================
strEpic = ["*개발 Epic 산정*", "*Epics*", "*EPICs*" ]
strMilestone = [ "*Milestone", "*Expected Deliveries*" ]

def getEpicsMilestoneFromDesc(description, fieldtitle) :
    startpos = description.find(fieldtitle)
    if(startpos > 1) :
        endpos = description.find('*', startpos + len(fieldtitle))

    if(startpos >= 1 and endpos > startpos):
        result = description[startpos:endpos]
        #print(result)
        return result

    print("getEpicsFromDesc = Null")
    return None



if __name__ == "__main__" :
    dev_jira = JIRA(DevTracker, basic_auth = (userID, userPasswd))
    q_jira = JIRA(QTracker, basic_auth = (userID, userPasswd))

    #Filter ID
    #Initiative_webOSTV45_Initial = 39060
    #result = getFilterIDResult(dev_jira, Initiative_webOSTV45_Initial)
    query = 'project = TVPLAT AND key = TVPLAT-7209'
    result = getFilterQueryResult(dev_jira, query)

    if (os.path.isfile("logfile.txt")) :
        os.remove("logfile.txt")

    log = open('logfile.txt', 'wt')


    for issue in result :
        print("###########################################################")
        a = getKey(issue)
        log.write(a)
        getSummary(issue)
        getStatusColor(issue)
        getAssignee(issue)
        getReleaseSprint(issue)
        getStatus(issue)
        getScopeOfChange(issue)
        desc = getDescription(issue)


        epics_desc = getEpicsMilestoneFromDesc(desc, strEpic)
        milestone_desc = getEpicsMilestoneFromDesc(desc, strMilestone)

        sprint = [ "SP16" ]
        print("================Epics===============")
        if(epics_desc != None) :
            epics_desc = epics_desc.splitlines(True)
            for word in sprint :
                for line in epics_desc :
                    if(line.find(word) != -1) :
                        line = line.replace(u'\xa0', ' ')
                        print(line)
                        log.write(line)
                    else :
                        msg = '{} {}'.format(sprint, "= Not Found\n")
                        #msg.encode('cp949')
                        log.write(msg)
                        #print(sprint, " = Not Found")
                        pass

        print("================Milestone===============")
        if(milestone_desc != None) :
            milestone_desc = milestone_desc.splitlines(True)
            for word in sprint :
                for line in milestone_desc :
                    if(line.find(word) != -1) :
                        line = line.replace(u'\xa0', 'Open')
                        print(line)
                        log.write(line)
                    else :
                        msg = '{} {}'.format(sprint, "= Not Found\n")
                        log.write(msg)
                        #print(sprint, " = Not Found")
                        pass
        #break

    log.close()
    '''
    query = 'project = TVPLAT AND issuetype = Initiative AND fixVersion in ("webOS TV 4.5 Initial")'
    result = getFilterQueryResult(dev_jira, query)

    for issue in result :
        print(issue, issue.raw['fields']['summary'])
        print(issue.raw['fields']['customfield_15926'])
    '''

# dict to str
#str_json = json.dumps({'my_key': 'my value'})
# str to dict
#dict_from_str_json = json.loads('{"my_key": "my value"}')


#GL2_IR2TVSP16
#19Y_TVSP9

'''
print("###########################################################")
print(issue, issue.raw['fields']['summary'])
print("issuetype = ", issue.raw['fields']['issuetype']['name'])
print("Status = ", issue.raw['fields']['status']['name'])
print("resolution = ", issue.raw['fields']['resolution'])
print("components = ", json.dumps(issue.raw['fields']['components']))
print("Rlease Sprint = ", issue.raw['fields']['customfield_15926'])
print("Status Summary = ", issue.raw['fields']['customfield_15710'])
getStatusColor(issue)
print("SE_Delivery = ", issue.raw['fields']['customfield_16988']['value'])
print("D_Comment = ", issue.raw['fields']['customfield_16984'])
getSE_Quality(issue)
print("Q_Comment = ", issue.raw['fields']['customfield_16983'])
getSTEList(issue)
print("STE 담당자 = ", json.dumps(issue.raw['fields']['customfield_15228']))
print("Initiative Order = ", issue.raw['fields']['customfield_16986'])
print("Initiative Score = ", issue.raw['fields']['customfield_16985'])
print("created = ", issue.raw['fields']['created'])
print("updated = ", issue.raw['fields']['updated'])
print("duedate = ", issue.raw['fields']['duedate'])
print("resolutiondate = ", issue.raw['fields']['resolutiondate'])
print("labels = ", issue.raw['fields']['labels'])
print("description = ", issue.raw['fields']['description'])
print("fixVersions = ", issue.raw['fields']['fixVersions'])
print("Scope of Change = ", issue.raw['fields']['customfield_15104'])
print("issuelinks = ", issue.raw['fields']['issuelinks'])
print("assignee = ", issue.raw['fields']['assignee']['name'])
print("reporter = ", issue.raw['fields']['reporter']['name'])
'''
