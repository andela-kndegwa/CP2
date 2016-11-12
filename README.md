[![Build Status](https://travis-ci.org/andela-kndegwa/CP2.svg?branch=feature-review)](https://travis-ci.org/andela-kndegwa/CP2)
[![Coverage Status](https://coveralls.io/repos/github/andela-kndegwa/CP2/badge.svg?branch=feature-review)](https://coveralls.io/github/andela-kndegwa/CP2?branch=feature-review)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]()
[![Kimani Ndegwa](https://img.shields.io/badge/Kimani%20Ndegwa-SecondCheckpoint-orange.svg)]()

# BUCKET LIST API.

>A project done in fulfillment of the second checkpoint of the Andela training program.

# SCOPE.

In this exercise, the task was to create a Flask API for a bucket list service. *Specification* for the API is as shown below.

METHOD | ENDPOINT | FUNCTIONALITY
--- | --- | ---
POST| /auth/login | Logs a user in
POST | /auth/register | Register a user
POST| /bucketlists| Create a new bucket list
GET|  /bucketlists | List all the created bucket lists
GET|  /bucketlists/<id>| Get single bucket list
PUT| /bucketlists/<id>| Update this bucket list
DELETE | /bucketlists/<id>| Delete this single bucket list
POST| /bucketlists/<id>/items/| Create a new item in bucket list
PUT |/bucketlists/<id>/items/<item_id>|Update item in bucket list
DELETE | /bucketlists/<id>/items/<item_id> | Delete item in bucket list