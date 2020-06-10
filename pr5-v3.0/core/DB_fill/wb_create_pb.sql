SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema purbeurre_orm
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema purbeurre_orm
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `purbeurre_orm` DEFAULT CHARACTER SET utf8 ;
USE `purbeurre_orm` ;

-- -----------------------------------------------------
-- Table `purbeurre_orm`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_orm`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `generic_name` VARCHAR(45) NOT NULL,
  `dumped_from` VARCHAR(45) NOT NULL,
  `image_url` VARCHAR(45) NULL,
  `nutrition_grade` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre_orm`.`substitutions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_orm`.`substitutions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `primary_prod_rel` INT NOT NULL,
  `final_prod_rel` INT NOT NULL,
  PRIMARY KEY (`id`, `primary_prod_rel`),
  INDEX `fk_prime_prod_idx` (`primary_prod_rel` ASC),
  INDEX `fk_sub_prod_idx` (`final_prod_rel` ASC),
  CONSTRAINT `fk_prime_prod`
    FOREIGN KEY (`primary_prod_rel`)
    REFERENCES `purbeurre_orm`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sub_prod`
    FOREIGN KEY (`final_prod_rel`)
    REFERENCES `purbeurre_orm`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre_orm`.`categories_dumped`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_orm`.`categories_dumped` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cat_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre_orm`.`sub_cats`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `purbeurre_orm`.`sub_cats` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `prod_rel_id` INT NOT NULL,
  `cat_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`, `prod_rel_id`),
  INDEX `fk_prod_idx` (`prod_rel_id` ASC),
  CONSTRAINT `fk_prod`
    FOREIGN KEY (`prod_rel_id`)
    REFERENCES `purbeurre_orm`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
