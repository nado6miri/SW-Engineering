# -*- coding:utf-8 -*-
#--------------------------------------------------------------------------------------
#
# author : jinkyeong.yoo@lge.com
#
#--------------------------------------------------------------------------------------
#
# CWorkingExcel를 상속받은 class   : Customizing시 각 작업 엑셀 파일에 맞춰 수정/확장.
#
#--------------------------------------------------------------------------------------
import sys
import os
import time
from workingExcel import *


class CUserExcelHandler(CWorkingExcel):

    def __init__(self):        
        CWorkingExcel.__init__(self)

        # 	분석할 엑셀 파일의 Column title 정보
        self.COL_TITLE_STRING_ID    = "String ID"
        self.COL_TITLE_PAGE         = "Page"
        self.COL_TITLE_KOR          = "Kor"
        self.COL_TITLE_ENG          = "Eng"
        self.COL_TITLE_COMMENT      = "Comment"

        # 	분석할 엑셀 파일의 Column 정보
        self.COL_POS_STRINGID     = -1
        self.COL_POS_PAGE         = -1
        self.COL_POS_KOR          = -1
        self.COL_POS_ENG          = -1
        self.COL_POS_COMMENT      = -1


    # --------------------------------------------------------------------
    # Excel 파일을 read하여 data를 취득한다.
    # --------------------------------------------------------------------
    # [in][stirng] sFileName   : 읽어들일 엑셀 파일
    # --------------------------------------------------------------------
    # [out] [ListType] : 읽어들인 엑셀 파일의 row value들을 List로 반환 하낟.
    #       [None]     : Excel 파일이 아니거나, 파일을 읽을 수 없는 경우.
    # --------------------------------------------------------------------
    def loadUXStringExcelFile(self, sFileName):
        try:
            listFileData = []

            workbook, worksheet = self.getWorkbook(sFileName)
            if workbook==None or worksheet == None :
                print "Error, 해당 파일에서 workbook 또는 worksheet 정보를 취득 할 수 없습니다."
                return None

            self.nCntRows = self.getSheetRows(worksheet)
            self.nCntCols = self.getSheetCols(worksheet)
            if self.nCntRows <= 0 or self.nCntCols <= 0 :
                print "Error, worksheet에서 cols, rows 정보를 취득 할 수 없습니다. "
                return None

            nHeaderRow = self.findStartPostionByUXCollab(worksheet)
            if nHeaderRow < 0 :
                print "----- Error >> Excel file Format 오류로 Parsing 하지 못합니다. : {}".format(sFileName)
                return None

            for collab_row in range(self.nCntRows):
                if collab_row <= nHeaderRow : continue
                objRow = {}

                for col_collab in range(self.nCntCols ):
                    if col_collab < self.COL_POS_STRINGID : continue
                    
                    value = self.getCellValue(worksheet, collab_row, col_collab) if col_collab < self.nCntCols else ''
                    if col_collab == self.COL_POS_STRINGID :
                        objRow[self.COL_TITLE_STRING_ID]=value

                    elif col_collab == self.COL_POS_PAGE :
                        objRow[self.COL_TITLE_PAGE] = value

                    elif col_collab == self.COL_POS_KOR :
                        objRow[self.COL_TITLE_KOR] = value

                    elif col_collab == self.COL_POS_ENG :
                        objRow[self.COL_TITLE_ENG] = value

                    elif col_collab == self.COL_POS_COMMENT :
                        objRow[self.COL_TITLE_COMMENT] = value

                    elif col_collab > self.COL_POS_COMMENT:
                        continue
                # END FOR : 2 :  for col_collab in range(nDefaultLoop):
                
                listFileData.append(objRow)                
            # END FOR: 1 :  for collab_row in range(self.nCntRows):

            self.release_resources(workbook)
            return listFileData
        except:
            print sys.exc_info()
            return None

    # --------------------------------------------------------------------
    # 로드한 Excel sheet의 Header column 위치와 body의 시작 위치를 찾는다.
    # --------------------------------------------------------------------
    # [in]  [worksheet] : getWorkbook 에서 취득한 worksheet
    # [out] [int]       : data body 시작 row
    # --------------------------------------------------------------------
    def findStartPostionByUXCollab(self, worksheet):
        try:
            for collab_row in range(self.nCntRows):
                for col in range(self.nCntCols):
                    if self.findColumnTitle(self.COL_TITLE_STRING_ID,
                                            self.getCellValue(worksheet, collab_row, col)):
                        self.COL_POS_STRINGID = col

                    elif self.findColumnTitle(self.COL_TITLE_PAGE, self.getCellValue(worksheet, collab_row, col)):
                        self.COL_POS_PAGE = col

                    elif self.findColumnTitle(self.COL_TITLE_KOR, self.getCellValue(worksheet, collab_row, col)):
                        self.COL_POS_KOR = col

                    elif self.findColumnTitle(self.COL_TITLE_ENG, self.getCellValue(worksheet, collab_row, col)):
                        self.COL_POS_ENG = col

                    elif self.findColumnTitle(self.COL_TITLE_COMMENT,
                                              self.getCellValue(worksheet, collab_row, col)):
                        self.COL_POS_COMMENT = col

                # END FOR : for col in range(self.nCntCols):
                if self.COL_POS_STRINGID >= 0:
                    break
            # END FOR: for collab_row in range(self.nCntRows):

            # 필수 column을 못 찾았다면, 포맷이 바뀌었거나 틀린 포맷의 파일이다.
            if self.COL_POS_STRINGID < 0:
                print"# [{}] not found collab col info. (Check Excel Format)".format(self.COL_TITLE_STRING_ID)
                return -1

            return collab_row
        except:
            print sys.exc_info()
            return -1

    # --------------------------------------------------------------------
    # worksheet를 추가 하고, data를 반영 한다.
    # --------------------------------------------------------------------
    # [in] [workbook] : createWorkbook()에서 취득한 workbook
    # [in] [ListType] : listRowDatas - 생성한 sheet에 추가할 data
    # --------------------------------------------------------------------
    # [out][boolean]  : True - 생성한 sheet에 data를 추가
    #                   False - 오류 발생.
    # --------------------------------------------------------------------
    def addWorksheet(self, workbook, listRowDatas, sheetName):
        try:
            print "+[addWorksheet]"

            worksheet = self.add_worksheet(workbook, sheetName)
            if worksheet == None:
                print "Error, Worksheet 생성 실패."
                return False

            # header
            nHeaderRow, nCntCol = self.writeExportHeader(workbook, worksheet)

            # sheet property
            self.setSheetProperty(worksheet, autofilter={'first_row' : nHeaderRow,
                                                         'first_col' : 0,
                                                         'last_row'  : nHeaderRow,
                                                          'last_col'  : nCntCol - 1},
                                             freeze_panes={'row'       : nHeaderRow + 1,
                                                           'col'       : 0})

            self.writeExportSheetRow(worksheet, nHeaderRow, listRowDatas)

            return True
        except:
            print sys.exc_info()
            return False
        finally:
            print "-[addWorksheet]"

    # --------------------------------------------------------------------
    # worksheet에 Header를 write 한다.
    # --------------------------------------------------------------------
    # [in] [workbook]  : createWorkbook()에서 취득한 workbook
    # [in] [worksheet] : addWorksheet()에서 취득한 worksheet
    # --------------------------------------------------------------------
    # [out] [Tuple]    : ( Header row, Column 개수 )
    # --------------------------------------------------------------------
    def writeExportHeader(self, workbook, worksheet):
        try:
            print "+[writeExportHeader]"
            listHeader = [{"name": self.COL_TITLE_STRING_ID, "width": 30},
                          {"name": self.COL_TITLE_PAGE, "width": 10},
                          {"name": self.COL_TITLE_KOR, "width": 50},
                          {"name": self.COL_TITLE_ENG, "width": 50},
                          {"name": self.COL_TITLE_COMMENT, "width": 30}]

            cellformat_header = self.add_format(workbook,
                                                properties={'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1},
                                                set_bg_color ='green',
                                                set_font_color = '#FFFFFF')
            nCol = 0
            nRow = 2
            for objHeader in listHeader:
                self.writeSheetRow(worksheet, nRow, [self.getStructColInfo(nCol, objHeader["name"], cellformat_header)])
                self.set_column(worksheet, nRow, nCol, width=objHeader["width"])
                nCol = nCol + 1

            return nRow, len(listHeader)
        except:
            print sys.exc_info()
            return -1, -1
        finally:
            print "-[writeExportHeader]"

    # --------------------------------------------------------------------
    # worksheet에 data를 write 한다.
    # --------------------------------------------------------------------
    # [in] [worksheet] : addWorksheet()에서 취득한 worksheet
    # [in] [int] nRow  : write 시작 위치
    # [in] [ListType] listRowDatas : worksheet에 write 할 data
    # --------------------------------------------------------------------
    # [out][boolean]   : True  : worksheet에 listRowDatas write 완료
    #                    False : 오류 발생
    # --------------------------------------------------------------------
    def writeExportSheetRow(self, worksheet, nRow, listRowDatas):
        try:
            print "+[writeExportSheetRow]"
            if not self.isNemeric(nRow) : nRow = 0

            # format
            cellformat_center = self.add_format(workbook, set_align='center', font_size=9, set_border=True)
            cellformat_left = self.add_format(workbook, set_align='left', font_size=9, set_border=True)
            cellformat_info = self.add_format(workbook, properties={'color':'blue'}, set_bold=True, set_align='left', font_size=9, set_border=True)


            sInfo = '{} : {}'.format("Export", datetime.today())
            self.writeSheetRow(worksheet, 0, [self.getStructColInfo(0, sInfo, cellformat_info) ])

            for objString in listRowDatas:

                nRow += 1
                listCols = []

                # StringID
                listCols.append(self.getStructColInfo(self.COL_POS_STRINGID,
                                          self.getJsonValue(objString, self.COL_TITLE_STRING_ID, ''),
                                          cellformat_left))

                # Page
                listCols.append(self.getStructColInfo(self.COL_POS_PAGE,
                                              self.getJsonValue(objString, self.COL_TITLE_PAGE, ''),
                                              cellformat_center))

                # Kor
                listCols.append(self.getStructColInfo(self.COL_POS_KOR,
                                          self.getJsonValue(objString, self.COL_TITLE_KOR, ''),
                                          cellformat_left))

                # Eng
                listCols.append(self.getStructColInfo(self.COL_POS_ENG,
                                          self.getJsonValue(objString, self.COL_TITLE_ENG, ''),
                                          cellformat_left))
                # comment
                listCols.append(self.getStructColInfo(self.COL_POS_COMMENT,
                                          self.getJsonValue(objString, self.COL_TITLE_COMMENT, ''),
                                          cellformat_left))

                self.writeSheetRow(worksheet, nRow, listCols)
            return True
        except:
            print sys.exc_info()
            return False
        finally:
            print "-[writeExportSheetRow]"



if __name__ == "__main__":
    myExcel = CUserExcelHandler()

    # 엑셀 파일 load
    listRowDatas = myExcel.loadUXStringExcelFile("{}{}{}".format(os.getcwd(), os.path.sep, "SampleFile.xlsx"))
    localtime = time.localtime(time.time())
    stamp =  "%02d%02d%02d_%02d%02d%02d" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)
    sFileName = "{}{}{}".format(os.getcwd(), os.path.sep, "Copy_SampleFile_{}.xlsx".format(stamp))

    # 엑셀 파일 생성
    workbook = myExcel.createWorkbook(sFileName)
    if workbook == None :
        print "Error, Workbook 생성 실패."
    else:
        myExcel.addWorksheet(workbook, listRowDatas, "first_sheet")
        myExcel.addWorksheet(workbook, listRowDatas, "second_sheet")
        myExcel.closeWorkbook(workbook)
        os.system('start excel.exe %s' % sFileName)