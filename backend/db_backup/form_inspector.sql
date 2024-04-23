use `form_inspector`;

create table if not exists `tasks` (
    `id` int primary key,
    `user_id` int unique not null,
    `enable` int not null,
    `schedule_config` text not null,
    `test_config` text not null,
    `created` timestamp default current_timestamp,
    `modified` timestamp default current_timestamp
);
