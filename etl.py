import os
import pandas as pd
import psycopg2
import re
from configparser import ConfigParser


def create_table(cursor, table_name, headers):
    columns = [f"{header} TEXT" for header in headers]
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
    cursor.execute(drop_table_query)
    cursor.execute(create_table_query)

def clean_string(string):
    # Replace special characters with underscores
    cleaned_string = re.sub(r'[^a-zA-Z0-9_]', '_', string)
    # Replace spaces with underscores
    cleaned_string = cleaned_string.replace(' ', '_')
    return cleaned_string

def transfer_data(file_path, db_host, db_port, db_name, db_user, db_password):
    print(f"file: {file_path}")

    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Extract table name from file name
        print(f"file found: {file_path}")

        # Extract directory and file name from file path
        directory, file_name = os.path.split(file_path)
        table_name = clean_string(file_name.split('.')[0])


        #file_name = file_path.split('/')[-1].split('.')[0]
        #table_name = clean_string(file_name)
        table_name = f"central_{table_name}"

        

        # Read XLS file
        df = pd.read_excel(file_path, dtype=str)
        df = df.fillna('')
        print(file_path)

        # Clean column names
        cleaned_headers = [clean_string(header) for header in df.columns]

        # Create connection to PostgreSQL database
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user
        )
        cursor = connection.cursor()

        # Create table in PostgreSQL
        create_table(cursor, table_name, cleaned_headers)

        # Transform and load data
        for _, row in df.iterrows():
            insert_query = f"INSERT INTO {table_name} ({', '.join(cleaned_headers)}) VALUES {tuple(row.values)}"
            cursor.execute(insert_query)

        # Commit changes and close the connection
        connection.commit()

        
        dump_file_path = f"{table_name}.sql"
        dump_command = f'pg_dump -h {db_host} -p {db_port} -U {db_user} -d {db_name} -t {table_name} > "{dump_file_path}"'
        os.system(dump_command)



        cursor.close()
        connection.close()
        print("Data transfer successful!")
    except FileNotFoundError as e:
        print(f"File not found. Please provide a valid file path. {file_path}" )
    except Exception as e:
        print("Error occurred during data transfer:", str(e))


# Read PostgreSQL configuration
postgres_config = ConfigParser()
postgres_config.read('postgres_config.ini')
postgres_host = postgres_config.get('postgres', 'host')
postgres_port = postgres_config.get('postgres', 'port')
postgres_user = postgres_config.get('postgres', 'user')
postgres_password = postgres_config.get('postgres', 'password')
postgres_database = postgres_config.get('postgres','database')


# Usage




# Get file path from user input
file_path = input("Enter the path of the XLS file: ")

transfer_data(file_path, postgres_host, postgres_port, postgres_database, postgres_user, postgres_password)
