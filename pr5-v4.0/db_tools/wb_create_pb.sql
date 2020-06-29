CREATE DATABASE IF NOT EXISTS purbeurre_db;
USE `purbeurre_db` ;

-- -----------------------------------------------------
-- Table `purbeurre_db`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_db`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `generic_name` VARCHAR(200) NOT NULL,
  `dumped_from` VARCHAR(200) NOT NULL,
  `image_url` VARCHAR(200) NULL,
  `nutrition_grade` CHAR(1) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `purbeurre_db`.`substitutions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_db`.`substitutions` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `primary_prod_rel` INT NOT NULL,
    `final_prod_rel` INT NOT NULL,
    PRIMARY KEY (`id`, `primary_prod_rel`),
    INDEX `fk_prime_prod_idx` (`primary_prod_rel` ASC),
    INDEX `fk_sub_prod_idx` (`final_prod_rel` ASC),
    CONSTRAINT `fk_prime_prod`
        FOREIGN KEY (`primary_prod_rel`)
        REFERENCES `purbeurre_db`.`products` (`id`)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    CONSTRAINT `fk_sub_prod`
        FOREIGN KEY (`final_prod_rel`)
        REFERENCES `purbeurre_db`.`products` (`id`)
        ON DELETE CASCADE
        ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `purbeurre_db`.`categories_dumped`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_db`.`categories_dumped` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `cat_name` VARCHAR(95) NOT NULL,
    PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `purbeurre_db`.`sub_cats`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_db`.`sub_cats` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `prod_rel_id` INT NOT NULL,
    `cat_name` VARCHAR(95) NOT NULL,
    PRIMARY KEY (`id`, `prod_rel_id`),
    INDEX `fk_prod_idx` (`prod_rel_id` ASC),
    CONSTRAINT `fk_prod`
        FOREIGN KEY (`prod_rel_id`)
        REFERENCES `purbeurre_db`.`products` (`id`)
        ON DELETE CASCADE
        ON UPDATE NO ACTION);
