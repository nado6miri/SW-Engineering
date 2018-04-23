#pip install XlsxWriter

#xlsxwriter
#https://xlsxwriter.readthedocs.io/index.html

#openpyxl
#http://www.hanul93.com/openpyxl-basic/
#https://openpyxl.readthedocs.io/en/stable/defined_names.html

import openpyxl as xlsrd
from datetime import datetime


# workbook 만들기
workbook = xlsrd.load_workbook('webOS4.5_Initial-Initiative.xlsx')
sheet = workbook["최종"]
sheet['c5'] = 'demo-nsb'
key = sheet['C4'].value
print(key)
workbook.save('webOS4.5_Initial-Initiative1.xlsx')


org_epic_list = [
    {
        'Key' : 'TVPLAT-XXXX',
        'summary' : "epic title1",
        'assignee' : 'sungbin.na',
        'duedate' : '20180531',
        'status' : 'in-progress',
    },]

org_init_list = [
    {
        'Initiative Key' : 'TVPLAT-XXXX',
        'EPIC' : [],
        'summary' : 'Initiative summary1',
        'assignee' : 'taesun.song',
        'status' : 'Ready',
        'release SP' : 'TVSP23',
        'Created Date' : '20180301',
    },]

print(org_epic_list)

org_init_list[0]['EPIC'] = org_epic_list


print(org_init_list)
