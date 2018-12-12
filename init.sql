create table post (
	id serial,
	title varchar(255) not null,
	body text


);

insert into post (title, body) values ('первый пост', 'Привет');



create table user_d (
	id serial primary key,
	login varchar(40) not null unique,
	password text not null,
	email text not null unique ,
	admin_privilege boolean default false
);

insert into user_d (login, password, email, admin_privilege) values ('admin', '1234', 'admin@t.py', 'true');

create table session (
	id serial primary key,
	user_ses varchar(40) ,
	session_num text
);
