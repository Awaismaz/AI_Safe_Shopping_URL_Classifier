import json # used to work with JSON data, which is a data format that is used to store and exchange data
import os # used to interact with the operating system, such as checking if a file exists
from PyQt5 import QtWidgets, QtGui, QtCore # part of the PyQt5 library, used to create the GUI (graphical user interface) of the application
from PyQt5.QtGui import QIcon # used to set an icon for the application
from PyQt5.QtWidgets import QApplication # used to start the event loop for the GUI, which handles user inputs and updates the UI accordingly
from shopping_classifier import check_category # custom function used to classify the category of a shopping website
from trust_classifier import check_url # custom function used to check the trustworthiness of a shopping website
import random # used to generate random numbers
from googlesearch import search # used to perform a search on Google and return the URLs of the results

class Application(QtWidgets.QWidget): # defines the Application class that inherits from the QWidget class of the PyQt5 library
    def __init__(self):
        super().__init__() # initializes the parent class
        self.initUI() # calls the initUI method to initialize the user interface
    def initUI(self):
        self.setWindowTitle('Trusted Shopping Website Classifier') # sets the title of the window to "Trusted Shopping Website Classifier"
        self.setMinimumSize(800, 410) # sets the minimum size of the window to 800x410
        
        # sets the style of the GUI elements using CSS-like syntax
        self.setStyleSheet("""
            QWidget {
                background-color: #F1F2F5;

            }
            QLabel {
                font-size: 14px;
                color: black;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: light-blue;
                color: white;
                border-radius: 5px;
                padding: 8px 12px;
            }
            QLineEdit {
                border: 1px solid black;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget {
                gridline-color: #D3D3D3;
                selection-background-color: #007BFF;
            }
            QTableWidget::item:hover {
                background-color: #E0E0E0;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self) # creates a vertical layout for the window and sets it as the layout for the window

        search_layout = QtWidgets.QHBoxLayout() # creates a horizontal layout for the search section of the window
        self.query_label = QtWidgets.QLabel('Enter your query:') # creates a label with the text "Enter your query:"
        self.query_entry = QtWidgets.QLineEdit() # creates a line edit widget for entering the search query
        self.query_entry.setFixedHeight(30) # sets the fixed height of the line edit widget to 30
        self.query_entry.setPlaceholderText("Enter Search Keywords") # sets the placeholder text of the line edit widget to "Enter Search Keywords"

        self.search_button = QtWidgets.QPushButton('Search') # creates a button with the text "Search"
        self.search_button.clicked.connect(self.search) # connects the clicked signal of the button to the search method
        self.search_button.setFixedHeight(30) # sets the fixed height of the button to 30

        search_layout.addWidget(self.query_label) # adds the query label to the search layout
        search_layout.addWidget(self.query_entry) # adds the query entry widget to the search layout
        search_layout.addWidget(self.search_button) # adds the search button to the search layout

        layout.addLayout(search_layout) # adds the search layout to the main layout

        self.results_label = QtWidgets.QLabel('Results:') # creates a label with the text "Results:"
        layout.addWidget(self.results_label) # adds the results label to the main layout

        self.scroll_area = QtWidgets.QScrollArea() # creates a scroll area widget
        self.scroll_area.setWidgetResizable(True) # sets the scroll area widget to be resizable

        self.result_table = QtWidgets.QTableWidget(0, 3) # creates a table widget with 0 rows and 3 columns
        self.result_table.setHorizontalHeaderLabels(
            ['Searched URL', 'Category', 'Trusted']) # sets the horizontal header labels of the table to "Searched URL", "Category", and "Trusted"
        self.scroll_area.setWidget(self.result_table) # sets the result table as the widget of the scroll area
        self.result_table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch) # sets the first column of the table to stretch to fill the width of the scroll area
        self.result_table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents) # sets the second column of the table to resize to its contents
        self.result_table.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents) # sets the third column of the table to resize to its contents

        self.result_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows) # sets the selection behavior of the table to select entire rows
        self.result_table.setMouseTracking(True) # sets mouse tracking to be enabled for the table

        layout.addWidget(self.scroll_area) # adds the scroll area to the main layout

    def search(self):
        query = self.query_entry.text() # gets the text entered in the query entry widget
        if query: # checks if there is any text entered in the query entry widget
            URLs = [j for j in search(query, num=10, stop=10, pause=2)] # performs a Google search with the entered query and gets the first 10 results

            self.result_table.setRowCount(0) # sets the number of rows in the result table to 0

            json_filename = 'search_results.json' # sets the name of the JSON file that will store the search results
            if os.path.isfile(json_filename): # checks if the JSON file already exists
                with open(json_filename, 'r') as f: # if it exists, open it in read mode
                    data = json.load(f) # load the data from the file
            else:
                data = [] # if the file does not exist, create an empty list

            search_results = [] # create an empty list to store the search results
            for url in URLs: # loop through the URLs obtained from the Google search
                row_position = self.result_table.rowCount() # get the current number of rows in the result table
                self.result_table.insertRow(row_position) # insert a new row at the end of the result table

                is_shopping = check_category(url) # check if the URL is a shopping website using the check_category function

                if is_shopping: # if the URL is a shopping website
                    category = "Shopping" # set the category to "Shopping"
                else:
                    category = "Information" # if the URL is not a shopping website, set the category to "Information"

                if is_shopping: # if the URL is a shopping website
                    status = check_url(url) # check if the URL is a trusted website using the check_url function
                    if status == 'Trusted': # if the URL is a trusted website
                        trusted = "Yes" # set the trusted status to "Yes"
                    else:
                        trusted = "No" # if the URL is not a trusted website, set the trusted status to "No"
                else:
                    trusted = "" # if the URL is not a shopping website, set the trusted status to an empty string

                search_results.append(
                    {'URL': url, 'Category': category, 'Trusted': trusted}) # add the URL, category, and trusted status to the search results list

                searched_url_item = QtWidgets.QTableWidgetItem(url) # create a table widget item for the URL
                category_item = QtWidgets.QTableWidgetItem(category) # create a table widget item for the category
                trusted_item = QtWidgets.QTableWidgetItem(trusted) # create a table widget item for the trust authentication
                if not is_shopping: # if the URL is not a shopping website
                    searched_url_item.setBackground(
                        QtGui.QColor(255, 255, 230)) # set the background color of the URL item to light yellow
                    category_item.setBackground(QtGui.QColor(255, 255, 230)) # set the background color of the category item to light yellow
                    trusted_item.setBackground(QtGui.QColor(255, 255, 230)) # set the background color of the trusted item to light yellow

                elif trusted == "Yes": # if the URL is a shopping website and is trusted
                    searched_url_item.setBackground(
                        QtGui.QColor(230, 255, 230)) # set the background color of the URL item to light green
                    category_item.setBackground(QtGui.QColor(230, 255, 230)) # set the background color of the category item to light green
                    trusted_item.setBackground(QtGui.QColor(230, 255, 230)) # set the background color of the trusted item to light green
                else:
                    searched_url_item.setBackground(
                        QtGui.QColor(255, 230, 230)) # if the URL is a shopping website but is not trusted, set the background color of the URL item to light red
                    category_item.setBackground(QtGui.QColor(255, 230, 230)) # set the background color of the category item to light red
                    trusted_item.setBackground(QtGui.QColor(255, 230, 230)) # set the background color of the trusted item to light red

                if trusted == "Yes":
                    # searched_url_item.setFlags(searched_url_item.flags() | QtCore.Qt.ItemIsEditable)
                    searched_url_item.setData(
                        QtCore.Qt.UserRole, QtCore.QUrl(url)) # set the URL data for the URL item

                self.result_table.setItem(row_position, 0, searched_url_item) # set the URL item in the first column of the current row
                self.result_table.setItem(row_position, 1, category_item) # set the category item in the second column of the current row
                self.result_table.setItem(row_position, 2, trusted_item) # set the trusted item in the third column of the current row

                QApplication.processEvents() # process any pending GUI events

            self.result_table.cellDoubleClicked.connect(self.open_url) # connect the cellDoubleClicked signal of the result table to the open_url function

            data.append({'query': query, 'results': search_results}) # add the query and search results to the data list

            with open(json_filename, 'w') as f: # open the JSON file in write mode
                json.dump(data, f, indent=4) # write the data to the JSON file

    def open_url(self, row, column): # function to open the URL when a cell in the first column is double-clicked
        if column == 0: # if the first column is double-clicked
            item = self.result_table.item(row, column)
            url = item.data(QtCore.Qt.UserRole) # get the URL data from the item
            if url is not None:
                QtGui.QDesktopServices.openUrl(url) # open the URL using the QtGui.QDesktopServices.openUrl method

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
   # Create a new Application window
    window = Application()
    app_icon = QIcon('icon.png')
    app.setWindowIcon(app_icon)
    # Show the window
    window.show()
    # Start the application event loop
    app.exec_()
