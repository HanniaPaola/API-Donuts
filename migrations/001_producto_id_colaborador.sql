USE tienda_db;

ALTER TABLE producto
  ADD COLUMN id_colaborador INT NULL AFTER id_admin,
  ADD INDEX idx_producto_id_colaborador (id_colaborador),
  ADD CONSTRAINT fk_producto_colaborador
    FOREIGN KEY (id_colaborador) REFERENCES colaboradores(id)
    ON DELETE SET NULL;
