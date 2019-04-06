create table post (
	id serial,
	title varchar(255) not null,
	body text


);





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


create table category (
	id serial primary key,
	title varchar(250) not null,
	slug varchar(250) not null unique
);

create table  tag (
	id serial primary key,
	title varchar(250) not null,
	slug varchar(250) not null unique
);

create table news(
	id serial primary key,
	title varchar(250) not null,
	slug varchar(250) not null unique,
	user_id integer, foreign key (user_id) references user_d (id) on delete set null,
	category_id integer, foreign key (category_id) references category (id) on delete set null,
	text text,
	text_min text,
	date_created timestamptz ,
	date_change timestamptz,
	description varchar(250),
	likes integer default 0,
	image varchar(250),
	moderation boolean default false

);

create table news_tag (
	id serial primary key,
	news_id integer, foreign key (news_id) references news (id) on delete set null,
	tag_id integer, foreign key (tag_id) references tag (id) on delete set null
);



insert into category (title, slug) values ('cat_test1', 'cat_test1');
insert into tag (title, slug) values ('tag_test1', 'tag_test1');
insert into news(title, slug, user_id, category_id, text, text_min, description)
	values('news1', 'news1', '1', '1', 'bla bla bla', 'bla', 'hz');


insert into category (title, slug) values ('cat_test2', 'cat_test2');
insert into tag (title, slug) values ('tag_test2', 'tag_test2');
insert into news(title, slug, user_id, category_id, text, text_min, description)
	values('news2', 'news2', '2', '2', 'bla rt', 'bl', 'hzkl');

create table news_image (
	id serial primary key,
	news_id integer, foreign key (news_id) references news (id) on delete set null,
	image varchar(250)
);

