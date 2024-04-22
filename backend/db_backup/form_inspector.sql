create databse if not exists `form_inspector`;

use `form_inspector`;

create table if not exists `tasks_config` (
    `id` int primary key,
    `user_id` int uniq not null,
    `schedule_config` text not null,
    `config` text not null,
    `created` timestamp default current_timestamp,
    `modified` timestamp default current_timestamp
);
