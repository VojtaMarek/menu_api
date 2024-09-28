## MENU API
Add food menu for each restaurant. Use endpoints to manipulate with data.

Stack: Python 3.12, Flask, SQLAlchemy, MySQL (perhaps tested on SQLite)

### Install
`git clone https://github.com/VojtaMarek/menu_api.git`

`pipenv install`

`apt install curl`

### Config
Copy `config.example.py` to `config.py` and fill in all variables.

### Run Example
`pipenv run gunicorn -b 127.0.0.1:5000 src.menu_api:app`

### Use Examples
`curl 127.0.0.1:5000/version`

..

### Version 
0.1.0 - init
