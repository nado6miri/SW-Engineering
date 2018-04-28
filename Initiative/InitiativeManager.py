import sys
import os
import copy
import time

#for Jira control
from jira import JIRA
from jira.exceptions import JIRAError

#pip install XlsxWriter

#xlsxwriter
#https://xlsxwriter.readthedocs.io/index.html

#openpyxl
#http://www.hanul93.com/openpyxl-basic/
#https://openpyxl.readthedocs.io/en/stable/defined_names.html



#http://hlm.lge.com/issue/rest/api/2/issue/GSWDIM-22476/
#http://hlm.lge.com/issue/rest/api/2/issue/TVPLAT-3963/
#http://hlm.lge.com/issue/rest/api/2/issue/TVPLAT-3963/editmeta
#http://hlm.lge.com/qi/rest/api/2/issue/QEVENTSEVT-7232/ - Q

import openpyxl as xlsrd
from datetime import datetime
import copy

DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'

startSP = 'TVSP16_1'
endSP = 'TVSP17_2'
updateSP = 'TVSP18_1'

Sprint_Info = {
    'TVSP16_1' : '',  'TVSP16_2' : '',  'TVSP17_1' : '',  'TVSP17_2' : '',
    'TVSP18_1' : '',  'TVSP18_2' : '',  'TVSP19_1' : '',  'TVSP19_2' : '',
    'TVSP20_1' : '',  'TVSP20_2' : '',  'TVSP21_1' : '',  'TVSP21_2' : '',
    'TVSP22_1' : '',  'TVSP22_2' : '',  'TVSP23_1' : '',  'TVSP23_2' : '',
    'TVSP24_1' : '',  'TVSP24_2' : '',  'TVSP25_1' : '',  'TVSP25_2' : '',
    'TVSP26_1' : '',  'TVSP26_2' : '',  'TVSP27_1' : '',  'TVSP27_2' : '',
    'TVSP28_1' : '',  'TVSP28_2' : '',  'TVSP29_1' : '',  'TVSP29_2' : '',
    'TVSP30_1' : '',  'TVSP30_2' : '',  'TVSP31_1' : '',  'TVSP31_2' : '',
    }


epic_info = {
        'Key' : '',
        'Release_SP' : '',
        'Summary' : "",
        'assignee' : '',
        'duedate' : '',
        'status' : '',
        'TVSP' : { },
    }

initiative_info = {}
jira_initiative_keylist = []
jira_epic_keylist = []

tmp = {
    'Initiative Key' : '',
    'Summary' : '',
    'Assignee' : '',
    'Status' : '',
    'Release_SP' : '',
    'CreatedDate' : '',
    '관리대상' : '',
    'Risk 관리 대상' : '',
    'Initiative Order' : '',
    'Epic Key' : '',
    'EPIC' : [],
    'DEMO' : [],
    'CCC' : [],
    'TestCase' : [],
    'Dev_Verification' : [],
    'TVSP' : {},
    }

org_init_list = [
    {
        'Initiative Key' : 'TVPLAT-XXXX',
        'EPIC' : [],
        'DEMO' : [],
        'CCC' : [],
        'TestCase' : [],
        'Dev_Verification' : [],
        'summary' : 'Initiative summary1',
        'assignee' : 'taesun.song',
        'status' : 'Ready',
        'release SP' : 'TVSP23',
        'Created Date' : '20180301',
        'TVSP' : {},
    },]


#####################################################################################################################
# JIRA Control
maxResultCnt = 3000

#===========================================================================
# Get filtered issue with Filter ID in Dev Tracker
# filter 지정을 통한 Initiative 검색
#===========================================================================
def getFilterIDResult(jiraHandle, filterId, getFieldList=()) :
    setFilterID = 'filter = ' + str(filterId)
    print('strFilterID =', setFilterID)
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
        #print("key = ", value)
        return value

    #print("key = Null")
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

#####################################################################################################################
# Exel Control

#===========================================================================
# Get row count of excel (with Data)
# [param] Sheetname : Excel Sheet handle
# [param] rowpos : start row position of Data ( 1 ~ XXXX )
# [param] colpos : reference col index to detect exact row count (This column should be filled with data)
# [return] row count
#===========================================================================
def getRowCount(Sheetname, rowpos, colpos) :
    for i in range(rowpos, 50000) :
        val = Sheetname.cell(row = i, column = colpos).value
        if(val == None) :
            break;

    print("Row Count of ", Sheetname, " = ", i-rowpos)
    return (i-rowpos)


#===========================================================================
# Get Column count of excel (with Data)
# [param] Sheetname : Excel Sheet handle
# [param] rowpos : start row position of Title / Header
# [param] colpos : start col position of title
# [return] column count
#===========================================================================
def getColumnCount(Sheetname, rowpos, colpos) :
    for i in range(colpos,50000) :
        val = Sheetname.cell(row = rowpos, column = i).value
        if(val == None) :
            break;

    print("Column Count of ", Sheetname, " = ", i-colpos)
    return (i-colpos)



#===========================================================================
# Get Column Index of excel (with title)
# [param] Sheetname : Excel Sheet handle
# [param] rowpos : start row position of Title / Header
# [return] column Index
#===========================================================================
def getColumnIndex(Sheetname, row, title) :
    index = 1
    for col in range(1, Sheetname.max_column) :
        if(title == str(Sheetname.cell(row = row, column = col).value)) :
            break;
        index += 1

    if (Sheetname.max_column <= index) :
        index = None
        #print("title = ", title, " : Can't find title in exel")
    else :
        #print("title = ", title, ", Index = ", index)
        pass

    return (index)



#===========================================================================
# Get row Index of initiative to find
# [param] Sheetname : Excel Sheet handle
# [param] InitiativeKey : InitiativeKey to find
# [return] row Index or 0 (Not found)
#===========================================================================
def getInitiativeRowIndex(Sheetname, InitiativeKey) :
    isFound = False
    for row_index in range(1, MAX_RowCount+1) :
        type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
        if(type == "Initiative") :
            keyvalue = str(Sheetname.cell(row = row_index, column = CI_InitKey).value).strip()
            if(keyvalue == InitiativeKey) :
                isFound = True
                #print("Found Initiative Key of ", Sheetname, " : Key = ", InitiativeKey, ", Index = ", row_index)
                break;

    if(isFound == False) :
        #print("Not Found Initiative Key of ", Sheetname, " : Key = ", InitiativeKey, ", Index = ", row_index)
        row_index = 0

    return row_index




#===========================================================================
# Get row Index of Epic to find
# [param] Sheetname : Excel Sheet handle
# [param] InitiativeKey : Epic to find
# [return] row Index or 0 (Not found)
#===========================================================================
def getEpicRowIndex(Sheetname, EpicKey) :
    isFound = False
    for row_index in range(1, MAX_RowCount+1) :
        type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
        if(type == "EPIC") :
            keyvalue = str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip()
            if(keyvalue == EpicKey) :
                isFound = True
                #print("Found Epic Key of ", Sheetname, " : Key = ", EpicKey, ", Index = ", row_index)
                break;

    if(isFound == False) :
        #print("Not Found Epic Key of ", Sheetname, " : Key = ", EpicKey, ", Index = ", row_index)
        row_index = 0

    return row_index


#===========================================================================
# Get title list of header / title
# [param] Sheetname : Excel Sheet handle
# [param] row : start row position of Title / Header
# [param] col : start col position of title
# [return] title[]
#===========================================================================
def getTitleListfromXls(Sheetname, row, col) :
    title = []
    for i in range(col, MAX_ColCount+1) :
        title.append(str(Sheetname.cell(row = row, column = i).value).strip())

    #print("Title List of ", Sheetname, " = ", title)
    return title



#===========================================================================
# Get All Initiative Key List from Excel
# [param] Sheetname : Excel Sheet handle
# [param] rowpos : start row position of Data ( 1 ~ XXXX )
# [return] Initiative Key List[ 'KEY1', 'KEY2', ... ]
#===========================================================================
def getInitiativeKeylist(Sheetname, row) :
    initative_key = []
    for row_index in range(row, MAX_RowCount+1) :
        type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
        if(type == "Initiative") :
            initative_key.append(str(Sheetname.cell(row = row_index, column = CI_InitKey).value).strip())

    #print("Initiative Key List of ", Sheetname, " = ", initative_key)
    return initative_key


#===========================================================================
# Get All Epic Key List from Excel
# [param] Sheetname : Excel Sheet handle
# [param] rowpos : start row position of Data ( 1 ~ XXXX )
# [return] Epic Key List[ 'KEY1', 'KEY2', ... ]
#===========================================================================
def getEpicKeyListfromXls(Sheetname, row) :
    epic_key = []
    for row_index in range(row, MAX_RowCount+1) :
        type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
        if(type == "EPIC") :
            epic_key.append(str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip())

    #print("Epic Key List of ", Sheetname, " = ", epic_key)
    return epic_key



#===========================================================================
# Get Sprint History (dict) from Excel
# [param] Sheetname : Excel Sheet handle
# [param] KeyID : Initiative or Epic Key to get Sprint History from excel
# [return] Sprint_Info{ 'SP16_1' : '', 'SP16_2' : '', .... }
#===========================================================================
def getSprintHistoryfromXls(Sheetname, KeyID, IssueType) :
    global initiative_info
    if(IssueType == "Initiative") :
        rowIndex = getInitiativeRowIndex(Sheetname, KeyID)
    elif (IssueType == "EPIC") :
        rowIndex = getEpicRowIndex(Sheetname, KeyID)
    else :
        pass

    if(rowIndex == 0) :
        pass
    else :
        for col_index in range(CI_StartPos, CI_EndPos+1) :
            tvspstr = str(Sheetname.cell(row = 2, column = col_index).value).strip()
            Sprint_Info[tvspstr] = str(Sheetname.cell(row = rowIndex, column = col_index).value).strip()

        if(IssueType == "Initiative") :
            #print("===============Update Initiative Sprint_Info===================== Row Index =", rowIndex)
            pass
        elif (IssueType == "EPIC") :
            #print("===============Update Epic Sprint_Info===================== Row Index =", rowIndex)
            pass
    #print (Sprint_Info)
    return Sprint_Info



#===========================================================================
# Get Epic Information from Excel
# [param] Sheetname : Excel Sheet handle
# [param] EpicKey : Epic Key to get detail information from excel
# [return] epic_info { 'key' : '', 'summary' : '', Sprint_Info{ 'SP16_1' : '', 'SP16_2' : '', .... } }
#===========================================================================
def getEpicInfofromXls(Sheetname, EpicKey) :
    global initiative_info

    for row_index in range(1, MAX_RowCount+1) :
        getEpicKey = str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip()
        epic_info["Release_SP"] = str(Sheetname.cell(row = row_index, column = CI_ReleaseSP).value).strip()

        if(getEpicKey == EpicKey) :
            epic_info['Key'] = getEpicKey
            spInfo = getSprintHistoryfromXls(cur_sheet, getEpicKey, "EPIC")
            epic_info['TVSP'] = spInfo

    return epic_info



#===========================================================================
# Get All Initiative - Epic Lists from Excel
# [param] Sheetname : Excel Sheet handle
# [return] epic_key [ { 'key' : 'Initative Key',  'epiclist' : [ 'Epic Key1', 'Epic Key2', ... ]}, ....  }
#===========================================================================
def getInitiativeAllEpicsListfromXls(Sheetname) :
    epic_key = []
    keylist = getInitiativeKeylist(Sheetname, 3)

    for keyID in keylist :
        tmp = { 'key' : '', 'epiclist' : []}
        tmp['key'] = keyID
        for row_index in range(1, MAX_RowCount+1) :
            type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
            epicparent = str(Sheetname.cell(row = row_index, column = CI_InitKey).value).strip()
            if(type == 'EPIC' and epicparent == keyID) :
                tmp['epiclist'].append(str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip())
        epic_key.append(tmp)

    #print("*********** All Epic key List from Xls **********************")
    #print(epic_key)
    return epic_key


#===========================================================================
# Get a specific Initiative - Epic Lists from Excel
# [param] Sheetname : Excel Sheet handle
# [param] InitiativeKey : Initiative Key to get Epic Lists
# [return] EpicList[ 'Epic Key1', 'Epic Key2', ... ]
#===========================================================================
def getInitiativeEpicsListfromXls(Sheetname, InitiativeKey) :
    epic_key = []
    for row_index in range(1, MAX_RowCount+1) :
        type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
        getInitkey = str(Sheetname.cell(row = row_index, column = CI_InitKey).value).strip()
        if(type == "EPIC" and InitiativeKey == getInitkey) :
            epic_key.append(str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip())

    #print("Initiative Key = ", InitiativeKey, " Epic Key List of ", Sheetname, " = ", epic_key)
    return epic_key



#===========================================================================
# Get All Initiative - Epic Lists from Jira
# [param] filterResult : Jira Result from Filtered JIRA Query
# [return] list[ { 'key' : 'Initative Key',  'epiclist' : [ 'Epic Key1', 'Epic Key2', ... ]}, ....  }
#===========================================================================
def getInitiativeAllEpicsListfromJira(filterResult) :
    epic_key = []

    for dissue in filterResult :
        # Get issue with All Fields in Dev Tracker
        tmp = { 'key' : '', 'epiclist' : []}
        tmp['key'] = dissue.raw['key']
        bfound = False
        for issuelink in dissue.raw['fields']['issuelinks'] :
            if 'outwardIssue' in issuelink :
                if(issuelink['outwardIssue']['fields']['issuetype']['name'] == 'Epic') :
                    #print ("Key = ", dissue.raw['key'], " Status = ", issuelink['outwardIssue']['fields']['status']['name'], " Linked Issue = ", issuelink['outwardIssue']['key'])
                    tmp['epiclist'].append(issuelink['outwardIssue']['key'])
                    bfound = True
            if 'inwardIssue' in issuelink :
                if(issuelink['inwardIssue']['fields']['issuetype']['name'] == 'Epic') :
                    #print ("Key = ", dissue.raw['key'], " Status = ", issuelink['inwardIssue']['fields']['status']['name'], " Linked Issue = ", issuelink['inwardIssue']['key'])
                    tmp['epiclist'].append(issuelink['inwardIssue']['key'])
                    bfound = True

        if(bfound == True) :
            epic_key.append(tmp)

    #print("*********** Initiative - All Epic key List **********************")
    #print(epic_key)
    return epic_key



#===========================================================================
# Get All Epic Lists from Jira
# [param] filterResult : Jira Result from Filtered JIRA Query
# [return] epic_key[ 'Epic Key1', 'Epic Key2', ... ]
#===========================================================================
def getEpicKeyListfromJira(filterResult) :
    epic_key = []

    for dissue in filterResult :
        # Get issue with All Fields in Dev Tracker
        for issuelink in dissue.raw['fields']['issuelinks'] :
            if 'outwardIssue' in issuelink :
                if(issuelink['outwardIssue']['fields']['issuetype']['name'] == 'Epic') :
                    #print ("Key = ", dissue.raw['key'], " Status = ", issuelink['outwardIssue']['fields']['status']['name'], " Linked Issue = ", issuelink['outwardIssue']['key'])
                    epic_key.append(issuelink['outwardIssue']['key'])
            if 'inwardIssue' in issuelink :
                if(issuelink['inwardIssue']['fields']['issuetype']['name'] == 'Epic') :
                    #print ("Key = ", dissue.raw['key'], " Status = ", issuelink['inwardIssue']['fields']['status']['name'], " Linked Issue = ", issuelink['inwardIssue']['key'])
                    epic_key.append(issuelink['inwardIssue']['key'])

    # remove duplicate item in list
    epic_key = RemoveDuplicateInList(epic_key)

    #print("*********** All Epic key List from Jira **********************")
    #print(epic_key)
    return epic_key


#===========================================================================
# Get a specific Initiative - Epic Lists from Jira
# [param] jiraAllEpicList : list[ { 'key' : 'Initative Key',  'epiclist' : [ 'Epic Key1', 'Epic Key2', ... ]}, ....  }
# [param] InitiativeKey : Initiative Key to get Epic Lists
# [return] EpicList[ 'Epic Key1', 'Epic Key2', ... ]
#===========================================================================
def getInitiativeEpicsListfromJira(jiraAllEpicList, InitiativeKey) :
    epic_key = []

    for item in jiraAllEpicList :
        if (InitiativeKey == item['key']) :
            epic_key.append(item['epiclist'])

    #print("*********** Initiative Key = {0} Epic key from JIRA **********************".format(InitiativeKey))
    #print(epic_key)
    return epic_key



#===========================================================================
# Get the detail Initiative Information needed for history management from excel
# [param] Sheetname : Excel Sheet handle
# [param] keyList : List[ 'KEY1', 'KEY2', ... ]
# [return] initiative_info
#===========================================================================
def getInitiativeDetailInfofromXls(Sheetname, keyList) :
    for key in keyList :
        global initiative_info
        initiative_info = copy.deepcopy(tmp)

        rowIndex = getInitiativeRowIndex(Sheetname, key)

        if(rowIndex > 0) :
            print("\n######## {0} row - Update Initiative Detail information from Xls".format(rowIndex))
            initiative_info["Initiative Key"] = str(Sheetname.cell(row = rowIndex, column = CI_InitKey).value).strip()
            initiative_info["Release_SP"] = str(Sheetname.cell(row = rowIndex, column = CI_ReleaseSP).value).strip()
            initiative_info["관리대상"] = str(Sheetname.cell(row = rowIndex, column = 2).value).strip()
            initiative_info["Risk 관리 대상"] = str(Sheetname.cell(row = rowIndex, column = 3).value).strip()

            #SP
            spInfo = getSprintHistoryfromXls(cur_sheet, key, "Initiative")
            initiative_info['TVSP'] = spInfo

            #EPIC
            epic_list = getInitiativeEpicsListfromXls(cur_sheet, key)
            for epickey in epic_list :
                epicInfo = getEpicInfofromXls(cur_sheet, epickey)
                initiative_info['EPIC'].append(epicInfo)

            #print(initiative_info)

    return initiative_info



def getFilteredInitiativeInfofromJira(jiraHandle, filterid) :
    #Filter ID
    Initiative_webOS45_Initial_Dev = filterid

    #setfield = ('summary, duedate, assignee, status, created, components, labels')
    #result = getFilterIDResult(jiraHandle, Initiative_webOS45_Initial_Dev, setfield)
    if(Initiative_webOS45_Initial_Dev == 42101) :
        result = getFilterIDResult(jiraHandle, Initiative_webOS45_Initial_Dev)
    else :
        setfield = ('summary, comment, assignee, duedate, created, labels')
        result = getFilterIDResult(jiraHandle, Initiative_webOS45_Initial_Dev, setfield)

    return result



# Python code to remove duplicate elements
def RemoveDuplicateInList(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def getDiffList(listA, listB) :
    return (list(set(listA) - set(listB)))



if __name__ == "__main__" :
    # jira open
    dev_jira = JIRA(DevTracker, basic_auth = ("sungbin.na", "Sungbin@1805"))

    # create log file
    if (os.path.isfile("Initiative_logfile.txt")) :
        os.remove("Initiative_logfile.txt")

    log = open('Initiative_logfile.txt', 'wt')

    # workbook 만들기
    workbook = xlsrd.load_workbook('Initiative일정관리_180426_v1.xlsx')
    cur_sheet = workbook["최종"]

    # set Init data
    MAX_RowCount = getRowCount(cur_sheet, 3, 1)
    MAX_ColCount = getColumnCount(cur_sheet, 2, 1)

    # set position
    CI_IssueType = getColumnIndex(cur_sheet, 2, "Type")
    CI_EpicKey = getColumnIndex(cur_sheet, 2, "Epic Key")
    CI_InitKey = getColumnIndex(cur_sheet, 2, "Initiative Key")
    CI_ReleaseSP = getColumnIndex(cur_sheet, 2, "Release_SP")
    CI_StartPos = getColumnIndex(cur_sheet, 2, startSP)
    CI_EndPos = getColumnIndex(cur_sheet, 2, endSP)

    CI_Summary = getColumnIndex(cur_sheet, 2, "Summary")
    CI_Assignee = getColumnIndex(cur_sheet, 2, "Assignee")
    CI_Status = getColumnIndex(cur_sheet, 2, "Status")
    CI_Created = getColumnIndex(cur_sheet, 2, "CreatedDate")
    CI_InitOrder = getColumnIndex(cur_sheet, 2, "Initiative Order")


    xls_initiative_keylist = getInitiativeKeylist(cur_sheet, 3)
    base = getInitiativeDetailInfofromXls(cur_sheet, xls_initiative_keylist)

    # jira filtering
    Initiative_FilterResult = getFilteredInitiativeInfofromJira(dev_jira, 42101)
    Epic_FilterResult = getFilteredInitiativeInfofromJira(dev_jira, 42317)

    # data handling...
    for issue in Initiative_FilterResult :
        jira_initiative_keylist.append(getKey(issue))

    # Compare Initiative List ........
    print("\n New Initiative List ..........")
    newkey = getDiffList(jira_initiative_keylist, xls_initiative_keylist)
    print(newkey)
    print("\n Del Initiative List ..........")
    delkey = getDiffList(xls_initiative_keylist, jira_initiative_keylist)
    print(delkey)


    # Compare Epic List ........
    for issue in Epic_FilterResult :
        jira_epic_keylist.append(getKey(issue))

    jiralink_epic_keylist = getEpicKeyListfromJira(Initiative_FilterResult)

    print("\n Compare1 Epic List (jira filter - jira link)..........")
    newkey = getDiffList(jira_epic_keylist, jiralink_epic_keylist)
    print(newkey)
    print("\n Compare2 Epic List (jira link - jira filter)..........")
    delkey = getDiffList(jiralink_epic_keylist, jira_epic_keylist)
    print(delkey)



    '''
    finalList = jira_initiative_keylist
    finalList.extend(xls_initiative_keylist)
    finalList = RemoveDuplicateInList(finalList)
    print("\n#### Display the Final Initiative Key List to be managed by SPE Initiative members ####")
    print(finalList)

    # Update Already Deleted or unLinked Epic Issue
    for keyID in delkey :
        dissue = dev_jira.issue(keyID)
        base["Summary"] = getSummary(dissue)
        base["Assignee"] = getAssignee(dissue)
        base["Status"] = getStatus(dissue)
        base["CreatedDate"] = getCreatedDate(dissue)
        base["Initiative Order"] = getInitiativeOrder(dissue)
        pass

    print("\n#### Display the Base Data to be managed by SPE Initiative members ####")
    print(base)
    '''

    print("\n#### Start to update initiative information from JIRA Lastest Valule to be managed by SPE Initiative members ####")

    jira_epic_keylist = getInitiativeAllEpicsListfromJira(Initiative_FilterResult)
    getInitiativeEpicsListfromJira(jira_epic_keylist, 'TVPLAT-11806')
    xls_epic_keylist = getInitiativeAllEpicsListfromXls(cur_sheet)

    a = getEpicKeyListfromJira(Initiative_FilterResult)
    a = RemoveDuplicateInList(a)
    b = getEpicKeyListfromXls(cur_sheet, 3)
    b = RemoveDuplicateInList(b)

    print("\n New Epic List ..........")
    newEpickey = getDiffList(a, b)
    print(newEpickey)
    print("\n Del Epic List ..........")
    delEpickey = getDiffList(b, a)
    print(delEpickey)



    '''

    '''

    '''
    s = set(temp2)
    temp3 = [x for x in temp1 if x not in s]
    '''

    '''
    #log.write(a)
    #print(jira_initiative_keylist)
    '''

    '''
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
    '''

    '''
    # workbook 만들기
    row_count = Sheetname.max_row
    column_count = Sheetname.max_column
    print(row_count)
    print(column_count)
    getRowCount(Sheetname, 3, 1)
    getColumnCount(Sheetname, 2, 1)
    getColumnIndex(Sheetname, 2, "Initiative Key")
    getColumnIndex(Sheetname, 2, "aaa")
    getColumnIndex(Sheetname, 2, "기타")
    getColumnIndex(Sheetname, 2, "TVSP17-2")
    getColumnIndex(Sheetname, 2, "Signal")
    getInitiativeKeylist(Sheetname, 3, "Initiative Key")
    getTitleListfromXls(Sheetname, 2, 1)
    getInitiativeDetailInfofromXls(Sheetname)

    Sheetname['c5'] = 'demo-nsb'
    key = Sheetname['C4'].value
    print(key)
    workbook.save('webOS4.5_Initial-Initiative1.xlsx')
    '''
