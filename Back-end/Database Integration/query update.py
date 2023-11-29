import mysql.connector as mysql
import pickle

mydb = mysql.connect(host='localhost', user='root', password='Unique@32')
mycursor = mydb.cursor()
mycursor.execute("USE nptel")

# get the table names present in the database
mycursor.execute("SHOW TABLES")
tables = mycursor.fetchall()
tables = [i[0] for i in tables]
# print(tables)

# create a dictionary with key as table names and values as column names
table_columns = {}

# get the column names of each table
for table in tables:
    mycursor.execute("SHOW COLUMNS FROM "+table)
    columns = mycursor.fetchall()
    columns = [i[0] for i in columns]
    # print(f"{table}:", columns)
    table_columns[table] = columns

# print(table_columns)

def print_count_of_rows():
    # Get the total number of columns in each table
    for table in tables:
        mycursor.execute("SELECT COUNT(*) FROM "+table)
        count = mycursor.fetchall()
        count = count[0][0]
        print(f"{table}:", count)

# print_count_of_rows()

def find_mapping(table_name, columns, global_columns):
    # Ontology based matching
    if table_name == 'skillshare':
        mapping = {
            'local_course_id': 'id',
            'course_name': 'Title',
            'course_description': """CONCAT(Instructor: , instructor, course duration: , course_duration)""",
            'university': '"NA"',
            'course_url': 'URL',
            'price': 'price',
            'course_vendor': '"skillshare"'
        }
    elif table_name == 'udacity':
        mapping = {
            'local_course_id': 'number',
            'course_name': 'Name',
            'course_description': 'About',
            'university': 'School',
            'course_url': 'Link',
            'price': 'Price',
            'course_vendor': '"udacity"'
        }
    elif table_name == 'udemy':
        mapping = {
            'local_course_id': 'course_id',
            'course_name': 'course_title',
            'course_description': """CONCAT(Subject: , subject, Number of lecture: , num_lectures, content duration in hours: , content_duration, Course Level: , level)""",
            'university': '"NA"',
            'course_url': 'url',
            'price': 'price',
            'course_vendor': '"udemy"'
        }
    elif table_name == 'nptel':
        mapping = {
            'local_course_id': 'id',
            'course_name': 'Course_Name',
            'course_description': """CONCAT(Prof: , SME_Name, Duration: , Duration, Applicable_NPTEL_Domain: , IFNULL(Applicable_NPTEL_Domain, 'NA'))""",
            'university': 'Institute',
            'course_url': 'NPTEL_URL',
            'price': 'Price',
            'course_vendor': '"nptel"'
        }
    elif table_name == 'coursera':
        mapping = {
            'local_course_id': 'Course_number',
            'course_name': 'Course_Name',
            'course_description': 'Course_Description',
            'university': 'University',
            'course_url': 'Course_URL',
            'price': 'Price',
            'course_vendor': '"coursera"'
        }
    else:
        with open('metadata_mapping.pkl', 'rb') as f:
            mapping = pickle.load(f)
        return mapping[table_name]
    
    return mapping

def get_columns(table_name):
    mycursor.execute("SHOW COLUMNS FROM "+table_name)
    res = mycursor.fetchall()
    columns = [i[0] for i in res]
    return columns


def update_table(actual_query, table_name, table_columns, table_description, execution=False, values=None, delete=None, update=None):
    # Execute actual_query
    print('----------------------------ACTUAL--QUERY--------------------------------')
    print(actual_query)
    print('-------------------------------------------------------------------------')
    if execution:
        mycursor.execute(actual_query)
        mydb.commit()
        print("Actual query executed successfully!")

    query = actual_query.split(' ')
    global_table_name = 'course_bucket'
    global_columns = get_columns(global_table_name)
    # print(f'{global_table_name}:', global_columns)

    # find the mapping between the columns of this table and the global table
    mapped_dic = find_mapping(table_name, table_columns, global_columns)

    # Create the mapped query
    mapped_query = ''
    if query[0].lower() == 'insert':
        # Insert the record in the db table
        mapped_query += f'INSERT INTO {global_table_name} (local_course_id, course_name, course_description, university, course_url, price, course_vendor) VALUES ( '
        # Explicitly check whether the course_description is also split into multiple columns or not
        
        # print(values)
        value_mapping = {}
        for i in range(len(values)):
            value_mapping[table_columns[i]] = values[i]
        # print(value_mapping)

        mapped_query += value_mapping[mapped_dic['local_course_id']]+", '"+value_mapping[mapped_dic['course_name']]+"', "
        # mapped_query += value_mapping[mapped_dic['course_description']]
        # print(mapped_query)

        course_descr = mapped_dic['course_description']
        # Check if the course_descr is a string or a function by looking for the word CONCAT
        if 'CONCAT' in course_descr:
            course_descr_temp = course_descr[7:-1]
            course_descr_temp = course_descr_temp.split(', ')
            # check if IFNULL is there in the second last term
            if 'IFNULL' in course_descr_temp[-2]:
                course_descr_temp[-2] = course_descr_temp[-2][7:]
                course_descr_temp = course_descr_temp[:-1]

            for i in range(len(course_descr_temp)):
                if i%2 == 1:
                    # check if it exists in the value_mapping
                    if course_descr_temp[i] in value_mapping:
                        course_descr_temp[i] = value_mapping[course_descr_temp[i]]+','
                    else:
                        course_descr_temp[i] = "'NA'"+','

            course_descr_temp[-1] = course_descr_temp[-1][:-1]
            course_descr_temp = ' '.join(course_descr_temp)
            course_descr_temp = "'"+course_descr_temp+"'"
            mapped_query += course_descr_temp+', '
        else:
            # This is a string
            mapped_query += "'"+value_mapping[course_descr]+"', "
        
        if mapped_dic['university'] == '"NA"':
            mapped_query += mapped_dic['university']+', '
        else:
            mapped_query += "'"+value_mapping[mapped_dic['university']]+"', "
        
        mapped_query += "'"+value_mapping[mapped_dic['course_url']]+"', "+value_mapping[mapped_dic['price']]+', '
        mapped_query += mapped_dic['course_vendor']
        mapped_query += ');'
    

    elif query[0].lower() == 'delete':
        # Delete the record from the db table
        mapped_query += f'DELETE FROM {global_table_name} WHERE '
        delete = delete.strip()
        if delete != '':
            # delete contains the where clause
            # iterate over delete and replace col_names with value_mapping and mapping_dic if it exists
            delete = delete.split(' and ')
            for i in range(len(delete)):
                if '=' in delete[i]:
                    key, value = delete[i].split('=')
                    cmp_operator = '='
                elif 'like' in delete[i]:
                    key, value = delete[i].split('like')
                    cmp_operator = 'like'
                elif '>' in delete[i]:
                    key, value = delete[i].split('>')
                    cmp_operator = '>'
                elif '<' in delete[i]:
                    key, value = delete[i].split('<')
                    cmp_operator = '<'
                else:
                    key, value = delete[i].split('in')
                    cmp_operator = 'in'

                key = key.strip()   # this is the key in the local table
                value = value.strip()   # this is the value in the local table
                # print(key, value)
                # search mapped_dic.values() for the key (reverse mapping)
                foundKey = False
                for k, v in mapped_dic.items():
                    if v == key:
                        global_mapped_key = k   # this is the key in the global table
                        foundKey = True
                        break
                
                if not foundKey:
                    break

                # all keys are present in the value_mapping
                # do the value_mapping for all keys
                mapped_query += global_mapped_key+" "+cmp_operator+" "+value+' and '
            
            if not foundKey:
                # no mapping found; refresh the global table
                mapped_query = f"DELETE FROM {global_table_name} WHERE course_vendor = '{table_name}';"
                if execution:
                    mycursor.execute(mapped_query)
                    mydb.commit()
                # print(mapped_query)
                mapped_query = f"INSERT INTO {global_table_name} (local_course_id, course_name, course_description, university, course_url, price, course_vendor) SELECT "
                for k, v in mapped_dic.items():
                    mapped_query += v+', '
                mapped_query = mapped_query[:-2]+' '
                mapped_query += f"FROM {table_name};"
            else:
                mapped_query = mapped_query[:-5]+f" and course_vendor = '{table_name}';"
        else:
            mapped_query += f' course_vendor = "{table_name}";'


    elif query[0].lower() == 'update':
        if update != '':
            mapped_query = f"DELETE FROM {global_table_name} WHERE course_vendor = '{table_name}';"
            if execution:
                mycursor.execute(mapped_query)
                mydb.commit()
            # print(mapped_query)
            mapped_query = f"INSERT INTO {global_table_name} (local_course_id, course_name, course_description, university, course_url, price, course_vendor) SELECT "
            for k, v in mapped_dic.items():
                mapped_query += v+', '
            mapped_query = mapped_query[:-2]+' '
            mapped_query += f"FROM {table_name};"
        else:
            where = delete
            mapped_query += 'UPDATE '+global_table_name+' SET '
            # check for mapping in the update variable
            update = update.split(',')
            update = [i.strip() for i in update]
            # check if all attributes are in the update are present in the global table or not
            for i in range(len(update)):
                if '=' in update[i]:
                    key, value = update[i].split('=')
                    cmp_operator = '='
                elif 'like' in update[i]:
                    key, value = update[i].split('like')
                    cmp_operator = 'like'
                elif '>' in update[i]:
                    key, value = update[i].split('>')
                    cmp_operator = '>'
                elif '<' in update[i]:
                    key, value = update[i].split('<')
                    cmp_operator = '<'
                else:
                    key, value = update[i].split('in')
                    cmp_operator = 'in'

                key = key.strip()
                value = value.strip()
                print(key, value)
                # search mapped_dic.values() for the key (reverse mapping)
                foundKey = False
                for k, v in mapped_dic.items():
                    if v == key:
                        global_mapped_key = k
                        foundKey = True
                        break
                
                if not foundKey:
                    break
            
            if not foundKey:
                # no mapping found; refresh the global table
                mapped_query = f"DELETE FROM {global_table_name} WHERE course_vendor = '{table_name}';"
                if execution:
                    mycursor.execute(mapped_query)
                    mydb.commit()
                print(mapped_query)
                mapped_query = f"INSERT INTO {global_table_name} (local_course_id, course_name, course_description, university, course_url, price, course_vendor) SELECT "
                for i in range(len(table_columns)):
                    if i == len(table_columns)-1:
                        mapped_query += table_columns[i]+' '
                    else:
                        mapped_query += table_columns[i]+', '
                mapped_query += f"FROM {table_name};"
            pass
    print('-------------------------MAPPED---QUERY----------------------------------')
    print(mapped_query)
    print('-------------------------------------------------------------------------')
    if execution:
        mycursor.execute(mapped_query)
        mydb.commit()
        print("Mapped query executed successfully!")


def take_input():
    table_name = input("Enter the local table name: ")
    mycursor.execute("SHOW COLUMNS FROM "+table_name)
    res = mycursor.fetchall()
    table_columns = [i[0] for i in res]
    table_description = [i[1] for i in res]
    table_description = [i.decode('utf-8') for i in table_description]
    
    return table_name, table_columns, table_description


def main(execution=True):
    # creating a main menu with insert, delete, update and exit options for each database table
    print("Welcome to the main menu!")
    
    print("1. Insert")
    print("2. Delete")
    print("3. Update")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    while choice != 4:
        if choice == 1:
            table_name, table_columns, table_description = take_input()
            values = []
            print("Enter the values for each column - ")
            for i in range(len(table_columns)):
                value = input(f"{table_columns[i]}: ")
                values.append(value)

            
            query = f"INSERT INTO {table_name} ("
            for i in range(len(table_columns)):
                query += table_columns[i]
                if i != len(table_columns)-1:
                    query += ', '
            query += ') VALUES ('
            for i in range(len(values)):
                # check if the value is a string or not through the table_description
                if 'int' in table_description[i] or 'float' in table_description[i] or 'double' in table_description[i]:
                    print(f"This was an int {values[i]}")
                    query += values[i]
                else:
                   query += "'"+values[i]+"'"
                if i != len(values)-1:
                    query += ', '
            query += ');'
            print(query)

            update_table(query, table_name, table_columns, table_description, execution=execution, values=values)
        
        elif choice == 2:
            table_name, table_columns, table_description = take_input()

            print('These are the columns to choose from: ')
            print(table_columns)
            delete = input('Enter the delete condition: ')
            
            query = f"DELETE FROM {table_name} WHERE {delete};"
            print(query)

            update_table(query, table_name, table_columns, table_description, execution=execution, delete=delete)

        elif choice == 3:
            table_name, table_columns, table_description = take_input()

            print('These are the columns to choose from: ')
            print(table_columns)
            update = input('Enter the update condition: ')
            query = f"UPDATE {table_name} SET {update} "
            where = input('Enter the filter conditions (where clause): ').strip()
            if where != '':
                query += 'WHERE '+where+';'
            else:
                query += ';'
            print(query)

            update_table(query, table_name, table_columns, table_description, execution=execution, update=update, delete=where)

        else:
            print("Invalid choice!")
        
        print('------------------------------------------')
        print("1. Insert")
        print("2. Delete")
        print("3. Update")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

main(execution=True)

# table_name = 'skillshare'
# mycursor.execute("SHOW COLUMNS FROM "+table_name)
# res = mycursor.fetchall()
# table_columns = [i[0] for i in res]
# table_description = [i[1] for i in res]
# table_description = [i.decode('utf-8') for i in table_description]
# query = '''INSERT INTO skillshare (id, Title, URL, students_count, course_duration, instructor, lessions_count, level, student_projects, engaging, clarity, quality, price) VALUES 
# (29999, 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', '0', '2.5 hours', 'Darrel Wilson', '21', 'Beginner', '1', '4.5', '4.5', '4.5', 80000);'''
# values = ['29999', 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', '0', '2.5 hours', 'Darrel Wilson', '21', 'Beginner', '1', '4.5', '4.5', '4.5', '80000']

# query for inserting into coursera table
# query = '''INSERT INTO coursera_courses (Course_number, Course_Name, University, Difficulty_Level, Course_Rating, Course_URL, Course_Description, Skills, Price) VALUES 
# (29999, 'Learn How to Create a WordPress Website', 'NA', 'Beginner', '4.5', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 'Instructor: Darrel Wilson course duration: 2.5 hours', 'NA', 80000);'''
# values = ['29999', 'Learn How to Create a WordPress Website', 'NA', 'Beginner', '4.5', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 'Instructor: Darrel Wilson course duration: 2.5 hours', 'NA', '80000']

# # query for inserting into udacity table
# query = '''INSERT INTO udacity_courses (number, Name, School, Difficulty_Level, Rating, Link, About, Price) VALUES
# (29999, 'Learn How to Create a WordPress Website', 'NA', 'Beginner', '4.5', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 'Instructor: Darrel Wilson course duration: 2.5 hours', 80000);'''
# values = ['29999', 'Learn How to Create a WordPress Website', 'NA', 'Beginner', '4.5', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 'Instructor: Darrel Wilson course duration: 2.5 hours', '80000']

# query for inserting into udemy table
# query = '''INSERT INTO udemy_courses (course_id, course_title, url, is_paid, price, num_subscribers, num_reviews, num_lectures, level, content_duration, published_timestamp, subject) VALUES
# ('1111', 'Introductory Financial Accounting', 'https://www.udemy.com/introductory-financial-accounting/', 'True', '80', '1793', '265', '54', 'Beginner Level', '10', '2012-10-03T03:20:10Z', 'Business Finance');'''
# values = ['1111', 'Introductory Financial Accounting', 'https://www.udemy.com/introductory-financial-accounting/', 'True', '80', '1793', '265', '54', 'Beginner Level', '10', '2012-10-03T03:20:10Z', 'Business Finance'
# ]

# query = '''DELETE FROM skillshare WHERE Title = 'Learn How to Create a WordPress Website' and Course_Rating='4.5';'''
# delete = "Title = 'Learn How to Create a WordPress Website' and Course_Rating='4.5'"

# update query
# query = '''UPDATE skillshare SET id = 4344 WHERE Title = 'Learn How to Create a WordPress Website' and Course_Rating='4.5';'''
# update = "id = 4344"
# delete = "Title = 'Learn How to Create a WordPress Website' and Course_Rating='4.5'"
# update_table(query, table_name, table_columns, table_description, execution=False, update=update, delete=delete)
































# query for inserting into coursera table
# query = '''INSERT INTO coursera_courses (Course_number, Course_Name, University, Difficulty_Level, Course_Rating, Course_URL, Course_Description, Skills, Price) VALUES (29999, 'Learn How to Create a WordPress Website', 'NA', 'Beginner', '4.5', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 'Instructor: Darrel Wilson course duration: 2.5 hours', 'NA', 80000);'''
# query for deleting from skillshare table
# query = '''DELETE FROM skillshare_courses WHERE id = 29999;'''
# update_table(query, table_columns)
# mycursor.execute('''SELECT * FROM course_bucket WHERE local_course_id = 29999 and course_vendor = 'skillshare';''')
# print(mycursor.fetchall())

# Query for deleting a record from the course_bucket table.
# query = '''DELETE FROM course_bucket WHERE course_id = 29999;'''

# Query for inserting a record into the course_bucket table.
# query = '''INSERT INTO course_bucket (course_id, course_name, course_description, university, course_url, price, course_vendor) VALUES (29999, 'Learn How to Create a WordPress Website', 'Instructor: Darrel Wilson, course duration: 2.5 hours', 'NA', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 80000, 'skillshare');'''

# Query for updating a record in the course_bucket table.
# query = '''UPDATE course_bucket SET price = 89000 WHERE course_id = 29999;'''


# Write an insert query for inserting into skillshare_courses
# query_insert = '''INSERT INTO skillshare_courses (id, Title, URL, students_count, course_duration, instructor, lessions_count, level, student_projects, engaging, clarity, quality, price) VALUES (29999, 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 0, '2.5 hours', 'Darrel Wilson', 21, 'Beginner', '1', '4.5', '4.5', '4.5', 80000);'''
# query_update = '''UPDATE skillshare_courses SET price = 89000 WHERE id = 29999;'''
# query_delete = '''DELETE FROM skillshare_courses WHERE id = 29999;'''
'''
['course_bucket', 'coursera_courses', 'nptel_courses', 'skillshare_courses', 'udacity_courses', 'udemy_courses']
course_bucket:      ['id', 'local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'course_vendor', 'price']

coursera_courses:   ['Course_number', 'Course_Name', 'University', 'Difficulty_Level', 'Course_Rating', 'Course_URL', 'Course_Description', 'Skills', 'Price']
nptel_courses:      ['id', 'Discipline', 'Course_Name', 'SME_Name', 'Institute', 'Co-ordinating_Institute', 'Duration', 'Type_of_course', 'Start_date', 'End_date', 'Exam_date', 'Enrollment_End_date', 'Exam_Registration_End_date', 'UG/PG', 'Core/Elective', 'FDP', 'Applicable_NPTEL_Domain', 'Click_here_to_join_the_course', 'Old_course_URL', 'NPTEL_URL', 'Price']
skillshare_courses: ['id', 'Title', 'URL', 'students_count', 'course_duration', 'instructor', 'lessions_count', 'level', 'student_projects', 'engaging', 'clarity', 'quality', 'price']
udacity_courses:    ['number', 'Name', 'School', 'Difficulty_Level', 'Rating', 'Link', 'About', 'Price']
udemy_courses:      ['course_id', 'course_title', 'url', 'is_paid', 'price', 'num_subscribers', 'num_reviews', 'num_lectures', 'level', 'content_duration', 'published_timestamp', 'subject']
'''
