import mysql.connector as mysql
import pickle

mydb = mysql.connect(host='localhost', user='root', password='Unique@32')
mycursor = mydb.cursor()
mycursor.execute("USE nptel")

# Global Schema
global_schema = ['local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'price', 'course_vendor']

# Dictionary containing words similar to the column names in the database for matching
column_name_similarity = {
    'id': ['id', 'course_id', 'courseid', 'course_id', 'courseid'],
    'local_course_id': ["code","CODE","Code","course code","Course Code","Course code","Course_Code","CourseCode","courseCode","Course","course","COURSE","ccode","c. code","C. Code","C. code","c_code","cCode","CCode","c_Code","cCode","C_Code","c_Code","c_code","Code","code","CODE","Course Code","Course code","course code","Course_Code","CourseCode","courseCode","courseCode","c_code","C. code","C. Code","C. Code","cCode","cCode","CCode","c_Code","cCode","C_Code","c_Code","c_code","Course_Code","CourseCode","courseCode","Course Code","Course code","course code","Course_Code","CourseCode","courseCode","courseCode","c_code","C. code","C. Code","C. Code","cCode","cCode","CCode","c_Code","cCode","C_Code","c_Code","c_code","Course_Code","CourseCode","courseCode","Course Code","Course code","course code","Course_Code","CourseCode","courseCode","courseCode","c_code","C. code","C. Code","C. Code","cCode","cCode","CCode","c_Code","cCode","C_Code","c_Code","c_code","Course_id","id","ID","course_id","Course_id","course_id","Course_id","Course_id","course_id","course_id","c_id","C. id","C. Id","C. id","cId","cId","CId","c_Id","cId","C_Id","c_Id","c_id","number","Number","NUMBER","Course Number","Course number","course number","Course_Number","CourseNumber","courseNumber","courseNumber","c_number","C. number","C. Number","C. Number","cNumber","cNumber","CNumber","c_Number","cNumber","C_Number","c_Number","c_number","no.","No.","NO.","Course No.","Course no.","course no.","Course_No.","CourseNo.","courseNo.","courseNo.","c_no.","C. no.","C. No.","C. No.","cNo.","cNo.","CNo.","c_No.","cNo.","C_No.","c_No.","c_no.","s.no.","S.no.","S.No.","Course S.No.","Course s.no.","course s.no.","Course_S.No.","CourseS.no.","courseS.no.","courseS.no.","c_s.no.","C. s.no.","C. S.no.","C. S.no.","cS.no.","cS.no.","CS.no.","c_S.no.","cS.no.","C_S.no.","c_S.no.","c_s.no."],
    'course_name': ["name","NAME","Name","course name","Course Name","Course name","Course_Name","CourseName","courseName","Course","course","COURSE","cname","c. name","C. Name","C. name","c_name","cName","CName","c_Name","cName","C_Name","c_Name","c_name","Title","title","TITLE","Course Title","Course title","course title","Course_Title","CourseTitle","courseTitle","courseTitle","c_title","C. title","C. Title","C. Title","cTitle","cTitle","CTitle","c_Title","cTitle","C_Title","c_Title","c_title","Course_Title","CourseTitle","courseTitle","Course Title","Course title","course title","Course_Title","CourseTitle","courseTitle","courseTitle","c_title","C. title","C. Title","C. Title","cTitle","cTitle","CTitle","c_Title","cTitle","C_Title","c_Title","c_title"],
    'course_description': ["Description","description","DESCRIPTION","Course Description","Course description","course description","Course_Description","CourseDescription","courseDescription","courseDescription","c_description","C. description","C. Description","C. Description","cDescription","cDescription","CDescription","c_Description","cDescription","C_Description","c_Description","c_description","about","About","ABOUT","Course About","Course about","course about","Course_About","CourseAbout","courseAbout","courseAbout","c_about","C. about","C. About","C. About","cAbout","cAbout","CAbout","c_About","cAbout","C_About","c_About","c_about","summary","Summary","SUMMARY","Course Summary","Course summary","course summary","Course_Summary","CourseSummary","courseSummary","courseSummary","c_summary","C. summary","C. Summary","C. Summary","cSummary","cSummary","CSummary","c_Summary","cSummary","C_Summary","c_Summary","c_summary","info","Info","INFO","Course Info","Course info","course info","Course_Info","CourseInfo","courseInfo","courseInfo","c_info","C. info","C. Info","C. Info","cInfo","cInfo","CInfo","c_Info","cInfo","C_Info","c_Info","c_info","information","Information","INFORMATION","Course Information","Course information","course information","Course_Information","CourseInformation","courseInformation","courseInformation","c_information","C. information","C. Information","C. Information","cInformation","cInformation","CInformation","c_Information","cInformation","C_Information","c_Information","c_information","desc","Desc","DESC","Coursedesc","Coursedescription","CourseDesc","CourseDescription","coursedescription","coursedesc","goals","Goals","GOALS","Course Goals","Course goals","course goals","Course_Goals","CourseGoals","courseGoals","courseGoals","c_goals","C. goals","C. Goals","C. Goals","cGoals","cGoals","CGoals","c_Goals","cGoals","C_Goals","c_Goals","c_goals","objective","Objective","OBJECTIVE","Course Objective","Course objective","course objective","Course_Objective","CourseObjective","courseObjective","courseObjective","c_objective","C. objective","C. Objective","C. Objective","cObjective","cObjective","CObjective","c_Objective","cObjective","C_Objective","c_Objective","c_objective","aim","Aim","AIM","Course Aim","Course aim","course aim","Course_Aim","CourseAim","courseAim","courseAim","c_aim","C. aim","C. Aim","C. Aim","cAim","cAim","CAim","c_Aim","cAim","C_Aim","c_Aim","c_aim","purpose","Purpose","PURPOSE","Course Purpose","Course purpose","course purpose","Course_Purpose","CoursePurpose","coursePurpose","coursePurpose","c_purpose","C. purpose","C. Purpose","C. Purpose","cPurpose","cPurpose","CPurpose","c_Purpose","cPurpose","C_Purpose","c_Purpose","c_purpose","objective","Objective","OBJECTIVE","Course Objective","Course objective","course objective","Course_Objective","CourseObjective","courseObjective","courseObjective","c_objective","C. objective","C. Objective","C. Objective","cObjective","cObjective","CObjective","c_Objective","cObjective","C_Objective","c_Objective","c_objective","aim","Aim","AIM","Course Aim","Course aim","course aim","Course_Aim","CourseAim","courseAim","courseAim","c_aim","C. aim","C. Aim","C. Aim","cAim","cAim","CAim","c_Aim","cAim","C_Aim","c_Aim","c_aim","purpose","Purpose","PURPOSE","Course Purpose","Course purpose","course purpose","Course_Purpose","CoursePurpose","coursePurpose","coursePurpose","c_purpose","C. purpose","C. Purpose","C. Purpose","cPurpose"],
    'university': ["university","University","UNIVERSITY","Course University","Course university","course university","Course_University","CourseUniversity","courseUniversity","courseUniversity","c_university","C. university","C. University","C. University","cUniversity","cUniversity","CUniversity","c_University","cUniversity","C_University","c_University","c_university","college","College","COLLEGE","Course College","Course college","course college","Course_College","CourseCollege","courseCollege","courseCollege","c_college","C. college","C. College","C. College","cCollege","cCollege","CCollege","c_College","cCollege","C_College","c_College","c_college","institute","Institute","INSTITUTE","Course Institute","Course institute","course institute","Course_Institute","CourseInstitute","courseInstitute","courseInstitute","c_institute","C. institute","C. Institute","C. Institute","cInstitute","cInstitute","CInstitute","c_Institute","cInstitute","C_Institute","c_Institute","c_institute","school","School","SCHOOL","Course School","Course school","course school","Course_School","CourseSchool","courseSchool","courseSchool","c_school","C. school","C. School","C. School","cSchool","cSchool","CSchool","c_School","cSchool","C_School","c_School","c_school"],
    'course_url': ["url","URL","Url","Course Url","Course url","course url","Course_Url","CourseUrl","courseUrl","courseUrl","c_url","C. url","C. Url","C. Url","cUrl","cUrl","CUrl","c_Url","cUrl","C_Url","c_Url","c_url","link","Link","LINK","Course Link","Course link","course link","Course_Link","CourseLink","courseLink","courseLink","c_link","C. link","C. Link","C. Link","cLink","cLink","CLink","c_Link","cLink","C_Link","c_Link","c_link","site","Site","SITE","website","Website","WEBSITE","Course Website","Course website","course website","Course_Website","CourseWebsite","courseWebsite","courseWebsite","c_website","C. website","C. Website","C. Website","cWebsite","cWebsite","CWebsite","c_Website","cWebsite","C_Website","c_Website","c_website","web","Web","WEB","Course Web","Course web","course web","Course_Web","CourseWeb","courseWeb","courseWeb","c_web","C. web","C. Web","C. Web","cWeb","cWeb","CWeb","c_Web","cWeb","C_Web","c_Web","c_web","webpage","Webpage","WEBPAGE","Course Webpage","Course webpage","course webpage","Course_Webpage","CourseWebpage","courseWebpage","courseWebpage","c_webpage","C. webpage","C. Webpage","C. Webpage","cWebpage","cWebpage","CWebpage","c_Webpage","cWebpage","C_Webpage","c_Webpage","c_webpage","web page","Web page","WEB PAGE","Course Web page","Course web page","course web page","Course_Web page","CourseWeb page","courseWeb page","courseWeb page","c_web page","C. web page","C. Web page","C. Web page","cWeb page","cWeb page","CWeb page","c_Web page","cWeb page","C_Web page","c_Web page","c_web page","web-page","Web-page","WEB-PAGE","Course Web-page","Course web-page","course web-page","Course_Web-page","CourseWeb-page","courseWeb-page","courseWeb-page","c_web-page","C. web-page","C. Web-page","C. Web-page","cWeb-page","cWeb-page","CWeb-page","c_Web-page","cWeb-page","C_Web-page","c_Web-page","c_web-page","web_page","Web_page","WEB_PAGE","Course Web_page","Course web_page","course web_page","Course_Web_page","CourseWeb_page","courseWeb_page","courseWeb_page","c_web_page","C. web_page","C. Web_page","C. Web_page","cWeb_page","cWeb_page","CWeb_page","c_Web_page","cWeb_page","C_Web_page","c_Webpage","domain","Domain","DOMAIN","Course Domain","Course domain","course domain","Course_Domain","CourseDomain","courseDomain","courseDomain","c_domain","C. domain","C. Domain","C. Domain","cDomain","cDomain","CDomain","c_Domain","cDomain","C_Domain","c_Domain","c_domain","web-domain","Web-domain","WEB-DOMAIN","Course Web-domain","Course web-domain","course web-domain","Course_Web-domain","CourseWeb-domain","courseWeb-domain","courseWeb-domain","c_web-domain","C. web-domain","C. Web-domain","C. Web-domain","cWeb-domain","cWeb-domain","CWeb-domain","c_Web-domain","cWeb-domain","C_Web-domain","c_Web-domain","c_web-domain","web_domain","Web_domain","WEB_DOMAIN","Course Web_domain","Course web_domain","course web_domain","Course_Web_domain","CourseWeb_domain","courseWeb_domain","courseWeb_domain","c_web_domain","C. web_domain","C. Web_domain","C. Web_domain","cWeb_domain","cWeb_domain","CWeb_domain","c_Web_domain","cWeb_domain","C_Web_domain","c_Web_domain","c_web_domain","web-domain","Web-domain","WEB-DOMAIN","Course Web-domain","Course web-domain","course web-domain","Course_Web-domain","CourseWeb-domain","courseWeb-domain","courseWeb-domain","c_web-domain","C. web-domain","C. Web-domain","C. Web-domain","cWeb-domain","cWeb-domain","CWeb-domain","c_Web-domain","cWeb-domain","C_Web-domain","c_Web-domain","c_web-domain","web_domain","Web_domain","WEB_DOMAIN","Course Web_domain","Course web_domain","course web_domain","Course_Web_domain","CourseWeb_domain","courseWeb_domain","courseWeb_domain","c_web_domain","C. web_domain","C. Web_domain","C. Web_domain","cWeb_domain","cWeb_domain","CWeb_domain","c_Web_domain","cWeb_domain","C_Web_domain","c_Web_domain","c_web_domain","web-domain","Web-domain","WEB-DOMAIN","Course Web-domain","Course web-domain","course web-domain","Course_Web-domain","CourseWeb-domain","courseWeb-domain","courseWeb-domain","c_web-domain","C. web-domain","C. Web-domain","C. Web-domain"],
    'price': ["price","Price","PRICE","Course Price","Course price","course price","Course_Price","CoursePrice","coursePrice","coursePrice","c_price","C. price","C. Price","C. Price","cPrice","cPrice","CPrice","c_Price","cPrice","C_Price","c_Price","c_price","cost","Cost","COST","Course Cost","Course cost","course cost","Course_Cost","CourseCost","courseCost","courseCost","c_cost","C. cost","C. Cost","C. Cost","cCost","cCost","CCost","c_Cost","cCost","C_Cost","c_Cost","c_cost","fee","Fee","FEE","Course Fee","Course fee","course fee","Course_Fee","CourseFee","courseFee","courseFee","c_fee","C. fee","C. Fee","C. Fee","cFee","cFee","CFee","c_Fee","cFee","C_Fee","c_Fee","c_fee","fees","Fees","FEES","Course Fees","Course fees","course fees","Course_Fees","CourseFees","courseFees","courseFees","c_fees","C. fees","C. Fees","C. Fees","cFees","cFees","CFees","c_Fees","cFees","C_Fees","c_Fees","c_fees","tuition","Tuition","TUITION","Course Tuition","Course tuition","course tuition","Course_Tuition","CourseTuition","courseTuition","courseTuition","c_tuition","C. tuition","C. Tuition","C. Tuition","cTuition","cTuition","CTuition","c_Tuition","cTuition","C_Tuition","c_Tuition","c_tuition","charge","Charge","CHARGE","Course Charge","Course charge","course charge","Course_Charge","CourseCharge","courseCharge","courseCharge","c_charge","C. charge","C. Charge","C. Charge","cCharge","cCharge","CCharge","c_Charge","cCharge","C_Charge","c_Charge","c_charge","amount","Amount","AMOUNT","Course Amount","Course amount","course amount","Course_Amount","CourseAmount","courseAmount","courseAmount","c_amount","C. amount","C. Amount","C. Amount","cAmount","cAmount","CAmount","c_Amount","money","Money","MONEY","Course Money","Course money","course money","Course_Money","CourseMoney","courseMoney","courseMoney","c_money","C. money","C. Money","C. Money","cMoney","cMoney","CMoney","c_Money","cMoney","C_Money","c_Money","c_money","total","Total","TOTAL","Course Total","Course total","course total","Course_Total","CourseTotal","courseTotal","courseTotal","c_total","C. total","C. Total","C. Total","cTotal","cTotal","CTotal","c_Total","cTotal","C_Total","c_Total","c_total","sum","Sum","SUM","Course Sum","Course sum","course sum","Course_Sum","CourseSum","courseSum","courseSum","c_sum","C. sum","C. Sum","C. Sum","cSum","cSum","CSum","c_Sum","cSum","C_Sum","c_Sum","c_sum","total amount","Total amount","TOTAL AMOUNT","Course Total amount","Course total amount","course total amount","Course_Total amount","CourseTotal amount","courseTotal amount","courseTotal amount","c_total amount","C. total amount","C. Total amount","C. Total amount","cTotal amount","cTotal amount","CTotal amount","c_Total amount","cTotal amount","C_Total amount","c_Total amount","c_total amount","sum amount","Sum amount","SUM AMOUNT","Course Sum amount","Course sum amount","course sum amount","Course_Sum amount","CourseSum amount","courseSum amount","courseSum amount","c_sum amount","C. sum amount","C. Sum amount","C. Sum amount","cSum amount","cSum amount","CSum amount","c_Sum amount","cSum amount","C_Sum amount","c_Sum amount","c_sum amount","total cost","Total cost","TOTAL COST","Course Total cost","Course total cost","course total cost","Course_Total cost","CourseTotal cost","courseTotal cost","courseTotal cost","c_total cost","C. total cost","C. Total cost","C. Total cost","cTotal cost","cTotal cost","CTotal cost","c_Total cost","cTotal cost","C_Total cost","c_Total cost","c_total cost","sum cost","Sum cost","SUM COST","Course Sum cost","Course sum cost","course sum cost","Course_Sum"],
    'course_vendor': ['course_vendor', 'coursevendor', 'course_vendor', 'coursevendor']
}

# MetaData contains the online course vendors and the mapping of their column names to the column names in the database
mapping_metadata = {}
global_vendors = []

def find_similar_col(column_name, column_name_similarity):
    for key in column_name_similarity:
        if column_name in column_name_similarity[key]:
            return key
    return None

# Function to add a new vendor to the metadata
def add_vendor_schema(vendor_name, vendor_schema):
    # Get the schema of the vendor from pickle file
    with open('metadata_mapping.pkl', 'rb') as f:
        mapping_metadata = pickle.load(f)
    cols_present = []
    course_desc_cols = []
    mapping_metadata[vendor_name] = {}
    for col_name in vendor_schema:
        # Finding the similarity of the column name with the column names in the database
        sim_global_col_name = find_similar_col(col_name, column_name_similarity)
        if sim_global_col_name is not None:
            mapping_metadata[vendor_name][sim_global_col_name] = col_name
            cols_present.append(sim_global_col_name)
        else:
            course_desc_cols.append(col_name)

    # Adding the left out columns to description in this format: CONCAT(Prof: , SME_Name, Duration: , Duration, Applicable_NPTEL_Domain: , IFNULL(Applicable_NPTEL_Domain, 'NA'))
    if mapping_metadata[vendor_name].get('course_description') is None:
        mapping_metadata[vendor_name]['course_description'] = "CONCAT(" + ", ".join(course_desc_cols) + ")"
    
    mapping_metadata[vendor_name]['course_vendor'] = '"'+vendor_name + '"'

    # Update the metadata in a pickle file
    with open('metadata_mapping.pkl', 'wb') as f:
        pickle.dump(mapping_metadata, f, pickle.HIGHEST_PROTOCOL)

    return mapping_metadata[vendor_name]

# Function to read records either as input or from a csv file
def read_records(vendor_name):
    choice = int(input("Enter 1 to enter records manually, 2 to read from a csv file: "))
    if choice == 1:
        records = []
        while True:
            record = {}
            for col_name in mapping_metadata[vendor_name]:
                record[col_name] = input("Enter the value for " + col_name + ": ")
            records.append(record)
            choice = input("Enter 1 to add another record, 2 to stop: ")
            if choice == 2:
                break
        return records
    else:
        records = []
        col_names = []
        csv_file = input("Enter the path of the csv file: ")
        # The first line of the csv file contains the column names of the local vendor
        with open(csv_file, 'r') as f:
            col_names = f.readline()[:-1].split(',')
            for i in range(len(col_names)):
                col_names[i] = col_names[i].strip()
            for line in f:
                # If \n is present at the end of the line, then remove it
                if line[-1] == '\n':
                    line = line[:-1]
                record = {}
                values = line.split(',')
                for i in range(len(col_names)):
                    record[col_names[i]] = values[i]
                records.append(record)
            # Closing the file
            f.close()

        # print("The records are: ")
        # print(records)

        return records, col_names

def generate_local_schema(vendor_name, col_names):
    print("The column names are: ")
    print(col_names)
    print("Enter the type of data for each column: ")
    print("For example, if the column is of type VARCHAR(255), enter VARCHAR(255)")
    choice = input("Enter 1 to enter the type of data manually, 2 to enter the type of data from a file: ")
    if choice == 1:
        local_vendor_schema = {}
        for col_name in col_names:
            local_vendor_schema[col_name] = input("Enter the type of data for " + col_name + ": ")
        return local_vendor_schema
    else:
        local_vendor_schema = {}
        schema_file = input("Enter the path of the schema file: ")
        # The file format is: col_name, data_type
        with open(schema_file, 'r') as f:
            for line in f:
                # Remove \n from the end of the line
                line = line[:-1]
                values = line.split(',')
                local_vendor_schema[values[0]] = values[1]
            # Closing the file
            f.close()
        return local_vendor_schema

def add_local_source(vendor_name):
    # Read records and schema from the csv file
    records, col_names = read_records(vendor_name)

    # Add this schema to the metadata
    vendor_schema = add_vendor_schema(vendor_name, col_names)

    # Now writing a query to create a table for the vendor and add the records to the table
    local_schema = generate_local_schema(vendor_name, col_names)

    # print('The local schema is: ')
    # print(local_schema)

    # Now writing a query to create a table for the vendor and add the records to the table
    query = "CREATE TABLE " + vendor_name + " ("
    for col_name in local_schema:
        query += col_name + " " + local_schema[col_name] + ", "
    query = query[:-2]
    query += ")"
    print('Query is: ')
    print(query)
    mycursor.execute(query)
    mydb.commit()
    print('Table created!')

    records_tuple = []
    for record in records:
        record_tuple = []
        for col_name in col_names:
            record_tuple.append(record[col_name])
        records_tuple.append(tuple(record_tuple))
    
    print('The records are: ')
    print(records_tuple[0:5])

    # Now writing a query to add the records to local table created
    query = "INSERT INTO " + vendor_name + " (" + ", ".join(col_names) + ") VALUES ("
    for record in records_tuple:
        for value in record:
            query += value + ", "
        query = query[:-2]
        query += "), ("
    query = query[:-3]
    print('Query is: ')
    print(query)

    mycursor.execute(query)
    mydb.commit()      
    
    # Local vendor is created now

def delete_local_source(vendor_name):
    # Now writing a query to delete the table for the vendor
    query = "DROP TABLE " + vendor_name
    mycursor.execute(query)
    mydb.commit()
    
    delete_vendor_schema(vendor_name)

def delete_vendor_schema(vendor_name):
    # Get the schema of the vendor from pickle file
    with open('metadata_mapping.pkl', 'rb') as f:
        mapping_metadata = pickle.load(f)

    # Check if the vendor is present in the metadata
    # If present, then delete the vendor from the metadata
    # Else, print that the vendor is not present
    if vendor_name not in mapping_metadata:
        print("Vendor not present!")
        return

    del mapping_metadata[vendor_name]

    # Update the metadata in a pickle file
    with open('metadata_mapping.pkl', 'wb') as f:
        pickle.dump(mapping_metadata, f, pickle.HIGHEST_PROTOCOL)

def get_vendor_schema(vendor_name):
    return mapping_metadata[vendor_name]

def get_vendor_list():
    return list(mapping_metadata.keys())

def get_global_schema():
    return global_schema

def __add_vendor_to_warehouse(vendor_name):
    # Get the schema of the vendor from pickle file
    with open('metadata_mapping.pkl', 'rb') as f:
        mapping_metadata = pickle.load(f)

    # Get the schema of the vendor
    vendor_schema = mapping_metadata[vendor_name]

    # Now writing a query to add the records from the vendor to the warehouse, using the vendor_schema
    query = "INSERT INTO course_bucket (" +(", ").join(global_schema) + ") SELECT "
    for col_name in global_schema:
        if col_name in vendor_schema:
            query += vendor_schema[col_name] + ", "
        else:
            query += "NULL, "
    query = query[:-2]
    query += " FROM " + vendor_name

    # Executing the query
    print('----------------------------------------------------------------------')
    print(query)
    mycursor.execute(query)
    mydb.commit()

def __delete_vendor_from_warehouse(vendor_name):
    # Now writing a query to add the records from the vendor to the warehouse, using the vendor_schema
    query = "DELETE FROM course_bucket WHERE course_vendor = '" + vendor_name + "'"

    # Executing the query
    mycursor.execute(query)
    mydb.commit()

# Defining a refresh function to repopulate the global schema
def refresh_CourseBucket():
    # Checking the difference in global_vendors and mapping_metadata. If there is a difference, then update the global schema

    # Load the mapping_metadata from the pickle file
    with open('metadata_mapping.pkl', 'rb') as f:
        mapping_metadata = pickle.load(f)

    # Get the list of vendors from the database
    mycursor.execute("SELECT DISTINCT course_vendor FROM course_bucket")
    vendors = mycursor.fetchall()
    vendors = [vendor[0] for vendor in vendors]

    # Get the list of vendors from the metadata
    metadata_vendors = list(mapping_metadata.keys())

    # Get the difference between the two lists
    del_diff = list(set(vendors) - set(metadata_vendors))
    add_diff = list(set(metadata_vendors) - set(vendors))

    # If there is a difference, then update the global schema
    if len(del_diff) > 0:
        for vendor_name in del_diff:
            __delete_vendor_from_warehouse(vendor_name)
    if len(add_diff) > 0:
        for vendor_name in add_diff:
            __add_vendor_to_warehouse(vendor_name)

    # Update the global schema
    global_schema = get_global_schema()


# Main menu for the local vendors
def main_menu():
    print("1. Add a new vendor")
    print("2. Delete a vendor")
    print("3. View the list of vendors")
    print("4. View the schema mapping of a vendor")
    print("5. View the global schema")
    print("6. Exit")
    choice = int(input("Enter your choice: "))

    global mapping_metadata
    # Read the metadata_mapping and store as a global variable
    with open('metadata_mapping.pkl', 'rb') as f:
        mapping_metadata = pickle.load(f)

    if choice == 1:
        vendor_name = input("Enter the name of the vendor: ")
        add_local_source(vendor_name)
        print("Vendor added successfully!")
        refresh_CourseBucket()
        
    elif choice == 2:
        vendor_name = input("Enter the name of the vendor: ")
        delete_local_source(vendor_name)
        print("Vendor deleted successfully!")
        refresh_CourseBucket()
    elif choice == 3:
        print("The list of vendors are: ")
        print(get_vendor_list())
    elif choice == 4:
        vendor_name = input("Enter the name of the vendor: ")
        print("The schema of the vendor is: ")
        print(get_vendor_schema(vendor_name))
    elif choice == 5:
        print("The global schema is: ")
        print(get_global_schema())
    else:
        exit()


if __name__ == '__main__':
    main_menu()