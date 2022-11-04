# T2A2

## Problem identified and why needs to be solved:

---

I am trying to build a web application for the sticker shop. The aim of this app is to provide solutions for the sticker shop to manage the information of their customers, products and orders and reviews. And also allows customers to update their personal information and check their order histories.

### Reasons for building this web application:

* Store Information
  
  At the beginning, a sticker shop might only have a small number of customer, product, order and review. Owner could easily use traditional methods such as excel files or notebooks to store these information. As the shop grows, the number of customers, products, orders and reviews grows as well. These methods could still be used to store information, but the size of excel file will become really big or the owner needs to used lots of notebooks to store these information, which makes these methods inefficient and difficult to use. Therefore, the shop needs new methods to store these information.
 
* Manage Information

  As mentioned above, with small number of information, it is easy to find a particular piece of information and update it. As the number grows, it is hard to locate and update particular information.

* Link Information
  
  A sticker shop needs to link all information together. For example, a reivew needs to be linked to a particular customer and product. With the traditional methods mentioned above, if the owner wants to find the order of a customer, the owner needs to search the customer in the customer file and find out the related review ids. Then use ids to find out the corresponding reviews in the review file. This process is complicated and time consuming.

* Allow customer to manage their own information

  With the traditional methods, customers can not manage and upate their information on their own. They are also not able to check their personal order hisotry. Customers needs to contact the owner to perform these operations, which reduces the customer experiece of the sticker shop.

* Benefits of the app

  With the web app, all of the information are stored in the databse which allows owner to easily manage the information. Customers could also create their own account, update their personal information and check their order history by themselves.

## PostgreSQL and Why

---

I am going to use postgresql for this web application. PostgreSQL is a widely used object-relational database management system for flask applications. It supports both relational and non-relational queries.

### The advantages of the postgresql are:

---

* It supports various data types, such as integer, numeric, string, boolean, geometric types, and non-relational data like JSON and XML. PostgreSQL also supports lots of SQL syntaxes.
* It is highly extensible. Users could extend the database by adding features they need, defining own functions and adding own data types.
* It has good scalability. Developers can use it for either small projects or large applications. When business grows, the software of the company grows as well, which requies the databse extention. With high scalability, postgreSQL supports business growth better. Together with good extensibility, is results in low maintencance.
* It has good security. PostgreSQL not only have features but also have extentions that enhance its security.
* It provides transactional DDL and it is fully acid compliant. Both DDL( data definition language) and DML (data manipulation language) in postgresql are transactional. DDL includes operations such as creating a table, drop a table, etc. DML includes insert, update, etc. A transaction could contains serveral SQL statements(operations). ACID includes atomicity (if one operation within a transaction fails, this transaction fails. The transaction only succeeds if all operations succeed. Then it will apply the changes to the database.), consistency (ensure changes made via a transaction obey the database constraints.), isolation (ensure transactions run in the isolated enviroment. Users could run transactions concurrently without affecting each other.), durability (After the commit, the changes made by the transaction is persist.)
  
  This feature ensures that all data within the database is accurate and consistant with the constraints. It also makes the storage more reliable.
* It implements parallelisation processing of queries, multi-version concurrency control and indexing methods which boost and optimise the performance. This allows users to read and write concurrently.
* It has a high level of conformance with SQL standards. Everyone who familiarise with SQL could easily use it.
* It is compatible with multiple platforms and procedural languages.
* It is reliable and manages data integrity well by introducing constraints. All data within the database must follow the constraints.
* Well documented and has support from communities.
* It is open-source and free.
* It has all RDBMS's features and additional features such as table inheritance.
  
### The disadvantages of the postgresql are:

---

* Compared with non relational based database, users have to define schema, attributes in postgresql first. After this, a object could only store values for these defined attributes, a object could not have values for attributes that not define. All obejcts within the same table have same attributes. Users can not add new fields or attributes to a particular object. Adding new fields or attributes will apply to all objects. While noSQL database allows different objects haveing different attributes.
* Slower reading speed compared with MySQL. PostgreSQL has to read from the first row and then go through each row of the table in order to find the data. This results in relatively slow reading speed compared with other databases.
* It does not implement replication well. Users need to export or replicate data to the new version.
  
## Functionalities and benefits of ORM

---

## What is an ORM

---
Object-realtional mapping (ORM) works between the application and the relational database. ORM converts data between these two systems, which allows developers to devlop databse, query and manipulate data within dabase by using the object-oriented programming languages.

## Functionalities

---

* Link the application and the relational database
  Developers could use the ORM together with database adapter to connect the application and the relational database. For example, developers could user SQLalchemy(ORM) and psycopy2(PostgreSQL database adapter) to connect the flask application and postgresql databse. And then create a database object that allows developers to use build in methods of the ORM in the following code to create model and perform different operations.
* Create Models
  Once the connection established, developers could use the ORM to define models. Models are defined as class, it represents a table in the database. Each object of the model class represents a record or row in the database. The attributes within the model class represents fields in the database, each attributes provides the name, data type and constraints of each fields.
* CLI commands
  Once models are created, developers can use the CLI commands functions from the ORM to perform serveral operations which is similar to the DDL commands in the SQL term. 
  
  These operations includes creating tables via flask create, which create all tables based on the models defined in the application.

  Create object or rows in the database via flask seed. Developers create objects of the model class, then add and commit the changes to the databse. 

  Drop the table via flask drop.

* CRUD
  The ORM create SQL statements for the developers and allows the developers to create new records of the table, read selected records, update or delete particular records. It will convert the programming language that users wrote to the SQL commands. The ORM also need another package called Marshmallow, which serialize data to allow flask to be able to convert it into JSON format and deserialize objects from JSON format to a python dict. The ORM and marshmallow package works together to allow developers to manipulate databse by writing object oriented programming languages instead of plain SQL statement.

## Benefits

---

* ORM is independent of the database. Its high level implementation supports database connections and migrations. If change the databse from one to another, the code might be the same or only need a small number of changes.
* Developers could use familarised object-oriented programming languages to develop database, query and manipulate data. It is helpful for those who are not good at SQL.
* ORM will handle the CRUD operations. As developers do not need to write tedious and repetitive SQL, developers could focus on the logic of the application(model), and write cleaner, less number of code. This is also time consuming.
* Developers is able to develop a class library to create a standalone DLL, which can be used for other applications.
* ORM is simple to implement, it uses a visual modeling process for object-to-table and table-to-object, which makes it easy to maintain and simple to use.
* The code of ORM has been tested, no need to test again, allows developers to save time and focus on testing the code of business logic.
* ORM prevents SQL injection better because queires are sanitised.





Ref:

* https://circle.visual-paradigm.com/docs/code-engineering/object-relational-mapping/
* https://www.keboola.com/blog/acid-transactions


  