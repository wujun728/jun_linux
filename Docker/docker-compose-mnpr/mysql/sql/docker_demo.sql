CREATE DATABASE `docker_demo`;

USE `docker_demo`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
	`user_id` BIGINT(20) NOT NULL DEFAULT '0' COMMENT 'uid',
	`nickname` VARCHAR(100) NULL DEFAULT NULL COMMENT 'name',
	`create_time` INT(11) NULL DEFAULT '0' COMMENT 'create_time',
	PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;