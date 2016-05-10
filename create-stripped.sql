drop table if exists single_order;
drop table if exists customer;
drop table if exists inventory;
drop table if exists seller;
drop table if exists user_info;
drop table if exists item;
drop table if exists category;
drop table if exists detail;

create table if not exists category (
	category_title 	varchar(255),
    category_desc 	text,				
    category_id 	serial not null,
	primary key(category_id)
);

create table if not exists user_info (
	user_name		varchar(225),
	user_pass		char(32),
	user_id 		serial not null,
	user_privilege	smallint,
	primary key(user_id)
);

create table if not exists seller (
	seller_id 			int not null,
    seller_name 		varchar(255),
    seller_addr 		text,
    primary key(seller_id),
	foreign key(seller_id) references user_info(user_id)
);


create table if not exists inventory (
	inventory_name 	varchar(255),
    inventory_price money,
	inventory_desc 	text,			
    picture_url		text,
	inventory_quantity	int,
	category_id 	int,	
	seller_id		int,
    inventory_id 	serial not null,
	primary key(inventory_id),
    foreign key (category_id) references category(category_id),
	foreign key (seller_id) references seller(seller_id)
);

create table if not exists customer (
    customer_id 	int not null,
    customer_name 	varchar(255),
    customer_email	varchar(255) unique,
    primary key(customer_id),
	foreign key(customer_id) references user_info(user_id)
);


create table if not exists single_order (
    customer_id		int not null,
	payment_status	smallint,
    deliver_id		varchar(255),					
	order_date		datetime year to fraction,
    payment_date 	datetime year to fraction,
    last_update 	datetime year to fraction,
	seller_id		int,
    order_id		serial not null,
    primary key (order_id),
    foreign key (customer_id) references customer(customer_id),
	foreign key (seller_id) references seller(seller_id)        
);

create table if not exists detail(
	order_id 		int not null,
	inventory_id	int not null,
	quantity		int,
	comment_inventory	text,
    comment_seller		text,
    foreign key (inventory_id) references inventory(inventory_id),	
	foreign key (order_id) references single_order(order_id)
);