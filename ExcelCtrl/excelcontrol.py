#pip install XlsxWriter

#xlsxwriter
#https://xlsxwriter.readthedocs.io/index.html

#openpyxl
#http://www.hanul93.com/openpyxl-basic/
#https://openpyxl.readthedocs.io/en/stable/defined_names.html

import xlsxwriter as xlswt
import openpyxl as xlsrd
from datetime import datetime



workbook = xlswt.Workbook('hello.xlsx')
ws1 = workbook.add_worksheet(name='Initiative')
ws1.write('A1', 'Hello world')
ws1.write('A2', 'Hello world')
workbook.close()

# 엑셀파일 열기
excel_file = xlsrd.load_workbook('hello.xlsx')
excel_sheet = excel_file['Initiative']

for row in excel_sheet.rows :
    print(row[0].value)


excel_file.save("hello.xlsx")
excel_file.close()

'''
#worksheet.write(row, 1, '=SUM(B1:B4)')

worksheet = workbook.add_worksheet('Example1')

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Add a number format for cells with money.
money = workbook.add_format({'num_format': '$#,##0'})

# Write some data headers.
worksheet.write('A1', 'Item', bold)
worksheet.write('B1', 'Cost', bold)

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)

# Start from the first cell below the headers.
row = 1
col = 0

# Iterate over the data and write it out row by row.
for item, cost in (expenses):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost, money)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total',       bold)
worksheet.write(row, 1, '=SUM(B2:B5)', money)
'''
workbook.close()
