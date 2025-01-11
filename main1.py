# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from ConnectSql import insert_data, delete_data, update_data, list_query, filter_by_color_no, close_connection
from datetime import datetime


class CRUDApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pompom Archieve Management System")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: white;")

        # "Insert" button
        self.add_record_button = QtWidgets.QPushButton()
        self.add_record_button.setIcon(QtGui.QIcon("photos/insert.png"))
        self.add_record_button.setIconSize(QtCore.QSize(45, 45))
        self.add_record_button.clicked.connect(self.open_new_record_dialog)
        self.add_record_button.setToolTip("Insert new record")
        self.add_record_button.setFixedSize(60, 60)
        self.add_record_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
            }
            QPushButton:hover {
                background-color: lightgreen;
            }
            QPushButton:pressed {
                background-color: darkgreen;
            };
            border-radius: 10px;
            font-size: 15px;
            font-family: Arial;
        """)

        # "Update" butonu
        self.update_button = QtWidgets.QPushButton()
        self.update_button.setIcon(QtGui.QIcon("photos/update.png"))
        self.update_button.setIconSize(QtCore.QSize(45, 45))
        self.update_button.clicked.connect(self.open_update_window)
        self.update_button.setEnabled(False)  
        self.update_button.setFixedSize(60, 60)
        self.update_button.setToolTip("Update record")
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
            }
            QPushButton:hover {
                background-color: orange;
            }
            QPushButton:pressed {
                background-color: darkorange;
            };
            border-radius: 10px;
            font-size: 15px;
            font-family: Arial;
        """)

        # "Delete" button
        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setIcon(QtGui.QIcon("photos/delete2.png"))
        self.delete_button.setIconSize(QtCore.QSize(45, 45))
        self.delete_button.clicked.connect(self.delete_record)
        self.delete_button.setEnabled(False) 
        self.delete_button.setFixedSize(60, 60)
        self.delete_button.setToolTip("Delete record")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
            }
            QPushButton:hover {
                background-color: blue;
            }
            QPushButton:pressed {
                background-color: darkblue;
            };
            border-radius: 10px;
            font-size: 15px;
            font-family: Arial;
        """)

        # filter by color no
        self.color_filter_box = QtWidgets.QLineEdit()
        self.color_filter_box.setPlaceholderText("Filter by color no")
        self.color_filter_box.textChanged.connect(self.filter_records)  # in each type refresh the list
        self.color_filter_box.setStyleSheet("""
            background-color: black;
            color: white;
            border: 3px solid black;
            border-radius: 10px;
        """)

        # Create table
        self.record_table = QtWidgets.QTableWidget()
        self.record_table.setColumnCount(6)  # 6 columns
        self.record_table.setHorizontalHeaderLabels(["ID", "Color no", "Cabinet no", "Cell no", "Date", "Lot No"])
        
        # Create a bold font
        header_font = QtGui.QFont()
        header_font.setBold(True)

        # Apply the bold font to the header
        self.record_table.horizontalHeader().setFont(header_font)

        # Row selection signal
        self.record_table.itemSelectionChanged.connect(self.enable_buttons)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        Hlayout = QtWidgets.QHBoxLayout()
        Hlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        Hlayout.addWidget(self.add_record_button)
        Hlayout.addWidget(self.update_button)  
        Hlayout.addWidget(self.delete_button)

        # Wrap Hlayout in a QWidget
        Hwidget = QtWidgets.QWidget()
        Hwidget.setLayout(Hlayout)

        layout.addWidget(Hwidget)  
        layout.addWidget(self.color_filter_box)
        layout.addWidget(self.record_table)

        self.setLayout(layout)
        self.load_records()

    def enable_buttons(self):
        # Enable delete and update buttons if a row is selected
        self.delete_button.setEnabled(self.record_table.currentRow() >= 0)
        self.update_button.setEnabled(self.record_table.currentRow() >= 0)

    def open_new_record_dialog(self):
        dialog = NewRecordDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_records()
            self.show_message("New record added successfully.")

    def open_update_window(self):
        selected_row = self.record_table.currentRow()
        if selected_row >= 0:
            # Send the selected row's data to the UpdateWindow
            row_data = [self.record_table.item(selected_row, col).text() for col in range(6)]
            dialog = UpdateWindow(row_data)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                self.load_records()
                self.show_message("Record updated successfully!")

    def delete_record(self):
        selected_items = self.record_table.selectedItems() 
    
        if not selected_items:
            return  

        # Create a set of selected row indices
        selected_rows = set(item.row() for item in selected_items)

        # Get the color numbers
        color_nos = [self.record_table.item(row, 1).text() for row in selected_rows]  # 1. sütundan renk numaralarını al
        
        # Confirmation message
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirm",
            f"{', '.join(color_nos)} Are you sure you want to delete data for the following color codes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes
            )

        if reply == QtWidgets.QMessageBox.Yes:
            for row in sorted(selected_rows, reverse=True):  
                record_id = int(self.record_table.item(row, 0).text()) 
                delete_data(record_id) 
                
                self.load_records()  
                self.show_message("Logs deleted successfully!")



    def filter_records(self):
        color_no = self.color_filter_box.text().strip()
        if color_no:
            records = filter_by_color_no(color_no)
            self.populate_table(records)
        else:
            self.load_records()

    def load_records(self):
        records = list_query()
        self.populate_table(records)

    def populate_table(self, records):
        records = records or []
        self.record_table.setRowCount(0)
        for row in records:
            row_position = self.record_table.rowCount()
            self.record_table.insertRow(row_position)
            for column in range(len(row)):
                self.record_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(row[column])))

    @staticmethod
    def show_message(message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(message)
        msg_box.setWindowTitle("Message")
        msg_box.exec_()

    def closeEvent(self, event):
        close_connection()
        event.accept()


# Yeni kayıt ekleme penceresi
class NewRecordDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Record")
        self.setGeometry(200, 200, 400, 300)

        # Fields for new record information
        self.color_no_label = QtWidgets.QLabel("Color No:")
        self.color_no_entry = QtWidgets.QLineEdit()
        self.cabinet_no_label = QtWidgets.QLabel("Cabinet No:")
        self.cabinet_no_entry = QtWidgets.QLineEdit()
        self.cell_no_label = QtWidgets.QLabel("Cell No:")
        self.cell_no_entry = QtWidgets.QLineEdit()
        self.lot_no_label = QtWidgets.QLabel("Lot No:")
        self.lot_no_entry = QtWidgets.QLineEdit()

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_record)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.color_no_label)
        layout.addWidget(self.color_no_entry)
        layout.addWidget(self.cabinet_no_label)
        layout.addWidget(self.cabinet_no_entry)
        layout.addWidget(self.cell_no_label)
        layout.addWidget(self.cell_no_entry)
        layout.addWidget(self.lot_no_label)
        layout.addWidget(self.lot_no_entry)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_record(self):
        try:
            color_no_text = self.color_no_entry.text()
            cabinet_no_text = self.cabinet_no_entry.text()
            cell_no_text = self.cell_no_entry.text()
            lot_no_text = self.lot_no_entry.text().strip()

            if not color_no_text:
                raise ValueError("Color number cannot be empty!")
            if not cabinet_no_text.isdigit():
                raise ValueError("Cabinet no cannot be empty!")
            if not cell_no_text.isdigit():
                raise ValueError("Cell no cannot be empty!")
            if lot_no_text and not lot_no_text.isdigit():
                raise ValueError("Lot no cannot be empty!")

            insert_data(color_no_text, int(cabinet_no_text), int(cell_no_text), int(lot_no_text) if lot_no_text else None)
            self.accept()
        except Exception as e:
            CRUDApp.show_message(str(e))
            

# Updating Window
class UpdateWindow(QtWidgets.QDialog):
    def __init__(self, record_data):
        super().__init__()
        self.setWindowTitle("Update Record")
        self.setGeometry(200, 200, 400, 300)

        self.record_id = record_data[0]
        self.color_no_entry = QtWidgets.QLineEdit(record_data[1])
        self.cabinet_no_entry = QtWidgets.QLineEdit(record_data[2])
        self.cell_no_entry = QtWidgets.QLineEdit(record_data[3])
        self.date_entry = QtWidgets.QLineEdit(record_data[4])
        self.lot_no_entry = QtWidgets.QLineEdit(record_data[5])

        self.save_button = QtWidgets.QPushButton("Update")
        self.save_button.clicked.connect(self.save_update)  

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Color No:"))
        layout.addWidget(self.color_no_entry)
        layout.addWidget(QtWidgets.QLabel("Cabinet No:"))
        layout.addWidget(self.cabinet_no_entry)
        layout.addWidget(QtWidgets.QLabel("Cell No:"))
        layout.addWidget(self.cell_no_entry)
        layout.addWidget(QtWidgets.QLabel("Lot No:"))
        layout.addWidget(self.lot_no_entry)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_update(self):
        try:
            color_no_text = self.color_no_entry.text()
            cabinet_no_text = self.cabinet_no_entry.text() 
            cell_no_text = self.cell_no_entry.text()
            #lot_no_text = self.lot_no_entry.text() or ""
            #lot_no_text = self.lot_no_entry.text() if self.lot_no_entry.text() != 'None' None else None
            if self.lot_no_entry.text()=='':
                lot_no_text=None
            elif self.lot_no_entry.text() != 'None':
                lot_no_text=self.lot_no_entry.text()
            else:
                lot_no_text=None
            if not color_no_text:
                raise ValueError("Color number cannot be empty!")
            if not cabinet_no_text.isdigit():
                raise ValueError("Cabinet number cannot be empty!")
            if not cell_no_text.isdigit():
                raise ValueError("Cell number cannot be empty!")
            if lot_no_text and not lot_no_text.isdigit():
                raise ValueError("Lot number cannot be empty!")


            # Get the updated data
            date_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  

            update_data(int(self.record_id), color_no_text, int(cabinet_no_text), int(cell_no_text), lot_no_text, date_text)
            self.accept()
        except Exception as e:
            CRUDApp.show_message(str(e))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CRUDApp()
    window.show()
    sys.exit(app.exec_())
