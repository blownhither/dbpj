drop table if exists single_order;
drop table if exists customer;
drop table if exists inventory;
drop table if exists seller;
drop table if exists user_info;
drop table if exists item;
drop table if exists category;
drop table if exists detail;

create table if not exists category (
	category_title 	varchar(255) unique,
    category_desc 	varchar(255),				
    category_id 	serial not null,
	primary key(category_id)
);

create table if not exists user_info (
	user_name		varchar(225) unique,
	user_pass		char(32),
	user_addr		varchar(225),
	user_tel		varchar(225),
	user_privilege	smallint,
	user_id 		serial not null,
	primary key(user_id)
);

create table if not exists seller (
    seller_name 		varchar(255),
    seller_addr 		varchar(255),
	user_id 			int not null,
    primary key(user_id),
	foreign key(user_id) references user_info(user_id)
);


create table if not exists inventory (
	inventory_name 	varchar(255),
	inventory_desc 	varchar(255),			
    picture_url		varchar(255),
    inventory_price money,
	inventory_quantity	int,
	category_id 	int,	
	seller_id		int,
    inventory_id 	serial not null,
	primary key(inventory_id),
    foreign key (category_id) references category(category_id),
	foreign key (seller_id) references seller(user_id)
);

create table if not exists customer (
	customer_name 	varchar(255),
    customer_email	varchar(255) unique not null,
    user_id 	int not null,
    primary key(user_id),
	foreign key(user_id) references user_info(user_id)
);


create table if not exists single_order (
    comment_seller	varchar(255),
	deliver_id		varchar(255),
	customer_id		int not null,
	payment_status	smallint not null,
	total_price		int not null,
	order_date		datetime year to fraction default current year to fraction,
    payment_date 	datetime year to fraction,
    last_update 	datetime year to fraction default current year to fraction,
	seller_id		int,
    order_id		serial not null,
    primary key (order_id),
    foreign key (customer_id) references customer(user_id),
	foreign key (seller_id) references seller(user_id)        
);

/* payment_status = {
1.unpaid,	2.paid	3.shipping	4.
cancelled
} */

create table if not exists detail(
	comment_inventory	varchar(255),
	order_id 		int not null,
	inventory_id	int not null,
	quantity		int,
	primary key (order_id, inventory_id),
    foreign key (inventory_id) references inventory(inventory_id),	
	foreign key (order_id) references single_order(order_id)
);
