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
-- Table structure for table `updates_web`
--

DROP TABLE IF EXISTS `updates_web`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `updates_web` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_idn` varchar(253) NOT NULL,
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


--
-- Table structure for table `webdomain_options`
--

DROP TABLE IF EXISTS `webdomain_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webdomain_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `lb_ipaddr` char(16) NOT NULL,
  `real_ipaddr` char(16) NOT NULL,
  `name_idn` varchar(255) NOT NULL,
  `active` char(3) NOT NULL DEFAULT 'on',
  `secure` char(3) NOT NULL DEFAULT 'off',
  `redirect_http` char(3) NOT NULL DEFAULT 'off',
  `botguard_check` char(3) NOT NULL DEFAULT 'on',
  `l7filter` char(3) NOT NULL DEFAULT 'off',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1424 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `webdomain_options`
--

DROP TABLE IF EXISTS `webdomain_alias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webdomain_alias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_idn` varchar(253) NOT NULL,
  `alias` char(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1424 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-28 16:24:14
