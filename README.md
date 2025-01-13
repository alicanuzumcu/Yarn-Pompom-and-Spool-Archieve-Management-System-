# Pom-Pom Shelf System

This is a simple CRUD (Create, Read, Update, Delete) application for managing records of Pom-Pom shelf data. The application allows users to insert, update, delete, and filter records, as well as view the information in a table format. 

The system is built using **PyQt5** for the GUI and connects to a SQL database for storing and managing records.

### Video Demonstration
Click to the video below to see on YouTube.
[![Yarn Pompom and Bobbin Archive Management System](https://img.youtube.com/vi/6lHP5wYNVy0/0.jpg)](https://youtu.be/6lHP5wYNVy0)
 

## Features

- **Insert New Record**: Add a new record by entering details such as color number, cabinet number, cell number, and lot number.
- **Update Record**: Update an existing record by selecting it and modifying its details.
- **Delete Record**: Delete selected records from the database.
- **Filter Records**: Filter records based on the color number.
- **Data Table**: View all records in a table format with columns for ID, color number, cabinet number, cell number, date, and lot number.

## Prerequisites

Make sure you have created a database on your local and the following installed:

- Python 
- PyQt5
- A MySQL or SQLite database for storing the records.

### Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/alicanuzumcu/Yarn-Pompom-and-Bobbin-Archive-Management-System-
    cd pom-pom-shelf-system
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your database by editing the `ConnectSql.py` file to match your database connection details.

### Requirements

- **PyQt5**: The application uses PyQt5 for the GUI.
- **SQL Database**: MySQL or SQLite for storing records.

## Usage

To run the application, execute the following command:

```bash
python main1.py

