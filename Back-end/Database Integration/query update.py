import mysql.connector as mysql

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
    # course_bucket:      ['id', 'local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'course_vendor', 'price']

    # Ontology based matching
    if table_name == 'skillshare_courses':
        mapping = {
            'local_course_id': 'id',
            'course_name': 'Title',
            'course_description': """CONCAT(Instructor: , instructor, course duration: , course_duration)""",
            'university': '"NA"',
            'course_url': 'URL',
            'price': 'price',
            'course_vendor': '"skillshare"'
        }
    elif table_name == 'udacity_courses':
        mapping = {
            'local_course_id': 'number',
            'course_name': 'Name',
            'course_description': 'About',
            'university': 'School',
            'course_url': 'Link',
            'price': 'Price',
            'course_vendor': '"udacity"'
        }
    elif table_name == 'udemy_courses':
        mapping = {
            'local_course_id': 'course_id',
            'course_name': 'course_title',
            'course_description': """CONCAT(Subject: , subject, Number of lecture: , num_lectures, content duration in hours: , content_duration, Course Level: , level)""",
            'university': '"NA"',
            'course_url': 'url',
            'price': 'price',
            'course_vendor': '"udemy"'
        }
    elif table_name == 'nptel_courses':
        mapping = {
            'local_course_id': 'id',
            'course_name': 'Course_Name',
            'course_description': """CONCAT(Prof: , SME_Name, Duration: , Duration, Applicable_NPTEL_Domain: , IFNULL(Applicable_NPTEL_Domain, 'NA'))""",
            'university': 'Institute',
            'course_url': 'NPTEL_URL',
            'price': 'Price',
            'course_vendor': '"nptel"'
        }
    elif table_name == 'coursera_courses':
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
        mapping = {}
    
    return mapping

'''
oursera_courses: ['Course_number', 'Course_Name', 'University', 'Difficulty_Level', 'Course_Rating', 'Course_URL', 'Course_Description', 'Skills', 'Price']
course_bucket: ['id', 'local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'price', 'course_vendor']

DELETE FROM coursera_courses WHERE University = 'NA' and Course_number = 29999;
'''


def update_table(actual_query, table_columns, execution=False):
    # Execute actual_query
    actual_query = actual_query.lower()
    print('-------------------------------------------------------------------------')
    print(actual_query)
    print('-------------------------------------------------------------------------')
    if execution:
        mycursor.execute(actual_query)
        mydb.commit()
        print("Actual query executed successfully!")

    # Check if its an insert, delete or update query
    query = actual_query.split(' ')
    table_name = query[2]
    if query[0].lower() == 'insert':
        table_name = query[2]
    elif query[0].lower() == 'delete':
        table_name = query[2]
    elif query[0].lower() == 'update':
        table_name = query[1]
    

    columns = table_columns[table_name]
    # print(f'{table_name}:', columns)
    global_table_name = 'course_bucket'
    global_columns = table_columns[global_table_name]
    # print(f'{global_table_name}:', global_columns)

    # find the mapping between the columns of this table and the global table
    mapped_dic = find_mapping(table_name, columns, global_columns)

    # Create the mapped query
    mapped_query = ''
    if query[0].lower() == 'insert':
        # Insert the record in the db table
        mapped_query += 'INSERT INTO '+global_table_name+' (local_course_id, course_name, course_description, university, course_url, price, course_vendor) VALUES ( '
        values = actual_query.split(' values ')[1].split('(')[1].split(')')[0].split(', ')
        # Explicitly check whether the course_description is also split into multiple columns or not
        
        print(values)
        value_mapping = {}
        for i in range(len(values)):
            value_mapping[columns[i]] = values[i]
        print(value_mapping)

        mapped_query += value_mapping[mapped_dic['local_course_id']]+', '+value_mapping[mapped_dic['course_name']]+', '
        # mapped_query += value_mapping[mapped_dic['course_description']]

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
                        course_descr_temp[i] = value_mapping[course_descr_temp[i]][1:-1]+','
                    else:
                        course_descr_temp[i] = "'NA'"+','

            course_descr_temp[-1] = course_descr_temp[-1][:-1]
            course_descr_temp = ' '.join(course_descr_temp)
            course_descr_temp = "'"+course_descr_temp+"'"
            mapped_query += course_descr_temp+', '
        else:
            # This is a string
            mapped_query += value_mapping[course_descr]+', '
        
        if mapped_dic['university'] == '"NA"':
            mapped_query += mapped_dic['university']+', '
        else:
            mapped_query += value_mapping[mapped_dic['university']]+', '
        
        mapped_query += value_mapping[mapped_dic['course_url']]+', '+value_mapping[mapped_dic['price']]+', '
        mapped_query += mapped_dic['course_vendor']
        mapped_query += ');'
    

    elif query[0].lower() == 'delete':
        # Delete the record from the db table
        mapped_query += 'DELETE FROM '+global_table_name+' WHERE '
        if 'where' in query:
            where_clause = actual_query.split('where ')[1].split(' and ')
            where_clause[-1] = where_clause[-1][:-1]
            for i in range(len(where_clause)):
                if '=' in where_clause[i]:
                    key, value = where_clause[i].split('=')
                    cmp_operator = '='
                elif 'like' in where_clause[i]:
                    key, value = where_clause[i].split('like')
                    cmp_operator = 'like'
                elif '>' in where_clause[i]:
                    key, value = where_clause[i].split('>')
                    cmp_operator = '>'
                elif '<' in where_clause[i]:
                    key, value = where_clause[i].split('<')
                    cmp_operator = '<'
                else:
                    key, value = where_clause[i].split('in')
                    cmp_operator = 'in'

                key = key.strip()
                value = value.strip()
                print(key, value)
                # search mapped_dic.values() for the key
                for k, v in mapped_dic.items():
                    if v == key:
                        key = k
                        break
                # find the value in the value_mapping
                # if value in value_mapping:
                #     value = value_mapping[value]
                # else:
                #     value = "'"+value+"'"
                where_clause[i] = key+' '+cmp_operator+' '+value
            where_clause = ' and '.join(where_clause)
                
            print(where_clause)
        mapped_query += where_clause+' and course_vendor = "'+table_name.split('_')[0]+'";'


    elif query[0].lower() == 'update':
        # Update the record in the db table
        mapped_query += 'UPDATE '+global_table_name+' SET '
    print('-------------------------------------------------------------------------')
    print(mapped_query)
    print('-------------------------------------------------------------------------')
    if execution:
        mycursor.execute(mapped_query)
        mydb.commit()
        print("Mapped query executed successfully!")


# Query for deleting a record from the course_bucket table.
# query = '''DELETE FROM course_bucket WHERE course_id = 29999;'''

# Query for inserting a record into the course_bucket table.
# query = '''INSERT INTO course_bucket (course_id, course_name, course_description, university, course_url, price, course_vendor) VALUES (29999, 'Learn How to Create a WordPress Website', 'Instructor: Darrel Wilson, course duration: 2.5 hours', 'NA', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 80000, 'skillshare');'''

# Query for updating a record in the course_bucket table.
# query = '''UPDATE course_bucket SET price = 89000 WHERE course_id = 29999;'''

def main_menu():
    # Create a main menu with insert, delete, update and exit options. 
    print("Welcome to the main menu!")
    print("1. Insert")
    print("2. Delete")
    print("3. Update")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    while choice != 4:
        if choice == 1:
            # insert
            # query = input("Enter the insert query: ")
            query = '''INSERT INTO skillshare_courses (id, Title, URL, students_count, course_duration, instructor, lessions_count, level, student_projects, engaging, clarity, quality, price) VALUES (29999, 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 0, '2.5 hours', 'Darrel Wilson', 21, 'Beginner', '1', '4.5', '4.5', '4.5', 80000);'''
            update_table(query, table_columns)
        elif choice == 2:
            # delete
            # query = input("Enter the delete query: ")
            query = '''DELETE FROM skillshare_courses WHERE id = 29999;'''
            update_table(query, table_columns)
        elif choice == 3:
            # update
            # query = input("Enter the update query: ")
            query = '''UPDATE skillshare_courses SET price = 89000 WHERE id = 29999;'''
            update_table(query, table_columns)
        else:
            print("Invalid choice!")
        
        print('------------------------------------------')
        print("1. Insert")
        print("2. Delete")
        print("3. Update")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

query = '''
INSERT INTO skillshare_courses 
(id, Title, URL, students_count, course_duration, instructor, lessions_count, level, student_projects, engaging, clarity, quality, price) 
VALUES 
(29999, 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 
0, '2.5 hours', 'Darrel Wilson', 21, 'Beginner', '1', '4.5', '4.5', '4.5', 80000);
'''
main_menu()
# query for inserting into coursera table
# query = '''INSERT INTO coursera_courses (Course_number, Course_Name, University, Difficulty_Level, Course_Rating, Course_URL, Course_Description, Skills, Price) VALUES (29999, 'Learn How to Create a WordPress Website', 'NA', 'Beginner', '4.5', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 'Instructor: Darrel Wilson course duration: 2.5 hours', 'NA', 80000);'''
# query for deleting from skillshare table
# query = '''DELETE FROM skillshare_courses WHERE id = 29999;'''
# update_table(query, table_columns)
# mycursor.execute('''SELECT * FROM course_bucket WHERE local_course_id = 29999 and course_vendor = 'skillshare';''')
# print(mycursor.fetchall())


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
