create view vMovimientos 
as
SELECT
  d.Folio,
  s.Sucursales,
  m.Fecha,
  d.Movimiento,
  d.Hora,
  i.Incidencia,
  sf.Tipo  AS TipoSF,
  sf.Importe
FROM met_manejovalores m
JOIN met_detmanval d
  ON d.Folio = m.Folio
LEFT JOIN met_mansf sf
  ON sf.idDetManVal = d.idDetManVal         -- ← LEFT JOIN (SF es opcional)
JOIN sucursales s
  ON s.idCentro = m.idCentro COLLATE utf8mb4_spanish2_ci
JOIN met_incmanval i
  ON i.idIncidencia = d.idIncidencia
ORDER BY d.idDetManVal;
 
 use scisp