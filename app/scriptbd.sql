--Creacion de la tabla en la bd
CREATE TABLE tareas (
  id int(11) NOT NULL,
  nombre_tarea varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  descripcion text COLLATE utf8_unicode_ci NOT NULL,
  tarea_realizada tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--Definir el campo id como llave primaria 
ALTER TABLE tareas
  ADD PRIMARY KEY (id);

--Definir el campo como auto incremental 
ALTER TABLE tareas
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;
COMMIT;