create table if not exists category (
	category_title 	varchar(255),
    category_desc 	text,				
    category_id 	serial not null,
	primary key(category_id)
);

create table if not exists item (
	item_name 		varchar(255),			
    category_id 	bigint unsigned ,
    item_id 		serial not null,
									
    primary key(item_id),
    constraint category_id_item foreign key (category_id) references category(category_id)
);

create table if not exists seller (
    seller_name 		varchar(255),
    seller_addr 		text,
    seller_city 		varchar(255),
    owner_id 		int,					
    seller_id 		serial not null,
    primary key(seller_id)
);

create table if not exists inventory (
    item_id 		bigint unsigned not null,
    inventory_price decimal(5,2),
	inventory_desc 	text,			
    main_picture_url	text,			
    inventory_id 	serial not null,
    last_update		timestamp,
	primary key(inventory_id),
    constraint item_id_inventory foreign key (item_id) references item(item_id)
);

create table if not exists customer (
    customer_name 	varchar(255),
    customer_email	varchar(255) unique,
    customer_id 	serial not null,
    primary key(customer_id)
);

create table if not exists private_sheet (
	customer_id		bigint unsigned not null,
    username 		varchar(255),
    password_md5 	char(32) not null,
	primary key(customer_id),
    constraint customer_id_private foreign key (customer_id) references customer(customer_id)
);

create table if not exists package (	
    inventory_id	bigint unsigned not null,
    package_id 		serial not null,
    primary key(package_id, inventory_id),
    constraint inventory_id_package foreign key (inventory_id) references inventory(inventory_id)
);

create table if not exists single_order (
    customer_id		bigint unsigned not null,
    inventory_id	bigint unsigned not null,
    quantity		tinyint default 1,
    discount_ratio	decimal(5,2) default 1.00,		
    discount_sub	decimal(5,2) default 0.00,	
    order_date		datetime,
    payment_date 	datetime,
    payment_status	enum('unpaid','paid','shipping','arrived','received','returning','refunded'),		
    last_update 	timestamp,
    deliver_id		int unsigned,					
    comment_inventory	text,
    comment_seller		text,
    order_id		serial not null,
    primary key(order_id),
    constraint inventory_id_sorder foreign key (inventory_id) references inventory(inventory_id),			
    constraint customer_id_sorder foreign key (customer_id) references customer(customer_id)
    
);

create table if not exists package_order (
    customer_id		bigint unsigned not null,
    package_id		bigint unsigned not null,
    quantity		tinyint default 1,
    discount_ratio	decimal(5,2) default 1.00,		
    discount_sub	decimal(5,2) default 0.00,	
    order_date		datetime,
    payment_date 	datetime,
    payment_status	enum('unpaid','paid','shipping','arrived','received','returning','refunded'),		
    last_update 	timestamp,
    deliver_id		int unsigned,					
    comment_package		text,
    comment_seller		text,
    order_id		serial not null,
    primary key(order_id),
    constraint package_id_porder foreign key (package_id) references package(package_id),			
    constraint customer_id_porder foreign key (customer_id) references customer(customer_id)
);
