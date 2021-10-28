from PyQt5.QtWidgets import QApplication
import sys
import json
from view import JiraUi
from model import JiraModel
from qt_material import apply_stylesheet
import pathlib

class JiraCtrl:
    """Controller class."""

    # Templates
    descriptionTemplate = (f"\n\n"
                        "*Requirements:*\n"
                        "* \n\n"
                        "*Success Criteria:*\n"
                        "* \n\n"
                        "*Ticket:* "
                        "\n\n")
    default_epics = [""]
    default_customers = [""]

    def __init__(self, model, view):
        """Controller initializer."""
        self._view = view
        self._model = model
        self._connectSignals() # Connect signals and slots
        self._loadConfig()
        self._setDefaultEpics()
        self._setDefaultCustomers()
        self._setDescriptionTemplate()
        model.jiraConnect(self.config['auth']['server'], self.config['auth']['user'], self.config['auth']['apikey'])
        self.getIssueSummariesForIssueList()

    def _loadConfig(self):
        # Config
        current_directory = str(pathlib.Path(__file__).parent.absolute())
        with open(current_directory + '/config.json', 'r') as f:
            self.config = json.load(f)

    def _connectSignals(self):
        """Connect signals and slots."""
        self._view.tab_widget.clearButton.clicked.connect(self._resetFields)
        self._view.tab_widget.createButton.clicked.connect(self.createIssue)
        self._view.tab_widget.epicsButton.clicked.connect(self.getEpics)
        self._view.tab_widget.issueList.itemClicked.connect(self._test)

    def _resetFields(self):
        self._view.tab_widget.summaryInput.clear()
        self._view.tab_widget.pointsInput.setValue(1)
        self._setDescriptionTemplate()
        self.getEpics()
        self._view.updateLink("Not created yet")
        self._view.updateStatusBar('Idle',0)
        self._view.setDefaultFocus()

    def _setDefaultEpics(self):
        self._view.populateEpics(self.default_epics)

    def _setDefaultCustomers(self):
        self._view.populateCustomers(self.default_customers)

    def _setDescriptionTemplate(self):
        self._view.updateDescription(self.descriptionTemplate)

    def createIssue(self):
        sprint = "current" if self._view.tab_widget.current_sprint.isChecked() else "backlog"
        issue_dict = {
            'project': 'CFNTEM',
            'summary': self._view.tab_widget.summaryInput.text(),
            'description': self._view.tab_widget.descriptionInput.toMarkdown(),
            'issuetype': {'name': 'Story'},
            self.customFields['points']: self._view.tab_widget.pointsInput.value(),
            self.customFields['epic']: self._view.tab_widget.epicInput.itemText(self._view.tab_widget.epicInput.currentIndex()),
            self.customFields['sprint']: sprint,
            self.customFields['customer']: [self._view.tab_widget.customerInput.itemText(self._view.tab_widget.customerInput.currentIndex())]
        }
        #customer = self._view.tab_widget.customerInput.itemText(self._view.tab_widget.customerInput.currentIndex())

        self._view.updateStatusBar('Creating issue', 5000)
        issue = self._model.createIssue(issue_dict, self.customFields)
        self._model.addWorklog(issue.key)
        linkAddress = 'https://example.atlassian.net/browse/' + issue.key
        self._view.updateLink('<a href='+ linkAddress +'>'+ linkAddress +'</a>')
        self._view.updateStatusBar('Created issue '+issue.key, 5000)

    def getEpics(self):
        self._view.updateStatusBar('Fetching epics', 5000)
        epics = self._model.getEpics()
        self._view.populateEpics(epics)
        self._view.updateStatusBar('Epics updated', 5000)

    def getIssueSummariesForIssueList(self):
        self.issues = self._model.getIssues()
        issueList = []
        for i in self.issues['issues']:
            issueList.append(i['fields']['summary'])
        self._view.populateIssueList(issueList)

    def _test(self, item):
        print(f"issue {item.text()} was selected from list")
        self._view.tab_widget.issueKey.setText(item.text())
        
        for i in self.issues['issues']:
            if i['fields']['summary'] == item.text():
                key = i['key']
        comments = self._model.getComments(key)
        self._view.updateComments(comments)

def main():
    """Main function."""
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Create the GUI
    # apply_stylesheet(app, theme='dark_yellow.xml')
    view = JiraUi()
    view.show()

    # Create the model
    model = JiraModel()

    # Create instances of the model and the controller
    controller = JiraCtrl(model=model, view=view)

    # Execute the main loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
