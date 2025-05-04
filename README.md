# INTRO_SE_SP_2025
Introduction to Software Engineering Spring 2025 MSU
E-Commerce Platform Project
Team Member: Nathan Jones - NetID: ndj4, GITHUB: n8dog73, email: ndj4@msstate.edu
Roles: Project Manageer, Developer, Tester, and Editor. 

Project Description:
The E-Commerce Platform is a web application that will allow users to search, compare, buy and return different types of products from different sellers.  The platform will allow multiple sellers to sell their products on a platform that will reach many customers.  The customers will be able to search an abundant different products from their web browser.  Users, sellers, and administrators of the system will be able to access the system and components they wish from ease from a web browser. 

Objectives:
The E-Commerce Platform is a new system that developed from the ground up. Users will access the web interface to search for products from multiple sellers.  The sellers will have a separate web interface to add, sell, and receive payments. The administrators of the website will have a separate web interface to approve or block new user accounts and products as well as oversee other user actions. 

5/4/2025
System Setup:
1. Create an Ecommerce_db mysql database.  The database will be controlled by the python scripts created in teh Django project, ecommerce
2. Start the MySQL database by running 'sudo service mysql start'
3. Check status of the mysql database running 'sudo service mysql status'
4. cd to ecommerce/
5. Migrate classes to create the Ecommerce_db database by performing the following:
    5.1. python manage.py makemigrations
    5.2. python manage.py migrate.
6. The Ecommerce_db should have database tables created by perfoming the above.
7. Run python manage.py runserver to start the E-Commerce Platform server. 

