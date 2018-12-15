# Item Catalog Project

This is the source code implementing the **Item Catalog** Udacity project. Information here relative only for developers and Udacity students.

### DEPENDENCIES

Dependencies can be installed using

    $ pip install dependency_name

###### DEPENDENCIES LIST

-   flask
-   httplib2
-   json
-   requests
-   oauth2client
-   sqlalchemy

### None-Unix user? Then VAGRANT

If you're Windows or Mac system user you may need to install unix environment to setup and use this web application.
You need to install [Vagrant](https://www.vagrantup.com/downloads.html)  and Virtual Machine like [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
Then will have to download FSND virtual machine [here](https://github.com/udacity/fullstack-nanodegree-vm).
Once you get environment setup done follow this instruction to get it up and running...

    $ cd vagrant
    $ vagrant up
    $ vagrant ssh
    $ cd /vagrant/catalogproject

### Get started

before starting browsing the catalog application you will need to install database and dumb some data inside it, this can be done using, first running database setup file `database.py` then running `dumbdata.py` file

      $ python database.py
      $ python dumbdata.py
      $ python application.py

### Data structure

Database contains three main tables:

1.  User
2.  Category
3.  Item

##### User

| Column  | Type   |
| ------- | ------ |
| id      | int    |
| name    | string |
| email   | string |
| picture | string |

##### Category

| Column        | Type     |
| ------------- | -------- |
| id            | int      |
| name          | string   |
| date_modified | datetime |
| user_id       | int      |

#### Item

| Column        | Type     |
| ------------- | -------- |
| id            | int      |
| name          | string   |
| description   | string   |
| date_modified | datetime |
| category_id   | int      |
| user_id       | int      |
