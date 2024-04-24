use `form_inspector`;

create table if not exists `tasks` (
    `_id` int primary key auto_increment,
    `user_id` int unique not null,
    `enable` int not null,
    `url` varchar(255) not null,
    `schedule` text not null,
    `actions` text not null,
    `created` timestamp default current_timestamp,
    `modified` timestamp default current_timestamp
);
