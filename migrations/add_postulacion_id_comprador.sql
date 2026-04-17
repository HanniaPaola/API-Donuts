-- Vincular postulaciones al comprador (ejecutar una vez en BD existente).
ALTER TABLE postulaciones_colaborador
  ADD COLUMN id_comprador INT NULL,
  ADD INDEX ix_postulaciones_id_comprador (id_comprador),
  ADD CONSTRAINT fk_postulaciones_usuario_comprador
    FOREIGN KEY (id_comprador) REFERENCES usuario_comprador (id_comprador);
