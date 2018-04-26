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

org_SP_Info = {
    'TVSP16_1' : '',  'TVSP16_2' : '',  'TVSP17_1' : '',  'TVSP17_2' : '',
    'TVSP18_1' : '',  'TVSP18_2' : '',  'TVSP19_1' : '',  'TVSP19_2' : '',
    'TVSP20_1' : '',  'TVSP20_2' : '',  'TVSP21_1' : '',  'TVSP21_2' : '',
    'TVSP22_1' : '',  'TVSP22_2' : '',  'TVSP23_1' : '',  'TVSP23_2' : '',
    'TVSP24_1' : '',  'TVSP24_2' : '',  'TVSP25_1' : '',  'TVSP25_2' : '',
    'TVSP26_1' : '',  'TVSP26_2' : '',  'TVSP27_1' : '',  'TVSP27_2' : '',
    'TVSP28_1' : '',  'TVSP28_2' : '',  'TVSP29_1' : '',  'TVSP29_2' : '',
    'TVSP30_1' : '',  'TVSP30_2' : '',  'TVSP31_1' : '',  'TVSP31_2' : '',
    }


org_epic_list = {
        'Key' : '',
        'Release_SP' : '',
        'Summary' : "",
        'assignee' : '',
        'duedate' : '',
        'status' : '',
        'TVSP' : { },
    }

org_initiative_info = {}
jira_initiative_keylist = []

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

#####################################################################################################################
# Exel Control

def getRowCount(Sheetname, rowpos, colpos) :
    for i in range(rowpos, 50000) :
        val = Sheetname.cell(row = i, column = colpos).value
        if(val == None) :
            break;

    print("Row Count of ", Sheetname, " = ", i-rowpos)
    return (i-rowpos)

def getColumnCount(Sheetname, rowpos, colpos) :
    for i in range(colpos,50000) :
        val = Sheetname.cell(row = rowpos, column = i).value
        if(val == None) :
            break;

    print("Column Count of ", Sheetname, " = ", i-colpos)
    return (i-colpos)


def getColumnIndex(Sheetname, row, title) :
    index = 1
    for col in range(1, Sheetname.max_column) :
        if(title == str(Sheetname.cell(row = row, column = col).value)) :
            break;
        index += 1

    if (Sheetname.max_column <= index) :
        index = None
        print("title = ", title, " : Can't find title in exel")
    else :
        print("title = ", title, ", Index = ", index)

    return (index)


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
        print("Not Found Initiative Key of ", Sheetname, " : Key = ", InitiativeKey, ", Index = ", row_index)
        row_index = 0

    return row_index


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
        print("Not Found Epic Key of ", Sheetname, " : Key = ", EpicKey, ", Index = ", row_index)
        row_index = 0

    return row_index


def getTitleListfromXls(Sheetname, row, col) :
    title = []
    for i in range(1, MAX_ColCount+1) :
        title.append(str(Sheetname.cell(row = row, column = i).value).strip())

    #print("Title List of ", Sheetname, " = ", title)
    return title



def getInitiativeKeyListfromXls(Sheetname, row) :
    initative_key = []
    for row_index in range(1, MAX_RowCount+1) :
        type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
        if(type == "Initiative") :
            initative_key.append(str(Sheetname.cell(row = row_index, column = CI_InitKey).value).strip())

    #print("Initiative Key List of ", Sheetname, " = ", initative_key)
    return initative_key



def getSprintHistoryfromXls(Sheetname, KeyID, IssueType) :
    global org_initiative_info
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
            org_SP_Info[tvspstr] = str(Sheetname.cell(row = rowIndex, column = col_index).value).strip()

        if(IssueType == "Initiative") :
            #print("===============Update Initiative org_SP_Info===================== Row Index =", rowIndex)
            pass
        elif (IssueType == "EPIC") :
            #print("===============Update Epic org_SP_Info===================== Row Index =", rowIndex)
            pass
    #print (org_SP_Info)
    return org_SP_Info


def getEpicInfofromXls(Sheetname, EpicKey) :
    global org_initiative_info

    for row_index in range(1, MAX_RowCount+1) :
        getEpicKey = str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip()
        org_epic_list["Release_SP"] = str(Sheetname.cell(row = row_index, column = CI_ReleaseSP).value).strip()

        if(getEpicKey == EpicKey) :
            org_epic_list['Key'] = getEpicKey
            spInfo = getSprintHistoryfromXls(cur_sheet, getEpicKey, "EPIC")
            org_epic_list['TVSP'] = spInfo


    return org_epic_list

def getInitiativeAllEpicsListfromXls(Sheetname) :
    epic_key = []
    tmp = { 'key' : '', 'epiclist' : []}
    tmp['key'] = dissue.raw['key']

    keylist = getInitiativeKeyListfromXls(Sheetname, 3)

    for keyID in keylist :
        tmp['key'] = keyID
        for row_index in range(1, MAX_RowCount+1) :
            type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
            epicparent = str(Sheetname.cell(row = row_index, column = CI_InitKey).value).strip()
            if(type == 'EPIC' and epicparent == keyID) :
                tmp['epiclist'].append(str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip())
        epic_key.append(tmp)

    print("*********** All Epic key List from Xls **********************")
    print(epic_key)
    return epic_key



def getInitiativeEpicsListfromXls(Sheetname, InitiativeKey) :
    epic_key = []
    for row_index in range(1, MAX_RowCount+1) :
        type = str(Sheetname.cell(row = row_index, column = CI_IssueType).value).strip()
        getInitkey = str(Sheetname.cell(row = row_index, column = CI_InitKey).value).strip()
        if(type == "EPIC" and InitiativeKey == getInitkey) :
            epic_key.append(str(Sheetname.cell(row = row_index, column = CI_EpicKey).value).strip())

    print("Initiative Key = ", InitiativeKey, " Epic Key List of ", Sheetname, " = ", epic_key)
    return epic_key



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

    #print("*********** All Epic key List **********************")
    #print(epic_key)
    return epic_key



def getInitiativeEpicsListfromJira(jiraAllEpicList, InitiativeKey) :
    epic_key = []

    for epic in jiraAllEpicList :
        if (InitiativeKey == epic['key']) :
            epic_key.append(epic['epiclist'])

    #print("*********** Epic key **********************")
    #print(epic_key)
    return epic_key




def getInitiativeDetailInfofromXls(Sheetname, keyList) :
    for key in keyList :
        global org_initiative_info
        org_initiative_info = copy.deepcopy(tmp)

        rowIndex = getInitiativeRowIndex(Sheetname, key)

        if(rowIndex > 0) :
            print("\n######## {0} row - Update Initiative Detail information from Xls".format(rowIndex))
            org_initiative_info["Initiative Key"] = str(Sheetname.cell(row = rowIndex, column = CI_InitKey).value).strip()
            org_initiative_info["Release_SP"] = str(Sheetname.cell(row = rowIndex, column = CI_ReleaseSP).value).strip()
            org_initiative_info["관리대상"] = str(Sheetname.cell(row = rowIndex, column = 2).value).strip()
            org_initiative_info["Risk 관리 대상"] = str(Sheetname.cell(row = rowIndex, column = 3).value).strip()

            #SP
            spInfo = getSprintHistoryfromXls(cur_sheet, key, "Initiative")
            org_initiative_info['TVSP'] = spInfo

            #EPIC
            epic_list = getInitiativeEpicsListfromXls(cur_sheet, key)
            for epickey in epic_list :
                epicInfo = getEpicInfofromXls(cur_sheet, epickey)
                org_initiative_info['EPIC'].append(epicInfo)

            #print(org_initiative_info)

    return org_initiative_info



def getFilteredInitiativeInfofromJira(jiraHandle, filterid) :
    #Filter ID
    Initiative_webOS45_Initial_Dev = filterid
    result = getFilterIDResult(jiraHandle, Initiative_webOS45_Initial_Dev)
    return result



# Python code to remove duplicate elements
def RemoveDuplicateInList(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def DiffBetweenLists(listA, listB) :
    return (list(set(listA) - set(listB)))
    print(newkey)


if __name__ == "__main__" :
    # jira open
    dev_jira = JIRA(DevTracker, basic_auth = ("sungbin.na", "Sungbin@1805"))

    # create log file
    if (os.path.isfile("Initiative_logfile.txt")) :
        os.remove("Initiative_logfile.txt")

    log = open('Initiative_logfile.txt', 'wt')

    # workbook 만들기
    workbook = xlsrd.load_workbook('Initiative일정관리_180423_v4.xlsx')
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


    xls_initiative_keylist = getInitiativeKeyListfromXls(cur_sheet, 3)
    base = getInitiativeDetailInfofromXls(cur_sheet, xls_initiative_keylist)

    # jira filtering
    filterResult = getFilteredInitiativeInfofromJira(dev_jira, 42101)

    # data handling...
    for issue in filterResult :
        jira_initiative_keylist.append(getKey(issue))

    newkey = DiffBetweenLists(jira_initiative_keylist, xls_initiative_keylist)
    print(newkey)
    delkey = DiffBetweenLists(xls_initiative_keylist, jira_initiative_keylist)
    print(delkey)

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


    print("\n#### Start to update initiative information from JIRA Lastest Valule to be managed by SPE Initiative members ####")

    result = getInitiativeAllEpicsListfromJira(filterResult)
    getInitiativeEpicsListfromJira(result, 'TVPLAT-11806')
    getInitiativeAllEpicsListfromXls(cur_sheet)

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
    getInitiativeKeyListfromXls(Sheetname, 3, "Initiative Key")
    getTitleListfromXls(Sheetname, 2, 1)
    getInitiativeDetailInfofromXls(Sheetname)

    Sheetname['c5'] = 'demo-nsb'
    key = Sheetname['C4'].value
    print(key)
    workbook.save('webOS4.5_Initial-Initiative1.xlsx')
    '''
