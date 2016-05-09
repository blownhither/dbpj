create table if not exists customer (
    customer_name 	varchar(255),
    customer_email	varchar(255),
    customer_id 	int auto_increment not null,
    primary key(customer_id)
);
