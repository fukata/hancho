drop database if exists hancho;
create database hancho ENCODING 'utf8';

\c hancho;

drop table if exists users;
create table users (
  id serial,
  username varchar(32) not null,
  created_at timestamp
);

drop table if exists user_messages;
create table user_messages (
  id serial,
  slack_user_id integer not null,
  message_type varchar(32),
  message text,
  created_at timestamp
);
