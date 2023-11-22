# import mysql.connector as mysql

# mydb = mysql.connect(host='localhost', user='root', password='Unique@32')
# mycursor = mydb.cursor()
# mycursor.execute("USE nptel")

# # Global Schema
# global_schema = ['id', 'local_course_id', 'course_name', 'course_description', 'university', 'course_url', 'price', 'course_vendor']

# # Dictionary containing words similar to the column names in the database for matching
# column_name_similarity = {
#     'id': ['id', 'course_id', 'courseid', 'course_id', 'courseid'],
#     'local_course_id': ['local_cou']
# }

# # MetaData contains the online course vendors and the mapping of their column names to the column names in the database
# mapping_metadata = {}
# global_vendors = []

def find_similar_col(column_name, column_name_similarity):
    for key in column_name_similarity:
        if column_name in column_name_similarity[key]:
            return key
    return None

# Function to add a new vendor to the metadata
def add_vendor_schema(vendor_name, vendor_schema):
    # Get the schema of the vendor from pickle file
    with open('metadata_mapping.pickle', 'rb') as f:
        mapping_metadata = pickle.load(f)
    cols_present = []
    course_desc_cols = []
    for col_name in vendor_schema:
        # Finding the similarity of the column name with the column names in the database
        sim_global_col_name = find_similar_col(col_name, column_name_similarity)
        if sim_global_col_name is not None:
            mapping_metadata[vendor_name][sim_global_col_name] = col_name
            cols_present.append(sim_global_col_name)
        else:
            course_desc_cols.append(col_name)

    # Adding the left out columns to description in this format: CONCAT(Prof: , SME_Name, Duration: , Duration, Applicable_NPTEL_Domain: , IFNULL(Applicable_NPTEL_Domain, 'NA'))
    if mapping_metadata[vendor_name]['course_description'] is None:
        mapping_metadata[vendor_name]['course_description'] = "CONCAT(" + ", ".join(course_desc_cols) + ")"
    
    mapping_metadata[vendor_name]['course_vendor'] = '"'+vendor_name + '"'

    # Update the metadata in a pickle file
    with open('metadata_mapping.pickle', 'wb') as f:
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
            for line in f:
                # Remove \n from the end of the line
                line = line[:-1]
                record = {}
                values = line.split(',')
                for i in range(len(col_names)):
                    record[col_names[i]] = values[i]
                records.append(record)
            # Closing the file
            f.close()

        print("The records are: ")
        print(records)

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

def add_local_source(vendor_name, records):
    # Read records and schema from the csv file
    records, col_name = read_records(vendor_name)

    # Add this schema to the metadata
    vendor_schema = add_vendor_schema(vendor_name, local_vendor_schema)

    # Now writing a query to create a table for the vendor and add the records to the table
    local_schema = generate_local_schema(vendor_name, col_names)

    # Now writing a query to create a table for the vendor and add the records to the table
    query = "CREATE TABLE " + vendor_name + " ("
    for col_name in local_schema:
        query += col_name + " " + local_schema[col_name] + ", "
    query = query[:-2]
    query += ")"
    mycursor.execute(query)
    mydb.commit()

    # Now writing a query to add the records to local table created
    query = "INSERT INTO " + vendor_name + " (" + ", ".join(col_names) + ") VALUES ("
    for col_name in col_names:
        query += "%s, "
    query = query[:-2]
    query += ")"
    mycursor.executemany(query, records)
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
    with open('metadata_mapping.pickle', 'rb') as f:
        mapping_metadata = pickle.load(f)

    # Check if the vendor is present in the metadata
    # If present, then delete the vendor from the metadata
    # Else, print that the vendor is not present
    if vendor_name not in mapping_metadata:
        print("Vendor not present!")
        return

    del mapping_metadata[vendor_name]

    # Update the metadata in a pickle file
    with open('metadata_mapping.pickle', 'wb') as f:
        pickle.dump(mapping_metadata, f, pickle.HIGHEST_PROTOCOL)

def get_vendor_schema(vendor_name):
    return mapping_metadata[vendor_name]

def get_vendor_list():
    return list(mapping_metadata.keys())

def get_global_schema():
    return global_schema

def __add_vendor_to_warehouse(vendor_name):
    # Get the schema of the vendor from pickle file
    with open('metadata_mapping.pickle', 'rb') as f:
        mapping_metadata = pickle.load(f)

    # Get the schema of the vendor
    vendor_schema = mapping_metadata[vendor_name]

    # Now writing a query to add the records from the vendor to the warehouse, using the vendor_schema
    query = "INSERT INTO course_details (" +global_schema.join(", ") + ") SELECT "
    for col_name in global_schema:
        if col_name in vendor_schema:
            query += vendor_schema[col_name] + ", "
        else:
            query += "NULL, "
    query = query[:-2]
    query += " FROM " + vendor_name

    # Executing the query
    mycursor.execute(query)
    mydb.commit()

def __delete_vendor_from_warehouse(vendor_name):
    # Now writing a query to add the records from the vendor to the warehouse, using the vendor_schema
    query = "DELETE FROM course_details WHERE course_vendor = '" + vendor_name + "'"

    # Executing the query
    mycursor.execute(query)
    mydb.commit()

# Defining a refresh function to repopulate the global schema
def refresh_CourseBucket():
    # Checking the difference in global_vendors and mapping_metadata. If there is a difference, then update the global schema

    # Get the list of vendors from the database
    mycursor.execute("SELECT DISTINCT course_vendor FROM course_details")
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
    print("4. View the schema of a vendor")
    print("5. View the global schema")
    print("6. Exit")
    choice = int(input("Enter your choice: "))

    global mapping_metadata
    # Read the metadata_mapping and store as a global variable
    with open('metadata_mapping.pickle', 'rb') as f:
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
    read_records('vendor1')
    # while True:
    #     main_menu()