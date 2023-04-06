# Flask Restful API

> This project is a RESTful JSON API using Python3/Flask to manage multiple applications and perform operations in 2 different levels of client hierarchy (admin, user).

### Dependencies

This project relies on`<Python 3.11>`, having its backend based on`<Flask / flask_restful /  flask_httpauth>`libraries, the data is persisted in a`<SQLite>`database and the connection between these two important elements is made through`<SQLAlchemy>`ORM. The container runtime for the project is`<Docker>`.

### Database Structure

The first point to discuss in this section is the chosen database technology: to keep this project lightweight and simple, it was decided to use the SQLite database. As this project has three main elements (Users, Applications and Messages), it was necessary to create three tables:

- Apps
- Messages
- Users

These tables were created as classes and can be seen in the models.py file.


## 💻 Application Requirements

The operations, or actions that each hierarchy role can do are explained in the table below:

|  Element/Role | ADMIN   | USER  |
| ------------ | ------------ | ------------ |
| Users  |  Create/Read/Delete | Read/Delete itself  |
|  Apps | Create/Read  | -  |
|  Messages  | Delete  | Post each other  |

Constraints:
* Each endpoint must be authenticated by the user (in the application context) or admin (in the general context)
* Each application is a new context, so one user will not see other user information or messages, only their own;
* Each user belongs to one application, one application user should not be able to see other application's users.

## 🚀 Installation

To install this application, it is necessary to have Docker Compose. If you don't have it, it's recommended to follow Docker's official installation tutorial on this page: `https://docs.docker.com/engine/install/`. Once you have Docker Compose, open your terminal on the same folder you have cloned this repository and run the following command on it to install the Flask Restful API:
```
docker-compose up
```
The installation will begin and when it finish a 'Running on http://127.0.0.1:5000' message will prompt in the console screen, this means the API is up and running.

## ☕ Project Features

### API Routes
The Routes were designed considering the operations requirements so that it could provide the necessary functions to each element. To achieve that, it was necessary to design 4 routes, with 4 main Management classes and its methods:

- ManageUsers class and the "/users/" route
- ManageMessages class and the "/messages/" route
- ManageApps class and the "/app/" route
- SpecificApp class and the "/app/< name >" route

#### ManageUsers
>Methods: GET, POST and DELETE.

This class can show (GET), create (POST) and delete (DELETE) users. According to the table above, it limits the User Role to Create New users, but it can still read and delete itself.
```
To show all the users, simply send a GET request to the route /users/ having any authentication
```
```
To create a new user, it is necessary to send a POST request to the route /users/ having a JSON-body with the following informations: 
* login
* password 
* role
```
```
To delete an existing user, it is necessary to send a DELETE request having a JSON-body with the name of the user to be deleted to the route /users/.
```
##### Tests
The testing of this route can be done using the Postman JSON file of this repository, and it consists of a GET method designed to show the registered users for both roles (user and admin). It is also possible to test the POST method by adding a new user using a pre-built customizable JSON Body, where the tester can try to create a new user having the right credentials and not having it, test some secure rules, such as not creating two users with the same login and typing wrong parameters. It also has a DELETE route, designed to give the admin role the power to delete any user and the user to delete itself only. It can also be tested using Postman to, for example, try to delete an unknow user or trying to do it with the wrong credentials.

#### ManageApps
>Methods: GET and POST.

This class can show all Apps (GET) and create new apps (POST). According to the table above, only the admin can create or see the apps.
```
To show all Apps, it is necessary to be logged as admin and send a GET request to the /app/ route.
```
```
To create a new app, it is necessary to send a POST request to the /app/ route having a JSON-body with the following information:
* name
* context 
The context is the login of the user who is related to the app.
```

##### Tests
It is possible to test this route with Postman too and it consists of a GET method designed to show all the Apps and a POST method designed to create new apps. It is possible to test the limits of the visualization of the Apps for users with the 'user' role and to see create new apps.

#### ManageMessages
>Methods: GET, POST and DELETE.

This class can show only the Messages related to the users and all the Messages if the requester is an admin. This operation is made through a GET method and also implements a concept of relations between the users, as they are able to send messages each other. It is also possible, only for the user role, to send messages to all the registered users on this application using the POST method. The messages can also be deleted by an admin.
```
To show all messages, it is necessary to be logged as admin and send a GET request to the /messages/ route.
```
```
To create a new message, it is necessary to send a POST request to the /messages/ route having a JSON-body with the following information:
* content
* to_user
to_user is the recipient of the message.
```
```
To delete a message, it is only necessary to send a DELETE request to the /messages/ route having the id of the message to be deleted in a JSON-body.
```
##### Tests
It is also possible to test this route with Postman. It provides some different points of view to do a same GET request. It is possible to do it as an admin and two different users. It is also possible to test the messaging rules and also viewing only the messages related to the user who requested it. It is also possible to delete messages using the DELETE method.

#### SpecificApp
>Methods: GET.

This class can show a information about a specific registered App. This can be done by sending a GET request to the /app/name route, where the field was designed to have the App name .

To provide a safe way of using this application, according to the first Constraint, it was also necessary to implement authentication in every route.

### Docker Container and Compose
To ease the installation and interoperability of this application, two main elements was designed: a Dockerfile, to build a docker image from the scripts, and a Docker Compose file, to make it able to be installed with 1 command line. These files can be downloaded from this repository.

## 🤝 Thanks and Acknowledgements

To all the people from Habit who gave me the opportunity to be challenged and learn a lot in this journey!

## 📝 License

This project is licensed under the MIT License.