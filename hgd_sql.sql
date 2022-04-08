CREATE TABLE `hnd_db`.`todo` (
  `pid` INT NOT NULL,
  `todocontent` VARCHAR(45) NOT NULL,
  `todook` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`pid`));

INSERT INTO todo (pid, todocontent) VALUES ('1', '가상현실 공부');
INSERT INTO todo (pid, todocontent) VALUES ('2', '가상응용 필기');

UPDATE `hnd_db`.`todo` SET `levelct` = '3' WHERE (`pid` = '1');
UPDATE `hnd_db`.`todo` SET `levelct` = '2' WHERE (`pid` = '2');


ALTER TABLE `hnd_db`.`member` ADD COLUMN regDate DATETIME;