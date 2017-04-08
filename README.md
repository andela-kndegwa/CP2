[![Build Status](https://travis-ci.org/andela-kndegwa/CP2.svg?branch=feature-review)](https://travis-ci.org/andela-kndegwa/CP2)
[![Coverage Status](https://coveralls.io/repos/github/andela-kndegwa/CP2/badge.svg?branch=feature-review)](https://coveralls.io/github/andela-kndegwa/CP2?branch=feature-review)
[![CircleCI](https://circleci.com/gh/andela-kndegwa/CP2/tree/feature-review.svg?style=svg)](https://circleci.com/gh/andela-kndegwa/CP2/tree/feature-review)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]()
[![Kimani Ndegwa](https://img.shields.io/badge/Kimani%20Ndegwa-SecondCheckpoint-orange.svg)]()

# BUCKET LIST API.

>A project done in fulfillment of the second checkpoint of the Andela training program.

# PROJECT OVERVIEW

Before getting into the details of this project, a brief run through of the following concepts is necessary:

1. API

2. REST

3. JSON

**API**

An **API**, acronym for Application Programming Interface, provides a blueprint for how software interacts with each other thus setting the foundation for building great software applications and programs.

**REST**

Throughout, the development of API's, some best practices have come up and thus the advent of REST and RESTFul API development. 
REST is another acronym that refers **RE**presentational **S**tate **T**ransfer and has become the de-facto way of building API's and thus API's using this standard are known as RESTFul API's. The five main principles the implementation of REST and RESTFulness are:

1. Everything is a resource.

2. Every resource is identified by a unique identifier.

3. Use simple and uniform interfaces.

4. Communication are done by representation.

5. Be Stateless.

**JSON**

Yet another acronym, JSON which stands for **J**avascript **O**bject **N**otation, is a light-weight format that facilitates interchange of data between different systems or, case in point, software. It is intended to be universal and thus allows consumption of data by any program regardless of the programming language it is written in. Sample JSON data would be as follows:

```
{
"name":"Blister",
"description":"A RESTFul Bucketlist API",
"author":"Kimani Ndegwa",
}

```
Read more about JSON [here](http://www.json.org/)

These three paradigms are thus what form the basis of how the ***bucketlist service***, BLISTER, was built.

To fully understand how BLISTER works, install the **Google Chrome** extension **Postman** [here](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en)

# SCOPE.

In this exercise, the task was to create a Flask API for a bucket list service. *Specification* for the API is as shown below.

>[Flask](http://flask.pocoo.org/) is a common microframework for the Python programming language.

METHOD | ENDPOINT | FUNCTIONALITY
--- | --- | ---
POST| /auth/login | Logs a user in
POST | /auth/register | Register a user
POST| /bucketlists| Create a new bucket list
GET|  /bucketlists | List all the created bucket lists
GET|  ```/bucketlists/<id>```| Get single bucket list
PUT| ```/bucketlists/<id>```| Update this bucket list
DELETE | ```/bucketlists/<id>```| Delete this single bucket list
POST| ```/bucketlists/<id>/items/```| Create a new item in bucket list
PUT |```/bucketlists/<id>/items/<item_id>```|Update item in bucket list
DELETE |```/bucketlists/<id>/items/<item_id>```| Delete item in bucket list

# INSTALLATION & SET UP.

1. First clone this repository to your local machine using git clone ```https://github.com/andela-kndegwa/CP2.git```

2. Checkout into the **feature-review** branch using ```git checkout feature-review```

3. Create a ***virtual environment*** on your machine using  and install the dependencies via ```pip install -r requirements.txt``` after activating the virtual environment.

>The above steps allow you to get the project to your machine. Next, create the database using migrations and set it up as follows.

1. ```python manage.py db init```

2. ```python manage.py db migrate```

3. ```python manage.py db upgrade```

>Now the project is fully set up with the database in place. Run the following command to get blister running:

```python manage.py runserver```

The server should be running on [http://127.0.0.1:5000] 

# USAGE.

As highlighted earlier, install the **Google Chrome** extension [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en)

Once your up and running with postman, the following steps should get your acquainted with how blister works:

- **Register a user.**

Copy the localhost link plus the **api/v1.0/auth/register** appended to the tail end of the link. i.e:
**http://127.0.0.1:5000/api/v1.0/auth/register**

- Ensure the dropdown to the left of the URL bar is a POST request

- In the body tab on Postman, enter a username and password in JSON format i.e:

```{"username":"demouser", "password":"pass"}```

***Set it by checking on the raw checkbox and clicking on application/json on the text drop down***

![Demo Image](/docs/img/1.png?raw=true)

A successful registeration should return the message:

```Sign Up successful. Please log in.```

- **Login a user.**

This time the link changes to:
**http://127.0.0.1:5000/api/v1.0/auth/login**

- Ensure that the method is a POST request also and log in with the same credentials used to sign up.

```{"username":"demouser", "password":"pass"}```

![Demo Image](/docs/img/2.png?raw=true)

A successful login should return a token such as above, e.g :

```
{
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTA1MDkyOCwiaWF0IjoxNDc5MDQ3MzI4fQ.eyJpZCI6NX0.I7XMV4jKhgczmSil9MwFpogyeDxlFvYc6ObFZTKsLZg"
}
```
Copy only the token as it will be used during the next step.

- **Create a bucketlist**

This project utilizes **Token Based Authentication** to restrict access to certain resources. Absence
of this token with the methods from here will result in a **401: Unauthorized Access** error.

To create a bucketlist, make a **POST** request to the following URI:
**http://127.0.0.1:5000/api/v1.0/bucketlists**.

In the headers tab ensure the following:

>Content-Type ----> application/json

>Authorization ---> **Bearer** eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTA1MDkyOCwiaWF0IjoxNDc5MDQ3MzI4fQ.eyJpZCI6NX0.I7XMV4jKhgczmSil9MwFpogyeDxlFvYc6ObFZTKsLZg

Ensure the ***Bearer*** prefix comes before the token earlier copied.
Give your Bucketlist a title and description and hit send, e.g:

```
{
"title": "Demo bucket list title",
"description":"This is a demo bucket list"
}
```

A successful request should be as follows:

![Demo Image](/docs/img/3.png?raw=true)

To view it you can make a **GET** request to the URI for bucketlists plus the ID of the bucketlists appended:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1**.


- **Update or Delete a bucketlist**

To **UPDATE** a bucketlist, navigate to the full link as stated above i.e:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1** with the method for the URL as **PUT.**

In the body tab, provide your information as follows:

```
{
"description":"This is a demo update for my earlier bucket list"
}
```
A successful update should be as follows:

![Demo Image](/docs/img/4.png?raw=true)

To **DELETE** a bucketlist, navigate to the full link as stated above i.e:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1** with the method for the URL as **DELETE**.

A successful request should return a HTTP 204 status code as follows:

![Demo Image](/docs/img/5.png?raw=true)

- **Creating a bucket list item**

To create a bucketlist item, make sure you have a bucketlist and navigate to the following url:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items** as a **POST** request.

>1 here represents the ID of the bucketlist you want to add items to.

Add your content:

```
{
"title": "Demo bucket list item title",
"description":"This is a demo bucket list item title"
}
```
A successful POST reqeuest should return the following:

![Demo Image](/docs/img/6.png?raw=true)

Make a **GET** request to view the item at the following URI:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1**

- **Updating or deleting a bucket list item**

The format takes the same approach as the bucketlist update or delete with the only difference being the URI:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1**

- **Paginantion and searching bucket lists**

Blister also allows you to paginate bucketlists by adding the **limit** parameter to the URI as follows:

**http://127.0.0.1:5000/api/v1.0/bucketlists?limit=1**

![Demo Image](/docs/img/7.png?raw=true)

Searching is also possible using the **q** parameter as follows:

**http://127.0.0.1:5000/api/v1.0/bucketlists?q=bucket 1**

![Demo Image](/docs/img/8.png?raw=true)


# TESTS.

Blister is configured using **Tox**. Thus use the command:

```
tox
```
will successfully run the tests.

Alternatively, the following nosetests command should also suffice:

```nosetests --with-coverage --cover-package=app```


### Contributors.

1. [Abdulmalik Abdulwahab.](https://github.com/andela-aabdulwahab)

2. [Chukwuerika Dike](https://github.com/andela-cdike)
