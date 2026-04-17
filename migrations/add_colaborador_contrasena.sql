-- Contraseña para acceso al panel del colaborador (login).
ALTER TABLE colaboradores
  ADD COLUMN contrasena VARCHAR(255) NULL AFTER email;
