-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema scisp
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema scisp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `scisp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci ;
USE `scisp` ;

-- -----------------------------------------------------
-- Table `scisp`.`estados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`estados` (
  `IdEstado` INT NOT NULL,
  `Estado` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`IdEstado`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`municipios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`municipios` (
  `idMunicipios` INT NOT NULL,
  `Municipio` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`idMunicipios`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_spanish2_ci;


-- -----------------------------------------------------
-- Table `scisp`.`tiposucursal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`tiposucursal` (
  `IdTipoSucursal` VARCHAR(1) NOT NULL,
  `TipoSucursal` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`IdTipoSucursal`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`zonas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`zonas` (
  `idZona` INT NOT NULL,
  `Zona` VARCHAR(13) NOT NULL,
  PRIMARY KEY (`idZona`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`sucursales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`sucursales` (
  `IdCentro` VARCHAR(4) NOT NULL,
  `Sucursales` VARCHAR(30) NOT NULL,
  `IdTipoSucursal` VARCHAR(1) NOT NULL,
  `IdZona` INT NOT NULL,
  `IdEstado` INT NOT NULL,
  `Latitud` VARCHAR(20) NOT NULL,
  `Longitud` VARCHAR(20) NOT NULL,
  `IdMunicipio` INT NOT NULL,
  PRIMARY KEY (`IdCentro`),
  INDEX `FkIdZonas_idx` (`IdZona` ASC) VISIBLE,
  INDEX `FkIdEstado_idx` (`IdEstado` ASC) VISIBLE,
  INDEX `FkIdMunicipio_idx` (`IdMunicipio` ASC) VISIBLE,
  INDEX `FkIdTipoSucursal_idx` (`IdTipoSucursal` ASC) VISIBLE,
  CONSTRAINT `FkdEstado`
    FOREIGN KEY (`IdEstado`)
    REFERENCES `scisp`.`estados` (`IdEstado`),
  CONSTRAINT `FkIdMunicipio`
    FOREIGN KEY (`IdMunicipio`)
    REFERENCES `scisp`.`municipios` (`idMunicipios`),
  CONSTRAINT `FkIdTipoSucursal`
    FOREIGN KEY (`IdTipoSucursal`)
    REFERENCES `scisp`.`tiposucursal` (`IdTipoSucursal`),
  CONSTRAINT `FkIdZonas`
    FOREIGN KEY (`IdZona`)
    REFERENCES `scisp`.`zonas` (`idZona`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`nivelusuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`nivelusuarios` (
  `IdNivelUsuario` INT NOT NULL,
  `NivelUsuario` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`IdNivelUsuario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`usuarios` (
  `IdUsuarios` INT NOT NULL,
  `NombreUsuario` VARCHAR(45) NOT NULL,
  `Contraseña` VARCHAR(205) NOT NULL,
  `idNivelUsuario` INT NOT NULL,
  `Estatus` TINYINT NOT NULL,
  `FechaAlta` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`IdUsuarios`),
  INDEX `IdNivelUsuario_idx` (`idNivelUsuario` ASC) VISIBLE,
  CONSTRAINT `IdNivelUsuario`
    FOREIGN KEY (`idNivelUsuario`)
    REFERENCES `scisp`.`nivelusuarios` (`IdNivelUsuario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`met_manejovalores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`met_manejovalores` (
  `Folio` INT NOT NULL AUTO_INCREMENT,
  `idCentro` VARCHAR(4) NOT NULL,
  `Fecha` DATE NULL DEFAULT NULL,
  `Anfitrion` INT NULL DEFAULT NULL,
  `idUsuarios` INT NOT NULL,
  `Estado` CHAR(1) NULL DEFAULT NULL,
  PRIMARY KEY (`Folio`),
  INDEX `SucursalManejoValores_idx` (`idCentro` ASC) VISIBLE,
  INDEX `UsuariosManejoVal_idx` (`idUsuarios` ASC) VISIBLE,
  CONSTRAINT `SucursalManejoValores`
    FOREIGN KEY (`idCentro`)
    REFERENCES `scisp`.`sucursales` (`IdCentro`),
  CONSTRAINT `UsuariosManejoVal`
    FOREIGN KEY (`idUsuarios`)
    REFERENCES `scisp`.`usuarios` (`IdUsuarios`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`met_incmanval`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`met_incmanval` (
  `idIncidencia` INT NOT NULL AUTO_INCREMENT,
  `Incidencia` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idIncidencia`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_spanish2_ci;


-- -----------------------------------------------------
-- Table `scisp`.`met_detmanval`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`met_detmanval` (
  `idDetManVal` INT NOT NULL AUTO_INCREMENT,
  `Folio` INT NOT NULL,
  `Movimiento` CHAR(1) NOT NULL,
  `Hora` TIME NOT NULL,
  `Caja` INT NOT NULL,
  `Cajero` INT NOT NULL,
  `idIncidencia` INT NOT NULL,
  `Deposito` CHAR(1) NOT NULL,
  `Comentario` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`idDetManVal`),
  INDEX `FolioDetManVal_idx` (`Folio` ASC) VISIBLE,
  INDEX `IncdetManVal_idx` (`idIncidencia` ASC) VISIBLE,
  CONSTRAINT `FolioDetManVal`
    FOREIGN KEY (`Folio`)
    REFERENCES `scisp`.`met_manejovalores` (`Folio`),
  CONSTRAINT `IncdetManVal`
    FOREIGN KEY (`idIncidencia`)
    REFERENCES `scisp`.`met_incmanval` (`idIncidencia`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`met_mansf`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`met_mansf` (
  `idSF` INT NOT NULL AUTO_INCREMENT,
  `Tipo` CHAR(1) NOT NULL,
  `Importe` FLOAT NOT NULL,
  `idDetManVal` INT NOT NULL,
  PRIMARY KEY (`idSF`),
  INDEX `DetManValSF_idx` (`idDetManVal` ASC) VISIBLE,
  CONSTRAINT `DetManValSF`
    FOREIGN KEY (`idDetManVal`)
    REFERENCES `scisp`.`met_detmanval` (`idDetManVal`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `scisp`.`met_usuariosuc`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`met_usuariosuc` (
  `idmet_UsuarioSuc` INT NOT NULL AUTO_INCREMENT,
  `idUsuarios` INT NOT NULL,
  `idCentro` VARCHAR(4) NOT NULL,
  PRIMARY KEY (`idmet_UsuarioSuc`),
  INDEX `UsuarioSuc_idx` (`idUsuarios` ASC) VISIBLE,
  INDEX `SucUsuario_idx` (`idCentro` ASC) VISIBLE,
  CONSTRAINT `SucUsuario`
    FOREIGN KEY (`idCentro`)
    REFERENCES `scisp`.`sucursales` (`IdCentro`),
  CONSTRAINT `UsuarioSuc`
    FOREIGN KEY (`idUsuarios`)
    REFERENCES `scisp`.`usuarios` (`IdUsuarios`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

ALTER TABLE met_detmanval
  ADD CONSTRAINT chk_movimientos_acr
  CHECK (`Movimiento` IN ('A','C','R'));
  
ALTER TABLE met_mansf
  ADD CONSTRAINT chk_mansf
  CHECK (`Tipo` IN ('S','F'));
  
ALTER TABLE met_detmanval
  ADD CONSTRAINT chk_deposito
  CHECK (`Deposito` IN ('S','N'));


USE `scisp` ;

-- -----------------------------------------------------
-- Placeholder table for view `scisp`.`vmovimientos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scisp`.`vmovimientos` (`Folio` INT, `Sucursales` INT, `Fecha` INT, `Movimiento` INT, `Hora` INT, `Incidencia` INT, `TipoSF` INT, `Importe` INT);

-- -----------------------------------------------------
-- procedure InsertarManVal
-- -----------------------------------------------------

DELIMITER $$
USE `scisp`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertarManVal`(
    IN pSucursal     VARCHAR(4),
    IN pAnfitrion    INT,
    IN pIdUsuarios   INT,
    IN pEstado       CHAR(1),   -- normalmente 'A' si crea folio
    IN pMovimiento   CHAR(1),   -- 'R' | 'C' | 'A'
    IN pHoraM        TIME,
    IN pCaja         INT,
    IN pCajero       INT,
    IN pIdIncidencia INT,       -- REQUERIDO (>0), FK a met_incmanval
    IN pDeposito     CHAR(1),   -- 'S'|'N'
    IN pComentario   VARCHAR(100),
    IN pSF           CHAR(1),   -- 'S'|'N'
    IN pTipoSF       CHAR(1),
    IN pSFMonto      FLOAT,
    OUT pMsg         VARCHAR(255)
)
BEGIN
    DECLARE vFolio INT;
    DECLARE vDetId INT;
    DECLARE vFecha DATE;

    -- si algo falla, rollback y sal del SP (sin llegar al COMMIT)
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET pMsg = 'Error al registrar el movimiento';
    END;

    START TRANSACTION;

    SET vFecha = CURDATE();

    -- Busca folio abierto del día
    SELECT Folio
      INTO vFolio
      FROM met_manejovalores
     WHERE idCentro = pSucursal COLLATE utf8mb4_spanish2_ci
       AND Fecha    = vFecha
       AND Estado   = 'A'
     LIMIT 1;

    -- Si no existe, crea encabezado (Folio AUTO_INCREMENT)
    IF vFolio IS NULL THEN
        INSERT INTO met_manejovalores (idCentro, Fecha, Anfitrion, idUsuarios, Estado)
        VALUES (pSucursal, vFecha, pAnfitrion, pIdUsuarios, pEstado);   -- pEstado suele ser 'A'
        SET vFolio = LAST_INSERT_ID();
    END IF;

    -- Inserta detalle (idDetManVal AUTO_INCREMENT)
    INSERT INTO met_detmanval
        (Folio, Movimiento, Hora, Caja, Cajero, idIncidencia, Deposito, Comentario)
    VALUES
        (vFolio, pMovimiento, pHoraM, pCaja, pCajero, pIdIncidencia, pDeposito, pComentario);

    SET vDetId = LAST_INSERT_ID();

    -- Inserta SF si aplica
    IF pSF = 'S' THEN
        INSERT INTO met_mansf (Tipo, Importe, idDetManVal)
        VALUES (pTipoSF, pSFMonto, vDetId);
    END IF;

    COMMIT;
    SET pMsg = CONCAT('Movimiento registrado. Folio=', vFolio, ' Detalle=', vDetId);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure mmv_abrir_folio
-- -----------------------------------------------------

DELIMITER $$
USE `scisp`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `mmv_abrir_folio`(
  IN  pCentro     VARCHAR(4),
  IN  pAnfitrion  INT,
  IN  pIdUsuarios INT,
  IN  pEstado     CHAR(1),    -- normalmente 'A'
  OUT pFolio      INT
)
BEGIN
  DECLARE vFolio INT;
  DECLARE vHoy   DATE;

  SET vHoy = CURDATE();

  SELECT Folio INTO vFolio
  FROM met_manejovalores
  WHERE idCentro=pCentro AND Fecha=vHoy AND Estado='A'
  LIMIT 1;

  IF vFolio IS NULL THEN
     INSERT INTO met_manejovalores (idCentro, Fecha, Anfitrion, idUsuarios, Estado)
     VALUES (pCentro, vHoy, pAnfitrion, pIdUsuarios, pEstado);
     SET vFolio = LAST_INSERT_ID();
  END IF;

  SET pFolio = vFolio;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure mmv_registrar_mov
-- -----------------------------------------------------

DELIMITER $$
USE `scisp`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `mmv_registrar_mov`(
  IN  pFolio        INT,
  IN  pMovimiento   CHAR(1),  -- 'R'|'C'|'A'
  IN  pHoraM        TIME,
  IN  pCaja         INT,
  IN  pCajero       INT,
  IN  pIdIncidencia INT,      -- >0 requiere existir en met_incmanval
  IN  pDeposito     CHAR(1),  -- 'S'|'N'
  IN  pComentario   VARCHAR(100),
  IN  pSF           CHAR(1),  -- 'S'|'N'
  IN  pTipoSF       CHAR(1),
  IN  pSFMonto      FLOAT,
  OUT pDetId        INT
)
BEGIN
  DECLARE vDetId INT;

  -- valida lo básico de forma explícita; si falla, MySQL te dará error claro
  IF pMovimiento NOT IN ('R','C','A') THEN
     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Movimiento inválido';
  END IF;

  -- Folio debe existir y estar 'A'
  IF NOT EXISTS (SELECT 1 FROM met_manejovalores WHERE Folio=pFolio AND Estado='A') THEN
     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Folio no existe o no está abierto';
  END IF;

  -- Incidencia debe existir (>0)
  IF NOT EXISTS (SELECT 1 FROM met_incmanval WHERE idIncidencia=pIdIncidencia) THEN
     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Incidencia no existe';
  END IF;

  INSERT INTO met_detmanval
    (Folio, Movimiento, Hora, Caja, Cajero, idIncidencia, Deposito, Comentario)
  VALUES
    (pFolio, pMovimiento, pHoraM, pCaja, pCajero, pIdIncidencia, pDeposito, pComentario);

  SET vDetId = LAST_INSERT_ID();

  IF pSF='S' THEN
     INSERT INTO met_mansf (Tipo, Importe, idDetManVal)
     VALUES (pTipoSF, pSFMonto, vDetId);
  END IF;

  SET pDetId = vDetId;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- View `scisp`.`vmovimientos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scisp`.`vmovimientos`;
USE `scisp`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `scisp`.`vmovimientos` AS select `d`.`Folio` AS `Folio`,`s`.`Sucursales` AS `Sucursales`,`m`.`Fecha` AS `Fecha`,`d`.`Movimiento` AS `Movimiento`,`d`.`Hora` AS `Hora`,`i`.`Incidencia` AS `Incidencia`,`sf`.`Tipo` AS `TipoSF`,`sf`.`Importe` AS `Importe` from ((((`scisp`.`met_manejovalores` `m` join `scisp`.`met_detmanval` `d` on((`d`.`Folio` = `m`.`Folio`))) left join `scisp`.`met_mansf` `sf` on((`sf`.`idDetManVal` = `d`.`idDetManVal`))) join `scisp`.`sucursales` `s` on((`s`.`IdCentro` = (`m`.`idCentro` collate utf8mb4_spanish2_ci)))) join `scisp`.`met_incmanval` `i` on((`i`.`idIncidencia` = `d`.`idIncidencia`))) order by `d`.`idDetManVal`;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
