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

# Get the total number of columns in each table
for table in tables:
    mycursor.execute("SELECT COUNT(*) FROM "+table)
    count = mycursor.fetchall()
    count = count[0][0]
    print(f"{table}:", count)
    

'''
CREATE VIEW course_bucket4 AS (
    (SELECT Course_number as course_id, Course_Name as course_name, Course_Description as course_description, University as university, 
     Course_URL as course_url, Price as price, 'coursera' AS course_vendor FROM coursera_courses) 
    Union 
    (SELECT (3440 + id) as course_id, Course_Name as course_name, CONCAT('Prof: ', SME_Name, ', Duration: ', Duration, ", Applicable_NPTEL_Domain: ", IFNULL(Applicable_NPTEL_Domain, 'NA')) as course_description, Institute as university, NPTEL_URL as course_url, 
     Price as price, 'nptel' AS course_vendor FROM nptel_courses)
    Union 
    (SELECT (3730 + id) as course_id, Title as course_name, CONCAT("Instructor: ", instructor, ", course duration: ", course_duration) as course_description, "NA" as university, URL as course_url, 
     price, 'skillshare' as course_vendor FROM skillshare_courses) 
    Union 
    (SELECT (3828 + number) as course_id, Name as course_name, About as course_description, School as university, Link as course_url, 
     Price as price, 'udacity' AS course_vendor FROM udacity_courses) 
    Union 
    (SELECT (3883 + course_id) as course_id, course_title as course_name, CONCAT("Subject: ", subject, ", Number of lecture: ", num_lectures, ", content duration in hours: ", content_duration, ", Course Level: ", level) as course_description, 
     "NA" as university, url as course_url, price, 'udemy' AS course_vendor FROM udemy_courses) 
    );
'''

# Create a table called course_bucket5 that stores the content of the view course_bucket4
# mycursor.execute("CREATE TABLE course_bucket5 AS SELECT * FROM course_bucket4")
# Drop the table course_bucket5
# mycursor.execute("DROP TABLE course_bucket5")

# table names-
# coursera_courses
# skillshare_courses
# udacity_courses
# udemy_courses
# nptel_courses
### course_bucket


def find_mapping(table_name, columns, global_columns):
    # course_bucket:      ['course_id', 'course_name', 'course_description', 'university', 'course_url', 'course_vendor', 'price']
    # skillshare_courses: ['id', 'Title', 'URL', 'students_count', 'course_duration', 'instructor', 'lessions_count', 'level', 'student_projects', 'engaging', 'clarity', 'quality', 'price']

    # Find coloumns that match based on some similarity in both the tables
    # For example, course_id and id are similar
    # Ontology based matching
    if table_name == 'skillshare_courses':
        mapping = {
            'course_id': 'id',
            'course_name': 'Title',
            'course_description': 'course_duration'+', '+ 'instructor',
            'university': 'NA',
            'course_url': 'URL',
            'course_vendor': 'skillshare',
            'price': 'price'
        }
        new_query = 'INSERT INTO course_bucket (course_id, course_name, course_description, university, course_url, course_vendor, price) VALUES '
        new_query += '('
    
    # NLP based matching
    
'''
(SELECT id as course_id, Title as course_name,
 ("Instructor:"+instructor+ " , course duration:"+'course duration') as course_description, 
 "NA" as university, URL as course_url, 
    price, 'skillshare' as course_vendor FROM skillshare_courses)
    

'''



def update_table(query, table_columns):
    # Check if its an insert, delete or update query
    query = query.split(' ')
    table_name = query[2]
    if query[0].lower() == 'insert':
        table_name = query[2]
    elif query[0].lower() == 'delete':
        table_name = query[2]
    elif query[0].lower() == 'update':
        table_name = query[1]
    
    # find_schema_mapping between this table and the global table course_bucket

    # find the columns of this table
    columns = table_columns[table_name]
    print(columns)
    # find the columns of the global table
    global_columns = table_columns['course_bucket']
    print(global_columns)

    # find the mapping between the columns of this table and the global table
    mapping = find_mapping(table_name, columns, global_columns)


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

# main_menu()
query = '''INSERT INTO skillshare_courses (id, Title, URL, students_count, course_duration, instructor, lessions_count, level, student_projects, engaging, clarity, quality, price) VALUES (29999, 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 0, '2.5 hours', 'Darrel Wilson', 21, 'Beginner', '1', '4.5', '4.5', '4.5', 80000);'''
# update_table(query, table_columns)

# Write an insert query for inserting into skillshare_courses
# query_insert = '''INSERT INTO skillshare_courses (id, Title, URL, students_count, course_duration, instructor, lessions_count, level, student_projects, engaging, clarity, quality, price) VALUES (29999, 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 0, '2.5 hours', 'Darrel Wilson', 21, 'Beginner', '1', '4.5', '4.5', '4.5', 80000);'''
# query_update = '''UPDATE skillshare_courses SET price = 89000 WHERE id = 29999;'''
# query_delete = '''DELETE FROM skillshare_courses WHERE id = 29999;'''
'''
['course_bucket', 'coursera_courses', 'nptel_courses', 'skillshare_courses', 'udacity_courses', 'udemy_courses']
course_bucket:      ['course_id', 'course_name', 'course_description', 'university', 'course_url', 'course_vendor', 'price']

coursera_courses:   ['Course_number', 'Course_Name', 'University', 'Difficulty_Level', 'Course_Rating', 'Course_URL', 'Course_Description', 'Skills', 'Price']
nptel_courses:      ['id', 'Discipline', 'Course_Name', 'SME_Name', 'Institute', 'Co-ordinating_Institute', 'Duration', 'Type_of_course', 'Start_date', 'End_date', 'Exam_date', 'Enrollment_End_date', 'Exam_Registration_End_date', 'UG/PG', 'Core/Elective', 'FDP', 'Applicable_NPTEL_Domain', 'Click_here_to_join_the_course', 'Old_course_URL', 'NPTEL_URL', 'Price']
skillshare_courses: ['id', 'Title', 'URL', 'students_count', 'course_duration', 'instructor', 'lessions_count', 'level', 'student_projects', 'engaging', 'clarity', 'quality', 'price']
udacity_courses:    ['number', 'Name', 'School', 'Difficulty_Level', 'Rating', 'Link', 'About', 'Price']
udemy_courses:      ['course_id', 'course_title', 'url', 'is_paid', 'price', 'num_subscribers', 'num_reviews', 'num_lectures', 'level', 'content_duration', 'published_timestamp', 'subject']
'''


# Writing a query for creating a global view of all the courses excluding the course_bucket table

# CREATE VIEW course_bucket4 AS ( 
#     (SELECT 'Course_number' as course_id, Course_Name as course_name, 'Course_Description' as course_description, University as university, Course_URL as course_url, 
#       Price as price, 'coursera' AS course_vendor FROM coursera_courses)
#     Union
#     (SELECT (1019 + id) as course_id, "Course Name" as course_name, ("Prof:"+'SME Name'+"Duration:"+Duration) as course_description, Institute as university, 
#       NPTEL_URL as course_url, Price as price, 'nptel' AS course_vendor FROM nptel_courses)
#     Union
#     (SELECT (1309 + id) as course_id, Title as course_name, ("Instructor:"+instructor+ " , course duration:"+'course duration') as course_description, "NA" as university, 
#       URL as course_url, price, 'skillshare' as course_vendor FROM skillshare_courses)
#     Union
#     (SELECT (1509 + number) as course_id, Name as course_name, About as course_description, School as university, Link as course_url, Price as price, 
#       'udacity' as course_vendor FROM udacity_courses)
#     Union
#     (SELECT (1709 + course_id) as course_id, course_title as course_name, content_duration as course_description, subject as university, url as course_url, price, 
#       'udemy' as course_vendor FROM udemy_courses)
# );
