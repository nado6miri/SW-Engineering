import sys
import os
from jira import JIRA
from PyQt5 import uic, QtWidgets, QtGui

DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'

userID = 'sungbin.na'
userPasswd = 'Sungbin'



if __name__ == "__main__" :
    dev_jira = JIRA(DevTracker, basic_auth = (userID, userPasswd))
    q_jira = JIRA(QTracker, basic_auth = (userID, userPasswd))

    #===========================================================================
    # Dev Trakcer
    #===========================================================================
    # Get issue with All Fields in Dev Tracker
    dissue = dev_jira.issue("LEADSWETDI-1")
    print("[Dev Tracker] Get JIRA Issue with All fields")

    # Get issue with specific Fields in Dev Tracker
    setfield = ('summary, comment, assignee')
    dissue = dev_jira.issue("LEADSWETDI-1", fields=setfield)
    print("[Dev Tracker] Get JIRA Issue with Specific fields")

    #===========================================================================
    # Get filtered issue with Filter ID in Dev Tracker
    setFilterID = 'filter = 34905'
    setfield = ('summary, comment, assignee')
    dissue = dev_jira.search_issues(setFilterID, startAt = 0, maxResults = 1000, fields = setfield, expand=None)
    print("[Dev Tracker] Get JIRA Issue with Specific Filter ID: " + setFilterID)

    # Get Filtered issue with JQL Querfy String in Dev Tracker
    setFilter = 'project = TVPLAT AND issuetype = Initiative AND status in (approved, "BACKLOG REFINEMENT", "In Progress", Delivered)'
    dissue = dev_jira.search_issues(setFilter)
    print("[Dev Tracker] Get JIRA Issue with Specific Filter String: " + setFilter)

    #===========================================================================
    # Create Issue in Dev Tracker
    # new_dissue = jira.create_issue(project='PROJ_key_or_id', summary='New issue from jira-python', description='Look into this one', issuetype={'name': 'Bug'})
    issue_dict = {
        'project': {'id': 123},
        'summary': 'New issue from jira-python',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
    }
    new_dissue = dev_jira.create_issue(fields=issue_dict)

    issue_list = [
    {
        'project': {'id': 123},
        'summary': 'First issue of many',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
    },
    {
        'project': {'key': 'FOO'},
        'summary': 'Second issue',
        'description': 'Another one',
        'issuetype': {'name': 'Bug'},
    },
    {
        'project': {'name': 'Bar'},
        'summary': 'Last issue',
        'description': 'Final issue of batch.',
        'issuetype': {'name': 'Bug'},
    }]
    new_dissue = dev_jira.create_issue(fields=issue_list)

    #===========================================================================
    # Update Issue in Dev Tracker
    dissue = dev_jira.issue("LEADSWETDI-1")
    dissue.update(notify=True, summary='new summary', description='A new summary was added')

    issueUpdate_dict = {
        'project': {'id': 123},
        'summary': 'New issue from jira-python',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
    }
    dissue = dev_jira.issue("LEADSWETDI-1")
    dissue.update(notify=True, fields = issueUpdate_dict)

    issue.update(notify=True, assignee={'name': 'new_user'})

    #===========================================================================
    # reassign an Issue in Dev Tracker
    issue = dev_jira.issue("LEADSWETDI-1")
    dev_jira.assign_issue(issue, 'id')

    #===========================================================================
    # Delete an Issue in Dev Tracker
    issue = dev_jira.issue("LEADSWETDI-1")
    issue.delete()

    #===========================================================================
    # Add comment to Issue in Dev Tracker
    comment = jira.add_comment('LEADSWETDI-1', 'new comment')    # no Issue object required

    issue = dev_jira.issue("LEADSWETDI-1")
    comment = jira.add_comment(issue, 'new comment', visibility={'type': 'role', 'value': 'Administrators'})  # for admins only

    comment.update(body = 'updated comment body')
    comment.delete()


    #===========================================================================
    # Add / Remove Watcher to Issue in Dev Tracker
    issue = dev_jira.issue("LEADSWETDI-1")
    watcher = jira.watchers(issue)
    print("Issue has {} watcher(s)".format(watcher.watchCount))
    for watcher in watcher.watchers:
        print(watcher)
        # watcher is instance of jira.resources.User:
        print(watcher.emailAddress)

    jira.add_watcher(issue, 'username')
    jira.revmove_watcher(issue, 'username')



    #===========================================================================
    # Attachment control in Dev Tracker
    issue = dev_jira.issue("LEADSWETDI-1")
    jira.add_attachment(issue=issue, attachment='/some/path/attachment.txt')

    # read and upload a file (note binary mode for opening, it's important):
    with open('/some/path/attachment.txt', 'rb') as f:
        jira.add_attachment(issue=issue, attachment=f)

    # attach file from memory (you can skip IO operations). In this case you MUST provide `filename`.
    import StringIO
    attachment = StringIO.StringIO()
    attachment.write(data)
    jira.add_attachment(issue=issue, attachment=attachment, filename='content.txt')


    #===========================================================================
    # Q Trakcer
    #===========================================================================
    # Get issue with All Fields in Q Tracker
    qissue = q_jira.issue("WOSLQEVENT-98853")
    print("[Dev Tracker] Get JIRA Issue with All fields")

    # Get issue with specific Fields in Q Tracker
    setfield = ('summary, comment, assignee')
    qissue = q_jira.issue("LEADSWETDI-1", fields=setfield)
    print("[Dev Tracker] Get JIRA Issue with Specific fields")

    #===========================================================================
    # Get filtered issue with Filter ID in Q Tracker
    setFilterID = 'filter = 95949'
    qissue = q_jira.search_issues(setFilterID)
    print("[QTracker] Get JIRA Issue with Specific Filter ID: " + setFilterID)

    # Get Filtered issue with JQL Querfy String in Q Tracker
    setFilter = 'Filter in (M3.LK61.EU.QA1, M3.LK61.EU.QA2, M3.LK61.EU.QA3, M3.LK61.EU.QA4)'
    qissue = q_jira.search_issues(setFilter)
    print("[QTracker] Get JIRA Issue with Specific Filter String: " + setFilter)
