FROM python:3.10.12

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./alembic.ini /code/alembic.ini
COPY ./.env /code/.env
COPY ./manage /code/manage
COPY ./manage.py /code/manage.py
COPY ./main.py /code/main.py
COPY ./alembic /code/alembic
COPY ./app /code/app

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]