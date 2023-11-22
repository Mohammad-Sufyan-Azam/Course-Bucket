from distutils.util import execute
# import execute from setuptools.command.install 
# from setuptools.command.install import execute
from importlib_metadata import Prepared
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    username = "root",
    passwd = "Unique@32",
    database = "nptel"
)

my_cursor = mydb.cursor(prepared = True)

def showTables():
    my_cursor.execute("show tables")
    result = my_cursor.fetchall()
    return result
    
# print(showTables())



def handleCourseName(course, myresult):
    course = preprocess_text(course)
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

    return result

def executeQuery(course_name, price, university, platform):
    sql = "select * from course_bucket where "
    if price == 'Free':
        sql += "price = 0 and "
    else:
        sql += "price > 0 and "
    
    if platform != '' and platform != 'na' and platform != 'null':
        platform = platform.split(',')
        # iterate and strip each element
        for i in range(len(platform)):
            platform[i] = platform[i].strip()    
            sql += f"course_vendor = '{platform}' or "
        
    
    if university != '' and university != 'na' and university != 'null':
        sql += f"university = '{university}' and "
    
    sql = sql[:-4]+';'
    my_cursor.execute(sql)
    all_result = my_cursor.fetchall()
    print(all_result)
    
    if course_name == '' or course_name == 'na' or course_name == 'null':
        return all_result
    
    handleCourseName(course_name, all_result)


# course_bucket: ['id', 'local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'price', 'course_vendor']
# my_cursor.execute("select * from course_bucket WHERE course_name LIKE '%machine%';")
# result = my_cursor.fetchall()
# for i in result:
#     print(i)

# renaming coursera_courses able to course_bucket
mydb.commit()
