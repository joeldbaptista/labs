
drop table if exists customers;
create table customers as
select * from read_json('outs/customers.json');

drop table if exists employees;
create table employees as
select * from read_json('outs/employees.json');

drop table if exists products;
create table products as
select * from read_json('outs/products.json');

drop table if exists orders;
create table orders as
select * from read_json('outs/orders.json');

drop table if exists order_product;
create table order_product as
select * from read_json('outs/order_product.json');

