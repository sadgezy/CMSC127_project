-- THIS IS A PRE-MADE DATABASE AND ITS VALUES
-- SUCCEEDING CHANGES WILL OCCUR THROUGH THE TASKER APP

DROP DATABASE IF EXISTS `taskdb`;
CREATE DATABASE IF NOT EXISTS `taskdb`;
GRANT ALL ON taskdb.* TO 'root'@'localhost';
USE `taskdb`;

CREATE TABLE IF NOT EXISTS `category` (
    `categoryid` int(5) NOT NULL AUTO_INCREMENT, 
    `categoryname` varchar(255) NOT NULL, 
    `task_count` int(5) NOT NULL DEFAULT 0, 
    CONSTRAINT `category_categoryid_pk` PRIMARY KEY (`categoryid`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE IF NOT EXISTS `task` (
    `taskid` int(10) NOT NULL AUTO_INCREMENT, 
    `taskname` varchar(255) NOT NULL, 
    `startingdate` date, 
    `enddate` date, 
    `content` varchar(255), 
    `taskstatus` int(1) NOT NULL DEFAULT 0, 
    `categoryid` int(5), 
    CONSTRAINT `task_taskid_pk` PRIMARY KEY (`taskid`),
    CONSTRAINT `task_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES `category`(`categoryid`) ON DELETE SET NULL
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

INSERT INTO `category` (`categoryname`) VALUES 
    ('DAILY'),
    ('ACADEMICS'),
    ('WORK');

INSERT INTO `task` (`taskname`, `startingdate`, `enddate`, `content`, `taskstatus`) VALUES 
    ('CLEANSING', '2021-01-01', '2022-12-31', 'Read the Bible from 11:30am to 12:00am', 1),
    ('SHOWER', '2022-06-04', '2022-06-04', 'Take the dog a bath', 0),
    ('CMSC 127 Project', '2022-05-29', '2022-06-06', 'Fix bugs and errors', 2),
    ('CMSC 100 Exercise 10', '2022-05-29', '2022-06-09', 'Add authentication to javascript', 1),
    ('CMSC 141 Exercise 12', '2022-06-02', '2022-06-09', 'Fix bugs and errors', 0);

UPDATE `task` SET `categoryid` = 1 WHERE `taskname` = "CLEANSING";
UPDATE `task` SET `categoryid` = 2 WHERE `taskname` LIKE "%CMSC%";
UPDATE `category` SET `task_count` = 1 WHERE `categoryid` = 1;
UPDATE `category` SET `task_count` = 3 WHERE `categoryid` = 2;