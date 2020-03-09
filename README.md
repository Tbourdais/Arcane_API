# ARCANE - API

## Database
### Database choice

I had to work on a MongoDB database with PyMongo 3 weeks ago for an internship test, so I've decided to use this kind of database for the case study (I had also saw in Flask tutorials that MongoDB databases were quite straightforward to manage with Flask).

### Database description

The database is composed of two collections :  
- **users** : this collection coontains the users information. Each user is represented by his first and last names and his birth date. At the creation of a user, a unique "_id" is automatically added to these information.  
- **real_estates** : this collection contains all the real estates. A real estate is represented by the *owner_id*, the *owner* first and last names, the type of the estate, the *rooms* organisation (how many rooms per type), the *city* it is located in and a *description*. When a customer adds a real estate, a unique "_id" field is automatically added.

## API

I didn't comment too much the api.py file. Here are some precision on some the app routes.

### /users/<user_id>, PUT

Update the user's info. Only the fields in the request are modified.

### /users/<user_id>, DELETE

Remove the user with *user_id* from the database. This also removes all the real estates posted by the user from the database.

### /real_estates/<user_id>/<estate_id>, PUT

Update the info of the real estate with *estate_id* if and only if *user_id* and *owner_id* matches. Only the fields in the request are modified.

## Instructions

1 - Download and install the MongoDB community server ([link](https://www.mongodb.com/download-center/community)).  
2 - Create a Python 3 environment with **Pandas**, **NumPy**, **PyMongo** and **Flask** installed.  
3 - If you want to generate a test database, uncomment the line 6 in **api.py**.  
4 - Run the **api.py** file in your Python environment. 
