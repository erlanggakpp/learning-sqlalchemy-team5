# Use an official Python runtime as a parent image
# FROM --platform=linux/amd64 python:3.12-slim
FROM python:3.12-slim

RUN mkdir -p /app
WORKDIR /app

COPY ./src /app/
RUN rm -rf .venv
RUN pip install -U pipenv
RUN pipenv install --deploy

# Set environment variables
# ENV FLASK_ENV=production
ENV SECRET_KEY=ANGGA
ENV API_KEY=TEAM5

EXPOSE 8080
CMD [ "pipenv", "run", "gunicorn",  "--bind",  "0.0.0.0:8080", "app:app"]

# Command to run the Flask application
# CMD ["python3", "app.py"]

# docker build -t nba_teams_api_gunicorn .
# docker run -p 5005:5000 'nba_teams_api_gunicorn'