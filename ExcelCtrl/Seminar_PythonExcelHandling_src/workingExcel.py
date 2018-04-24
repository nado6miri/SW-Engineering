# -*- coding:utf-8 -*-
#--------------------------------------------------------------------------------------
#
# author : jinkyeong.yoo@lge.com
#
#--------------------------------------------------------------------------------------
#
# Excel File Read / Write 하기 위한 xlsxwriter, xlrd Wrapper class
#
#--------------------------------------------------------------------------------------
import sys
import os
import xlsxwriter
import xlrd
import types
from datetime import datetime

class CWorkingExcel():

    def __init__(self):
        print "[CWorkingExcel::__init__]"

    # --------------------------------------------------------------------
    # [out] True  : data가 숫자 type
    #       False : data가 숫자 type이 아니다.
    # --------------------------------------------------------------------
    def isNemeric(self,data):
        dataType = type(data)
        return ( dataType == types.FloatType or dataType == types.LongType or dataType == types.IntType)

    # --------------------------------------------------------------------
    # [out] True  : data가 문자 type
    #       False : data가 문자 type이 아니다.
    # --------------------------------------------------------------------
    def isString(self,  data) :
        dataType = type(data)
        return ( dataType == types.StringType or dataType == types.UnicodeType)

    # --------------------------------------------------------------------
    # data 가 unicode가 아닌 경우 unicode로 변환
    # --------------------------------------------------------------------
    def unicode_ex(self, data):
        dataType = type(data)
        return data if dataType == types.UnicodeType else unicode(data, 'utf-8')

    # --------------------------------------------------------------------
    # [in] [dictionary]     dictData
    # [in] [dictionary key] key            : dictData에서 갖고올 값의 key
    # [in] [data type]      defaultValue   : dictData에 key가 존재 하지 않는 경우 반환 할 값
    # --------------------------------------------------------------------
    # [out] dictData의 Key값 또는 defaultValue
    # --------------------------------------------------------------------
    def getJsonValue(self, dictData, key, defaultValue):
        try:
            if type(dictData) != types.DictType or len(dictData) == 0:
                return defaultValue
            if key == None or len(key) == 0 :
                return defaultValue
            return dictData[key] if key in dictData else defaultValue
        except:
            print sys.exc_info()
            return defaultValue

    # ---------------------------------------------------------------------
    #
    # -----  xlsxwriter  -----
    #
    # --------------------------------------------------------------------
    # close workbook : createWorkbook() 함수로 엑셀 파일 생성 후, 호출한다.
    #                  해당 함수를 호출 하지 않으면, 엑셀 파일이 생성되지 않는다.
    # --------------------------------------------------------------------
    def closeWorkbook(self, workbook):
        try:
            if workbook != None:
                workbook.close()
            return True
        except:
            print sys.exc_info()
            return False

    # --------------------------------------------------------------------
    # workbook 생성
    # --------------------------------------------------------------------
    # [in] [string] sFileName  : 엑셀 파일로 생성할 파일이름.
    # --------------------------------------------------------------------
    # [out] workbook
    # --------------------------------------------------------------------
    def createWorkbook(self, sFileName):
        try:
            if os.path.isfile(sFileName):
                print "# Error, 이미 존재하는 파일이다. ({})".format(sFileName)
                return None

            return xlsxwriter.Workbook(sFileName)            
        except:
            print sys.exc_info()
            return None

    # --------------------------------------------------------------------
    #  worksheet 추가.
    # --------------------------------------------------------------------
    # [in] [workbook]        : createWorkbook() 함수에서 반환된 workbook
    # --------------------------------------------------------------------
    # [out] [worksheet]
    # --------------------------------------------------------------------
    def add_worksheet(self, workbook, name=None):
        try:
            if workbook :
                return workbook.add_worksheet(name)
            else:
                print "# Error, invalild workbook"
                return None
        except:
            print sys.exc_info()
            return None

    # --------------------------------------------------------------------
    # worksheet 속성 설정
    # --------------------------------------------------------------------
    # [in] [worksheet]        : add_worksheet() 함수에서 반환된 worksheet
    # --------------------------------------------------------------------
    # [out] [boolen] True / Fasle
    # --------------------------------------------------------------------
    def setSheetProperty(self, worksheet, **kwargs):
        try:
            if worksheet == None :
                print "# Error, invalild worksheet"
                return False

            autofilter = kwargs.pop('autofilter', None)
            if autofilter != None :
                first_row = self.getJsonValue(autofilter, 'first_row', 0)
                first_col = self.getJsonValue(autofilter, 'first_col', 0)
                last_row = self.getJsonValue(autofilter, 'last_row', 0)
                last_col = self.getJsonValue(autofilter, 'last_col', 0)
                worksheet.autofilter( first_row, first_col, last_row, last_col)

            freeze_panes = kwargs.pop('freeze_panes', None)
            if freeze_panes != None :
                row = self.getJsonValue(freeze_panes, 'row', 0)
                col = self.getJsonValue(freeze_panes, 'col', 0)
                worksheet.freeze_panes(row, col)

            return True
        except:
            print sys.exc_info()
            return False

    # --------------------------------------------------------------------
    #  Set the width, and other properties of a single column or arange of columns.
    # --------------------------------------------------------------------
    # [in] [worksheet]  add_worksheet() 함수에서 반환된 worksheet
    # [in] [int] firstcol:    First column (zero-indexed).
    # [in] [int] lastcol:     Last column (zero-indexed). Can be same as firstcol.
    # [in] [int] width :       Column width. (optional).
    # [in] [cell_format] : Column cell_format. (optional).
    # [in] [Dictionary Type]options:     Dict of options such as hidden and level.
    # --------------------------------------------------------------------
    # [out] [boolean] : True : worksheet의 row에 write 성공
    #                   False : 실패.
    # --------------------------------------------------------------------
    def set_column(self, worksheet, firstcol, lastcol, width=None, cell_format=None, options={}):
        try:
            if worksheet == None:
                print "Error, invalid worksheet"
                return False

            return worksheet.set_column(firstcol, lastcol, width, cell_format, options)
        except:
            print sys.exc_info()
            return -1
    # --------------------------------------------------------------------
    #  Format 객체 생성
    # --------------------------------------------------------------------
    # [in] [workbook]        : createWorkbook() 함수에서 반환된 workbook
    # --------------------------------------------------------------------
    # [out] [format_properties] : Format to the Excel Workbook
    # --------------------------------------------------------------------
    def add_format(self, workbook, **kwargs):
        try:
            if workbook == None :
                print "# Error, invalild workbook"
                return None

            properties  = kwargs.pop('properties', {})
            bBold       = kwargs.pop('set_bold', False)
            align       = kwargs.pop('set_align', None)
            font_size   = kwargs.pop('font_size', None)
            bBorder     = kwargs.pop('set_border', False)
            bg_color    = kwargs.pop('set_bg_color', None)
            font_color  = kwargs.pop('set_font_color', None)

            cellformat = workbook.add_format(properties)
            cellformat.set_bold(bBold)
            if align != None            : cellformat.set_align(align)
            if font_size != None        : cellformat.font_size = font_size
            if bBorder                  : cellformat.set_border()
            if bg_color != None         : cellformat.set_bg_color(bg_color)
            if font_color != None       : cellformat.set_font_color(font_color)

            return cellformat
        except:
            print sys.exc_info()
            return None

    # --------------------------------------------------------------------
    #  worksheet의 row write
    # --------------------------------------------------------------------
    # [in] [worksheet]        : add_worksheet() 함수에서 반환된 worksheet
    # [in] [int]row           : write 할 row
    # [ListType] listCols     : write할 row의 column value 정보
    #                           {'col':col, 'value':value, 'format':format}의 List
    # --------------------------------------------------------------------
    # [out] [boolean] : True : worksheet의 row에 write 성공
    #                   False : 실패.
    # --------------------------------------------------------------------
    def writeSheetRow(self, worksheet, row, listCols):
        try:
            if worksheet == None or row == None or listCols == None :
                print "Error, invalid Param."
                return False

            if row < 0 :
                print "Error, invalid row"
                return False

            for dictCols in listCols:
                col = self.getJsonValue(dictCols, 'col', -1)
                if col < 0 : continue
                value  = self.getJsonValue(dictCols, 'value', '')
                format = self.getJsonValue(dictCols, 'format', None)

                if format == None :
                    worksheet.write(row, col, value)
                else:
                    worksheet.write(row, col, value, format)
            return True
        except:
            print sys.exc_info()
            return False

    # --------------------------------------------------------------------
    # writeSheetRow()의 IN Param인 listCols 의 item
    # --------------------------------------------------------------------
    def getStructColInfo(self, col, value, format):
        try:
            return {'col': col, 'value': value, 'format': format}
        except:
            print sys.exc_info()
            return {}

    #---------------------------------------------------------------------
    #
    # -----  xlrd  -----
    #
    # --------------------------------------------------------------------
    # getWorkbook() 함수로, workbook resource를 사용 한 경우, 호출한다.
    # --------------------------------------------------------------------
    def release_resources(self, workbook):
        try:
            if workbook == None:
                print "Error, invalid workbook."
                return False
            workbook.release_resources()
            return True
        except:
            print sys.exc_info()
            return False

    # --------------------------------------------------------------------
    # excel file의 workbook, worksheet 취득
    # 사용 완료 후, 반드시 release_resources() 함수 호출 한다.
    # --------------------------------------------------------------------
    # [in] [string] sFileName        : 엑셀 파일
    # [in] [string] sWishSheetName   : 엑셀 파일내의 취득하고나 하는 sheet name
    #                                  해당 값이 유효하지 않은 경우, 첫번째 sheet 반환
    # --------------------------------------------------------------------
    # [out] [Tuple] workbook, worksheet
    # --------------------------------------------------------------------
    def getWorkbook(self, sFileName, sWishSheetName=''):
        try:
            if os.path.isfile(sFileName) == False   :
                print "# Error, 유효한 파일이 아니다. ({})".format(sFileName)
                return None, None
            if sFileName.lower().find(".xls") < 0   :
                print "# Error, 엑셀 파일이 아니다. ({})".format(sFileName)
                return None, None

            open_workbook   = xlrd.open_workbook(sFileName)
            sheet_names     = open_workbook.sheet_names()
            nCntSheet = len(sheet_names)
            if nCntSheet == 0 : return None, None

            cur_sheet = None
            if len(sWishSheetName) > 0 :
                for idx in range(nCntSheet):
                    if unicode(sheet_names[idx]) == unicode(sWishSheetName) :
                        cur_sheet = open_workbook.sheet_by_index(idx)
                        break

            if cur_sheet == None :
                cur_sheet = open_workbook.sheet_by_index(0)

            return open_workbook, cur_sheet
        except:
            print sys.exc_info()
            return None, None

    # --------------------------------------------------------------------
    # worksheet rows 정보 취득
    # --------------------------------------------------------------------
    # [in] [worksheet] getWorkbook()에서 취득한 worksheet
    # --------------------------------------------------------------------
    # [out][int] worksheet의 rows
    # --------------------------------------------------------------------
    def getSheetRows(self, worksheet):
        try:
            if worksheet == None :
                print "Error, invalid worksheet"
                return -1
            return worksheet.nrows
        except:
            print sys.exc_info()

    # --------------------------------------------------------------------
    # worksheet cols 정보 취득
    # --------------------------------------------------------------------
    # [in] [worksheet] getWorkbook()에서 취득한 worksheet
    # --------------------------------------------------------------------
    # [out][int] worksheet의 cols
    # --------------------------------------------------------------------
    def getSheetCols(self, worksheet):
        try:
            if worksheet == None:
                print "Error, invalid worksheet"
                return -1
            return worksheet.ncols
        except:
            print sys.exc_info()
    # --------------------------------------------------------------------
    # worksheet의 cell 값 취득
    # --------------------------------------------------------------------
    # [in] [worksheet]
    # [in] row
    # [in] col
    # --------------------------------------------------------------------
    # [out] worksheet의 (row, col) 위치의 값
    # --------------------------------------------------------------------
    def getCellValue(self, worksheet, row, col):
        try:
            return worksheet.cell_value(row, col) if worksheet != None else None
        except:
            print sys.exc_info()
            return None

    def findColumnTitle(self, sWishName, sCellData):
        try:
            if sCellData == None or sWishName == None: return False

            if self.isString(sCellData):
                sCellData = self.unicode_ex(sCellData).strip().lower()
                if len(sCellData) == 0: return False

            if self.isString(sWishName):
                sWishName = self.unicode_ex(sWishName).strip().lower()
                if len(sWishName) == 0: return False

            return True if sWishName == sCellData else False
        except:
            print sys.exc_info()
            return False