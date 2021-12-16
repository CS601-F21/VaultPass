# <img src="/VaultPass/VaultPass/static/vault.png" width="50" height="50">  VaultPass


 
VaultPass is a local password manager.


## Instructions

### Clone the repository

`git clone git@github.com:CS601-F21/side-project-anchitbhatia.git`

### Install the requirements

`pip install -r requirements.txt`

### Run the Django server

`python3 VaultPass/manage.py runserver PORT`

Default Port is 8000


## About

### Motivation:
The motivation behind developing VaultPass is to have an easy to use password manager that is hosted locally. The existing cloud based 
password managers are complicated and cluttered with so many multiple use cases. It gets difficult to store and manage passwords for people 
who are not into technology (like my parents). With this project i want to develop a minimal password manager that my parents can use easily.

Also i wanted to learn Django since last few months and therefore decided to use this opportunity.


### Features:
* High priority
  * encrypt and decrypt passwords
  * retrieve and store passwords in database
  * random password generator
  * view and delete passwords
  * set password hint
  * change master password
  * multiple user support
  
* Nice to have priority 
  * better UI
  * email verification
  * identify stored websites with same passwords
  * store notes securely
  * copy password
  * copy username

### Tech stack:
I am using Python and Django framework for the backend and HTML, CSS for the front-end.
