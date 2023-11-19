-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: nptel
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `course_bucket4`
--

DROP TABLE IF EXISTS `course_bucket4`;
/*!50001 DROP VIEW IF EXISTS `course_bucket4`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `course_bucket4` AS SELECT 
 1 AS `course_id`,
 1 AS `course_name`,
 1 AS `course_description`,
 1 AS `university`,
 1 AS `course_url`,
 1 AS `price`,
 1 AS `course_vendor`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `course_bucket4`
--

/*!50001 DROP VIEW IF EXISTS `course_bucket4`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `course_bucket4` AS select `coursera_courses`.`Course_number` AS `course_id`,`coursera_courses`.`Course_Name` AS `course_name`,`coursera_courses`.`Course_Description` AS `course_description`,`coursera_courses`.`University` AS `university`,`coursera_courses`.`Course_URL` AS `course_url`,`coursera_courses`.`Price` AS `price`,'coursera' AS `course_vendor` from `coursera_courses` union select (3440 + `nptel_courses`.`id`) AS `course_id`,`nptel_courses`.`Course_Name` AS `course_name`,concat('Prof: ',`nptel_courses`.`SME_Name`,', Duration: ',`nptel_courses`.`Duration`,', Applicable_NPTEL_Domain: ',ifnull(`nptel_courses`.`Applicable_NPTEL_Domain`,'NA')) AS `course_description`,`nptel_courses`.`Institute` AS `university`,`nptel_courses`.`NPTEL_URL` AS `course_url`,`nptel_courses`.`Price` AS `price`,'nptel' AS `course_vendor` from `nptel_courses` union select (3730 + `skillshare_courses`.`id`) AS `course_id`,`skillshare_courses`.`Title` AS `course_name`,concat('Instructor: ',`skillshare_courses`.`instructor`,', course duration: ',`skillshare_courses`.`course_duration`) AS `course_description`,'NA' AS `university`,`skillshare_courses`.`URL` AS `course_url`,`skillshare_courses`.`price` AS `price`,'skillshare' AS `course_vendor` from `skillshare_courses` union select (3828 + `udacity_courses`.`number`) AS `course_id`,`udacity_courses`.`Name` AS `course_name`,`udacity_courses`.`About` AS `course_description`,`udacity_courses`.`School` AS `university`,`udacity_courses`.`Link` AS `course_url`,`udacity_courses`.`Price` AS `price`,'udacity' AS `course_vendor` from `udacity_courses` union select (3883 + `udemy_courses`.`course_id`) AS `course_id`,`udemy_courses`.`course_title` AS `course_name`,concat('Subject: ',`udemy_courses`.`subject`,', Number of lecture: ',`udemy_courses`.`num_lectures`,', content duration in hours: ',`udemy_courses`.`content_duration`,', Course Level: ',`udemy_courses`.`level`) AS `course_description`,'NA' AS `university`,`udemy_courses`.`url` AS `course_url`,`udemy_courses`.`price` AS `price`,'udemy' AS `course_vendor` from `udemy_courses` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-20  2:13:10
