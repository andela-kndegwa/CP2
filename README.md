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

2. Checkout into the **feature-review** branch using ```git checkout develop```

3. Create a ***virtual environment*** on your machine using  and install the dependencies via ```pip install -r requirements.txt``` after activating the virtual environment.

>The above steps allow you to get the project to your machine. Next, create the database using migrations and set it up as follows.

1. ```python manage.py db init```

2. ```python manage.py db migrate```

3. ```python manage.py db upgrade```

>Now the project is fully set up with the database in place. Run the following command to get blister running:

```python manage.py runserver```

The server should be running on [http://12.0.0.1:5000] 

# USAGE.

As highlighted earlier, install the **Google Chrome** extension [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en)

Once your up and running with postman, the following steps should get your acquainted with how blister works:

1. Register a user.

Copy the localhost link plus the **api/v1.0/auth/register** appended to the tail end of the link. i.e:
**http://12.0.0.1:5000/api/v1.0/auth/register**

- Ensure the dropdown to the left of the URL bar is a POST request

- In the body tab on Postman, enter a username and password in JSON format i.e:

```{"username":"demouser", "password":"pass"}```

***Set it by checking on the raw checkbox and clicking on application/json on the text drop down***

![Demo Image](/docs/img/1.png?raw=true)


