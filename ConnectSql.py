# -*- coding: utf-8 -*-
import pyodbc
from datetime import datetime

# Connection settings
server = 'LAPTOP-ADPAUIQ5\\SQLEXPRESS'  # SQL Server address (localhost or server name)
database = 'QualityControlDB'  # Database to connect to

# Connection string (using Windows Authentication)
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Open connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


def insert_data(color_no, cabinet_no, cell_no, lot_no=None, date=None):
    if not all([color_no, cabinet_no, cell_no]):
        print("Error: Color Number, Cabinet Number, and Cell Number cannot be empty.")
        return
    
    try:
        date = date or datetime.now()  # Default to today's date if no date is provided
        insert_query = """
            INSERT INTO YarnStorage (color_no, cabinet_no, cell_no, date, lot_no)
            VALUES (?,?,?,?,?)
        """
        data = (color_no, cabinet_no, cell_no, date, lot_no)
        cursor.execute(insert_query, data)
        conn.commit()
    except Exception as e:
        print(f"Error (Data Insertion): {e}")


def delete_data(row_id):
    if not row_id:
        print("Error: Row ID to delete cannot be empty.")
        return
    
    try:
        delete_query = "DELETE FROM YarnStorage WHERE ID= ?"
        cursor.execute(delete_query, row_id)
        conn.commit()
        print("Record successfully deleted.")
    except Exception as e:
        print(f"Error (Data Deletion): {e}")


def update_data(row_id, new_color_no, new_cabinet_no, new_cell_no, new_lot_no, new_date):
    if not row_id or not all([new_color_no, new_cabinet_no, new_cell_no]):
        print("Error: All fields must be filled for update.")
        return
    
    try:
        new_date = new_date or datetime.now()
        update_query = """
            UPDATE YarnStorage
            SET color_no = ?, cabinet_no = ?, cell_no = ?, lot_no = ?, date = ?
            WHERE ID = ?
        """
        data = (new_color_no, new_cabinet_no, new_cell_no, new_lot_no, new_date, row_id)
        cursor.execute(update_query, data)
        conn.commit()
        print("Record successfully updated.")
    except Exception as e:
        print(f"Error (Data Update): {e}")
        

def list_query():
    try:
        select_query = "SELECT * FROM YarnStorage"
        cursor.execute(select_query)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error (Record Listing): {e}")
        return []


def filter_by_color_no(color_no):
    try:
        cursor.execute("SELECT * FROM YarnStorage WHERE color_no LIKE ?", (f"%{color_no}%",))
        records = cursor.fetchall()
        return records if records else []  # Return empty list if no data found
    except Exception as e:
        print(f"Error: {e}")
        return []


def close_connection():
    try:
        conn.close()
    except Exception as e:
        print(f"Error (Closing Connection): {e}")
