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
    customer_email	varchar(255) unique,
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

create table if not exists detail(
	comment_inventory	varchar(255),
	order_id 		int not null,
	inventory_id	int not null,
	quantity		int,
	primary key (order_id, inventory_id),
    foreign key (inventory_id) references inventory(inventory_id),	
	foreign key (order_id) references single_order(order_id)
);

insert into category values('Video','Digital Video',0);insert into category values ('Music','Digital & Prime Music',0);insert into category values ('App','Appstore',0);insert into category values ('Cloud','Cloud Drive Service',0);insert into category values ('EBook','E-readers & Books',0);insert into category values ('EverydayFresh','Fresh Food & Health Care',0);insert into category values ('Book','Books',0);insert into category values ('Movies','Movies',0);insert into category values ('Games','Games',0);insert into category values ('Electronics','Electronics',0);insert into category values ('Household','Household',0);insert into category values ('Health','Beauty Health & Grocery',0);insert into category values ('Toys','Toys Kids & Baby',0);insert into category values ('Clothing','Clothing Shoes & Jewelry',0);insert into category values ('Sports','Sports & Outdoors',0);insert into category values ('Industrial','Automotive & Industrial',0);insert into category values ('Handmade','Handmade',0);insert into category values ('Services','Services',0);

insert into user_info values ('Username1','password',1,0);insert into user_info values ('Username2','password',1,0);insert into user_info values ('Username3','password',1,0);insert into user_info values ('Username4','password',1,0);insert into user_info values ('Username5','password',1,0);insert into user_info values ('Username6','password',1,0);insert into user_info values ('Username7','password',1,0);insert into user_info values ('Username8','password',1,0);insert into user_info values ('Username9','password',1,0);insert into user_info values ('Username10','password',2,0);insert into user_info values ('Username11','password',2,0);insert into user_info values ('Username12','password',2,0);insert into user_info values ('Username13','password',2,0);insert into user_info values ('Username14','password',2,0);insert into user_info values ('Username15','password',2,0);insert into user_info values ('Username16','password',2,0);insert into user_info values ('Username17','password',2,0);insert into user_info values ('Username18','password',2,0);insert into user_info values ('Username19','password',2,0);insert into user_info values ('maziyin','maziyin',0,0);insert into user_info values ('chenkan','chenkan',0,0);insert into user_info values ('shengyutao','shengyutao',0,0);
insert into seller values ('Seller0','Shanghai',0);insert into seller values ('Seller1','Shanghai',1);insert into seller values ('Seller2','Shanghai',2);insert into seller values ('Seller3','Shanghai',3);insert into seller values ('Seller4','Shanghai',4);insert into seller values ('Seller5','Shanghai',5);insert into seller values ('Seller6','Shanghai',6);insert into seller values ('Seller7','Shanghai',7);insert into seller values ('Seller8','Shanghai',8);insert into seller values ('Seller9','Shanghai',9);
insert into customer values ('Customer10','public10@customer.cn',10);insert into customer values ('Customer11','public11@customer.cn',11);insert into customer values ('Customer12','public12@customer.cn',12);insert into customer values ('Customer13','public13@customer.cn',13);insert into customer values ('Customer14','public14@customer.cn',14);insert into customer values ('Customer15','public15@customer.cn',15);insert into customer values ('Customer16','public16@customer.cn',16);insert into customer values ('Customer17','public17@customer.cn',17);insert into customer values ('Customer18','public18@customer.cn',18);insert into customer values ('Customer19','public19@customer.cn',19);

insert into inventory values('MacBook',				NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_macbook_opt_large.jpg',9288,100,10,1,0);
insert into inventory values('MacBook Air 11-inch',	NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_macbook_air_11_large.jpg',6288,100,10,1,0);
insert into inventory values('MacBook Air 13-inch',	NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_macbook_air_13_large.jpg',6988,100,10,1,0);
insert into inventory values('MacBook Pro 13-inch',	NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_macbook_pro_13_large.jpg',7788,100,10,1,0);
insert into inventory values('MacBook Pro 13-inch Retina',NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_macbook_pro_retina_13_large.jpg',9288,100,10,1,0);
insert into inventory values('MacBook Pro 15-inch',	NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_macbook_pro_retina_15_large.jpg',14288,100,10,1,0);
insert into inventory values('iMac 21.5-inch',		NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_imac_retina_21_large.jpg',7988,100,10,1,0);
insert into inventory values('iMac 21.5-inch Retina',NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_imac_retina_21_large.jpg',10988,100,10,1,0);
insert into inventory values('iMac 27-inch Retina',	NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_imac_retina_27_large.jpg',13488,100,10,1,0);
insert into inventory values('Mac mini',				NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_mac_mini_large.jpg',3588,100,10,1,0);
insert into inventory values('Mac Pro',				NULL,'http://images.apple.com/v/mac/compare/d/results/images/results_product_mac_pro_large.jpg',2188,100,10,1,0);
