create table kanto_mesh (
  river_code VARCHAR(10),
  river_name VARCHAR(50),
  min_lng DOUBLE,
  min_lat DOUBLE,
  max_lng DOUBLE,
  max_lat DOUBLE
);

create index river_code_i on kanto_mesh(river_code);


