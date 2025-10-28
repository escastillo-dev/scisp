CREATE TABLE `scisp`.`met_detapci` (
  `idDetApCi` INT NOT NULL AUTO_INCREMENT,
  `idApCi` INT NOT NULL,
  `idEquipo` INT NOT NULL,
  `Calificacion` CHAR(1) NOT NULL,
  `Comentario` VARCHAR(45) NULL,
  PRIMARY KEY (`idDetApCi`),
  INDEX `DetApCi_idx` (`idApCi` ASC) VISIBLE,
  INDEX `EquipoApCi_idx` (`idEquipo` ASC) VISIBLE,
  CONSTRAINT `DetApCi`
    FOREIGN KEY (`idApCi`)
    REFERENCES `scisp`.`met_apci` (`idApCi`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `EquipoApCi`
    FOREIGN KEY (`idEquipo`)
    REFERENCES `scisp`.`met_equipos` (`idEquipo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);