create table ushort.urls (
	shorturl varchar(50) not null,
	origurl varchar(255) not null,
	userid int,
	creation_date timestamp(0) default current_timestamp,
	expiration_date timestamp(0),
	constraint shorturl_pk primary key(shorturl),
	constraint userid_fk foreign key(userid)
		references ushort.userid(id)
		on delete cascade
);
create table ushort.userid (
	id int not null generated always as indentity,
	username varchar(255) not null,
	email varchar(255),
	creation_date timestamp(0) default current_timestamp,
	last_login timestamp(0),
	constraint id_pk primary key(id)
)
