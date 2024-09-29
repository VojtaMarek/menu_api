## MENU API
Add food menu for each restaurant. Use endpoints to manipulate with data.

_Note: naming foods is used intentionally for demonstrating plurality of food, not incorrect english_

Stack: Python 3.12, Flask, SQLAlchemy, MySQL (perhaps tested on SQLite)

### Install
`git clone https://github.com/VojtaMarek/menu_api.git`

`pipenv install`

`apt install curl`

### Config
Copy `config.example.py` to `config.py` and fill in all variables.

### Run Example
`pipenv run gunicorn -b 0.0.0.0:8000 src.menu_api:app`

### Use Examples
`curl 0.0.0.0:8000/`

`curl 0.0.0.0:8000/token`


`curl -H "Authorization: Bearer <your-token>" -X PUT http://localhost:5000/restaurant/new_restaurant_name`

### Run tests
`pipenv run python -m pytest`

### Version 
0.1.0 - init
