create table ambiente(
	id_ambiente SERIAL not null,
	nome varchar(100),
	primary key (id_ambiente)
);

create table sensor_temperatura(
	id_sensor_temperatura SERIAL not null,
	id_ambiente integer not null,
	nome varchar(100),
	primary key (id_sensor_temperatura),
	foreign key (id_ambiente) references ambiente(id_ambiente)
);

create table sensor_umidade(
	id_sensor_umidade SERIAL not null,
	id_ambiente integer not null,
	nome varchar(100),
	primary key (id_sensor_umidade),
	foreign key (id_ambiente) references ambiente(id_ambiente)
);

create table balanca(
	id_balanca SERIAL not null,
	id_ambiente integer not null,
	nome varchar(100),
	primary key (id_balanca),
	foreign key (id_ambiente) references ambiente(id_ambiente)
);

create table aves(
	id_ave SERIAL not null,
	rfid integer not null,
	id_ambiente integer not null,
	nome varchar(100),
	primary key (id_ave)
);

create table tipo_alimento(
	id_tipo_alimento SERIAL not null,
	nome varchar(100),
	primary key (id_tipo_alimento)
);

create table alimento(
	id_alimento SERIAL not null,
	id_tipo_alimento integer not null,
	data_hora TIMESTAMP DEFAULT NOW(),
	id_ambiente integer not null,
	primary key (id_alimento),
	foreign key (id_ambiente) references ambiente(id_ambiente)
);

create table temperatura(
	id_temperatura SERIAL not null,
	data_hora TIMESTAMP DEFAULT NOW(),
	id_sensor_temperatura integer not null,
	id_ambiente integer not null,
	valor float,
	primary key (id_temperatura),
	foreign key (id_ambiente) references ambiente(id_ambiente),
	foreign key (id_sensor_temperatura) references sensor_temperatura(id_sensor_temperatura)
);

create table umidade(
	id_umidade SERIAL not null,
	data_hora TIMESTAMP DEFAULT NOW(),
	id_sensor_umidade integer not null,
	id_ambiente integer not null,
	valor float,
	primary key (id_umidade),
	foreign key (id_ambiente) references ambiente(id_ambiente),
	foreign key (id_sensor_umidade) references sensor_umidade(id_sensor_umidade)
);

create table peso(
	id_peso SERIAL not null,
	data_hora TIMESTAMP DEFAULT NOW(),
	id_balanca integer not null,
	id_ambiente integer not null,
	valor float,
	primary key (id_peso),
	foreign key (id_balanca) references balanca(id_balanca),
	foreign key (id_ambiente) references ambiente(id_ambiente)
);
