## MENU API
Add food menu for each restaurant. Use endpoints to manipulate with data.

_Note: naming foods is used intentionally for demonstrating plurality of food, not incorrect english_

Stack: Python 3.12, Flask, SQLAlchemy, MySQL (perhaps tested on SQLite)

### Config
Set up your database in `config.py` or export it as environment variables with name `DB_URL`.
For running docker container, set up `DB_URL` in `Dockerfile`.

### Run Docker
`git clone https://github.com/VojtaMarek/menu_api.git`

`cd menu_api`

`docker build -t menu_api .`

### Add curl, in case you need to make http requests from the container
`apt-get update && apt-get install -y curl`

### Use Examples
`curl 0.0.0.0:8000/`

`curl 0.0.0.0:8000/token`

`curl -H "Authorization: Bearer <your-token>" -X PUT http://0.0.0.0:8000/restaurant/new_restaurant_name`

### Run tests from the container
`docker exec -it <container_id> /bin/bash`
`pipenv run pytest`


### Version 
0.1.0 - init
