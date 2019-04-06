create table game_xbox360(
	id serial primary key,
	title varchar(250) not null,
	slug varchar(250) not null unique,
	description text,
	image text,
	rating integer,
	screenshot text,
	platform_id integer, foreign key (platform_id) references platform(id) on delete set null,
	torr_link varchar(255),
	active boolean default true
);