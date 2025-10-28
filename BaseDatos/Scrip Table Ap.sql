CREATE TABLE `scisp`.`met_apci` (
  `idApCi` INT NOT NULL AUTO_INCREMENT,
  `IdCentro` VARCHAR(4) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `HoraI` TIME NOT NULL,
  `HoraF` TIME NOT NULL,
  `Anfitrion` INT NOT NULL,
  `Plantilla` INT NOT NULL,
  `Candados` INT NOT NULL,
  `idUsuario` INT NOT NULL,
  `TipoRecorrido` CHAR(1) CHARACTER SET 'utf8mb4' NOT NULL,
  PRIMARY KEY (`idApCi`),
  INDEX `SucursalApCi_idx` (`IdCentro` ASC) VISIBLE,
  INDEX `UsuariosApCi_idx` (`idUsuario` ASC) VISIBLE,
  CONSTRAINT `SucursalApCi`
    FOREIGN KEY (`IdCentro`)
    REFERENCES `scisp`.`sucursales` (`IdCentro`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `UsuariosApCi`
    FOREIGN KEY (`idUsuario`)
    REFERENCES `scisp`.`usuarios` (`IdUsuarios`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);