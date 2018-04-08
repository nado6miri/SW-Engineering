

desc = "|| name || desc || expected || Actual || Done || \n\
 | backlog 완료 | refinement 완료 | TVSP16 | ? | (?) | \n\
 | Demo | 실물데모 | TVSP20 | ? | (?) | \n\
 | CCC | OE-Build반영 | TVSP21 | ? | (?) | \n\
 | TEST | Event 검증 | 19Y_TVSP6 | ? | (?) |"

print(desc)

'''
1. ||로 시작하는 line에서 title을 List로 반환
  First title =
  Expected Sprint =
  Actual Sprint =

2. Sprint String이 있는 Line 추출하여 Sprint 빠른순 ~ 늦은순으로 정렬
 desc = [ { 'TVSP16' : " Item16 - Description"},
        { 'TVSP17' : " Item17 - Description"},
        { 'TVSP21' : " Item21 - Description"},
        { '19Y_TVSP1' : " Item19Y1 - Description"},
        { '19Y_TVSP6' : " Item19Y6 - Description"}]
'''

desc = [ { 'TVSP16' : " Item16 - Description"},
        { 'TVSP17' : " Item17 - Description"},
        { 'TVSP21' : " Item21 - Description"},
        { '19Y_TVSP1' : " Item19Y1 - Description"},
        { '19Y_TVSP6' : " Item19Y6 - Description"}]

print(desc)
findstr = "TVSP"

sprint = [ 'TVSP20', 'TVSP19', 'TVSP25', 'TVSP7', '19Y_TVSP5', '19Y_TVSP1', 'TVSP', 'TBD', 'None']
print(sprint)
sorted = sprint.sort()
print(sprint)

import re

for sp in sprint :
    # 19년 Sprint 식별 (Event F.up IR 이후 항목)
    if(sp.find('19Y_', 0, len(sp)) == 0) :
        spbase = 50
        sp = sp.replace('19Y_', '')
        step = re.findall('\\d+', sp)
        print("findall = step = ", step)
        if(len(step) == 1) :
            step = str(step[0])
            print("step =", step, "len=", len(step))
            if(len(step) < 2):
                step = step.zfill(2)
                print("zfill=", step)
            print("Sprint = 19Y_TVSP, Step = ", step)
        else :
            print("Sprint Step Error....... = ", step)
    # 18년 Sprint 식별
    else :
        step = re.findall('\\d+', sp)
        print("findall = step = ", step)
        if(len(step) == 1) :
            step = str(step[0])
            print("step =", step, "len=", len(step))
            if(len(step) < 2):
                step = step.zfill(2)
                print("zfill=", step)
            print("Sprint = 19Y_TVSP, Step = ", step)
        else :
            print("Sprint Step Error....... = ", step)
