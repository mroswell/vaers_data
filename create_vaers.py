# Given the clarification that the non-domestic files represent the same structure as the yearly files but pertain to non-US data, you can easily modify the script to handle both domestic (yearly) and non-domestic data. The approach involves adding a step to process the non-domestic files after or before handling the yearly files, ensuring all data is consolidated into the database. Here's an updated version of the script that includes processing for both types of files:

import sqlite3
import csv
import os

# Database connection
conn = sqlite3.connect('vaers_data.db')
c = conn.cursor()

# Create tables - Assuming the table creation code is here (omitted for brevity)

# Function to insert data from CSV to the database
def insert_csv_data(file_path, table_name, columns):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        placeholders = ', '.join(['?'] * len(columns))
        sql = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
        for row in reader:
            values = [row[column] for column in columns]
            c.execute(sql, values)


# Process yearly and non-domestic files
def process_files(directory_path):
    # Process non-domestic files first
    non_domestic_files = [
        ("NonDomesticVAERSDATA.csv", "VAERSData", ["VAERS_ID", "RECVDATE", "STATE", "AGE_YRS", "CAGE_YR", "CAGE_MO", "SEX", "RPT_DATE", "SYMPTOM_TEXT", "DIED", "DATEDIED", "L_THREAT", "ER_VISIT", "HOSPITAL", "HOSPDAYS", "X_STAY", "DISABLE", "RECOVD", "VAX_DATE", "ONSET_DATE", "NUMDAYS", "LAB_DATA", "V_ADMINBY", "V_FUNDBY", "OTHER_MEDS", "CUR_ILL", "HISTORY", "PRIOR_VAX", "SPLTTYPE", "FORM_VERS", "TODAYS_DATE", "BIRTH_DEFECT", "OFC_VISIT", "ER_ED_VISIT", "ALLERGIES"]),
        ("NonDomesticVAERSSYMPTOMS.csv", "VAERSSymptoms", ["VAERS_ID", "SYMPTOM1", "SYMPTOMVERSION1", "SYMPTOM2", "SYMPTOMVERSION2", "SYMPTOM3", "SYMPTOMVERSION3", "SYMPTOM4", "SYMPTOMVERSION4", "SYMPTOM5", "SYMPTOMVERSION5"]),
        ("NonDomesticVAERSVAX.csv", "VAERSVax", ["VAERS_ID", "VAX_TYPE", "VAX_MANU", "VAX_LOT", "VAX_DOSE_SERIES", "VAX_ROUTE", "VAX_SITE", "VAX_NAME"])
    ]

    for file_name, table_name, columns in non_domestic_files:
        file_path = os.path.join(directory_path, file_name)
        if os.path.exists(file_path):
            insert_csv_data(file_path, table_name, columns)
        else:
            print(f"File not found: {file_path}")


    # Process yearly files
    for year in range(1990, 2025):  # Adjust end year as necessary
        for file_type, table_name, columns in [
            (f"{year}VAERSDATA.csv", "VAERSData", ["VAERS_ID", "RECVDATE", "STATE", "AGE_YRS", "CAGE_YR", "CAGE_MO", "SEX", "RPT_DATE", "SYMPTOM_TEXT", "DIED", "DATEDIED", "L_THREAT", "ER_VISIT", "HOSPITAL", "HOSPDAYS", "X_STAY", "DISABLE", "RECOVD", "VAX_DATE", "ONSET_DATE", "NUMDAYS", "LAB_DATA", "V_ADMINBY", "V_FUNDBY", "OTHER_MEDS", "CUR_ILL", "HISTORY", "PRIOR_VAX", "SPLTTYPE", "FORM_VERS", "TODAYS_DATE", "BIRTH_DEFECT", "OFC_VISIT", "ER_ED_VISIT", "ALLERGIES"]),
            (f"{year}VAERSSYMPTOMS.csv", "VAERSSymptoms", ["VAERS_ID", "SYMPTOM1", "SYMPTOMVERSION1", "SYMPTOM2", "SYMPTOMVERSION2", "SYMPTOM3", "SYMPTOMVERSION3", "SYMPTOM4", "SYMPTOMVERSION4", "SYMPTOM5", "SYMPTOMVERSION5"]),
            (f"{year}VAERSVAX.csv", "VAERSVax", ["VAERS_ID", "VAX_TYPE", "VAX_MANU", "VAX_LOT", "VAX_DOSE_SERIES", "VAX_ROUTE", "VAX_SITE", "VAX_NAME"])
        ]:
            file_path = os.path.join(directory_path, file_type)
            if os.path.exists(file_path):
                insert_csv_data(file_path, table_name, columns)
            else:
                print(f"File not found: {file_path}")

    conn.commit()

# Replace 'path/to/your/directory' with the actual directory path
directory_path = '.'
process_files(directory_path)

conn.close()
