CREATE TABLE `user` (
	`user_id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(100) NOT NULL,
	`email` VARCHAR(100) NOT NULL,
	`password` VARCHAR(100) NOT NULL,
	`mobile_no` VARCHAR(10) NOT NULL,
	PRIMARY KEY (`user_id`)
);

CREATE TABLE `model` (
	`model_id` INT NOT NULL AUTO_INCREMENT,
	`model_name` VARCHAR(100) NOT NULL,
	`model_path` VARCHAR(100) NOT NULL,
	`model_file_name` VARCHAR(100) NOT NULL,
	`user_id` INT(100) NOT NULL,
	PRIMARY KEY (`model_id`)
);

CREATE TABLE `gateway` (
	`gateway_id` INT NOT NULL AUTO_INCREMENT,
	`ip` VARCHAR(20) NOT NULL,
	`uname` VARCHAR(100) NOT NULL,
	`password` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`gateway_id`)
);

CREATE TABLE `sensor` (
	`sensor_id` INT NOT NULL AUTO_INCREMENT,
	`type` VARCHAR(100) NOT NULL,
	`location` VARCHAR(100) NOT NULL,
	`gateway_id` INT(100) NOT NULL,
	PRIMARY KEY (`sensor_id`)
);

CREATE TABLE `schedule` (
	`schedule_id` INT NOT NULL AUTO_INCREMENT,
	`start_time` VARCHAR(10) NOT NULL,
	`end_time` VARCHAR(10) NOT NULL,
	`interval` INT NOT NULL,
	`count` INT NOT NULL,
	`repeat` VARCHAR(5) NOT NULL,
	`deploy_socket` VARCHAR(20) NOT NULL,
	`deploy_loc` VARCHAR(20) NOT NULL,
	`model_id` INT NOT NULL,
	PRIMARY KEY (`schedule_id`)
);

ALTER TABLE `model` ADD CONSTRAINT `model_fk0` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`);

ALTER TABLE `sensor` ADD CONSTRAINT `sensor_fk0` FOREIGN KEY (`gateway_id`) REFERENCES `gateway`(`gateway_id`);

ALTER TABLE `schedule` ADD CONSTRAINT `schedule_fk0` FOREIGN KEY (`model_id`) REFERENCES `model`(`model_id`);

