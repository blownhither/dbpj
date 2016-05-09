create table if not exists category (
	category_title 	varchar(255),
    category_desc 	text,				#description
    category_id 	smallint auto_increment not null,
	primary key(category_id)
);

create table if not exists item (
	item_name 		varchar(255),			# notes: varchar stores up to 255B for safe Chinese usage, use text otherwise
    category_id 	smallint ,
    item_id 		int auto_increment not null,
									# maybe other attributes
    primary key(item_id),
    constraint category_id_item foreign key (category_id) references category(category_id)
);

create table if not exists seller (
    store_name 		varchar(255),
    store_addr 		text,
    store_city 		varchar(255),
    owner_id 		int,					# this ought to be personal identity id
    store_id 		int auto_increment not null,
    primary key(store_id)
);

create table if not exists inventory (
    item_id 		int not null,
    inventory_price decimal(5,2),
	inventory_desc 	text,			# description
    main_picture_url	text,			# normally used as preview photo
    inventory_id 	int auto_increment not null,
    last_update		timestamp,
	primary key(inventory_id),
    constraint item_id_inventory foreign key (item_id) references item(item_id)
);

create table if not exists customer (
    customer_name 	varchar(255),
    customer_email	varchar(255),
    customer_id 	int auto_increment not null,
    primary key(customer_id)
);

create table if not exists private_sheet (
	customer_id		int not null,
    username 		varchar(255),
    password_md5 	char(32) not null,
	primary key(customer_id),
    constraint customer_id_private foreign key (customer_id) references customer(customer_id)
);

create table if not exists package (	# multiple entry for one package
    inventory_id	int not null,
    package_id 		int auto_increment not null,
    primary key(package_id, inventory_id),
    constraint inventory_id_package foreign key (inventory_id) references inventory(inventory_id)
);

drop table if exists single_order;
create table if not exists single_order (
    customer_id		int not null,
    inventory_id	int not null,
    quantity		tinyint default 1,
    discount_ratio	decimal(5,2) default 1.00,		
    discount_sub	decimal(5,2) default 0.00,	
    order_date		datetime,
    payment_date 	datetime,
    payment_status	enum('unpaid','paid','shipping','arrived','received','returning','refunded'),		# check
    last_update 	timestamp,
    deliver_id		int unsigned,					# need constraint
    comment_inventory	text,
    comment_seller		text,
    order_id		int auto_increment not null,
    primary key(order_id),
    constraint inventory_id_sorder foreign key (inventory_id) references inventory(inventory_id),			# should not duplicate contr
    constraint customer_id_sorder foreign key (customer_id) references customer(customer_id)
    
);

create table if not exists package_order (
    customer_id		int not null,
    package_id		int not null,
    quantity		tinyint default 1,
    discount_ratio	decimal(5,2) default 1.00,		
    discount_sub	decimal(5,2) default 0.00,	
    order_date		datetime,
    payment_date 	datetime,
    payment_status	enum('unpaid','paid','shipping','arrived','received','returning','refunded'),		# check
    last_update 	timestamp,
    deliver_id		int unsigned,					# need constraint
    comment_package		text,
    comment_seller		text,
    order_id		int auto_increment not null,
    primary key(order_id),
    constraint package_id_porder foreign key (package_id) references package(package_id),			# should not duplicate contr
    constraint customer_id_porder foreign key (customer_id) references customer(customer_id)
);

### sample data ###


load data infile 

#show char set;						# available character sets
#show variables; 					# make sure utf-8 is used at all the place

#notes:
#note that decimal in Workbench works as ()
