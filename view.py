# library modules
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QComboBox, QLineEdit, QRadioButton, QSpinBox, QTextEdit,QWidget,QToolBar,QStatusBar,QHBoxLayout,QTableWidget
from PyQt5.QtWidgets import QLabel, QTableWidgetItem, QListWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QTabWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow, QHeaderView
import pathlib

class JiraUi(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        current_directory = str(pathlib.Path(__file__).parent.absolute())
        self.setWindowTitle('Dave\'s Jira Thing')
        self.setWindowIcon(QtGui.QIcon(current_directory + '/icon.png'))
        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self._createStatusBar()

    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("Idle")
        self.setStatusBar(self.status)

    def updateStatusBar(self, msg, timeout=1000):
        self.status.showMessage(msg, timeout)

    def populateEpics(self, epics):
        self.tab_widget.epicInput.clear()
        self.tab_widget.epicInput.addItems(epics)

    def populateCustomers(self, customers):
        self.tab_widget.customerInput.clear()
        self.tab_widget.customerInput.addItems(customers)

    def populateIssueList(self, summarys):
        self.tab_widget.issueList.addItems(summarys)

    def updateDescription(self, text):
        self.tab_widget.descriptionInput.setPlainText(text)

    def updateComments(self, comments):
        print(f"len(comments)={len(comments)}")
        self.tab_widget.issueCommentsTable.setRowCount(len(comments))
        row = 0
        if len(comments) == 0:
            self.tab_widget.issueCommentsTable.setCellWidget(row,0, QLabel("No comment :)"))
            print("Im here")
        else:
            for c in comments:
                commentBody = c.author.displayName + " " + c.updated + "\n" + c.body
                self.tab_widget.issueCommentsTable.setCellWidget(row,0, QLabel(commentBody))
                row = +1
        self.tab_widget.issueCommentsTable.resizeRowsToContents()

    def updateLink(self, url):
        self.tab_widget.issueLinkOutput.setText(url)

    def setDefaultFocus(self):
        self.tab_widget.summaryInput.setFocus()


# Creating tab widgets
class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        
        self.layout = QVBoxLayout(self)
        parent = parent

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "New")
        self.tabs.addTab(self.tab2, "Existing")

        # Create first tab
        self.tab1.layout = QGridLayout(self)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        # Create input widgets
        self.summaryInput = QLineEdit()
        self.pointsInput = QSpinBox(value=1)
        self.epicInput = QComboBox()
        self.customerInput = QComboBox()
        self.current_sprint = QRadioButton("Current")
        self.backlog = QRadioButton("Backlog")
        self.descriptionInput = QTextEdit()
        self.issueLinkOutput = QLabel("Not created yet")

        ## Tab 2
        self.issueKey = QLabel("...")
        self.issueList = QListWidget()
        self.issueCommentsTable = QTableWidget()

        # Create buttons
        self.epicsButton = QPushButton(text="Fetch")
        self.clearButton = QPushButton(text="Clear")
        self.createButton = QPushButton(text="Create")

        # Customize input widgets
        self.current_sprint.setChecked(True)
        self.issueLinkOutput.setOpenExternalLinks(True)
        self.descriptionInput.toMarkdown()
        self.issueCommentsTable.setColumnCount(1)
        # self.issueCommentsTable.setRowCount(5)
        self.issueCommentsTable.verticalHeader().setVisible(False)
        self.issueCommentsTable.horizontalHeader().setVisible(False)
        issueCommentsTableHeader = self.issueCommentsTable.horizontalHeader()
        issueCommentsTableHeader.setSectionResizeMode(0, QHeaderView.Stretch)

        # Add input widgets to UI
        ## Summary
        self.tab1.layout.addWidget(QLabel('Summary'), 0, 0)
        self.tab1.layout.addWidget(self.summaryInput, 0, 1)

        ## Points
        self.tab1.layout.addWidget(QLabel('Points'), 1, 0)
        self.tab1.layout.addWidget(self.pointsInput, 1,1)

        ## Epics
        self.tab1.epicsLayout = QHBoxLayout()
        self.tab1.layout.addWidget(QLabel('Epic'), 2, 0)
        self.tab1.layout.addLayout(self.tab1.epicsLayout, 2, 1)
        self.tab1.epicsLayout.addWidget(self.epicInput)
        self.tab1.epicsLayout.addWidget(self.epicsButton)
        self.epicsButton.setFixedWidth(50)

        ## Customer
        self.tab1.layout.addWidget(QLabel('Customer'), 3, 0)
        self.tab1.layout.addWidget(self.customerInput, 3, 1)

        ## Sprint
        self.tab1.sprintsLayout = QHBoxLayout()
        self.tab1.layout.addWidget(QLabel('Sprint'), 4, 0)
        self.tab1.layout.addLayout(self.tab1.sprintsLayout, 4, 1)
        self.tab1.sprintsLayout.addWidget(self.current_sprint)
        self.tab1.sprintsLayout.addWidget(self.backlog)

        ## Description
        self.tab1.layout.addWidget(QLabel('Description'), 5, 0, QtCore.Qt.AlignTop)
        self.tab1.layout.addWidget(self.descriptionInput, 5, 1)

        ## Link
        self.tab1.layout.addWidget(QLabel('Link'), 6, 0)
        self.tab1.layout.addWidget(self.issueLinkOutput, 6, 1)

        ## Create button
        self.tab1.buttonsLayout = QHBoxLayout()
        self.tab1.layout.addLayout(self.tab1.buttonsLayout, 7, 1)
        self.tab1.buttonsLayout.addWidget(self.clearButton)
        self.tab1.buttonsLayout.addWidget(self.createButton)

        # Tab2 - 
        self.tab2.layout2 = QGridLayout(self)
        self.tab2.setLayout(self.tab2.layout2)
        self.tab2.layout2.addWidget(self.issueList,0,0)

        self.tab2.commentsLayout = QVBoxLayout()
        self.tab2.layout2.addLayout(self.tab2.commentsLayout, 0, 1)
        self.tab2.commentsLayout.addWidget(self.issueKey)
        self.tab2.commentsLayout.addWidget(self.issueCommentsTable)

        self.summaryInput.setFocus()

# class LoginController(QtWidgets.QDialog, Ui_Dialog):
#     loginSuccessful = QtCore.pyqtSignal()

#     def __init__(self, parent=None):
#         super(LoginController, self).__init__(parent)
#         self.setupUi(self)
#         self.pushButton.clicked.connect(self.valid_login)



