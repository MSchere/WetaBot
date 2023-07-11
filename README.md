# Wetabot 
Python bot that automatically orders food from https://wetaca.com/carta by selecting the dishes with the best macros.
## Technologies
Project was created with:
* Python 3.10.2
* Selenium 4.8.0

## Usage
Optinally, create a credentials.txt file with your credentials in the following format:
```
name
email
credit card number
credit card expiration date
credit card cvv
```
Install the dependencies and run the script:
```
$ pip install selenium
$ python wetabot.py [browser] [number_of_dishes]
```
Example:
```
$ python wetabot.py firefox 5
```
Supported browsers: **firefox, chrome, edge, opera, safari, phantomjs**