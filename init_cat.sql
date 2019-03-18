create table platform(
	id serial primary key,
	title varchar(250) not null,
	slug varchar(250) not null unique,
	description text,
	image text
	);

create table game(
	id serial primary key,
	title varchar(250) not null,
	slug varchar(250) not null unique,
	description text,
	image text,
	rating integer,
	screenshot text,
	platform_id integer, foreign key (platform_id) references platform(id) on delete set null,
	torr_link varchar(255)
);

create table genre(
	id serial primary key,
	title varchar(250) not null,
	slug varchar(250) not null unique,
	description text,
	image text,
);

create table genre_game(
	genre_id integer, foreign key (genre_id) references genre(id) on delete set null,
	game_id integer, foreign key (game_id) references game(id) on delete set null
	);

insert into platform (title, slug) values ('xbox 360' , 'xbox_360');