USE kanto_rivers;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;

-- create table kanto_mesh (
--   river_code VARCHAR(10),
--   river_name VARCHAR(50),
--   min_lng DOUBLE,
--   min_lat DOUBLE,
--   max_lng DOUBLE,
--   max_lat DOUBLE
-- );
-- create index river_code_i on kanto_mesh(river_code);


-- DROP TABLE IF EXISTS compact_kanto_mesh;
-- CREATE TABLE compact_kanto_mesh (
--   modified_mesh_code BIGINT,
--   river_code         BIGINT,
-- KEY idx_mesh_code (modified_mesh_code),
-- KEY idx_river_code (river_code)
-- ) DEFAULT CHARSET=utf8;

-- CREATE TABLE river_codes (
--   river_code BIGINT,
--   name       VARCHAR(50),
-- KEY idx_river_code (river_code)
-- ) DEFAULT CHARSET=utf8;

truncate compact_kanto_mesh;

SET character_set_client = @saved_cs_client;

