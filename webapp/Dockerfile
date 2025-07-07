FROM python:3.13-slim

ARG SU_PASSWORD
ARG SU_EMAIL
ARG SU_USERNAME

WORKDIR /webapp

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DJANGO_SUPERUSER_PASSWORD=$SU_PASSWORD
ENV DJANGO_SUPERUSER_EMAIL=$SU_EMAIL
ENV DJANGO_SUPERUSER_USERNAME=$SU_USERNAME

WORKDIR /

ENV PYTHONPATH=/:/webapp:/usr/local/lib/python3.13/site-packages

WORKDIR /webapp

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
