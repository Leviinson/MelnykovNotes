MelnykovNotes
=============

Objective of the project
---------------------------

#### Objective of the project is to provide user-friendly notes with elements of social interactions.

#### Registration, authentication, authorization will be implemented using social networks or mail with a password. It will also be possible to set up two-factor authentication.

#### The user can expose the board with his tasks so that other users can look and find out is this user free at certain time or no. The tasks can be marked as "public" and "private", and both with boolean parameter "Visibility to others".

#### Difference between "private" and "public" tasks is the ability for other users to see the name and description of created task. Boolean parameter "Visibility to others" means the ability for other users to see the task itself. It follows that users can have a list of friends. This detail allows to pin the tasks of your friends to your board if they are common.

#### A text editor for tasks will be implemented, where it will be possible to implement text selection, inserting hyperlinks, images, emoji, etc.

#### Since all this looks not entirely safe for the user's personal data, only friends will be able to see the user's tasks, and the user will also be able to select a group of friends for whom certain task will be visible.

#### Since it is not always convenient to check upcoming tasks in the browser, integration with the telegram will be implemented, where it will be possible to check the list of your tasks. Auhtentication into the bot will be carried out using re-authorization link in the chat of the bot.

#### Also user will have opportunity to edit his profile: 
* #### Edit username
* #### Edit profile photo
* #### Edit description
* #### Edit e-mail
* #### Change password

#### The password will be reset by confirming the action in the mail + two-factor authentication.


#### So it's time to sum up the sounded functionality.

Functionality
-------------
* ### Registration, authentication, two-factor authentication, authorization.
* ### Resetting a user's password using mail and two-factor authentication.
* ### Editing user profile.
* ### Create, read, update and delete (CRUD) "private" and "public" tasks with boolean parameter "Visibility to others".
* ### Text editor for creating the description for the tasks.
* ### Add or remove friends from friend list.
* ### The ability to share your tasks with others гsing a public task board.
* ### The ability to select group of friends, for whom certain task will be visible.
* ### Integration with telegram-bot.

Entities
--------
* ### User
* ### Task
* ### Task board
* ### Friend list

Estimated technology stack
==========================

* ## Backend
    - ### Python
    - ### PostgreSQL
    - ### Django
    - ### Django REST-framework
    - ### Aiogram for integration with telegram-bot
  
* ## Frontend
    - ### Raw JS    
    - ### CSS
    - ### HTML