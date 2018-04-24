#pip install XlsxWriter

#xlsxwriter
#https://xlsxwriter.readthedocs.io/index.html

#openpyxl
#http://www.hanul93.com/openpyxl-basic/
#https://openpyxl.readthedocs.io/en/stable/defined_names.html

import openpyxl as xlsrd
from datetime import datetime

org_SP_Info = [
    { 'SP16_1' : ''}, { 'SP16_2' : ''}, { 'SP17_1' : ''}, { 'SP17_2' : ''},
    { 'SP18_1' : ''}, { 'SP18_2' : ''}, { 'SP19_1' : ''}, { 'SP19_2' : ''},
    { 'SP20_1' : ''}, { 'SP20_2' : ''}, { 'SP21_1' : ''}, { 'SP21_2' : ''},
    { 'SP22_1' : ''}, { 'SP22_2' : ''}, { 'SP23_1' : ''}, { 'SP23_2' : ''},
    { 'SP24_1' : ''}, { 'SP24_2' : ''}, { 'SP25_1' : ''}, { 'SP25_2' : ''},
    { 'SP26_1' : ''}, { 'SP26_2' : ''}, { 'SP27_1' : ''}, { 'SP27_2' : ''},
    { 'SP28_1' : ''}, { 'SP28_2' : ''}, { 'SP29_1' : ''}, { 'SP29_2' : ''},
    { 'SP30_1' : ''}, { 'SP30_2' : ''}, { 'SP31_1' : ''}, { 'SP31_2' : ''},
]

org_epic_list = [
    {
        'Key' : 'TVPLAT-11693',
        'summary' : "epic title1",
        'assignee' : 'sungbin.na',
        'duedate' : '20180531',
        'status' : 'in-progress',
        'TVSP' : [],
    },]

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
        'TVSP' : [],
    },]


def getRowCount(rowpos, colpos, Sheetname) :
    print(Sheetname.cell(row = rowpos, column = colpos))
    print(Sheetname.cell(row = rowpos, column = colpos).value)

    for i in range(rowpos,50000) :
        val = Sheetname.cell(row = i, column = colpos).value
        if(val == None) :
            break;

    print(i-rowpos)
    return (i-rowpos)

def getColumnCount(rowpos, colpos, Sheetname) :
    print(Sheetname.cell(row = rowpos, column = colpos))
    print(Sheetname.cell(row = rowpos, column = colpos).value)

    for i in range(colpos,50000) :
        val = Sheetname.cell(row = rowpos, column = i).value
        if(val == None) :
            break;

    print(i-colpos)
    return (i-colpos)


def makeInitiativeInfofromExcel() :
    # workbook 만들기
    workbook = xlsrd.load_workbook('Initiative일정관리_180423_v4.xlsx')
    sheet = workbook["최종"]
    row_count = sheet.max_row
    column_count = sheet.max_column
    print(row_count)
    print(column_count)
    getRowCount(3, 1, sheet)
    getColumnCount(2, 1, sheet)

    '''
    sheet['c5'] = 'demo-nsb'
    key = sheet['C4'].value
    print(key)
    workbook.save('webOS4.5_Initial-Initiative1.xlsx')
    org_init_list[0]['EPIC'] = org_epic_list
    '''
    pass


def makeInitiativeInfofromJira() :
    pass


if __name__ == "__main__" :
    makeInitiativeInfofromExcel()


    '''
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
    '''
