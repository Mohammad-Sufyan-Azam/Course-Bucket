query = 'INSERT INTO table (column1, column2) VALUES (value1, value2);'


def update_view(query):
    query = query.split(' ')
    table_name = query[2]
    data = query.split(' VALUES ')[1]
    
    result = []
    
    begin = ''
    if query[0].lower() == 'insert':
        # Insert the record in the db table
        begin = 'INSERT INTO '
    elif query[0].lower() == 'delete':
        # Delete the record from the db table
        begin = 'DELETE FROM '
    elif query[0].lower() == 'update':
        # Update the record in the db table
        begin = 'UPDATE VIEW '
    actual_query = begin + 'course_bucket4 (course_id, course_name, course_description, university, course_url, price, course_vendor) VALUES '

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


coursera_courses = ['Course_number', 'Course_Name', 'University', 'Difficulty_Level', 'Course_Rating', 'Course_URL', 'Course_Description', 'Skills', 'Price']
skillshare_courses = ['id', 'Title', 'URL', 'students_count', 'course_duration', 'instructor', 'lessons_count', 'level', 'student_projects', 'engaging', 'clarity', 
                      'quality', 'price']
udacity_courses = ['number', 'Name', 'School', 'Difficulty_Level', 'Rating', 'Link', 'About', 'Price']
udemy_courses = ['course_id', 'course_title', 'url', 'is_paid', 'price', 'num_subscribers', 'num_reviews', 'num_lectures', 'level', 'content_duration', 
                 'published_timestamp', 'subject']
nptel_courses = ['id', 'Discipline', 'Course Name', 'SME Name', 'Institute', 'Co-ordinating Institute', 'Duration', 'Type of course', 'Start date', 'End date', 
                 'Exam date', 'Enrollment End date', 'Exam Registration End date', 'UG/PG', 'Core/Elective', 'FDP', 'Applicable NPTEL Domain', 
                 'Click here to join the course', 'Old course URL', 'NPTEL_URL', 'Price']


'''
CREATE VIEW course_bucket4 AS (
    (SELECT 'Course number' as course_id, Course_Name as course_name, 'Course Description' as course_description, University as university, Course_URL as course_url, Price as price, 
    'coursera' AS course_vendor FROM coursera_courses) 
    Union 
    (SELECT (1019 + id) as course_id, "Course Name" as course_name, ("Prof:"+'SME Name'+"Duration:"+Duration) as course_description, Institute as university, NPTEL_URL as course_url, 
    Price as price, 'nptel' AS course_vendor FROM nptel_courses) 
    Union 
    (SELECT (1309 + id) as course_id, Title as course_name, ("Instructor:"+instructor+ " , course duration:"+'course duration') as course_description, "NA" as university, URL as course_url, 
    price, 'skillshare' as course_vendor FROM skillshare_courses) 
    Union 
    (SELECT (1407 + number) as course_id, Name as course_name, About as course_description, School as university, Link as course_url, Price as price, 'udacity' AS course_vendor FROM udacity_courses) 
    Union 
    (SELECT (1475 + course_id) as course_id, course_title as course_name, ("Subject:" + subject+",Number of lecture:"+num_lectures+"content_duration in hours:"+content_duration) as course_description, 
    "NA" as university, url as course_url, price, 'udemy' AS course_vendor FROM udemy_courses) 
    );

'''