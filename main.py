import json
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from shopping_classifier import check_category
from trust_classifier import check_url
import random
from googlesearch import search


class Application(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Trusted Shopping Website Classifier')
        self.setMinimumSize(800, 410)

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

        layout = QtWidgets.QVBoxLayout(self)

        search_layout = QtWidgets.QHBoxLayout()
        self.query_label = QtWidgets.QLabel('Enter your query:')
        self.query_entry = QtWidgets.QLineEdit()
        self.query_entry.setFixedHeight(30)
        self.query_entry.setPlaceholderText("Enter Search Keywords")

        self.search_button = QtWidgets.QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        self.search_button.setFixedHeight(30)

        search_layout.addWidget(self.query_label)
        search_layout.addWidget(self.query_entry)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

        self.results_label = QtWidgets.QLabel('Results:')
        layout.addWidget(self.results_label)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.result_table = QtWidgets.QTableWidget(0, 3)
        self.result_table.setHorizontalHeaderLabels(
            ['Searched URL', 'Category', 'Trusted'])
        self.scroll_area.setWidget(self.result_table)
        self.result_table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)

        self.result_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.result_table.setMouseTracking(True)

        layout.addWidget(self.scroll_area)

    def search(self):
        query = self.query_entry.text()
        if query:
            URLs = [j for j in search(query, num=10, stop=10, pause=2)]

            self.result_table.setRowCount(0)

            json_filename = 'search_results.json'
            if os.path.isfile(json_filename):
                with open(json_filename, 'r') as f:
                    data = json.load(f)
            else:
                data = []

            search_results = []
            for url in URLs:
                row_position = self.result_table.rowCount()
                self.result_table.insertRow(row_position)

                is_shopping = check_category(url)

                if is_shopping:
                    category = "Shopping"
                else:
                    category = "Information"

                if is_shopping:
                    status = check_url(url)
                    if status == 'Trusted':
                        trusted = "Yes"
                    else:
                        trusted = "No"
                else:
                    trusted = ""

                search_results.append(
                    {'URL': url, 'Category': category, 'Trusted': trusted})

                searched_url_item = QtWidgets.QTableWidgetItem(url)
                category_item = QtWidgets.QTableWidgetItem(category)
                trusted_item = QtWidgets.QTableWidgetItem(trusted)

                if not is_shopping:
                    searched_url_item.setBackground(
                        QtGui.QColor(255, 255, 230))
                    category_item.setBackground(QtGui.QColor(255, 255, 230))
                    trusted_item.setBackground(QtGui.QColor(255, 255, 230))

                elif trusted == "Yes":
                    searched_url_item.setBackground(
                        QtGui.QColor(230, 255, 230))
                    category_item.setBackground(QtGui.QColor(230, 255, 230))
                    trusted_item.setBackground(QtGui.QColor(230, 255, 230))
                else:
                    searched_url_item.setBackground(
                        QtGui.QColor(255, 230, 230))
                    category_item.setBackground(QtGui.QColor(255, 230, 230))
                    trusted_item.setBackground(QtGui.QColor(255, 230, 230))

                if trusted == "Yes":
                    # searched_url_item.setFlags(searched_url_item.flags() | QtCore.Qt.ItemIsEditable)
                    searched_url_item.setData(
                        QtCore.Qt.UserRole, QtCore.QUrl(url))

                self.result_table.setItem(row_position, 0, searched_url_item)
                self.result_table.setItem(row_position, 1, category_item)
                self.result_table.setItem(row_position, 2, trusted_item)

                QApplication.processEvents()

            self.result_table.cellDoubleClicked.connect(self.open_url)

            data.append({'query': query, 'results': search_results})

            with open(json_filename, 'w') as f:
                json.dump(data, f, indent=4)

    def open_url(self, row, column):
        if column == 0:
            item = self.result_table.item(row, column)
            url = item.data(QtCore.Qt.UserRole)
            if url is not None:
                QtGui.QDesktopServices.openUrl(url)


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
