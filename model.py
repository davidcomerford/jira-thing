from jira import JIRA, JIRAError
from datetime import datetime

class JiraModel():

    def __init__(self):
        pass

    def jiraConnect(self, server, user, apikey):
        self.jira = JIRA(server=server, basic_auth=(user, apikey))

    def _jiraSearchIssues(self, query):
        try:
            print(query)
            result = self.jira.search_issues(query, json_result=True, maxResults=100)
        except JIRAError as e:
            print(e.status_code, e.text)
        return result

    def getEpics(self):
        epic_list = []
        epics = self._jiraSearchIssues("project = 'CFNTEMPLATE' AND issuetype = 'Epic' AND status = Open")
        for e in epics['issues']:
            epic_list.append(e['fields']['summary'])
        return epic_list
    
    def getEpicKey(self, name):
        epics = self._jiraSearchIssues("project = 'CFNTEMPLATE' AND issuetype = 'Epic' AND Summary ~ '"+ name +"'")
        if epics['total'] != 1:
            print("Error: getting epic name found incorrect number of results")
        else:
            return epics['issues'][0]['key']

    def getIssues(self):
        issues = self._jiraSearchIssues("project = 'CFNTEMPLATE' AND issuetype = Story AND assignee = 'David Comerford' AND (status = 'ToDo' OR status = 'In Progress')")
        return issues

    def getSprintId(self, sprintField):
        sprint = self._jiraSearchIssues("project = CFNTEM AND sprint in openSprints()")
        return sprint['issues'][0]['fields'][sprintField][0]['id']

    def getComments(self, issue_key):
        issue = self.jira.issue(issue_key)
        return issue.fields.comment.comments

    def createIssue(self, issue_dict, customFields):
        epicField = customFields['epic']
        sprintField = customFields['sprint']
        customerField = customFields['customer']
        accountId = customFields['accountId']

        epicKey = self.getEpicKey(issue_dict[epicField])
        issue_dict.update({epicField: epicKey})
        issue_dict.update({'assignee': {'accountId': accountId}})

        # Get and set the sprint if required
        if issue_dict[sprintField] == "current":
            issue_dict.update({sprintField: self.getSprintId(sprintField)})
        else:
            issue_dict.pop(sprintField)

        # Get and set the customer if required
        if not issue_dict[customerField]:
            issue_dict.pop(customerField)

        # Put a timestamp on the end of the description field. ISO 8601
        timestamp = "_Created " + datetime.now().replace(microsecond=0).isoformat() +"_"
        description_with_timestamp = issue_dict['description'] + timestamp
        issue_dict.update({'description': description_with_timestamp})

        result = self.jira.create_issue(fields=issue_dict)
        return result

    def addWorklog(self, key):
        self.jira.add_worklog(issue=key, timeSpent='15m', comment='Creating story')

    # def getCustomers(self):
    #     customer_list = []
    #     customers = self._jiraSearchIssues("'Customer Name' is not EMPTY and project = 'CFNTEMPLATE' AND updated > -7d")

    #     for c in customers:
    #         customer_list.append()
    #         except JIRAError as e:
    #             print(e.text)
    #     return customer_list