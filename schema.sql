-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: dnsmon
-- ------------------------------------------------------
-- Server version       5.5.68-MariaDB-cll-lve

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `updates`
--

DROP TABLE IF EXISTS `updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `updates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(253) NOT NULL,
  `updated_at` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1424 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `updates`
--

LOCK TABLES `updates` WRITE;
/*!40000 ALTER TABLE `updates` DISABLE KEYS */;
/*!40000 ALTER TABLE `updates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;



--
-- Table structure for table `updates_web`
--

DROP TABLE IF EXISTS `updates_web`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `updates_web` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(253) NOT NULL,
  `updated_at` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1424 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `updates_web`
--

LOCK TABLES `updates_web` WRITE;
/*!40000 ALTER TABLE `updates_web` DISABLE KEYS */;
/*!40000 ALTER TABLE `updates_web` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-28 16:24:14

DELIMITER //

CREATE TRIGGER `powerdns`.`insert_record` AFTER INSERT ON `powerdns`.`records`
FOR EACH ROW
BEGIN
SELECT `name` INTO @domain FROM `powerdns`.`domains` WHERE id = NEW.domain_id;
INSERT INTO `dnsmon`.`updates` Set domain = @domain, updated_at = UNIX_TIMESTAMP();
INSERT INTO `dnsmon`.`updates_web` Set domain = @domain, updated_at = UNIX_TIMESTAMP();
END//

CREATE TRIGGER `powerdns`.`update_record` AFTER UPDATE ON `powerdns`.`records`
FOR EACH ROW
BEGIN
SELECT `name` INTO @domain FROM `powerdns`.`domains` WHERE id = NEW.domain_id;
INSERT INTO `dnsmon`.`updates` Set domain = @domain, updated_at = UNIX_TIMESTAMP();
INSERT INTO `dnsmon`.`updates_web` Set domain = @domain, updated_at = UNIX_TIMESTAMP();
END//

CREATE TRIGGER `powerdns`.`delete_record` AFTER DELETE ON `powerdns`.`records`
FOR EACH ROW
BEGIN
SELECT `name` INTO @domain FROM `powerdns`.`domains` WHERE id = OLD.domain_id;
INSERT INTO `dnsmon`.`updates` Set domain = @domain, updated_at = UNIX_TIMESTAMP();
INSERT INTO `dnsmon`.`updates_web` Set domain = @domain, updated_at = UNIX_TIMESTAMP();
END//

DELIMITER ;