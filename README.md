# CS50 Final Project - Notes

### Video Demo: <https://www.youtube.com/watch?v=YpOgBwHMkUU>

### Description:

Hello, my name is Sourov. This is my cs50 final project "Notes". With this web app you can add notes daily as many as you need, you can find notes of a spacific day also edit and delete them. Every note you write is of "Unlisted" visibility so you can share them with your friends if you want. You can also add, remove and check todos to keep track of your doings.

Technologies used:

- python
- flask
- flask_paginate
- werkzeug
- Bootstrap
- sqlite3
- other small libraries or packages

## How the webpage works?

Frist time you navigate to this website, you need to register as a user. During registration you need to enter these fields:

- UserName: it is checked this field can'n be empty
- Password: it is checked to match, must be at least 6 symbols long and is hashed after checks are done
- Password Conformation: in order to register you the password and the conformation password must match.

you will be automaticly redirect to the homepage after registration. in intial stage homepage will be empty. but in navbar you will notice navigation to features like Notes and Todos. You can navigate to any of them of your choice.

in My Note page you can add new notes. view all of your older notes.
you can filter notes by date. you can also edit and remove the notes. if your note is too big full note will not be visible to view full note you have to navigate to see full button.

in ToDos page you can add small todos mark as done after done also delete when no need.

### Routing

Each route checks if the user is authenticated. It means notes and todos of every individual is protected. For example if you are loged in as "user_1" you can not edit or delete user_2's notes. however you will be able to view others note if he/she share notes link with you.

### Sessions

The webpage uses sessions to confirm that user is registered. Once the user logins, his credentials are checked with werkzeug. Once everything passes a session is created stored in the cookies.

### Database

Database stores all users, all notes, all todos and all reletions among them. notes and todo tables use user_id as foreign key.that make sure user always get correct response.

## Possible improvements

As all applications this one can also be improved. Possible improvements:

- Ability to change account details.
- Add reminder system to todos that will send Notificaitons and email to user about todos.
