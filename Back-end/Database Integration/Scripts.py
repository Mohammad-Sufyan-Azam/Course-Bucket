# connect to the mysql server. the connection string is root@127.0.0.1:3306
import mysql.connector as mysql
import pandas as pd


mydb = mysql.connect(host='localhost', database='nptel', user='root', password='Unique@32')
if not mydb.is_connected():
    print('Could not connect to MySQL database')
    exit(1)
else:
    print('Connected to MySQL database\n')


def print_tables():
    # print all table names in the database
    mycursor = mydb.cursor()
    mycursor.execute('show tables;')
    tables = mycursor.fetchall()
    print('Tables in the database:')
    for table in tables:
        print(*table)
    print('\n')


# print all table names in the database
mycursor = mydb.cursor()
# print_tables()


# create a function that takes a csv as input and creates a table in the database to store its data
def create_table(csv_file):
    df = pd.read_csv(csv_file)
    column_names = list(df.columns)
    
    table_name = csv_file.split('/')[-1].split('.')[0]
    # figuring out the data type of each column using infer_objects()
    data_types = []
    for column in column_names:
        # replace 'object' type with 'varchar(255)' type
        type = str(df[column].infer_objects().dtype)
        if type == 'object':
            data_types.append('varchar(255)')
        else:
            data_types.append(type)
    print(data_types)
    

    query = 'CREATE TABLE ' + table_name + ' ('
    for column in column_names:
        query += column + ' VARCHAR(255), '
    query = query[:-2] + ');'
    # mycursor.execute(query)
    print(query)
    print('Table created successfully')

# create_table('Back-end/Database Integration/skillshare_courses.csv')