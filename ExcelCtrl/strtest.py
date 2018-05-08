

desc = "|| name || desc || expected || Actual || Done || \n\
 | backlog 완료 | refinement 완료 | TVSP16 | ? | (?) | \n\
 | Demo | 실물데모 | TVSP20 | ? | (?) | \n\
 | CCC | OE-Build반영 | TVSP21 | ? | (?) | \n\
 | TEST | Event 검증 | 19Y_TVSP6 | ? | (?) |"

#print(desc)

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


#===========================================================================
# convert ReleaseSprint to ShortSprint
# [param] duedate : duedate
# [return] Sprint str
#===========================================================================
def conversionReleaseSprintToSprint() :
    sp = [
        'GL2_IR2TVSP11(1/15-1/26)',
        'GL2_IR2TVSP15_Hardening(3/12-3/30)',
        'GL2_IR3TVSP16(4/2-4/13)',
        'GL2_IR3TVSP17(4/16-4/27)',
        'GL2_IR3TVSP18(4/30-5/11)',
        'GL2_IR3TVSP19(5/14-5/25)',
        'GL2_IR3TVSP20(5/28-6/8)',
        'GL2_IR3TVSP21(6/11-6/22)',
        'GL2_IR3TVSP22(6/25-7/6)',
        'GL2_IR3TVSP23_Hardening(7/9-7/20)',
        'GL2_IR4TVSP24(7/23-8/3)',
        'GL2_IR4TVSP25(8/6-8/17)',
        'GL2_IR4TVSP26(8/20-8/31)',
        'GL2_IR4TVSP29(10/1-10/12)',
        'FC2_TVSP20(8/14-8/25)',
        ]

    for sprint in sp :
        print("\n")
        a = sprint.replace('GL2_', '')
        #a = a.replace('FC2_', '')
        a = a.replace('19Y_', '')
        a = a.split('_')
        print(a[0])
        b = a[0]
        b = b.replace('IR2', '')
        b = b.replace('IR3', '')
        b = b.replace('IR4', '')
        print(b)
        c = b.split('(')
        d = c[0]
        print(d)

    pass


'''
print(desc)
findstr = "TVSP"

sprint = [ 'TVSP20', 'TVSP19', 'TVSP25', 'TVSP7', '19Y_TVSP5', '19Y_TVSP1', 'TVSP', 'TBD', 'None']
print(sprint)
sorted = sprint.sort()
print(sprint)
'''
conversionReleaseSprintToSprint()
'''
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
'''
