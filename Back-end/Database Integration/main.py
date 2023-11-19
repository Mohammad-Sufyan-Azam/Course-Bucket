import mysql.connector as mysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import re
import nltk
from nltk.corpus import stopwords
import random

# function to preprocess the query
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = "".join([char for char in text if char not in string.punctuation])
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

#function to rank the courses based on the similarity between the query and the course name
def compute_similarity(query, string, weight=0.5):
    
    vectorizer = TfidfVectorizer().fit_transform([string, query])
    vector_similarity = vectorizer * vectorizer.T
    cosine_sim = cosine_similarity(vectorizer)
    combined_similarity = weight * vector_similarity.toarray()[0][1] + (1 - weight) * cosine_sim[0][1]
    return combined_similarity

mydb = mysql.connect(host='localhost', user='root', password='Unique@32')
mycursor = mydb.cursor()
mycursor.execute("USE nptel")

# Global columns: course_id	course_name	course_description	university	course_url	course_vendor	price
global_cols = ['course_id', 'course_name', 'description', 'university', 'course_url', 'price']
data_types = ['int', 'varchar(255) not null', 'varchar(1024)', 'varchar(255)', 'varchar(255)', 'int']

existing_view_query = '''(SELECT Course_number as course_id, Course_Name as course_name, CourseDescription as course_description, University as university, Course_URL as course_url, Price as price, 'coursera' AS course_vendor FROM coursera_courses) Union (SELECT (1019 + id) as course_id, Course_Name as course_name, ("Prof:"+'SME Name'+"Duration:"+Duration) as course_description, Institute as university, NPTEL_URL as course_url, Price as price, 'nptel' AS course_vendor FROM nptel_courses) Union (SELECT (1309 + id) as course_id, Title as course_name, ("Instructor:"+instructor+ " , course duration:"+'course duration') as course_description, "NA" as university, URL as course_url, price, 'skillshare' as course_vendor FROM skillshare_courses) Union (SELECT (1407 + number) as course_id, Name as course_name, About as course_description, School as university, Link as course_url, Price as price, 'udacity' AS course_vendor FROM udacity_courses) Union (SELECT (1475 + course_id) as course_id, course_title as course_name, ("Subject:" + subject+",Number of lecture:"+num_lectures+"content_duration in hours:"+content_duration) as course_description, "NA" as university, url as course_url, price, 'udemy' AS course_vendor FROM udemy_courses)''' 
source_names = ['coursera_courses', 'nptel_courses', 'skillshare_courses', 'udacity_courses', 'udemy_courses']


def insert_source(source, col_names, source_name):
    # source is a list of tuples to be inserted as a new source in the database. Source has multiple tuples which store the course information.
    # col_names is a list of column names in the new source.
    # Now match the columns from the source with the columns in the database, and insert the source in the database.

    # First, check if the columns in the source match with the columns in the database
    # If yes, then continue
    # If no, then return an error message
    global global_cols
    global existing_view_query
    if 'course_id' not in col_names:
        return "Error: Column course_id not found in the source."

    # cols_merged = []

    # for g_col in global_cols:
    #     if g_col in col_names:
    #         cols_merged.append(g_col)
    #         col_names.remove(g_col)
    
    # Update the source list of tuples by adding source_vendor at the end of each tuple in list
    for i in range(len(source)):
        source[i] = source[i] + (source_name,)
    
    source_names.append(source_name)

    # SQL Query to update the original global table, and insert these values.
    # update_view = "ALTER VIEW course_bucket4 ("
    # for i in global_cols:
    #     update_view += i + ", "
    #     print(i)
    # update_view = update_view[:-2] + ") AS (" + existing_view_query + " UNION SELECT "
    
    
        

    # for col in global_cols:
    #         update_view += col + ", "

    # update_view += "course_vendor) VALUES ("
    # for col in range(6):
    #     update_view += "%s, "
    # update_view += "%s);"
    # print('-------------------------------------------------')
    # print(update_view)
    
    create_view = "(SELECT " 
    for i in global_cols:
        create_view += i + ", "
        
    create_view += " '" + str(source_name) + "' AS course_vendor FROM new_data_source) UNION "
    create_view += existing_view_query
    create_view += ";" 

    existing_view_query = create_view

    create_view = 'ALTER VIEW course_bucket5 AS '+ create_view
        
    
    
    
    print(create_view)
    
    mycursor.execute(create_view)
    
    mydb.commit()


def delete_source(source_name):
    # source_name is the name of the source to be deleted from the database.
    # First, check if the source_name exists in the database.
    # If yes, then continue
    # If no, then return an error message
    # SQL Query to delete the source from the database
    # delete_view = "ALTER VIEW course_bucket4 AS (" + existing_view_query + " WHERE course_vendor != '" + source_name + "');"
    # mycursor.execute(delete_view)
    # mydb.commit()
    global existing_view_query
    global source_names
    

    mycursor.execute("SHOW TABLES;")
    source_names = [name[0] for name in mycursor.fetchall()]

    if source_name not in source_names:
        return "Error: Source " + source_name + " not found in the database."
    else:
        # Run exoisting_view_query and get the query
        # delete_query = "ALTER VIEW course_bucket5 AS " + existing_view_query + ";"
        # mycursor.execute(delete_query)
        # mycursor.execute("DROP TABLE " + source_del + ";")
        # mydb.commit()
        
        source_names.remove(source_name)
        # Update existing view query, by removing the selected source from the query
        # find the index of the source_name in existing_view_query
        index = existing_view_query.find(source_name)
        
        # find the index of the previous UNION, if not found else 0
        index_union = existing_view_query[:index].rfind('UNION')

        if index_union == -1:
            index_union = 0

        print(index_union)
        print(index)
        print(existing_view_query[:index_union])
        print(existing_view_query[index + len(source_name) + 1:])
        print(existing_view_query)
        # Now removing the from UNION to the next UNION
        existing_view_query = existing_view_query[:index_union] + existing_view_query[index + len(source_name) + 1:]
        
        ind_ = existing_view_query.find('UNION')

        # Now, update the view
        update_view = "ALTER VIEW course_bucket4 AS (" + existing_view_query + ";"
        # print(update_view)
        mycursor.execute(update_view)
        
        # Drop the table from the database
        mycursor.execute("DROP TABLE " + source_del + ";")

        mydb.commit()
    
def create_table(source, col_names, source_name):
    # Create a new table in the database with the name source_name
    sql_query = "CREATE TABLE " + source_name + " ("
    for i in range(len(col_names)):
        sql_query += col_names[i] + " " + data_types[i] + ", "
    sql_query = "PRIMARY KEY (course_id));"
    mycursor.execute(sql_query)

    # Now, insert the source in the database

    insert_query = "INSERT INTO " + source_name + " ("
    for col in col_names:
        insert_query += col + ", "
    insert_query = insert_query[:-2] + ") VALUES ("
    for i in range(len(col_names)):
        insert_query += "%s, "
    insert_query = insert_query[:-2] + ");"

    mycursor.executemany(insert_query, source)

    mydb.commit()
    
    



choice=0
while choice!=5:
    print("1. Search for a course")
    print("2. View all courses")
    print("3. Adding a new data source")
    print("4. Delete a data source")
    print("5. Exit")
    choice=int(input("Enter your choice: "))
    if choice==1:
        query=input("Enter the query: ")
        query=preprocess_text(query)
        mycursor.execute("SELECT * FROM course_bucket4")
        myresult = mycursor.fetchall()
        result=[]
        for x in myresult:
            if compute_similarity(query,(x[1]))>0:
                result.append([x[1],x[4],x[5],x[6]])
        result.sort(key=lambda x: compute_similarity(query,(x[0])), reverse=True)
        print("The results sorted by relevance are: ")   
        print("s.no.\tCourse\tvendor\turl\tprice")     
        for i in range(len(result)):
            print(i+1,".\t",result[i][0],"\t",result[i][2],"\t",result[i][1],"\t",result[i][3],sep="")
        print()
    elif choice==2:
        mycursor.execute("SELECT * FROM course")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x[1])
        print()
    elif choice==3:
        mycursor.execute("SELECT * FROM new_data_source;")
        myresult = mycursor.fetchall()
        # print(myresult)
        insert_source(myresult, global_cols, "new_data_source")
    elif choice==4:
        source_del = input("Enter the name of the source to be deleted: ")
        delete_source(source_del)
        print("Successfully deleted the source " + source_del + " from the database.")
        
        
    elif choice==5:
        print("Thank you for using the course bucket!")
        print()
    else:
        print("Invalid choice!")
        print()




'''
TODO:
Total tasks that needs to be present - 
1. Course searching based on jaccard, levelnshetin, cosine similarity
    a. NLP techniques can be used to improve the search     --> Extra
2. Adding a new data source     --> Aamleen
3. Deleting a data source       --> Aamleen
4. Adding some rows to a data source        --> Sufyan
5. Deleting some rows from a data source    --> Sufyan
6. Updating some rows in a data source      --> Sufyan
'''