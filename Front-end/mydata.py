from distutils.util import execute
from importlib_metadata import Prepared
import mysql.connector as mysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import re
import nltk
from nltk.corpus import stopwords
import random
import pickle


mydb = mysql.connect(
    host = "localhost",
    username = "root",
    passwd = "Unique@32",
    database = "nptel"
)

# course_bucket: ['id', 'local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'course_vendor', 'price']


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


mycursor = mydb.cursor(prepared = True)

def showTables():
    mycursor.execute("show tables")
    result = mycursor.fetchall()
    return result
    
# print(showTables())



def handleCourseName(course, myresult):
    # course_bucket: ['id', 'local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'course_vendor', 'price']

    course = preprocess_text(course)
    result = []
    for x in myresult:
        if compute_similarity(course, (x[2])) > 0:
            result.append([x[2], x[5], x[6], x[7]])
    
    result.sort(key=lambda x: compute_similarity(course, (x[0])), reverse=True)

    # print("The results sorted by relevance are: ")
    # print("s.no.\tCourse\tvendor\turl\tprice")
    # for i in range(len(result)):
    #     print(i+1,".\t",result[i][0],"\t",result[i][2],"\t",result[i][1],"\t",result[i][3],sep="")
    # print()
    # dump results in pkl file
    with open('data.pkl', 'wb') as f:
        pickle.dump(result, f)
    
    print('Done')

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
            print(platform[i])
            platform[i] = platform[i].strip()
            sql += f"course_vendor = '{platform[i]}' or "
        
    
    if university != '' and university != 'na' and university != 'null':
        sql += f"university = '{university}' and "
    
    sql = sql[:-4]+';'
    mycursor.execute(sql)
    all_result = mycursor.fetchall()
    # print(all_result)
    print(sql)
    
    if course_name == '' or course_name == 'na' or course_name == 'null':
        return all_result
    
    query_result = handleCourseName(course_name, all_result)
    return query_result

# executeQuery('python', 'Paid', 'na', 'udemy, udacity, nptel, skillshare')
