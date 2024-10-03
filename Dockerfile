FROM python:3.12-slim

# set the working directory in the container
WORKDIR /app

# set db url
# RUN touch menu_api.db
ENV DB_URL=sqlite:///menu_api.db
#EVN DB_URL=mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}

# install system dependencies
COPY Pipfile* ./
RUN pip install pipenv && pipenv install --deploy  --ignore-pipfile

# Copy the /src directory contents into the container at /app
COPY ./src .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# set flask env variables
ENV FLASK_APP=menu_api
ENV FLASK_ENV=production

# run app using gunicorn
CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:5000", "menu_api:app"]
