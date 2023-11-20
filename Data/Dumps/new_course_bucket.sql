use nptel;

CREATE VIEW course_bucket4 AS (
    (SELECT Course_number as local_course_id, Course_Name as course_name, Course_Description as course_description, University as university, 
     Course_URL as course_url, Price as price, 'coursera' AS course_vendor FROM coursera_courses) 
    Union 
    (SELECT id as local_course_id, Course_Name as course_name, CONCAT('Prof: ', SME_Name, ', Duration: ', Duration, ", Applicable_NPTEL_Domain: ", IFNULL(Applicable_NPTEL_Domain, 'NA')) as course_description, Institute as university, NPTEL_URL as course_url, 
     Price as price, 'nptel' AS course_vendor FROM nptel_courses)
    Union 
    (SELECT id as local_course_id, Title as course_name, CONCAT("Instructor: ", instructor, ", course duration: ", course_duration) as course_description, "NA" as university, URL as course_url, 
     price, 'skillshare' as course_vendor FROM skillshare_courses) 
    Union 
    (SELECT number as local_course_id, Name as course_name, About as course_description, School as university, Link as course_url, 
     Price as price, 'udacity' AS course_vendor FROM udacity_courses) 
    Union 
    (SELECT course_id as local_course_id, course_title as course_name, CONCAT("Subject: ", subject, ", Number of lecture: ", num_lectures, ", content duration in hours: ", content_duration, ", Course Level: ", level) as course_description, 
     "NA" as university, url as course_url, price, 'udemy' AS course_vendor FROM udemy_courses) 
    );
SELECT * FROM course_bucket4;

CREATE TABLE course_bucket (
    id INT AUTO_INCREMENT,
	local_course_id int NOT NULL DEFAULT '0',
	course_name varchar(200) DEFAULT NULL,
	course_description text,
	university varchar(200) DEFAULT NULL,
	course_url varchar(200) DEFAULT NULL,
	price int DEFAULT NULL,
	course_vendor varchar(10) NOT NULL DEFAULT '',
    PRIMARY KEY (id)
);
INSERT INTO course_bucket (local_course_id, course_name, course_description, university, course_url, price, course_vendor)
SELECT local_course_id, course_name, course_description, university, course_url, price, course_vendor FROM course_bucket4;
SELECT * FROM course_bucket;

-- course_bucket: 4132
-- coursera_courses: 3440
-- nptel_courses: 290
-- skillshare_courses: 98
-- udacity_courses: 55
-- udemy_courses: 249