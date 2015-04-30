-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ehelp
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.04.1

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(100) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `chat_token` varchar(100) DEFAULT NULL,
  `salt` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coin_trade`
--

DROP TABLE IF EXISTS `coin_trade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coin_trade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eventid` int(11) NOT NULL,
  `from` int(11) NOT NULL,
  `to` int(11) NOT NULL,
  `lovecoin` int(11) NOT NULL DEFAULT '0',
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `eventid_idx` (`eventid`),
  KEY `from_idx` (`from`),
  KEY `to_idx` (`to`),
  CONSTRAINT `coin_trade_eventid_fk` FOREIGN KEY (`eventid`) REFERENCES `event` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coin_trade_from_fk` FOREIGN KEY (`from`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coin_trade_to_fk` FOREIGN KEY (`to`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `author` int(11) NOT NULL,
  `content` text,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `event_id_idx` (`event_id`),
  KEY `author_idx` (`author`),
  CONSTRAINT `comment_author_fk` FOREIGN KEY (`author`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_eventid_fk` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `donate_event`
--

DROP TABLE IF EXISTS `donate_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donate_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from` int(11) NOT NULL,
  `to` int(11) NOT NULL,
  `donate_love_coin` int(11) DEFAULT NULL,
  `donate_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `from_idx` (`from`),
  KEY `to_idx` (`to`),
  CONSTRAINT `donate_event_from_fk` FOREIGN KEY (`from`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `donate_event_to_fk` FOREIGN KEY (`to`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `evaluation`
--

DROP TABLE IF EXISTS `evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `from` int(11) NOT NULL,
  `to` int(11) NOT NULL,
  `value` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `event_idx` (`event_id`),
  KEY `to_idx` (`to`),
  KEY `from_idx` (`from`),
  CONSTRAINT `evaluation_eventid_fk` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `evaluation_from_fk` FOREIGN KEY (`from`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `evaluation_to_fk` FOREIGN KEY (`to`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `launcher` int(11) NOT NULL,
  `content` varchar(500) DEFAULT NULL,
  `type` int(11) NOT NULL DEFAULT '0',
  `time` datetime DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT '999.9999999',
  `latitude` decimal(10,7) DEFAULT '999.9999999',
  `state` int(11) NOT NULL DEFAULT '0',
  `follow_number` int(11) NOT NULL DEFAULT '0',
  `support_number` int(11) NOT NULL DEFAULT '0',
  `group_pts` decimal(7,4) NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`id`),
  KEY `launcher_idx` (`launcher`),
  CONSTRAINT `event_launcher_fk` FOREIGN KEY (`launcher`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `health`
--

DROP TABLE IF EXISTS `health`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `health` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `value` decimal(7,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_idx` (`user_id`),
  CONSTRAINT `health_userid_fk` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `illness`
--

DROP TABLE IF EXISTS `illness`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `illness` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `content` varchar(45) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_idx` (`user_id`),
  CONSTRAINT `illness_userid_fk` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `loving_bank`
--

DROP TABLE IF EXISTS `loving_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loving_bank` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `score_rank` int(11) NOT NULL DEFAULT '0',
  `score_exchange` int(11) NOT NULL DEFAULT '0',
  `love_coin` int(11) NOT NULL DEFAULT '0',
  `family_love_coin` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `userid_idx` (`userid`),
  CONSTRAINT `loving_bank_userid_fk` FOREIGN KEY (`userid`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `static_relation`
--

DROP TABLE IF EXISTS `static_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `static_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_a` int(11) NOT NULL,
  `user_b` int(11) NOT NULL,
  `type` int(11) NOT NULL DEFAULT '0',
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_a_idx` (`user_a`),
  KEY `user_b_idx` (`user_b`),
  CONSTRAINT `relation_usera_fk` FOREIGN KEY (`user_a`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relation_userb_fk` FOREIGN KEY (`user_b`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `support_relation`
--

DROP TABLE IF EXISTS `support_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `support_relation` (
  `event_id` int(11) NOT NULL,
  `supportee` int(11) NOT NULL,
  `supporter` int(11) NOT NULL,
  `type` int(11) NOT NULL DEFAULT '0',
  `time` datetime NOT NULL,
  PRIMARY KEY (`event_id`,`supportee`,`supporter`),
  KEY `relation_supportee_fk` (`supportee`),
  KEY `relation_supporter_fk` (`supporter`),
  KEY `relation_event_id_fk` (`event_id`),
  CONSTRAINT `relation_eventid_fk` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relation_supportee_fk` FOREIGN KEY (`supportee`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relation_supporter_fk` FOREIGN KEY (`supporter`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `nickname` varchar(45) DEFAULT NULL,
  `gender` int(11) DEFAULT '1',
  `age` int(11) DEFAULT '0',
  `phone` varchar(45) DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT '999.9999999',
  `latitude` decimal(10,7) DEFAULT '999.9999999',
  `occupation` int(11) DEFAULT '0',
  `reputation` decimal(7,4) DEFAULT '0.0000',
  `avatar` varchar(200) DEFAULT NULL,
  `identity_id` varchar(45) DEFAULT NULL,
  `type` int(11) DEFAULT '0',
  `isVerify` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nickname` (`nickname`),
  CONSTRAINT `user_id_fk` FOREIGN KEY (`id`) REFERENCES `account` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-04-30 17:27:44
