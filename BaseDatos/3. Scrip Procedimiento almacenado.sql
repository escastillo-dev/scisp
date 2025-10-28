DELIMITER //

DROP PROCEDURE IF EXISTS InsertarManVal //
CREATE PROCEDURE InsertarManVal(
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
END //

DELIMITER ;






-- Variables de salida
SET @msg := '';

/* Caso #1: Abre folio en T013 (Estado 'A' en encabezado) y registra un Retiro (R) */
CALL InsertarManVal(
  'T017',        -- pSucursal
  321,           -- pAnfitrion
  821,           -- pIdUsuarios (usuario APP que abre)
  'A',           -- pEstado (encabezado si se crea)
  'R',           -- pMovimiento
  '10:05:00',    -- pHoraM
  5,             -- pCaja
  778,           -- pCajero
  1,             -- pIdIncidencia (0 -> NULL)
  'S',           -- pDeposito
  'Retiro por ajuste', -- pComentario
  'N',           -- pSF (no registra SF)
  NULL,          -- pTipoSF
  NULL,          -- pSFMonto
  @msg           -- OUT
);
SELECT @msg AS msg_1;

/* Caso #2: Mismo folio T013, registra un Corte (C) con incidencia 2 */
CALL InsertarManVal(
  'T014',
  321,
  456,
  'A',
  'C',
  '13:00:00',
  3,
  771,
  2,            -- idIncidencia = 2 (Valores fuera de caja)
  'N',
  'Semáforo naranja',
  'N',
  NULL,
  NULL,
  @msg
);
SELECT @msg AS msg_2;

/* Caso #3: Mismo folio T013, registra Arqueo (A) con SF */
CALL InsertarManVal(
  'T013',
  321,
  456,
  'A',
  'A',
  '14:30:00',
  2,
  700,
  2,            -- sin incidencia
  'S',          -- depósito marcado
  'Arqueo vespertino',
  'S',          -- pSF = 'S' -> crea registro en met_mansf
  'S',          -- pTipoSF (ej. N=naranja)
  150.00,       -- pSFMonto
  @msg
);
SELECT @msg AS msg_3;

/* Caso #4: Otra sucursal T021: debería crear folio nuevo para este día */
CALL InsertarManVal(
  'T021',
  321,
  456,
  'A',
  'R',
  '09:10:00',
  4,
  660,
  0,
  'N',
  'Retiro inicial',
  'N',
  NULL,
  NULL,
  @msg
);
SELECT @msg AS msg_4;

SET @msg := '';
CALL InsertarManVal(
  'T014', 321, 456, 'A',
  'R', '10:05:00', 5, 778,
  1,  'N', 'Retiro prueba',
  'N', NULL, NULL, @msg
);
SELECT @msg AS msg;


