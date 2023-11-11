import mysql.connector as mysql

mydb = mysql.connect(host="localhost",user="root",password="aA1zZ26")
mycursor = mydb.cursor()
mycursor.execute("USE nptel")


def update_view(query):
    table_name = query[2]
    
    result = []
    
    begin = ''
    view_name = 'course_bucket4'
    query = query.split(' ')
    if query[0].lower() == 'insert':
        # Insert the record in the db table
        data = query.split(' VALUES ')[1]
        begin = 'ALTER view course_bucket4 AS ('
    elif query[0].lower() == 'delete':
        # chANGE THE TABLE NAME FROM QUERY
        delete_query = 'query[0] '+ ' ' + query[1] + ' ' + view_name + ' ' + ' '.join(query[3:])
        print(delete_query)
        mycursor.execute(delete_query)
        mydb.commit()
        return
    elif query[0].lower() == 'update':
        # Update the record in the db table
        begin = 'UPDATE VIEW '
    actual_query = begin + view_name+' (course_id, course_name, course_description, university, course_url, price, course_vendor) VALUES '

    data_ = data.split('(')[1].split(')')[0].split(', ')
    if table_name == 'coursera_courses':
        result = [data_[0], data_[1], data_[6], data_[2], data_[5], data_[8], 'coursera']
    elif table_name == 'skillshare_courses':
        result = [data_[0], data_[1], data_[3], data_[5], data_[4], data_[11], 'skillshare']
    elif table_name == 'udacity_courses':
        result = [data_[0], data_[1], data_[6], data_[3], data_[4], data_[5], 'udacity']
    elif table_name == 'udemy_courses':
        result = [data_[0], data_[1], data_[11], data_[8], data_[4], data_[5], 'udemy']
    elif table_name == 'nptel_courses':
        result = [data_[0], data_[2], data_[3], data_[4], data_[5], data_[20], 'nptel']
    else:
        result = [data_[0], data_[1], data_[2], data_[3], data_[4], data_[5], table_name]
    
    # converting to string
    result = ', '.join(result)
    actual_query += '( '+ result + ' );'
    print(actual_query)
    mycursor.execute(actual_query)
    mydb.commit()

# Write an insert query for inserting into skillshare_courses
query_insert = '''INSERT INTO skillshare_courses (id, Title, URL, students_count, course_duration, instructor, lessions_count, level, student_projects, engaging, clarity, quality, price) VALUES (29999, 'Learn How to Create a WordPress Website', 'https://www.skillshare.com/classes/Learn-How-to-Create-a-WordPress-Website/2126456149?via=browse-rating-wordpress-layout-grid', 0, '2.5 hours', 'Darrel Wilson', 21, 'Beginner', '1', '4.5', '4.5', '4.5', 80000);'''
query_update = '''UPDATE skillshare_courses SET price = 89000 WHERE id = 29999;'''
query_delete = '''DELETE FROM skillshare_courses WHERE id = 29999;'''

print('1. Insert\n2. Update\n3. Delete')
choice = int(input())
if (choice == 1):
    query_insert = input()
    update_view(query_delete)
elif (choice == 2):
    query_update = input()
    update_view(query_delete)
elif (choice == 3):
    query_delete = input()
    update_view(query_delete)